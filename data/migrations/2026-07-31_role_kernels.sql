-- 2026-07-31 · SSOT 마이그레이션 1단계 (obs#84 ⑨ → obs#105)
-- 목적: 툴 `MAPS`(85 역할×포커스 커널 25자)를 DB로 옮긴다.
--   이 85개 커널은 프로젝트 모든 적합값(placedMap·cmpCos·fit_sim·COLL_CAL·에메리 솔버)의
--   뿌리인데 **툴에만 존재하고 원자료 백업이 없었다** = 손실 위험 최고 블록.
-- 키가 game_role_focus(game_version, role_id, focus) 85행과 **양방향 차집합 0**으로
--   완전 일치함을 확인했으므로, 신설 테이블이 아니라 기존 테이블 확장으로 끝난다.
--   → 행 추가 0건, ALTER 2회 + UPDATE 85건. 불변규칙 2(추가만) 준수, 파괴적 변경 없음.
ALTER TABLE game_role_focus ADD COLUMN kernel25 TEXT;       -- 25자 히트맵 커널 (0/1-9/X, X=최대)
ALTER TABLE game_role_focus ADD COLUMN kernel_source TEXT;  -- 커널 출처(description 출처와 다르다)
