-- 052 진화 후 29속성 (2026-09-19) — 진화가 끝나면 카드의 **개별 속성**이 바뀌는데
-- player_card_items.attrs는 기본 카드 값이라 케미 추천이 옛 수치로 계산된다.
-- 보유 선수의 현재 속성을 따로 들고, 화면은 이 값이 있으면 우선 쓴다.
ALTER TABLE fut_club_players ADD COLUMN current_attrs TEXT;   -- {한글 속성: 값} JSON
