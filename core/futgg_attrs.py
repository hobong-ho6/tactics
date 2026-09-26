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


# ── 진화 보상 적용 · 6대 스탯 환산 (2026-09-26 신설) ────────────────────────────
#
# ⛔⛔ **왜 서버로 옮겼나** — 「현재 카드」가 원장에 **두 벌**로 있었고 한 벌만 갱신됐다.
#    `fut_club_players`의 `current_ovr`/`current_six`는 `evolve`가 올리는데 `current_attrs`는
#    **아무도 안 올렸다**. 화면은 before를 `current_six`에서, after를 `current_attrs`에서 가져와
#    계산하므로 두 벌이 갈리는 순간 **after가 before보다 낮게** 나온다.
#    실증(2026-09-26 마조 빛나는 스트라이커): `current_ovr`=73인데 `current_attrs`는 인쇄값
#    (가속 65·질주 74)이라 1단계 기록이 PAC 75→**70**, SHO 73→**69**로 적혔다.
#    진화가 스탯을 내리는 일은 없다 — 조용히 틀린 값이라 화면만 봐선 알 수 없었다.
# ⇒ 불변규칙 13 ①: 「화면이 계산해 보내고 서버가 받아 적는」 구조를 없앤다.
#    서버가 `current_attrs`에서 직접 계산해 **세 값을 한꺼번에** 갱신하면 갈릴 수가 없다.
# ⚠️ 라벨 표는 위 ATTR_KR과 **다른 키 체계**다(fut.gg 수집 필드 ≠ 진화 카탈로그 필드) — 그래서 따로 둔다.

EVO_ATTR_KR = {
    "acceleration": "가속", "sprint_speed": "질주 속도", "positioning": "공격 위치 선정",
    "finishing": "결정력", "shot_power": "슈팅력", "long_shots": "중거리슛", "volleys": "발리 슛",
    "penalties": "페널티킥", "vision": "시야", "crossing": "크로스", "fk_accuracy": "프리킥 정확도",
    "short_passing": "짧은 패스", "long_passing": "긴 패스", "curve": "커브", "agility": "민첩성",
    "balance": "균형 감각", "reactions": "반응력", "ball_control": "볼컨트롤", "dribbling": "드리블",
    "composure": "침착", "interceptions": "차단력", "heading_accuracy": "헤딩 정확도",
    "def_awareness": "수비 위치 선정", "standing_tackle": "스탠딩 태클", "sliding_tackle": "슬라이딩 태클",
    "jumping": "점프", "stamina": "체력", "strength": "힘", "aggression": "공격성",
}


def apply_upgrades(attrs, upgrades):
    """진화 보상 한 묶음을 29속성 dict에 **제자리 적용**하고 OVR 상승분을 돌려준다.

    ⭐ 상한(`maxValue`) 규칙: 이미 상한 이상이면 **그대로 둔다**. 내리지 않는다.
       (표기 +10이 캡에 걸려 실제 +0이 되는 일이 흔하다 — 런북 「추천할 때」 ②)
    반환: (ovr_delta_fn, unknown) · ovr은 호출측이 현재 OVR을 알아야 캡을 적용할 수 있어 콜백으로 준다.
    """
    unknown, ovr_ups = [], []
    for u in upgrades or []:
        key = str(u.get("upgrade") or "")
        if key == "overall":
            ovr_ups.append((u.get("value") or 0, u.get("maxValue")))
            continue
        if not key.startswith("attribute_"):
            continue
        kr = EVO_ATTR_KR.get(key[len("attribute_"):])
        if kr is None:
            unknown.append(key)
            continue
        if attrs.get(kr) is None:
            continue
        cap, cur = u.get("maxValue"), attrs[kr]
        if cap is not None and cur >= cap:
            continue
        attrs[kr] = min(cur + (u.get("value") or 0), cap) if cap is not None else cur + (u.get("value") or 0)

    def bump(ovr):
        for val, cap in ovr_ups:
            if cap is not None and ovr >= cap:
                continue
            ovr = min(ovr + val, cap) if cap is not None else ovr + val
        return ovr

    return bump, unknown


def face_of(attrs, face_rows, *, is_gk=False):
    """29속성 → 6대 스탯. 구성식 정본은 `fc_face_stats`다(화면의 faceOf와 같은 축).

    ⛔ 결손 속성을 0으로 세지 않는다(obs#132) — 가중을 남은 속성에 정규화한다.
    """
    w = {}
    for r in face_rows:
        if bool(r["is_gk"]) is bool(is_gk):
            w.setdefault(r["abbr"], {})[r["attr"]] = r["weight"]
    out = {}
    for abbr, ws in w.items():
        have = {k: v for k, v in ws.items() if attrs.get(k) is not None}
        tot = sum(have.values())
        if not tot:
            continue
        out[abbr] = round(sum(attrs[k] * v for k, v in have.items()) / tot)
    return out
