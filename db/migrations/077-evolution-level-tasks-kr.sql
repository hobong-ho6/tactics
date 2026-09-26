-- 077 진화 **단계별 미션**의 한국어 (2026-09-26 사용자 지시 「진화 수행을 위한 각 단계별 미션도
--    수집해서 보여줘」 · migration 076의 이어짐)
--
-- 영문 미션은 이미 `fc_evolutions.levels[].challenges`에 있다(fut.gg). 없던 것은 **한국어**다.
--   futmind: `levels[].objectives[].locales.names.ko`
--   ⭐ 단계 번호가 정확히 맞는다 — futmind `level` == fut.gg `idx`(2026-09-26 대조 확인).
--
-- ⛔ `levels` JSON을 고쳐 쓰지 않는다 — 그건 fut.gg 원문이고 덮으면 출처가 섞인다.
--    ⇒ 한국어만 **별도 컬럼**에 `{단계: [문구…]}`로 담고, 화면이 둘을 병기한다(불변규칙 11).
ALTER TABLE fc_evolutions ADD COLUMN levels_kr TEXT;   -- JSON {"1": ["…"], "2": […]}
