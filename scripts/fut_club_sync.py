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
    ap.add_argument("--force-overwrite", action="store_true",
                    help="진화 선수 보호를 해제하고 EA 값으로 전부 덮는다(진화 기록이 틀렸다고 확정했을 때만)")
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
    # ⛔⛔ 진화 보호(2026-09-21 신설, 사용자 지시 「진화 선수들은 싱크 시 덮이지 않도록」).
    #    fut.gg는 EA 싱크를 눌러야 갱신되므로 **우리 원장보다 낡을 수 있다**. 그 상태로 덮으면
    #    방금 기록한 진화가 통째로 되돌아간다(실증: 지모알로바 78 → 73).
    #    ⇒ 진화 로그가 있는 선수는 **EA 값이 원장보다 낮을 때만** 스탯을 보호한다.
    #       (EA가 더 높으면 fut.gg가 최신이라는 뜻이므로 그대로 받는다 — 진화 완주 반영 경로를 막지 않는다.)
    #    ⚠️ 보호는 `current_ovr`·`current_six`에만 건다. 케미 스타일·개인 케미는 진화와 무관하고
    #       EA가 정본이라 항상 갱신한다.
    evolved = {r["club_player_id"] for r in
               con.execute("""SELECT DISTINCT club_player_id FROM fut_evolution_log
                              WHERE COALESCE(is_void,0)=0""")}
    cards = {r["ea_item_id"]: dict(r) for r in
             con.execute("SELECT ea_item_id, player_id, name_kr, best_pos FROM player_card_items WHERE game_version='FC27'")}
    # ⭐⭐ ① PlayStyle은 숫자 id로 온다 — 이름표 정본은 `fc_playstyle_ids`(scripts/collect_playstyle_ids.py).
    #    ⛔ 이름을 여기서 짓지 않는다. 표에 없는 id는 **그대로 두지 않고 보고**한다(조용히 흘리면 못 본다).
    ps_name = {r["ea_id"]: r["name"] for r in
               con.execute("SELECT ea_id, name FROM fc_playstyle_ids WHERE game_version='FC27'")}
    ps_unknown = set()

    def ps_text(r):
        """EA 실측 PlayStyle id 배열 → 원장 표기('Tiki Taka, Inventive+'). 안 왔으면 None(=덮지 않음)."""
        if not isinstance(r.get("ps"), list) and not isinstance(r.get("psp"), list):
            return None
        out = []
        for ids, suffix in ((r.get("ps") or [], ""), (r.get("psp") or [], "+")):
            for i in ids:
                if i in ps_name:
                    out.append(ps_name[i] + suffix)
                else:
                    ps_unknown.add(i)
        return ", ".join(out)

    ins = upd = same = 0
    conflicts, applied_styles, done, protected, ps_fixed = [], [], [], [], []
    stats_n = 0
    for r in rows:
        card = cards.get(r["ea"]) or {}
        gk = (card.get("best_pos") == "GK")
        six = json.dumps(dict(zip(GK_SIX_K if gk else SIX_K, r["six"])), ensure_ascii=False)
        style = styles.get(r.get("cs"))
        if style and style not in ("Basic", "GK Basic"):
            applied_styles.append((card.get("name_kr") or r["n"], style, r.get("cp")))
        cur = have.get(r["ea"])
        if not cur:
            attrs_json = json.dumps(r["attrs"], ensure_ascii=False) if r.get("attrs") else None
            rp_json = json.dumps(r["rp"]) if isinstance(r.get("rp"), list) else None
            rpp_json = json.dumps(r["rpp"]) if isinstance(r.get("rpp"), list) else None
            con.execute("""INSERT INTO fut_club_players(account_id, player_id, ea_item_id, name, acquired, acquired_how,
                             status, current_ovr, current_six, current_attrs, current_roles_plus,
                             current_roles_plus_plus, chem_style_ea, chem_points, gg_player_id, synced_at, notes, updated)
                           VALUES(?,?,?,?,?,?,'owned',?,?,?,?,?,?,?,?,?,?,?)""",
                        (acc["id"], card.get("player_id"), r["ea"], card.get("name_kr") or r["n"], r.get("added"),
                         "GG Club 싱크", r["ovr"], six, attrs_json, rp_json, rpp_json,
                         r.get("cs"), r.get("cp"), r.get("gg"), a.pulled,
                         f"gg-club {r.get('gg')} · {r['ovr']} · 구매가 {r.get('paid')} ({a.pulled} 싱크)", TODAY))
            ins += 1
            continue
        # ③ 어긋남 검출 — 원장이 기록한 현재 OVR과 EA 실제값이 다르면 보고한다(진화 기록 오류 신호)
        if cur["current_ovr"] is not None and cur["current_ovr"] != r["ovr"]:
            conflicts.append((cur["name"], cur["current_ovr"], r["ovr"], cur["evo_count"]))
        # ⭐ 진화 완주 추정 (2026-09-19, 사용자 질문 「fut.gg 데이터로 진화 완료 여부는 파악하기 어렵나?」)
        #    fut.gg는 **경로**를 주지 않지만 완주 흔적은 셋이 남는다:
        #      ⑴ 아이템 id에 `-N` 반복 접미 ⑵ isInProgressEvolution 플래그 ⑶ **OVR·스탯 상승**
        #    ⛔ 자동으로 완료 처리하지 않는다 — 어떤 진화였는지는 데이터에 없으므로 사람이 확정한다.
        # ⛔ REJECTED(무효로 판정된) 기록은 「진행 중」이 아니다 — 완주 후보에서 뺀다(2026-09-19 오탐 수정)
        pend = con.execute("""SELECT evo_name, ovr_after FROM fut_evolution_log
                              WHERE club_player_id=? AND completed_at IS NULL
                                AND COALESCE(confidence,'') NOT LIKE 'REJECTED%' ORDER BY applied_at LIMIT 1""",
                           (cur["id"],)).fetchone()
        if pend and (r["ovr"] > (cur["current_ovr"] or 0) or "-" in str(r.get("gg") or "").rsplit("-", 1)[-1][:1]
                     or str(r.get("gg") or "").count("-") > 1):
            done.append((cur["name"], pend["evo_name"], cur["current_ovr"], r["ovr"], pend["ovr_after"]))
        # ⛔ 진화 보호 — 위 `evolved` 주석 참조. EA가 낮으면 스탯을 지키고 케미만 갱신한다.
        protect = (not a.force_overwrite and cur["id"] in evolved
                   and cur["current_ovr"] is not None and r["ovr"] < cur["current_ovr"])
        if protect:
            protected.append((cur["name"], cur["current_ovr"], r["ovr"]))
            changed = (cur["chem_style_ea"] != r.get("cs") or cur["chem_points"] != r.get("cp"))
            con.execute("""UPDATE fut_club_players SET chem_style_ea=?, chem_points=?,
                             gg_player_id=?, synced_at=?, updated=? WHERE id=?""",
                        (r.get("cs"), r.get("cp"), r.get("gg"), a.pulled,
                         TODAY if changed else cur["updated"], cur["id"]))
            # ⛔ 29속성·AcceleRATE·**PlayStyle**도 스탯이라 보호 대상이다 — EA가 낡았으면 덮지 않는다
            #    (2026-09-24: PlayStyle을 받기 시작하면서 같은 규칙을 적용했다. 진화 보상 PlayStyle이
            #     EA 싱크 전 fut.gg 값으로 되돌아가는 걸 막는다).
        else:
            ps_new = ps_text(r)
            if ps_new is not None and (cur["current_playstyles"] or "") != ps_new:
                ps_fixed.append((cur["name"], cur["current_playstyles"], ps_new))
            changed = (cur["current_ovr"] != r["ovr"] or cur["current_six"] != six
                       or cur["chem_style_ea"] != r.get("cs") or cur["chem_points"] != r.get("cp")
                       or (r.get("attrs") and cur["current_attrs"] != json.dumps(r["attrs"], ensure_ascii=False))
                       or (isinstance(r.get("rp"), list) and cur["current_roles_plus"] != json.dumps(r["rp"]))
                       or (isinstance(r.get("rpp"), list) and cur["current_roles_plus_plus"] != json.dumps(r["rpp"]))
                       or (ps_new is not None and (cur["current_playstyles"] or "") != ps_new))
            # ⭐ 29속성(`attrs`)·AcceleRATE는 GG Club이 **EA 실측 그대로** 준다(2026-09-22) —
            #    받은 회차에만 덮고, 안 온 회차에는 기존 값을 지운다(COALESCE로 보존).
            attrs_json = json.dumps(r["attrs"], ensure_ascii=False) if r.get("attrs") else None
            rp_json = json.dumps(r["rp"]) if isinstance(r.get("rp"), list) else None
            rpp_json = json.dumps(r["rpp"]) if isinstance(r.get("rpp"), list) else None
            con.execute("""UPDATE fut_club_players SET current_ovr=?, current_six=?, chem_style_ea=?, chem_points=?,
                             current_attrs=COALESCE(?, current_attrs),
                             current_roles_plus=COALESCE(?, current_roles_plus),
                             current_roles_plus_plus=COALESCE(?, current_roles_plus_plus),
                             current_playstyles=COALESCE(?, current_playstyles),
                             gg_player_id=?, synced_at=?, updated=? WHERE id=?""",
                        (r["ovr"], six, r.get("cs"), r.get("cp"), attrs_json, rp_json, rpp_json, ps_new,
                         r.get("gg"), a.pulled, TODAY if changed else cur["updated"], cur["id"]))
        # ③ 스쿼드·자산 축 — 진화와 무관하고 EA가 정본이라 **보호 여부와 관계없이** 갱신한다(케미와 같은 취급).
        b = lambda v: None if v is None else int(bool(v))       # noqa: E731
        con.execute("""UPDATE fut_club_players SET is_untradeable=?, is_in_active_squad=?, is_captain=?,
                         kit_number=?, number_of_owners=? WHERE id=?""",
                    (b(r.get("unt")), b(r.get("act")), b(r.get("cap")), r.get("kit"), r.get("own"), cur["id"]))
        # ② 경기 기록 — 누적값이라 **회차 스냅샷**으로 쌓는다(같은 날 재실행이면 덮어쓴다).
        st = r.get("st") or {}
        if any(v is not None for v in st.values()):
            con.execute("""INSERT OR REPLACE INTO fut_club_player_stats(club_player_id, pulled,
                             games_played, goals, assists, yellow_cards, red_cards, ga,
                             lifetime_games_played, lifetime_goals, lifetime_assists,
                             lifetime_yellow_cards, lifetime_red_cards, source, confidence)
                           VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                        (cur["id"], a.pulled, st.get("gp"), st.get("g"), st.get("a"), st.get("yc"),
                         st.get("rc"), st.get("ga"), st.get("lgp"), st.get("lg"), st.get("la"),
                         st.get("lyc"), st.get("lrc"),
                         f"GG Club API 보유행 (scripts/fut_club_sync.py, {a.pulled} 싱크)",
                         "MEASURED — EA 실측. ⚠️ games_played는 현재 보유분 기준, lifetime_*은 카드 일생 누적이다."))
            stats_n += 1
        upd += changed
        same += (not changed)

    # ⭐⭐ ④⑤ 카드 프로필·링크 백필 (2026-09-24 신설 · migration 061 참조).
    #    GG Club은 보유 카드의 **국적·리그·클럽·스킬무브·약발·주발·키·몸무게·생일·희귀도·base 링크**를
    #    다 준다. 종전엔 `collect_futgg_cards.py`만 채워서, 새로 뽑은 카드는 그 수집기가 돌 때까지
    #    화면에서 빈칸이었다(심하면 `player_card_items` 행 자체가 없어 **카드가 통째로 안 보였다** —
    #    실측 2026-09-24: 보유 99장 중 2장이 그랬다).
    #    ⛔ **빈 칸만 채운다.** 카드 수집기가 넣은 값을 덮지 않는다 — 그쪽이 카드 페이지 원문을 본다.
    CARD_COLS = [("base_ea_id", "base"), ("futgg_url", "url"), ("skill_moves", "sm"), ("weak_foot", "wf"),
                 ("preferred_foot", "foot"), ("height_cm", "h"), ("weight_kg", "w"), ("birthdate", "dob"),
                 ("nation", "nat"), ("league", "lg"), ("club", "club"),
                 ("is_real_face", "face"),
                 ("rarity_name", "rar"), ("rarity_ea_id", "rar_ea")]
    filled, made = 0, []
    for r in rows:
        c = r.get("card") or {}
        if r["ea"] not in cards:
            # 카드 행 자체가 없다 — 최소 정보로 만든다. ⛔ player_id는 잇지 않는다(관리 4팀 밖은 NULL이 정상).
            con.execute("""INSERT INTO player_card_items(game_version, ea_item_id, base_ea_id, is_base, name_kr,
                             ovr, pac, sho, pas, dri, def, phy, attrs, source, confidence, first_seen)
                           VALUES('FC27',?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                        (r["ea"], c.get("base"), int(c.get("base") == r["ea"]), r["n"], r["ovr"],
                         # ⛔ GK는 `six`가 gkFace*라 필드 표기 칸(pac..phy)에 넣지 않는다 — 카드 수집기가 채운다.
                         *([None] * 6 if c.get("gk") else r["six"]),
                         json.dumps(r["attrs"], ensure_ascii=False) if r.get("attrs") else None,
                         f"GG Club 싱크 (scripts/fut_club_sync.py, {a.pulled}) — 카드 페이지 미수집",
                         "MEASURED(EA 실측) — ⚠️ 카드 페이지 전용 필드(포지션·카드 이미지·AcceleRATE"
                         + (" · GK 6대 표기" if c.get("gk") else "") + ")는 비어 있다. "
                         "collect_futgg_cards.py가 돌면 채워진다.", a.pulled))
            made.append(r["n"])
            # ⛔ 여기서 빠져나가지 않는다 — 아래 백필이 **같은 규칙으로** 나머지 칸을 채운다.
            #    (2026-09-24: 신설 경로만 따로 컬럼을 적었다가 `club`을 빠뜨려 G23이 걸렸다.)
        sets, vals = [], []
        for col, key in CARD_COLS:
            if c.get(key) is not None:
                sets.append(f"{col}=COALESCE({col}, ?)")       # ⛔ 빈 칸만 — 기존 값을 덮지 않는다
                vals.append(c[key])
        if sets:
            cur_before = con.execute(f"SELECT {', '.join(col for col, _ in CARD_COLS)} "
                                     "FROM player_card_items WHERE game_version='FC27' AND ea_item_id=?",
                                     (r["ea"],)).fetchone()
            con.execute(f"UPDATE player_card_items SET {', '.join(sets)} "
                        "WHERE game_version='FC27' AND ea_item_id=?", (*vals, r["ea"]))
            filled += sum(1 for v in cur_before if v is None)

    gone = [v["name"] for k, v in have.items() if v["status"] == "owned" and k not in {x["ea"] for x in rows}]
    if a.dry_run:
        con.rollback()
    else:
        con.commit()

    print(f"{'(dry-run) ' if a.dry_run else ''}싱크 {len(rows)}장 · 신규 {ins} · 갱신 {upd} · 변화 없음 {same}")
    print(f"경기 기록 스냅샷 {stats_n}행 · 카드 빈칸 보충 {filled}칸" + (f" · 카드 행 신설 {len(made)}장 {made}" if made else ""))
    if ps_fixed:
        print("\n⭐ PlayStyle을 EA 실측으로 정정 — 종전 값은 fut.gg 계산 카드에서 온 것이라 틀릴 수 있었다:")
        for n_, before, after in ps_fixed:
            print(f"   {n_:<16} [{before or '—'}] → [{after or '—'}]")
    if ps_unknown:
        print(f"\n⚠️ 이름표에 없는 PlayStyle id {sorted(ps_unknown)} — "
              "`.venv/bin/python scripts/collect_playstyle_ids.py`로 채울 것(그 전까지 원장에서 빠진다)")
    if applied_styles:
        print("\n적용된 케미 스타일:")
        for n, s, cp in applied_styles:
            print(f"   {n:<16} {s:<10} 개인 케미 {cp}")
    if done:
        print("\n⭐ 진화 완주로 보이는 선수 — `fut_club.py complete`로 닫을 것(어떤 진화였는지는 fut.gg가 주지 않는다):")
        for n_, evo, before, after, expect in done:
            print(f"   {n_:<16} {evo:<32} 원장 {before} → EA {after}" + (f" (기록상 완주 시 {expect})" if expect else ""))
    if protected:
        print(f"\n🛡️ 진화 보호 {len(protected)}명 — EA가 원장보다 낮아 **스탯을 덮지 않았다**(케미만 갱신):")
        for n, mine, ea in protected:
            print(f"   {n:<16} 원장 {mine} ← 유지 · EA {ea} ← 무시")
        print("   ⇒ fut.gg가 아직 EA를 싱크하지 않은 상태다. 「Sync Club」 후 다시 돌리면 값이 맞춰진다.")
        print("   ⛔ 진화 기록이 틀렸다고 확정했을 때만 `--force-overwrite`로 덮는다.")
    if conflicts:
        print("\n⚠️ 원장 ↔ EA 불일치 — 진화 기록을 다시 봐야 한다:")
        for n, mine, ea, ec in conflicts:
            tag = "  🛡️보호됨" if any(x[0] == n for x in protected) else ""
            print(f"   {n:<16} 원장 {mine} ↔ EA {ea} (원장 진화 {ec}회){tag}")
    if gone:
        print(f"\n원장에는 보유인데 EA 구단에 없음 {len(gone)}명 — **자동으로 처분 처리하지 않는다**: {', '.join(gone)}")
    print("\n다음: python3 scripts/export.py && scripts/db_dump.sh")


if __name__ == "__main__":
    main()
