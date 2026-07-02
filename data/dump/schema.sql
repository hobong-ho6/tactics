CREATE TABLE players(
  id INTEGER PRIMARY KEY,
  name TEXT UNIQUE NOT NULL,
  primary_position TEXT,
  shirt_no INTEGER,
  minutes_2526 INTEGER,
  notes TEXT
);
CREATE TABLE matches(
  id INTEGER PRIMARY KEY,
  date TEXT,
  opponent TEXT,
  competition TEXT,
  venue TEXT,           -- H / A / N
  result TEXT, season TEXT, team TEXT, is_club INTEGER DEFAULT 1,          -- e.g. "W 3-0"
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
  confidence TEXT,
  UNIQUE(player_id, match_id)
);
CREATE VIEW v_best AS
  SELECT p.name, p.primary_position, m.date, m.opponent, m.competition, m.result,
         a.rank_for_player, a.rating, a.minutes, a.position, a.role, a.heat_zones
  FROM appearances a JOIN players p ON p.id=a.player_id JOIN matches m ON m.id=a.match_id
  ORDER BY p.name, a.rank_for_player
/* v_best(name,primary_position,date,opponent,competition,result,rank_for_player,rating,minutes,position,role,heat_zones) */;
CREATE TABLE streaks(id INTEGER PRIMARY KEY, label TEXT UNIQUE, note TEXT, season TEXT);
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
  rationale TEXT,
  PRIMARY KEY(player_id, season, game_version, kind)
);
CREATE TABLE game_tactic_params(
  game_version TEXT NOT NULL,
  param TEXT NOT NULL,        -- build_up_style / defensive_approach / line_height ...
  option TEXT NOT NULL,       -- the selectable value ('numeric' for sliders)
  description TEXT,
  UNIQUE(game_version, param, option)
);
CREATE TABLE team_tactic_setups(
  id INTEGER PRIMARY KEY,
  season TEXT NOT NULL REFERENCES seasons(code),
  game_version TEXT NOT NULL,
  kind TEXT NOT NULL,          -- measured / role / optimal / match:<tag> (joins player_role_map.kind)
  formation TEXT,
  build_up_style TEXT,
  defensive_approach TEXT,
  line_height INTEGER,
  tactic_code TEXT,            -- in-game share code once created & verified in FC26
  rationale TEXT,
  confidence TEXT,
  UNIQUE(season, game_version, kind)
);
CREATE TABLE tactic_observations(
  id INTEGER PRIMARY KEY,
  season TEXT NOT NULL REFERENCES seasons(code),
  scope TEXT NOT NULL,       -- philosophy / build_up / defence / in_possession / modulation / verdict
  claim TEXT NOT NULL,
  evidence TEXT,
  source TEXT,
  confidence TEXT
);
