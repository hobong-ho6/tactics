#!/usr/bin/env python3
"""브라우저 수집분(window.__RES 파이프 텍스트) → player_matches 적재.

core.sofascore.parse_collected와 같은 필드 순서를 쓰되, 맨 앞에 player_id가 붙은
다중 선수 변형을 읽는다. 이미 있는 (player_id, event_id)는 건너뛴다 — 불변규칙 2.

사용: python3 scripts/load_matches.py /tmp/fm/matches.txt
"""
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core import DB
from core.encode import encode
from core.sofascore import FLOATS, STAT_FIELDS

SRC = "SofaScore API (2026-08-11 전수 수집 — heatmap+statistics+average-positions)"


def season_of(date):
    y, m = int(date[:4]), int(date[5:7])
    return f"{y}-{str(y+1)[2:]}" if m >= 7 else f"{y-1}-{str(y)[2:]}"


def main(path):
    con = sqlite3.connect(DB)
    have = {(r[0], r[1]) for r in con.execute(
        "SELECT player_id, event_id FROM player_matches WHERE event_id IS NOT NULL")}
    ins = skip = 0
    for ln in Path(path).read_text(encoding="utf-8").splitlines():
        if not ln.strip():
            continue
        p = ln.split("|")
        base = 8 + len(STAT_FIELDS) + 1
        # 마지막에 team_code가 붙은 변형도 받는다 (타 팀 수집분)
        team = "AVL"
        if len(p) == base + 1:
            team = p.pop()
        elif len(p) != base:
            raise ValueError(f"필드 수 불일치({len(p)} != {base}): {ln[:80]}")
        pid, eid, date, comp, hp, lineup_pos = int(p[0]), int(p[1]), p[2], p[3], int(p[4]), p[5]
        if (pid, eid) in have:
            skip += 1
            continue
        stats = {}
        for (name, _), raw in zip(STAT_FIELDS, p[8:8 + len(STAT_FIELDS)]):
            if name in FLOATS:
                stats[name] = float(raw) if raw else None
            elif name == "minutes":
                stats[name] = int(raw) if raw else None
            else:
                stats[name] = int(raw) if raw else 0    # 키 생략 = 0 확정 (docs/30 ①)
        cells = p[-1].replace(".", ",") if p[-1] else None
        con.execute("""INSERT INTO player_matches(player_id,event_id,team_code,season,date,competition,
            minutes,rating,lineup_pos,avg_x,avg_y,hit_points,cells,map25,
            xg,xa,key_passes,duels_won,duels_lost,tackles,interceptions,goals,assists,touches,recoveries,
            source,confidence)
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,'measured')""",
                    (pid, eid, team, season_of(date), date, comp or None,
                     stats["minutes"], stats["rating"], lineup_pos or None,
                     float(p[6]) if p[6] else None, float(p[7]) if p[7] else None,
                     hp, cells, encode([int(x) for x in cells.split(",")]) if cells else None,
                     stats["xg"], stats["xa"], stats["key_passes"], stats["duels_won"],
                     stats["duels_lost"], stats["tackles"], stats["interceptions"],
                     stats["goals"], stats["assists"], stats["touches"], stats["recoveries"], SRC))
        ins += 1
    con.commit()
    print(f"적재 {ins}행 · 기존 중복 건너뜀 {skip}행")


if __name__ == "__main__":
    main(sys.argv[1])
