#!/usr/bin/env python3
"""GG Club 스냅샷 → 내 구단 원장 반영 (2026-09-19 신설, 사용자 지시 「싱크했어 스쿼드 업데이트」).

왜: fut.gg GG Club은 **EA 구단의 현재 상태**(보유 아이템·현재 능력치·적용한 케미 스타일·진화 진행 플래그)를 준다.
    우리 원장(fut_club_players)은 「내가 무엇을 했는가」를 담고, 이 스크립트가 둘을 맞춘다.

⛔ 자동 수집이 아니다. 사용자가 fut.gg에 로그인하고 「Sync Club」을 누른 뒤, 브라우저에서 읽은 응답을
   JSON으로 넘겨 적재한다(로그인·싱크 대행 금지 — CLAUDE.md 운영 규칙).

입력 JSON: [{"gg","ea","base","n","ovr","six":[6],"cs","cp","ip","evo","boost","added","paid"}, ...]
  cs = EA 케미 스타일 소모품 id(250 Basic … 273 GK Basic) — fc_chemistry_styles.ea_id와 대조한다.

⭐ 하는 일
  ① 없는 선수는 보유로 추가(카드 표에 있으면 player_id·이름을 붙인다)
  ② 있는 선수는 **현재 OVR·6대 스탯·케미 스타일·개인 케미**를 갱신하고 synced_at을 찍는다
  ③ 원장 값과 EA 값이 **어긋나면 경고로 보고**한다 — 조용히 덮지 않는다(진화 기록이 사실과 다르다는 신호다)
  ④ EA에 없는 보유 행은 **자동으로 팔았다고 처리하지 않는다** — 목록만 내고 사람이 판단한다

사용:
    .venv/bin/python scripts/fut_club_sync.py /tmp/ggclub.json --account main
    .venv/bin/python scripts/fut_club_sync.py /tmp/ggclub.json --account main --dry-run
"""
import argparse
import datetime as dt
import json
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from core import DB                                     # noqa: E402

TODAY = dt.date.today().isoformat()
SIX_K = ["PAC", "SHO", "PAS", "DRI", "DEF", "PHY"]
GK_SIX_K = ["DIV", "HAN", "KIC", "REF", "SPD", "POS"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--account", required=True)
    ap.add_argument("--pulled", default=TODAY)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    acc = con.execute("SELECT * FROM fut_accounts WHERE name=?", (a.account,)).fetchone()
    if not acc:
        raise SystemExit(f"⛔ 계정 '{a.account}' 없음")
    rows = json.load(open(a.path, encoding="utf-8"))
    styles = {r["ea_id"]: r["name"] for r in con.execute("SELECT ea_id, name FROM fc_chemistry_styles WHERE ea_id IS NOT NULL")}
    have = {r["ea_item_id"]: dict(r) for r in
            con.execute("SELECT * FROM fut_club_players WHERE account_id=?", (acc["id"],))}
    cards = {r["ea_item_id"]: dict(r) for r in
             con.execute("SELECT ea_item_id, player_id, name_kr, best_pos FROM player_card_items WHERE game_version='FC27'")}

    ins = upd = same = 0
    conflicts, applied_styles = [], []
    for r in rows:
        card = cards.get(r["ea"]) or {}
        gk = (card.get("best_pos") == "GK")
        six = json.dumps(dict(zip(GK_SIX_K if gk else SIX_K, r["six"])), ensure_ascii=False)
        style = styles.get(r.get("cs"))
        if style and style not in ("Basic", "GK Basic"):
            applied_styles.append((card.get("name_kr") or r["n"], style, r.get("cp")))
        cur = have.get(r["ea"])
        if not cur:
            con.execute("""INSERT INTO fut_club_players(account_id, player_id, ea_item_id, name, acquired, acquired_how,
                             status, current_ovr, current_six, chem_style_ea, chem_points, gg_player_id, synced_at,
                             notes, updated)
                           VALUES(?,?,?,?,?,?,'owned',?,?,?,?,?,?,?,?)""",
                        (acc["id"], card.get("player_id"), r["ea"], card.get("name_kr") or r["n"], r.get("added"),
                         "GG Club 싱크", r["ovr"], six, r.get("cs"), r.get("cp"), r.get("gg"), a.pulled,
                         f"gg-club {r.get('gg')} · {r['ovr']} · 구매가 {r.get('paid')} ({a.pulled} 싱크)", TODAY))
            ins += 1
            continue
        # ③ 어긋남 검출 — 원장이 기록한 현재 OVR과 EA 실제값이 다르면 보고한다(진화 기록 오류 신호)
        if cur["current_ovr"] is not None and cur["current_ovr"] != r["ovr"]:
            conflicts.append((cur["name"], cur["current_ovr"], r["ovr"], cur["evo_count"]))
        changed = (cur["current_ovr"] != r["ovr"] or cur["current_six"] != six
                   or cur["chem_style_ea"] != r.get("cs") or cur["chem_points"] != r.get("cp"))
        con.execute("""UPDATE fut_club_players SET current_ovr=?, current_six=?, chem_style_ea=?, chem_points=?,
                         gg_player_id=?, synced_at=?, updated=? WHERE id=?""",
                    (r["ovr"], six, r.get("cs"), r.get("cp"), r.get("gg"), a.pulled,
                     TODAY if changed else cur["updated"], cur["id"]))
        upd += changed
        same += (not changed)

    gone = [v["name"] for k, v in have.items() if v["status"] == "owned" and k not in {x["ea"] for x in rows}]
    if a.dry_run:
        con.rollback()
    else:
        con.commit()

    print(f"{'(dry-run) ' if a.dry_run else ''}싱크 {len(rows)}장 · 신규 {ins} · 갱신 {upd} · 변화 없음 {same}")
    if applied_styles:
        print("\n적용된 케미 스타일:")
        for n, s, cp in applied_styles:
            print(f"   {n:<16} {s:<10} 개인 케미 {cp}")
    if conflicts:
        print("\n⚠️ 원장 ↔ EA 불일치 — 진화 기록을 다시 봐야 한다:")
        for n, mine, ea, ec in conflicts:
            print(f"   {n:<16} 원장 {mine} ↔ EA {ea} (원장 진화 {ec}회)")
    if gone:
        print(f"\n원장에는 보유인데 EA 구단에 없음 {len(gone)}명 — **자동으로 처분 처리하지 않는다**: {', '.join(gone)}")
    print("\n다음: python3 scripts/export.py && scripts/db_dump.sh")


if __name__ == "__main__":
    main()
