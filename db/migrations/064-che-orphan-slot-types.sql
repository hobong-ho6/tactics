-- 064 첼시에서 화면에 안 잡히던 squad_entries 7행 정리 (2026-09-25 사용자 지시
--    「첼시 숨은 7명도 정리해줘 — 윙백은 WM, 헨더슨 CM, W 4명은 CAM」)
--
-- 배경: G24(migration 063)가 「정본 포메이션(3-4-2-1)에 없는 slot_type을 가진 행」 7건을 잡았다.
--   그 slot_type을 가진 슬롯이 없으면 `v_slot_candidates`가 조인에서 떨어뜨려 **화면에서 통째로 사라진다**.
--
-- ⭐ 조사해 보니 「숨은 7명」은 **7행이지 7명이 아니었다**. 6명은 이미 유효한 행을 따로 갖고 있었고
--   고아 행이 하나씩 더 있었다. **실제로 아무 데도 안 보이던 사람은 조던 헨더슨 한 명**이다.
-- ⭐ 그리고 `W`는 `WM`의 중복 표기가 아니라 **별개 커널 역할군**(윙어 `w_*` ↔ 와이드미드 `wm_*`)이다.
--   에스테방·페드루 네투는 두 행의 **map25 그리드 자체가 다르다** — 그래서 일괄 변환하지 않고 둘로 갈랐다.
--
-- ⑴ 갈 곳이 비어 있는 행 → slot_type을 옮긴다(정보가 늘어난다)
--    · 조던 헨더슨  DM/RDM → CM/RCM   (유일한 행이었다. 좌우 정보 보존 위해 RDM→RCM)
--    · 에스테방     W/RW   → CAM/RAM  (CAM 행이 없었다 · 그리드도 WM 행과 다르다)
--    · 페드루 네투  W/RW   → CAM/RAM  (CAM 행이 없었다 · 그리드도 WM 행과 다르다)
--
-- ⑵ 갈 곳에 **이미 같은 (선수, 자리)** 행이 있는 경우 → 옮기면 후보가 두 번 뜬다.
--    ⇒ 살아남는 행에 **없는 값만 채워 넣고**(rate_v 등) 고아 행은 지운다.
--    · 말로 귀스토 FB    ↔ 이미 WM/RM 있음  — FB 행에만 있던 rate_v 6.84를 WM 행으로 옮긴다
--    · 차바리아    FB    ↔ 이미 WM/LM 있음  — FB 행에만 있던 rate_v 6.8을 WM 행으로 옮긴다
--    · 로저스      W/LW  ↔ 이미 CAM/LAM 있음 — CAM 행이 rate 7.4로 더 갖춰져 있다(옮길 값 없음)
--    · 콜 파머     W/RW  ↔ 이미 CAM/RAM 있음 — CAM 행이 rate 6.95로 더 갖춰져 있다(옮길 값 없음)
--    ⚠️ 지우는 4행의 내용은 위에 그대로 적어 뒀다 — 사실을 잃지 않기 위한 기록이다.

-- ⑴ 이동
UPDATE squad_entries SET slot_type='CM',  pos_only='RCM' WHERE id=138;   -- 조던 헨더슨
UPDATE squad_entries SET slot_type='CAM', pos_only='RAM' WHERE id=73;    -- 에스테방
UPDATE squad_entries SET slot_type='CAM', pos_only='RAM' WHERE id=72;    -- 페드루 네투

-- ⑵ 병합 후 제거 — 살아남는 행이 비어 있을 때만 채운다(⛔ 있는 값을 덮지 않는다)
UPDATE squad_entries SET rate_v      = (SELECT rate_v      FROM squad_entries o WHERE o.id=24),
                         rate_basis  = COALESCE(rate_basis,  (SELECT rate_basis  FROM squad_entries o WHERE o.id=24)),
                         rate_note   = COALESCE(rate_note,   (SELECT rate_note   FROM squad_entries o WHERE o.id=24))
 WHERE id=71 AND rate_v IS NULL;                                          -- 말로 귀스토 WM/RM
UPDATE squad_entries SET rate_v      = (SELECT rate_v      FROM squad_entries o WHERE o.id=63),
                         rate_basis  = COALESCE(rate_basis,  (SELECT rate_basis  FROM squad_entries o WHERE o.id=63)),
                         rate_note   = COALESCE(rate_note,   (SELECT rate_note   FROM squad_entries o WHERE o.id=63))
 WHERE id=70 AND rate_v IS NULL;                                          -- 차바리아 WM/LM

DELETE FROM squad_entries WHERE id IN (24, 63, 74, 75);
