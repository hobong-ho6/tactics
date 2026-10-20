-- 110 카드 포지션 변경 이력 (2026-10-20 사용자 지시 「맥긴 포지션 안 갱신되는 원인 확인」 → 「최신값으로 갱신 + 이력 기록」).
--
-- 왜: `collect_futgg_cards.py`의 upsert가 포지션을 「비었을 때만 채움」으로 저장해, 출시일(2026-09-14)에 받은 값이
--   그대로 굳었다. EA가 그 뒤 대체 포지션을 늘린 카드(맥긴·퀜다 +CM·LW · 소보슬라이 +RM)가 DB에 반영되지 않아
--   진화 요구조건(Position)·SBC·케미 판정이 낡은 포지션으로 돌았다.
-- ⇒ `player_card_items.positions`는 **현재 값**으로 갱신하고(판정 입력이라 현재가 맞아야 한다), 바뀌기 전 값은
--   이 표에 한 줄씩 남긴다(불변규칙 2 — 과거 사실을 잃지 않는다).
-- 기록 기준: 주 포지션 또는 포지션 **집합**이 다를 때만. 순서만 다른 것은 같은 사실이라 기록·갱신하지 않는다.
CREATE TABLE card_position_changes (
  id INTEGER PRIMARY KEY,
  game_version TEXT NOT NULL REFERENCES game_versions(code),
  ea_item_id INTEGER NOT NULL,
  positions_before TEXT,
  positions_after TEXT NOT NULL,
  observed TEXT NOT NULL,
  source TEXT NOT NULL,
  UNIQUE (game_version, ea_item_id, observed)
);
INSERT INTO _migration_log (run_at, v1_path, note) VALUES
 ('2026-10-20', '110-card-position-changes', 'card_position_changes 신설 — collect_futgg_cards.py가 포지션 변경(주 포지션·집합)을 이력 한 줄 + 현재값 갱신으로 반영 · 사용자 지시 2026-10-20 「최신값으로 갱신 + 이력 기록」(맥긴 RM/LM/CAM/RW → RM/CM/LM/CAM/RW/LW)');
