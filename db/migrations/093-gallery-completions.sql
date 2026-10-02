-- 093 내가 완성한 갤러리 — 이력형 원장 (2026-10-02 사용자 지시 「완성한 세트는 fut.gg에 기록하지 말고 DB에」 →
--   「내가 완성한 갤러리 정보도 우리 디비에서 관리」).
--
-- 왜: 092의 `fut_gallery_log`는 세트당 등급 한 칸을 **덮어썼다** — 언제 완성했는지·무슨 카드를 넣었는지·
--   등급을 언제 올렸는지가 남지 않았다(불변규칙 2 「추가만」에도 어긋난다).
--   ⇒ 완성·등급 상승마다 **행을 추가**한다. 「지금 내 등급」은 세트별 최신 행이다.
-- ⭐ 넣은 카드(card_ids)를 남기는 이유: 세트에 넣은 카드는 팔거나 SBC에 내도 그 세트 점수로 남는다(가이드 공통 · 등급 D)
--   — 원장에서 카드가 빠져도 「무엇으로 완성했나」는 여기서 안다.
-- ⛔ fut.gg에는 쓰지 않는다 — 인게임 갤러리 화면이 정본이고 우리 DB가 그 기록이다.
CREATE TABLE fut_gallery_completions(
  id           INTEGER PRIMARY KEY,
  game_version TEXT NOT NULL,
  set_id       INTEGER NOT NULL,
  grade        TEXT NOT NULL CHECK(grade IN ('D','C','B','A','S')),
  completed_at TEXT NOT NULL,
  score        INTEGER,          -- 기록 시점 우리 계산(태그 제외 하한) — 인게임 점수와 다를 수 있다
  card_ids     TEXT,             -- 넣은 카드 fut_club_players.id JSON — 우리 제안대로 넣었을 때만(아니면 NULL)
  source TEXT, notes TEXT
);
CREATE INDEX ix_gal_comp_set ON fut_gallery_completions(game_version, set_id, completed_at);

-- 092의 덮어쓰기 표는 비어 있는 채로 대체된다(같은 날 신설 · 행 0). 남겨 두면 「내 등급」 정본이 두 곳이 된다.
DROP TABLE fut_gallery_log;
