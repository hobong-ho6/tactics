CREATE TABLE players(
  id INTEGER PRIMARY KEY,
  name TEXT UNIQUE NOT NULL,
  primary_position TEXT,
  shirt_no INTEGER,
  minutes_2526 INTEGER,
  notes TEXT
, name_kr TEXT);
CREATE TABLE matches(
  id INTEGER PRIMARY KEY,
  date TEXT,
  opponent TEXT,
  competition TEXT,
  venue TEXT,           -- H / A / N
  result TEXT, season TEXT, team TEXT, is_club INTEGER DEFAULT 1, stage TEXT, possession REAL,          -- e.g. "W 3-0"
  UNIQUE(date, opponent, competition)
);
CREATE TABLE appearances(
  id INTEGER PRIMARY KEY,
  player_id INTEGER NOT NULL REFERENCES players(id),
  match_id INTEGER NOT NULL REFERENCES matches(id),
  rank_for_player INTEGER,   -- 1..3 (Nth best-rated for that player)
  rating REAL,               -- SofaScore
  minutes INTEGER,
  position TEXT,             -- position played that match (AMC, LW, CDM ...)
  role TEXT,                 -- tactical role / description
  heat_zones TEXT,           -- hottest zones summary
  heat_summary TEXT,         -- movement / heatmap description
  goals INTEGER,
  assists INTEGER,
  source TEXT,
  confidence TEXT, heat_map25 TEXT, heat_tool_x REAL, heat_tool_y REAL, xg REAL, xa REAL, key_passes INTEGER, stats_json TEXT,
  UNIQUE(player_id, match_id)
);
CREATE VIEW v_best AS
  SELECT p.name, p.primary_position, m.date, m.opponent, m.competition, m.result,
         a.rank_for_player, a.rating, a.minutes, a.position, a.role, a.heat_zones
  FROM appearances a JOIN players p ON p.id=a.player_id JOIN matches m ON m.id=a.match_id
  ORDER BY p.name, a.rank_for_player
/* v_best(name,primary_position,date,opponent,competition,result,rank_for_player,rating,minutes,position,role,heat_zones) */;
CREATE TABLE streaks(id INTEGER PRIMARY KEY, label TEXT UNIQUE, note TEXT, season TEXT, team TEXT DEFAULT 'AVL');
CREATE TABLE match_streak(match_id INTEGER REFERENCES matches(id), streak_id INTEGER REFERENCES streaks(id), UNIQUE(match_id,streak_id));
CREATE TABLE seasons(
  code TEXT PRIMARY KEY,          -- '2025-26'
  label TEXT
);
CREATE TABLE player_seasons(
  player_id INTEGER REFERENCES players(id),
  season TEXT REFERENCES seasons(code),
  club TEXT DEFAULT 'Aston Villa',
  primary_position TEXT,
  shirt_no INTEGER,
  minutes INTEGER,
  PRIMARY KEY(player_id, season)
);
CREATE TABLE game_roles(
  game_version TEXT,              -- 'FC26'
  role_id TEXT,                   -- 'wm_insidefwd'
  name TEXT,                      -- '인사이드 포워드'
  position_type TEXT,             -- WM
  focuses TEXT,                   -- JSON array of focus names
  PRIMARY KEY(game_version, role_id)
);
CREATE TABLE player_role_map(
  player_id INTEGER REFERENCES players(id),
  season TEXT,
  game_version TEXT,             -- 'FC26' / 'FC27'
  kind TEXT,                     -- 'measured' | 'optimal' | 'role'
  pos_label TEXT,                -- GK/LB/CAM...
  x INTEGER, y INTEGER,
  role_id TEXT,                  -- FK-ish to game_roles(game_version, role_id)
  focus TEXT,
  map25 TEXT,                    -- optional real-heatmap grid
  rationale TEXT, team TEXT DEFAULT 'AVL',
  PRIMARY KEY(player_id, season, game_version, kind)
);
CREATE TABLE game_tactic_params(
  game_version TEXT NOT NULL,
  param TEXT NOT NULL,        -- build_up_style / defensive_approach / line_height ...
  option TEXT NOT NULL,       -- the selectable value ('numeric' for sliders)
  description TEXT,
  UNIQUE(game_version, param, option)
);
CREATE TABLE tactic_observations(
  id INTEGER PRIMARY KEY,
  season TEXT NOT NULL REFERENCES seasons(code),
  scope TEXT NOT NULL,       -- philosophy / build_up / defence / in_possession / modulation / verdict
  claim TEXT NOT NULL,
  evidence TEXT,
  source TEXT,
  confidence TEXT
, team TEXT DEFAULT 'AVL');
CREATE TABLE player_duties(
  id INTEGER PRIMARY KEY,
  season TEXT NOT NULL REFERENCES seasons(code),
  player_id INTEGER NOT NULL REFERENCES players(id),
  position TEXT NOT NULL,
  duties TEXT NOT NULL,
  execution TEXT,
  adherence TEXT,
  game_role_implication TEXT,
  source TEXT,
  confidence TEXT, team TEXT DEFAULT 'AVL',
  UNIQUE(season, player_id, position)
);
CREATE TABLE player_match_positions(
  id INTEGER PRIMARY KEY,
  season TEXT NOT NULL,
  player_id INTEGER NOT NULL REFERENCES players(id),
  event_id INTEGER NOT NULL,     -- SofaScore event id
  date TEXT, opponent TEXT, venue TEXT, competition TEXT,
  minutes INTEGER, rating REAL,
  avg_x REAL, avg_y REAL,        -- SofaScore average-position (x attack dir, y low=right)
  started INTEGER,               -- 1=start, 0=sub appearance
  pos_class TEXT,                -- classified slot; NULL when minutes<45 (avg unreliable)
  source TEXT, confidence TEXT, team TEXT DEFAULT 'AVL', lineup_order INTEGER, formation TEXT, lineup_pos TEXT,
  UNIQUE(player_id, event_id)
);
CREATE VIEW v_position_profile AS
SELECT p.name, pmp.player_id, pmp.pos_class,
       COUNT(*) apps, SUM(pmp.minutes) mins,
       ROUND(AVG(pmp.rating),2) avg_rating, MAX(pmp.rating) best,
       ROUND(AVG(pmp.avg_x),1) ax, ROUND(AVG(pmp.avg_y),1) ay
FROM player_match_positions pmp JOIN players p ON p.id=pmp.player_id
WHERE pmp.pos_class IS NOT NULL
GROUP BY pmp.player_id, pmp.pos_class
/* v_position_profile(name,player_id,pos_class,apps,mins,avg_rating,best,ax,ay) */;
CREATE TABLE player_fc_stats(
  id INTEGER PRIMARY KEY,
  game_version TEXT NOT NULL,            -- 'FC26'
  roster_date TEXT,                      -- sofifa roster update the stats were read from
  name_kr TEXT NOT NULL,                 -- transfer_targets.name_kr / 툴 표기와 동일
  player_id INTEGER REFERENCES players(id),  -- NULL = 외부(이적 후보)
  sofifa_id INTEGER,                     -- NULL = FC26 DB에 없는 선수
  sofifa_name TEXT,
  club TEXT,
  positions TEXT,                        -- 'CAM,LM,CM' (sofifa 등록 포지션)
  best_pos TEXT,                         -- sofifa 계산 최적 포지션
  age INTEGER, height_cm INTEGER, value_eur TEXT,
  ovr INTEGER, pot INTEGER,
  pac INTEGER, sho INTEGER, pas INTEGER, dri INTEGER, def INTEGER, phy INTEGER,
  -- GK 행의 6개 스탯 = 다이빙/핸들링/킥/반응속도/속도/위치선정
  source TEXT, confidence TEXT, attrs TEXT, playstyles TEXT, traits TEXT, detail_date TEXT, role_familiarity TEXT, accelerate TEXT, body_type TEXT, preferred_foot TEXT, role_detail TEXT,
  UNIQUE(game_version, name_kr)
);
CREATE VIEW v_event_profile AS
SELECT p.name, a.player_id, COUNT(*) n,
 ROUND(AVG(a.xg),2) xg_pm, ROUND(AVG(a.xa),2) xa_pm, ROUND(AVG(a.key_passes),1) kp_pm,
 ROUND(AVG(json_extract(a.stats_json,'$.duels_won')),1) duelw_pm,
 ROUND(AVG(json_extract(a.stats_json,'$.tackles')),1) tkl_pm,
 ROUND(AVG(json_extract(a.stats_json,'$.interceptions')),1) int_pm,
 ROUND(AVG(json_extract(a.stats_json,'$.dribbles_won')),1) drb_pm,
 ROUND(AVG(json_extract(a.stats_json,'$.passes_acc')*1.0/NULLIF(json_extract(a.stats_json,'$.passes_total'),0)),2) pass_pct
FROM appearances a JOIN players p ON p.id=a.player_id
WHERE a.stats_json IS NOT NULL GROUP BY a.player_id
/* v_event_profile(name,player_id,n,xg_pm,xa_pm,kp_pm,duelw_pm,tkl_pm,int_pm,drb_pm,pass_pct) */;
CREATE TABLE player_shot_profile(
  player_id INTEGER PRIMARY KEY REFERENCES players(id),
  window TEXT,             -- sample window note
  events_n INTEGER, shots INTEGER, xg_sum REAL,
  box_n INTEGER, sixyard_n INTEGER, headers INTEGER, goals INTEGER,
  mean_dist REAL,          -- mean playerCoordinates.x = distance from OPPONENT goal line (0=goal)
  mean_y REAL,             -- lateral (SofaScore y, low=right assumed as heatmap)
  source TEXT, confidence TEXT
);
CREATE TABLE ingame_checks(
  id INTEGER PRIMARY KEY,
  checked_at TEXT,            -- 날짜
  preset TEXT,                -- (역할) / (최적) / 스쿼드 변형명
  tactic_code TEXT,           -- 게임 공유 코드
  matches_played INTEGER,
  position TEXT, player TEXT,
  axis TEXT,                  -- shape(히트맵) / function(스탯) / arrival(득점유형)
  expected TEXT,              -- 실측 기준 기대값
  observed TEXT,              -- 게임에서 관찰된 것
  verdict TEXT,               -- MATCH / PARTIAL / MISMATCH
  action TEXT                 -- 유지 / 역할변경 / 포커스변경 / 팀설정변경
);
CREATE TABLE transfer_outgoing(
  id INTEGER PRIMARY KEY,
  window TEXT NOT NULL,
  player_id INTEGER NOT NULL REFERENCES players(id),
  dest_club TEXT,
  likelihood TEXT,
  rationale TEXT,
  source TEXT,
  confidence TEXT, last_news_date TEXT, team TEXT DEFAULT 'AVL',
  UNIQUE(window, player_id)
);
CREATE TABLE teams(
  code TEXT PRIMARY KEY,        -- 'AVL' / 'CHE' — 분석 주체 팀 코드 (FK는 걸지 않는다: 기존 행 재작성 회피)
  name TEXT NOT NULL,           -- 정규 영문 표기
  name_kr TEXT,
  manager TEXT,
  note TEXT
);
CREATE TABLE IF NOT EXISTS "team_tactic_setups"(
  id INTEGER PRIMARY KEY,
  team TEXT NOT NULL DEFAULT 'AVL',   -- teams.code (FK 미설정)
  season TEXT NOT NULL REFERENCES seasons(code),
  game_version TEXT NOT NULL,
  kind TEXT NOT NULL,
  formation TEXT, build_up_style TEXT, defensive_approach TEXT, line_height INTEGER,
  tactic_code TEXT, rationale TEXT, confidence TEXT,
  UNIQUE(team, season, game_version, kind)
);
CREATE TABLE IF NOT EXISTS "team_match_stats"(
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
CREATE TABLE IF NOT EXISTS "transfer_targets"(
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
CREATE TABLE IF NOT EXISTS "transfer_ledger"(
  id INTEGER PRIMARY KEY,
  team TEXT NOT NULL DEFAULT 'AVL',  -- kind(in/out)는 이 팀 관점에서의 방향이다
  window TEXT NOT NULL, kind TEXT NOT NULL, label TEXT NOT NULL,
  amount_m REAL NOT NULL, note TEXT, source TEXT, confidence TEXT,
  UNIQUE(team, window, kind, label)
);
CREATE TABLE IF NOT EXISTS "squad_positions"(
  id INTEGER PRIMARY KEY,
  team TEXT NOT NULL DEFAULT 'AVL',
  label TEXT NOT NULL, slot_type TEXT NOT NULL, lh TEXT NOT NULL, map25 TEXT NOT NULL,
  rate_v REAL, rate_basis TEXT, rate_note TEXT,
  fit_role TEXT, fit_focus TEXT, fit_sim REAL,
  source TEXT, confidence TEXT, sort_order INTEGER,
  UNIQUE(team, label, slot_type)
);
CREATE TABLE player_match_grids(
  team TEXT NOT NULL DEFAULT 'AVL', season TEXT NOT NULL,
  player_id INTEGER REFERENCES players(id), name_kr TEXT NOT NULL,
  event_id INTEGER NOT NULL, possession REAL, hit_points INTEGER,
  cells TEXT NOT NULL, map25 TEXT, source TEXT, confidence TEXT,
  PRIMARY KEY(name_kr, event_id));
CREATE TABLE game_role_focus(
  game_version TEXT NOT NULL,
  role_id TEXT NOT NULL,
  focus TEXT NOT NULL,
  ea_role_name TEXT,          -- EA/fut.gg 표기 역할명
  description TEXT,           -- 포커스 1차 정의문 (EA 원문)
  plus TEXT,                  -- JSON array — 그 포커스가 강화하는 특성
  equal TEXT,                 -- JSON array — 중립 특성
  negative TEXT,              -- JSON array — 희생되는 특성
  side_conflict INTEGER DEFAULT 0,  -- 1 = fut.gg의 좌/우 변형이 서로 다른 값을 준 항목
  note TEXT,
  source TEXT, kernel25 TEXT, kernel_source TEXT,
  PRIMARY KEY(game_version, role_id, focus)
);
CREATE TABLE game_role_variants(
  game_version TEXT NOT NULL,
  role_id      TEXT NOT NULL,
  focus        TEXT NOT NULL,
  pitch_x      INTEGER NOT NULL,   -- 이 변형의 좌우 위치(질량중심 x, 10~90). placedMap이 슬롯 x와 최근접 매칭한다
  kernel25     TEXT NOT NULL,      -- 25자 히트맵 (0/1-9/X, X=최대)
  source       TEXT,
  confidence   TEXT,
  PRIMARY KEY(game_version, role_id, focus, pitch_x)
);
