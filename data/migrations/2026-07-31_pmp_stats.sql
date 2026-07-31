-- 2026-07-31 · 기능축 실측 저장소 확장 (obs#109 ②ⓑ 해소 경로 → obs#116)
-- 문제: 첼시 선수의 기능축 실측(듀얼·인터셉트·패스·캐리)이 DB에 0행이다.
--   그래서 obs#102 ⑷(카이세도 RDM)를 기능축으로 판정할 수 없었고 C5에 첼시 인원이 0명이다.
-- 왜 `appearances`가 아닌가: 그 테이블은 `match_id`가 `matches` FK인데 첼시 경기가 `matches`에 없다.
--   경기 행을 먼저 만들어야 하는 연쇄가 생긴다.
-- 왜 `player_match_positions`인가: 이미 (player_id, event_id) UNIQUE · team · minutes · rating을 갖고
--   `event_id`를 FK 없이 직접 쓴다(`player_match_grids`와 같은 관례). 기능축은 같은 (선수, 경기) 축이므로
--   자연스러운 집이고, 빌라·첼시·리버풀에 동일하게 쓸 수 있다. 순수 ADD COLUMN = 불변규칙 2 준수.
ALTER TABLE player_match_positions ADD COLUMN stats_json TEXT;  -- SofaScore /event/{eid}/player/{pid}/statistics 원값(선별)
