-- 109 경기 분석 화면용 정형 축 3개 (2026-10-20 사용자 지시
--    「경기 흐름이나 선수 포인트, 관전 메모 가설 판정, 부상 등에 대해서도 경기 분석에서 항상 제공해줘」).
--
-- 왜: 지금까지 이 셋은 리포트 원문(markdown) 안에만 있었다 — 화면(match-report.html)은 원문을 「펼치기」로만
--   보여줘서 읽히지 않았다. 불변규칙 1(페이지는 export 산출물만 소비)대로 DB 행으로 올린다.
--   부상은 새 표가 아니라 기존 player_status(kind='injury')를 export가 경기 출전자 기준으로 붙인다.
--
-- ⛔ 추가만(불변규칙 2): 가설 판정이 D+N에서 바뀌면 원래 행을 고치지 않고 **새 행**을 넣고
--    supersedes_id로 원래 행을 가리킨다. 화면은 최신 행을 보여주고 이전 판정을 「정정 전」으로 남긴다.
CREATE TABLE match_hypotheses (
  id INTEGER PRIMARY KEY,
  report_id INTEGER NOT NULL REFERENCES match_reports(id),
  seq INTEGER NOT NULL,                 -- 리포트 대조표의 행 번호
  tag TEXT,                             -- Q1·H1·N1 등 관전 메모의 표지(없으면 NULL)
  round TEXT NOT NULL CHECK (round IN ('D0','D1','D2','D3')),   -- 판정한 회차(D0 = 경기 당일·첫 수집)
  claim TEXT NOT NULL,                  -- 사용자 의견(원문 요약)
  measured TEXT NOT NULL,               -- 실측 결과
  evidence TEXT,                        -- 근거 원천(WS·SS·FM·K·기사 …)
  verdict TEXT NOT NULL CHECK (verdict IN ('match','partial','mismatch','undecided','pending')),
  verdict_note TEXT,                    -- 판정 칸의 단서(「위치는 일치 · 관여는 적음」 등)
  supersedes_id INTEGER REFERENCES match_hypotheses(id),
  obs_id INTEGER,
  source TEXT NOT NULL,
  confidence TEXT NOT NULL,
  created_at TEXT NOT NULL,
  UNIQUE (report_id, seq, round)
);

-- 구간별 지표 — 「경기 흐름」 차트의 원료. 구간은 분 단위 [seg_from, seg_to) · seg_to NULL = 종료까지.
-- side: v = 리포트 팀, o = 상대. metric 목록과 화면 라벨의 정본은 core/whoscored.py PHASE_METRICS.
CREATE TABLE match_phase_metrics (
  id INTEGER PRIMARY KEY,
  report_id INTEGER NOT NULL REFERENCES match_reports(id),
  side TEXT NOT NULL CHECK (side IN ('v','o')),
  metric TEXT NOT NULL,
  seg_from INTEGER NOT NULL,
  seg_to INTEGER,
  value REAL NOT NULL,
  n INTEGER,                            -- 표본(이벤트 수 등) — 작으면 화면이 흐리게 그린다
  note TEXT,
  source TEXT NOT NULL,
  confidence TEXT NOT NULL,
  UNIQUE (report_id, side, metric, seg_from)
);

-- 요약 포인트 — 리포트 「## 요약」을 화면 머리에 그대로 올린다(산문 · prose.js 렌더).
ALTER TABLE match_reports ADD COLUMN key_points TEXT;

INSERT INTO _migration_log (run_at, v1_path, note) VALUES
 ('2026-10-20', '109-match-hypotheses-phases',
  'match_hypotheses·match_phase_metrics 신설 + match_reports.key_points — 경기 분석 화면에 가설 판정·구간 흐름·요약을 항상 제공(사용자 지시 2026-10-20) · 부상은 player_status 재사용');
