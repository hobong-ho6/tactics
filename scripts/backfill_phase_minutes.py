#!/usr/bin/env python3
"""`player_matches.stats_json`의 스코어 국면 분(phase_lead/level/trail) 결손 보충 (2026-10-22 신설).

원료는 **이미 적재된 `match_events`**(goal·penalty_goal·own_goal = 득점 · sub = 교체 투입 분)다 —
SofaScore를 다시 부르지 않는다. 계산은 core.phase_minutes 하나만 쓴다(불변규칙 4·13 ②).
⛔ stats_json의 다른 키는 건드리지 않고 phase_* 세 키만 **없을 때** 덧붙인다(불변규칙 2).
⛔ 득점 사건이 0건인 경기는 0-0으로 해석하지 않는다 — match_events에 득점이 없고 결과가 0-0이 아니면 건너뛰고 보고한다.

사용:
    .venv/bin/python scripts/backfill_phase_minutes.py --dry-run
    .venv/bin/python scripts/backfill_phase_minutes.py --team AVL
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from core import DB                                   # noqa: E402
from core.db import connect as connect_db             # noqa: E402
from core.phase_minutes import LEAD, LEVEL, TRAIL, phase_minutes, score_timeline  # noqa: E402

GOAL_KINDS = ("goal", "penalty_goal", "own_goal")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--team", default=None)
    ap.add_argument("--since", default="2026-07-01", help="이 날짜 이후 경기만(기본 26/27 프리시즌부터 — 그 전 v1 승계 경기는 match_events가 없다)")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    con = connect_db(DB)
    q = ("SELECT DISTINCT m.id, m.date, m.opponent, m.result FROM player_matches pm JOIN matches m ON m.id=pm.match_id "
         "WHERE json_extract(pm.stats_json,'$.phase_lead') IS NULL AND pm.match_id IS NOT NULL")
    args = ()
    q += " AND m.date>=?"
    args = (a.since,)
    if a.team:
        q += " AND m.team_code=?"
        args += (a.team,)
    done, skipped = 0, []
    for mid, date, opp, result in con.execute(q + " ORDER BY m.date", args).fetchall():
        goals = con.execute("SELECT minute, side FROM match_events WHERE match_id=? AND kind IN (?,?,?)",
                            (mid, *GOAL_KINDS)).fetchall()
        if not goals and (result or "") not in ("0-0", ""):
            skipped.append(f"#{mid} {date} {opp} {result}: match_events에 득점 0건")
            continue
        if not con.execute("SELECT 1 FROM match_events WHERE match_id=? LIMIT 1", (mid,)).fetchone():
            skipped.append(f"#{mid} {date} {opp}: match_events 없음")
            continue
        # ⛔ 득점 사건 수가 결과(a-b)와 다르면 타임라인이 틀리므로 넣지 않는다(결손을 0으로 만들지 않는다).
        parts = (result or "").split()[0].split("-") if result else []
        if len(parts) == 2 and all(x.isdigit() for x in parts) and len(goals) != int(parts[0]) + int(parts[1]):
            skipped.append(f"#{mid} {date} {opp} {result}: match_events 득점 {len(goals)}건 ≠ 결과 합 — 사건 수집 결손")
            continue
        tl = score_timeline(goals)
        subs = {r[0]: r[1] for r in con.execute(
            "SELECT player_id, minute FROM match_events WHERE match_id=? AND kind='sub' AND side='v' AND player_id IS NOT NULL",
            (mid,))}
        rows = con.execute("SELECT id, player_id, minutes, started, stats_json FROM player_matches "
                           "WHERE match_id=? AND json_extract(stats_json,'$.phase_lead') IS NULL", (mid,)).fetchall()
        n = 0
        for rid, pid, minutes, started, sj in rows:
            ph = phase_minutes(tl, minutes, started, subs.get(pid))
            if ph is None:
                continue
            d = json.loads(sj or "{}")
            d.update(ph)
            if not a.dry_run:
                con.execute("UPDATE player_matches SET stats_json=? WHERE id=?", (json.dumps(d, ensure_ascii=False), rid))
            n += 1
        print(f"#{mid} {date} {opp} {result}: 득점 {len(goals)} · 교체 분 {len(subs)} · {n}/{len(rows)}행 보충")
        done += n
    if not a.dry_run:
        con.commit()
    print(f"{'[dry-run] ' if a.dry_run else ''}합계 {done}행")
    for s in skipped:
        print("  ⚠️ 건너뜀:", s)


if __name__ == "__main__":
    main()
