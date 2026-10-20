-- 108 사용자가 숨긴 진화·SBC 세트 (2026-10-20 사용자 지시
--    「SBC나 진화 카탈로그나 선수별 진화 패스에서 수집한 진화나 sbc를 내가 숨김 처리 하는 기능 — 수행 안 할 진화나 sbc는 숨기고 싶어」).
--
-- 왜 별도 테이블인가: 숨김은 EA·fut.gg가 주는 사실이 아니라 **사용자 판단**이다. 수집 행(fc_evolutions·fc_sbc_sets)에
--   표시를 달면 다음 회차 수집이 새 행을 만들 때 판단이 사라진다 — 수집과 무관한 축으로 둔다(fc_sbc_exclusions와 같은 원칙).
-- ⛔ 수집 행을 지우거나 고치지 않는다(불변규칙 2). 화면은 숨긴 것을 조용히 없애지 않고 건수와 「보기」 토글을 둔다.
-- kind: 'evo' = fc_evolutions.evo_id(카탈로그·선수별 패스·지금 걸 수 있는 진화에서 함께 빠진다) · 'sbc_set' = fc_sbc_sets.set_ea_id.
CREATE TABLE fut_hidden_items (
  id INTEGER PRIMARY KEY,
  game_version TEXT NOT NULL REFERENCES game_versions(code),
  kind TEXT NOT NULL CHECK (kind IN ('evo', 'sbc_set')),
  item_id INTEGER NOT NULL,
  reason TEXT,
  hidden_at TEXT NOT NULL,
  source TEXT NOT NULL,
  UNIQUE (game_version, kind, item_id)
);
INSERT INTO _migration_log (run_at, v1_path, note) VALUES
 ('2026-10-20', '108-user-hidden', 'fut_hidden_items 신설 — 사용자가 화면에서 숨긴 진화·SBC 세트(serve.py /api/fut/hide → fut_club.cmd_hide) · 사용자 지시 2026-10-20 「수행 안 할 진화나 sbc는 숨기고 싶어」');
