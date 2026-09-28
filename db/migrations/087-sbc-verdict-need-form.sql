-- 087 SBC 판정에 `need_form`(포메이션 미기록)을 더한다 (2026-09-28 사용자 지시
--    「SBC 해법은 포메이션 입력 이후에 계산하도록 고쳐 — 포메이션 없이 계산하는 건 의미없어」)
--
-- 왜: 인게임 SBC는 챌린지마다 포메이션이 고정이다. 종전 sbc_solve.py는 기록이 없으면 흔한 6종 중
--   케미 최대를 골라 **추정 해법**을 저장했고, 화면은 그걸 「포메이션 입력 필요」 배지 아래 보여줬다.
--   포메이션이 다르면 자리·케미가 달라져 그 스쿼드는 인게임에서 그대로 쓸 수 없다 ⇒ 풀지 않는다.
-- ⭐ 스쿼드를 적지 않고 판정만 `need_form`으로 남긴다 — 행을 아예 안 쓰면 화면이 **전날의 추정 해법**을
--   최신으로 읽는다(최신 pulled만 내보내기 때문).
-- ⚠️ SQLite는 CHECK를 ALTER로 못 고친다 ⇒ 테이블 재작성(참조하는 FK 없음).

PRAGMA foreign_keys=OFF;
BEGIN;
CREATE TABLE fc_sbc_solutions_new(
  game_version    TEXT NOT NULL REFERENCES game_versions(code),
  challenge_ea_id INTEGER NOT NULL,
  pulled          TEXT NOT NULL,          -- 판정일 = 그날의 보유 카드 기준이라는 뜻
  account_id      INTEGER REFERENCES fut_accounts(id),
  verdict         TEXT NOT NULL CHECK(verdict IN ('ok','impossible','not_found','oneclick','unparsed','need_form')),
  squad_json      TEXT,                   -- 찾은 스쿼드(선수 id·이름·OVR·클럽·리그·국적)
  team_rating     INTEGER, chem_total INTEGER,
  pool_size       INTEGER,                -- 1인 조건을 통과한 보유 카드 수
  note            TEXT,                   -- 못 맞춘 조건·못 읽은 문장 등
  source TEXT, confidence TEXT,
  PRIMARY KEY(game_version, challenge_ea_id, pulled)
);
INSERT INTO fc_sbc_solutions_new SELECT * FROM fc_sbc_solutions;
DROP TABLE fc_sbc_solutions;
ALTER TABLE fc_sbc_solutions_new RENAME TO fc_sbc_solutions;
COMMIT;
PRAGMA foreign_keys=ON;
