"""포지션별 OVR 산정식 **단일 정본** (2026-10-02 신설 · migration 091).

왜 (사용자 지시 「진화에서 세부 스탯뿐 아니라 전체 오버롤을 올려주는 진화가 있는데 … 실제 세부 스탯은
    그만큼 안 오르는데 오버롤만 뻥튀기되는 경우를 막고 싶어」):
  진화의 `overall +N` 보상은 세부 스탯과 따로 OVR을 올린다. 세부 스탯으로 계산한 OVR과 견줘야
  「표기만 높은 카드」를 가려낼 수 있다.

⚠️ 가중치는 **EA 공개값이 아니다** — FC27 비진화·비특별 카드로 적합한 값이다(등급 C · `fc_position_ovr_weights`).
   시험셋(적합에 안 쓴 30%) 정확 일치 55~88%, 거의 전부 ±1 이내다. ⛔ 풀백(FB)은 32%로 약하다.
   ⇒ **절대값보다 진화 전후의 차이(Δ)로 쓴다** — 선수마다 붙는 오차(국제 명성 보너스 등)가 차이에서 상쇄된다.
⛔ 화면(`site/assets/posovr.js`)은 이 파일을 옮긴 것이다. 두 구현은 게이트 G31이 같은 입력으로 대조한다.
⛔ 포지션→그룹 표는 **여기 한 곳**에 둔다. export가 화면으로 내보낸다(화면이 다시 적지 않는다).
"""
import math

# 카드 주 포지션 → 산정식 그룹. ⚠️ LWB·RWB·CF는 FC27 일반 카드가 거의 없어 따로 적합하지 못했다 —
#   가장 가까운 그룹으로 **근사**한다(LWB·RWB→FB · CF→ST). 그 사실을 화면이 함께 띄운다(APPROX).
GROUP = {"GK": "GK", "CB": "CB", "LB": "FB", "RB": "FB", "LWB": "FB", "RWB": "FB",
         "CDM": "CDM", "CM": "CM", "CAM": "CAM", "LM": "WM", "RM": "WM",
         "LW": "WF", "RW": "WF", "ST": "ST", "CF": "ST"}
APPROX = {"LWB", "RWB", "CF"}


def load(con, game="FC27"):
    """최신 적합 회차의 가중치 {그룹: {속성: %}}. 없으면 빈 dict(⛔ 지어내지 않는다)."""
    rows = con.execute("""SELECT pos_group, attr, weight_pct FROM fc_position_ovr_weights
                          WHERE game_version=? AND fitted=(SELECT MAX(fitted) FROM fc_position_ovr_weights
                                                           WHERE game_version=?)""", (game, game)).fetchall()
    out = {}
    for g, a, w in rows:
        out.setdefault(g, {})[a] = w
    return out


def raw(attrs, pos, weights):
    """세부 스탯 → 그 포지션의 OVR(실수). 그룹·가중이 없거나 속성이 빠지면 None(⛔ 0으로 세지 않는다)."""
    w = weights.get(GROUP.get(pos))
    if not w or not attrs:
        return None
    if any(attrs.get(k) is None for k in w):
        return None
    return sum(attrs[k] * v for k, v in w.items()) / sum(w.values())


def ovr(attrs, pos, weights):
    """정수 OVR(반올림 = floor(v + 0.5) · JS와 같은 규칙)."""
    v = raw(attrs, pos, weights)
    return None if v is None else math.floor(v + 0.5)
