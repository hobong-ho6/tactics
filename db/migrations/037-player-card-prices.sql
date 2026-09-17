-- 037 — player_card_prices: FC 카드 시세 스냅샷 (2026-09-18, 사용자 지시
--       「초반 스쿼드 구성을 위해 제한된 자원에서 누구를 먼저 사야 하는지 등 선수 가격 정보까지 붙여」).
--
-- 시세는 하루에도 움직이는 값이라 **덮어쓰지 않고 날짜별로 쌓는다**(불변규칙 2). 화면은 최신 pulled만 읽고,
-- 「구매 우선순위」는 화면이 처방 역할·대체 가능성과 시세를 대조해 만든다 — 순위를 여기 굳히지 않는다.
--
-- 원천: fut.gg 목록 API `/api/fut/players/v2/{game}/?ea_ids=…`의 `currentDbPrice`/`price`/`hasPrice`
--   (전용 `/api/fut/player-prices/`는 Cloudflare 403 — curl·브라우저 fetch 모두, 2026-09-18 실증).
--   ⚠️ FC27 이적시장이 열리기 전(얼리액세스 09-18 · 정식 09-25)에는 hasPrice=0이라 **가격 없음 = 미형성**이지 0이 아니다.
PRAGMA foreign_keys = ON;
BEGIN;
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
COMMIT;
