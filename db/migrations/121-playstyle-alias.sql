-- 121 PlayStyle 이름 별칭 표 (2026-10-22 FC27 시스템 검토 §2 ⒜5 · §4 「어휘 드리프트」 · §7 조치 2).
--
-- 왜: EA FC27 공식 명칭은 「1v1 Close Down」(옛 Rush Out) · 「Gamechanger」(한 단어)인데, fut.gg 카드 페이지·번들 라벨과
--   우리 저장 행(fut_club_players.current_playstyles 46장 · player_game_stats FC27 10행 · fc_playstyle_ids 31/37)은 옛 이름을 쓴다.
--   같은 PlayStyle이 두 이름으로 돌아다니면 비교 화면의 「상대에게 없는 PlayStyle」 판정이 갈린다(collect_playstyle_ids.py 머리말 실증).
--   파생 어휘는 정본 집합 + 게이트로 묶는다(obs#527 교훈) — 저장 행은 **고치지 않고** 별칭 표를 둔다(불변규칙 2).
-- 읽기: core/playstyles.py(canonical · vocab) 한 곳. 화면은 export가 index.json에 실은 playstyle_aliases를 playstyle-icons.js psLookup 한 곳에서 쓴다.
-- 게이트: G35 ⑵ — 현행 버전 카드 데이터의 PlayStyle 이름이 정본 ∪ 별칭 밖이면 실패.
CREATE TABLE IF NOT EXISTS fc_playstyle_aliases (
  game_version TEXT NOT NULL,
  alias        TEXT NOT NULL,          -- 저장 행·외부 소스에서 보이는 이름
  canonical    TEXT,                   -- EA 공식 이름. NULL = 이 버전 목록에 없는 이름(FC24~25 잔존)
  source       TEXT NOT NULL,
  note         TEXT,
  added        TEXT NOT NULL,
  PRIMARY KEY (game_version, alias)
);
INSERT OR IGNORE INTO fc_playstyle_aliases (game_version, alias, canonical, source, note, added) VALUES
 ('FC27', 'Rush Out',      '1v1 Close Down', 'EA what-are-playstyles (2026-09-25) · fut.gg /playstyles/ (slug rush-out 유지 · 2026-10-22 열람)', 'FC27 개명. fut.gg 카드 페이지·번들 라벨은 Rush Out', '2026-10-22'),
 ('FC27', 'Game Changer',  'Gamechanger',    'EA what-are-playstyles (2026-09-25)', 'EA 표기는 한 단어. fc_playstyle_ids 37은 두 단어', '2026-10-22'),
 ('FC27', 'Long Ball',     'Long Ball Pass', 'fut.gg 웹앱 번들 PLAY_STYLE_LABELS 축약 라벨 (collect_playstyle_ids.py 머리말)', '번들 라벨 ↔ 카드 이름', '2026-10-22'),
 ('FC27', 'Low Driven',    'Low Driven Shot','fut.gg 웹앱 번들 PLAY_STYLE_LABELS 축약 라벨 (collect_playstyle_ids.py 머리말)', '번들 라벨 ↔ 카드 이름', '2026-10-22'),
 ('FC27', 'Flair',         NULL, 'EA what-are-playstyles (2026-09-25) 36종 목록에 없음', 'FC24~25 잔존 이름(fut.gg 번들 라벨 id 18) — FC27 없음', '2026-10-22'),
 ('FC27', 'Trivela',       NULL, 'EA what-are-playstyles (2026-09-25) 36종 목록에 없음', 'FC24~25 잔존 이름(id 24) — FC27 없음', '2026-10-22'),
 ('FC27', 'Power Header',  NULL, 'EA what-are-playstyles (2026-09-25) 36종 목록에 없음', 'FC24~25 잔존 이름(id 4) — FC27 없음(Precision Header 39가 현행)', '2026-10-22'),
 ('FC27', 'Aerial',        NULL, 'EA what-are-playstyles (2026-09-25) 36종 목록에 없음', 'FC24~25 잔존 이름(id 27) — FC27 없음(Aerial Fortress 35가 현행)', '2026-10-22');
INSERT INTO _migration_log (run_at, v1_path, note) VALUES
 ('2026-10-22', '121-playstyle-alias',
  'fc_playstyle_aliases 신설 — FC27 개명(Rush Out→1v1 Close Down · Game Changer→Gamechanger) · 번들 축약 라벨 2 · FC24~25 잔존 4(canonical NULL) · core/playstyles.py 단일 읽기 · export index.json playstyle_aliases · G35 ⑵ 어휘 게이트');
