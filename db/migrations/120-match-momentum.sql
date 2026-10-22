-- 120 경기 모멘텀 분 단위 표 (2026-10-22 경기 데이터 결손 검토 §3-2 · §5 #6).
--
-- 왜: 경기 흐름 3묶음·전술 변화 분 경계가 득점·교체 분으로만 그어졌다(수치 근거 없음). SofaScore `/event/{id}/graph`가
--   분 단위 모멘텀(−100~100 · 홈 우세 +)을 주는데 받지 않았다. FotMob `content.momentum`도 있으나 **한 소스만** 쓴다(SofaScore).
-- 값: `value`는 우리 팀 기준(+ = 우리 우세 · core.momentum.sign_for_side로 부호 통일) · minute는 그래프 분(추가시간은 90+n 그대로).
-- 경계 제안: core.momentum.propose_boundaries — 제안이지 판정이 아니다(match_tactical_changes는 사람이 쓴다).
CREATE TABLE match_momentum(
  id INTEGER PRIMARY KEY,
  match_id INTEGER NOT NULL REFERENCES matches(id),
  minute REAL NOT NULL,
  value INTEGER NOT NULL,
  source TEXT NOT NULL,
  pulled TEXT NOT NULL,
  UNIQUE(match_id, minute, source)
);
CREATE INDEX ix_match_momentum_m ON match_momentum(match_id, minute);
INSERT INTO _migration_log (run_at, v1_path, note) VALUES
 ('2026-10-22', '120-match-momentum',
  'match_momentum 신설 — SofaScore graph 분 단위 모멘텀(우리 팀 기준 부호) · scripts/load_momentum.py · core.momentum 경계 제안');
