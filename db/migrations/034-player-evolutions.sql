-- 034 — player_evolutions: FC 진화(Evolutions) 경로와 그 결과 카드 (2026-09-17, 사용자 지시
--       「어떻게 진화하면 좋을지도 수집해서 페이지 내에서 최적의 제안을 보여줘」).
--
-- 왜 별도 표인가: `player_card_items`는 **이미 발매된 아이템**이고, 진화는 **내가 적용하면 생기는 가상의 결과**다.
-- 둘을 한 표에 섞으면 「발매된 카드」와 「만들 수 있는 카드」가 구분되지 않는다(불변규칙 2의 정신 — 층을 섞지 않는다).
--
-- 원천: fut.gg `/api/fut/evolutions/v2/{game}/paths/v2/{basePlayerEaId}/`
--   ⚠️ **base eaId만 받는다** — 특별 카드 id를 넣으면 404다(2026-09-17 실증: 이강인 OTW 50575428 → "Not found").
--   한 응답이 경로 후보 여럿을 주고, 각 후보는 `evolutions`(단계 목록)·`path`(단계별 결과 카드)·`upgrades`(속성 델타)를 담는다.
--
-- ⛔ **추천 순위를 여기서 굳히지 않는다.** 이 표는 사실(경로·비용·델타)만 담고, 「최적」 판정은 화면이
--    그 선수의 처방 역할과 대조해 만든다 — 처방이 바뀌면 추천도 바뀌어야 하기 때문이다.
PRAGMA foreign_keys = ON;
BEGIN;
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
  pulled TEXT NOT NULL,             -- 수집일 — 진화는 기간제라 시점이 정본이다
  UNIQUE(game_version, base_ea_id, path_key, pulled)
);
CREATE INDEX ix_player_evolutions_player ON player_evolutions(player_id, game_version);
COMMIT;
