"""포지션 사후 분류 — lineup_pos(G/D/M/F)는 포지션-순수 집계에 너무 거칠다 (2026-08-11).

⭐ 2026-09-08 재작성(obs 참조: 「pos_class 어휘 3종 혼재·백3 오분류」).
   ⑴ **포메이션을 받는다.** 선수 한 명의 좌표만으로는 백3와 백4를 구분할 수 없다.
   ⑵ **어휘 정본은 `slots` 테이블**이다. 좌우 위치(x)도 그 표에서 가져온다 —
      임의 임계값을 새로 만들지 않는다. 옛 구현은 독스트링에 「슬롯 x 정본표로 세분류한다」고
      써 놓고 실제로는 쓰지 않았고, 그래서 백3 CB 셋이 전부 풀백으로 찍혔다.
   ⑶ 포메이션·슬롯을 모를 때만 좌표 밴딩으로 물러선다(정확도 낮음을 호출자가 알 수 있게 분리).

좌표 규약(docs/30): SofaScore avg_x = 공격 방향, avg_y 낮음 = 오른쪽.
슬롯 표의 x는 **툴 좌표**이므로 `툴x = 100 − 소파y`로 변환해 비교한다.
"""

# 포메이션 → 11개 슬롯 라벨. 각 라인을 우→좌로 나열한다(SofaScore 라인업 배열 규약).
# scripts/load_lineup_order.py의 FORM 표를 core로 옮긴 것이다(불변규칙 4 — 로직은 core에만).
FORM = {
    '4-2-3-1': ['GK', 'RB', 'RCB', 'LCB', 'LB', 'RDM', 'LDM', 'RAM', 'CAM', 'LAM', 'ST'],
    '4-4-2':   ['GK', 'RB', 'RCB', 'LCB', 'LB', 'RM', 'RCM', 'LCM', 'LM', 'RST', 'LST'],
    '4-2-2-2': ['GK', 'RB', 'RCB', 'LCB', 'LB', 'RDM', 'LDM', 'RAM', 'LAM', 'RST', 'LST'],
    '4-3-3':   ['GK', 'RB', 'RCB', 'LCB', 'LB', 'RCM', 'CM', 'LCM', 'RW', 'ST', 'LW'],
    '4-1-4-1': ['GK', 'RB', 'RCB', 'LCB', 'LB', 'CDM', 'RM', 'RCM', 'LCM', 'LM', 'ST'],
    '3-4-2-1': ['GK', 'RCB', 'CCB', 'LCB', 'RM', 'RCM', 'LCM', 'LM', 'RAM', 'LAM', 'ST'],
    '3-4-3':   ['GK', 'RCB', 'CCB', 'LCB', 'RM', 'RCM', 'LCM', 'LM', 'RW', 'ST', 'LW'],
    '3-5-2':   ['GK', 'RCB', 'CCB', 'LCB', 'RM', 'RCM', 'CM', 'LCM', 'LM', 'RST', 'LST'],
    '5-4-1':   ['GK', 'RB', 'RCB', 'CCB', 'LCB', 'LB', 'RM', 'RCM', 'LCM', 'LM', 'ST'],
}

# 슬롯 라벨 → 라인 그룹
GROUP = {
    'GK': 'GK',
    'LB': 'FB', 'RB': 'FB',
    'LCB': 'CB', 'CCB': 'CB', 'RCB': 'CB',
    'LDM': 'DM', 'CDM': 'DM', 'RDM': 'DM',
    'LCM': 'CM', 'CM': 'CM', 'RCM': 'CM',
    'LM': 'WM', 'RM': 'WM',
    'LAM': 'CAM', 'CAM': 'CAM', 'RAM': 'CAM',
    'LW': 'W', 'RW': 'W',
    'LST': 'ST', 'ST': 'ST', 'RST': 'ST',
}

# lineup_pos(+깊이) → 허용 라인 그룹.
#   깊이 분기 52는 새 값이 아니라 scripts/load_lineup_order.py가 이미 쓰던 규약이다.
#   WM(LM/RM)은 양쪽 밴드에 모두 넣는다 — 백3의 윙백은 깊고, 백4의 와이드 미드는 높다.
DEPTH_SPLIT = 52.0
ALLOWED_DEEP     = {'DM', 'CM', 'WM'}
ALLOWED_ADVANCED = {'CAM', 'W', 'WM', 'CM'}
ALLOWED_D        = {'CB', 'FB'}
ALLOWED_F        = {'ST', 'W', 'CAM', 'WM'}

# slots 표에 없는 라벨의 보조 좌우값(툴 좌표). 표에 있으면 언제나 표가 이긴다.
FALLBACK_X = {'CM': 50.0, 'CDM': 50.0, 'CCB': 50.0, 'CAM': 50.0, 'ST': 50.0, 'GK': 50.0}

# 라인 그룹별 기대 깊이(avg_x) — **이 저장소 실측의 중앙값**이다(2026-09-08 산출, 값 발명 아님).
# 좌우가 같은 후보(예: 중앙의 CAM ↔ ST)가 붙었을 때 결정론적으로 가르는 데만 쓴다.
DEPTH_PRIOR = {'GK': 12.2, 'CB': 36.4, 'FB': 47.5, 'DM': 49.6, 'CM': 51.6,
               'WM': 53.9, 'CAM': 60.9, 'ST': 64.1, 'W': 67.4}
DEPTH_WEIGHT = 0.15     # ⚠️ 좌우가 주(主)다. 깊이는 국면(리드/추격)에 크게 흔들리므로 보조로만 쓴다 —
                        #    0.5로 두면 전진한 CB(아체암퐁)가 윙백으로 넘어간다(2026-09-08 실측).

# 표본 신뢰 하한 — docs/30 ③(히트맵 hit_points 15 미만은 그리드 무효)과
# scripts/load_lineup_order.py의 「minutes<45면 NULL」 규약을 그대로 따른다.
MIN_MINUTES = 45
MIN_HIT_POINTS = 15


def normalize_formation(formation):
    """'4-2-3-1 Wide' → '4-2-3-1'. slots와 player_matches의 표기가 다르다."""
    if not formation:
        return None
    f = formation.strip()
    for suffix in (' Wide', ' Narrow', ' Diamond', ' Flat', ' Holding'):
        if f.endswith(suffix):
            f = f[: -len(suffix)]
    return f.strip()


def lateral_canon(con):
    """`slots` 테이블에서 라벨 → 좌우값(툴 x) 정본을 만든다.

    같은 라벨이 팀·포메이션마다 조금씩 다르므로 **중앙값**을 쓴다. 값을 발명하지 않는다.
    """
    xs = {}
    for pos, x in con.execute("SELECT pos, x FROM slots WHERE x IS NOT NULL"):
        xs.setdefault(pos, []).append(float(x))
    out = {}
    for pos, vals in xs.items():
        vals.sort()
        n = len(vals)
        out[pos] = vals[n // 2] if n % 2 else (vals[n // 2 - 1] + vals[n // 2]) / 2
    return out


def lateral_for_formation(con, formation, regime_id=None):
    """그 포메이션의 라벨 → 좌우값. 팀 슬롯이 있으면 팀 값을, 없으면 전체 중앙값을 쓴다."""
    labels = FORM.get(normalize_formation(formation))
    if not labels:
        return None
    canon = lateral_canon(con)
    team = {}
    if regime_id is not None:
        for pos, x in con.execute(
                "SELECT pos, x FROM slots WHERE regime_id=? AND x IS NOT NULL", (regime_id,)):
            team.setdefault(pos, float(x))
    out = {}
    for lab in labels:
        if lab == 'GK':
            continue
        v = team.get(lab, canon.get(lab, FALLBACK_X.get(lab)))
        if v is not None:
            out[lab] = v
    return out


def line_groups(avg_x, lineup_pos):
    """그 선수가 어느 라인에서 뛰었는지 → 허용 슬롯 그룹 집합. None이면 GK.

    ⚠️ `lineup_pos`에도 어휘가 두 종류 섞여 있다(2026-09-08 실측): 거친 G/D/M/F와
    슬롯 라벨(RB·LAM·RCB…)이 같은 컬럼에 들어 있고, 일부는 NULL이다. 셋 다 받는다.
    """
    if lineup_pos in ('G', 'GK'):
        return None
    if lineup_pos in ('D', 'M', 'F'):
        if lineup_pos == 'D':
            return ALLOWED_D
        if lineup_pos == 'F':
            return ALLOWED_F
        return ALLOWED_DEEP if float(avg_x) < DEPTH_SPLIT else ALLOWED_ADVANCED
    g = GROUP.get(lineup_pos)
    if g:                       # lineup_pos가 이미 슬롯 라벨이면 라인이 확정된다
        return {g}
    # lineup_pos 결손 → 깊이로 라인을 추정한다. 경계는 이 저장소 실측 평균의 중점이다
    # (G 10.8 · D 41.9 · M 55.0 · F 64.7 → 26 / 48 / 60).
    ax = float(avg_x)
    if ax < 26.0:
        return None
    if ax < 48.0:
        return ALLOWED_D
    if ax < 60.0:
        return ALLOWED_DEEP
    return ALLOWED_ADVANCED | ALLOWED_F


def pos_class(avg_x, avg_y, lineup_pos, lateral=None, minutes=None, hit_points=None):
    """슬롯 분류. `lateral`(라벨→툴x)을 주면 포메이션 인식 분류, 없으면 좌표 밴딩 폴백.

    반환은 `slots.pos` 어휘를 따른다(GK/LB/LCB/CCB/RCB/RB/LDM/CDM/RDM/LCM/CM/RCM/
    LM/RM/LAM/CAM/RAM/LW/RW/LST/ST/RST) 또는 None(판정 불가).

    ⭐ `minutes`/`hit_points`를 주면 표본이 얇을 때 **추측하지 않고 None을 낸다**.
       결손과 오분류는 다르다 — 9분 출전의 평균 좌표로 역할을 정하면 안 된다(obs#132 계열).
    """
    if lineup_pos in ('G', 'GK'):
        return 'GK'
    if avg_x is None or avg_y is None:
        return None
    if minutes is not None and minutes < MIN_MINUTES:
        return None
    if hit_points is not None and hit_points < MIN_HIT_POINTS:
        return None

    groups = line_groups(avg_x, lineup_pos)
    if groups is None:
        return 'GK'

    toolx = 100.0 - float(avg_y)

    if lateral:
        # ⭐ 백3 계열에는 풀백 슬롯이 없다 — 그 포메이션에서 「수비수로 등재된 와이드」는
        #    윙백이고 정본 슬롯은 WM(LM/RM)이다. FB가 없는 포메이션에서만 WM을 열어 준다.
        if 'CB' in groups and not any(GROUP.get(l) == 'FB' for l in lateral):
            groups = set(groups) | {'WM'}
        cands = [(lab, x) for lab, x in lateral.items() if GROUP.get(lab) in groups]
        if not cands:  # 그 포메이션에 해당 그룹이 없으면 라인 제약을 풀고 좌우로만 고른다
            cands = list(lateral.items())
        if cands:
            ax = float(avg_x)
            def score(kv):
                lab, x = kv
                d = DEPTH_PRIOR.get(GROUP.get(lab), ax)
                return (abs(x - toolx) + DEPTH_WEIGHT * abs(d - ax), lab)
            return min(cands, key=score)[0]

    return _band_fallback(avg_x, toolx, lineup_pos)


def _band_fallback(avg_x, toolx, lineup_pos):
    """포메이션을 모를 때의 좌우 밴딩. ⚠️ 백3/백4를 구분하지 못한다 — 정확도가 낮다."""
    left, right = toolx < 30.0, toolx > 70.0          # 툴x 낮음 = 좌측
    half_left, half_right = toolx < 45.0, toolx > 55.0
    if lineup_pos == 'D':
        if left:  return 'LB'
        if right: return 'RB'
        return 'LCB' if half_left else ('RCB' if half_right else 'CCB')
    if lineup_pos == 'M':
        if float(avg_x) < DEPTH_SPLIT:
            if left:  return 'LM'
            if right: return 'RM'
            return 'LDM' if half_left else ('RDM' if half_right else 'CDM')
        if left:  return 'LM'
        if right: return 'RM'
        return 'LAM' if half_left else ('RAM' if half_right else 'CAM')
    if left:  return 'LW'
    if right: return 'RW'
    return 'LST' if half_left else ('RST' if half_right else 'ST')
