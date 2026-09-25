-- 063 정본 포메이션을 DB에 표시한다 (2026-09-25 사용자 지시 「정본 표시를 DB에 두고 통일」)
--
-- 증상: 아틀레티코 화면의 LAM·RAM 후보가 0명이었다.
-- 진짜 원인은 후보 결손이 아니라 **화면이 포메이션을 배열 순서로 골랐다**는 것이다.
--   7개 화면(compare·squad·heatmap·index·report·player…)이 각자
--   `slots.filter(s => s.formation === slots[0].formation)`을 써 왔다.
--   ⇒ 한 regime에 포메이션이 여러 개 등록돼 있으면 **어느 것이 그려질지는 정렬 우연**이다.
--   실측: ATM은 3-4-2-1 / 4-1-4-1 / 4-4-2 셋이 등록돼 있는데 3-4-2-1이 먼저 잡혔다.
--     · 그런데 ATM 실측 정본은 **4-1-4-1**이다(team_tactic_setups 2026-27 measured ·
--       2026-08-20 정정 「Opta formations 4141→442 · 포지션 라벨 DL/DR/ML/MR로 검증」).
--     · `squad_entries.slot_type`(GK·FB·CB·DM·CM·WM·ST)도 **4-1-4-1과 정확히 일치**한다.
--     · 3-4-2-1로 그리면 LAM/RAM이 0명이 되고 **FB 5명·DM 4명이 화면에서 통째로 사라진다**
--       (그 slot_type을 가진 슬롯이 3-4-2-1에 없기 때문 — 조용히 사라져서 아무도 몰랐다).
--
-- ⛔ 「배열 순서를 조심하자」로 막지 않는다 — 읽는 사람이 있어야 작동한다(CLAUDE.md 불변규칙 13).
--   ⇒ ① **정본을 DB에 적고**(여기) ② 화면은 `data.js`의 한 함수만 부르게 하고(단일 정본)
--     ③ 게이트가 「정본 1개인가 · 정본 슬롯에 빈 칸이 있는가」를 막는다.
-- ⚠️ 어느 포메이션이 정본인가는 **사람 판단**이다 — 그래서 값으로 적고 스크립트가 고르지 않는다.

ALTER TABLE slots ADD COLUMN is_canon INTEGER NOT NULL DEFAULT 0;   -- 1 = 이 regime의 정본 포메이션

-- 정본 지정 (2026-09-25 현재)
--   AVL 4-2-3-1 Wide  — 시즌 내 불변이 실측으로 확인됨(manager_profiles formation)
--   CHE 3-4-2-1       — 현 화면과 동일(후보 풀이 이 포메이션에 맞춰 등록돼 있다)
--   LIV 4-2-3-1 Wide  — 등록된 포메이션이 하나뿐이다
--   ATM 4-1-4-1       — 2026-08-20 Opta 검증으로 3-4-2-1에서 정정된 값(위 주석)
UPDATE slots SET is_canon = 1 WHERE regime_id = 1 AND formation = '4-2-3-1 Wide';
UPDATE slots SET is_canon = 1 WHERE regime_id = 2 AND formation = '3-4-2-1';
UPDATE slots SET is_canon = 1 WHERE regime_id = 3 AND formation = '4-2-3-1 Wide';
UPDATE slots SET is_canon = 1 WHERE regime_id = 4 AND formation = '4-1-4-1';
