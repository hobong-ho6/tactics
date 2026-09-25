-- 069 챌린지별 요구 포메이션 (2026-09-25 사용자 지적 「노르웨이대 포르투갈에서 요구하는 포메이션과
--     네가 보여준 포메이션이 다르다」 · 이어 「챌린지마다 고정이다」로 확인)
--
-- ⛔⛔ **EA도 fut.gg도 이 값을 주지 않는다**(2026-09-25 실측):
--   · `requirementsText`에 포메이션 문장이 없다(Norway v Portugal은 6개 조건이 전부).
--   · 챌린지 API 응답 어디에도 formation 필드가 없다.
--   · fut.gg 자체 해법도 **자기가 임의로 고른다**(Break Away 해법 = 4-3-3).
--   ⇒ 인게임은 **챌린지마다 포메이션이 고정**인데 그 값이 어디서도 안 나온다.
--     ⇒ 진화 로그·SBC 완료와 같은 축이다: **사용자가 알려 주면 우리가 적는다.**
--
-- ⛔ 값이 없으면 화면은 「포메이션 미기록」으로 적고 **아무 포메이션이나 골라 보여주지 않는다**
--    — 그게 이번 사고(케미 최대 포메이션을 임의로 골라 인게임과 달랐다)의 원인이었다.
CREATE TABLE IF NOT EXISTS fc_sbc_formations(
  game_version    TEXT NOT NULL REFERENCES game_versions(code),
  challenge_ea_id INTEGER NOT NULL,
  formation       TEXT NOT NULL,           -- '4-2-3-1' 같은 표기. FORMS 키와 맞춘다
  source TEXT, confidence TEXT, updated TEXT,
  PRIMARY KEY(game_version, challenge_ea_id)
);
