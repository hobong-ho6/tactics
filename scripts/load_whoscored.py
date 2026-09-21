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
from core.whoscored import DEF_X_METHOD, PPDA_METHOD, def_x, phase_cells, ppda  # noqa: E402

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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("json_path")
    ap.add_argument("--event", type=int, required=True, help="SofaScore event_id")
    ap.add_argument("--team", required=True)
    ap.add_argument("--side", choices=["home", "away"], required=True, help="우리 팀이 어느 쪽인가")
    ap.add_argument("--ws-match", type=int, required=True)
    ap.add_argument("--map", action="append", default=[], help='"WhoScored 이름=player_id"')
    ap.add_argument("--apply", action="store_true")
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

    print(f"{d['home']['name']} {d['ftScore']} {d['away']['name']} — 이벤트 {len(events)}건")
    print(f"PPDA  {a.team} {pv} ({nv}/{dv})  상대 {po} ({no}/{do})")
    print(f"def_x {a.team} {xv} (n={sv})  상대 {xo} (n={so})")

    con = sqlite3.connect(DB)
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
    else:
        print("(--apply 없음 — 쓰기 생략)")

    print(json.dumps({"ppda_v": pv, "ppda_num_v": nv, "ppda_den_v": dv,
                      "ppda_o": po, "ppda_num_o": no, "ppda_den_o": do,
                      "def_x_v": xv, "def_x_n_v": sv, "def_x_o": xo, "def_x_n_o": so,
                      "ppda_method": PPDA_METHOD + f" matchId={a.ws_match} ({today} 수집)",
                      "def_x_method": DEF_X_METHOD + f" matchId={a.ws_match} · 표본 "
                                      f"{a.team} {sv}·상대 {so} ({today} 수집)"}, ensure_ascii=False))
    con.close()


if __name__ == "__main__":
    main()
