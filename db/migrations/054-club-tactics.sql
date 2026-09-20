-- 054 · 내 구단 인게임 전술 스냅샷 (2026-09-20 · 사용자 지시 「현 스쿼드와 전술을 파악할 수 있는 영역을 추가」)
--
-- 왜: 지금까지 인게임 전술은 `team_tactic_setups`에 `ingame:user-YYYY-MM-DD` kind로 손으로 적었다.
--   ⇒ 이제 GG Club `/api/gg-club/tactics/`에서 **11칸 역할·포커스 + 빌드업 + 수비 접근 + 라인**을 그대로 읽는다.
--   ⛔ 이것은 **내 얼티밋 구단의 실제 설정**이고, 감독 재현(`team_tactic_setups`)과 **다른 층**이다 — 섞지 않는다.
--   ⭐ 날짜별로 쌓는다(`pulled`). fut.gg의 `lastUpdatedAt`도 함께 저장해 **내가 언제 바꿨는지**를 남긴다.
CREATE TABLE IF NOT EXISTS fut_tactics (
  account_id        INTEGER NOT NULL,
  pulled            TEXT    NOT NULL,          -- 우리가 읽은 날
  tactic_code       TEXT,                      -- 인게임 공유 코드
  title             TEXT,
  formation         TEXT,                      -- 화면 표기 그대로(예: 4-2-3-1 (2))
  formation_id      TEXT,
  build_up_style    TEXT,                      -- 화면 표기(예: Balanced)
  defensive_approach TEXT,
  line_height       INTEGER,                   -- 커스텀 수비 접근 값
  is_custom_def     INTEGER DEFAULT 0,
  chemistry         INTEGER,
  squad_name        TEXT,
  last_updated_at   TEXT,                      -- fut.gg가 기록한 마지막 변경 시각(UTC)
  source            TEXT,
  confidence        TEXT,
  PRIMARY KEY (account_id, pulled)
);
-- 11칸 역할·포커스
CREATE TABLE IF NOT EXISTS fut_tactic_roles (
  account_id   INTEGER NOT NULL,
  pulled       TEXT    NOT NULL,
  position_id  INTEGER NOT NULL,               -- EA positionUniqueId
  position_name TEXT,                          -- GK/RB/CB/...
  role_ea_id   INTEGER,
  role_name    TEXT,
  focus        TEXT,
  PRIMARY KEY (account_id, pulled, position_id)
);
