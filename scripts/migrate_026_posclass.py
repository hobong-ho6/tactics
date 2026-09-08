#!/usr/bin/env python3
"""026 — player_matches.pos_class 전량 재계산 (사용자 승인 2026-09-08).

왜: pos_class에 **어휘 3종이 섞여 있었다** — ⑴ core.classify의 GK/LB/…/ST,
⑵ scripts/load_lineup_order.py의 별도 어휘(pivot-right·LW/AML·CAM),
⑶ 손으로 친 문장('Right winger / inside-right forward' 등). 값이 있는 839행 중
450행이 정본 어휘 밖이었고, 백3 경기에서는 CB 셋이 전부 풀백으로 찍혔다.

무엇을: core.classify를 포메이션 인식으로 재작성한 뒤 839행을 전량 재계산해
`slots.pos` 어휘 하나로 통일한다. 표본이 얇은 행(minutes<45 · hit_points<15)은
추측하지 않고 NULL로 둔다(결손과 오분류는 다르다).

안전성: pos_class는 **표시 전용**이다. core/aggregate.py도, G3·G4 앵커도,
scripts/phase_split.py도 이 컬럼을 쓰지 않는다(phase_split은 주석으로 금지까지 해 뒀다).
따라서 적합도·처방·커널 값은 이 변경의 영향을 받지 않는다.

되돌리기: 변경 전 값은 `db/dump/player_matches.sql`의 직전 커밋에 그대로 있다.

사용법:  python3 scripts/migrate_026_posclass.py --dry-run
         python3 scripts/migrate_026_posclass.py --apply
"""
import argparse
import sqlite3
import sys
from collections import Counter

sys.path.insert(0, '.')
from core.classify import pos_class, lateral_for_formation, normalize_formation  # noqa: E402

DB = 'db/tactics.db'
MIG = '026-posclass-formation-aware'
REGIME_BY_TEAM = {'AVL': 1, 'CHE': 2, 'LIV': 3, 'ATM': 4}


def recompute(con):
    cache = {}

    def lateral(formation, regime_id):
        key = (normalize_formation(formation), regime_id)
        if key not in cache:
            cache[key] = lateral_for_formation(con, formation, regime_id)
        return cache[key]

    con.row_factory = sqlite3.Row
    rows = con.execute(
        "SELECT id, pos_class, lineup_pos, avg_x, avg_y, formation, team_code, "
        "       minutes, hit_points "
        "FROM player_matches WHERE pos_class IS NOT NULL").fetchall()

    plan, moves = [], Counter()
    for r in rows:
        new = pos_class(r['avg_x'], r['avg_y'], r['lineup_pos'],
                        lateral(r['formation'], REGIME_BY_TEAM.get(r['team_code'] or '')),
                        r['minutes'], r['hit_points'])
        if new != r['pos_class']:
            plan.append((new, r['id']))
            moves[(r['pos_class'], new)] += 1
    return rows, plan, moves


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true')
    ap.add_argument('--dry-run', action='store_true')
    a = ap.parse_args()
    if not (a.apply or a.dry_run):
        ap.error('--dry-run 또는 --apply 중 하나를 주세요')

    con = sqlite3.connect(DB)
    rows, plan, moves = recompute(con)
    to_null = sum(1 for new, _ in plan if new is None)

    print(f"대상 {len(rows)}행 · 변경 {len(plan)} (그중 NULL 전환 {to_null}) · 유지 {len(rows) - len(plan)}")
    print("\n변경 상위 15 (구 → 신):")
    for (old, new), n in moves.most_common(15):
        print(f"  {n:4d}  {old!r:22s} → {new!r}")

    if a.dry_run:
        print("\n(dry-run — 쓰지 않았습니다)")
        return

    con.execute('BEGIN IMMEDIATE')
    con.executemany("UPDATE player_matches SET pos_class=? WHERE id=?", plan)
    con.execute(
        "INSERT INTO _migration_log(run_at, v1_path, note) VALUES(date('now'), ?, ?)",
        (MIG,
         f"pos_class 전량 재계산 — 어휘 3종 혼재를 slots.pos 하나로 통일(사용자 승인 2026-09-08). "
         f"대상 {len(rows)}행 중 {len(plan)}행 변경, 그중 {to_null}행은 표본 부족(minutes<45 또는 "
         f"hit_points<15)이라 추측 대신 NULL. core/classify.py를 포메이션 인식으로 재작성했다 — "
         f"좌우값은 slots 표에서, 깊이 사전값은 이 저장소 실측 중앙값에서 가져왔고 임계값을 새로 "
         f"발명하지 않았다. pos_class는 표시 전용이라(aggregate·G3·G4·phase_split 모두 미사용) "
         f"적합도·처방은 영향받지 않는다. 변경 전 값은 직전 커밋의 db/dump/player_matches.sql에 있다."))
    con.commit()
    print(f"\n✅ 적용 완료 — {len(plan)}행 갱신, _migration_log에 {MIG} 기록")


if __name__ == '__main__':
    main()
