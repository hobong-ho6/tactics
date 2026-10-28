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
from core.db import connect as connect_db  # noqa: E402  ⭐ DB 연결 정본(대기·작성 중 표시)
from scripts.gates import g8_prescription_checks, g12_role_group_orphans, g15_checks  # noqa: E402

FAIL = []


def check(name, cond, detail=""):
    print(f"  {'✅' if cond else '❌'} {name}{'' if cond else '  ← ' + detail}")
    if not cond:
        FAIL.append(name)


def inject(con, sql, params=()):
    """주입 1건 실행 — 바뀐 행이 0이면 「검출 실패」가 아니라 「픽스처 낡음」으로 따로 실패시킨다.
    ⭐ 2026-10-28: 주입 ⑤가 report_id=28을 박아 두었는데 그 행이 09-08 재판정으로 이미 RULE이라
       'RULE'→'RULE' 무변경 주입이 됐고, 한 달 넘게 「G15가 못 잡는다」로 잘못 보였다.
       ⇒ 대상은 id를 박지 않고 **조건으로 고르며**, 무변경 주입은 여기서 멈춘다."""
    n = con.execute(sql, params).rowcount
    check("주입 대상 존재", n > 0, f"바뀐 행 0 — 픽스처 조건에 맞는 행이 DB에 없다: {sql.split('WHERE')[-1].strip()[:120]}")
    return n


def fresh():
    src = connect_db(DB)
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
inject(con, "UPDATE prescriptions SET kind='measured season villa' WHERE id=(SELECT MIN(id) FROM prescriptions)")
check("kind_vocab 검출", g8_prescription_checks(con)["kind_vocab"])

print("주입 ② opt 선발 12명 (비선발 후보 1명을 선발로)")
con = fresh()
inject(con, """UPDATE prescriptions SET starter=1 WHERE id=(
    SELECT p.id FROM prescriptions p WHERE (p.kind LIKE 'opt:%' OR p.kind LIKE 'fc26:opt:%') AND p.kind NOT LIKE '%-deprecated'
      AND p.starter=0 AND EXISTS (SELECT 1 FROM prescriptions q WHERE q.regime_id=p.regime_id AND q.starter=1
        AND COALESCE(q.game_version,'FC26')=COALESCE(p.game_version,'FC26') AND (q.kind LIKE 'opt:%' OR q.kind LIKE 'fc26:opt:%'))
    ORDER BY p.id LIMIT 1)""")
check("opt_xi 검출", g8_prescription_checks(con)["opt_xi"])

print("주입 ③ opt 역할군 불일치 (CB 아닌 칸에 CB 역할)")
con = fresh()
inject(con, """UPDATE prescriptions SET role_id='cb_bpd' WHERE id=(
    SELECT p.id FROM prescriptions p JOIN slots s ON s.regime_id=p.regime_id AND s.pos=p.pos_label
    WHERE (p.kind LIKE 'opt:%' OR p.kind LIKE 'fc26:opt:%') AND p.kind NOT LIKE '%-deprecated' AND p.starter=1
      AND NOT EXISTS (SELECT 1 FROM slots t WHERE t.regime_id=p.regime_id AND t.pos=p.pos_label AND t.slot_type='CB')
    ORDER BY p.id LIMIT 1)""")
check("opt_role_group 검출", g8_prescription_checks(con)["opt_role_group"])

print("주입 ④ 경기 프리셋 역할군 밖 (CM 아닌 칸에 cm_b2b)")
con = fresh()
inject(con, """UPDATE match_player_prescriptions SET role_id='cm_b2b' WHERE rowid=(
    SELECT mpp.rowid FROM match_player_prescriptions mpp JOIN match_reports mr ON mr.id=mpp.report_id
    WHERE NOT EXISTS (SELECT 1 FROM slots t WHERE t.regime_id=mr.regime_id AND t.pos=mpp.pos_label AND t.slot_type='CM')
      AND EXISTS (SELECT 1 FROM slots t WHERE t.regime_id=mr.regime_id AND t.pos=mpp.pos_label)
    ORDER BY mpp.report_id, mpp.rowid LIMIT 1)""")
check("G12 역할군밖 검출", g12_role_group_orphans(con))

print("주입 ⑤ 규칙 편차인데 rule_note='RULE' (미신고 편차)")
con = fresh()
# DIVERGE로 신고된 행 전부의 신고를 지운다 — 그중 실제로 규칙과 다른 행이 하나라도 있으면 G15가 잡아야 한다
inject(con, "UPDATE match_game_setups SET rule_note='RULE' WHERE rule_note LIKE 'DIVERGE%'")
check("undeclared_diverge 검출", g15_checks(con)["undeclared_diverge"])

print("주입 ⑥ complete 리포트의 rule_note NULL")
con = fresh()
inject(con, """UPDATE match_game_setups SET rule_note=NULL WHERE report_id=(
    SELECT g.report_id FROM match_game_setups g JOIN match_reports r ON r.id=g.report_id
    WHERE r.status='complete' AND TRIM(COALESCE(g.rule_note,''))<>'' ORDER BY g.report_id LIMIT 1)""")
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
