-- 090 진화 EA id 매핑 + 보유 카드의 EA 진화 이력 (2026-09-28 사용자 지시 「진화 이력 EA id 매핑 작업 진행해줘」)
--
-- 왜: 런북은 「어떤 진화를 밟았는지는 싱크로 못 받는다」고 적어 왔다(2026-09-24 실측 — `playerDef`만 봤다).
--   그런데 GG Club **보유행**에 `evolutions`([{evolutionId, repetitionIndex, completedLevels, status}])와
--   `activeEvolution`({evolutionId, level, maxLevel})이 온다(2026-09-28 확인). 두 필드는 id 체계가 다르다:
--     · `evolutions[].evolutionId` = **EA id**(예: 반복 배급 2707)
--     · `activeEvolution.evolutionId` = **fut.gg id**(예: 2489)
--   fut.gg 진화 객체가 `eaId`를 함께 준다(paths API · 2489 ↔ 2707 확인) ⇒ 이름 대조 없이 정확히 잇는다.
-- ⭐ 효과: 「진화 완주 추정」·「어떤 진화였나」를 사람에게 묻지 않고 EA 이력으로 확정할 수 있다.
ALTER TABLE fc_evolutions ADD COLUMN ea_evo_id INTEGER;          -- fut.gg evolution.eaId
ALTER TABLE fut_club_players ADD COLUMN ea_evo_history TEXT;     -- GG Club 보유행 evolutions 원형(JSON · 최신 싱크)
ALTER TABLE fut_club_players ADD COLUMN ea_evo_active TEXT;      -- GG Club 보유행 activeEvolution(JSON · fut.gg id 체계)
