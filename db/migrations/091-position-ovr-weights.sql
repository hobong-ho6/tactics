-- 091 포지션별 OVR 산정식 가중치 (2026-10-02 사용자 지시 「진화를 수행하지 않은 카드로 각 포지션별 오버롤 산정식을 추정해보자」)
--
-- 왜: 진화 중에는 세부 스탯과 별개로 **OVR 자체를 올려 주는** 보상(`overall +N (^cap)`)이 있다.
--   그 OVR이 세부 스탯으로 뒷받침되지 않으면 카드가 「표기만 높은」 상태가 된다
--   (실측: 바르가스 반복 배급 — EA OVR +6 · 세부 스탯 기준 +1.3).
--   ⇒ 세부 스탯 → OVR 산정식을 가져야 「진화 OVR Δ」와 「계산 OVR Δ」를 견줄 수 있다.
-- ⛔ EA는 산정식을 공개하지 않는다. 커뮤니티 표(FIFA 19 기준 · 등급 D)는 FC27 일반 카드 383장에서
--   정확 일치 32%였다(풀백·윙어 0%) ⇒ **FC27 비진화·비특별 카드로 직접 적합**한다(등급 C).
-- 행 단위: (버전, 포지션 그룹, 속성) 하나 = 정수 % 가중 하나. 회차(`fitted`)마다 행을 **추가**한다(불변규칙 2).
CREATE TABLE fc_position_ovr_weights(
  game_version TEXT NOT NULL REFERENCES game_versions(code),
  pos_group    TEXT NOT NULL,          -- GK·CB·FB·CDM·CM·CAM·WM·WF·ST (포지션→그룹은 core/position_ovr.py)
  attr         TEXT NOT NULL,          -- 29속성 한국어 키(core/futgg_attrs.ATTR_KR 값)
  weight_pct   INTEGER NOT NULL,       -- 정수 %. 그룹 합 = 100
  fitted       TEXT NOT NULL,          -- 적합 회차(날짜)
  sample_n     INTEGER,                -- 그 그룹 표본 수
  test_n       INTEGER,                -- 시험셋(적합에 안 쓴 30%) 수
  test_exact   INTEGER,                -- 시험셋 정확 일치 수
  test_within1 INTEGER,                -- 시험셋 ±1 이내 수
  source TEXT, confidence TEXT,
  PRIMARY KEY(game_version, pos_group, attr, fitted)
);
