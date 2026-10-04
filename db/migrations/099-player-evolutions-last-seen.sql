-- 099 진화 경로(player_evolutions) — 「바뀐 행만 저장」 (2026-10-04 사용자 결정 「바뀐 행만 저장 (추천)」).
--
-- 왜: 싱크마다 fut.gg 경로 전량(하루 ~2,000행 · ~8MB)을 새 pulled로 다시 적어 DB가 103.8MB가 됐고
--   GitHub 상한(100MB)에 막혀 푸시가 거부됐다. 12,913행 중 9,054행이 직전 관측과 내용이 완전히 같았다.
-- ⭐ 의미: 행 = 「pulled부터 last_seen까지 같은 내용으로 연속 관측된 경로」. 그날 유효한 경로는
--   pulled ≤ 날짜 ≤ last_seen 인 행이다. 관측이 끊겼다 다시 나타나면 **합치지 않는다**(부재도 사실이다).
-- ⚠️ 불변규칙 2(추가만)의 예외 — 지우는 행은 「바로 앞 관측과 같은 값의 반복」뿐이라 정보 손실이 없다.
--    중복 정리는 scripts/migrate_099_evo_dedupe.py가 하고 _migration_log에 건수를 남긴다.
ALTER TABLE player_evolutions ADD COLUMN last_seen TEXT;
UPDATE player_evolutions SET last_seen = pulled WHERE last_seen IS NULL;
CREATE INDEX ix_player_evolutions_seen ON player_evolutions(game_version, base_ea_id, last_seen);
