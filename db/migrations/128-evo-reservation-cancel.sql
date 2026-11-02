-- 128 진화 예약 해제 (2026-11-02 사용자 지시 「각 선수에게 진화를 예약을 걸어놓고(진화는 하지 않고), 다른 진화를 통해 해당 선수가
--   걸어놓은 진화 조건을 넘어서게 되면 알려주도록 … 다른 진화를 예약하거나 시작할 때 알려주면」).
-- 127은 예약 행을 손으로 넣었다 — 이제 화면(fut_club.py evo_reserve)이 걸고 푼다.
-- ⛔ 풀 때 행을 지우지 않는다(불변규칙 2) — `cancelled`에 푼 날을 적는다. 다시 걸면 NULL로 되돌린다.
ALTER TABLE fut_evo_reservations ADD COLUMN cancelled TEXT;
INSERT INTO _migration_log (run_at, v1_path, note) VALUES
 ('2026-11-02', '128-evo-reservation-cancel',
  'fut_evo_reservations.cancelled — 화면에서 예약 걸기/풀기(fut_club.py evo_reserve) · 푼 예약은 행을 남기고 날짜만 적는다 · export는 활성 예약만 낸다');
