#!/usr/bin/env python3
"""migration 106 후속 — futgg_chem_signals의 「직전 회차와 같은 값의 반복」 행을 합친다 (2026-10-12, 1회).

같은 (ea_item_id, style_name)의 행을 회차 순으로 보고, **바로 앞 수집 회차**(표 전체의 관측일)에 같은 값이
있었으면 앞 행의 last_seen을 늘리고 뒤 행을 지운다. 그 카드가 빠진 회차가 끼면 합치지 않는다.
정본 규칙은 core/chem_signals.py(수집기와 같은 비교 함수)다.
"""
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from core import DB                              # noqa: E402
from core.chem_signals import content_key        # noqa: E402


def main():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    cols = [r[1] for r in con.execute("PRAGMA table_info(futgg_chem_signals)")]
    assert "last_seen" in cols, "migration 106 SQL을 먼저 적용할 것"
    rounds = [d for (d,) in con.execute("SELECT DISTINCT pulled FROM futgg_chem_signals ORDER BY pulled")]
    before = {d: i for i, d in enumerate(rounds)}
    drop, extend, cur = [], {}, {}
    for r in con.execute("SELECT * FROM futgg_chem_signals ORDER BY ea_item_id, style_name, pulled"):
        k = (r["ea_item_id"], r["style_name"])
        prev = cur.get(k)
        if prev is not None and content_key(prev["accelerate"], prev["vote_pct"]) == \
                content_key(r["accelerate"], r["vote_pct"]):
            last = extend.get(prev["id"], prev["last_seen"])
            i = before[r["pulled"]]
            if i > 0 and rounds[i - 1] == last:          # 바로 앞 회차에 이어진다
                extend[prev["id"]] = r["pulled"]
                drop.append(r["id"])
                continue
        cur[k] = r
    n0 = con.execute("SELECT COUNT(*) FROM futgg_chem_signals").fetchone()[0]
    con.executemany("UPDATE futgg_chem_signals SET last_seen=? WHERE id=?", [(v, k) for k, v in extend.items()])
    con.executemany("DELETE FROM futgg_chem_signals WHERE id=?", [(i,) for i in drop])
    con.execute("INSERT INTO _migration_log(run_at, v1_path, note) VALUES(date('now'), ?, ?)", (
        "106-chem-signals-last-seen",
        f"futgg_chem_signals 「바뀐 행만 저장」 전환(2026-10-12 사용자 결정). {n0}행 중 직전 회차와 같은 값의 반복 "
        f"{len(drop)}행을 앞 행 last_seen으로 합쳤다(연장 {len(extend)}행). 그 카드가 빠진 회차가 낀 경우는 합치지 않았다. "
        "불변규칙 2의 예외 — 정보 손실 없음(그날 유효 행 = pulled ≤ 날짜 ≤ last_seen). 원인: DB 101.2MB로 GitHub 100MB 상한 초과(099에 이어 두 번째)."))
    con.commit()
    con.execute("VACUUM")
    print(f"futgg_chem_signals {n0} → {n0 - len(drop)}행 (합침 {len(drop)} · 연장 {len(extend)})")


if __name__ == "__main__":
    main()
