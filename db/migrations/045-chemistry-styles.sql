-- 045 케미스트리 스타일 (2026-09-19, 사용자 지시 「내가 이야기한 케미스트리는 선수에게 부여할 호크나 엔진 이런 케미였어」)
-- 스쿼드 링크(044)와 다른 축이다 — 이건 선수에게 **붙이는 소모품**이고, 개별 속성에 3/6/9를 더한다.
-- ⛔ 6대 스탯(PAC/SHO/…) 단위로 적지 않는다. 역할 가중(game_role_key_attrs)이 **개별 속성** 단위라
--    같은 +3이라도 그 역할에 쓸모가 있는지 없는지가 갈린다. 원천도 개별 속성으로 준다.
CREATE TABLE IF NOT EXISTS fc_chemistry_styles(
  id INTEGER PRIMARY KEY,
  game_version TEXT NOT NULL REFERENCES game_versions(code),
  style_id INTEGER NOT NULL,        -- fut.gg 내부 id(1=Basic … 24=Cat). EA 소모품 id와 다르다
  name TEXT NOT NULL,               -- 'Hawk' · 'Engine' …
  is_gk INTEGER NOT NULL DEFAULT 0,
  boosts TEXT NOT NULL,             -- {"공격 위치 선정": 9, …} — 최대 케미(3) 기준 한글 속성 라벨 JSON
  pulled TEXT NOT NULL,
  source TEXT NOT NULL, confidence TEXT NOT NULL,
  UNIQUE(game_version, style_id)
);
