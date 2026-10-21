-- 114 판정 쟁점(claim_issues) — 영상 구현 주장 PENDING을 「닫히는 구조」로 (2026-10-21 사용자 지시
--     「영상분석의 판정대기는 언제 판정완료되는거야?」 → 「이 구조를 만들자」).
--
-- 왜: PENDING 165건의 「판정 조건」이 verdict_note 산문에만 있어 기계가 셀 수 없었다 — G17은 건수만 셌고,
--   match-watch·주간 예약 어디에도 「조건이 찬 주장을 다시 판정한다」 단계가 없었다 ⇒ 사람이 따로 보지 않으면 영원히 대기.
--   같은 조건의 주장이 여러 영상에 흩어져 있어(잭슨 역할 계열 약 20행) 한 번 판정으로 닫혀야 할 것이 행마다 따로 남았다.
-- 구조: ① 판정 조건이 같은 PENDING 주장을 **쟁점 1행**으로 묶는다(video_impl_claims.issue_id)
--       ② 조건을 셀 수 있는 트리거로 둔다(팀 공식전 N경기 · 선수 선발 N경기 · 날짜) — 판정 로직 정본 core/claim_issues.py
--       ③ 트리거가 찬 쟁점은 scripts/claim_issues.py --due 목록에 뜨고, 찬 뒤 7일이 지나도 열려 있으면 G39가 막는다
--       ④ --close로 쟁점을 닫으면 묶인 PENDING 주장의 verdict가 한 번에 바뀐다(verdict_note에 판정 이력을 덧붙인다 — 지우지 않음)
CREATE TABLE claim_issues(
  id INTEGER PRIMARY KEY,
  team_code TEXT NOT NULL REFERENCES teams(code),
  title_kr TEXT NOT NULL,           -- 쟁점 이름 ≤40자(질문의 이름 — 결론이 아니다)
  question_kr TEXT NOT NULL,        -- 무엇을 판정하나
  measure_kr TEXT NOT NULL,         -- 판정에 쓸 실측(표·지표·기준값)
  trigger_kind TEXT NOT NULL CHECK(trigger_kind IN ('matches','player_starts','date')),
  trigger_n INTEGER,                -- matches·player_starts: 몇 경기
  trigger_comp TEXT CHECK(trigger_comp IS NULL OR trigger_comp IN ('league','official')),
  trigger_player_id INTEGER REFERENCES players(id),
  trigger_pos TEXT,                 -- player_starts: pos_class CSV(선택)
  trigger_date TEXT,                -- date: 이 날짜가 지나면
  since TEXT,                       -- matches·player_starts: 이 날짜 **이후** 경기부터 센다
  hold INTEGER NOT NULL DEFAULT 0,  -- 1 = 그 팀 수집 보류 중(CHE·LIV·ATM 2026-10-20~) — G39 기한 검사 제외
  status TEXT NOT NULL DEFAULT 'open' CHECK(status IN ('open','closed')),
  resolution TEXT CHECK(resolution IS NULL OR resolution IN ('APPLIED','HELD','REJECTED')),
  resolution_note TEXT,             -- 판정 근거(실측 수치) — 닫을 때 필수
  closed TEXT,
  source TEXT, confidence TEXT,
  created TEXT NOT NULL DEFAULT (date('now')),
  CHECK(trigger_kind <> 'date' OR trigger_date IS NOT NULL),
  CHECK(trigger_kind = 'date' OR (trigger_n IS NOT NULL AND since IS NOT NULL)),
  CHECK(trigger_kind <> 'player_starts' OR trigger_player_id IS NOT NULL),
  CHECK(status = 'open' OR (resolution IS NOT NULL AND resolution_note IS NOT NULL AND closed IS NOT NULL))
);
ALTER TABLE video_impl_claims ADD COLUMN issue_id INTEGER REFERENCES claim_issues(id);
CREATE INDEX ix_vic_issue ON video_impl_claims(issue_id);
INSERT INTO _migration_log (run_at, v1_path, note) VALUES
 ('2026-10-21', '114-claim-issues',
  'claim_issues 신설 + video_impl_claims.issue_id — PENDING을 판정 조건별 쟁점으로 묶고 트리거(팀 공식전 N·선수 선발 N·날짜)로 기한을 둔다 · core/claim_issues.py 판정 정본 · scripts/claim_issues.py --due/--close · G39');
