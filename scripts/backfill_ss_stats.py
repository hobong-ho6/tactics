#!/usr/bin/env python3
"""SofaScore 선수 statistics 확장 필드 소급 — 기존 player_matches 행에 **빠진 키만** 덧붙인다 (2026-10-22 신설).

왜: `core.sofascore.STAT_FIELDS`가 19필드였고 lineups.players[].statistics는 70여 필드를 준다(롱볼·크로스·드리블·
공중·GK 스위핑·⭐ 실측 운반 ballCarriesCount). 어휘 정본은 STAT_FIELDS 하나다 — 이 스크립트는 그 목록을 **같은 호출**
(`/api/v1/event/<eid>/lineups`)로 다시 받아 `stats_json`에 없는 키만 추가한다(있는 값은 절대 덮지 않는다 · 불변규칙 2).
새 수집(`collect_event.py`)은 STAT_FIELDS를 그대로 직렬화하므로 앞으로의 회차엔 이 스크립트가 필요 없다.

사용:
    .venv/bin/python scripts/backfill_ss_stats.py --team AVL [--since 2026-08-12] [--match 126] [--dry-run]
"""
import argparse
import datetime as dt
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core import DB                                   # noqa: E402
from core.db import connect as connect_db             # noqa: E402
from core.sofascore import FLOATS, STAT_FIELDS        # noqa: E402

ORIGIN = "https://www.sofascore.com/robots.txt"


def fetch_lineups(page, event_id):
    return page.evaluate("async (e) => { const r = await fetch('/api/v1/event/'+e+'/lineups'); "
                         "return r.ok ? await r.json() : {status:r.status}; }", event_id)


def conv(name, raw):
    if raw is None:
        return None
    if name in FLOATS:
        return float(raw)
    if name == "minutes":
        return int(raw)
    return int(raw)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--team", required=True)
    ap.add_argument("--since", default="2026-08-12")
    ap.add_argument("--match", type=int, nargs="*", help="matches.id 지정(없으면 공식전 전부)")
    ap.add_argument("--pulled", default=dt.date.today().isoformat())
    ap.add_argument("--eid", nargs="*", default=[], help="matches.id=SofaScore eventId — matches.event_id가 FotMob id로 적힌 경기(#86·#94·#95) 우회")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    eid_over = {int(kv.split("=")[0]): int(kv.split("=")[1]) for kv in a.eid}
    con = connect_db(DB)
    q = ("SELECT id, event_id, date, opponent FROM matches WHERE team_code=? AND date>=? "
         "AND competition NOT LIKE '%Friendly%' AND event_id IS NOT NULL")
    ms = con.execute(q, (a.team, a.since)).fetchall()
    if a.match:
        ms = [m for m in ms if m[0] in set(a.match)]
    by_ss = {r[0]: r[1] for r in con.execute("SELECT sofascore_id, id FROM players WHERE sofascore_id IS NOT NULL")}
    from playwright.sync_api import sync_playwright
    report = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(ORIGIN, wait_until="domcontentloaded")
        for mid, eid, date, opp in ms:
            eid = eid_over.get(mid, eid)
            lu = fetch_lineups(page, eid)
            if not lu or "home" not in lu:
                report.append((mid, date, opp, "lineups 실패", lu))
                continue
            stats_by_pid = {}
            for sd in ("home", "away"):
                for pl in lu[sd].get("players", []):
                    pid = by_ss.get(pl["player"]["id"])
                    if pid and pl.get("statistics"):
                        stats_by_pid[pid] = pl["statistics"]
            rows = con.execute("SELECT id, player_id, stats_json FROM player_matches WHERE match_id=?", (mid,)).fetchall()
            n_upd = n_keys = n_miss = 0
            for rid, pid, sj in rows:
                st = stats_by_pid.get(pid)
                if not st:
                    n_miss += 1
                    continue
                cur = json.loads(sj) if sj else {}
                add = {}
                for name, api in STAT_FIELDS:
                    if name in cur:
                        continue
                    if api not in st:
                        # SofaScore는 0인 키를 생략한다 — 「키 생략 = 0 확정」(docs/30 ① · parse_collected와 같은 규칙). 실수형은 결손(None).
                        if name in FLOATS or name == "minutes":
                            continue
                        add[name] = 0
                        continue
                    v = conv(name, st.get(api))
                    if v is not None:
                        add[name] = v
                if add:
                    add["ss_ext_pulled"] = a.pulled
                    cur.update(add)
                    n_upd += 1
                    n_keys += len(add)
                    if not a.dry_run:
                        con.execute("UPDATE player_matches SET stats_json=? WHERE id=?",
                                    (json.dumps(cur, ensure_ascii=False), rid))
            report.append((mid, date, opp, f"행 {len(rows)} · 갱신 {n_upd} · 키 +{n_keys} · 통계 없음 {n_miss}", None))
        browser.close()
    if not a.dry_run:
        con.commit()
    for r in report:
        print(r[0], r[1], r[2], "—", r[3], (r[4] if r[4] else ""))


if __name__ == "__main__":
    main()
