"""스코어 국면 분(phase_lead/level/trail) — 단일 정본 (2026-10-22 신설).

왜: `player_matches.stats_json.phase_*`는 2026-08-23부터 회차마다 **세션 JS로 따로 계산**해 넣었고,
09-12·10-15 수집 회차는 그 단계를 빠뜨려 공식전 5경기(08-31·09-08·09-19·10-10·10-14)가 0행이었다
(@lead/@trail 분리 집계 표본이 반토막 · 2026-10-22 FC27 구현 검토 §2.1). 불변규칙 13 ②: 계산을 한 모듈에 두고
`load_sofascore_json.py`(수집 시)와 `scripts/backfill_phase_minutes.py`(결손 보충)가 import만 한다.

정의(기존 행 실측으로 확인 · 바이킹전 #126 · 뉴캐슬전 #120):
  - 경기 시계는 0~90분(정규 시간만 · 추가시간 골은 분 그대로 — 90 이후면 무시).
  - 득점 사건은 그 분부터 스코어에 반영된다(23′ 골 → 0~22분 level 23분 · 23~89분 lead 67분).
  - 선발: [0, minutes) · 교체 투입: [90−minutes, 90) — 투입 분이 따로 있으면 그것을 쓴다.
  - 우리 쪽 득점(자책골 포함)은 side='v', 상대 득점은 'o'.
"""

LEAD, LEVEL, TRAIL = "phase_lead", "phase_level", "phase_trail"
FULL = 90


def score_timeline(goals):
    """goals: (minute, side) 목록(side 'v'|'o'). 분 m(0~89)의 상태 → 'lead'|'level'|'trail' 배열(길이 90)."""
    gs = sorted((int(m), s) for m, s in goals if m is not None)
    out, v, o, i = [], 0, 0, 0
    for m in range(FULL):
        while i < len(gs) and gs[i][0] <= m:
            if gs[i][1] == "v":
                v += 1
            elif gs[i][1] == "o":
                o += 1
            i += 1
        out.append("lead" if v > o else "trail" if v < o else "level")
    return out


def phase_minutes(timeline, minutes, started, minute_on=None):
    """한 선수의 국면 분 dict {phase_lead, phase_level, phase_trail}. minutes가 없으면 None."""
    if minutes is None:
        return None
    minutes = int(minutes)
    if started:
        a, b = 0, min(minutes, FULL)
    else:
        a = int(minute_on) if minute_on is not None else max(0, FULL - minutes)
        b = min(a + minutes, FULL)
    c = {"lead": 0, "level": 0, "trail": 0}
    for m in range(a, b):
        c[timeline[m]] += 1
    return {LEAD: c["lead"], LEVEL: c["level"], TRAIL: c["trail"]}


def goals_from_incidents(incidents):
    """js_event_collect의 incidents(type goal · side home/away) + 우리 side → (minute, 'v'|'o')."""
    out = []
    for i in incidents or []:
        if i.get("type") != "goal":
            continue
        out.append((i.get("t"), i.get("side")))
    return out
