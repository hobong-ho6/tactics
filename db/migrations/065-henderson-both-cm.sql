-- 065 조던 헨더슨을 양쪽 CM 후보로 (2026-09-25 사용자 지시 「헨더슨 pos_only 비워서 양쪽 CM 다 되게 해줘」)
--
-- 064에서 DM/RDM → CM/RCM으로 옮길 때 **원래 행의 좌우 정보(RDM)를 보존**하려고 RCM으로 넣었는데,
-- 사용자 판단은 「좌우를 가르지 않는다」다. `pos_only`를 비우면 slot_type의 모든 pos에 노출된다
-- (v_slot_candidates: `WHERE se.pos_only IS NULL OR se.pos_only = sl.pos`).
-- ⭐ 같은 regime의 라비아가 이미 NULL이라 관행과도 맞는다.
UPDATE squad_entries SET pos_only = NULL WHERE id = 138;
