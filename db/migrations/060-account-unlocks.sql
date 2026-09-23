-- 060 진화 해금 상태 (2026-09-23 사용자 지적 「여전히 적용할 진화가 없는데 선수들이 노출되고 있음」)
--
-- 왜: 진화는 **소진**과 **해금**이 서로 다른 축인데 우리는 소진만 보고 있었다.
--   `fc_evolutions.unlock_text`를 보면 잠금이 세 종류다:
--     ⑴ `Unlocked by reaching level N in the Premium Season Pass.`  — 프리미엄 구매 + 레벨 N
--     ⑵ `Unlocked by reaching level N in the Standard Season Pass.` — 레벨 N (구매 불필요)
--     ⑶ `Ted Lasso's Masterclass` · `Pep's Domination` 같은 **목표(objective) 완료**
--   종전엔 ⑴만 필터가 있었다 ⇒ ⑵⑶이 「지금 걸 수 있는 진화」로 모든 선수에게 붙었다
--   (실측: Relentless [SP 11] · Creative or Composed? [SP 27] · Pinged Pass가 AVL 전원에게 노출).
--
-- ⛔ 해금 여부는 **계정의 상태**라 fut.gg가 알려주지 않는다 — 사용자가 기록한다.
-- ⛔ 「모름(NULL)」과 「해금 안 됨」을 구분한다(obs#132) — 모르면 숨기되 **건수를 적고** 토글로 편다.
ALTER TABLE fut_accounts ADD COLUMN season_pass_level INTEGER;   -- 표준/프리미엄 공통 진행 레벨. NULL=모름
ALTER TABLE fut_accounts ADD COLUMN has_premium_pass INTEGER;    -- 1=구매함 0=아님 NULL=모름
ALTER TABLE fut_accounts ADD COLUMN unlocks_checked TEXT;        -- 위 두 값을 마지막으로 확인한 날

-- 목표형(⑶) 해금은 레벨로 계산되지 않는다 — 진화 단위로 기록한다.
CREATE TABLE IF NOT EXISTS fut_evolution_unlocks(
  account_id INTEGER NOT NULL REFERENCES fut_accounts(id),
  evo_id     INTEGER NOT NULL,
  unlocked   INTEGER NOT NULL DEFAULT 1,   -- 1=해금됨 0=명시적으로 아직 아님
  noted      TEXT,                          -- 확인한 날
  note       TEXT,
  PRIMARY KEY (account_id, evo_id)
);
