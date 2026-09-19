-- 046 카드 신체 정보 (2026-09-19, 사용자 지시 「fc27기준 상세 스탯과 스탯에 따른 선수 분석도 채워줘」)
-- player_game_stats(FC27)는 sofifa 미수집분이 많아 나이·키·몸무게가 비어 있다(472행 중 121~132행만 보유).
-- fut.gg 아이템 정의에는 전부 들어 있으므로 카드 표에 함께 담아 화면이 결손을 메운다.
ALTER TABLE player_card_items ADD COLUMN height_cm INTEGER;
ALTER TABLE player_card_items ADD COLUMN weight_kg INTEGER;
ALTER TABLE player_card_items ADD COLUMN birthdate TEXT;
