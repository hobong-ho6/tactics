-- 043 — 카드 획득 경로·신규 알림 (2026-09-19, 사용자 지시 「새로운 선수 카드가 나오면 보여주고 어떻게 하면 얻을 수 있는지도」).
--
-- 왜 컬럼 추가인가: `player_card_items`는 **발매된 아이템 한 장 = 한 행**이고, 「어떻게 얻나」는 그 아이템의 속성이다(별도 층이 아니다).
--   원천은 fut.gg 목록 API의 `isSbc`·`isObjective`·`price`/`hasPrice`·`isSpecial`·`url`. ⚠️ 셋 다 거짓이면 **팩/이적시장**이라는 뜻이고,
--   「알 수 없음」과 구분해야 하므로 수집한 회차에만 채운다(NULL = 미조회).
-- ⭐ `first_seen`: 우리가 **처음 본 날**. released_at(EA 생성일)과 다르다 — 「새 카드 알림」은 우리 기준이라야 한다
--   (과거 카드를 뒤늦게 수집해도 새 카드로 뜨면 안 된다).
PRAGMA foreign_keys = ON;
BEGIN;
ALTER TABLE player_card_items ADD COLUMN acquisition TEXT;      -- 'SBC' | 'Objective' | 'Pack/Market' | NULL(미조회)
ALTER TABLE player_card_items ADD COLUMN is_special INTEGER;    -- fut.gg isSpecial (base 외 특별 카드)
ALTER TABLE player_card_items ADD COLUMN first_seen TEXT;       -- 우리가 처음 적재한 날(YYYY-MM-DD)
COMMIT;
