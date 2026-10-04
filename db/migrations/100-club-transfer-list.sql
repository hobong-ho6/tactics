-- 100 보유 카드의 이적 명단 상태 (2026-10-04 사용자 지시 「클럽 싱크할 때 내 이적명단에 있는 선수도 확인해서
--   보유했던 선수로 기록해줘 — 나중에 갤러리에서 사용하게」).
--
-- 확인(2026-10-04 실측): fut.gg GG Club `/api/gg-club/players/` 응답의 보유행에 이미
--   isOnTransferList · transferListState · transferListBuyNowPrice · transferListExpiresAt 이 온다
--   (fut.gg 「Transfer List」 페이지도 같은 API에 is_on_transfer_list 필터를 건다 — 별도 경로가 아니다).
--   ⇒ 이적 명단 카드도 보유 목록에 들어오므로 원장에 「보유」로 남고, 팔린 뒤에도 행이 지워지지 않아 갤러리 후보로 남는다.
--   종전 수집기는 이 칸들을 버렸다 — 무엇이 명단에 올라 있었는지가 기록되지 않았다.
ALTER TABLE fut_club_players ADD COLUMN is_on_transfer_list INTEGER;   -- 마지막 싱크 시점
ALTER TABLE fut_club_players ADD COLUMN tl_state TEXT;                 -- fut.gg transferListState 원문
ALTER TABLE fut_club_players ADD COLUMN tl_buy_now INTEGER;            -- 즉시 구매가
ALTER TABLE fut_club_players ADD COLUMN tl_expires TEXT;               -- 등록 만료 시각
ALTER TABLE fut_club_players ADD COLUMN tl_last_seen TEXT;             -- 이적 명단에서 마지막으로 본 싱크일(내려간 뒤에도 남는다)
