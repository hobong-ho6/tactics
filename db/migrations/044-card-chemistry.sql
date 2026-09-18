-- 044 케미스트리 원료 (2026-09-19, 사용자 지시 「적용할 케미스트리도 제안해줘」)
-- 케미스트리는 클럽·리그·국적 **카운트**로 결정된다 — 카드 표에 국적·리그가 없어 계산이 불가능했다.
-- ⭐ 아이콘/히어로의 추가 기여분은 규칙을 하드코딩하지 않고 fut.gg가 주는 extra*Chemistry를 그대로 담는다
--    (EA가 규칙을 바꾸면 소스가 따라 바뀐다 — 우리 코드가 틀릴 여지를 줄인다).
ALTER TABLE player_card_items ADD COLUMN nation TEXT;
ALTER TABLE player_card_items ADD COLUMN league TEXT;
ALTER TABLE player_card_items ADD COLUMN chem_extra TEXT;   -- {"club":0,"league":0,"nation":0}
ALTER TABLE player_card_items ADD COLUMN is_icon INTEGER;
ALTER TABLE player_card_items ADD COLUMN is_hero INTEGER;
