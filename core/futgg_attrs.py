"""fut.gg 속성 필드 → 한글 라벨 **정본** (2026-09-23 신설).

왜 (사용자 질문 「프리킥 스탯은 fut.gg에서 안 준다는 거지?」에서 드러남):
  같은 표가 **네 파일에 복제**돼 있었고 그중 하나만 키가 틀렸다 —
  `collect_ggclub.py`만 `attributeFreeKickAccuracy`를 찾았는데 fut.gg의 실제 필드는 **`attributeFkAccuracy`**다
  (나머지 셋은 맞았다). 그래서 **GG Club 수집만 「프리킥 정확도」를 100% 흘렸고**, 6대 스탯 PAS가
  보유 89명 전원에서 2~4 낮게 계산됐다(구성식이 없는 값을 0으로 셌다).
  ⛔ fut.gg가 안 주는 게 아니라 **우리가 잘못된 이름으로 찾고 있었다.**

⇒ 표는 여기 하나만 둔다(불변규칙 13 ② 단일 정본). 복제하면 또 한 곳만 틀린다.
⚠️ 한글 라벨은 `player_game_stats.attrs`·`player_card_items.attrs`와 **같은 키**여야 한다 —
   여기를 바꾸면 버전 간 비교·6대 스탯 구성식(`fc_face_stats.attr`)이 통째로 어긋난다.
"""

# 필드 30종(필드플레이어 29 + 체형 관련 없음) + GK 5종.
ATTR_KR = {
    "attributeAcceleration": "가속", "attributeSprintSpeed": "질주 속도",
    "attributePositioning": "공격 위치 선정", "attributeFinishing": "결정력", "attributeShotPower": "슈팅력",
    "attributeLongShots": "중거리슛", "attributeVolleys": "발리 슛", "attributePenalties": "페널티킥",
    "attributeVision": "시야", "attributeCrossing": "크로스",
    # ⛔ `attributeFreeKickAccuracy`가 아니다 — 2026-09-23에 그 오타로 89명의 PAS가 틀어졌다.
    "attributeFkAccuracy": "프리킥 정확도",
    "attributeShortPassing": "짧은 패스", "attributeLongPassing": "긴 패스", "attributeCurve": "커브",
    "attributeAgility": "민첩성", "attributeBalance": "균형 감각", "attributeReactions": "반응력",
    "attributeBallControl": "볼컨트롤", "attributeDribbling": "드리블", "attributeComposure": "침착",
    "attributeInterceptions": "차단력", "attributeHeadingAccuracy": "헤딩 정확도",
    "attributeDefensiveAwareness": "수비 위치 선정", "attributeStandingTackle": "스탠딩 태클",
    "attributeSlidingTackle": "슬라이딩 태클", "attributeJumping": "점프", "attributeStamina": "체력",
    "attributeStrength": "힘", "attributeAggression": "공격성",
    "attributeGkDiving": "다이빙", "attributeGkHandling": "핸들링", "attributeGkKicking": "킥",
    "attributeGkPositioning": "포지셔닝", "attributeGkReflexes": "반사신경",
}

# 필드플레이어가 반드시 다 채워져야 하는 29속성 — 수집기가 **누락을 조용히 넘기지 않게** 대조한다.
FIELD_ATTRS = frozenset(v for k, v in ATTR_KR.items() if not k.startswith("attributeGk"))


def parse_attrs(obj, *, want=None):
    """fut.gg 응답 한 건에서 한글 라벨 dict를 만들고, **빠진 속성을 함께 돌려준다.**

    ⛔ 결손을 조용히 버리지 않는다(obs#132) — 호출측이 건수를 보고할 수 있어야 한다.
    반환: (attrs, missing) · `want`가 None이면 필드플레이어 29속성을 기준으로 본다.
    """
    attrs = {kr: obj[k] for k, kr in ATTR_KR.items() if obj.get(k) is not None}
    need = set(want if want is not None else FIELD_ATTRS)
    return attrs, sorted(need - set(attrs))
