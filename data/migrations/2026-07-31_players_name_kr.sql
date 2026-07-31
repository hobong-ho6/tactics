-- 2026-07-31 · SSOT 마이그레이션 3단계 (obs#105 ⑤ → obs#115)
-- 목적: `players`에 한글 표기 컬럼을 신설한다.
--   `players.name`은 전부 영문("John McGinn")인데 툴의 모든 인선 블록은 한글 라벨이라,
--   지금은 FORMATIONS·CMP_SLOTS·SQUAD_SLOTS·FUNC_AXIS 어떤 블록도 DB에서 생성할 수 없다.
--   → 4단계 이하 전부의 차단 요소이므로 먼저 푼다.
-- 값의 형태(obs#115): 접두·접미 없는 순수 한글 표기. 성만으로 유일하면 성, 충돌하면 '이름 성'.
--   원천은 `player_fc_stats.name_kr` 중 player_id NOT NULL인 22행 — 이 22개는 툴 키와 **정확히 일치**한다.
-- ⚠️ 나머지 행은 NULL로 둔다. 추측으로 채우면 불변규칙 3(실측>서사) 위반이고,
--   그 선수들은 이 4블록에 원천이 없다.
ALTER TABLE players ADD COLUMN name_kr TEXT;   -- 툴 라벨 정본(접미 없음). NULL = 원천 미확보
