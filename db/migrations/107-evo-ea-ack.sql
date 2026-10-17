-- 107 EA 진화 이력 대조 경고의 「사용자 확인 — 우리 기록이 맞다」 표 (2026-10-18 사용자 지시 「전부 다 우리 기록이 맞고」).
--
-- 왜: `evo_detect.py --ea`가 같은 카드·같은 진화에 매 회차 같은 경고를 낸다(코스메틱 로그 · EA 이력이 빈 카드 ·
--   이름이 같은 진화 두 종의 id 갈림). 10-14에 메모리(문서)로 「무시」를 적었는데 10-18에 다시 보고됐다 — 불변규칙 13
--   두 번째 확인이라 문서가 아니라 구조로 막는다: 확인된 쌍은 스크립트가 경고에서 뺀다.
-- 한 행 = (보유 카드, 진화) 하나에 대한 확인. evo_id는 fut.gg id, ea_evo_id는 매핑이 없는 EA id(둘 중 하나만).
-- ⛔ 원장(fut_evolution_log)을 고치지 않는다 — 경고 표시만 끈다. 새 진화·새 카드의 경고는 그대로 뜬다.
CREATE TABLE fut_evo_ea_ack (
  id INTEGER PRIMARY KEY,
  club_player_id INTEGER NOT NULL REFERENCES fut_club_players(id),
  evo_id INTEGER,
  ea_evo_id INTEGER,
  reason TEXT NOT NULL,
  acked_at TEXT NOT NULL,
  source TEXT NOT NULL,
  CHECK ((evo_id IS NULL) <> (ea_evo_id IS NULL)),
  UNIQUE (club_player_id, evo_id, ea_evo_id)
);
INSERT INTO fut_evo_ea_ack (club_player_id, evo_id, ea_evo_id, reason, acked_at, source) VALUES
 (18, 2526, NULL, '코스메틱(Season Ladder Excellence [SP 27]) — EA 이력에 안 잡힘', '2026-10-18', '사용자 확인 2026-10-14·10-18'),
 (18, NULL, 2700, '코스메틱 EA id — fc_evolutions 매핑 없음', '2026-10-18', '사용자 확인 2026-10-14·10-18'),
 (30, 2503, NULL, '코스메틱(Ones to Watch Retro 18 [SP 27]) — EA 이력에 안 잡힘', '2026-10-18', '사용자 확인 2026-10-14·10-18'),
 (30, NULL, 2686, '코스메틱 EA id — fc_evolutions 매핑 없음', '2026-10-18', '사용자 확인 2026-10-14·10-18'),
 (31, 2544, NULL, 'Future Stars Regular Badge — 같은 이름 2종(2544·2553) 중 EA는 2553으로 매핑', '2026-10-18', '사용자 확인 2026-10-14·10-18'),
 (31, 2553, NULL, 'Future Stars Regular Badge — 로그는 2544로 기록(같은 배지)', '2026-10-18', '사용자 확인 2026-10-18'),
 (25, 2489, NULL, 'Alysson EA 이력이 빈 배열(EA 카드 70 ↔ 원장 83 진화 보호) — 원장이 맞다', '2026-10-18', '사용자 확인 2026-10-18'),
 (25, 2534, NULL, 'Alysson EA 이력이 빈 배열(EA 카드 70 ↔ 원장 83 진화 보호) — 원장이 맞다', '2026-10-18', '사용자 확인 2026-10-18');
INSERT INTO _migration_log (run_at, v1_path, note) VALUES
 ('2026-10-18', '107-evo-ea-ack', 'fut_evo_ea_ack 신설 — evo_detect --ea 반복 경고 8쌍(스즈키·마조·헤밍스 코스메틱 · 알리송 Repeat Delivery·Wing Specialization)을 사용자 확인으로 끔 · 사용자 지시 2026-10-18 「전부 다 우리 기록이 맞고」 · 불변규칙 13(10-14 메모리에 이은 두 번째)');
