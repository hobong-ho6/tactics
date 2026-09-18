#!/usr/bin/env python3
"""시즌 전술 「설정 층」 변경 로그 — tactic_change_log 적재 (2026-09-18, migration 039).

  python3 scripts/tactic_changes.py --backfill                 # git 이력(db/dump)에서 커밋 단위로 복원 — 최초 1회
  python3 scripts/tactic_changes.py --reason "obs#8xx …"       # DB 현재 ↔ 로그 마지막 상태 차이를 사유와 함께 추가
  python3 scripts/tactic_changes.py --check                    # 차이만 보고(G19가 쓰는 것과 같은 판정)

층·키·값은 core/tactic_state.state()가 정본이다(세션 내 재구현 금지 — 불변규칙 4).
backfill 사유는 **커밋 제목**이다 — 정밀한 사유(obs#)는 커밋 본문·obs에 있으니 화면은 커밋 해시를 함께 보인다.
"""
import argparse
import datetime as dt
import sqlite3
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from core import DB                                     # noqa: E402
from core.tactic_state import state                     # noqa: E402

DUMPS = ["db/dump/schema.sql", "db/dump/slot_canon_roles.sql", "db/dump/team_tactic_setups.sql", "db/dump/prescriptions.sql", "db/dump/players.sql"]


def git(*a):
    return subprocess.run(["git", *a], cwd=ROOT, capture_output=True, text=True).stdout


def state_at(commit):
    """그 커밋의 덤프를 임시 sqlite에 부어 state()를 편다. 덤프가 없던 시절은 빈 dict."""
    con = sqlite3.connect(":memory:")
    for f in DUMPS:
        sql = git("show", f"{commit}:{f}")
        if not sql:
            continue
        if f.endswith("schema.sql"):
            # 스키마 전체 대신 세 표만 — 다른 표의 뷰/트리거가 옛 버전에서 깨질 수 있다
            for stmt in sql.split(";\n"):
                if any(f"TABLE {t}" in stmt or f'TABLE "{t}"' in stmt for t in ("slot_canon_roles", "team_tactic_setups", "prescriptions", "regimes", "players")):
                    try:
                        con.execute(stmt)
                    except sqlite3.Error:
                        pass
        else:
            try:
                con.executescript(sql)
            except sqlite3.Error:
                pass
    try:
        return state(con)
    except sqlite3.Error:
        return {}


def logged_state(con):
    cur = {}
    for r in con.execute("SELECT layer, regime_id, key, after FROM tactic_change_log ORDER BY changed_at, id"):
        k = (r[0], r[1], r[2])
        if r[3] is None:
            cur.pop(k, None)
        else:
            cur[k] = r[3]
    return cur


def diff(prev, curr):
    out = []
    for k in sorted(set(prev) | set(curr), key=str):
        if prev.get(k) != curr.get(k):
            out.append((k, prev.get(k), curr.get(k)))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--backfill", action="store_true")
    ap.add_argument("--reason")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--date", default=dt.date.today().isoformat())
    a = ap.parse_args()
    con = sqlite3.connect(DB)

    if a.backfill:
        assert con.execute("SELECT COUNT(*) FROM tactic_change_log").fetchone()[0] == 0, "로그가 비어 있을 때만 backfill"
        commits = git("log", "--reverse", "--format=%h|%ad|%s", "--date=short", "--", *DUMPS[1:4]).strip().splitlines()
        prev, n = {}, 0
        for line in commits:
            h, d, subj = line.split("|", 2)
            curr = state_at(h)
            if not curr:
                continue
            rows = [(k[1], k[0], k[2], b, af, d, subj, f"git:{h}") for k, b, af in diff(prev, curr)]
            con.executemany("INSERT INTO tactic_change_log(regime_id, layer, key, before, after, changed_at, reason, source) "
                            "VALUES(?,?,?,?,?,?,?,?)", rows)
            n += len(rows); prev = curr
        con.commit()
        print(f"backfill: 커밋 {len(commits)}개 · 변경 {n}행")
        # 마지막 커밋 ↔ 현재 DB(미커밋 변경) 차이는 사유가 없으니 보고만
        pend = diff(prev, state(con))
        if pend:
            print(f"⚠️ 미커밋 변경 {len(pend)}건 — --reason으로 적재할 것:", [(k, b, af) for k, b, af in pend][:5])
        return

    pend = diff(logged_state(con), state(con))
    if a.check or not a.reason:
        print(f"로그 대비 미기록 변경 {len(pend)}건" + ("" if not pend else ":"))
        for k, b, af in pend:
            print(f"  [{k[0]}] regime {k[1]} {k[2]}: {b} → {af}")
        if pend and not a.reason:
            print("→ python3 scripts/tactic_changes.py --reason \"obs#… 사유\"")
        return
    rows = [(k[1], k[0], k[2], b, af, a.date, a.reason, f"tactic_changes.py {a.date}") for k, b, af in pend]
    con.executemany("INSERT INTO tactic_change_log(regime_id, layer, key, before, after, changed_at, reason, source) "
                    "VALUES(?,?,?,?,?,?,?,?)", rows)
    con.commit()
    print(f"적재 {len(rows)}행 (사유: {a.reason})")


if __name__ == "__main__":
    main()
