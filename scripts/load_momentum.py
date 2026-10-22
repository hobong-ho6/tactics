#!/usr/bin/env python3
"""SofaScore `/event/<eid>/graph` → match_momentum (2026-10-22 신설 · migration 120).

사용:
    .venv/bin/python scripts/load_momentum.py --team AVL [--since 2026-08-12] [--match 126 120] [--propose] [--dry-run]
--propose: 적재 뒤 core.momentum.propose_boundaries로 흐름 3묶음 경계를 제안하고 match_tactical_changes 분과 나란히 찍는다(보고만).
이미 있는 (match_id, minute, source) 행은 건너뛴다(불변규칙 2).
"""
import argparse
import datetime as dt
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core import DB                                   # noqa: E402
from core.db import connect as connect_db             # noqa: E402
from core.momentum import propose_boundaries, runs, sign_for_side  # noqa: E402

ORIGIN = "https://www.sofascore.com/robots.txt"
SOURCE = "SofaScore /event/{eid}/graph"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--team", required=True)
    ap.add_argument("--since", default="2026-08-12")
    ap.add_argument("--match", type=int, nargs="*")
    ap.add_argument("--pulled", default=dt.date.today().isoformat())
    ap.add_argument("--propose", action="store_true")
    ap.add_argument("--eid", nargs="*", default=[], help="matches.id=SofaScore eventId — matches.event_id가 FotMob id로 적힌 경기(#86·#94·#95) 우회")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    eid_over = {int(kv.split("=")[0]): int(kv.split("=")[1]) for kv in a.eid}
    con = connect_db(DB)
    ms = con.execute("SELECT id, event_id, date, opponent, venue FROM matches WHERE team_code=? AND date>=? "
                     "AND competition NOT LIKE '%Friendly%' AND event_id IS NOT NULL", (a.team, a.since)).fetchall()
    if a.match:
        ms = [m for m in ms if m[0] in set(a.match)]
    by_ss = {r[0]: r[1] for r in con.execute("SELECT sofascore_id, id FROM players WHERE sofascore_id IS NOT NULL")}
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(ORIGIN, wait_until="domcontentloaded")
        for mid, eid, date, opp, venue in ms:
            eid = eid_over.get(mid, eid)
            res = page.evaluate("async (e) => { const g = await fetch('/api/v1/event/'+e+'/graph').then(r=>r.ok?r.json():null);"
                                " const lu = await fetch('/api/v1/event/'+e+'/lineups').then(r=>r.ok?r.json():null);"
                                " return {g, home: lu && lu.home ? lu.home.players.map(x=>x.player.id) : []}; }", eid)
            g = (res or {}).get("g")
            if not g or not g.get("graphPoints"):
                print(mid, date, opp, "— graph 없음")
                continue
            # 우리 쪽 판정: 홈 라인업에 이 경기 player_matches 행이 있는 우리 선수가 있으면 home (venue N=중립도 이걸로)
            ours = {r[0] for r in con.execute("SELECT player_id FROM player_matches WHERE match_id=?", (mid,))}
            ours_home = any(by_ss.get(x) in ours for x in res.get("home", []))
            sgn = sign_for_side("home" if ours_home else "away")
            src = SOURCE.format(eid=eid)
            have = {r[0] for r in con.execute("SELECT minute FROM match_momentum WHERE match_id=? AND source=?", (mid, src))}
            pts, ins = [], 0
            for gp in g["graphPoints"]:
                mnt, val = float(gp["minute"]), int(gp["value"]) * sgn
                pts.append((mnt, val))
                if mnt in have:
                    continue
                if not a.dry_run:
                    con.execute("INSERT INTO match_momentum(match_id,minute,value,source,pulled) VALUES(?,?,?,?,?)",
                                (mid, mnt, val, src, a.pulled))
                ins += 1
            print(mid, date, opp, f"— {'home' if ours_home else 'away'} · 점 {len(pts)} · 적재 {ins}")
            if a.propose:
                ipts = [(int(m), v) for m, v in pts]
                rs = runs(ipts)
                print("   구간:", " · ".join(f"{r['start']}–{r['end']}′ {'+' if r['sign']>0 else '−'}{abs(r['mean'])}" for r in rs))
                print("   경계 제안:", propose_boundaries(ipts))
                tc = con.execute("SELECT tc.minute, tc.minute_to, tc.title FROM match_tactical_changes tc JOIN match_reports r ON r.id=tc.report_id "
                                 "WHERE r.match_id=? ORDER BY seq", (mid,)).fetchall()
                if tc:
                    print("   match_tactical_changes:", " · ".join(f"{m}–{mt}′ {t[:18]}" for m, mt, t in tc))
        browser.close()
    if not a.dry_run:
        con.commit()


if __name__ == "__main__":
    main()
