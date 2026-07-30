-- 2026-07-30 팀 축 도입 (A3 감사 권고안 b: 텍스트 team 컬럼 + FK 없는 teams 어휘 테이블)
-- Phase 1: teams 신설 / Phase 2: 무충돌 6테이블 ADD COLUMN team DEFAULT 'AVL' (기존 행 재기록 없음)
-- Phase 3: UNIQUE 충돌 5테이블 재작성 — docs/40-pipeline.md의 "파괴적 변경" 조항 적용(사전 커밋 = 롤백 기준점)
--   team_tactic_setups(team,season,game_version,kind) / team_match_stats PK(event_id,team)
--   transfer_targets(team,window,name,slot) / transfer_ledger(team,window,kind,label) / squad_positions(team,label,slot_type)
-- team_match_stats의 _v/_o 접미는 컬럼명을 유지하고 의미만 상대화한다: _v = 해당 team 행의 팀, _o = 상대.
PRAGMA foreign_keys=OFF;
BEGIN;

CREATE TABLE team_tactic_setups_new(
  id INTEGER PRIMARY KEY,
  team TEXT NOT NULL DEFAULT 'AVL',   -- teams.code (FK 미설정)
  season TEXT NOT NULL REFERENCES seasons(code),
  game_version TEXT NOT NULL,
  kind TEXT NOT NULL,
  formation TEXT, build_up_style TEXT, defensive_approach TEXT, line_height INTEGER,
  tactic_code TEXT, rationale TEXT, confidence TEXT,
  UNIQUE(team, season, game_version, kind)
);
INSERT INTO team_tactic_setups_new SELECT id,'AVL',season,game_version,kind,formation,build_up_style,defensive_approach,line_height,tactic_code,rationale,confidence FROM team_tactic_setups;
DROP TABLE team_tactic_setups;
ALTER TABLE team_tactic_setups_new RENAME TO team_tactic_setups;

CREATE TABLE team_match_stats_new(
  event_id INTEGER NOT NULL,
  team TEXT NOT NULL DEFAULT 'AVL',
  date TEXT,
  xg_v REAL, xg_o REAL, shots_v INT, shots_o INT, sot_v INT, sot_o INT,
  bigch_v INT, bigch_o INT, passes_v INT, passes_o INT,
  long_att_v INT, long_acc_v INT, long_att_o INT, long_acc_o INT,
  cross_att_v INT, cross_acc_v INT, corners_v INT, corners_o INT,
  duelpct_v REAL, fouls_v INT, fouls_o INT,
  formation_v TEXT, formation_o TEXT,
  source TEXT, confidence TEXT,
  PRIMARY KEY(event_id, team)
);
INSERT INTO team_match_stats_new SELECT event_id,'AVL',date,xg_v,xg_o,shots_v,shots_o,sot_v,sot_o,bigch_v,bigch_o,passes_v,passes_o,long_att_v,long_acc_v,long_att_o,long_acc_o,cross_att_v,cross_acc_v,corners_v,corners_o,duelpct_v,fouls_v,fouls_o,formation_v,formation_o,source,confidence FROM team_match_stats;
DROP TABLE team_match_stats;
ALTER TABLE team_match_stats_new RENAME TO team_match_stats;

CREATE TABLE transfer_targets_new(
  id INTEGER PRIMARY KEY,
  team TEXT NOT NULL DEFAULT 'AVL',  -- 영입 주체(분석 대상 팀). club = 매도 클럽이므로 구분한다
  window TEXT NOT NULL,
  name TEXT NOT NULL, name_kr TEXT,
  sofascore_id INTEGER, club TEXT, position TEXT,
  slot TEXT NOT NULL,
  likelihood TEXT,
  map25 TEXT, tool_x REAL, tool_y REAL, sample_n INTEGER, avg_rating REAL,
  opt_role TEXT, opt_focus TEXT, fit_role TEXT, fit_focus TEXT, fit_sim REAL,
  rationale TEXT, source TEXT, confidence TEXT, short_label TEXT, last_news_date TEXT,
  UNIQUE(team, window, name, slot)
);
INSERT INTO transfer_targets_new SELECT id,'AVL',window,name,name_kr,sofascore_id,club,position,slot,likelihood,map25,tool_x,tool_y,sample_n,avg_rating,opt_role,opt_focus,fit_role,fit_focus,fit_sim,rationale,source,confidence,short_label,last_news_date FROM transfer_targets;
DROP TABLE transfer_targets;
ALTER TABLE transfer_targets_new RENAME TO transfer_targets;

CREATE TABLE transfer_ledger_new(
  id INTEGER PRIMARY KEY,
  team TEXT NOT NULL DEFAULT 'AVL',  -- kind(in/out)는 이 팀 관점에서의 방향이다
  window TEXT NOT NULL, kind TEXT NOT NULL, label TEXT NOT NULL,
  amount_m REAL NOT NULL, note TEXT, source TEXT, confidence TEXT,
  UNIQUE(team, window, kind, label)
);
INSERT INTO transfer_ledger_new SELECT id,'AVL',window,kind,label,amount_m,note,source,confidence FROM transfer_ledger;
DROP TABLE transfer_ledger;
ALTER TABLE transfer_ledger_new RENAME TO transfer_ledger;

CREATE TABLE squad_positions_new(
  id INTEGER PRIMARY KEY,
  team TEXT NOT NULL DEFAULT 'AVL',
  label TEXT NOT NULL, slot_type TEXT NOT NULL, lh TEXT NOT NULL, map25 TEXT NOT NULL,
  rate_v REAL, rate_basis TEXT, rate_note TEXT,
  fit_role TEXT, fit_focus TEXT, fit_sim REAL,
  source TEXT, confidence TEXT, sort_order INTEGER,
  UNIQUE(team, label, slot_type)
);
INSERT INTO squad_positions_new SELECT id,'AVL',label,slot_type,lh,map25,rate_v,rate_basis,rate_note,fit_role,fit_focus,fit_sim,source,confidence,sort_order FROM squad_positions;
DROP TABLE squad_positions;
ALTER TABLE squad_positions_new RENAME TO squad_positions;

COMMIT;
PRAGMA foreign_keys=ON;
