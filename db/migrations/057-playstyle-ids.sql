-- PlayStyle 숫자 id → 이름 (2026-09-22 신설)
-- 왜: 진화 분기(`upgradeOptions`)와 `playstyles_after`가 PlayStyle을 **숫자 id로만** 준다.
--     이름표가 없으면 화면에 「PlayStyle #8」처럼 못 읽는 값이 나온다.
-- ⛔ 표를 손으로 적지 않는다 — `player_evolutions`의 id 배열 ↔ 이름 배열 교차로 역산한다.
-- ⛔⛔ **역산 결과를 그때그때 계산해 쓰면 표본이 줄 때 이름이 사라진다**(2026-09-22 실증:
--     코스메틱 경로 210행을 지우자 29개 → 17개로 줄어 「#8」이 화면에 떴다).
--     ⇒ 여기에 **누적**한다. 새로 확정된 것만 넣고 기존 행은 지우지 않는다(불변규칙 2).
CREATE TABLE IF NOT EXISTS fc_playstyle_ids(
  game_version TEXT NOT NULL REFERENCES game_versions(code),
  ea_id INTEGER NOT NULL,
  name TEXT NOT NULL,
  source TEXT, confidence TEXT, pulled TEXT NOT NULL,
  PRIMARY KEY(game_version, ea_id)
);
