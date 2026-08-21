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
  source TEXT, confidence TEXT,
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
  source TEXT, confidence TEXT, ppda_v REAL, ppda_o REAL, ppda_num_v INTEGER, ppda_den_v INTEGER, ppda_num_o INTEGER, ppda_den_o INTEGER, ppda_method TEXT, aerial_won_v INTEGER, aerial_att_v INTEGER, aerial_won_o INTEGER, aerial_att_o INTEGER, dribble_succ_v INTEGER, dribble_att_v INTEGER, dribble_succ_o INTEGER, dribble_att_o INTEGER, tackles_v INTEGER, tackles_o INTEGER, interceptions_v INTEGER, interceptions_o INTEGER, clearances_v INTEGER, clearances_o INTEGER,
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
  source TEXT, confidence TEXT, observed_from TEXT, observed_to TEXT, sample_scope TEXT, sample_note TEXT,
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
  kernel25 TEXT, kernel_source TEXT,
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
  detail_date TEXT, source TEXT, confidence TEXT, nationality TEXT, full_name TEXT,
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
  updated TEXT, fotmob_eval TEXT,
  UNIQUE(regime_id, player_id)
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
  updated_at TEXT NOT NULL,
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
);
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
