-- 105 진화 로그 상태 판정 정본 뷰 (2026-10-10 사용자 지시 「구조로 정리해줘」 · 불변규칙 13 ②)
--
-- 왜: 무효(is_void) 행을 「진행 중」으로 집는 사고가 **두 번** 났다.
--   ⑴ 2026-10-09 fut_club.py complete — 마조 Batigol 무효 시작 행을 닫으려 했다
--   ⑵ 2026-10-10 fut_club_sync.py 완주 추정 — 같은 무효 행(OVR 73)을 「진행 중」으로 보고했다
--   파이썬 9곳이 저마다 `COALESCE(is_void,0)=0`을 적어 왔고, 빠뜨린 곳에서 터졌다.
-- ⇒ 판정을 뷰 두 개에 두고 읽는 쪽은 뷰만 쓴다. 원본 표를 직접 읽는 SELECT는 게이트 G32가 막는다.
-- ⭐ 화면(JS)의 같은 판정 정본은 site/assets/evorules.js `logState()`다 — 의미를 맞춘다(void · done · progress).
-- ⚠️ 쓰기(INSERT·UPDATE)는 원본 표에 그대로 한다 — 뷰는 읽기 전용이다.
CREATE VIEW v_evo_log AS                       -- 유효 행(무효 제외) = logState ≠ 'void'
  SELECT * FROM fut_evolution_log WHERE COALESCE(is_void, 0) = 0;

CREATE VIEW v_evo_log_open AS                  -- 진행 중 = logState = 'progress'
  SELECT * FROM v_evo_log WHERE completed_at IS NULL;

INSERT INTO _migration_log(run_at, v1_path, note) VALUES
  ('2026-10-10', '105-evo-log-views',
   'v_evo_log·v_evo_log_open 신설 — 진화 로그 무효/진행 중 판정 정본(파이썬 측) · G32가 원본 표 직접 읽기를 막는다 · 사용자 지시 2026-10-10');
