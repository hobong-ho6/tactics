-- 088 보유 카드의 **임대** 여부·임대 경기 수 (2026-09-28 사용자 지적 「아자르는 임대카드인데 포함되어있어」)
--
-- 왜: GG Club 보유행은 `playerType`('player'|'evolution'|'loan')과 `playerDef.loanDuration`(임대 경기 수)을 준다.
--   수집기가 이걸 버려서 임대 카드가 일반 보유와 똑같이 취급됐고, **TOTW Upgrade 해법에 임대 아자르가 들어갔다**.
--   ⛔ 임대 아이템은 SBC에 낼 수 없다(근거 등급 D — 통설 · 인게임 확인 권장) ⇒ 그 해법은 제출이 안 된다.
-- ⭐ 남은 경기 = loan_games − 경기 기록(gamesPlayed)로 **추정**한다(등급 C 미만 — 실측 대조 전). 컬럼으로는 원값만 둔다.
ALTER TABLE fut_club_players ADD COLUMN is_loan INTEGER;      -- 1=임대 · 0=아님 · NULL=미수집
ALTER TABLE fut_club_players ADD COLUMN loan_games INTEGER;   -- playerDef.loanDuration(임대 총 경기 수)
