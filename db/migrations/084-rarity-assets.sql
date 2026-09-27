-- 084 레어도 판(카드 틀) 자산 — 브론즈/실버/골드 3단계 (2026-09-27)
--
-- 왜 (사용자 지시 「진화해서 금카가 된 건 금카로 카드 이미지도 바꿔줘」):
--   ⛔⛔ **fut.gg도 EA도 진화 카드의 완성 이미지를 주지 않는다** — 실측으로 확인했다:
--      `paths/v2`가 주는 단계별 카드의 `cardImagePath`가 **OVR 65 카드와 75 카드가 동일 파일**이고,
--      GG Club은 아이템 id를 **base 그대로**(80652) 준다. 진화 아이템의 별도 id·이미지는 없다.
--   ⭐ 그런데 fut.gg 화면은 골드로 보인다. 이유는 **클라이언트에서 합성**하기 때문이다:
--      빈 레어도 판(`rarities-level-{1,2,3}-large`) + 선수 렌더(`player-item/`) + 텍스트·로고.
--      `rarity.imageUrls`·`lineColor`·`textColor`가 전부 **3단계 배열**로 온다.
--   ⇒ 우리도 같은 재료를 받아 합성한다. 이 표가 그 재료(판)다.
--
-- ⭐⭐ **등급 경계는 실측으로 확정했다**(2026-09-27 · 등급 C):
--    fut.gg 간이 카드 자산 4장을 직접 열어 판 색을 확인했다 —
--    **64 브론즈 · 65 실버 · 74 실버 · 75 골드**. ⇒ 브론즈 ≤64 · 실버 65~74 · 골드 ≥75.
--    ⛔ 이 값을 코드에 흩뿌리지 않는다 — 판정은 `core/`의 한 함수가 한다(불변규칙 13 ②).
--
-- ⚠️ `level`은 1=브론즈 · 2=실버 · 3=골드다(fut.gg 배열 인덱스 0/1/2에 +1).
-- ⚠️ 특별 카드(아이콘·히어로 등)는 레어도마다 판이 하나뿐일 수 있다 — 그때는 level 3만 채운다.
CREATE TABLE fc_rarity_assets(
  game_version  TEXT NOT NULL,
  rarity_ea_id  INTEGER NOT NULL,
  rarity_name   TEXT,
  level         INTEGER NOT NULL,        -- 1 브론즈 · 2 실버 · 3 골드
  image_url     TEXT,                    -- 빈 판(large)
  compact_url   TEXT,
  line_color    TEXT,                    -- 테두리/구분선 색 (#RRGGBB 없이 6자리)
  text_color    TEXT,
  dominant_color TEXT,
  is_special    INTEGER DEFAULT 0,
  pulled        TEXT NOT NULL,
  source        TEXT,
  confidence    TEXT,
  PRIMARY KEY(game_version, rarity_ea_id, level, pulled)
);
CREATE INDEX ix_fc_rarity_assets_pulled ON fc_rarity_assets(pulled);
