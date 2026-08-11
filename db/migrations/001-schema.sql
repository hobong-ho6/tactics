-- ============================================================================
-- tactics.db 스키마 v2 (2026-08-11 재설계)
--
-- 설계 원칙 (v1 운영에서 실증된 교훈의 성문화):
--  1. 축 3개가 1급 엔티티다 — 감독·팀 페어(regimes), 게임 버전(game_versions),
--     선수 정체성(players: 외부 식별자를 컬럼으로).
--  2. 팀 참조는 어디서나 team_code(TEXT, regimes/teams 코드)다.
--     v1의 matches 풀네임 함정(WHERE team='AVL' → 조용히 0행)을 제거한다.
--  3. 문자열 라벨 조인 금지 — 사람 참조는 player_id FK로만.
--  4. 정형 값(평점·표본수·적합값)은 컬럼이다. 산문(rationale)은 근거 서술 전용.
--  5. 사실(실세계 관측)과 판단(매핑·처방)은 레이어가 다르다 — 사실 테이블은
--     team_code+date로 자명하고, 판단 테이블은 regime_id를 명시한다.
-- ============================================================================

PRAGMA foreign_keys = ON;

-- ── 축(axes) ────────────────────────────────────────────────────────────────

CREATE TABLE game_versions(
  code TEXT PRIMARY KEY,            -- 'FC26', 'FC27'
  released TEXT,                    -- 발매일 (YYYY-MM-DD, 예정이면 NULL)
  notes TEXT
);

CREATE TABLE teams(
  code TEXT PRIMARY KEY,            -- 'AVL' / 'CHE' / 'LIV'
  name TEXT NOT NULL,               -- 정규 영문 표기 (SofaScore 표기 기준)
  name_kr TEXT,
  sofascore_id INTEGER,             -- 팀 페이지/rumours teamIds
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
);

CREATE TABLE player_tenures(
  player_id INTEGER NOT NULL REFERENCES players(id),
  season TEXT NOT NULL REFERENCES seasons(code),
  club_code TEXT,                   -- teams.code 또는 외부 클럽명 그대로 (외부는 코드 없음)
  club_name TEXT,                   -- 표시용
  position TEXT, shirt_no INTEGER, minutes INTEGER,
  PRIMARY KEY(player_id, season)
);

-- ── 실세계 레이어 (사실 — 관측치) ──────────────────────────────────────────

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

-- ⭐ v1의 appearances + player_match_grids + player_match_positions 3테이블 통합.
--    한 행 = (선수, 경기). SofaScore event_id가 기본 키이지만, event_id를 모르는
--    v1 appearances 잔여분은 match_id로만 연결된다(둘 다 NULL은 불가).
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
  source TEXT, confidence TEXT,
  PRIMARY KEY(event_id, team_code)
);

CREATE TABLE player_shot_profile(   -- v1 그대로
  player_id INTEGER PRIMARY KEY REFERENCES players(id),
  window TEXT, events_n INTEGER, shots INTEGER, xg_sum REAL,
  box_n INTEGER, sixyard_n INTEGER, headers INTEGER, goals INTEGER,
  mean_dist REAL, mean_y REAL,
  source TEXT, confidence TEXT
);

CREATE TABLE streaks(
  id INTEGER PRIMARY KEY, label TEXT UNIQUE, note TEXT,
  season TEXT, team_code TEXT REFERENCES teams(code)
);
CREATE TABLE match_streak(
  match_id INTEGER REFERENCES matches(id),
  streak_id INTEGER REFERENCES streaks(id),
  UNIQUE(match_id, streak_id)
);

-- ── 지식 레이어 (관찰·판단의 기록) ─────────────────────────────────────────

-- obs 번호(id)는 v1에서 그대로 승계된다 — 141개 상호참조(obs#NNN)가 살아있는 주소다.
CREATE TABLE observations(
  id INTEGER PRIMARY KEY,
  regime_id INTEGER REFERENCES regimes(id),
  season TEXT REFERENCES seasons(code),
  scope TEXT NOT NULL,              -- philosophy/build_up/defence/in_possession/modulation/verdict/reference
  claim TEXT NOT NULL,
  evidence TEXT, source TEXT, confidence TEXT
);

-- 감독 분석의 정형화 — docs/1x 산문의 구조화 사본이 아니라, "현재 확정된 결론"의 슬롯.
-- axis 어휘(11): philosophy / traits / role_demands / formation / situational /
--   pressing / buildup / rest_defense / set_pieces / rotation / market
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
  source TEXT, confidence TEXT,
  UNIQUE(season, player_id, position)
);

-- ── 게임 레이어 (FC 버전별) ─────────────────────────────────────────────────

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

-- ⭐ 로스터 스냅샷 이력 — v1 UNIQUE(game_version,name_kr)는 이력을 덮어썼다.
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
  detail_date TEXT, source TEXT, confidence TEXT,
  UNIQUE(game_version, roster_date, name_kr)
);

-- ⭐ 신설 — FIFA→FC 시스템 변천 관찰 로그 (재설계 요구사항: 시리즈 변화 추적)
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

-- ── 매핑 레이어 (판단 — 분석의 산출물) ──────────────────────────────────────

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

-- v1 player_role_map의 승계. kind 어휘는 그대로(measured / measured:<class> /
-- @dom/@tight / optimal / projected / role / match:<tag>).
-- ⭐ 정형 필드 추가: sample_n / avg_rating / fit_sim — v1에서 rationale 산문에 갇혀
--    정규식으로 긁어야 했던 값들.
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
  rationale TEXT,                   -- 근거 서술 전용 (값은 위 컬럼으로)
  UNIQUE(player_id, regime_id, season, game_version, kind)
);

-- v1 squad_positions의 승계 — label 문자열 조인 폐지, player_id FK.
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
  source TEXT, confidence TEXT, sort_order INTEGER,
  UNIQUE(regime_id, player_id, slot_type)
);

CREATE TABLE team_tactic_setups(    -- v1 그대로 (team → regime_id)
  id INTEGER PRIMARY KEY,
  regime_id INTEGER REFERENCES regimes(id),
  season TEXT NOT NULL REFERENCES seasons(code),
  game_version TEXT NOT NULL,
  kind TEXT NOT NULL,
  formation TEXT, build_up_style TEXT, defensive_approach TEXT, line_height INTEGER,
  tactic_code TEXT, rationale TEXT, confidence TEXT,
  UNIQUE(regime_id, season, game_version, kind)
);

-- ── 이적 레이어 (transfer-watch — v1 파이프라인 그대로) ─────────────────────

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
  amount_m REAL NOT NULL, note TEXT, source TEXT, confidence TEXT,
  UNIQUE(team_code, window, kind, label)
);

-- ── 뷰 ──────────────────────────────────────────────────────────────────────

-- 선수별 이벤트 스탯 프로필 (v1 v_event_profile 승계).
-- ⚠️ n은 경기 수다 — 지표별 표본 수가 아니다. 지표별 COUNT 컬럼을 반드시 볼 것 (obs#132).
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
FROM player_matches GROUP BY player_id;

-- 마이그레이션 메타 (재실행 이력)
CREATE TABLE _migration_log(
  run_at TEXT, v1_path TEXT, note TEXT
);
