#!/usr/bin/env python3
"""WhoScored 이벤트 → 선수별 **운반(추정)·수신 귀속** 지표를 player_matches.stats_json에 덧붙인다 (2026-10-22 신설 · 같은 날 수신 추가 후 이름 변경 load_carry_est → load_ws_player_extras).

왜: 운반(progressive carries)은 공개 제공사에 경기 단위가 없다(FC27 구현 검토 §2.2). 바이킹전 대조표 10행(고메스 볼 캐리)을
    손으로 센 뒤 같은 정의가 core.whoscored.carry_est에 올라갔다 — 회차마다 콘솔에서 다시 세지 않는다(불변규칙 4).
무엇을: stats_json에 carry_est_n · carry_est_prog10_n · carry_est_prog_m_sum · carry_est_method(운반 추정) +
        recv_n · recv_x_mean · recv_deep_n · recv_deep80_n · recv_prog_n · recv_through_n · recv_method(수신 귀속 · core.whoscored.receptions)를
        **덧붙인다**(다른 키 불변). 운반은 추정이라 est — 리포트·화면에서 「운반(추정)」으로만 쓴다. 수신은 Opta 패스 끝 좌표의 귀속이라 추정 아님(방법은 recv_method).

사용:
    .venv/bin/python scripts/load_ws_player_extras.py reports/match-watch/data/2026-10-21-avl-ws-2029164.json \\
        --event 16938853 --team AVL --side home [--map "WhoScored 이름=player_id"] [--apply]
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
from core import DB                                   # noqa: E402
from core.db import connect as connect_db             # noqa: E402
from core.whoscored import carry_est, receptions      # noqa: E402
from load_whoscored import match_players              # noqa: E402  ⭐ 이름 매칭 정본은 load_whoscored 하나


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("json_path")
    ap.add_argument("--event", type=int, required=True, help="SofaScore event_id(player_matches.event_id)")
    ap.add_argument("--team", required=True)
    ap.add_argument("--side", choices=["home", "away"], required=True)
    ap.add_argument("--map", action="append", default=[])
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    d = json.loads(Path(a.json_path).read_text())
    events = d["events"]
    us = d["home"] if a.side == "home" else d["away"]
    manual = {k: int(v) for k, v in (m.split("=", 1) for m in a.map)}
    con = connect_db(DB)
    our_ids = {e["playerId"] for e in events if e.get("teamId") == us["teamId"] and e.get("playerId") is not None}
    names = {k: v for k, v in d["playerIdNameDictionary"].items() if int(k) in our_ids}
    pairs, unmatched = match_players(con, a.event, names, manual)
    print(f"매칭 {len(pairs)}명 · 미매칭 {len(unmatched)}: {unmatched}")
    rows = []
    for ws_id, pid, ws_name in pairs:
        c = carry_est(events, ws_id)
        c.update(receptions(events, ws_id))
        rows.append((pid, ws_name, c))
        print(f"  {ws_name:28} 운반(추정) {c['carry_est_n']:>3} · 전진10+ {c['carry_est_prog10_n']:>2} · 전진 {c['carry_est_prog_m_sum']:>6.1f}m"
              f" | 수신 {c['recv_n']:>3} · x̄ {str(c['recv_x_mean']):>5} · 깊은(≥66.7) {c['recv_deep_n']:>2} · ≥80 {c['recv_deep80_n']:>2}"
              f" · 전진 {c['recv_prog_n']:>2} · 스루 {c['recv_through_n']}")
    if not a.apply:
        print("(--apply 없음 — 쓰기 생략)")
        return
    n = 0
    for pid, _, c in rows:
        row = con.execute("SELECT stats_json FROM player_matches WHERE player_id=? AND event_id=?", (pid, a.event)).fetchone()
        if not row:
            continue
        sj = json.loads(row[0] or "{}")
        sj.update(c)                                                   # carry_est_*·recv_* 키만 덧붙인다(같은 키는 같은 정의의 재계산)
        con.execute("UPDATE player_matches SET stats_json=? WHERE player_id=? AND event_id=?",
                    (json.dumps(sj, ensure_ascii=False), pid, a.event))
        n += 1
    con.commit()
    print(f"적용 {n}행 → player_matches.stats_json(carry_est_* · recv_*)")


if __name__ == "__main__":
    main()
