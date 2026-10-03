#!/usr/bin/env python3
"""인게임 갤러리 세트 전사(JSON) → `fut_gallery_placed` · `fut_gallery_snapshots` (2026-10-03 · migration 098).

왜 (사용자 지시 「세트별 등록 진행해줘」): 세트에는 예전에 가졌던 아이템이 들어가 있고 fut.gg는 진행 상태를 주지 않는다
  ⇒ PS 리모트 캡처를 사람이(세션이) 전사한 JSON을 적는다. 전사 형식은 reports/ingame/2026-10-03-gallery-placed.json 머리말.

식별 순서(아이템 id를 채우는 것 — 못 채우면 비워 둔다 · ⛔ 추측하지 않는다):
  ① 우리 원장(fut_club_players · 판매·SBC 포함) 중 그 세트에 넣을 수 있는 카드 — 점수·OVR·주 포지션이 같고, 여럿이면 국적으로 좁혀 **아이템 하나**일 때
  ② player_card_items 전체(원장 밖 아이템) — 같은 조건
⛔ 점수 합이 화면 「기본 등급」 값과 다르면 적지 않는다(전사 오류).

사용:
    python3 scripts/gallery_placed_load.py reports/ingame/2026-10-03-gallery-placed.json [--dry-run]
"""
import argparse
import json
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from core import DB                     # noqa: E402
from core.gallery import eligible       # noqa: E402

GAME = "FC27"


def pick(cands, nat):
    """후보 → 아이템 하나면 그 행. 국적으로 좁히고, 같은 아이템 여러 장(중복본)은 하나로 본다."""
    if nat and len({c["ea_item_id"] for c in cands}) > 1:
        cands = [c for c in cands if c["nation"] == nat] or cands
    return cands[0] if cands and len({c["ea_item_id"] for c in cands}) == 1 else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("json")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    d = json.loads(Path(a.json).read_text())
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    sets = {r["name"]: dict(r) for r in con.execute(
        """SELECT * FROM fc_gallery_sets WHERE game_version=?
             AND pulled=(SELECT MAX(pulled) FROM fc_gallery_sets WHERE game_version=?)""", (GAME, GAME))}
    ledger = [dict(r) for r in con.execute(
        """SELECT c.id club_player_id, i.* FROM fut_club_players c
             JOIN player_card_items i ON i.ea_item_id=c.ea_item_id AND i.game_version=?
            WHERE COALESCE(c.is_loan,0)=0 ORDER BY c.status='owned' DESC, c.id""", (GAME,))]
    items = [dict(r) for r in con.execute("SELECT * FROM player_card_items WHERE game_version=?", (GAME,))]
    src = f"{a.json} — PS 리모트 캡처 전사(사용자 캡처 · 세션 전사)"
    rows, snaps, bad = [], [], []
    print(f"■ 갤러리 세트 전사 적재 {d['captured_at']} — {len(d['sets'])}세트")
    for name, v in d["sets"].items():
        s = sets.get(name)
        if not s:
            bad.append(f"세트 이름 없음: {name}")
            continue
        cs = [x.split(" ", 3) for x in v["cards"]]
        total = sum(int(c[0]) for c in cs)
        st = v.get("state") or {}
        if st.get("base") is not None and st["base"] != total:
            bad.append(f"{name}: 카드 점수 합 {total} ≠ 화면 기본 {st['base']} — 적지 않음")
            continue
        led = [c for c in ledger if eligible(c, s)]
        itm = [c for c in items if eligible(c, s)]
        used, hits = set(), {}
        same = lambda c, sc, ov, pos: (c["grading_score"] == int(sc) and c["ovr"] == int(ov)   # noqa: E731
                                       and (c["positions"] or c["best_pos"] or "").split("/")[0] == pos and c["ea_item_id"] not in used)
        for pool, how in ((led, "ledger"), (itm, "item")):
            for k, (sc, ov, pos, *nat) in enumerate(cs, 1):
                if k not in hits:
                    hit = pick([c for c in pool if same(c, sc, ov, pos)], nat[0] if nat else None)
                    if hit:
                        used.add(hit["ea_item_id"])
                        hits[k] = (hit, how)
            # ⭐ 같은 표기(점수·OVR·포지션·국적)가 여러 칸이고 후보 아이템 수가 칸 수와 **같으면** 함께 확정한다
            #    (예: 분데스리가 「410 83 LB 독일」 두 칸 = Raum·Mittelstädt — 하나씩 보면 모호하다)
            grp = {}
            for k, c in enumerate(cs, 1):
                if k not in hits:
                    grp.setdefault(tuple(c), []).append(k)
            for (sc, ov, pos, *nat), ks in grp.items():
                cand = {}
                for c in pool:
                    if same(c, sc, ov, pos) and (not nat or c["nation"] == nat[0]):
                        cand.setdefault(c["ea_item_id"], c)
                if len(ks) > 1 and len(cand) == len(ks):
                    for k, c in zip(ks, cand.values()):
                        used.add(c["ea_item_id"])
                        hits[k] = (c, how)
        n_led = sum(1 for _, h in hits.values() if h == "ledger")
        n_itm = len(hits) - n_led
        for k, (sc, ov, pos, *nat) in enumerate(cs, 1):
            hit, how = hits.get(k, (None, None))
            rows.append((GAME, s["set_id"], d["captured_at"], k, int(sc), int(ov), pos, nat[0] if nat else None,
                         hit["ea_item_id"] if hit else None, hit.get("club_player_id") if hit and how == "ledger" else None,
                         src, None if hit else "아이템 미식별 — 점수·OVR·포지션·국적만"))
        if st.get("base") is not None:
            snaps.append((GAME, s["set_id"], d["captured_at"], len(cs), st["base"], st.get("bonus"), st.get("total"),
                          st.get("grade"), st.get("pending", 0), src))
        print(f"   {name:<24} {len(cs):>2}장 합 {total:>6,}"
              + (f" (화면 기본 {st['base']:,} ✓ · 총점 {st['total']:,} {st.get('grade')}{' · 확정 전' if st.get('pending') else ''})"
                 if st.get("base") is not None else "")
              + f" · 원장 {n_led} · 원장 밖 아이템 {n_itm} · 미식별 {len(cs) - n_led - n_itm}")
    for b in bad:
        print("⛔", b)
    if a.dry_run or bad:
        print("\n(적지 않았다)" + (" — 위 오류부터 고친다" if bad else " --dry-run"))
        return 1 if bad else 0
    # 같은 캡처 날짜를 다시 적으면 그 묶음을 갈아 쓴다(재전사 정정용)
    for t in ("fut_gallery_placed", "fut_gallery_snapshots"):
        con.execute(f"DELETE FROM {t} WHERE game_version=? AND captured_at=?", (GAME, d["captured_at"]))
    con.executemany("""INSERT INTO fut_gallery_placed(game_version,set_id,captured_at,slot,score,ovr,pos,nation,
                         ea_item_id,club_player_id,source,notes) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)""", rows)
    con.executemany("""INSERT INTO fut_gallery_snapshots(game_version,set_id,captured_at,placed_n,base_score,bonus_score,
                         total_score,grade,pending,source) VALUES(?,?,?,?,?,?,?,?,?,?)""", snaps)
    con.commit()
    print(f"\n적재 아이템 {len(rows)}행 · 스냅숏 {len(snaps)}행")
    return 0


if __name__ == "__main__":
    sys.exit(main())
