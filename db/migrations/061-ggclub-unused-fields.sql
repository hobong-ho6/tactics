-- 061 GG Club 싱크가 **줄 수 있는데 안 받던** 축들 (2026-09-24 사용자 지시 「1순위부터 5순위까지 전부 진행」)
--
-- 왜: GG Club API는 카드 한 장에 `playerDef` 163필드 + 보유행 29필드를 준다. 우리는 13개만 썼다.
--   그 결과 두 가지가 실제로 터졌다:
--     ⑴ **PlayStyle**을 안 받아 `current_playstyles`가 fut.gg **계산 결과 카드**(path_json)에서 왔다
--        ⇒ 보가르데에 Inventive가, 루제리에 Inventive가 **없는 능력으로 찍혔다**(EA 실측은 Tiki Taka뿐).
--        API의 `playstyles`/`playstylesPlus`가 EA 실측이다 — 그걸 받으면 이 오류가 **구조적으로 불가능**해진다.
--     ⑵ **경기 기록**(출전·득점·도움·경고)이 통째로 비어 있었다. 「내가 실제로 누굴 썼고 어땠나」는
--        처방·구매 판단의 1차 근거인데 원장에 축 자체가 없었다.
--
-- ⛔ 여기 있는 것은 전부 **EA 실측**이다(fut.gg 계산값이 아니다). 산출값과 충돌하면 실측을 채택한다(불변규칙 3).

-- ── ③ 스쿼드·자산 축 — 카드의 현재 상태라 fut_club_players에 둔다 ──────────────────
ALTER TABLE fut_club_players ADD COLUMN is_untradeable INTEGER;      -- 1=거래 불가. ⭐ 진화 대상 선정과 직결(팔 수 없는 카드부터 태운다)
ALTER TABLE fut_club_players ADD COLUMN is_in_active_squad INTEGER;  -- 1=활성 스쿼드(선발+교체). fut_squad_slots와 교차 검산용
ALTER TABLE fut_club_players ADD COLUMN is_captain INTEGER;          -- 1=주장
ALTER TABLE fut_club_players ADD COLUMN kit_number INTEGER;          -- 등번호(인게임 실제값)
ALTER TABLE fut_club_players ADD COLUMN number_of_owners INTEGER;    -- 이 아이템을 거쳐 간 소유자 수

-- ── ② 경기 기록 — **누적값**이라 회차 스냅샷으로 쌓는다(덮지 않는다 · 불변규칙 2) ────────
-- ⚠️ `games_played`/`goals`는 **현재 클럽 보유분 기준 누적**이고 `lifetime_*`은 카드 일생 누적이다.
--    둘이 다를 수 있다(이적시장을 거쳐 온 카드) — 그래서 둘 다 남긴다.
CREATE TABLE IF NOT EXISTS fut_club_player_stats(
  club_player_id INTEGER NOT NULL REFERENCES fut_club_players(id),
  pulled         TEXT NOT NULL,             -- 수집일 — 누적값이라 시점이 정본이다
  games_played   INTEGER, goals INTEGER, assists INTEGER,
  yellow_cards   INTEGER, red_cards INTEGER,
  ga             REAL,                      -- fut.gg가 계산해 주는 경기당 공격포인트
  lifetime_games_played INTEGER, lifetime_goals INTEGER, lifetime_assists INTEGER,
  lifetime_yellow_cards INTEGER, lifetime_red_cards INTEGER,
  source TEXT, confidence TEXT,
  PRIMARY KEY(club_player_id, pulled)
);
CREATE INDEX IF NOT EXISTS ix_fut_club_player_stats_pulled ON fut_club_player_stats(pulled);
