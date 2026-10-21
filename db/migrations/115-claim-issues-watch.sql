-- 115 판정 쟁점 「감시(watch)」 단계 — 정본 유지(HELD) 판정도 다시 뜨게 (2026-10-21 사용자 「보류 판정도 이후에
--     업데이트 되는거야?」 → 「제안대로 변경」).
--
-- 왜: HELD 185건 전부 「재판정 조건」이 verdict_note 산문에만 있었다 — PENDING 165건이 쌓였던 것과 같은 구조다(migration 114).
--   쟁점을 HELD로 닫으면 그대로 끝나 재판정 조건이 와도 아무것도 뜨지 않았다.
-- 구조: 쟁점에 단계(phase)를 둔다 — decide(판정 대기: 묶인 주장 PENDING) → HELD로 판정하면 watch(감시: 묶인 주장 HELD ·
--   트리거 = 재판정 조건)로 남는다. 트리거가 차면 「재판정할 차례」 → 다시 HELD+새 트리거(계속 감시) / APPLIED·REJECTED(종결) /
--   HELD --final(재판정 조건 없음 · 사유 필수 · 종결). armed = 지금 트리거를 건 날(기한 7일은 max(찬 날, armed)부터).
-- 화면 라벨: HELD는 「보류」가 아니라 「유지」(판정 완료 — 미룬 게 아니다).
ALTER TABLE claim_issues ADD COLUMN phase TEXT NOT NULL DEFAULT 'decide' CHECK(phase IN ('decide','watch'));
ALTER TABLE claim_issues ADD COLUMN armed TEXT;
UPDATE claim_issues SET armed = created WHERE armed IS NULL;
INSERT INTO _migration_log (run_at, v1_path, note) VALUES
 ('2026-10-21', '115-claim-issues-watch',
  'claim_issues.phase(decide|watch)·armed — HELD 판정을 재판정 트리거가 걸린 감시 쟁점으로 · G39가 쟁점 없는 HELD·빈 감시 쟁점·재판정 기한 초과를 막는다 · 화면 HELD 라벨 「유지」');
