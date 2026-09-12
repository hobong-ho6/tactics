#!/usr/bin/env python3
"""collect_sofascore.py(선수 축) · collect_event.py(이벤트 축) JSON → player_matches 적재.

왜 (2026-09-12 신설): 두 수집기는 JSON만 남기고 DB에 쓰지 않는다. 기존 `load_matches.py`는 브라우저 파이프
텍스트 전용이라 이 JSON을 못 읽는다. ⭐ team_code는 「그 경기에서 소속」이므로 적재 시점에 반드시 채운다
(obs#618 규약: NULL은 미배정이지 해당 없음이 아니다).

  선수 축:  load_sofascore_json.py /tmp/ss_musso.json --player-id 164 --club ATM --nat ARG
            [--club-before 2026-09-01=JUV ...]  (그 날짜 이전 클럽 경기의 코드 — 시즌 중 이적)
  이벤트 축: load_sofascore_json.py /tmp/ev_liv.json --event --team LIV --regime 3

이미 있는 (player_id, event_id)는 건너뛴다(불변규칙 2). 미등록 선수(이벤트 축)는 적재하지 않고 보고한다.
pos_class는 core.classify.pos_class — 이벤트 축은 포메이션 인식(lateral), 선수 축은 좌표 폴백.
"""
import argparse
import json
import re
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core import DB                                   # noqa: E402
from core.classify import lateral_for_formation, normalize_formation, pos_class  # noqa: E402
from core.encode import encode                        # noqa: E402
from core.sofascore import FLOATS, STAT_FIELDS        # noqa: E402

NT_RE = re.compile(r"World Cup Qual|FIFA World Cup|Africa Cup|Nations League|International Friendly|Euro.*Qual|"
                   r"Copa America|Championship Qual|Asian Cup|Gold Cup|^EURO$|U-?2[01]|U-?1[6789]|European Championship",
                   re.I)
CLUB_YOUTH = re.compile(r"Youth League|Primavera|Juvenil|Premier League 2|International Cup", re.I)


def is_nt(comp):
    comp = comp or ""
    if "Club World Cup" in comp or CLUB_YOUTH.search(comp):
        return False
    return bool(NT_RE.search(comp))


def season_of(date):
    y, m = int(date[:4]), int(date[5:7])
    return f"{y}-{str(y+1)[2:]}" if m >= 7 else f"{y-1}-{str(y)[2:]}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--event", action="store_true", help="collect_event.py 산출(이벤트 축)")
    ap.add_argument("--team", help="[이벤트 축] 우리 팀 코드")
    ap.add_argument("--regime", type=int, help="[이벤트 축] 포메이션 인식 pos_class용 regime_id")
    ap.add_argument("--player-id", type=int, help="[선수 축]")
    ap.add_argument("--club", help="[선수 축] 기본 클럽 코드")
    ap.add_argument("--club-before", nargs="*", default=[], help="[선수 축] DATE=CODE — 그 날짜 이전 클럽 경기 코드")
    ap.add_argument("--nat", help="[선수 축] 대표팀(연령별 포함) 코드")
    ap.add_argument("--pulled", default="2026-09-12")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    con = sqlite3.connect(DB)
    have = {(r[0], r[1]) for r in con.execute("SELECT player_id, event_id FROM player_matches WHERE event_id IS NOT NULL")}
    codes = {r[0] for r in con.execute("SELECT code FROM teams")}
    data = json.load(open(a.path, encoding="utf-8"))
    rows, unmatched = [], []

    if a.event:
        assert a.team and a.regime, "--team --regime 필수"
        lateral = lateral_for_formation(con, normalize_formation(data.get("formation_v") or ""), a.regime)
        by_ss = {r[0]: r[1] for r in con.execute("SELECT sofascore_id, id FROM players WHERE sofascore_id IS NOT NULL")}
        src = (f"SofaScore lineups/heatmap/average-positions event={data['event_id']} (core.sofascore.js_event_collect, "
               f"scripts/collect_event.py Playwright, {a.pulled} 수집) → scripts/load_sofascore_json.py")
        for pl in data["players"]:
            pid = by_ss.get(pl["sofascore_id"])
            if not pid:
                unmatched.append((pl["sofascore_id"], pl["name"], pl["shirt"]))
                continue
            p = pl["row"].split("|")
            eid, date, comp, opp, venue, started, hp, lpos, ax, ay = (int(p[0]), p[1], p[2], p[3], p[4], int(p[5]),
                                                                     int(p[6]), p[7], p[8], p[9])
            stats = {}
            for (name, _), raw in zip(STAT_FIELDS, p[10:10 + len(STAT_FIELDS)]):
                stats[name] = (float(raw) if raw else None) if name in FLOATS else (
                    (int(raw) if raw else None) if name == "minutes" else (int(raw) if raw else 0))
            cells = p[-1].replace(".", ",") if p[-1] else None
            rows.append(dict(player_id=pid, event_id=eid, team_code=a.team, date=date, competition=comp or None,
                             opponent=opp or None, venue=venue, started=started, hit_points=hp, lineup_pos=lpos or None,
                             avg_x=float(ax) if ax else None, avg_y=float(ay) if ay else None, cells=cells,
                             formation=normalize_formation(data.get("formation_v") or "") or None,
                             stats=stats, lateral=lateral, source=src,
                             confidence=f"measured. 대회={comp}. 45분 미만 출전은 시즌 집계 기준(45분+·hit_points 15+) 밖이며 리포트용. "
                                        f"결손은 NULL(0 아님). ⚠️ 국면 그리드(cells_poss/def)·possession 미수집 — 후속 회차."))
    else:
        assert a.player_id and a.club, "--player-id --club 필수"
        before = sorted((kv.split("=")[0], kv.split("=")[1]) for kv in a.club_before)
        src = (f"SofaScore API player events/last+heatmap+statistics (scripts/collect_sofascore.py Playwright, {a.pulled} 수집) "
               f"→ scripts/load_sofascore_json.py")
        for r in data:
            comp = r.get("competition")
            if is_nt(comp):
                code = a.nat
                if not code:
                    unmatched.append((r["event_id"], comp, "대표팀 코드(--nat) 없음"))
                    continue
            else:
                code = a.club
                for d, c in before:
                    if r["date"] < d:
                        code = c
                        break
            stats = {k: r.get(k) for k, _ in STAT_FIELDS}
            rows.append(dict(player_id=a.player_id, event_id=r["event_id"], team_code=code, date=r["date"], competition=comp,
                             opponent=r.get("opponent"), venue=r.get("venue"), started=r.get("started"),
                             hit_points=r.get("hit_points") or 0, lineup_pos=r.get("lineup_pos") or None,
                             avg_x=r.get("avg_x"), avg_y=r.get("avg_y"), cells=r.get("cells"), formation=None,
                             stats=stats, lateral=None, source=src,
                             confidence="measured. 선수 축 수집(이벤트별 라인업·팀 포메이션 미수집 → pos_class는 좌표 폴백). "
                                        "결손은 NULL(0 아님). team_code는 대회 성격(대표팀 정규식)·이적일 규칙으로 배정."))

    missing_codes = {r["team_code"] for r in rows} - codes
    assert not missing_codes, f"teams에 없는 코드: {missing_codes} — 먼저 등재할 것"
    ins = skip = 0
    for r in rows:
        if (r["player_id"], r["event_id"]) in have:
            skip += 1
            continue
        s = r["stats"]
        cells_l = [int(x) for x in r["cells"].split(",")] if r["cells"] else None
        pc = pos_class(r["avg_x"], r["avg_y"], r["lineup_pos"], lateral=r["lateral"],
                       minutes=s.get("minutes"), hit_points=r["hit_points"]) if r["avg_x"] is not None else None
        if not a.dry_run:
            con.execute("""INSERT INTO player_matches(player_id,event_id,team_code,season,date,opponent,venue,competition,
                minutes,rating,started,lineup_pos,pos_class,formation,avg_x,avg_y,hit_points,cells,map25,
                xg,xa,key_passes,duels_won,duels_lost,tackles,interceptions,goals,assists,touches,recoveries,
                stats_json,source,confidence)
                VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                        (r["player_id"], r["event_id"], r["team_code"], season_of(r["date"]), r["date"], r["opponent"], r["venue"],
                         r["competition"], s.get("minutes"), s.get("rating"), r["started"], r["lineup_pos"], pc, r["formation"],
                         r["avg_x"], r["avg_y"], r["hit_points"], r["cells"], encode(cells_l) if cells_l else None,
                         s.get("xg"), s.get("xa"), s.get("key_passes"), s.get("duels_won"), s.get("duels_lost"), s.get("tackles"),
                         s.get("interceptions"), s.get("goals"), s.get("assists"), s.get("touches"), s.get("recoveries"),
                         json.dumps({k: v for k, v in s.items() if v is not None}, ensure_ascii=False), r["source"], r["confidence"]))
        have.add((r["player_id"], r["event_id"]))
        ins += 1
    if not a.dry_run:
        con.commit()
    by_code = {}
    for r in rows:
        by_code[r["team_code"]] = by_code.get(r["team_code"], 0) + 1
    print(f"{Path(a.path).name}: 적재 {ins} · 기존 건너뜀 {skip} · 코드 분포 {by_code}")
    if unmatched:
        print("  ⚠️ 미적재:", unmatched)


if __name__ == "__main__":
    main()
