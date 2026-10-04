#!/usr/bin/env python3
"""migration 099 후속 — player_evolutions의 「직전 관측과 같은 값의 반복」 행을 합친다 (2026-10-04, 1회).

같은 (game_version, base_ea_id, path_key)의 행을 관측일 순으로 보고, **그 base 카드의 바로 앞 관측일**에
같은 내용이 있었으면 앞 행의 last_seen을 늘리고 뒤 행을 지운다. 관측이 끊겼으면(그 base 카드를 조회한 날
이 경로가 없었으면) 합치지 않는다. 내용 비교에서 id·pulled·last_seen·source·confidence는 뺀다.
정본 규칙은 core/evo_paths.py(수집기와 같은 비교 함수)다.
"""
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from core import DB                          # noqa: E402
from core.evo_paths import content_key       # noqa: E402


def main():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    cols = [r[1] for r in con.execute("PRAGMA table_info(player_evolutions)")]
    assert "last_seen" in cols, "migration 099 SQL을 먼저 적용할 것"
    obs = {}   # (gv, base) -> 정렬된 관측일
    for gv, base, p in con.execute("SELECT DISTINCT game_version, base_ea_id, pulled FROM player_evolutions"):
        obs.setdefault((gv, base), set()).add(p)
    obs = {k: sorted(v) for k, v in obs.items()}
    drop, extend = [], {}
    cur = {}   # (gv, base, path) -> 살아남은 행 dict
    for r in con.execute("SELECT * FROM player_evolutions ORDER BY game_version, base_ea_id, path_key, pulled"):
        r = dict(r)
        k = (r["game_version"], r["base_ea_id"], r["path_key"])
        prev = cur.get(k)
        dates = obs[(r["game_version"], r["base_ea_id"])]
        if prev is not None and content_key(prev) == content_key(r):
            last = extend.get(prev["id"], prev["last_seen"])
            i = dates.index(r["pulled"])
            if i > 0 and dates[i - 1] == last:           # 바로 앞 관측에 이어진다
                extend[prev["id"]] = r["pulled"]
                drop.append(r["id"])
                continue
        cur[k] = r
    n0 = con.execute("SELECT COUNT(*) FROM player_evolutions").fetchone()[0]
    con.executemany("UPDATE player_evolutions SET last_seen=? WHERE id=?", [(v, k) for k, v in extend.items()])
    con.executemany("DELETE FROM player_evolutions WHERE id=?", [(i,) for i in drop])
    con.execute("INSERT INTO _migration_log(run_at, v1_path, note) VALUES(date('now'), ?, ?)", (
        "099-player-evolutions-last-seen",
        f"player_evolutions 「바뀐 행만 저장」 전환(2026-10-04 사용자 결정). {n0}행 중 직전 관측과 같은 값의 반복 "
        f"{len(drop)}행을 앞 행 last_seen으로 합쳤다(연장 {len(extend)}행). 관측이 끊긴 경우는 합치지 않았다. "
        "불변규칙 2의 예외 — 정보 손실 없음(그날 유효 경로 = pulled ≤ 날짜 ≤ last_seen). 원인: DB 103.8MB로 GitHub 100MB 상한 초과."))
    con.commit()
    con.execute("VACUUM")
    print(f"player_evolutions {n0} → {n0 - len(drop)}행 (합침 {len(drop)} · 연장 {len(extend)})")


if __name__ == "__main__":
    main()
