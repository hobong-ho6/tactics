-- 123 진화 제거 기록 (2026-10-24 사용자 지시 「FC27에 최근 진화 제거 기능이 있는데 동일하게 진화에 구현해줘」).
--
-- EA 규칙(help.ea.com Ultimate Team Evolutions · 2026-10-24 열람 · 등급 A):
--   ⑴ 「마지막 진화 제거」와 「모든 진화 제거」 두 가지 — 진행 중인 진화도 제거할 수 있다 · 되돌릴 수 없다
--   ⑵ 카드 스탯은 제거한 진화 이전으로 돌아간다(확인 전에 하락 내역을 보여 준다)
--   ⑶ ⭐ **진화 사용(슬롯)은 돌려받지 못한다** — 반복 횟수·1회성 소진은 그대로다
--   ⑷ 원래 거래 가능하던 카드는 **전부 제거해야** 다시 거래 가능 — 마지막 하나만 빼서는 안 된다
-- ⇒ 행을 지우거나 is_void로 돌리지 않는다(is_void = 「적용된 적 없음」 · 소진에서 빠진다 — 뜻이 다르다).
--   removed_at·removed_how를 적고 뷰를 둘로 가른다:
--     v_evo_log         유효 행 전체(제거분 포함) — **소진·이력** 계산용
--     v_evo_log_active  제거분 제외 — **「지금 이 카드에 걸린 진화」**(진화 보호·SBC 제외·직전 상태 사슬·카드 배지)
--     v_evo_log_open    active 중 진행 중
ALTER TABLE fut_evolution_log ADD COLUMN removed_at TEXT;   -- 인게임에서 제거한 날
ALTER TABLE fut_evolution_log ADD COLUMN removed_how TEXT;  -- 'last'(마지막 진화 제거) | 'all'(모든 진화 제거)

DROP VIEW IF EXISTS v_evo_log_open;
CREATE VIEW v_evo_log_active AS                -- 지금 카드에 걸린 진화 = 유효 행 중 제거되지 않은 것
  SELECT * FROM v_evo_log WHERE removed_at IS NULL;
CREATE VIEW v_evo_log_open AS                  -- 진행 중 = 걸려 있고 완료 전
  SELECT * FROM v_evo_log_active WHERE completed_at IS NULL;

INSERT INTO _migration_log (run_at, v1_path, note) VALUES
 ('2026-10-24', '123-evo-removal',
  'fut_evolution_log.removed_at·removed_how + v_evo_log_active(제거분 제외) · v_evo_log_open은 active 기준 — 소진은 v_evo_log(제거분 포함)로 계속 센다(EA: 슬롯 환급 없음) · fut_club.py evo_remove · 화면 「마지막/모든 진화 제거」');
