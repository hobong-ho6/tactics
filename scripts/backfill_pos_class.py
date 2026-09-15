#!/usr/bin/env python3
"""`player_matches.pos_class` 결손 백필 — **채움 전용** (2026-09-15 신설).

왜 (사용자 지시 「pos_class NULL 백필해줘」, obs#772가 「감사의 다음 병목」으로 지목):
  ⛔ **migration 026은 `WHERE pos_class IS NOT NULL`이라 NULL 행을 한 번도 건드린 적이 없다.**
     그래서 「분류할 수 있는데 분류되지 않은」 행이 **1,170행** 남아 있었다.
     이 결손이 `core.aggregate`의 포지션-순수 집계에서 경기를 통째로 빠뜨린다
     (맥 알리스터 #491은 그래서 유효 표본이 서지 않아 fit을 비워야 했다).

⛔ **채움 전용이다** — 값이 있는 행은 건드리지 않는다. 재계산이 필요하면 migration 026을 쓴다.
   (refresh_duty_applied.py 사고 부류 — 자동 스크립트가 기존 값을 덮지 않게 한다.)

⛔ **추측하지 않는다.** 분류는 `core.classify.pos_class`만 쓰고(불변규칙 4), 다음은 **NULL로 남긴다**:
  · `formation`이 없는 행 — 좌표 밴딩 폴백은 **백3와 백4를 구분하지 못한다**(classify 독스트링).
    「결손과 오분류는 다르다」가 이 저장소의 규약이다.
  · `core.classify.FORM`에 없는 포메이션 — 슬롯 라벨 순서를 모르면 매핑을 발명하게 된다.
  · 표본 하한 미달(45분 미만 · hit_points 15 미만) — classify가 스스로 None을 낸다.

⚠️ **파급**: `pos_class`는 migration 026 주석이 「표시 전용」이라 했지만, 2026-09-15 신설된
   표본 감사·재집계 경로는 이 컬럼으로 경기를 고른다. 채우면 **집계 표본이 커진다** ⇒
   백필 후 `scripts/audit_measured_samples.py`를 돌려 「노후」로 뜨는 행을 재집계해야 한다.

사용:
    .venv/bin/python scripts/backfill_pos_class.py --dry-run
    .venv/bin/python scripts/backfill_pos_class.py --apply
    .venv/bin/python scripts/backfill_pos_class.py --dry-run --season 2026-27
"""
import argparse
import sqlite3
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core import DB                                                        # noqa: E402
from core.classify import (FORM, lateral_for_formation, normalize_formation,  # noqa: E402
                           pos_class)

REGIME_BY_TEAM = {'AVL': 1, 'CHE': 2, 'LIV': 3, 'ATM': 4}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true')
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--season', help='특정 시즌만(예: 2026-27)')
    a = ap.parse_args()
    if not (a.apply or a.dry_run):
        ap.error('--dry-run 또는 --apply 중 하나를 주세요')

    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    q = ("SELECT id, player_id, season, team_code, formation, lineup_pos, avg_x, avg_y, "
         "       minutes, hit_points "
         "FROM player_matches WHERE pos_class IS NULL")
    params = ()
    if a.season:
        q += " AND season=?"
        params = (a.season,)
    rows = con.execute(q, params).fetchall()

    cache = {}

    def lateral(formation, regime_id):
        key = (normalize_formation(formation), regime_id)
        if key not in cache:
            cache[key] = lateral_for_formation(con, formation, regime_id)
        return cache[key]

    plan, skip, dist = [], Counter(), Counter()
    for r in rows:
        if not r['formation']:
            skip['formation 결손 — 폴백은 백3/백4를 구분 못 해 채우지 않는다'] += 1
            continue
        if normalize_formation(r['formation']) not in FORM:
            skip[f"FORM 미등록 포메이션({normalize_formation(r['formation'])})"] += 1
            continue
        new = pos_class(r['avg_x'], r['avg_y'], r['lineup_pos'],
                        lateral(r['formation'], REGIME_BY_TEAM.get(r['team_code'] or '')),
                        r['minutes'], r['hit_points'])
        if new is None:
            skip['표본 하한 미달·좌표 결손 — classify가 None'] += 1
            continue
        plan.append((new, r['id']))
        dist[new] += 1

    print(f"NULL 행 {len(rows)}" + (f" (season={a.season})" if a.season else "")
          + f" · **채울 수 있는 행 {len(plan)}** · 남기는 행 {sum(skip.values())}")
    print("\n채움 분포:")
    for k, n in dist.most_common():
        print(f"  {k:<6}{n}")
    print("\n남기는 사유(⛔ 추측하지 않는다):")
    for k, n in skip.most_common():
        print(f"  {n:5d}  {k}")

    if a.dry_run:
        print("\n(dry-run — 쓰지 않았습니다)")
        return

    con.execute('BEGIN IMMEDIATE')
    con.executemany("UPDATE player_matches SET pos_class=? WHERE id=? AND pos_class IS NULL", plan)
    con.execute(
        "INSERT INTO _migration_log(run_at, v1_path, note) VALUES(date('now'), ?, ?)",
        ('pos_class-null-backfill-2026-09-15',
         f"pos_class 결손 백필 {len(plan)}행(채움 전용). 사용자 지시 2026-09-15. "
         f"⛔ migration 026이 `WHERE pos_class IS NOT NULL`이라 NULL 행을 한 번도 보지 않았다 — "
         f"분류 가능한데 비어 있던 행이 그만큼 쌓였고, 표본 감사의 포지션-순수 집계에서 "
         f"경기가 통째로 빠지고 있었다. formation 결손·FORM 미등록·표본 하한 미달은 "
         f"추측하지 않고 NULL로 남겼다(결손과 오분류는 다르다). "
         f"⚠️ 집계 표본이 커지므로 audit_measured_samples.py로 「노후」 행을 재집계해야 한다."))
    con.commit()
    print(f"\n✅ 백필 {len(plan)}행")
    print("다음: .venv/bin/python scripts/audit_measured_samples.py  # 「노후」 재집계 대상 확인")


if __name__ == '__main__':
    main()
