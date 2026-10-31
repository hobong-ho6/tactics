-- 127 진화 예약 (2026-11-01 사용자 지시 「시세 다른 진화할 때 공포의 벽 진화 조건을 넘어서면 경고해줘 알림창이 됐든 내가 알수 있도록」).
--
-- 왜: 진화 요구조건(OVR·PS·PAC 상한 등)은 **시작 시점**에 검사된다 — 해금만 해 두고 아껴 둔 진화가 있는데
--   그 선수에게 다른 진화를 먼저 걸면 조건을 넘어 영구히 못 쓰게 된다(런북 「추천할 때」 ⑥ 순서 함정).
--   종전엔 문서 경고뿐이라 화면이 막지 않았다 ⇒ 「누구에게 무엇을 아껴 뒀나」를 행으로 두고 화면이 판정한다.
-- 활성 = 그 선수의 보유 카드에 이 진화 로그(무효 아님)가 아직 없고 · 진화가 만료되지 않았다. 적용하면 저절로 풀린다(행은 지우지 않는다).
-- 판정 정본은 site/evolutions.html `TREQ`(요구조건) + `tryRun`(진화 적용 후 상태) — 파이썬 재구현 없음.
CREATE TABLE fut_evo_reservations (
  account_id INTEGER NOT NULL REFERENCES fut_accounts(id),
  evo_id     INTEGER NOT NULL,              -- fc_evolutions.evo_id (fut.gg id)
  player_id  INTEGER NOT NULL REFERENCES players(id),
  noted      TEXT NOT NULL,                 -- 예약한 날
  note       TEXT,
  PRIMARY KEY (account_id, evo_id, player_id)
);
INSERT INTO fut_evo_reservations VALUES
 (1, 2622, 57, '2026-11-01', 'The Haunted Wall(공포의 벽) → 시세 예약 — 사용자 「우선 공포의 벽은 해금했어 좀 지켜보다가 나중에 업글할께」 · 「시세 다른 진화할 때 공포의 벽 진화 조건을 넘어서면 경고해줘」(2026-11-01) · 조건 OVR ≤81 · PS ≤7 · PAC ≤85 · 지금 OVR 78 · PS 1 · PAC 69');
INSERT INTO _migration_log (run_at, v1_path, note) VALUES
 ('2026-11-01', '127-evo-reservations',
  'fut_evo_reservations — 해금해 두고 아껴 둔 진화(선수 지정) · 다른 진화가 그 조건을 깨면 진화 화면이 카드·걸어보기·시작/완료 확인창에서 경고 · 첫 행 시세 × The Haunted Wall(2622)');
