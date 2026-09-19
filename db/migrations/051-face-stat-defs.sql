-- 051 6대 스탯 구성식 (2026-09-19, 사용자 지시 「붙인 후 스탯의 변경도 볼수있게」)
-- PAC/SHO/PAS/DRI/DEF/PHY는 개별 속성의 **가중 평균**이다. 이 표가 있어야 케미 스타일을 붙였을 때
-- 6대 스탯이 몇으로 바뀌는지 계산할 수 있다(스타일 부스트는 개별 속성에만 들어온다).
CREATE TABLE IF NOT EXISTS fc_face_stats(
  id INTEGER PRIMARY KEY,
  game_version TEXT NOT NULL REFERENCES game_versions(code),
  face_key TEXT NOT NULL,        -- facePace / gkFaceDiving …
  abbr TEXT NOT NULL,            -- PAC / DIV …
  is_gk INTEGER NOT NULL DEFAULT 0,
  attr TEXT NOT NULL,            -- 한글 속성 라벨(다른 표와 같은 키)
  weight REAL NOT NULL,
  pulled TEXT NOT NULL, source TEXT NOT NULL, confidence TEXT NOT NULL,
  UNIQUE(game_version, face_key, attr)
);
