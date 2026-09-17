-- 036 — 진화 카탈로그 + 내 얼티밋 구단 원장 (2026-09-17, 사용자 지시
--       「진화 메뉴를 아예 신설… 내 얼티밋 계정에서 내 구단의 선수들이 어떻게 진화를 적용하고 발전해가는지 기록」).
--
-- 층이 셋이다 — 섞지 않는다(불변규칙 2의 정신):
--   ⑴ fc_evolutions        : EA가 연 **진화 자체**(요구조건·단계별 업그레이드·마감·해금 경로). 선수와 무관한 카탈로그.
--   ⑵ player_evolutions    : 우리 관리 선수 × 진화 = **가능한 경로와 결과**(034). 여기에 단계별 결과 카드 path_json을 더한다.
--   ⑶ fut_*                : **내 계정이 실제로 한 일** — 보유 선수, 적용한 진화, 그때의 스탯 변화. 사실 기록이며 재계산하지 않는다.
--
-- 원천: ⑴⑵ fut.gg `/api/fut/evolutions/v2/{game}/paths/v2/{basePlayerEaId}/` 응답에 진화 객체가 통째로 박혀 있다
--   (requirementsText·levels·endTime·customUnlockable·sbcName…). 별도 카탈로그 API는 404다(2026-09-17 탐색 8경로 전부).
--   ⑶ 사용자 입력(scripts/fut_club.py). ⛔ EA 구단 자동 수집은 **FC Community API 승인 파트너 전용**이라 우리는 못 쓴다 —
--   fut.gg GG Club이 그 경로다. 사용자가 거기 연결하면 그 세션을 읽는 임포터를 붙일 수 있다(별도 작업).
--
-- ⛔ 「누구에게 적용하면 좋은가」는 여기 없다 — 화면이 처방 역할과 대조해 만든다(034와 같은 원칙).
PRAGMA foreign_keys = ON;
BEGIN;

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

-- 034 보강: 단계별 결과 카드(적용했을 때 무엇이 되는지) + 선택형 분기
ALTER TABLE player_evolutions ADD COLUMN path_json TEXT;     -- JSON [{step, evo_id, ovr, six, position, playstyles, roles_plus, roles_plus_plus, card_image_url}]
ALTER TABLE player_evolutions ADD COLUMN path_choices TEXT;  -- JSON evolutionPathChoices (선택형 업그레이드 인덱스)

-- ⑶ 내 계정 원장
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

COMMIT;
