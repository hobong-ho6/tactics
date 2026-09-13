#!/usr/bin/env python3
"""평가 표본 컬럼(T1) 재계산 — 경기 수집 직후에 돌린다.

배경(2026-09-13 사용자 논의):
  `player_evaluations`는 표본 수치를 **산문 안에** 적어 왔다("공식전 4경기 209분·평균 7.20").
  그래서 경기가 하나만 늘어도 산문을 다시 써야 했고, 그것이 갱신을 비싸게 만들었다.
  CLAUDE.md DoD는 이미 「파생 결론은 정형 필드에 기록한다 — 값을 rationale 산문에 묻지 않는다」를
  요구하고 `prescriptions`는 그 규약을 지킨다. 이 스크립트는 `player_evaluations`를 같은 규약으로 끌어온다.

무엇을 하나:
  현재 시즌 **공식전**(친선 제외) 출전 기록을 집계해 아래 5개 컬럼만 덮어쓴다.
    sample_season · sample_n · sample_minutes · sample_avg_rating · sample_as_of
  ⛔ 산문(overall/traits/strengths/stat_eval/fit_*)은 **건드리지 않는다** — 그건 T2(임계 도달) 작업이다.
  ⛔ `updated`도 건드리지 않는다 — 그 필드는 「판단을 다시 내린 날」이지 「수치를 새로 계산한 날」이 아니다.

사용:
  python3 scripts/refresh_eval_samples.py            # 드라이런(무엇이 바뀌는지만 출력)
  python3 scripts/refresh_eval_samples.py --apply    # 실제 반영
  python3 scripts/refresh_eval_samples.py --season 2026-27 --apply
"""
import argparse
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "db" / "tactics.db"
DEFAULT_SEASON = "2026-27"

# 친선은 표본에서 제외한다 — 강도가 달라 공식전과 같은 척도로 못 읽는다(docs/30).
FRIENDLY = "%Friendly%"

SQL = """
SELECT pe.id, pe.player_id,
       COUNT(DISTINCT m.event_id)                      AS n,
       COALESCE(SUM(m.minutes), 0)                     AS minutes,
       ROUND(AVG(m.rating), 2)                         AS avg_rating,
       MAX(m.date)                                     AS as_of
FROM player_evaluations pe
LEFT JOIN player_matches m
       ON m.player_id = pe.player_id
      AND m.season    = ?
      AND m.minutes IS NOT NULL
      AND m.competition NOT LIKE ?
GROUP BY pe.id
"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--season", default=DEFAULT_SEASON)
    ap.add_argument("--apply", action="store_true", help="실제 반영(기본은 드라이런)")
    a = ap.parse_args()

    con = sqlite3.connect(DB)
    rows = con.execute(SQL, (a.season, FRIENDLY)).fetchall()

    changed, cleared = [], 0
    for eid, pid, n, minutes, avg, as_of in rows:
        cur = con.execute(
            "SELECT sample_season, sample_n, sample_minutes, sample_avg_rating, sample_as_of "
            "FROM player_evaluations WHERE id=?", (eid,)).fetchone()
        new = (a.season, n, minutes, avg, as_of)
        if n == 0:
            # 출전 0 — 결손을 0으로 위장하지 않는다. 시즌만 적고 나머지는 NULL로 둔다.
            new = (a.season, 0, 0, None, None)
            cleared += 1
        if tuple(cur) != new:
            changed.append((eid, pid, tuple(cur), new))

    print(f"대상 평가행 {len(rows)}개 · 변경 {len(changed)}개 · 그중 출전0 {cleared}개 (시즌 {a.season})")
    for eid, pid, old, new in changed[:15]:
        name = con.execute("SELECT COALESCE(name_kr, name) FROM players WHERE id=?", (pid,)).fetchone()[0]
        print(f"  #{eid:>4} {name:<16} {old[1]}경기/{old[2]}분 → {new[1]}경기/{new[2]}분 (평점 {new[3]}, ~{new[4]})")
    if len(changed) > 15:
        print(f"  … 외 {len(changed) - 15}개")

    if not a.apply:
        print("\n드라이런이다. 반영하려면 --apply 를 붙여라.")
        return 0

    con.executemany(
        "UPDATE player_evaluations SET sample_season=?, sample_n=?, sample_minutes=?, "
        "sample_avg_rating=?, sample_as_of=? WHERE id=?",
        [(*new, eid) for eid, _, _, new in changed])
    con.commit()
    print(f"\n✅ {len(changed)}개 행 반영. ⛔ 산문·updated는 건드리지 않았다(T2 대상).")
    print("   다음: python3 scripts/gates.py → scripts/export.py → scripts/db_dump.sh")
    return 0


if __name__ == "__main__":
    sys.exit(main())
