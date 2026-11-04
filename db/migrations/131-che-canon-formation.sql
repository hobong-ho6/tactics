-- 131 CHE 정본 포메이션 표시를 4-2-3-1 Wide로 옮긴다 (2026-11-04 사용자 「첼시 팀전술은 여전히 3421인데?」).
--
-- 왜: 같은 날 CHE 시즌 정본을 4-2-3-1 Wide로 바꿨다(team_tactic_setups optimal 신설 · 커밋 877c2593). 그런데 화면이 자리 배치를 읽는
--   slots.is_canon(migration 063)은 3-4-2-1에 남아, 팀 전술 화면이 「설정 줄 4-2-3-1 · 경기장·표 3-4-2-1 자리」로 섞여 그려졌다.
--   ⇒ 정본 포메이션이 두 곳(team_tactic_setups optimal · slots.is_canon)에 있던 구조다. 이번에 G24 ⑸가 둘의 일치를 강제한다.
-- 어떻게: 표시만 옮긴다(3-4-2-1 칸은 지우지 않는다 — 대안 포메이션으로 남는다 · 불변규칙 2).
UPDATE slots SET is_canon = 0 WHERE regime_id = (SELECT id FROM regimes WHERE team_code='CHE');
UPDATE slots SET is_canon = 1 WHERE regime_id = (SELECT id FROM regimes WHERE team_code='CHE') AND formation = '4-2-3-1 Wide';
INSERT INTO _migration_log (run_at, v1_path, note) VALUES
 ('2026-11-04', '131-che-canon-formation',
  'CHE slots.is_canon 3-4-2-1 → 4-2-3-1 Wide(시즌 정본 optimal과 일치) · G24 ⑸ 신설 — 정본 표시 포메이션 = 현행 버전 optimal 포메이션');
