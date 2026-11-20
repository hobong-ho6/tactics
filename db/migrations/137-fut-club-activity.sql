-- 137 GG Club 액티비티 피드 원본(2026-11-20 사용자 지시 「액티비티 히스토리 … 진화 정보를 수집할수 있는지 검토」 → 「1·2 둘 다 여기서 구현」).
--
-- 왜: fut.gg GG Club 액티비티(`/api/gg-club/<클럽>/activity/` · 로그인 불요)가 진화 완료·영입을 **시각과 함께** 준다.
--   ⑴ 진화 완료일 — 원장(fut_evolution_log.completed_at)이 EA 이력 백필 날짜로 7~11일 늦게 적힌 행이 있었다(5건 · 11-18).
--      액티비티의 evo.completed(date_kind='sync')는 「싱크에서 발견한 시각」이라 **실제 완료일의 상한**이다.
--   ⑵ 영입 경로 — fut_club_players.acquired_how가 전부 「GG Club 싱크」였다. signing.* 이벤트가 구매가·SBC/목표 이름·시즌패스 레벨을 준다.
-- 어떻게: 이벤트를 **추가만** 한다(event_id = fut.gg 이벤트 id). 정정·채우기는 scripts/collect_ggclub_activity.py가 이 표를 근거로 한다.
-- ⚠️ 한계: 피드는 2026-10-23부터만 있고, 주요 장면 위주다(10-23 이후 추가 카드 323장 중 38장만 영입 이벤트). 판매·SBC 제출 이벤트는 없다.
CREATE TABLE IF NOT EXISTS fut_club_activity(
  event_id TEXT PRIMARY KEY,
  account_id INTEGER NOT NULL REFERENCES fut_accounts(id),
  type TEXT NOT NULL,              -- evo.completed · signing.bought · signing.reward …
  occurred_at TEXT NOT NULL,       -- UTC ISO(fut.gg 원값)
  date_kind TEXT,                  -- sync = 싱크에서 발견한 시각(상한) · exact = 실제 시각
  payload TEXT NOT NULL,           -- fut.gg payload JSON 원문
  pulled TEXT NOT NULL,
  source TEXT NOT NULL,
  confidence TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS ix_fut_club_activity_type ON fut_club_activity(type, occurred_at);
