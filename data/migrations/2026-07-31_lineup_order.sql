-- 2026-07-31 · player_match_positions 확장 (HANDOFF P0)
-- 목적: SofaScore 라인업 배열 순서를 원천 그대로 보존하고, 그로부터 슬롯을 파생한다.
--   `pos_class`(좌표 밴딩 파생)는 불변규칙 2에 따라 손대지 않는다.
-- 배경: /event/{eid}/lineups 의 `formationPlace`는 전 이벤트에서 NULL이고 `position`은
--   G/D/M/F 4단계뿐이라, HANDOFF가 가정한 "라인업 원천 포지션"은 존재하지 않는다.
--   대신 `players[]` **배열 순서가 포메이션 순서**(GK → 수비 우→좌 → …)임이 실측으로 확인됐다.
ALTER TABLE player_match_positions ADD COLUMN lineup_order INTEGER; -- 선발 XI 내 배열 인덱스(0=GK), 교체출장은 NULL
ALTER TABLE player_match_positions ADD COLUMN formation TEXT;       -- 해당 경기 소속팀 포메이션 문자열
ALTER TABLE player_match_positions ADD COLUMN lineup_pos TEXT;      -- (formation, lineup_order) → 슬롯 파생
