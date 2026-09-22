-- 058 진화 적용 가능 선수 (2026-09-22 사용자 지적 「구단 싱크로 누락됐던 진화가 추가됐다 —
--     각 메뉴의 진화 수행 선수 제안에 모두 반영」 · 「선수별 경로뿐 아니라 카탈로그에도 없었다」)
--
-- 왜 따로 필요한가: `player_evolutions`(fut.gg paths API)는 **base 카드 기준 조합 경로**만 준다.
--   ⛔ 그래서 두 부류를 통째로 놓친다 —
--     ⑴ 특별 카드에만 열리는 진화(음바예는 특별 카드가 대상인데 `paths/v2/50406097/`은 404다),
--     ⑵ paths 응답이 아예 만들지 않는 단독 진화(Relentless 2495는 적용 가능 선수가 150명인데
--        그 카드들의 paths 응답 어디에도 나오지 않는다 — 카탈로그에도 안 잡혀 손수집해야 했다).
--   2026-09-22 실측: 이렇게 빠진 (선수, 진화) 쌍이 **33건**이었다(음바예 4종·잭슨·비조 2종·마첸 등).
--
-- ⛔ 경로(단계·비용·결과 카드)를 여기서 지어내지 않는다 — fut.gg가 주지 않는 사실이다.
--    이 표가 담는 것은 **「이 선수에게 이 진화가 열려 있다」는 사실 하나**이고,
--    화면은 경로가 없다는 것을 숨기지 말고 그대로 적는다(결손과 0은 다르다, obs#132).
CREATE TABLE IF NOT EXISTS fc_evolution_eligibility(
  game_version TEXT NOT NULL REFERENCES game_versions(code),
  evo_id       INTEGER NOT NULL,
  player_id    INTEGER NOT NULL REFERENCES players(id),
  ea_item_id   INTEGER NOT NULL,     -- 적용 대상 카드 (base일 수도 특별 카드일 수도 있다)
  is_base      INTEGER,              -- 그 카드가 기본 카드인가 — paths 축이 덮는지와 직결된다
  pulled       TEXT NOT NULL,        -- 진화는 기간제다. 덮지 않고 날짜별로 쌓는다.
  source       TEXT,
  PRIMARY KEY (game_version, evo_id, ea_item_id, pulled)
);
CREATE INDEX IF NOT EXISTS ix_evo_elig_player ON fc_evolution_eligibility(player_id, pulled);
