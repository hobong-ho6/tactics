CREATE TABLE game_versions(
  code TEXT PRIMARY KEY,            -- 'FC26', 'FC27'
  released TEXT,                    -- 발매일 (YYYY-MM-DD, 예정이면 NULL)
  notes TEXT
);
CREATE TABLE teams(
  code TEXT PRIMARY KEY,            -- 'AVL' / 'CHE' / 'LIV'
  name TEXT NOT NULL,               -- 정규 영문 표기 (SofaScore 표기 기준)
  name_kr TEXT,
  sofascore_id INTEGER,             -- SofaScore 팀 id
  fotmob_id INTEGER,                -- Fotmob rumours teamIds (이적 감시용)
  note TEXT
);
CREATE TABLE regimes(
  id INTEGER PRIMARY KEY,
  team_code TEXT NOT NULL REFERENCES teams(code),
  manager TEXT NOT NULL,            -- 'Unai Emery'
  manager_kr TEXT,
  start TEXT,                       -- 부임일 (YYYY-MM-DD)
  end TEXT,                         -- NULL = 현직
  is_main INTEGER DEFAULT 0,        -- 1 = 주 분석 대상 (에메리·빌라)
  note TEXT,
  UNIQUE(team_code, manager, start)
);
CREATE TABLE seasons(
  code TEXT PRIMARY KEY,            -- '2025-26'
  label TEXT
);
CREATE TABLE players(
  id INTEGER PRIMARY KEY,
  name TEXT UNIQUE NOT NULL,        -- 정규 영문 표기
  name_kr TEXT,                     -- 툴 표시명 (조인 키로 쓰지 말 것)
  sofascore_id INTEGER,             -- v1에서는 notes 산문에 갇혀 있었다 — 컬럼 승격
  sofifa_id INTEGER,
  birth_year INTEGER,
  primary_position TEXT,
  notes TEXT
, fotmob_id INTEGER, nationality TEXT, understat_id INTEGER, positions_alt TEXT);
CREATE TABLE player_tenures(
  player_id INTEGER NOT NULL REFERENCES players(id),
  season TEXT NOT NULL REFERENCES seasons(code),
  club_code TEXT,                   -- teams.code 또는 외부 클럽명 그대로 (외부는 코드 없음)
  club_name TEXT,                   -- 표시용
  position TEXT, shirt_no INTEGER, minutes INTEGER,
  PRIMARY KEY(player_id, season)
);
CREATE TABLE matches(
  id INTEGER PRIMARY KEY,           -- v1 id 승계
  event_id INTEGER,                 -- SofaScore event id (아는 경우)
  team_code TEXT NOT NULL REFERENCES teams(code),
  season TEXT REFERENCES seasons(code),
  date TEXT, opponent TEXT, competition TEXT,
  venue TEXT,                       -- H / A / N
  result TEXT, is_club INTEGER DEFAULT 1, stage TEXT, possession REAL,
  UNIQUE(team_code, date, opponent, competition)
);
CREATE TABLE player_matches(
  id INTEGER PRIMARY KEY,
  player_id INTEGER NOT NULL REFERENCES players(id),
  event_id INTEGER,                 -- SofaScore event id
  match_id INTEGER REFERENCES matches(id),
  team_code TEXT,                   -- 그 경기에서 소속(클럽/대표팀 구분은 competition으로)
  season TEXT,
  date TEXT, opponent TEXT, venue TEXT, competition TEXT,
  minutes INTEGER, rating REAL, started INTEGER,
  lineup_pos TEXT,                  -- SofaScore lineups position (G/D/M/F)
  pos_class TEXT,                   -- 분류된 슬롯 (v1 승계 — lineup_pos보다 세밀, NULL 가능)
  lineup_order INTEGER, formation TEXT,
  avg_x REAL, avg_y REAL,           -- SofaScore 평균 위치 (x 공격방향, y 낮음=오른쪽)
  possession REAL,                  -- 그 경기 팀 점유율 (@dom/@tight·국면 분리의 원료 — obs#96·#101)
  hit_points INTEGER,               -- 히트맵 포인트 수 (15 미만이면 그리드 무효 — docs/30 ③)
  cells TEXT,                       -- 5×5 원자료 카운트 CSV (무손실 — map25의 소스)
  map25 TEXT,                       -- 인코딩 그리드 (X=최대, round(v/max*10), 9 클램프)
  xg REAL, xa REAL, key_passes INTEGER,
  duels_won INTEGER, duels_lost INTEGER, tackles INTEGER, interceptions INTEGER,
  goals INTEGER, assists INTEGER, touches INTEGER, recoveries INTEGER,
  stats_json TEXT,                  -- 위 컬럼 외 롱테일 (⚠️ 0은 API 키 생략의 확정값 — docs/30 ①)
  role_note TEXT,                   -- v1 appearances.role (서술)
  heat_note TEXT,                   -- v1 appearances.heat_zones + heat_summary (서술)
  source TEXT, confidence TEXT, cells_poss TEXT, cells_def TEXT, map25_poss TEXT, map25_def TEXT, phase_source TEXT,
  UNIQUE(player_id, event_id),
  CHECK(event_id IS NOT NULL OR match_id IS NOT NULL)
);
CREATE TABLE team_match_stats(      -- v1 그대로 (team → team_code만 정규화)
  event_id INTEGER NOT NULL,
  team_code TEXT NOT NULL REFERENCES teams(code),
  date TEXT,
  xg_v REAL, xg_o REAL, shots_v INT, shots_o INT, sot_v INT, sot_o INT,
  bigch_v INT, bigch_o INT, passes_v INT, passes_o INT,
  long_att_v INT, long_acc_v INT, long_att_o INT, long_acc_o INT,
  cross_att_v INT, cross_acc_v INT, corners_v INT, corners_o INT,
  duelpct_v REAL, fouls_v INT, fouls_o INT,
  formation_v TEXT, formation_o TEXT,
  source TEXT, confidence TEXT, ppda_v REAL, ppda_o REAL, ppda_num_v INTEGER, ppda_den_v INTEGER, ppda_num_o INTEGER, ppda_den_o INTEGER, ppda_method TEXT, aerial_won_v INTEGER, aerial_att_v INTEGER, aerial_won_o INTEGER, aerial_att_o INTEGER, dribble_succ_v INTEGER, dribble_att_v INTEGER, dribble_succ_o INTEGER, dribble_att_o INTEGER, tackles_v INTEGER, tackles_o INTEGER, interceptions_v INTEGER, interceptions_o INTEGER, clearances_v INTEGER, clearances_o INTEGER, xg_op_v REAL, xg_op_o REAL, blocked_v INTEGER, blocked_o INTEGER, xg_source TEXT, def_x_v REAL, def_x_o REAL, def_x_method TEXT,
  PRIMARY KEY(event_id, team_code)
);
CREATE TABLE player_shot_profile(   -- v1 그대로
  player_id INTEGER PRIMARY KEY REFERENCES players(id),
  window TEXT, events_n INTEGER, shots INTEGER, xg_sum REAL,
  box_n INTEGER, sixyard_n INTEGER, headers INTEGER, goals INTEGER,
  mean_dist REAL, mean_y REAL,
  source TEXT, confidence TEXT
, penalties INTEGER, npxg_sum REAL);
CREATE TABLE streaks(
  id INTEGER PRIMARY KEY, label TEXT UNIQUE, note TEXT,
  season TEXT, team_code TEXT REFERENCES teams(code)
);
CREATE TABLE match_streak(
  match_id INTEGER REFERENCES matches(id),
  streak_id INTEGER REFERENCES streaks(id),
  UNIQUE(match_id, streak_id)
);
CREATE TABLE observations(
  id INTEGER PRIMARY KEY,
  regime_id INTEGER REFERENCES regimes(id),
  season TEXT REFERENCES seasons(code),
  scope TEXT NOT NULL,              -- philosophy/build_up/defence/in_possession/modulation/verdict/reference
  claim TEXT NOT NULL,
  evidence TEXT, source TEXT, confidence TEXT
);
CREATE TABLE manager_profiles(
  regime_id INTEGER NOT NULL REFERENCES regimes(id),
  axis TEXT NOT NULL,
  content TEXT NOT NULL,            -- 확정 결론 (2~5문장)
  evidence TEXT,                    -- obs#/문서 상호참조
  source TEXT, confidence TEXT,
  updated TEXT,                     -- YYYY-MM-DD
  PRIMARY KEY(regime_id, axis)
);
CREATE TABLE player_duties(         -- v1 그대로 (team → regime_id)
  id INTEGER PRIMARY KEY,
  regime_id INTEGER REFERENCES regimes(id),
  season TEXT NOT NULL REFERENCES seasons(code),
  player_id INTEGER NOT NULL REFERENCES players(id),
  position TEXT NOT NULL,
  duties TEXT NOT NULL, execution TEXT, adherence TEXT,
  game_role_implication TEXT,
  source TEXT, confidence TEXT, observed_from TEXT, observed_to TEXT, sample_scope TEXT, sample_note TEXT, applied_status TEXT, applied_note TEXT,
  UNIQUE(season, player_id, position)
);
CREATE TABLE game_roles(
  game_version TEXT NOT NULL REFERENCES game_versions(code),
  role_id TEXT NOT NULL,            -- 'wm_insidefwd'
  name TEXT, name_en TEXT,
  position_type TEXT,               -- GK/CB/FB/DM/CM/CAM/WM/W/ST (슬롯 타입 필터의 정본 — obs#141)
  focuses TEXT,                     -- JSON array
  PRIMARY KEY(game_version, role_id)
);
CREATE TABLE game_role_focus(       -- 커널 85개 — 모든 적합값의 뿌리 (obs#105). v1 전 컬럼 승계
  game_version TEXT NOT NULL,
  role_id TEXT NOT NULL,
  focus TEXT NOT NULL,
  ea_role_name TEXT,                -- EA/fut.gg 표기 역할명
  description TEXT,                 -- 포커스 1차 정의문 (EA 원문)
  plus TEXT, equal TEXT, negative TEXT,   -- JSON array — 강화/중립/희생 특성
  side_conflict INTEGER DEFAULT 0,  -- 1 = fut.gg 좌/우 변형이 서로 다른 값
  note TEXT, source TEXT,
  kernel25 TEXT, kernel_source TEXT, movement_kr TEXT,
  PRIMARY KEY(game_version, role_id, focus)
);
CREATE TABLE game_role_variants(    -- 위치 변형 217개 — placedMap의 실질 본체 (obs#94·#107)
  game_version TEXT NOT NULL,
  role_id TEXT NOT NULL,
  focus TEXT NOT NULL,
  pitch_x INTEGER NOT NULL,         -- 변형 질량중심 x (placedMap이 슬롯 x와 최근접 매칭)
  kernel25 TEXT NOT NULL,
  source TEXT, confidence TEXT,
  PRIMARY KEY(game_version, role_id, focus, pitch_x)
);
CREATE TABLE game_tactic_params(    -- v1 그대로
  game_version TEXT NOT NULL,
  param TEXT NOT NULL, option TEXT NOT NULL, description TEXT,
  UNIQUE(game_version, param, option)
);
CREATE TABLE player_game_stats(
  id INTEGER PRIMARY KEY,
  game_version TEXT NOT NULL REFERENCES game_versions(code),
  roster_date TEXT,                 -- sofifa 로스터 갱신일 — 같은 버전 안의 시점 축
  player_id INTEGER REFERENCES players(id),   -- NULL = 외부(영입 후보 등)
  name_kr TEXT NOT NULL,            -- 표시용 (조인 금지)
  sofifa_id INTEGER, sofifa_name TEXT, club TEXT,
  positions TEXT, best_pos TEXT,
  age INTEGER, height_cm INTEGER, value_eur TEXT,
  ovr INTEGER, pot INTEGER,
  pac INTEGER, sho INTEGER, pas INTEGER, dri INTEGER, def INTEGER, phy INTEGER,
  attrs TEXT, playstyles TEXT, traits TEXT,
  role_familiarity TEXT, role_detail TEXT,
  accelerate TEXT, body_type TEXT, preferred_foot TEXT,
  detail_date TEXT, source TEXT, confidence TEXT, nationality TEXT, full_name TEXT, weight_kg INTEGER, card_image_url TEXT,
  UNIQUE(game_version, roster_date, name_kr)
);
CREATE TABLE game_system_changes(
  id INTEGER PRIMARY KEY,
  game_version TEXT NOT NULL REFERENCES game_versions(code),  -- 변화가 도입된 버전
  area TEXT NOT NULL,               -- roles/tactics/positioning/attributes/playstyles/engine/meta
  change TEXT NOT NULL,             -- 무엇이 바뀌었나
  evidence TEXT,                    -- EA 피치노트 인용·실측 근거
  impact TEXT,                      -- 이 시스템(실측→구현 매핑)에 미치는 영향
  source TEXT, confidence TEXT,
  recorded TEXT                     -- YYYY-MM-DD
);
CREATE TABLE slots(                 -- 오늘(v1) 만든 team_slots의 승계 — regime 슬롯 기하
  regime_id INTEGER NOT NULL REFERENCES regimes(id),
  formation TEXT NOT NULL,          -- '4-2-3-1 Wide' / '3-4-2-1' — 같은 regime의 복수 포메이션 허용
  pos TEXT NOT NULL,                -- GK/LB/LCB/CCB/RCB/RB/LDM/RDM/LM/CAM/RM/ST
  slot_type TEXT NOT NULL,          -- 커널 역할군 (game_roles.position_type과 매칭 — obs#141 필터)
  x INTEGER NOT NULL, y INTEGER NOT NULL,
  sort_order INTEGER NOT NULL,
  source TEXT, confidence TEXT,
  PRIMARY KEY(regime_id, formation, pos)
);
CREATE TABLE prescriptions(
  id INTEGER PRIMARY KEY,
  player_id INTEGER NOT NULL REFERENCES players(id),
  regime_id INTEGER REFERENCES regimes(id),
  season TEXT REFERENCES seasons(code),
  game_version TEXT REFERENCES game_versions(code),
  kind TEXT NOT NULL,
  pos_label TEXT,
  x INTEGER, y INTEGER,
  role_id TEXT, focus TEXT,
  map25 TEXT,
  fit_sim REAL, sample_n INTEGER, avg_rating REAL, minutes INTEGER,
  rationale TEXT, starter INTEGER DEFAULT 0, grid_club TEXT,                   -- 근거 서술 전용 (값은 위 컬럼으로)
  UNIQUE(player_id, regime_id, season, game_version, kind)
);
CREATE TABLE squad_entries(
  id INTEGER PRIMARY KEY,
  regime_id INTEGER NOT NULL REFERENCES regimes(id),
  player_id INTEGER NOT NULL REFERENCES players(id),
  label TEXT,                       -- 표시용 오버라이드 (예: '아브라함(보유)') — NULL이면 name_kr
  slot_type TEXT NOT NULL,
  lh TEXT NOT NULL,                 -- OWNED/CONFIRMED/…
  map25 TEXT NOT NULL,
  rate_v REAL, rate_basis TEXT, rate_note TEXT,
  fit_role TEXT, fit_focus TEXT, fit_sim REAL,
  source TEXT, confidence TEXT, sort_order INTEGER, grid_club TEXT, grid_caveat TEXT, pos_only TEXT,
  UNIQUE(regime_id, player_id, slot_type)
);
CREATE TABLE team_tactic_setups(    -- v1 그대로 (team → regime_id)
  id INTEGER PRIMARY KEY,
  regime_id INTEGER REFERENCES regimes(id),
  season TEXT NOT NULL REFERENCES seasons(code),
  game_version TEXT NOT NULL,
  kind TEXT NOT NULL,
  formation TEXT, build_up_style TEXT, defensive_approach TEXT, line_height INTEGER,
  tactic_code TEXT, rationale TEXT, confidence TEXT, ingame_formation TEXT,
  UNIQUE(regime_id, season, game_version, kind)
);
CREATE TABLE transfer_targets(
  id INTEGER PRIMARY KEY,
  team_code TEXT NOT NULL REFERENCES teams(code),
  window TEXT NOT NULL,
  name TEXT NOT NULL, name_kr TEXT, short_label TEXT,
  player_id INTEGER REFERENCES players(id),   -- ⭐ 신설: players 승격 시 연결 (v1은 이름만)
  sofascore_id INTEGER, club TEXT, position TEXT,
  slot TEXT NOT NULL,
  likelihood TEXT, last_news_date TEXT,
  map25 TEXT, tool_x REAL, tool_y REAL, sample_n INTEGER, avg_rating REAL,
  opt_role TEXT, opt_focus TEXT, fit_role TEXT, fit_focus TEXT, fit_sim REAL,
  rationale TEXT, source TEXT, confidence TEXT,
  UNIQUE(team_code, window, name, slot)
);
CREATE TABLE transfer_outgoing(
  id INTEGER PRIMARY KEY,
  team_code TEXT NOT NULL REFERENCES teams(code),
  window TEXT NOT NULL,
  player_id INTEGER NOT NULL REFERENCES players(id),
  dest_club TEXT, likelihood TEXT, last_news_date TEXT,
  rationale TEXT, source TEXT, confidence TEXT,
  UNIQUE(team_code, window, player_id)
);
CREATE TABLE transfer_ledger(
  id INTEGER PRIMARY KEY,
  team_code TEXT NOT NULL REFERENCES teams(code),
  window TEXT NOT NULL, kind TEXT NOT NULL, label TEXT NOT NULL,
  amount_m REAL NOT NULL, note TEXT, source TEXT, confidence TEXT, contract_years REAL,
  UNIQUE(team_code, window, kind, label)
);
CREATE VIEW v_player_profile AS
SELECT player_id,
       COUNT(*) AS n,
       ROUND(AVG(rating),2) AS avg_rating,
       SUM(minutes) AS minutes,
       ROUND(AVG(xg),3) AS xg_pg, COUNT(xg) AS xg_n,
       ROUND(AVG(xa),3) AS xa_pg, COUNT(xa) AS xa_n,
       ROUND(AVG(key_passes),2) AS kp_pg, COUNT(key_passes) AS kp_n,
       ROUND(AVG(duels_won),2) AS dw_pg, COUNT(duels_won) AS dw_n,
       ROUND(AVG(tackles),2) AS tk_pg, COUNT(tackles) AS tk_n,
       ROUND(AVG(interceptions),2) AS ic_pg, COUNT(interceptions) AS ic_n
FROM player_matches GROUP BY player_id
/* v_player_profile(player_id,n,avg_rating,minutes,xg_pg,xg_n,xa_pg,xa_n,kp_pg,kp_n,dw_pg,dw_n,tk_pg,tk_n,ic_pg,ic_n) */;
CREATE TABLE _migration_log(
  run_at TEXT, v1_path TEXT, note TEXT
);
CREATE TABLE fbref_percentiles(
  id INTEGER PRIMARY KEY,
  player_id INTEGER NOT NULL REFERENCES players(id),
  pulled TEXT,                -- 수집일 YYYY-MM-DD
  pos_group TEXT,             -- FBref 비교 포지션군 원문 (예: 'Midfielders')
  period TEXT,                -- 비교 기간·모집단 원문 (예: 'Last 365 days, Big 5 Leagues')
  metric TEXT NOT NULL,       -- FBref 지표명 영문 원문
  metric_kr TEXT,
  per90 TEXT,                 -- 원값 문자열 그대로 (%·소수 혼재하므로 TEXT)
  percentile INTEGER,         -- 0~100
  source TEXT,
  UNIQUE(player_id, metric, period)
);
CREATE VIEW v_player_season_stats AS
SELECT player_id, season,
       CASE competition
         WHEN 'PL' THEN 'Premier League'
         WHEN 'EL' THEN 'UEFA Europa League'
         WHEN 'CL' THEN 'UEFA Champions League'
         WHEN 'FIFA World Cup' THEN 'World Cup'
         WHEN '' THEN '미분류'
         ELSE COALESCE(competition, '미분류')
       END AS competition,
       COUNT(*)        AS n,
       SUM(started)    AS starts,
       SUM(minutes)    AS minutes,
       SUM(goals)      AS goals,
       SUM(assists)    AS assists,
       ROUND(AVG(rating),2) AS avg_rating,
       COUNT(rating)   AS rating_n
FROM player_matches
GROUP BY player_id, season,
       CASE competition
         WHEN 'PL' THEN 'Premier League'
         WHEN 'EL' THEN 'UEFA Europa League'
         WHEN 'CL' THEN 'UEFA Champions League'
         WHEN 'FIFA World Cup' THEN 'World Cup'
         WHEN '' THEN '미분류'
         ELSE COALESCE(competition, '미분류')
       END
/* v_player_season_stats(player_id,season,competition,n,starts,minutes,goals,assists,avg_rating,rating_n) */;
CREATE TABLE fotmob_traits(
  id INTEGER PRIMARY KEY,
  player_id INTEGER NOT NULL REFERENCES players(id),
  pulled TEXT,                 -- 수집일
  pos_group TEXT,              -- 비교 모집단 원문 (예: 'Stats compared to other midfielders')
  metric TEXT NOT NULL,        -- Fotmob key (chances_created 등)
  metric_kr TEXT,
  percentile INTEGER,          -- 0~100 (원값 0~1 × 100)
  source TEXT,
  UNIQUE(player_id, metric)
);
CREATE TABLE fotmob_season_stats(
  id INTEGER PRIMARY KEY,
  player_id INTEGER NOT NULL REFERENCES players(id),
  pulled TEXT,
  league TEXT,                 -- 'Bundesliga 2025/2026'
  season TEXT,
  metric TEXT NOT NULL,        -- 라벨 원문 ('Goals','xG' 등)
  metric_kr TEXT,
  value TEXT,                  -- 원값 문자열 (%·소수 혼재)
  source TEXT,
  UNIQUE(player_id, league, season, metric)
);
CREATE TABLE fotmob_detail_stats(
  id INTEGER PRIMARY KEY,
  player_id INTEGER NOT NULL REFERENCES players(id),
  pulled TEXT, season TEXT, league TEXT,
  metric_key TEXT NOT NULL, metric TEXT, metric_kr TEXT,
  stat_value TEXT, per90 REAL,
  percentile INTEGER,          -- 같은 리그 동포지션 대비 백분위(합계 기준)
  percentile_per90 INTEGER,    -- 90분당 기준 백분위
  source TEXT,
  UNIQUE(player_id, season, league, metric_key));
CREATE TABLE slot_canon_roles(
  regime_id INTEGER NOT NULL REFERENCES regimes(id),
  formation TEXT NOT NULL,
  pos TEXT NOT NULL,                -- slots.pos와 동일 키
  game_version TEXT NOT NULL REFERENCES game_versions(code),
  role_id TEXT NOT NULL,
  focus TEXT NOT NULL,
  rationale TEXT,                   -- 어느 축·obs에서 왔는지
  source TEXT, confidence TEXT,
  updated TEXT,
  PRIMARY KEY(regime_id, formation, pos, game_version),
  FOREIGN KEY(regime_id, formation, pos) REFERENCES slots(regime_id, formation, pos),
  FOREIGN KEY(game_version, role_id) REFERENCES game_roles(game_version, role_id)
);
CREATE UNIQUE INDEX uq_squad_entries_regime_player_type
ON squad_entries(regime_id, player_id, slot_type);
CREATE TABLE match_reports(
  id INTEGER PRIMARY KEY,
  event_id INTEGER NOT NULL,
  match_id INTEGER REFERENCES matches(id),
  regime_id INTEGER NOT NULL REFERENCES regimes(id),
  team_code TEXT NOT NULL REFERENCES teams(code),
  season TEXT REFERENCES seasons(code),
  report_date TEXT NOT NULL,
  title TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'draft' CHECK(status IN ('draft','complete')),
  tactical_description TEXT NOT NULL,
  tactical_features TEXT NOT NULL,
  tactical_changes TEXT NOT NULL,
  game_implications TEXT NOT NULL,
  report_path TEXT NOT NULL,
  source TEXT NOT NULL,
  confidence TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL, overall_assessment TEXT,
  UNIQUE(team_code,event_id)
);
CREATE TABLE match_player_reports(
  report_id INTEGER NOT NULL REFERENCES match_reports(id) ON DELETE CASCADE,
  player_id INTEGER NOT NULL REFERENCES players(id),
  position TEXT NOT NULL,
  tactical_role TEXT NOT NULL,
  characteristics TEXT NOT NULL,
  performance TEXT NOT NULL,
  game_implication TEXT NOT NULL,
  source TEXT NOT NULL,
  confidence TEXT NOT NULL,
  PRIMARY KEY(report_id,player_id)
);
CREATE TABLE match_game_setups(
  report_id INTEGER PRIMARY KEY REFERENCES match_reports(id) ON DELETE CASCADE,
  game_version TEXT NOT NULL REFERENCES game_versions(code),
  formation TEXT NOT NULL,
  build_up_style TEXT NOT NULL,
  defensive_approach TEXT NOT NULL,
  line_height INTEGER NOT NULL CHECK(line_height BETWEEN 0 AND 100),
  tactic_code TEXT,
  match_only INTEGER NOT NULL DEFAULT 1 CHECK(match_only=1),
  rationale TEXT NOT NULL,
  source TEXT NOT NULL,
  confidence TEXT NOT NULL
, rule_note TEXT);
CREATE TABLE match_player_prescriptions(
  report_id INTEGER NOT NULL REFERENCES match_reports(id) ON DELETE CASCADE,
  player_id INTEGER NOT NULL REFERENCES players(id),
  game_version TEXT NOT NULL,
  pos_label TEXT NOT NULL,
  role_id TEXT NOT NULL,
  focus TEXT NOT NULL,
  fit_sim REAL,
  starter INTEGER NOT NULL DEFAULT 1,
  sort_order INTEGER,
  rationale TEXT NOT NULL,
  source TEXT NOT NULL,
  confidence TEXT NOT NULL, replaced_player_id INTEGER REFERENCES players(id), minute_on INTEGER,
  PRIMARY KEY(report_id,player_id),
  FOREIGN KEY(game_version,role_id,focus)
    REFERENCES game_role_focus(game_version,role_id,focus)
);
CREATE VIEW v_slot_candidates AS
SELECT
  r.id AS regime_id,
  r.team_code,
  sl.formation,
  sl.pos,
  sl.slot_type,
  se.player_id,
  COALESCE(se.label, p.name_kr, p.name) AS label,
  p.name AS name_en,
  COALESCE(p.name_kr, p.name) AS name_kr,
  'squad' AS source_kind,
  se.lh AS status,
  se.map25,
  se.rate_v AS rating,
  se.rate_basis,
  se.rate_note,
  se.fit_role,
  se.fit_focus,
  se.fit_sim,
  se.source,
  se.confidence,
  se.sort_order,
  se.grid_club,
  se.grid_caveat
FROM squad_entries se
JOIN regimes r ON r.id=se.regime_id
JOIN players p ON p.id=se.player_id
JOIN slots sl ON sl.regime_id=se.regime_id AND sl.slot_type=se.slot_type
-- pos_only: 좌우 쌍 슬롯(FB=LB/RB, CB=LCB/RCB, DM=LDM/RDM, WM=LM/RM)에서 한쪽만
-- 후보로 쓰고 싶을 때 그 pos를 적는다. NULL이면 종전대로 slot_type의 모든 pos에 노출된다.
WHERE (se.pos_only IS NULL OR se.pos_only = sl.pos)

UNION ALL

SELECT
  r.id AS regime_id,
  r.team_code,
  sl.formation,
  sl.pos,
  sl.slot_type,
  COALESCE(tt.player_id, tp.id) AS player_id,
  CASE WHEN tt.likelihood='CONFIRMED'
       THEN COALESCE(tt.short_label, tt.name_kr, tt.name)
       ELSE '영입·' || COALESCE(tt.short_label, tt.name_kr, tt.name) END AS label,
  tt.name AS name_en,
  COALESCE(tt.name_kr, tp.name_kr, tt.short_label, tt.name) AS name_kr,
  'transfer' AS source_kind,
  tt.likelihood AS status,
  tt.map25,
  tt.avg_rating AS rating,
  'transfer' AS rate_basis,
  '표본 ' || COALESCE(tt.sample_n, 0) || '경기 (' || COALESCE(tt.club, '') || ')' AS rate_note,
  tt.fit_role,
  tt.fit_focus,
  tt.fit_sim,
  tt.source,
  tt.confidence,
  10000 + tt.id AS sort_order,
  tt.club AS grid_club,
  CASE WHEN tt.map25 IS NOT NULL THEN '⚠️ 영입 전 현 소속팀 실측' END AS grid_caveat
FROM transfer_targets tt
JOIN regimes r ON r.team_code=tt.team_code AND r.end IS NULL
JOIN slots sl ON sl.regime_id=r.id AND sl.pos=(
  CASE tt.slot WHEN 'LW' THEN 'LM' WHEN 'RW' THEN 'RM' ELSE tt.slot END
)
LEFT JOIN players tp ON tp.id=tt.player_id OR (tt.player_id IS NULL AND tp.name=tt.name)
WHERE tt.map25 IS NOT NULL
  AND tt.likelihood!='OWNED'
  AND tt.likelihood NOT LIKE 'DEAD%'
  AND NOT EXISTS (
    SELECT 1
    FROM squad_entries se2
    WHERE se2.regime_id=r.id
      AND se2.player_id=COALESCE(tt.player_id, tp.id)
      AND se2.slot_type=sl.slot_type
  )
/* v_slot_candidates(regime_id,team_code,formation,pos,slot_type,player_id,label,name_en,name_kr,source_kind,status,map25,rating,rate_basis,rate_note,fit_role,fit_focus,fit_sim,source,confidence,sort_order,grid_club,grid_caveat) */;
CREATE TABLE player_market_values(
  id INTEGER PRIMARY KEY,
  player_id INTEGER NOT NULL REFERENCES players(id),
  val_date TEXT NOT NULL,        -- 평가 기준일 (FotMob/scisports 시계열의 date)
  value_eur INTEGER,             -- 중앙 추정값
  lower_eur INTEGER, upper_eur INTEGER,   -- scisports 신뢰구간
  team_name TEXT,                -- 그 시점 소속 (이적 시 값 점프의 원인을 남긴다)
  source TEXT,
  UNIQUE(player_id, val_date)
);
CREATE TABLE player_status(
  id INTEGER PRIMARY KEY,
  player_id INTEGER NOT NULL REFERENCES players(id),
  pulled TEXT NOT NULL,          -- 수집일 (스냅샷이므로 날짜가 정본이다)
  kind TEXT NOT NULL,            -- injury / contract_end
  value TEXT,                    -- injury: 부상명 · contract_end: YYYY-MM-DD
  detail TEXT,                   -- injury: 복귀 예상 표기 원문
  as_of TEXT,                    -- 소스가 밝힌 갱신일 (injuryInformation.lastUpdated)
  source TEXT, confidence TEXT,
  UNIQUE(player_id, pulled, kind)
);
CREATE TABLE understat_player_matches(
  id INTEGER PRIMARY KEY,
  player_id INTEGER NOT NULL REFERENCES players(id),
  us_match_id INTEGER NOT NULL,   -- Understat match id (경기 조인 키)
  season TEXT,                    -- 시작연도 표기 그대로 ('2025' = 25/26)
  match_date TEXT, h_team TEXT, a_team TEXT,
  position TEXT,                  -- Understat 표기 원문 (FW·AMC·Sub 등)
  minutes INTEGER,
  goals INTEGER, assists INTEGER, shots INTEGER, key_passes INTEGER,
  xg REAL, xa REAL, npxg REAL, xg_chain REAL, xg_buildup REAL,
  source TEXT,
  UNIQUE(player_id, us_match_id)
);
CREATE TABLE IF NOT EXISTS "player_evaluations"(
  id INTEGER PRIMARY KEY,
  regime_id INTEGER REFERENCES regimes(id),   -- NULL = 아직 우리 선수가 아니다(영입 후보). 불변규칙 7.
  player_id INTEGER NOT NULL REFERENCES players(id),
  overall TEXT NOT NULL,
  traits TEXT,
  strengths TEXT,
  stat_eval TEXT,
  fit_emery TEXT,
  fit_alonso TEXT,
  fit_iraola TEXT,
  source TEXT,
  confidence TEXT,
  updated TEXT, fotmob_eval TEXT, sample_season TEXT, sample_n INTEGER, sample_minutes INTEGER, sample_avg_rating REAL, sample_as_of TEXT,
  UNIQUE(regime_id, player_id)
);
CREATE TABLE player_shirt_numbers (
  id INTEGER PRIMARY KEY,
  player_id INTEGER NOT NULL REFERENCES players(id),
  team_code TEXT NOT NULL,
  season TEXT NOT NULL,
  shirt_number INTEGER,
  source TEXT,
  confidence TEXT,
  UNIQUE(player_id, team_code, season));
CREATE TABLE transfer_summary(
  team_code TEXT NOT NULL REFERENCES teams(code),
  window TEXT NOT NULL,
  summary TEXT NOT NULL,
  source TEXT NOT NULL,
  confidence TEXT NOT NULL,
  updated TEXT NOT NULL,
  PRIMARY KEY(team_code, window)
);
CREATE TABLE reproduction_limits(
  id INTEGER PRIMARY KEY,
  game_version TEXT NOT NULL REFERENCES game_versions(code),
  regime_id INTEGER REFERENCES regimes(id),       -- NULL = 전 체제 공통
  axis TEXT NOT NULL,                              -- manager_profiles.axis 어휘 (pressing/buildup/formation/…)
  real_feature TEXT NOT NULL,                      -- 실축에서 관측·요구되는 것
  limitation TEXT NOT NULL,                        -- 게임 설정 축에 왜 없는가
  workaround TEXT,                                 -- 근사 수단(있으면)
  source TEXT NOT NULL, confidence TEXT NOT NULL,
  added TEXT NOT NULL
);
CREATE TABLE ingame_captures(
  id INTEGER PRIMARY KEY,
  captured TEXT NOT NULL,                       -- YYYY-MM-DD
  game_version TEXT NOT NULL REFERENCES game_versions(code),
  regime_id INTEGER REFERENCES regimes(id),
  tactic_code TEXT,                             -- 그 경기에 쓴 FC 공유 코드(12자) — team_tactic_setups.tactic_code와 대조
  report_id INTEGER REFERENCES match_reports(id),  -- 경기 전용 프리셋을 재현한 경우
  player_id INTEGER REFERENCES players(id),
  image_path TEXT NOT NULL,
  attack_dir TEXT NOT NULL,                     -- up/down/left/right (스크린샷 안 공격 방향)
  box TEXT,                                     -- 피치 픽셀 상자 x0,y0,x1,y1
  cells TEXT NOT NULL,                          -- 25칸 가중치 CSV
  map25 TEXT NOT NULL,
  ref_kind TEXT,                                -- 'player:<id>:<kind>' | 'kernel:<role>/<focus>@x<n>'
  ref_map25 TEXT,
  cosine REAL,
  note TEXT, source TEXT NOT NULL, confidence TEXT NOT NULL
);
CREATE VIEW v_ingame_capture_norm AS
WITH c AS (
  SELECT id, tactic_code, player_id, game_version, ref_kind, cosine, note, cells,
         (note LIKE '%조작 오염%') AS controlled,
         -- 자기진영 = 25칸 중 16~25번째(행3·행4) 가중치 합 / 전체
         (SELECT SUM(CAST(value AS REAL)) FROM (
            SELECT value, row_number() OVER () rn FROM json_each('[' || cells || ']')) WHERE rn > 15)
         / (SELECT SUM(CAST(value AS REAL)) FROM json_each('[' || cells || ']')) * 100.0 AS own_pct
  FROM ingame_captures),
m AS (
  SELECT tactic_code, AVG(own_pct) AS team_mean_own, COUNT(*) AS n_players
  FROM c WHERE controlled = 0 AND ref_kind NOT LIKE 'kernel:gk_%' GROUP BY tactic_code)
SELECT c.id, c.tactic_code, c.player_id, c.game_version, c.ref_kind, c.cosine, c.controlled,
       ROUND(c.own_pct, 1) AS own_pct, ROUND(m.team_mean_own, 1) AS team_mean_own,
       ROUND(c.own_pct - m.team_mean_own, 1) AS own_delta, m.n_players
FROM c JOIN m ON m.tactic_code = c.tactic_code
/* v_ingame_capture_norm(id,tactic_code,player_id,game_version,ref_kind,cosine,controlled,own_pct,team_mean_own,own_delta,n_players) */;
CREATE VIEW v_kernel_fidelity AS
SELECT game_version,
       substr(ref_kind, 8, instr(ref_kind, '/') - 8)                          AS role_id,
       substr(ref_kind, instr(ref_kind, '/') + 1,
              instr(ref_kind, '@') - instr(ref_kind, '/') - 1)                AS focus,
       COUNT(*) AS n, COUNT(DISTINCT tactic_code) AS n_matches, COUNT(DISTINCT player_id) AS n_players,
       ROUND(AVG(cosine), 2) AS cos_avg, ROUND(MIN(cosine), 2) AS cos_min, ROUND(MAX(cosine), 2) AS cos_max,
       CASE WHEN COUNT(*) >= 3 AND AVG(cosine) >= 0.6 THEN 'HIGH'
            WHEN COUNT(*) >= 3 AND AVG(cosine) >= 0.45 THEN 'MID'
            WHEN COUNT(*) >= 3 THEN 'LOW'
            ELSE 'n<3' END AS fidelity
FROM ingame_captures
WHERE ref_kind LIKE 'kernel:%' AND note NOT LIKE '%조작 오염%'
GROUP BY game_version, role_id, focus
/* v_kernel_fidelity(game_version,role_id,focus,n,n_matches,n_players,cos_avg,cos_min,cos_max,fidelity) */;
CREATE TABLE player_card_items(
  id INTEGER PRIMARY KEY,
  game_version TEXT NOT NULL REFERENCES game_versions(code),
  ea_item_id INTEGER NOT NULL,      -- fut.gg eaId. 프로모 카드는 base와 다른 id를 받는다
  base_ea_id INTEGER,               -- 그 선수의 base eaId (= player_game_stats 카드 URL의 27-{id})
  is_base INTEGER NOT NULL DEFAULT 0,
  player_id INTEGER REFERENCES players(id),
  name_kr TEXT NOT NULL,            -- 표시용 (조인 금지 — 사람 조인은 player_id)
  rarity_ea_id INTEGER, rarity_name TEXT,     -- 'Rare' / 'Team of the Week' / …
  released_at TEXT,                 -- 아이템 createdAt(EA 공개일) — 시점 축
  club TEXT, positions TEXT, best_pos TEXT,
  ovr INTEGER, pac INTEGER, sho INTEGER, pas INTEGER, dri INTEGER, def INTEGER, phy INTEGER,
  attrs TEXT, playstyles TEXT,      -- attrs는 한글 라벨 JSON(다른 표와 같은 키), playstyles는 '…, …+' 문자열
  roles_plus TEXT, roles_plus_plus TEXT,      -- ⛔ FC27 역할 id는 카탈로그 미공개라 **raw id 목록**으로 둔다
  skill_moves INTEGER, weak_foot INTEGER, accelerate TEXT, preferred_foot TEXT,
  card_image_url TEXT, futgg_url TEXT,
  source TEXT, confidence TEXT,
  UNIQUE(game_version, ea_item_id)
);
CREATE INDEX ix_card_items_player ON player_card_items(player_id, game_version);
CREATE TABLE match_videos(
  id INTEGER PRIMARY KEY,
  video_id TEXT NOT NULL,           -- 유튜브 id (전사 파일명의 앞부분)
  lang TEXT,                        -- 전사 언어 (en/es/pt/…)
  report_id INTEGER REFERENCES match_reports(id) ON DELETE SET NULL,  -- 경기 귀속(없으면 NULL = 시즌·선수 축)
  regime_id INTEGER REFERENCES regimes(id),   -- 팀 축 필터용 (불변규칙 6 — 팀은 team_code/regime로 조인)
  team_code TEXT REFERENCES teams(code),
  channel TEXT NOT NULL,            -- 채널명 (UTV | Aston Villa Fan Channel · The Villans · 1874 …)
  title TEXT,                       -- 영상 제목
  published TEXT,                   -- 게시일. '경' 접미가 붙은 추정치는 published_approx=1
  published_approx INTEGER NOT NULL DEFAULT 0,
  url TEXT,
  transcript_path TEXT,             -- reports/transcripts/{id}.{lang}.md
  kind TEXT,                        -- 경기반응 / 전술분석 / 선수스카우팅 / 감독회견 / 상대팀 / 프리시즌
  summary TEXT,                     -- ⑶ 사람이 쓴 핵심 요약 (NULL = 아직 안 씀)
  key_points TEXT,                  -- ⑶ 줄바꿈 구분 핵심 포인트
  obs_refs TEXT,                    -- ⑵ 이 전사를 인용한 observations id 목록(CSV) — 자동 산출
  source TEXT, confidence TEXT,
  UNIQUE(video_id, lang)
);
CREATE INDEX ix_match_videos_report ON match_videos(report_id);
CREATE INDEX ix_match_videos_team ON match_videos(team_code, published);
CREATE TABLE video_impl_claims(
  id INTEGER PRIMARY KEY,
  video_id TEXT NOT NULL,           -- match_videos.video_id (lang은 묶지 않는다 — 주장은 언어와 무관)
  axis TEXT NOT NULL,               -- role / focus / team_axis / instruction / limit / none
  player_id INTEGER REFERENCES players(id),
  team_code TEXT REFERENCES teams(code),
  role_id TEXT,                     -- 우리 역할 어휘(kernel role_group의 키) — ⛔ 자유 문자열 금지
  focus TEXT,                       -- Attack / Support / Balanced / Build-Up / Roaming / Ball-Winning / Aggressive …
  field TEXT,                       -- team_axis·instruction·limit에서 무엇을 건드리는가
  value TEXT,                       -- 그 필드의 주장값
  quote TEXT,                       -- ⭐ 전사 원문 인용(불변규칙 11 — 한국어 번역 병기)
  verdict TEXT NOT NULL,            -- APPLIED / HELD / REJECTED / PENDING / NA
  verdict_note TEXT,                -- ⛔ HELD·REJECTED는 사유·재판정 조건 필수(G17)
  source TEXT, confidence TEXT,
  added TEXT NOT NULL DEFAULT (date('now'))
);
CREATE INDEX ix_vic_video ON video_impl_claims(video_id);
CREATE INDEX ix_vic_axis ON video_impl_claims(axis, verdict);
CREATE INDEX ix_vic_player ON video_impl_claims(player_id);
CREATE TABLE player_evolutions(
  id INTEGER PRIMARY KEY,
  game_version TEXT NOT NULL REFERENCES game_versions(code),
  player_id INTEGER REFERENCES players(id),
  base_ea_id INTEGER NOT NULL,      -- 진화 대상 base 카드(= player_card_items.base_ea_id)
  name_kr TEXT NOT NULL,            -- 표시용 (조인 금지)
  path_key TEXT NOT NULL,           -- 이 경로를 식별하는 evolution id 사슬 '2499' / '2488>2491'
  evolution_ids TEXT NOT NULL,      -- JSON 배열
  evolution_names TEXT NOT NULL,    -- ' → '로 이은 단계 이름
  evolution_urls TEXT,              -- fut.gg 경로 URL(들), 줄바꿈 구분
  steps INTEGER NOT NULL,           -- 단계 수
  coins_cost INTEGER, points_cost INTEGER,
  training_time INTEGER,            -- 초
  is_expired INTEGER NOT NULL DEFAULT 0,
  ovr_before INTEGER, ovr_after INTEGER,
  upgrades TEXT,                    -- 속성 델타 JSON(한글 라벨 — 다른 표와 같은 키)
  six_before TEXT, six_after TEXT,  -- 6대 스탯 JSON(PAC/SHO/PAS/DRI/DEF/PHY, GK는 DIV/HAN/KIC/REF/SPD/POS)
  playstyles_after TEXT,            -- 결과 카드 PlayStyles ('…, …+')
  roles_plus_after TEXT,            -- ⭐ 결과 카드 Role+ raw id JSON (roles 카탈로그 plusEaId로 해석)
  roles_plus_plus_after TEXT,       -- ⭐ 결과 카드 Role++ raw id JSON (plusPlusEaId로 해석)
  source TEXT, confidence TEXT,
  pulled TEXT NOT NULL, path_json TEXT, path_choices TEXT,             -- 수집일 — 진화는 기간제라 시점이 정본이다
  UNIQUE(game_version, base_ea_id, path_key, pulled)
);
CREATE INDEX ix_player_evolutions_player ON player_evolutions(player_id, game_version);
CREATE TABLE fc_role_familiarity_map(
  game_version TEXT NOT NULL REFERENCES game_versions(code),
  ea_id INTEGER NOT NULL,           -- plusEaId 또는 plusPlusEaId
  kind TEXT NOT NULL CHECK(kind IN ('plus','plusplus')),
  slug TEXT NOT NULL,               -- 'cm-box-to-box'
  name TEXT NOT NULL,               -- 'Box-To-Box'
  position_name TEXT,               -- 'CM'
  source TEXT, confidence TEXT, pulled TEXT NOT NULL,
  PRIMARY KEY(game_version, ea_id, kind)
);
CREATE TABLE fc_evolutions(
  id INTEGER PRIMARY KEY,
  game_version TEXT NOT NULL REFERENCES game_versions(code),
  evo_id INTEGER NOT NULL,              -- fut.gg evolution id (= 034 path_key의 구성 요소)
  name TEXT NOT NULL,
  slug TEXT, url TEXT, description TEXT,
  category TEXT,                        -- categoryName (없으면 NULL)
  unlock_text TEXT,                     -- customUnlockable / sbcName / objectiveGroupName 중 있는 것
  coins_cost INTEGER, points_cost INTEGER, token_cost INTEGER,
  repeatability INTEGER,                -- repeatabilityCount (1=1회, n=반복 가능 횟수)
  is_reward INTEGER NOT NULL DEFAULT 0, -- isRewardEvolution (시즌패스·목표 보상)
  is_gk INTEGER NOT NULL DEFAULT 0,
  is_timed INTEGER NOT NULL DEFAULT 0,
  training_time INTEGER,                -- 초 (훈련 캠프형)
  created_at TEXT, end_time TEXT, end_submission_time TEXT,
  requirements_text TEXT,               -- JSON [{label,value}] — 사람이 읽는 요구조건
  total_upgrades_text TEXT,             -- JSON [{label,value,maxValue}]
  levels TEXT,                          -- JSON 단계별 upgrades·challenges·upgradeOptions (선택형은 options로 갈린다)
  allowed_prior_ids TEXT,               -- JSON — 이 진화 전에 거쳐야/거칠 수 있는 진화 id
  number_of_players INTEGER,            -- fut.gg 집계 적용 가능 선수 수(전체 DB 기준)
  is_expired INTEGER NOT NULL DEFAULT 0,
  source TEXT, confidence TEXT,
  pulled TEXT NOT NULL,                 -- 진화는 기간제 — 시점이 정본
  UNIQUE(game_version, evo_id, pulled)
);
CREATE INDEX ix_fc_evolutions_gv ON fc_evolutions(game_version, is_expired, end_time);
CREATE TABLE fut_accounts(
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL UNIQUE,            -- 표시명 (예: 'main-ps5')
  platform TEXT,                        -- PS / Xbox / PC
  game_version TEXT NOT NULL REFERENCES game_versions(code),
  notes TEXT,
  created TEXT NOT NULL
);
CREATE TABLE fut_club_players(
  id INTEGER PRIMARY KEY,
  account_id INTEGER NOT NULL REFERENCES fut_accounts(id),
  player_id INTEGER REFERENCES players(id),   -- 우리 DB 선수면 연결(조인 규칙: player_id)
  ea_item_id INTEGER,                         -- 보유 아이템(카드) id — player_card_items.ea_item_id
  name TEXT NOT NULL,                         -- 표시용
  acquired TEXT, acquired_how TEXT,           -- 입수일·경로(팩/이적시장/보상/SBC)
  status TEXT NOT NULL DEFAULT 'owned' CHECK(status IN ('owned','sold','discarded')),
  current_ovr INTEGER, current_six TEXT,      -- 마지막 기록 시점 상태(진화 적용 후 갱신)
  current_playstyles TEXT, current_roles_plus TEXT, current_roles_plus_plus TEXT,
  evo_count INTEGER NOT NULL DEFAULT 0,       -- 적용한 진화 단계 수(로그와 일치해야 한다)
  notes TEXT,
  updated TEXT NOT NULL,
  UNIQUE(account_id, ea_item_id)
);
CREATE TABLE fut_evolution_log(
  id INTEGER PRIMARY KEY,
  club_player_id INTEGER NOT NULL REFERENCES fut_club_players(id),
  evo_id INTEGER NOT NULL, evo_name TEXT NOT NULL,
  level INTEGER,                              -- 다단계 진화의 단계(1부터)
  applied_at TEXT NOT NULL, completed_at TEXT,
  ovr_before INTEGER, ovr_after INTEGER,
  six_before TEXT, six_after TEXT,            -- JSON
  attrs_delta TEXT,                           -- JSON {한글 라벨: +n}
  playstyles_after TEXT, roles_plus_after TEXT, roles_plus_plus_after TEXT,
  source TEXT, confidence TEXT, notes TEXT
);
CREATE INDEX ix_fut_evolution_log_cp ON fut_evolution_log(club_player_id, applied_at);
CREATE TABLE player_card_prices(
  id INTEGER PRIMARY KEY,
  game_version TEXT NOT NULL REFERENCES game_versions(code),
  ea_item_id INTEGER NOT NULL,          -- player_card_items.ea_item_id
  player_id INTEGER REFERENCES players(id),
  price INTEGER,                        -- 코인. NULL = 시세 미형성(hasPrice=0)
  has_price INTEGER NOT NULL DEFAULT 0,
  momentum REAL,                        -- fut.gg momentumPercentage (추세)
  platform TEXT NOT NULL DEFAULT 'console',   -- fut.gg 기본 표시 플랫폼
  source TEXT, confidence TEXT,
  pulled TEXT NOT NULL,
  UNIQUE(game_version, ea_item_id, platform, pulled)
);
CREATE INDEX ix_player_card_prices_item ON player_card_prices(game_version, ea_item_id, pulled);
CREATE TABLE game_role_key_attrs(
  id INTEGER PRIMARY KEY,
  game_version TEXT NOT NULL REFERENCES game_versions(code),
  role_id TEXT NOT NULL,
  attr TEXT NOT NULL,
  weight INTEGER NOT NULL CHECK(weight BETWEEN 1 AND 3),
  source TEXT NOT NULL DEFAULT 'docs/20·22 역할 설명 기반 판단 (2026-09-18)',
  confidence TEXT NOT NULL DEFAULT 'MEDIUM — EA 미공개, 역할 서술에서 판단한 가중',
  UNIQUE(game_version, role_id, attr)
);
CREATE TABLE tactic_change_log(
  id INTEGER PRIMARY KEY,
  regime_id INTEGER NOT NULL REFERENCES regimes(id),
  layer TEXT NOT NULL CHECK(layer IN ('slot_canon','team_setup','starter')),
  key TEXT NOT NULL,                 -- slot_canon: 'formation|pos' · team_setup: 'season|kind' · starter: 'pos_label'
  before TEXT,                       -- NULL = 신설
  after TEXT,                        -- NULL = 삭제
  changed_at TEXT NOT NULL,          -- 날짜(YYYY-MM-DD)
  reason TEXT NOT NULL,              -- 왜 바뀌었나 — obs# 참조 권장
  source TEXT NOT NULL               -- 'git:<hash>' (backfill) 또는 'tactic_changes.py <날짜>'
);
CREATE INDEX ix_tactic_change_log_r ON tactic_change_log(regime_id, changed_at);
CREATE TABLE match_events(
  id INTEGER PRIMARY KEY,
  match_id INTEGER NOT NULL REFERENCES matches(id),
  minute INTEGER NOT NULL,             -- 90+3 은 93
  added INTEGER,                       -- 추가시간 표기용(3) — minute은 합산값
  side TEXT NOT NULL CHECK(side IN ('v','o')),   -- v=우리 팀(matches.team_code) · o=상대
  kind TEXT NOT NULL CHECK(kind IN ('goal','own_goal','penalty_goal','penalty_miss','sub','yellow','red','gk_change','var')),
  player_id INTEGER REFERENCES players(id),
  player_name TEXT,                    -- 상대 선수 등 미등록자 표시용
  assist_player_id INTEGER REFERENCES players(id),
  assist_name TEXT,
  player_out_id INTEGER REFERENCES players(id),  -- sub: 나간 선수
  player_out_name TEXT,
  score_v INTEGER, score_o INTEGER,    -- 이 이벤트 직후 스코어(득점류만)
  note TEXT,
  source TEXT NOT NULL, confidence TEXT
);
CREATE INDEX ix_match_events_m ON match_events(match_id, minute);
CREATE TABLE match_period_stats(
  id INTEGER PRIMARY KEY,
  match_id INTEGER NOT NULL REFERENCES matches(id),
  period TEXT NOT NULL CHECK(period IN ('1H','2H','ET')),
  possession_v REAL, xg_v REAL, xg_o REAL, shots_v INTEGER, shots_o INTEGER, sot_v INTEGER, sot_o INTEGER,
  ppda_v REAL, ppda_o REAL,
  source TEXT NOT NULL, confidence TEXT,
  UNIQUE(match_id, period)
);
