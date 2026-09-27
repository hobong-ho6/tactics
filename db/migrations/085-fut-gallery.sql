-- 085 FUT 갤러리 — 세트 정의와 등급별 최저 비용 조합 (2026-09-27)
--
-- 왜 (사용자 「https://www.fut.gg/fut-gallery/ 에 갤러리 관련 메뉴가 있는데 이건 api가 없다는 거지?」):
--   ⛔⛔ **내가 「없다」고 단정한 것이 틀렸다.** `/api/gg-club/gallery/`(구단 하위)만 찔러 보고
--      「fut.gg는 갤러리를 주지 않는다」고 보고했는데, 실제 경로는 **`/api/fut/gallery/fc27/hub/`**이고
--      **인증 없이 200**이다. ⇒ 「없다」는 결론은 **찔러 본 범위 안에서만** 유효하다. 범위를 밝히지 않고
--      단정하면 있는 것을 없다고 말하게 된다.
--
-- 무엇인가: 세트를 채우면 **갤러리 토큰**이 나오고 그걸로 Hall of FUT 선수를 해금한다(최대 1,649 토큰).
--   ⭐ 수집 인정은 **보유가 아니라 「거쳐 갔는가」**다 — 팩에서 깠거나 샀다가 팔아도 인정된다(fut.gg 설명).
--
-- ⛔⛔ **내 수집 현황은 받을 수 없다.** 개인 진행도 경로는 전부 404다
--    (`gallery/fc27/progress|my|collected`, `gg-club/gallery|fut-gallery|collection`).
--    ⚠️ 우리 원장으로 근사하면 **과소 집계**가 된다 — EA가 인정하는 범위는 **계정 전체 이력**인데
--       `fut_club_players`는 2026-09-17부터라 그 전에 거쳐 간 카드를 모른다. 화면은 그 사실을 적는다.
CREATE TABLE fc_gallery_sets(
  game_version  TEXT NOT NULL,
  set_id        INTEGER NOT NULL,
  category_id   INTEGER, category_name TEXT,
  name          TEXT, slug TEXT, description TEXT,
  required_cards INTEGER,          -- 예: 아스널 20장
  total_tokens  INTEGER,           -- 그 세트가 줄 수 있는 토큰 총량
  club_ea_id    INTEGER, league_ea_id INTEGER, rarity_ea_id INTEGER,
  start_time    TEXT,
  grades_json   TEXT,              -- [{name:'D',threshold:10}, …] — 등급 임계(점수)
  pulled        TEXT NOT NULL,
  source TEXT, confidence TEXT,
  PRIMARY KEY(game_version, set_id, pulled)
);
-- ⭐ fut.gg가 계산해 주는 **등급별 최저 비용 조합**. 시세라 **금방 낡는다** — 날짜별 스냅샷으로 쌓는다.
-- ⛔ 이 조합은 **시장 최저가 기준**이고 내가 이미 가진 카드를 빼지 않는다. 화면이 그 사실을 적는다.
CREATE TABLE fc_gallery_tiers(
  game_version TEXT NOT NULL,
  set_id       INTEGER NOT NULL,
  grade        TEXT NOT NULL,      -- D·C·B·A·S
  threshold    INTEGER,            -- 그 등급에 필요한 점수
  tokens       INTEGER,            -- 그 등급에서 받는 토큰
  cost         INTEGER,            -- 조합 총 코인 (⚠️ 시세라 회차마다 바뀐다)
  peak_price   INTEGER,            -- 조합에서 가장 비싼 카드
  total_score  INTEGER,
  items_json   TEXT,               -- [{eaId, price}, …]
  pulled       TEXT NOT NULL,
  source TEXT, confidence TEXT,
  PRIMARY KEY(game_version, set_id, grade, pulled)
);
CREATE INDEX ix_fc_gallery_sets_pulled ON fc_gallery_sets(pulled);
CREATE INDEX ix_fc_gallery_tiers_pulled ON fc_gallery_tiers(pulled);
