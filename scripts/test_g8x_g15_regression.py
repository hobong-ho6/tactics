#!/usr/bin/env python3
"""G8+(게임 처방 정합)·G12 역할군·G15(팀 설정 규칙) 회귀 테스트 — 결함을 **합성 주입**해 검사가 잡는지 본다.
scripts/test_g13_regression.py와 같은 원칙: 검사식을 복사하지 않고 scripts/gates.py의 함수를 import한다.
⚠️ 원본 DB는 건드리지 않는다 — 메모리 복제에만 주입한다(읽기 전용).
사용: python3 scripts/test_g8x_g15_regression.py   종료 코드 0=통과.
"""
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core import DB                                                           # noqa: E402
from scripts.gates import g8_prescription_checks, g12_role_group_orphans, g15_checks  # noqa: E402

FAIL = []


def check(name, cond, detail=""):
    print(f"  {'✅' if cond else '❌'} {name}{'' if cond else '  ← ' + detail}")
    if not cond:
        FAIL.append(name)


def fresh():
    src = sqlite3.connect(DB)
    mem = sqlite3.connect(":memory:")
    src.backup(mem)
    src.close()
    return mem


print("기준선(현 DB) — 전항 0이어야 한다")
con = fresh()
base8 = g8_prescription_checks(con)
check("G8+ 기준선 0", not any(base8.values()), str({k: len(v) for k, v in base8.items()}))
check("G12 역할군 기준선 0", not g12_role_group_orphans(con))
base15 = g15_checks(con)
check("G15 기준선 0", not any(base15.values()), str({k: len(v) for k, v in base15.items()}))

print("주입 ① kind 자유 어휘")
con = fresh()
con.execute("UPDATE prescriptions SET kind='measured season villa' WHERE id=(SELECT MIN(id) FROM prescriptions)")
check("kind_vocab 검출", g8_prescription_checks(con)["kind_vocab"])

print("주입 ② fc26:opt 선발 12명 (RB 추가)")
con = fresh()
con.execute("UPDATE prescriptions SET starter=1 WHERE id=259")   # CHE 5-4-1 RB 귀스토 — 027이 0으로 내린 행
check("opt_xi 검출", g8_prescription_checks(con)["opt_xi"])

print("주입 ③ fc26:opt 역할군 불일치 (LM에 CB 역할)")
con = fresh()
con.execute("UPDATE prescriptions SET role_id='cb_bpd' WHERE regime_id=1 AND kind='fc26:opt:LM' AND starter=1")
check("opt_role_group 검출", g8_prescription_checks(con)["opt_role_group"])

print("주입 ④ 경기 프리셋 교체 선수 역할군 밖 (ST에 cm_b2b)")
con = fresh()
con.execute("UPDATE match_player_prescriptions SET role_id='cm_b2b' WHERE report_id=27 AND pos_label='ST' AND starter=0")
check("G12 역할군밖 검출", g12_role_group_orphans(con))

print("주입 ⑤ 규칙 편차인데 rule_note='RULE' (미신고 편차)")
con = fresh()
con.execute("UPDATE match_game_setups SET rule_note='RULE' WHERE report_id=28")   # 백필이 DIVERGE로 판정한 행
check("undeclared_diverge 검출", g15_checks(con)["undeclared_diverge"])

print("주입 ⑥ complete 리포트의 rule_note NULL")
con = fresh()
con.execute("UPDATE match_game_setups SET rule_note=NULL WHERE report_id=26")
check("note_missing 검출", g15_checks(con)["note_missing"])

print("오탐 ⑦ DIVERGE 신고된 편차는 통과")
con = fresh()
check("DIVERGE 신고 통과", not g15_checks(con)["undeclared_diverge"])

print("오탐 ⑧ -deprecated kind는 opt 검사에서 제외")
con = fresh()
r = g8_prescription_checks(con)
check("deprecated 제외", not r["opt_pos_orphan"] and not r["opt_role_group"])

print("✅ 전항 통과" if not FAIL else f"❌ 실패 {FAIL}")
sys.exit(1 if FAIL else 0)
