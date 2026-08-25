#!/usr/bin/env python3
"""전후(라인 높이) 이봉(bimodal) 분포 점검 — **읽기 전용**.

왜 있는가 (2026-08-25 신설, obs#328~330의 x축 짝):
  좌우 점검(check_side_bimodality.py)이 **양측을 뛴 선수의 시즌 평균은 양쪽 다 틀린다**는 것을
  실증했다(린델뢰프 0.75 → LCB .952/RCB .929). **같은 왜곡이 전후 축에도 있을 수 있다** —
  풀백이 어떤 경기엔 윙백 높이로, 어떤 경기엔 수비형으로 뛰면 그리드 **행**이 뭉개진다.
  (`core.encode`: row = 4 − ⌊소파x/20⌋ ⇒ **높이는 행에 인코딩된다.**)

⛔⛔ **좌우와 판정 방식이 다르다 — 절대 구간을 쓸 수 없다.**
  좌우는 피치 좌우가 고정이라 「avg_y<45=우측」 같은 절대 기준이 성립한다.
  그러나 **라인 높이의 기준선은 포지션마다 다르다** — CB의 30과 ST의 80은 둘 다 정상이다.
  ⇒ **선수별 상대 분할**을 쓴다: 그 선수의 avg_x를 정렬해 **가장 큰 내부 간극**에서 자른다.

판정 규칙 (좌표는 불변규칙 9: `player_matches.avg_x`는 SofaScore 원좌표 = **공격 방향**, 툴y와 같다):
  ⑴ 정렬한 avg_x의 인접 간극 중 최대값을 찾아 그 지점에서 저/고 두 군으로 나눈다.
  ⑵ 이봉 판정 3조건을 **모두** 만족해야 한다:
      · 적은 쪽이 MIN_SIDE 경기 이상
      · 적은 쪽이 전체의 MIN_RATIO 이상
      · **최대 간극이 MIN_GAP_ABS 이상이고, 나머지 간극 중앙값의 GAP_FACTOR 배 이상**
    ⑵의 마지막 조건이 없으면 **단봉으로 퍼진 분포까지 전부 이봉으로 오탐**한다
    (간극이 고르게 퍼져 있으면 최대 간극도 평균과 비슷하다).

⛔ **쓰지 않는다.** 진단만 한다 — 그리드 재적재·처방 변경은 사람이 판단한다.
   높이가 갈리는 것이 **로테이션·체제 변화·경기 국면(리드/추격)** 중 무엇 때문인지는 표본 밖 정보다.

사용:
    python3 scripts/check_height_bimodality.py                 # 확정 고정 선수만(기본)
    python3 scripts/check_height_bimodality.py --all           # 유출 감시 대상 포함
    python3 scripts/check_height_bimodality.py --team AVL
"""
import argparse
import sqlite3
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from core.aggregate import player_aggregate  # noqa: E402
from core.kernel import Kernel  # noqa: E402

DB = ROOT / "db" / "tactics.db"

MIN_N = 8          # 이봉 판정에 필요한 최소 경기 수 (좌우 점검과 동일)
MIN_SIDE = 3       # 적은 쪽 군의 최소 경기 수
MIN_RATIO = 0.25   # 적은 쪽이 전체에서 차지해야 하는 최소 비율
MIN_GAP_ABS = 8.0  # 최대 간극의 절대 하한 (툴 단위 ≈ 피치 길이의 8%)
GAP_FACTOR = 2.5   # 최대 간극 / 나머지 간극 중앙값
MIN_HP = 15        # core.aggregate 기본값과 일치


def split_at_largest_gap(xs):
    """정렬된 avg_x → (분할점, 최대간극, 나머지간극중앙값). 간극이 없으면 None."""
    s = sorted(xs)
    gaps = [(s[i + 1] - s[i], i) for i in range(len(s) - 1)]
    if not gaps:
        return None
    top_gap, idx = max(gaps)
    others = [g for g, _ in gaps if (g, _) != (top_gap, idx)]
    med = statistics.median(others) if others else 0.0
    thr = (s[idx] + s[idx + 1]) / 2
    return thr, top_gap, med


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--team")
    ap.add_argument("--all", action="store_true",
                    help="transfer_outgoing 등재 선수도 포함(기본은 제외)")
    ap.add_argument("--exclude", nargs="*", type=int, default=[])
    a = ap.parse_args()

    con = sqlite3.connect(DB)
    k = Kernel()
    slots = {}
    for rid, pos, x, st in con.execute("SELECT regime_id, pos, x, slot_type FROM slots"):
        slots.setdefault((rid, st), []).append((pos, x))

    outgoing = set(a.exclude)
    if not a.all:
        outgoing |= {r[0] for r in con.execute(
            "SELECT player_id FROM transfer_outgoing WHERE player_id IS NOT NULL")}

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
        xs = [r[0] for r in con.execute(
            "SELECT avg_x FROM player_matches WHERE player_id=? AND avg_x IS NOT NULL "
            "AND hit_points>=?", (pid, MIN_HP))]
        if len(xs) < MIN_N:
            skipped.append((team, nm, len(xs)))
            continue
        checked += 1
        sp = split_at_largest_gap(xs)
        if not sp:
            continue
        thr, gap, med = sp
        lo = sum(1 for x in xs if x < thr)
        hi = len(xs) - lo
        small = min(lo, hi)
        if (small >= MIN_SIDE and small / len(xs) >= MIN_RATIO
                and gap >= MIN_GAP_ABS and (med == 0 or gap >= GAP_FACTOR * med)):
            flagged.append((team, pid, nm, thr, gap, med, lo, hi, len(xs)))

    print(f"대상 {len(people)}행 · 점검 {checked}명 · 표본부족(<{MIN_N}) {len(skipped)}명 "
          f"· 유출/제외 스킵 {len(outgoing)}명분")
    print(f"판정 기준: 적은군>={MIN_SIDE}경기 & 비율>={MIN_RATIO} & "
          f"최대간극>={MIN_GAP_ABS} & 최대간극>={GAP_FACTOR}×나머지중앙값")
    if not flagged:
        print("\n✅ 전후 이봉 0건 — 모든 대상의 라인 높이가 단봉으로 수렴한다.")
    for team, pid, nm, thr, gap, med, lo, hi, n in flagged:
        print(f"\n⚠️ [{team}] {nm} (pid={pid}) — 저 {lo} · 고 {hi} (n={n}) "
              f"분할 avg_x={thr:.1f} · 최대간극 {gap:.1f} (나머지중앙값 {med:.1f})")
        rid = _regime(con, pid)
        for st in [r[0] for r in con.execute(
                "SELECT DISTINCT slot_type FROM squad_entries WHERE player_id=?", (pid,))]:
            cands = slots.get((rid, st))
            if not cands:
                continue
            rows = []
            for label, where, params in (("전체", "", ()),
                                         ("저위치", "avg_x < ?", (thr,)),
                                         ("고위치", "avg_x >= ?", (thr,))):
                agg = player_aggregate(pid, where=where, params=params)
                rows.append((label, agg,
                             {pos: k.best_fit(agg["map25"], x, st)[2]
                              for pos, x in sorted(set(cands))} if agg else None))
            if not any(r[1] for r in rows):
                continue
            print(f"    slot_type={st}")
            for label, agg, best in rows:
                if not agg:
                    print(f"      {label:5} 표본 부족(<2경기)")
                    continue
                fits = " · ".join(f"{p} {v:.3f}" for p, v in sorted(best.items()))
                print(f"      {label:5} n={agg['n']:<3} {agg['minutes']:>5}분 "
                      f"평점 {agg['avg_rating']} 툴y {agg['tool_y']} | {fits}")
    if skipped:
        print(f"\n표본부족(<{MIN_N}경기, hp>={MIN_HP}) — 판정 보류 {len(skipped)}명")


def _regime(con, pid):
    r = con.execute("SELECT regime_id FROM squad_entries WHERE player_id=? LIMIT 1",
                    (pid,)).fetchone()
    return r[0] if r else None


if __name__ == "__main__":
    main()
