-- 055 · fut.gg 케미 스타일 신호 (2026-09-21, 사용자 지시 「fut.gg 케미 등급이랑 투표율 수집해줘」)
--
-- ⚠️ fut.gg 선수 페이지의 스타일 옆 배지는 **등급이 아니다**. 2026-09-21 실측으로 확정:
--    카마라(AcceleRATE Controlled)는 19개 스타일이 전부 `C`, 음바페(Explosive)는 대부분 `E`이고
--    Sniper·Architect만 `C`였다 ⇒ 배지는 **그 스타일을 붙였을 때의 AcceleRATE**다
--    (C=Controlled · E=Explosive · L=Lengthy). 「케미 등급」으로 읽으면 안 된다.
-- ⭐ 투표율(`vote_pct`)은 커뮤니티 투표 비율이고 **fut.gg 편집부 추천이 아니다** — 인기이지 정답이 아니다.
-- ⛔ 투표가 0건이면 행을 만들되 vote_pct는 NULL이다(0이 아니다 — obs#132 결손/0 구분).
--
-- 키는 `ea_item_id`(카드 단위)다. 같은 선수라도 카드가 다르면 속성이 달라 AcceleRATE가 갈린다.
CREATE TABLE IF NOT EXISTS futgg_chem_signals (
  id INTEGER PRIMARY KEY,
  ea_item_id INTEGER NOT NULL,
  pulled TEXT NOT NULL,              -- 수집일 (스냅샷이므로 날짜가 정본)
  style_name TEXT NOT NULL,          -- fut.gg 표기 그대로 (Basic/Sniper/…)
  accelerate TEXT,                   -- 그 스타일 적용 시 AcceleRATE: Controlled/Explosive/Lengthy
  vote_pct REAL,                     -- 커뮤니티 투표 비율(%) · 투표 없으면 NULL
  source TEXT,
  confidence TEXT,
  UNIQUE(ea_item_id, pulled, style_name)
);
CREATE INDEX IF NOT EXISTS ix_futgg_chem_item ON futgg_chem_signals(ea_item_id, pulled);

-- 카드 단위 메타(현재 AcceleRATE·투표 총수)는 별도로 두지 않고 signals의 Basic 행 + vote 합으로 읽는다.
