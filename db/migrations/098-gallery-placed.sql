-- 098 인게임 갤러리 세트에 들어가 있는 아이템 + 세트 점수 스냅숏 (2026-10-03 사용자 지시 「세트별 등록 진행해줘」).
--
-- 왜: 갤러리 세트에는 **예전에 가졌던 아이템**이 대거 들어가 있다(레알 마드리드 16장 중 우리 원장이 아는 것 8장 ·
--   프리미어 리그 인게임 기본 28,426 vs 원장만으로 14,976). 넣은 아이템은 팔거나 SBC에 내도 남는다(EA 피치노트 FUT 딥다이브
--   2026-08-02 · 등급 A). ⛔ fut.gg는 갤러리 진행 상태를 주지 않는다 ⇒ 인게임 캡처를 전사해 적는다.
-- 행은 캡처 1회 = 세트별 묶음으로 **추가만** 한다(불변규칙 2). 평가는 세트별 최신 captured_at 묶음을 쓴다.
CREATE TABLE fut_gallery_placed(
  id            INTEGER PRIMARY KEY,
  game_version  TEXT NOT NULL,
  set_id        INTEGER NOT NULL,
  captured_at   TEXT NOT NULL,
  slot          INTEGER NOT NULL,          -- 화면 순서(1부터)
  score         INTEGER NOT NULL,          -- 화면의 아이템 점수
  ovr           INTEGER, pos TEXT,         -- 카드 표기(주 포지션)
  nation        TEXT,                      -- 국기 판독(틀릴 수 있다 — 매칭 보조)
  ea_item_id    INTEGER,                   -- 식별되면(원장 또는 player_card_items에서 점수·OVR·포지션·국적이 하나로 맞을 때)
  club_player_id INTEGER,                  -- 우리 원장(fut_club_players.id)과 맞으면
  source TEXT, notes TEXT
);
CREATE INDEX ix_gal_placed_set ON fut_gallery_placed(game_version, set_id, captured_at);

-- 화면에 점수가 나온 세트의 인게임 값(완성된 세트만 점수가 나온다). 우리 계산식 검증용 정답지.
CREATE TABLE fut_gallery_snapshots(
  id            INTEGER PRIMARY KEY,
  game_version  TEXT NOT NULL,
  set_id        INTEGER NOT NULL,
  captured_at   TEXT NOT NULL,
  placed_n      INTEGER NOT NULL,
  base_score    INTEGER, bonus_score INTEGER, total_score INTEGER,
  grade         TEXT CHECK(grade IN ('D','C','B','A','S')),
  pending       INTEGER NOT NULL DEFAULT 0,  -- 1 = 화면 버튼이 「변경 사항 확인」(확정 전 구성)
  source TEXT, notes TEXT
);
