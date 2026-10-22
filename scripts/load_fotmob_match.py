#!/usr/bin/env python3
"""FotMob 경기별 선수 스탯(`/api/data/matchDetails?matchId=`) → player_matches.stats_json 덧붙임 (2026-10-22 신설).

왜: 상대 박스 터치·라인 브레이킹 패스·파이널서드 패스·기회 창출·피지컬(PL만)·GK 스위핑이 FotMob 경기 응답에 있는데
브라이튼전(#86) 한 경기만 들어갔다(경기 데이터 결손 검토 §3-3). 같은 호출인데 런북에 필수가 아니었다 — 이제 G21이 결손을 막는다.
⛔ FotMob API는 페이지 컨텍스트 밖(curl·WebFetch)에서 막힌다 — Playwright로 fotmob.com을 열고 **페이지 안에서 fetch**한다
   (2026-10-22 확인: `__NEXT_DATA__`에는 더 이상 경기 데이터가 없다 · 페이지 안 fetch는 200).
⭐ 키 어휘는 FotMob 내부 키(`stats[*].stats[*].key` · 시즌 수집기 `collect_fotmob_players.LABELS`와 **같은 사전**)를 그대로 쓴다.
   분수형(69/71)은 `<key>`=분자 · `<key>_total`=분모. 이미 있는 키는 덮지 않는다(불변규칙 2 · SofaScore 값이 우선).
   ⚠️ 운반(Carries)·프로그레시브 캐리는 2026-10-22 확인 시점에 **경기 응답에 없다**(UCL·PL 모두) — 실측 운반은 SofaScore
   `carries_ss`(core.sofascore.STAT_FIELDS)가 담당한다.

사용:
    .venv/bin/python scripts/load_fotmob_match.py --map 126=6106285 120=5795482 [--dry-run]
    .venv/bin/python scripts/load_fotmob_match.py --team AVL --resolve   # FotMob 팀 일정으로 matchId를 날짜 매칭해 전부
"""
import argparse
import datetime as dt
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core import DB                                   # noqa: E402
from core.db import connect as connect_db             # noqa: E402
from collect_fotmob_players import LABELS             # noqa: E402  ⭐ 라벨 사전 단일 정본

SKIP_KEYS = {None, "fantasy_points"}                  # Shotmap(불리언)·판타지 점수는 안 담는다
RENAME = {"rating_title": "fm_rating", "minutes_played": "fm_minutes"}   # SofaScore 키와 충돌하는 둘만 접두


def fetch_match(page, fm_id):
    st, txt = page.evaluate("async (m) => { const r = await fetch('/api/data/matchDetails?matchId='+m); "
                            "return [r.status, await r.text()]; }", str(fm_id))
    if st != 200:
        return None
    return json.loads(txt)


def resolve_ids(page, team_fotmob_id, since):
    fx = page.evaluate("async (t) => { const r = await fetch('/api/data/teams?id='+t+'&ccode3=KOR'); const j = await r.json();"
                       " return ((j.fixtures||{}).allFixtures||{}).fixtures||[]; }", str(team_fotmob_id))
    out = {}
    for f in fx:
        d = ((f.get("status") or {}).get("utcTime") or "")[:10]
        if d >= since:
            out[d] = (f["id"], f["home"]["name"], f["away"]["name"])
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--team", default="AVL")
    ap.add_argument("--map", nargs="*", default=[], help="matches.id=fotmobMatchId")
    ap.add_argument("--resolve", action="store_true", help="FotMob 팀 일정으로 날짜 매칭(공식전 전부)")
    ap.add_argument("--since", default="2026-08-12")
    ap.add_argument("--pulled", default=dt.date.today().isoformat())
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    con = connect_db(DB)
    by_fm = {r[0]: r[1] for r in con.execute("SELECT fotmob_id, id FROM players WHERE fotmob_id IS NOT NULL")}
    pairs = [(int(kv.split("=")[0]), int(kv.split("=")[1])) for kv in a.map]
    from playwright.sync_api import sync_playwright
    unknown_keys, report = set(), []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("https://www.fotmob.com/", wait_until="domcontentloaded", timeout=90_000)
        page.wait_for_timeout(1500)
        if a.resolve:
            tfm = con.execute("SELECT fotmob_id FROM teams WHERE code=?", (a.team,)).fetchone()[0]
            byd = resolve_ids(page, tfm, a.since)
            for mid, date in con.execute("SELECT id, date FROM matches WHERE team_code=? AND date>=? AND competition NOT LIKE '%Friendly%'",
                                         (a.team, a.since)).fetchall():
                # UTC 날짜와 현지 날짜가 하루 어긋날 수 있다 — ±1일
                for dd in (date, (dt.date.fromisoformat(date) - dt.timedelta(days=1)).isoformat(),
                           (dt.date.fromisoformat(date) + dt.timedelta(days=1)).isoformat()):
                    if dd in byd and mid not in {m for m, _ in pairs}:
                        pairs.append((mid, byd[dd][0]))
                        break
        for mid, fm_id in pairs:
            d = fetch_match(page, fm_id)
            ps = ((d or {}).get("content") or {}).get("playerStats") or {}
            if not ps:
                report.append((mid, fm_id, "playerStats 없음"))
                continue
            rows = {r[1]: (r[0], r[2]) for r in con.execute("SELECT id, player_id, stats_json FROM player_matches WHERE match_id=?", (mid,))}
            n_upd = n_keys = n_nomap = 0
            for fmpid, v in ps.items():
                pid = by_fm.get(int(fmpid))
                if not pid or pid not in rows:
                    n_nomap += 1 if pid is None and v.get("teamName") and v.get("teamId") else 0
                    continue
                rid, sj = rows[pid]
                cur = json.loads(sj) if sj else {}
                add = {}
                for sec in v.get("stats", []):
                    for title, item in (sec.get("stats") or {}).items():
                        if not isinstance(item, dict):
                            continue
                        key = item.get("key")
                        if key in SKIP_KEYS:
                            continue
                        key = RENAME.get(key, key)
                        if key not in LABELS and key not in RENAME.values():
                            unknown_keys.add((key, title))
                        st = item.get("stat") or {}
                        val = st.get("value")
                        if val is None or key in cur:
                            continue
                        add[key] = val
                        if st.get("total") is not None and f"{key}_total" not in cur:
                            add[f"{key}_total"] = st["total"]
                if add:
                    add["fm_match_pulled"] = a.pulled
                    add["fm_match_id"] = fm_id
                    cur.update(add)
                    n_upd += 1
                    n_keys += len(add)
                    if not a.dry_run:
                        con.execute("UPDATE player_matches SET stats_json=? WHERE id=?", (json.dumps(cur, ensure_ascii=False), rid))
            report.append((mid, fm_id, f"선수 {len(ps)} · 우리 행 {len(rows)} · 갱신 {n_upd} · 키 +{n_keys}"))
        browser.close()
    if not a.dry_run:
        con.commit()
    for r in report:
        print(*r)
    if unknown_keys:
        print("⚠️ LABELS에 없는 키(저장은 했다 — collect_fotmob_players.LABELS에 라벨을 추가할 것):", sorted(unknown_keys))


if __name__ == "__main__":
    main()
