#!/usr/bin/env python3
"""좌우 이봉(bimodal) 분포 점검 — **읽기 전용**.

왜 있는가 (2026-08-25 신설, obs#327):
  일링주니어에서 드러났다 — **양측을 모두 뛴 선수를 시즌 평균으로 집계하면 그리드가 양쪽 다 틀린다.**
  그는 30경기 중 우측 17 · 좌측 12로 갈리는데, 전체 집계는 LM 0.353 / RM 0.696을 준다.
  사이드를 분리하면 **좌측 스틴트 LM 0.830 · 우측 스틴트 RM 0.799**다 —
  즉 평균이 좌측 능력을 0.830 → 0.353으로 **과소평가**하고 우측도 깎는다.
  ⇒ 슬롯 적합을 쓰기 전에 「이 선수의 그리드가 한 사이드를 대표하는가」를 먼저 물어야 한다.

판정 규칙 (좌표는 불변규칙 9: `player_matches.avg_y`는 SofaScore 원좌표 — **낮을수록 우측**):
  우측 avg_y < 45 · 중앙 45~55 · 좌측 >= 55
  이봉 = 좌우 중 **적은 쪽이 MIN_SIDE 경기 이상**이고 **좌우 합의 MIN_RATIO 이상**을 차지할 때.

⛔ **쓰지 않는다.** 이 스크립트는 진단만 한다 — 그리드 재적재·`pos_only` 변경은 사람이 판단한다.
   사이드가 갈리는 것이 **로테이션 때문인지 체제 변화 때문인지**를 구분하는 것은 표본 밖의 정보다.

사용:
    .venv/bin/python scripts/check_side_bimodality.py                 # 확정 고정 선수만(기본)
    .venv/bin/python scripts/check_side_bimodality.py --all           # 유출 감시 대상 포함
    .venv/bin/python scripts/check_side_bimodality.py --team AVL
    .venv/bin/python scripts/check_side_bimodality.py --exclude 28 58 # 추적 제외(임대·이탈)
"""
import argparse
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from core.aggregate import player_aggregate  # noqa: E402
from core.kernel import Kernel  # noqa: E402

DB = ROOT / "db" / "tactics.db"

MIN_N = 8        # 이봉 판정에 필요한 최소 경기 수
MIN_SIDE = 3     # 적은 쪽 사이드의 최소 경기 수
MIN_RATIO = 0.25  # 적은 쪽이 좌우 합에서 차지해야 하는 최소 비율
MIN_HP = 15      # core.aggregate 기본값과 일치


def side_of(y):
    return "R" if y < 45 else ("L" if y >= 55 else "C")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--team", help="팀 코드")
    ap.add_argument("--all", action="store_true",
                    help="transfer_outgoing 등재 선수도 포함(기본은 제외)")
    ap.add_argument("--exclude", nargs="*", type=int, default=[],
                    help="추적 제외할 player_id (임대·이탈 확정)")
    a = ap.parse_args()

    con = sqlite3.connect(DB)
    k = Kernel()
    slots = {}
    for rid, pos, x, st in con.execute("SELECT regime_id, pos, x, slot_type FROM slots"):
        slots.setdefault((rid, st), []).append((pos, x))

    outgoing = set()
    if not a.all:
        outgoing = {r[0] for r in con.execute(
            "SELECT player_id FROM transfer_outgoing WHERE player_id IS NOT NULL")}
    outgoing |= set(a.exclude)

    q = """SELECT DISTINCT r.team_code, se.player_id, COALESCE(se.label, p.name_kr)
           FROM squad_entries se
           JOIN players p ON p.id = se.player_id
           JOIN regimes r ON r.id = se.regime_id
           WHERE se.map25 NOT LIKE '0000000000000000000000000'"""
    args = []
    if a.team:
        q += " AND r.team_code = ?"
        args.append(a.team)
    people = con.execute(q + " ORDER BY r.team_code", args).fetchall()

    checked, skipped, flagged = 0, [], []
    for team, pid, nm in people:
        if pid in outgoing:
            continue
        ys = [r[0] for r in con.execute(
            "SELECT avg_y FROM player_matches WHERE player_id=? AND avg_y IS NOT NULL "
            "AND hit_points>=?", (pid, MIN_HP))]
        if len(ys) < MIN_N:
            skipped.append((team, nm, len(ys)))
            continue
        checked += 1
        L = sum(1 for y in ys if side_of(y) == "L")
        R = sum(1 for y in ys if side_of(y) == "R")
        C = len(ys) - L - R
        lo, hi = min(L, R), max(L, R)
        if lo >= MIN_SIDE and (L + R) and lo / (L + R) >= MIN_RATIO:
            flagged.append((team, pid, nm, L, C, R, len(ys)))

    print(f"대상 {len(people)}행 · 점검 {checked}명 · 표본부족(<{MIN_N}) {len(skipped)}명 "
          f"· 유출/제외 스킵 {len(outgoing)}명분")
    if not flagged:
        print("\n✅ 이봉 분포 0건 — 모든 대상이 한 사이드로 수렴한다.")
    for team, pid, nm, L, C, R, n in flagged:
        print(f"\n⚠️ [{team}] {nm} (pid={pid}) — 좌 {L} · 중앙 {C} · 우 {R} (n={n})")
        for st in [r[0] for r in con.execute(
                "SELECT DISTINCT slot_type FROM squad_entries WHERE player_id=?", (pid,))]:
            cands = slots.get((_regime(con, pid), st))
            if not cands:
                continue
            rows = []
            for label, where in (("전체", ""), ("좌측만", "avg_y>=55"), ("우측만", "avg_y<45")):
                agg = player_aggregate(pid, where=where)
                if not agg or not agg.get("n"):
                    rows.append((label, None, None))
                    continue
                best = {}
                for pos, x in sorted(set(cands)):
                    b = k.best_fit(agg["map25"], x, st)
                    best[pos] = b[2]
                rows.append((label, agg, best))
            if not any(r[1] for r in rows):
                continue
            print(f"    slot_type={st}")
            for label, agg, best in rows:
                if not agg:
                    print(f"      {label:5} 표본 없음")
                    continue
                fits = " · ".join(f"{p} {v:.3f}" for p, v in sorted(best.items()))
                print(f"      {label:5} n={agg['n']:<3} {agg['minutes']:>5}분 "
                      f"평점 {agg['avg_rating']} | {fits}")
    if skipped:
        print(f"\n표본부족(<{MIN_N}경기, hp>={MIN_HP}) — 판정 보류:")
        print("  " + " · ".join(f"[{t}]{n}({c})" for t, n, c in skipped))


def _regime(con, pid):
    r = con.execute("SELECT regime_id FROM squad_entries WHERE player_id=? LIMIT 1",
                    (pid,)).fetchone()
    return r[0] if r else None


if __name__ == "__main__":
    main()
