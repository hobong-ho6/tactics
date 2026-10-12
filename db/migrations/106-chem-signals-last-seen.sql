-- 106 케미 신호(futgg_chem_signals) — 「바뀐 행만 저장」 (2026-10-12 사용자 결정 「①+② 둘 다 진행」).
--
-- 왜: 싱크마다 보유 카드 전량의 스타일 격자(하루 ~4,400행)를 새 pulled로 다시 적어 DB가 101.2MB가 됐고
--   GitHub 상한(100MB)에 막혀 푸시가 거부됐다(10-04 migration 099에 이어 **두 번째**). 10-10 → 10-11
--   4,406행 중 4,353행(98.8%)이 직전 회차와 값이 같았다.
-- ⭐ 의미: 행 = 「pulled부터 last_seen까지 같은 값으로 연속 관측된 (카드, 스타일)」. 그날 유효한 행은
--   pulled ≤ 날짜 ≤ last_seen 이다. 「연속」은 수집 회차 기준 — 그 카드가 빠진 회차가 끼면 합치지 않는다.
-- ⚠️ 불변규칙 2(추가만)의 예외 — 지우는 행은 「바로 앞 회차와 같은 값의 반복」뿐이라 정보 손실이 없다.
--    중복 정리는 scripts/migrate_106_chem_dedupe.py가 하고 _migration_log에 건수를 남긴다.
-- 정본 규칙: core/chem_signals.py
ALTER TABLE futgg_chem_signals ADD COLUMN last_seen TEXT;
UPDATE futgg_chem_signals SET last_seen = pulled WHERE last_seen IS NULL;
CREATE INDEX ix_futgg_chem_seen ON futgg_chem_signals(ea_item_id, style_name, last_seen);
