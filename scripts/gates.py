#!/usr/bin/env python3
"""회귀 게이트 — v2의 정본성 보증. DB 쓰기 스크립트는 시작 시 이걸 통과해야 한다.

게이트 (docs/20 게이트 표의 v2 이관):
  G1. 커널 정합 — 역할 37 / 조합 85 / 변형 217 (Kernel 로드 시 assert)
  G2. 인코딩 회귀 — player_matches 전 그리드 cells→map25 재인코딩 대조
  G3. 커널 앵커 — 저장 그리드로 기준 적합값 재현:
        캐시 measured:season RM(x=85, WM)  .835 wm_widemid/Support   (독립 앵커)
        Jackson ST(x=50, ST)               .752 st_advanced/Support
        만잠비 CAM(x=50, CAM)              .861 cam_halfwinger/Balanced
        가르나초 LM(x=14, WM)              .771 wm_winger/Attack
        알리송 RM(x=85, WM)                .833 wm_widemid/Build-Up
        하지무사 RM(x=85, WM)              .821 wm_winger/Attack — 그리드 상수
          (DB에서 삭제된 행 — docs/20에 박힌 사본이 유일본, 커널 자체의 앵커)
  G4. 집계 공식 — 만잠비 대표팀 12경기 재집계가 저장 map25와 일치

사용: python3 scripts/gates.py          (전체)
      from scripts.gates import run    (프로그램 내 호출)
"""
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core import DB
from core.aggregate import player_aggregate
from core.encode import regression_check
from core.kernel import Kernel

HADJ_MOUSSA = "312691114X000140002400001"   # docs/20 게이트 표의 사본 (DB에 원본 없음)

ANCHORS = [
    # (라벨, 그리드 조회 SQL, params, x, slot_type, 기대 role, focus, sim)
    ("캐시 RM(measured:season)",
     "SELECT map25 FROM prescriptions p JOIN players pl ON pl.id=p.player_id "
     "WHERE pl.name='Matty Cash' AND p.kind='measured:season'", (), 85, "WM",
     "wm_widemid", "Support", 0.835),
    ("Jackson ST",
     "SELECT map25 FROM transfer_targets WHERE name='Nicolas Jackson' AND slot='ST'", (),
     50, "ST", "st_advanced", "Support", 0.752),
    ("만잠비 CAM",
     "SELECT map25 FROM transfer_targets WHERE name='Johan Manzambi' AND slot='CAM'", (),
     50, "CAM", "cam_halfwinger", "Balanced", 0.861),
    ("가르나초 LM",
     "SELECT map25 FROM transfer_targets WHERE name='Alejandro Garnacho' AND slot='LM'", (),
     14, "WM", "wm_winger", "Attack", 0.771),
    ("알리송 RM",
     "SELECT map25 FROM transfer_targets WHERE name='Alysson' AND slot='RM'", (),
     85, "WM", "wm_widemid", "Build-Up", 0.833),
    ("하지무사 RM(상수)", None, HADJ_MOUSSA, 85, "WM", "wm_winger", "Attack", 0.821),
]


def run(db_path=None, verbose=True):
    db_path = db_path or DB
    con = sqlite3.connect(db_path)
    fails = []

    # G1 — Kernel 로드가 정합 assert를 겸한다
    k = Kernel("FC26", db_path)
    if verbose:
        print("G1 커널 정합: 37/85/217 ✅")

    # G2
    bad, total = regression_check(con)
    if verbose:
        print(f"G2 인코딩 회귀: {total}행 중 불일치 {len(bad)} {'✅' if not bad else '⛔ ' + str(bad[:5])}")
    if bad:
        fails.append("G2")

    # G3
    for label, sql, params, x, st, wr, wf, ws in ANCHORS:
        if sql is None:
            m25 = params
        else:
            row = con.execute(sql, params).fetchone()
            if not row or not row[0]:
                if verbose:
                    print(f"G3 {label}: ⚠️ 행 없음 — 건너뜀 (보존정책 삭제 가능)")
                continue
            m25 = row[0]
        r, f, s = k.best_fit(m25, x, st)
        ok = r == wr and f == wf and abs(s - ws) < 0.001
        if verbose:
            print(f"G3 {label}: {r}/{f} {s:.3f} {'✅' if ok else f'⛔ 기대 {wr}/{wf} {ws}'}")
        if not ok:
            fails.append(f"G3:{label}")

    # G4 — 집계 공식 재현 (만잠비 대표팀 12경기 → prescriptions measured:national)
    manz = con.execute("SELECT id FROM players WHERE name='Johan Manzambi'").fetchone()
    if manz:
        stored = con.execute(
            "SELECT map25 FROM prescriptions WHERE player_id=? AND kind='measured:national'",
            (manz[0],)).fetchone()
        agg = player_aggregate(manz[0],
                               "competition IN ('FIFA World Cup','World Cup Qual. UEFA',"
                               "'International Friendly')", db_path=db_path)
        ok = stored and agg and agg["map25"] == stored[0] and agg["n"] == 12
        if verbose:
            print(f"G4 집계 재현(만잠비 national n={agg['n'] if agg else '?'}): "
                  f"{'✅' if ok else '⛔ 저장 ' + str(stored[0] if stored else None) + ' vs 재집계 ' + str(agg['map25'] if agg else None)}")
        if not ok:
            fails.append("G4")

    con.close()
    if verbose:
        print("✅ 게이트 전항 통과" if not fails else f"⛔ 실패: {fails}")
    return not fails


if __name__ == "__main__":
    sys.exit(0 if run() else 1)
