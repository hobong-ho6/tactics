#!/usr/bin/env python3
"""DB → site/data 익스포트 CLI. 게이트 통과가 선행 조건이다."""
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core import ROOT
from core.export import export_all
from scripts.gates import run as run_gates

if __name__ == "__main__":
    # 선발 처방 층은 손으로 고르지 않는다 — 게이트 전에 산출해 반영한다(core/opt_starters · obs#1148)
    from core.db import connect as connect_db
    from core.opt_starters import apply as apply_opt_starters
    _con = connect_db()
    for pos, before, after, why in apply_opt_starters(_con):
        print(f"  선발 자동 산출 {pos}: {before} → {after} ({why})")
    _con.close()
    if not run_gates(verbose=False):
        sys.exit("⛔ 게이트 실패 — 익스포트 중단. scripts/gates.py로 확인할 것")
    written = export_all()
    for p in written:
        print(f"  {p.relative_to(ROOT)}")
    # 프리뷰 미러 (TCC — docs/40): site/ 전체를 /private/tmp에 복사
    mirror = Path("/private/tmp/tactics-preview")
    if mirror.is_dir():
        shutil.copytree(ROOT / "site", mirror / "site", dirs_exist_ok=True)
        print(f"mirrored → {mirror / 'site'}")
    print(f"✅ {len(written)}개 파일 익스포트 (게이트 통과 후)")
