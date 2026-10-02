-- 092 갤러리 — 내 카드로 달성 가능한 등급 평가 (2026-10-02 사용자 지시
--   「내 카드들로 어떤 갤러리 팀들을 완성할 수 있는지」 → 「얼티밋팀 하위에 갤러리 메뉴 · 클럽 싱크 선수 수집이 끝나면
--    달성 가능한 갤러리와 더 높일 수 있는 갤러리 목록 · 달성 가능하면 NEW 배지나 알림」).
--
-- ⛔ fut.gg는 **내 갤러리 진행도를 주지 않는다**(개인 경로 전부 404 — collect_futgg_gallery.py 주석).
--   ⇒ 「지금 카드로 낼 수 있는 등급」은 우리가 계산하고(fut_gallery_eval),
--      「이미 달성한 등급」은 사용자가 화면에서 기록한다(fut_gallery_log).

-- 카드 → 세트 매칭은 **EA id로** 한다(불변규칙 6 — 이름 조인 금지). 클럽 세트는 남녀 자매 구단까지 인정한다.
ALTER TABLE player_card_items ADD COLUMN club_ea_id INTEGER;
ALTER TABLE player_card_items ADD COLUMN sibling_club_ea_id INTEGER;   -- fut.gg club.siblingClubEaId(남↔여 구단)
ALTER TABLE player_card_items ADD COLUMN league_ea_id INTEGER;

-- 싱크 회차마다 세트별 평가 스냅샷을 **추가**한다(불변규칙 2). 직전 회차와 견줘 「새로 달성 가능」을 가른다.
CREATE TABLE fut_gallery_eval(
  game_version TEXT NOT NULL,
  set_id       INTEGER NOT NULL,
  pulled       TEXT NOT NULL,
  eligible_n   INTEGER,          -- 세트에 넣을 수 있는 보유 카드 수
  required_n   INTEGER,          -- 세트 칸 수
  base_score   INTEGER,          -- 상위 required_n장 아이템 점수 합(태그 보너스 제외 = 하한)
  grade        TEXT,             -- 그 점수로 닿는 최고 등급(D~S) · 없으면 NULL
  next_grade   TEXT, next_gap INTEGER,
  prev_grade   TEXT,             -- 직전 회차의 grade
  card_ids     TEXT,             -- 고른 카드 fut_club_players.id JSON
  supported    INTEGER NOT NULL DEFAULT 1,   -- 0이면 대상 규칙 미상(판정하지 않음)
  source TEXT, confidence TEXT,
  PRIMARY KEY(game_version, set_id, pulled)
);

-- 사용자가 기록한 「지금 내 등급」 — 인게임 갤러리 화면이 정본이다.
CREATE TABLE fut_gallery_log(
  game_version TEXT NOT NULL,
  set_id       INTEGER NOT NULL,
  grade        TEXT,             -- D~S · NULL이면 기록 취소
  recorded_at  TEXT NOT NULL,
  source TEXT, notes TEXT,
  PRIMARY KEY(game_version, set_id)
);
