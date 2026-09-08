"""팀 설정 3축 매핑 규칙 — 실측(점유·롱볼 비율·PPDA) → FC26 팀 설정 제안 (2026-09-08 사전 등록).

왜 이 모듈이 있나: `match_game_setups`의 빌드업·수비접근·라인은 지금까지 회차마다 산문 판단으로
정해졌다(2026-09-08 점검 — 19행 중 동일 실측에 다른 값이 여럿). 규칙을 먼저 고정해 두면
「규칙과 다르게 고른 이유」가 반드시 남는다(G15 · `match_game_setups.rule_note`).

⚠️ 임계값은 **FC26 옵션 정의(game_tactic_params)와 docs/12 PPDA 정본표**에서 정했고, 기존 19행에
맞춰 조정하지 않았다 — 기존 행과의 불일치는 규칙의 결함이 아니라 「설명해야 할 편차」다.
⚠️ PPDA는 **이 저장소 WhoScored 정의**(상대 자기진영 3/5 패스 / 우리 상대진영 2/5 수비액션)만 넣는다.
   다른 산출사 PPDA를 넣으면 대역이 어긋난다(docs/12). PPDA는 자기 점유율이 높을수록 기계적으로
   올라간다(ppda_method 주석) — 점유 60%+에서 나온 큰 PPDA는 편차 사유로 쓸 수 있다.

규칙 (docs/20 「팀 설정 매핑 규칙」과 동일해야 한다 — 둘 중 하나만 고치지 말 것):
  빌드업   Counter        롱볼 비율 ≥ 13% 또는 점유 ≤ 40%
           Short Passing  롱볼 비율 ≤ 8% 그리고 점유 ≥ 55%
           Balanced       그 밖
  수비접근 High           PPDA ≤ 8          라인 62~72
           Balanced       8 < PPDA ≤ 18     라인 48~62 (PPDA ≤ 12면 상단, 그 위면 하단)
           Deep           PPDA > 18         라인 ≤ 45
  Aggressive는 제안하지 않는다 — EA 정의가 「즉시 카운터프레스 + 오프사이드 트랩」이라 PPDA만으로
  근거가 안 된다. 쓰려면 편차 사유에 카운터프레스 실측을 적는다.
"""

__all__ = ["suggest", "compare"]


def suggest(possession=None, passes=None, long_att=None, ppda=None):
    """실측 → dict(build_up_style, defensive_approach, line_lo, line_hi, long_pct).
    입력이 모자라면 해당 항목은 None(결손이지 0이 아니다)."""
    out = {"build_up_style": None, "defensive_approach": None,
           "line_lo": None, "line_hi": None, "long_pct": None}
    if passes and long_att is not None:
        out["long_pct"] = round(100.0 * long_att / passes, 1)
    lp, poss = out["long_pct"], possession
    if lp is not None or poss is not None:
        if (lp is not None and lp >= 13) or (poss is not None and poss <= 40):
            out["build_up_style"] = "Counter"
        elif lp is not None and poss is not None and lp <= 8 and poss >= 55:
            out["build_up_style"] = "Short Passing"
        elif lp is not None and poss is not None:
            out["build_up_style"] = "Balanced"
    if ppda is not None:
        if ppda <= 8:
            out.update(defensive_approach="High", line_lo=62, line_hi=72)
        elif ppda <= 12:
            out.update(defensive_approach="Balanced", line_lo=55, line_hi=62)
        elif ppda <= 18:
            out.update(defensive_approach="Balanced", line_lo=48, line_hi=58)
        else:
            out.update(defensive_approach="Deep", line_lo=0, line_hi=45)
    return out


def compare(sug, build_up_style, defensive_approach, line_height):
    """기록값과 규칙 제안의 편차 목록. 비어 있으면 일치. 제안이 None인 축은 비교하지 않는다."""
    diff = []
    if sug["build_up_style"] and sug["build_up_style"] != build_up_style:
        diff.append(f"빌드업 규칙 {sug['build_up_style']} vs 기록 {build_up_style}")
    if sug["defensive_approach"] and sug["defensive_approach"] != defensive_approach:
        diff.append(f"수비접근 규칙 {sug['defensive_approach']} vs 기록 {defensive_approach}")
    if sug["line_lo"] is not None and line_height is not None \
            and not (sug["line_lo"] <= line_height <= sug["line_hi"]):
        diff.append(f"라인 규칙 {sug['line_lo']}~{sug['line_hi']} vs 기록 {line_height}")
    return diff
