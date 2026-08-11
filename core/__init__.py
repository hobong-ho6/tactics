"""tactics core — 실측→FC 구현 파이프라인의 공용 엔진 (v2, 2026-08-11 재설계).

v1에서는 이 로직들이 세션마다 /tmp 스크립트로 재작성됐다(커널 적합·인코딩·집계).
여기 있는 것이 정본이고, 게이트(scripts/gates.py)가 정본성을 보증한다.

모듈:
  kernel    — decodeMap/placedMap/cmpCos/best_fit (DB의 game_role_variants가 커널 정본)
  encode    — 5×5 그리드 인코딩 (docs/30 ③ 정본 규약)
  aggregate — 통합 그리드 (포지션-순수·맥락분리·대회별)
  sofascore — 수집 헬퍼 (브라우저 JS 스니펫 + 행 파서)
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "db" / "tactics.db"
