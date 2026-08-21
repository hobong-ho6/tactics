#!/usr/bin/env python3
"""저장된 적합값 vs 커널 재산출값의 드리프트 점검 — **읽기 전용**.

왜 있는가 (2026-08-21 신설):
  HANDOFF가 R2(08-23) 이후 「슬롯 기하 재산출 → 전 행 `fit_sim` 재산출 → `sort_order` 재도출」
  연쇄를 예고했다. 슬롯 x가 바뀌면 **어느 행이 얼마나 움직이는지**를 먼저 알아야 하는데,
  지금은 그것을 손으로 세고 있다. 이 스크립트가 그 대조표를 만든다.

⛔ **쓰지 않는다.** 저장값을 자동으로 갱신하지 않는 이유가 있다 — 실측 대조 결과
   93행 중 **85행만 「슬롯군 내 최대 적합」 규칙으로 재현**된다. 나머지 8행은 `player_duties`의
   require/prefer 제약이나 특정 사이드 고정 때문에 순수 argmax가 아니다(C5·C6, obs#121·#130).
   ⇒ 불일치는 **오류가 아니라 판정일 수 있다.** 사람이 행별로 봐야 한다.

재산출 규칙: `slots`에서 (regime_id, slot_type)에 속한 모든 pos의 x로 `Kernel.best_fit`을 돌려
             최대 적합을 취한다. 자리표시 그리드(전부 0)는 건너뛴다.

사용:
    .venv/bin/python scripts/check_fit_drift.py                 # 전 팀
    .venv/bin/python scripts/check_fit_drift.py --team ATM --min-delta 0.02
"""
import argparse
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from core.kernel import Kernel  # noqa: E402

DB = ROOT / "db" / "tactics.db"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--team", help="팀 코드 (없으면 전 팀)")
    ap.add_argument("--min-delta", type=float, default=0.001,
                    help="이 이상 벌어진 행만 출력 (기본 0.001)")
    a = ap.parse_args()

    con = sqlite3.connect(DB)
    k = Kernel()
    slots = {}
    for rid, pos, x, st in con.execute("SELECT regime_id, pos, x, slot_type FROM slots"):
        slots.setdefault((rid, st), []).append((pos, x))

    sql = """SELECT r.team_code, se.player_id, COALESCE(se.label, p.name_kr), se.slot_type,
                    se.map25, se.fit_role, se.fit_focus, se.fit_sim, se.regime_id
             FROM squad_entries se
             JOIN players p ON p.id = se.player_id
             JOIN regimes r ON r.id = se.regime_id
             WHERE se.map25 NOT LIKE '0000000000000000000000000'"""
    args = []
    if a.team:
        sql += " AND r.team_code = ?"
        args.append(a.team)
    rows = con.execute(sql + " ORDER BY r.team_code, se.slot_type", args).fetchall()

    same, drift, missing, noval = 0, [], [], 0
    for team, pid, kr, st, m, role, focus, sim, rid in rows:
        cands = slots.get((rid, st))
        if not cands:
            missing.append((team, kr, st))
            continue
        best = max((k.best_fit(m, x, st) + (pos,) for pos, x in cands), key=lambda t: t[2])
        if sim is None:
            noval += 1
            drift.append((team, kr, st, None, None, None, best))
            continue
        if abs(best[2] - sim) < a.min_delta and best[0] == role and best[1] == focus:
            same += 1
        else:
            drift.append((team, kr, st, role, focus, sim, best))

    print(f"대조 {len(rows)}행 · 일치 {same} · 차이 {len(drift)}"
          f"(그중 저장값 NULL {noval}) · 슬롯 기하 없음 {len(missing)}")
    if drift:
        print("\n차이 — ⚠️ 오류가 아니라 duty 제약·사이드 고정에 따른 판정일 수 있다:")
        for team, kr, st, role, focus, sim, best in drift:
            cur = "저장 없음" if sim is None else f"저장 {role}/{focus} {sim:.3f}"
            d = "" if sim is None else f" (Δ{best[2] - sim:+.3f})"
            print(f"  [{team}] {kr} {st}: {cur} vs 커널 {best[0]}/{best[1]} {best[2]:.3f}"
                  f" @{best[3]}{d}")
    if missing:
        print("\n⚠️ slots에 해당 (regime, slot_type) 기하가 없어 대조 불가:")
        for team, kr, st in missing:
            print(f"  [{team}] {kr} {st}")


if __name__ == "__main__":
    main()
