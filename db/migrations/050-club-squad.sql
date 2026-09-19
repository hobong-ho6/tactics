-- 050 실제 스쿼드 (2026-09-19, 사용자 지적 「난 지금 골키퍼 스즈키 쓰고 있는데? 케미 추천이 지금 구성과 다르다」)
-- 케미 제안은 「보유 카드로 짤 수 있는 최적」이라 **실제로 쓰는 XI와 다르다**. 둘을 나란히 보려면 실제 스쿼드가 필요하다.
-- GG Club active-squad 응답이 슬롯·선발/교체·포메이션·감독 국적/리그를 준다.
CREATE TABLE IF NOT EXISTS fut_squads(
  account_id INTEGER PRIMARY KEY REFERENCES fut_accounts(id),
  title TEXT, formation_id TEXT,
  manager_nation_id INTEGER, manager_league_id INTEGER,   -- 케미 감독 보너스(+1) 판정에 쓴다
  build_up_style_id INTEGER, defensive_approach_id INTEGER, custom_def_value INTEGER,
  synced_at TEXT NOT NULL, source TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS fut_squad_slots(
  account_id INTEGER NOT NULL REFERENCES fut_accounts(id),
  grp TEXT NOT NULL,            -- FIELD / SUBSTITUTE
  idx INTEGER NOT NULL,         -- 포메이션 슬롯 순서(FIELD 0=GK …)
  ea_item_id INTEGER,
  gg_player_id TEXT,
  synced_at TEXT NOT NULL,
  PRIMARY KEY(account_id, grp, idx)
);
