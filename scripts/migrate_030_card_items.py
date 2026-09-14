#!/usr/bin/env python3
"""migration 030 — `player_card_items` 신설 (2026-09-14, 사용자 지시 「새 카드가 나오면 확인할 수 있게」).

왜 별도 테이블인가:
  `player_game_stats`는 **「그 선수의 능력치 정본」**이고 키가 `(game_version, roster_date, name_kr)`다.
  프로모 카드(TOTW·Path to Glory·…)를 여기에 넣으면 ⑴ 같은 날 두 장이 나오면 UNIQUE에 걸리고
  ⑵ 시즌 분석 질의(`roster_date='2026-09-10'`)가 조용히 프로모 능력치를 집어간다.
  ⇒ **카드 아이템은 카드 테이블에**. 기본(base) 카드도 같은 표에 넣어 한 선수의 카드 목록이 한 곳에서 끝나게 한다.

수집 경로: fut.gg `/api/fut/players/v2/all-versions/{basePlayerEaId}/` — 한 응답에 그 선수의
**전 버전·전 카드**가 6대 스탯·34속성·PlayStyles(+)·Role+/++까지 붙어서 온다(curl 200).
희귀도 이름만 목록 API(`/api/fut/players/v2/{game}/?ea_ids=`)에서 따로 받는다.

재실행 안전: 테이블이 이미 있으면 아무것도 하지 않는다.
"""
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core import DB                                     # noqa: E402

DDL = """
CREATE TABLE IF NOT EXISTS player_card_items(
  id INTEGER PRIMARY KEY,
  game_version TEXT NOT NULL REFERENCES game_versions(code),
  ea_item_id INTEGER NOT NULL,      -- fut.gg eaId. 프로모 카드는 base와 다른 id를 받는다
  base_ea_id INTEGER,               -- 그 선수의 base eaId (= player_game_stats 카드 URL의 27-{id})
  is_base INTEGER NOT NULL DEFAULT 0,
  player_id INTEGER REFERENCES players(id),
  name_kr TEXT NOT NULL,            -- 표시용 (조인 금지 — 사람 조인은 player_id)
  rarity_ea_id INTEGER, rarity_name TEXT,     -- 'Rare' / 'Team of the Week' / …
  released_at TEXT,                 -- 아이템 createdAt(EA 공개일) — 시점 축
  club TEXT, positions TEXT, best_pos TEXT,
  ovr INTEGER, pac INTEGER, sho INTEGER, pas INTEGER, dri INTEGER, def INTEGER, phy INTEGER,
  attrs TEXT, playstyles TEXT,      -- attrs는 한글 라벨 JSON(다른 표와 같은 키), playstyles는 '…, …+' 문자열
  roles_plus TEXT, roles_plus_plus TEXT,      -- ⛔ FC27 역할 id는 카탈로그 미공개라 **raw id 목록**으로 둔다
  skill_moves INTEGER, weak_foot INTEGER, accelerate TEXT, preferred_foot TEXT,
  card_image_url TEXT, futgg_url TEXT,
  source TEXT, confidence TEXT,
  UNIQUE(game_version, ea_item_id)
);
CREATE INDEX IF NOT EXISTS ix_card_items_player ON player_card_items(player_id, game_version);
"""

con = sqlite3.connect(DB)
existed = con.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='player_card_items'").fetchone()
con.executescript(DDL)
con.execute("INSERT OR IGNORE INTO _migration_log(run_at, v1_path, note) VALUES(?,?,?)",
            ("2026-09-14", "030-card-items",
             "player_card_items 신설 — 관리 선수의 FC 카드 버전(base + 프로모)을 fut.gg all-versions API로 적재한다. "
             "player_game_stats는 능력치 정본이라 프로모를 섞지 않는다(UNIQUE 충돌·시즌 질의 오염). "
             "FC27 역할 숙련(Role+/++)은 카탈로그 미공개라 raw id로만 보관한다."))
con.commit()
print("이미 존재 — 변경 없음" if existed else "✅ player_card_items 생성")
