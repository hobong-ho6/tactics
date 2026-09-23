#!/usr/bin/env python3
"""G21·G22 회귀 시험 — **결함을 합성 주입해 게이트가 실제로 잡는지** 확인한다 (2026-09-23 신설).

왜 (사용자 지시 「코드레벨이나 스크립트로 수행할 수 있는 것들은 전환해줘」):
  게이트는 **통과할 때 아무 말도 안 하므로** 조용히 고장 나도 알 수 없다. G13·G14가 같은 이유로
  회귀 시험을 갖고 있다(`test_g13_regression.py`·`test_g14_regression.py`) — 같은 규약을 따른다.

⛔ 원본 DB·저장소 파일을 건드리지 않는다. DB는 복제본에, 파일 검사는 원복을 보장한다.

사용: python3 scripts/test_g21_g22_regression.py
"""
import shutil
import sqlite3
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import gates  # noqa: E402

fails = []


def check(name, got, want):
    ok = got == want
    print(f"  {'✅' if ok else '⛔'} {name}: {'잡음' if got else '못 잡음'} (기대 {'잡음' if want else '통과'})")
    if not ok:
        fails.append(name)


def g21_case(mutate, label, want_fail):
    """복제 DB를 손본 뒤 gates.run()이 실패하는지 본다."""
    with tempfile.TemporaryDirectory() as td:
        db = Path(td) / "t.db"
        shutil.copy(ROOT / "db" / "tactics.db", db)
        con = sqlite3.connect(db)
        mutate(con)
        con.commit()
        con.close()
        # ⚠️ verbose=False — 회귀 시험의 출력은 판정 줄만 남긴다(대화 비용).
        check(label, not gates.run(db_path=str(db), verbose=False), want_fail)


print("G21 수집 회차 완결성")
# ⑴ 2026-09-23 아침 실제 사고 재현: 경로 수집이 11명에서 끊겨 295 → 27이 됐다.
g21_case(lambda c: c.execute(
    "DELETE FROM player_evolutions WHERE pulled=(SELECT MAX(pulled) FROM player_evolutions) "
    "AND rowid NOT IN (SELECT rowid FROM player_evolutions "
    "                   WHERE pulled=(SELECT MAX(pulled) FROM player_evolutions) LIMIT 20)"),
         "중단된 경로 수집(최신 회차가 직전의 절반 미만)", True)
# ⑵ 오탐 검사 — 조금 줄어든 것(정상: 진화 마감·카드 처분)은 잡으면 안 된다.
g21_case(lambda c: c.execute(
    "DELETE FROM fc_evolution_eligibility WHERE pulled=(SELECT MAX(pulled) FROM fc_evolution_eligibility) "
    "AND rowid IN (SELECT rowid FROM fc_evolution_eligibility "
    "               WHERE pulled=(SELECT MAX(pulled) FROM fc_evolution_eligibility) LIMIT 5)"),
         "소폭 감소는 통과(오탐 검사)", False)

print("G22 화면 코드 정적 검사")
# ⑶ CSS 템플릿 리터럴 안 백틱 — 네 번 재발한 실수.
target = ROOT / "site" / "assets" / "clubviz.js"
orig = target.read_text(encoding="utf-8")
try:
    hurt = orig.replace("export const FC_CSS = `", "export const FC_CSS = `\n/* `백틱` */", 1)
    if hurt == orig:
        print("  ⚠️ FC_CSS 블록을 못 찾아 건너뜀 — 주입 지점이 바뀌었는지 확인할 것")
    else:
        target.write_text(hurt, encoding="utf-8")
        check("CSS 리터럴 백틱", not gates.run(verbose=False), True)
finally:
    target.write_text(orig, encoding="utf-8")       # ⛔ 무슨 일이 있어도 원복한다

# ⑷ 공용 규칙을 화면이 다시 짜는 것 — 2026-09-22에 74건을 낳은 부류.
target2 = ROOT / "site" / "player.html"
orig2 = target2.read_text(encoding="utf-8")
try:
    target2.write_text(orig2 + "\n<!-- /Premium Season Pass/ -->\n", encoding="utf-8")
    check("공용 규칙 재구현(evorules.js 밖)", not gates.run(verbose=False), True)
finally:
    target2.write_text(orig2, encoding="utf-8")

print(f"\n{'⛔ 실패: ' + ', '.join(fails) if fails else '✅ G21·G22 전항 검출 확인'}")
sys.exit(1 if fails else 0)
