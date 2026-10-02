-- 094 카드별 갤러리 점수 (2026-10-02 사용자 지시 「1번 진행해줘」 — fut.gg gradingScore로 바꾸기)
--
-- 왜: 갤러리 등급 계산에 커뮤니티 정리 점수표(등급 D)를 썼다. fut.gg 카드 정의·목록 API가 카드마다
--   `gradingScore`를 준다(EA 데이터를 fut.gg가 전달 · 등급 B) — 87 레어 5,500 · 83 레어 410 등 표와 일치하고,
--   표에 없는 카드(아이콘·특별 카드·98)까지 값이 있다. ⇒ 이 값을 정본으로 쓰고 표는 결손일 때만 대신한다.
-- ⚠️ 갤러리는 진화 전 원래 카드로 센다 — 이 값은 아이템(ea_item_id) 정의의 값이라 진화와 무관하다.
ALTER TABLE player_card_items ADD COLUMN grading_score INTEGER;
