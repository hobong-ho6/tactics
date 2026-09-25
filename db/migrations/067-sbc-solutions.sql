-- 067 SBC 달성 판정 결과 (2026-09-25 사용자 지시 「sbc 메뉴를 만들고」)
--
-- 왜 표로 두나: 판정은 **탐색**이라 느리고(무작위 재시작) 결과가 시드에 따라 달라진다.
--   화면이 매번 풀면 ⑴ 느리고 ⑵ 새로고침마다 답이 바뀐다. ⇒ `sbc_solve.py --save`가 한 번 풀어 적고
--   화면은 읽기만 한다(export 경유). 다시 풀고 싶으면 스크립트를 다시 돌린다.
--
-- ⛔⛔ `verdict`의 세 값을 섞지 않는다:
--   · `ok`        해를 찾았다 — `squad_json`에 11명(또는 N명)이 들어 있다
--   · `impossible` **불가 확정** — 1인 조건(등급·OVR·리그)을 통과하는 카드가 인원보다 적다
--   · `not_found` **못 찾았을 뿐** — 탐색이 최적을 보장하지 않으므로 「불가능」이 아니다
--   · `oneclick`  원클릭 제출 — fut.gg가 제출 인원을 주지 않아 인원 판정을 하지 않는다
--   · `unparsed`  조건 문장을 못 읽었다 — 판정하지 않는다(조용히 「가능」으로 세지 않기 위해)
CREATE TABLE IF NOT EXISTS fc_sbc_solutions(
  game_version    TEXT NOT NULL REFERENCES game_versions(code),
  challenge_ea_id INTEGER NOT NULL,
  pulled          TEXT NOT NULL,          -- 판정일 = 그날의 보유 카드 기준이라는 뜻
  account_id      INTEGER REFERENCES fut_accounts(id),
  verdict         TEXT NOT NULL CHECK(verdict IN ('ok','impossible','not_found','oneclick','unparsed')),
  squad_json      TEXT,                   -- 찾은 스쿼드(선수 id·이름·OVR·클럽·리그·국적)
  team_rating     INTEGER, chem_total INTEGER,
  pool_size       INTEGER,                -- 1인 조건을 통과한 보유 카드 수
  note            TEXT,                   -- 못 맞춘 조건·못 읽은 문장 등
  source TEXT, confidence TEXT,
  PRIMARY KEY(game_version, challenge_ea_id, pulled)
);
