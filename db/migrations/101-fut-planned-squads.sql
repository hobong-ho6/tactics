-- 101 내가 설계한 얼티밋 스쿼드(EA 활성 스쿼드가 아닌 「저장 처방」) — 2026-10-04 사용자 지시
--   「아틀레티코 세컨팀을 얼티밋팀 화면에서도 보게 — 진행」.
--
-- 왜: 세컨팀 11명이 team_tactic_setups.rationale **산문 안에만** 있었다(값을 산문에 묻지 않는다 — CLAUDE.md DoD 위반).
--   화면이 읽을 수 없고, 카드를 팔아도 어긋남을 알 수 없다. ⇒ 칸 단위로 정형화한다.
-- ⭐ EA 활성 스쿼드(fut_squad_slots · 싱크 실측)와 **다른 층**이다 — 서로 덮지 않는다. 화면은 「저장 처방」 배지를 단다.
-- 팀 설정 3축(빌드업·수비·라인)은 setup_kind로 team_tactic_setups 행을 가리킨다(두 벌로 적지 않는다).
CREATE TABLE fut_planned_squads(
  id           INTEGER PRIMARY KEY,
  account_id   INTEGER NOT NULL REFERENCES fut_accounts(id),
  key          TEXT NOT NULL UNIQUE,      -- 예: atm-second-2026-10-04
  title        TEXT NOT NULL,             -- 화면 칩 이름
  regime_id    INTEGER REFERENCES regimes(id),
  game_version TEXT NOT NULL,
  formation    TEXT NOT NULL,             -- fc_formations.name (예: '4-4-2 (2)')
  setup_kind   TEXT,                      -- team_tactic_setups.kind (같은 regime·season)
  created      TEXT NOT NULL,
  source TEXT, notes TEXT
);
CREATE TABLE fut_planned_squad_slots(
  squad_id       INTEGER NOT NULL REFERENCES fut_planned_squads(id),
  idx            INTEGER NOT NULL,        -- fc_formations.slots 순서(0=GK)
  pos            TEXT NOT NULL,           -- 그 슬롯 라벨(RS·LDM …)
  club_player_id INTEGER NOT NULL REFERENCES fut_club_players(id),
  role_id        TEXT, focus TEXT,        -- 감독 정본 역할(slot_canon_roles에서 옮긴 값)
  PRIMARY KEY(squad_id, idx)
);
