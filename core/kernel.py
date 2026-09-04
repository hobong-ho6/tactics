"""커널 적합 엔진 — 툴의 decodeMap/placedMap/cmpCos의 파이썬 정본 (v2).

v1과의 결정적 차이: **커널의 정본이 DB다** (game_role_variants / game_roles).
v1은 fc26-heatmap.html의 JS 상수를 정규식으로 파싱했고, 마지막 항목에 개행이
없어 조용히 누락되는 함정이 있었다(docs/20 파싱 함정). v2는 그 함정이 없다.

placedMap 의미론 (obs#93·#94 — EA 정본 변형 선택):
  슬롯 x에 질량중심(pitch_x)이 가장 가까운 변형을 골라 **그대로** 쓴다.
  미러·시프트 합성은 폐기됐다.

역할군 필터 (obs#141 — 문서에 없던 필수 필터):
  슬롯은 자기 slot_type(GK/CB/FB/DM/CM/CAM/WM/W/ST)의 역할만 후보로 쓴다.
  이걸 빼면 LM이 w_winger(.936)를 집는 식으로 게이트가 조용히 깨진다.
"""
import math
import sqlite3

from . import DB

__all__ = ["Kernel"]


def decode(code):
    return [1.0 if ch == "X" else int(ch) / 10 for ch in code]


def cos(a, b):
    dot = sum(p * q for p, q in zip(a, b))
    na = math.sqrt(sum(p * p for p in a))
    nb = math.sqrt(sum(q * q for q in b))
    return dot / (na * nb) if na and nb else 0.0


class Kernel:
    """게임 버전 하나의 커널 라이브러리. 로드 시 정합성 assert."""

    # FC26 정합 기대값 — 버전 추가 시 여기 확장 (docs/20 게이트 표와 동기)
    EXPECTED = {"FC26": (37, 85, 217)}

    def __init__(self, game_version="FC26", db_path=None):
        self.gv = game_version
        con = sqlite3.connect(db_path or DB)
        self.role_group = dict(con.execute(
            "SELECT role_id, position_type FROM game_roles WHERE game_version=?", (self.gv,)))
        self.variants = {}          # (role_id, focus) -> [(pitch_x, decoded25), …]
        n_var = 0
        for role, focus, px, k25 in con.execute(
                "SELECT role_id, focus, pitch_x, kernel25 FROM game_role_variants "
                "WHERE game_version=?", (self.gv,)):
            self.variants.setdefault((role, focus), []).append((px, decode(k25)))
            n_var += 1
        n_combo = len(self.variants)
        con.close()
        # 버전이 EXPECTED에 없으면(FC27 사전 적재 단계) assert 대신 경고만 — FC26 게이트(G1)는 불변.
        # 카운트가 fut.gg FC27 응답으로 확정되면 EXPECTED에 행을 추가한다(docs/21 · obs#445).
        exp = self.EXPECTED.get(self.gv)
        if exp is None:
            import sys
            print(f"⚠️ Kernel({self.gv}): EXPECTED 미등재 — 정합 assert 생략(사전 적재 단계)", file=sys.stderr)
        if exp:
            got = (len(self.role_group), n_combo, n_var)
            assert got == exp, (
                f"⛔ {self.gv} 커널 정합 실패 — 기대 {exp}, 실제 {got}. "
                f"DB game_roles/game_role_variants 확인.")

    def placed(self, role, focus, x):
        lst = self.variants.get((role, focus))
        if not lst:
            return None
        return min(lst, key=lambda t: abs(t[0] - x))[1]

    def fit(self, map25, role, focus, x):
        pm = self.placed(role, focus, x)
        return cos(decode(map25), pm) if pm else 0.0

    def best_fit(self, map25, x, slot_type):
        """(role, focus, sim) — 슬롯 x·역할군에서 최고 적합 조합."""
        v = decode(map25)
        best = (None, None, -1.0)
        for (role, focus), lst in self.variants.items():
            if self.role_group.get(role) != slot_type:
                continue
            pm = min(lst, key=lambda t: abs(t[0] - x))[1]
            s = cos(v, pm)
            if s > best[2]:
                best = (role, focus, s)
        return best

    def best_fit_slot(self, map25, regime_id, pos, db_path=None):
        """slots 테이블의 regime 기하로 best_fit. (팀 고유 x — 빌라 x 재사용 금지)"""
        con = sqlite3.connect(db_path or DB)
        row = con.execute(
            "SELECT x, slot_type FROM slots WHERE regime_id=? AND pos=?",
            (regime_id, pos)).fetchone()
        con.close()
        if not row:
            raise KeyError(f"slots에 없음: regime={regime_id} pos={pos}")
        return self.best_fit(map25, row[0], row[1])
