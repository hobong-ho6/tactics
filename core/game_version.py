"""「어느 게임 버전인가」 단일 정본 (2026-10-22 신설 · 사용자 지적 「FC27용으로 패치도 분석했는데 안 바뀌어 있다니」).

왜:
  FC27이 2026-09-25에 나왔는데 역할표·시즌 정본·경기 세팅·적합 호출이 전부 `'FC26'`을 **코드에 박아 두고** 있었다.
  그래서 FC27 출시 뒤 경기 11건의 세팅이 FC26으로 적혔고, FC27 역할표는 한 달 가까이 0행이었다.
  ⇒ 버전을 문자열로 적지 말고 여기서 받는다. 기준은 `game_versions.released` 하나다.

⛔ 새 코드에서 `'FC26'`·`'FC27'`을 「현행」이라는 뜻으로 박지 않는다 — `current(con)`·`live_on(con, date)`를 쓴다.
   (특정 버전을 일부러 가리키는 곳 — 이관·버전 비교 — 은 예외다.)
⭐ 게이트 G40이 「경기 날짜에 살아 있던 버전 ≠ 기록 버전」과 「현행 버전 행이 없는 버전 축 표」를 막는다.
"""
from datetime import date as _date


def live_on(con, on):
    """그 날짜(YYYY-MM-DD)에 출시돼 있던 가장 새 버전. 출시 전 날짜면 None."""
    row = con.execute("SELECT code FROM game_versions WHERE released <= ? ORDER BY released DESC LIMIT 1",
                      (str(on)[:10],)).fetchone()
    return row[0] if row else None


def current(con):
    """오늘 기준 현행 버전."""
    return live_on(con, _date.today().isoformat())
