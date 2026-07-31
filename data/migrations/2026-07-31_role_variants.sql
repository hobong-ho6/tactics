-- 2026-07-31 · SSOT 마이그레이션 2단계 (obs#105 ⑤ → obs#107)
-- 목적: 툴 `ROLE_VARIANTS`(85 조합 × 217 위치 변형)를 DB로 옮긴다.
--   obs#94에서 `placedMap`이 "슬롯 x에 질량중심이 가장 가까운 변형을 골라 그대로 쓴다"로
--   교체된 이후, **이 변형 표가 placedMap의 실질 본체**다.
-- 1단계(MAPS → game_role_focus.kernel25)와 달리 키가 (role, focus, pitch_x)로 한 단계 깊어
--   기존 테이블 확장이 불가 → 신설. 순수 추가이므로 불변규칙 2 준수, 파괴적 변경 없음.
-- ⚠️ MAPS(85 커널)와 ROLE_VARIANTS는 별개다: MAPS는 커널 1개(중앙판), VARIANTS는 위치별 판.
--   MAPS는 `roleOptions`의 존재 판정에, VARIANTS는 `placedMap`의 실제 선택에 쓰인다.
CREATE TABLE IF NOT EXISTS game_role_variants(
  game_version TEXT NOT NULL,
  role_id      TEXT NOT NULL,
  focus        TEXT NOT NULL,
  pitch_x      INTEGER NOT NULL,   -- 이 변형의 좌우 위치(질량중심 x, 10~90). placedMap이 슬롯 x와 최근접 매칭한다
  kernel25     TEXT NOT NULL,      -- 25자 히트맵 (0/1-9/X, X=최대)
  source       TEXT,
  confidence   TEXT,
  PRIMARY KEY(game_version, role_id, focus, pitch_x)
);
