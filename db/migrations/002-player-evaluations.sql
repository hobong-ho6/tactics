-- 002 · 선수 종합 평가 (2026-08-11)
-- 사용자 요청: 선수 분석 페이지에 종합 평가 영역 — 특성·특장점·감독 3인 전술핏·스탯 기반 평가.
-- 판단 테이블이므로 regime_id 명시(불변규칙 6). 평가 산문은 근거(실측 obs·duties·스탯)를 인용한다.
-- 전술핏은 3감독 공통 컬럼 — 타 팀 감독 핏은 교차 투영이므로 confidence에 그 사실을 명기(불변규칙 7).

CREATE TABLE player_evaluations(
  id INTEGER PRIMARY KEY,
  regime_id INTEGER NOT NULL REFERENCES regimes(id),   -- 선수 소속 팀의 현 체제
  player_id INTEGER NOT NULL REFERENCES players(id),
  overall TEXT NOT NULL,      -- 종합 평가 (등급 접두 'S/A/B/C — ' + 서술)
  traits TEXT,                -- 선수 특성 (플레이 유형·성향)
  strengths TEXT,             -- 특장점 (·약점 병기 허용)
  stat_eval TEXT,             -- 경기 스탯 기반 평가 (v_player_profile·백분위 근거)
  fit_emery TEXT,             -- 에메리(AVL) 전술핏: 'HIGH/MEDIUM/LOW — 서술'
  fit_alonso TEXT,            -- 알론소(CHE) 전술핏
  fit_iraola TEXT,            -- 이라올라(LIV) 전술핏
  source TEXT,                -- 인용한 데이터 (obs#·duties·prescriptions·stats)
  confidence TEXT,            -- 표본·교차투영 캐비앗
  updated TEXT,
  UNIQUE(regime_id, player_id)
);
