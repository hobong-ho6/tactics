"""WhoScored(Opta) matchCentreData 이벤트 → 팀·선수 파생 지표 (2026-09-08 신설).

지금까지 PPDA는 브라우저 콘솔 JS로 회차마다 다시 짜서 계산했다(불변규칙 4 위반 — core 밖 재구현).
이 모듈이 정본이다. 입력은 `matchCentreData.events` 리스트(dict) 그대로이며, 좌표 규약은
WhoScored 원본: **x = 그 팀의 공격 방향 0~100, y 낮음 = 오른쪽**(SofaScore와 동일 관례 —
2026-09-01 Cash/Maatsen 좌우로 검증, team_match_stats.ppda_method 주석).

이벤트 종류 (type.displayName):
  수비액션(PPDA 분모·수비 국면 그리드)  Tackle · Interception · Challenge · Foul(범한 것) ·
                                          Clearance · BlockedPass · Aerial · BallRecovery
  보유 국면 그리드                         Pass · TakeOn · BallTouch · Goal · MissedShots ·
                                          SavedShot · ShotOnPost · Dispossessed
  ⚠️ PPDA 분모는 위 8종 중 앞 4종만(기존 정의 유지 — 바꾸면 기존 14행과 비교 불가).
"""
from .encode import cells_from_points, encode

__all__ = ["ppda", "def_x", "phase_cells", "PPDA_METHOD", "DEF_X_METHOD"]

PPDA_DEN = {"Tackle", "Interception", "Challenge", "Foul"}
DEF_TYPES = PPDA_DEN | {"Clearance", "BlockedPass", "Aerial", "BallRecovery"}
POSS_TYPES = {"Pass", "TakeOn", "BallTouch", "Goal", "MissedShots", "SavedShot",
              "ShotOnPost", "Dispossessed"}

PPDA_METHOD = ("분자=상대가 자기 진영 3/5(x<60)에서 시도한 패스 · 분모=해당 팀 수비액션"
               "(Tackle·Interception·Challenge·Foul) 상대 진영 2/5(x>40). "
               "원천=WhoScored matchCentreData(Opta) — core.whoscored.ppda")
DEF_X_METHOD = ("팀 수비액션 8종(Tackle·Interception·Challenge·Foul·Clearance·BlockedPass·"
                "Aerial·BallRecovery)의 x 평균(자기 공격 방향 0~100). 라인 높이 프록시 — "
                "core.whoscored.def_x")


def _type(e):
    t = e.get("type")
    return t.get("displayName") if isinstance(t, dict) else t


def ppda(events, team_id, opp_id):
    """(ppda, 분자, 분모). 분모 0이면 (None, 분자, 0)."""
    num = sum(1 for e in events if e.get("teamId") == opp_id
              and _type(e) == "Pass" and e.get("x", 100) < 60)
    den = sum(1 for e in events if e.get("teamId") == team_id
              and _type(e) in PPDA_DEN and e.get("x", 0) > 40)
    return (round(num / den, 2) if den else None), num, den


def def_x(events, team_id):
    """(수비액션 x 평균, n). 표본 0이면 (None, 0)."""
    xs = [e["x"] for e in events if e.get("teamId") == team_id
          and _type(e) in DEF_TYPES and e.get("x") is not None]
    return (round(sum(xs) / len(xs), 1) if xs else None), len(xs)


def phase_cells(events, player_id):
    """선수 한 명의 국면별 5×5 카운트 → dict(cells_poss, cells_def, map25_poss, map25_def, n_poss, n_def).
    cells는 CSV 문자열(player_matches.cells와 같은 규약), map25는 core.encode.encode."""
    poss = [e for e in events if e.get("playerId") == player_id and _type(e) in POSS_TYPES]
    dfn = [e for e in events if e.get("playerId") == player_id and _type(e) in DEF_TYPES]
    cp, cd = cells_from_points(poss), cells_from_points(dfn)
    return dict(cells_poss=",".join(map(str, cp)), cells_def=",".join(map(str, cd)),
                map25_poss=encode(cp), map25_def=encode(cd), n_poss=len(poss), n_def=len(dfn))
