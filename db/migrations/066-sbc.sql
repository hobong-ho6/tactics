-- 066 SBC(스쿼드 빌딩 챌린지) 수집 (2026-09-25 사용자 지시 「sbc 정보도 가져오자」)
--
-- 왜: 종전엔 SBC가 `player_card_items.acquisition='SBC'`라는 **꼬리표 한 칸**으로만 있었다
--   (FC27 251장 중 1장). 「그 카드는 SBC로 얻는다」까지만 알고 **SBC 자체**(요구 조건·보상·마감)는
--   원장에 통째로 없었다. ⇒ 보유 카드로 무엇을 달성할 수 있는지 판정할 근거가 없었다.
--
-- 어디서: `https://www.fut.gg/api/fut/sbc/`(세트 목록) + `/sbc/challenge/{eaId}/`(세트+챌린지 상세).
-- ⚠️⚠️ **요구 조건은 사람이 읽는 문장으로만 온다**(`requirementsText`). 구조화된 조건이 아니다.
--   실측(2026-09-25): 16세트 · 77챌린지 · 조건 문장 238개 · **유형 26가지**
--   (Min. Squad Total Chemistry Points / Min. N Players from: X OR Y / Exact Leagues in Squad: N …).
--   ⇒ 원문을 **그대로** 보관한다. 파싱은 판정할 때 하고, 못 읽은 문장은 「판정 불가」로 남긴다.
--   ⛔ 파싱 결과를 원문 대신 저장하지 않는다 — fut.gg가 문구를 바꾸면 되돌릴 수 없다.

CREATE TABLE IF NOT EXISTS fc_sbc_sets(
  game_version TEXT NOT NULL REFERENCES game_versions(code),
  set_ea_id    INTEGER NOT NULL,
  pulled       TEXT NOT NULL,              -- 수집일 — SBC는 기간제라 시점이 정본이다
  name TEXT NOT NULL, slug TEXT, description TEXT,
  category TEXT,                           -- players / upgrades / challenges / foundations …
  end_time TEXT, is_expired INTEGER NOT NULL DEFAULT 0,
  is_repeatable INTEGER, repeatability_mode TEXT, number_of_repeats INTEGER,
  repeat_refresh_text TEXT,
  challenges_count INTEGER,
  awards_text TEXT,                        -- 세트 보상 표기(JSON)
  url TEXT, source TEXT, confidence TEXT,
  PRIMARY KEY(game_version, set_ea_id, pulled)
);

CREATE TABLE IF NOT EXISTS fc_sbc_challenges(
  game_version TEXT NOT NULL REFERENCES game_versions(code),
  set_ea_id       INTEGER NOT NULL,
  challenge_ea_id INTEGER NOT NULL,
  pulled TEXT NOT NULL,
  name TEXT NOT NULL, description TEXT,
  challenge_type TEXT, eligibility_op TEXT,   -- AND / OR — 조건을 어떻게 묶는지
  requirements_text TEXT,                     -- ⭐ fut.gg 원문 배열(JSON) — 판정의 원료
  awards_text TEXT,
  cheapest_price INTEGER,                     -- fut.gg가 계산한 최저 해법 가격(참고용 · 우리 계산 아님)
  source TEXT, confidence TEXT,
  PRIMARY KEY(game_version, challenge_ea_id, pulled)
);
CREATE INDEX IF NOT EXISTS ix_sbc_ch_set ON fc_sbc_challenges(set_ea_id, pulled);
