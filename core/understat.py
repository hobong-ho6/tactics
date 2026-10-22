"""Understat 선수·경기 창조 지표(xGChain·xGBuildup) ↔ 우리 matches 연결 (2026-10-22 신설 · 경기 데이터 결손 검토 §3-5 「활용 결손」).

왜: `understat_player_matches` 6천여 행이 있는데 리포트·화면이 안 썼다. Understat에는 우리 match_id가 없고 팀 이름 표기도 다르다
    (「Brighton」·「Hull」 ↔ 우리 「Brighton & Hove Albion」). 상대 이름을 맞추지 않고 **경기 날짜 + 우리 팀 이름(teams.name)** 으로 잇는다 —
    같은 날 같은 팀의 경기는 하나다. PL(빅5)만 있으므로 UCL·컵 경기는 빈 목록이 정상이다.
"""
from .db import connect as connect_db
from . import DB

COLS = "player_id, us_match_id, match_date, h_team, a_team, position, minutes, xg, xa, npxg, xg_chain, xg_buildup"


def match_rows(con, team_code, date):
    """한 경기(팀·날짜)의 Understat 선수 행 — [(player_id, us_match_id, match_date, h_team, a_team, position, minutes, xg, xa, npxg, xg_chain, xg_buildup)]."""
    return con.execute(f"""
        SELECT {COLS} FROM understat_player_matches
        WHERE match_date=? AND (h_team=(SELECT name FROM teams WHERE code=?) OR a_team=(SELECT name FROM teams WHERE code=?))
        ORDER BY xg_chain DESC""", (date, team_code, team_code)).fetchall()


def season_rows(con, team_code, season):
    """팀의 한 시즌(Understat season = 시작 연도) 전 경기 선수 행 — 선수 화면용."""
    return con.execute(f"""
        SELECT {COLS} FROM understat_player_matches
        WHERE season=? AND (h_team=(SELECT name FROM teams WHERE code=?) OR a_team=(SELECT name FROM teams WHERE code=?))
        ORDER BY match_date, xg_chain DESC""", (season, team_code, team_code)).fetchall()


if __name__ == "__main__":                            # 손 점검: python3 -m core.understat AVL 2026-10-17
    import sys
    con = connect_db(DB)
    for r in match_rows(con, sys.argv[1], sys.argv[2]):
        print(r)
