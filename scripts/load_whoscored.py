#!/usr/bin/env python3
"""WhoScored matchCentreData → 국면 그리드(선수) + PPDA·def_x(팀). match-watch §2·§3용.

지금까지 회차마다 손으로 짜던 단계다(불변규칙 4 — core 밖 재구현 금지). 계산은 전부
`core.whoscored`가 하고 이 스크립트는 **이름 매칭과 DB 쓰기**만 맡는다.

사용:
    .venv/bin/python scripts/load_whoscored.py /tmp/ws_liv.json \
        --event 16363648 --team LIV --side away --ws-match 1983571 [--apply]

`--apply` 없이 돌리면 매칭 결과와 팀 지표만 출력한다(미매칭 확인용).
미매칭 이름은 `--map "WhoScored 이름=우리 player_id"`로 수동 지정한다
 (docs/30 오인식 대조표 — `Jonathan David ↔ Dávid Hancko` 류가 실제로 재발했다).
"""
import argparse
import json
import sqlite3
import sys
import unicodedata
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from core.whoscored import DEF_X_METHOD, PPDA_METHOD, def_x, phase_cells, ppda, set_pieces  # noqa: E402
from core.db import connect as connect_db  # noqa: E402  ⭐ DB 연결 정본(대기·작성 중 표시)

DB = ROOT / "db" / "tactics.db"


def norm(s):
    s = unicodedata.normalize("NFKD", s or "")
    return "".join(c for c in s if not unicodedata.combining(c)).lower().replace("-", " ").strip()


def match_players(con, event_id, names, manual):
    """우리 player_matches 행 ↔ WhoScored playerId 매칭. (쌍 리스트, 미매칭 이름 리스트)"""
    rows = con.execute("SELECT m.player_id, COALESCE(p.name_kr, p.name), p.name "
                       "FROM player_matches m JOIN players p ON p.id=m.player_id "
                       "WHERE m.event_id=?", (event_id,)).fetchall()
    by_token = {}
    for pid, _kr, name in rows:
        for tok in norm(name).split():
            by_token.setdefault(tok, set()).add(pid)

    pairs, unmatched = [], []
    for ws_id, ws_name in names.items():
        if ws_name in manual:
            pairs.append((int(ws_id), manual[ws_name], ws_name))
            continue
        hit = set.intersection(*[by_token.get(t, set()) for t in norm(ws_name).split()]) \
            if all(t in by_token for t in norm(ws_name).split()) else set()
        if len(hit) != 1:
            # 성(마지막 토큰) 단독으로 한 번 더 — "Alisson Becker" ↔ "Alisson" 류
            hit = by_token.get(norm(ws_name).split()[-1], set())
        if len(hit) == 1:
            pairs.append((int(ws_id), hit.pop(), ws_name))
        else:
            unmatched.append(ws_name)
    return pairs, unmatched


def load_set_pieces(con, d, events, a, pairs, src):
    """코너·FK·PK 키커/타깃을 match_set_pieces에 쓴다(migration 117 · 계산은 core.whoscored.set_pieces).
    같은 match_id에 행이 이미 있으면 건너뛴다(불변규칙 2 — 재수집은 사람이 판단). 상대 선수는 player_id 없이 note에 이름만."""
    us = d["home"] if a.side == "home" else d["away"]
    mrow = con.execute("SELECT id FROM matches WHERE event_id=? AND team_code=?", (a.event, a.team)).fetchone()
    if not mrow:
        print(f"⚠️ matches에 event_id={a.event} {a.team} 행이 없다 — 세트피스 생략(팀 스탯 적재 뒤 다시 돌릴 것)")
        return
    match_id = mrow[0]
    have = con.execute("SELECT COUNT(*) FROM match_set_pieces WHERE match_id=?", (match_id,)).fetchone()[0]
    if have and not getattr(a, "sp_merge", False):
        print(f"세트피스: match {match_id}에 이미 {have}행 — 생략(--sp-merge면 키커 결손 행을 채우고 없는 장면만 추가)")
        return
    rrow = con.execute("SELECT id FROM match_reports WHERE event_id=? AND team_code=?", (a.event, a.team)).fetchone()
    report_id = rrow[0] if rrow else None
    ws2pid = {ws_id: pid for ws_id, pid, _ in pairs}
    names = d.get("playerIdNameDictionary", {})
    n, merged, kept = 0, [], []
    # ⭐ 병합 후보는 **이 실행 전에 있던 행**뿐이고, 한 행은 한 번만 짝이 된다 — 같은 분의 두 코너가 한 행에 겹쳐 쓰이거나
    #    방금 넣은 행이 다음 WS 행과 짝지어지는 사고(2026-10-22 바이킹전 fk 41·코너 48·66 실증)를 막는다.
    pool = {row[0] for row in con.execute("SELECT id FROM match_set_pieces WHERE match_id=?", (match_id,))} if have else set()
    for r in set_pieces(events):
        side = "v" if r["team_id"] == us["teamId"] else "o"
        taker, target = ws2pid.get(r["taker"]), ws2pid.get(r["target"])
        note = None
        if side == "o" or (r["taker"] and taker is None) or (r["target"] and target is None):
            note = "WS " + " → ".join(names.get(str(x), str(x)) for x in (r["taker"], r["target"]) if x)
        if have:
            # ⭐ --sp-merge(2026-10-22): SS 슛맵으로 먼저 넣어 둔 행(키커 NULL)이 있으면 같은 장면(kind·side·분 ±1)을 찾아
            #    키커·타깃·방향만 채운다(outcome은 SS 슛 결과를 유지). 짝이 없는 장면(슛으로 안 끝난 코너 등)만 새 행.
            hit = None
            for cand in con.execute("""SELECT id, taker_id, target_id, flank FROM match_set_pieces
                                       WHERE match_id=? AND kind=? AND side=? AND ABS(minute-?)<=1
                                       ORDER BY ABS(minute-?), id""",
                                    (match_id, r["kind"], side, r["minute"], r["minute"])):
                if cand[0] in pool:
                    hit = cand
                    break
            if hit:
                hid, t0, g0, f0 = hit
                pool.discard(hid)
                if t0 is None or g0 is None or f0 is None:
                    con.execute("""UPDATE match_set_pieces SET taker_id=COALESCE(taker_id,?), target_id=COALESCE(target_id,?),
                                   flank=COALESCE(flank,?), note=COALESCE(note,'') || ?, source=source || ?,
                                   confidence=confidence || ? WHERE id=?""",
                                (taker, target, r["flank"],
                                 " · [WS 보강] " + (note or " → ".join(names.get(str(x), str(x)) for x in (r["taker"], r["target"]) if x)),
                                 " · " + src + " 키커/타깃/방향 보강(--sp-merge)",
                                 " · 키커 WS qualifier 직접(HIGH) · 타깃=킥 뒤 20초 안 같은 팀 첫 볼 이벤트(추정)", hid))
                    merged.append(hid)
                else:
                    kept.append(hid)
                continue
        con.execute("""INSERT INTO match_set_pieces(match_id,report_id,kind,minute,side,taker_id,target_id,flank,outcome,note,source,confidence)
                       VALUES(?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (match_id, report_id, r["kind"], r["minute"], side, taker, target, r["flank"], r["outcome"], note,
                     src + " · core.whoscored.set_pieces(qualifier CornerTaken/FreekickTaken/Penalty/DirectFreekick)",
                     "HIGH — Opta qualifier 직접 추출 · 타깃=킥 뒤 20초 안 같은 팀 첫 볼 이벤트(추정)"))
        n += 1
    con.commit()
    if have:
        print(f"세트피스 병합: 기존 행 보강 {len(merged)}(id {merged}) · 이미 채워져 유지 {len(kept)} · 새 행 {n}")
    print(f"세트피스 {n}행 → match_set_pieces(match {match_id} · report {report_id})"
          + ("" if n else " ⚠️ 0건 — qualifier가 없는 축약 전사본이면 scope=full로 다시 받을 것"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("json_path")
    ap.add_argument("--event", type=int, required=True, help="SofaScore event_id")
    ap.add_argument("--team", required=True)
    ap.add_argument("--side", choices=["home", "away"], required=True, help="우리 팀이 어느 쪽인가")
    ap.add_argument("--ws-match", type=int, required=True)
    ap.add_argument("--map", action="append", default=[], help='"WhoScored 이름=player_id"')
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--sp-merge", action="store_true",
                    help="match_set_pieces에 이미 행이 있어도 키커 NULL 행을 WS로 채우고 없는 장면만 추가(2026-10-22)")
    a = ap.parse_args()

    d = json.loads(Path(a.json_path).read_text())
    events = d["events"]
    us, them = (d["home"], d["away"]) if a.side == "home" else (d["away"], d["home"])
    manual = {k: int(v) for k, v in (m.split("=", 1) for m in a.map)}

    pv, nv, dv = ppda(events, us["teamId"], them["teamId"])
    po, no, do = ppda(events, them["teamId"], us["teamId"])
    xv, sv = def_x(events, us["teamId"])
    xo, so = def_x(events, them["teamId"])
    today = date.today().isoformat()

    # ⚠️ 저장소에 남긴 축약본(reports/match-watch/data/*-ws-*.json)은 ftScore 대신 score만 있다(2026-10-22)
    print(f"{d['home']['name']} {d.get('ftScore') or d.get('score')} {d['away']['name']} — 이벤트 {len(events)}건")
    print(f"PPDA  {a.team} {pv} ({nv}/{dv})  상대 {po} ({no}/{do})")
    print(f"def_x {a.team} {xv} (n={sv})  상대 {xo} (n={so})")

    con = connect_db(DB)
    # 우리 팀 선수만 매칭 대상이다 — 상대 이름이 섞이면 토큰 충돌이 늘어난다.
    our_ids = {e["playerId"] for e in events
               if e.get("teamId") == us["teamId"] and e.get("playerId") is not None}
    names = {k: v for k, v in d["playerIdNameDictionary"].items() if int(k) in our_ids}
    pairs, unmatched = match_players(con, a.event, names, manual)
    print(f"매칭 {len(pairs)}명 · 미매칭 {len(unmatched)}: {unmatched}")

    src = f"pulled={today} · scope=full · whoscored matchId={a.ws_match}"
    if a.apply:
        for ws_id, pid, _ in pairs:
            c = phase_cells(events, ws_id)
            con.execute("UPDATE player_matches SET cells_poss=?, cells_def=?, map25_poss=?, "
                        "map25_def=?, phase_source=? WHERE player_id=? AND event_id=?",
                        (c["cells_poss"], c["cells_def"], c["map25_poss"], c["map25_def"],
                         src, pid, a.event))
        con.commit()
        print(f"적용 {len(pairs)}행 · phase_source='{src}'")
        load_set_pieces(con, d, events, a, pairs, src)
    else:
        print("(--apply 없음 — 쓰기 생략)")
        sp = set_pieces(events)
        print(f"세트피스 후보 {len(sp)}건(우리 {sum(1 for r in sp if r['team_id'] == us['teamId'])}) — --apply 때 match_set_pieces에 쓴다")

    print(json.dumps({"ppda_v": pv, "ppda_num_v": nv, "ppda_den_v": dv,
                      "ppda_o": po, "ppda_num_o": no, "ppda_den_o": do,
                      "def_x_v": xv, "def_x_n_v": sv, "def_x_o": xo, "def_x_n_o": so,
                      "ppda_method": PPDA_METHOD + f" matchId={a.ws_match} ({today} 수집)",
                      "def_x_method": DEF_X_METHOD + f" matchId={a.ws_match} · 표본 "
                                      f"{a.team} {sv}·상대 {so} ({today} 수집)"}, ensure_ascii=False))
    con.close()


if __name__ == "__main__":
    main()
