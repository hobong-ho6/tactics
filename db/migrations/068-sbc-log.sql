-- 068 내가 완료한 SBC 기록 (2026-09-25 사용자 보고로 신설)
--
-- ⛔⛔ **EA도 fut.gg도 「내가 무엇을 완료했는지」를 주지 않는다**(2026-09-25 실측):
--   · GG Club 싱크(EA)는 보유 카드의 최종 상태만 준다 — SBC 이력 없음.
--   · fut.gg `/api/fut/gg-club/?game=27`의 `sbcs`·`sbcChallenges`는 **사용자가 「Mark as Completed」를
--     직접 누른 표시**일 뿐이고 지금 전부 비어 있다. 같은 응답의 `evolutions`도 빈 배열인데
--     실제로는 8명이 진화를 마쳤다 — ⇒ EA 동기화가 아님이 확정된다.
--   ⇒ **진화 로그(fut_evolution_log)와 같은 축**이다: 사용자가 말해 주면 우리가 적는다.
--
-- ⚠️ 챌린지 단위로 적는다 — 세트 전체를 끝내도 「세트 완료」가 아니라 그 세트의 챌린지가 전부 찬 것이다.
--    (Marquee Matchups처럼 4개 중 3개만 한 경우가 실제로 있다.)
CREATE TABLE IF NOT EXISTS fut_sbc_log(
  id INTEGER PRIMARY KEY,
  account_id      INTEGER NOT NULL REFERENCES fut_accounts(id),
  game_version    TEXT NOT NULL REFERENCES game_versions(code),
  set_ea_id       INTEGER NOT NULL,
  challenge_ea_id INTEGER NOT NULL,
  completed_at    TEXT,                 -- 사용자가 알려 준 완료일(모르면 보고받은 날)
  squad_note      TEXT,                 -- 어떤 카드로 냈는지(알면) — 카드 소모 추적의 단서
  source TEXT, confidence TEXT, notes TEXT,
  UNIQUE(account_id, game_version, challenge_ea_id)
);
