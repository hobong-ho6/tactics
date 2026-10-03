#!/usr/bin/env python3
"""갤러리 평가 — 보유 카드로 세트별 달성 가능 등급을 계산해 `fut_gallery_eval`에 쌓는다 (2026-10-02 · migration 092).

왜 (사용자 지시 「클럽 싱크 선수 수집이 끝나면 달성 가능한 갤러리와 더 높일 수 있는 갤러리 목록 ·
    달성 가능한 갤러리가 있으면 NEW 뱃지나 알림」 + 「스크립트로 작성해서 돌려줘」):
  계산 규칙은 `core/gallery.py`가 정본이다 — 여기는 입력을 채우고 결과를 적고 보고만 한다.

순서:
  ⑴ 보유 카드의 클럽·자매 구단·리그 EA id가 비어 있으면 fut.gg에서 채운다(채움 전용 · 목록 API → 빠지면 상세 API).
  ⑵ 최신 세트 정의(`fc_gallery_sets`)로 평가 → 오늘 회차로 적는다(같은 날 다시 돌리면 그 회차를 갈아 쓴다).
  ⑶ 직전 회차·내 완성 원장(`fut_gallery_completions` · core.gallery.mine)과 견줘 **달성 가능 / 더 높일 수 있음 / NEW**를 찍는다.
⚠️ 등급은 태그 보너스를 뺀 **하한**이다(core/gallery.py 주석). 「C 이상」만 목록에 올린다 — D는 카드 한 장이면 된다.

사용:
    python3 scripts/gallery_eval.py            # 채우고 평가하고 적는다
    python3 scripts/gallery_eval.py --dry-run  # 적지 않고 보고만
"""
import argparse
import datetime as dt
import json
import sqlite3
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from core import DB                                        # noqa: E402
from core.gallery import MIN_LIST, classify, evaluate, mine as gal_mine  # noqa: E402

GAME = "FC27"
TODAY = dt.date.today().isoformat()


def fill_ids(con):
    from scripts.collect_futgg_history import API, get
    need = [r[0] for r in con.execute(
        """SELECT DISTINCT i.ea_item_id FROM player_card_items i
             JOIN fut_club_players c ON c.ea_item_id=i.ea_item_id   -- ⭐ 지금 보유 + 예전에 가졌던 카드(판매·SBC) 전부
            WHERE i.game_version=? AND (i.club_ea_id IS NULL OR i.grading_score IS NULL)""", (GAME,))]
    got = {}
    for k in range(0, len(need), 40):
        for x in (get(f"{API}/players/v2/27/?ea_ids=" + ",".join(map(str, need[k:k + 40]))) or {}).get("data", []):
            cl, lg = x.get("club") or {}, x.get("league") or {}
            got[x["eaId"]] = (cl.get("eaId"), cl.get("siblingClubEaId"), lg.get("eaId"), x.get("gradingScore"))
    for ea in [e for e in need if e not in got]:                 # ⚠️ 목록 API가 일부를 빠뜨린다 — 상세로 보충
        d = get(f"{API}/player-item-definitions/27/{ea}/")
        d = (d or {}).get("data") or d or {}
        cl = d.get("club") or {}
        got[ea] = (d.get("clubEaId") or cl.get("eaId"), cl.get("siblingClubEaId"), d.get("leagueEaId"), d.get("gradingScore"))
        time.sleep(0.3)
    for ea, (c, s, l, gs) in got.items():
        # ⭐ gradingScore = fut.gg가 주는 카드별 갤러리 점수(migration 094 · 등급 B) — 채움 전용
        con.execute("""UPDATE player_card_items SET club_ea_id=COALESCE(club_ea_id,?),
                         sibling_club_ea_id=COALESCE(sibling_club_ea_id,?), league_ea_id=COALESCE(league_ea_id,?),
                         grading_score=COALESCE(grading_score,?)
                       WHERE game_version=? AND ea_item_id=?""", (c, s, l, gs, GAME, ea))
    con.commit()
    print(f"카드 EA id·갤러리 점수 채움: 대상 {len(need)}장 · 받음 {len(got)}장")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--no-fill", action="store_true", help="fut.gg 조회 없이 평가만")
    a = ap.parse_args()
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    if not a.no_fill and not a.dry_run:
        fill_ids(con)
    sets = [dict(r) for r in con.execute(
        """SELECT * FROM fc_gallery_sets WHERE game_version=?
             AND pulled=(SELECT MAX(pulled) FROM fc_gallery_sets WHERE game_version=?)""", (GAME, GAME))]
    # ⭐ 진화 전 원래 카드로 센다(i.ovr = 아이템 정의) — 같은 아이템을 여러 장 갖고 있으면 각각 센다.
    cards = [dict(r) for r in con.execute(
        """SELECT c.id, c.name, c.number_of_owners, i.ovr, i.grading_score, i.club_ea_id, i.best_pos, i.nation, i.base_ea_id,
                  i.skill_moves, i.weak_foot, COALESCE(i.is_icon,0) is_icon, i.sibling_club_ea_id, i.league_ea_id, i.rarity_ea_id,
                  i.rarity_name, COALESCE(i.is_hero,0) is_hero, COALESCE(i.is_special,0) is_special
             FROM fut_club_players c JOIN player_card_items i ON i.ea_item_id=c.ea_item_id AND i.game_version=?
            WHERE c.status='owned' AND COALESCE(c.is_loan,0)=0
            GROUP BY c.id""", (GAME,))]
    miss = sum(1 for c in cards if c["club_ea_id"] is None)
    if miss:
        print(f"⚠️ 클럽 EA id가 없는 보유 카드 {miss}장 — 클럽·리그 세트에서 빠진다(--no-fill이면 채우지 않는다)")
    res = evaluate(sets, cards)
    # ⭐ 직전 회차와는 **태그 포함 추정 등급**끼리 견준다(2026-10-03 · 없던 회차는 확정 하한으로)
    prev = {r["set_id"]: r["grade"] for r in con.execute(
        """SELECT set_id, COALESCE(est_grade, grade) grade FROM fut_gallery_eval WHERE game_version=?
             AND pulled=(SELECT MAX(pulled) FROM fut_gallery_eval WHERE game_version=? AND pulled<?)""",
        (GAME, GAME, TODAY))}
    mine = gal_mine(con, GAME)
    name = {s["set_id"]: s["name"] for s in sets}
    unsup = [name[r["set_id"]] for r in res if not r["supported"]]
    by = {r["set_id"]: r for r in res}
    ra, hi, nw = classify(res, prev, mine)
    reach, higher, new = [by[i] for i in ra], [by[i] for i in hi], [by[i] for i in nw]
    line = lambda r: (f"   {name[r['set_id']]:<26} {r['est_grade']}(추정 · 확정 하한 {r['grade']}) (추정 {r['est_score']:,} = 기본 {r['base_score']:,}+태그 · {r['eligible_n']}/{r['required_n']}장"  # noqa: E731
                      + (f" · 다음 {r['next_grade']}까지 {r['next_gap']:,})" if r["next_grade"] else ")"))
    print(f"\n■ 갤러리 평가 {TODAY} — 세트 {len(sets)} · 보유 카드 {len(cards)}장 (태그 포함 추정 · 확정 하한 병기)")
    print(f"⭐ 달성 가능 {len(reach)}" + ("".join("\n" + line(r) for r in reach) if reach else ""))
    print(f"⬆️ 더 높일 수 있음 {len(higher)}" + ("".join(
        "\n" + line(r) + f"  ← 기록 {mine[r['set_id']]}" for r in higher) if higher else ""))
    print(f"🆕 직전 회차보다 새로 달성 가능 {len(new)}" + (f": {', '.join(name[r['set_id']] for r in new)}" if new else
                                                     ("" if prev else " (첫 회차 — 비교 대상 없음)")))
    if unsup:
        print(f"❔ 대상 규칙 미상이라 판정 안 함 {len(unsup)}: {', '.join(unsup)}")
    if a.dry_run:
        print("\n(--dry-run: 적지 않았다)")
        return
    src = f"scripts/gallery_eval.py ({TODAY}) — 보유 카드 × fc_gallery_sets 최신 회차 · core/gallery.py"
    conf = ("카드 점수 = fut.gg gradingScore(등급 B · 없으면 커뮤니티 표 등급 D) · grade=기본 점수 확정 하한 · est_grade=태그 포함 추정"
            "(공개 21종 표 · 등급 D · fut.gg 조합 재현 오차 중앙값 −1.3%) · First Owner=보유한 사람 수 0·1(사용자 기준) · Holographic 미반영 · "
            "진화 전 원래 카드 OVR · 한 카드를 여러 세트에 쓸 수 있다고 봄")
    con.execute("DELETE FROM fut_gallery_eval WHERE game_version=? AND pulled=?", (GAME, TODAY))
    con.executemany("""INSERT INTO fut_gallery_eval(game_version,set_id,pulled,eligible_n,required_n,base_score,grade,
                         next_grade,next_gap,prev_grade,card_ids,supported,source,confidence,est_score,est_grade,tag_detail)
                       VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                    [(GAME, r["set_id"], TODAY, r["eligible_n"], r["required_n"], r["base_score"], r["grade"],
                      r["next_grade"], r["next_gap"], prev.get(r["set_id"]), json.dumps(r["card_ids"]),
                      r["supported"], src, conf, r["est_score"], r["est_grade"], r["tag_detail"]) for r in res])
    con.commit()
    print(f"\n적재 {len(res)}행 → fut_gallery_eval ({TODAY})")


if __name__ == "__main__":
    main()
