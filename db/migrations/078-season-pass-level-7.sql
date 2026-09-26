-- 078 시즌패스 레벨 0 → 7 (2026-09-26 사용자 보고 「시즌 레벨 7 달성해서 진화 해제했어」)
--
-- 종전 0은 **값이 아니라 보수적 하한**이었다(2026-09-23 notes): 「7 미만」만 확인됐고,
-- 현행 최저 레벨형 진화가 SP 7이라 0으로 둬도 판정 결과가 같았다 — 잘못 열리는 것보다
-- 잘못 잠기는 쪽이 안전하다는 판단이었다.
-- ⇒ 이제 7이 실측으로 확인됐으니 적는다. 이 값이 바뀌면 `Striker Glow Up [SP 7]`의 🔒가 풀린다.
--
-- ⚠️ **프리미엄은 여전히 미구매다**(has_premium_pass=0) — `[SP+ N]` 진화들은 그대로 잠긴다.
--    Shooting Practice[SP+ 28] · Tactical Ascent[SP+ 14] · Winger Glow Up[SP+ 26] · Midfield Polish[SP+ 1].
-- ⚠️ 레벨은 플레이하면 계속 오른다 — 이 값은 **2026-09-26 시점**이고, 더 오르면 다시 적어야
--    그보다 높은 레벨형 진화(Relentless[SP 11] · Creative or Composed?[SP 27])의 판정이 맞는다.
UPDATE fut_accounts
   SET season_pass_level = 7,
       notes = notes || ' [2026-09-26] 시즌패스 레벨 **7 달성**(사용자 보고) — Striker Glow Up [SP 7] 해금 확인. '
               || '⚠️ 프리미엄은 여전히 미구매라 [SP+ N] 진화는 잠긴 채다. '
               || '⚠️ 레벨은 계속 오르므로 SP 11·27짜리 판정을 맞추려면 그때 다시 적어야 한다.'
 WHERE id = 1;
