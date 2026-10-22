-- 117 세트피스 키커·타깃 정형 표 (2026-10-22 구현 검토 §2.2 「세트피스 키커·타깃 — 산문뿐」 · §2.3 #9).
--
-- 왜: 게임이 받는 세트피스 입력은 「키커 지정」뿐인데 누가 코너·FK·PK를 차고 누가 받는지가 리포트 산문에만 있었다
--   (바이킹전 「음바예 코너 → 바클리 니어포스트」). 산문은 기계가 대조할 수 없다 — 시즌 집계(키커 빈도·타깃 빈도)가 안 된다.
-- 적재: scripts/load_whoscored.py --apply가 WS 이벤트 qualifier(CornerTaken·FreekickTaken·Penalty·DirectFreekick)로 자동 추출
--   (계산은 core.whoscored.set_pieces). WS JSON이 없는 경기는 SofaScore 슛맵·리포트 서술로 가능한 칸만 채우고 taker_id NULL=결손.
-- 어휘: kind corner|fk|pk · side v/o(다른 match_* 표와 같다 · v=matches.team_code) · flank L/R(코너가 날아온 쪽 · 공격 방향 기준)
--   · outcome goal|shot|retained|lost|saved|miss(슛 결과 또는 볼 소유 유지 여부).
CREATE TABLE match_set_pieces(
  id INTEGER PRIMARY KEY,
  match_id INTEGER NOT NULL REFERENCES matches(id),
  report_id INTEGER REFERENCES match_reports(id),
  kind TEXT NOT NULL CHECK(kind IN ('corner','fk','pk')),
  minute INTEGER NOT NULL,
  side TEXT NOT NULL CHECK(side IN ('v','o')),
  taker_id INTEGER REFERENCES players(id),     -- NULL = 결손(미등록 선수·출처 없음)
  target_id INTEGER REFERENCES players(id),    -- 첫 수신자(코너·FK) · PK는 NULL
  flank TEXT CHECK(flank IS NULL OR flank IN ('L','R')),
  outcome TEXT,
  note TEXT,
  source TEXT NOT NULL,
  confidence TEXT
);
CREATE INDEX ix_match_set_pieces_m ON match_set_pieces(match_id, minute);
INSERT INTO _migration_log (run_at, v1_path, note) VALUES
 ('2026-10-22', '117-match-set-pieces',
  'match_set_pieces 신설 — 코너·FK·PK 키커/타깃/방향/결과 정형(kind corner|fk|pk · side v/o · flank L/R) · core.whoscored.set_pieces + load_whoscored.py --apply 자동 추출 · WS JSON 없는 경기는 SS 슛맵·리포트로 부분 적재');
