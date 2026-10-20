-- 111 경기 분석 「전술 분석」 4칸 정형화 (2026-10-20 사용자 지시 「여기도 좀 더 시각화해서 잘 보이게 정리」 —
--     전술 설명·전술적 특성·경기 중 변화·게임 구현 함의가 숫자가 빽빽한 산문 한 덩어리였다).
--
-- 왜 칼럼인가: 산문의 「강점:」「취약:」을 export가 잘라 내면 문장 모양이 바뀔 때 조용히 깨진다 — 수집 회차가
--   처음부터 나눠 적는다(load_match_extras.py의 "tactics" 키). 기존 tactical_* 산문은 원문 그대로 둔다(추가만 · 불변규칙 2).
-- 경기 중 변화는 분 축을 가진 단계라 행(match_tactical_changes)이다 — 경기 흐름(match_phase_metrics)·타임라인과 같은 분 축.
-- 무결정 Δ는 선수 처방 행의 정형 값이다(rationale 산문의 「Δ.011」을 화면이 읽지 않게).
ALTER TABLE match_reports ADD COLUMN tac_possession TEXT;   -- 점유 구조·빌드업(markdown 불릿)
ALTER TABLE match_reports ADD COLUMN tac_defense TEXT;      -- 비점유 구조·압박
ALTER TABLE match_reports ADD COLUMN tac_transition TEXT;   -- 전환·rest-defense·세트피스
ALTER TABLE match_reports ADD COLUMN strengths TEXT;        -- JSON 배열 ["…", …] — 칩
ALTER TABLE match_reports ADD COLUMN weaknesses TEXT;       -- JSON 배열
ALTER TABLE match_reports ADD COLUMN opp_disruption TEXT;   -- 상대가 만든 교란(한 문장)
ALTER TABLE match_reports ADD COLUMN impl_verdict TEXT CHECK (impl_verdict IS NULL OR impl_verdict IN ('유지','추가 관찰','시험 프리셋','정본 변경'));
ALTER TABLE match_reports ADD COLUMN recheck_items TEXT;    -- JSON 배열 — 다음 경기 재검증 체크리스트

CREATE TABLE match_tactical_changes (
  id INTEGER PRIMARY KEY,
  report_id INTEGER NOT NULL REFERENCES match_reports(id),
  seq INTEGER NOT NULL,
  minute INTEGER NOT NULL,          -- 단계 시작 분
  minute_to INTEGER,                -- 끝 분(NULL = 다음 단계까지/종료)
  title TEXT NOT NULL,              -- 짧은 제목(「43′ 뉴캐슬 압박 전환」)
  detail TEXT,                      -- 한두 문장
  source TEXT NOT NULL,
  confidence TEXT NOT NULL,
  UNIQUE (report_id, seq)
);

ALTER TABLE match_player_prescriptions ADD COLUMN fit_delta REAL;   -- 1위 − 2위 커널 적합(≤.05 = 실측 무결정)
ALTER TABLE match_player_prescriptions ADD COLUMN alt_role TEXT;    -- 2위 후보(역할·포커스 한국어 라벨)

INSERT INTO _migration_log (run_at, v1_path, note) VALUES
 ('2026-10-20', '111-match-tactical-structured',
  'match_reports 전술 3단·강점/취약/교란·구현 결론·재검증 + match_tactical_changes + match_player_prescriptions.fit_delta/alt_role — 전술 분석 4칸 시각화(사용자 지시 2026-10-20) · 기존 산문은 원문 유지');
