-- 047 GG Club 싱크 반영 (2026-09-19, 사용자 지시 「싱크했어 스쿼드 업데이트」)
-- ⭐ 케미 스타일은 **EA 소모품 id**로 들어온다(250 Basic … 273 GK Basic). fut.gg 내부 id(1~24)와 다르므로 대조 컬럼을 만든다.
--    매핑 근거: fut.gg 번들 styleAttribMods(styleId ↔ 6대 스탯 보너스 패턴)로 1:1 확인했다.
ALTER TABLE fc_chemistry_styles ADD COLUMN ea_id INTEGER;
-- 보유 선수의 **현재 적용 상태** — 싱크할 때마다 갱신되는 스냅샷이다(원장의 진화 로그와 별개 층).
ALTER TABLE fut_club_players ADD COLUMN chem_style_ea INTEGER;
ALTER TABLE fut_club_players ADD COLUMN chem_points INTEGER;
ALTER TABLE fut_club_players ADD COLUMN gg_player_id TEXT;
ALTER TABLE fut_club_players ADD COLUMN synced_at TEXT;
