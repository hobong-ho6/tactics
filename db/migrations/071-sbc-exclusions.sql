-- 071 SBC 챌린지별 선수 제외 (2026-09-25 사용자 지시
--    「선수를 스쿼드에서 제외하고 재계산하는 기능을 넣어줘 제외한 선수는 해당 sbc에 포함 안 시키는 용이야」)
--
-- 왜 별도 테이블인가:
--   전역 제외(활성 스쿼드 · 아스톤 빌라)는 `sbc_solve.py`의 인자로 이미 있다. 하지만 「이 카드는
--   저 SBC에 쓸 거라 이번 건에는 빼 둔다」는 **챌린지마다 다른 판단**이라 전역 축으로는 못 적는다.
--
-- ⛔ 카드를 지우거나 status를 바꾸지 않는다 — 제외는 **판정 입력**이지 보유 사실의 변경이 아니다(불변규칙 2).
-- ⛔ EA·fut.gg가 주지 않는 축이다(사용자 판단) — source에 그렇게 적는다.
CREATE TABLE IF NOT EXISTS fc_sbc_exclusions(
  game_version    TEXT NOT NULL REFERENCES game_versions(code),
  challenge_ea_id INTEGER NOT NULL,
  club_player_id  INTEGER NOT NULL REFERENCES fut_club_players(id),
  reason          TEXT,
  added           TEXT,
  PRIMARY KEY(game_version, challenge_ea_id, club_player_id)
);
