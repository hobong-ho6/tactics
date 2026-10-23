-- 122 진화 해금 문구 보충 표 (2026-10-22 사용자 지적 「이 진화 같은 경우 챔스토큰으로 획득할 수 있는 것 같은데
--   각 진화의 획득 조건이 잘 안 보여 — 획득 조건을 별도 카드 영역으로」).
--
-- 왜: fut.gg 진화 객체는 해금 경로를 sbcName·objectiveGroupName·customUnlockable·eventTokenId로 주는데,
--   Composed Stopper(2606)는 전부 null · coins/points/token 0 이라 우리 화면에 「무료」로 떴다.
--   그런데 ⑴ futmind(EA 진화 랩 노출 목록)에 없다 — 이 목록에 없는 현행 진화는 이것 말고 전부 시즌패스·과제·배지(해금형)다.
--   ⑵ 생성 시각 2026-10-22T07:00:28Z가 fut.gg 토큰 스토어 「S2 Champs EVO Token」(챔피언스 토큰 125 · item 387 · eaId 20311)
--      판매 시작 2026-10-22T07:00:00Z와 같다. 그 상품은 evolutionId가 null이라 **연결은 fut.gg가 주지 않는다**.
--   ⇒ 근거 등급 C(정황 2개 · 1차 확인 없음). 인게임에서 확인되면 confidence를 올리고, 틀리면 행을 무효로 둔다(지우지 않는다).
-- 쓰기: 손으로 행을 넣는다(수집기가 만들지 않는다 — fut.gg가 이 연결을 주지 않으므로).
-- 읽기: core/export.py 가 catalog.unlock_text = COALESCE(fut.gg 값, 이 표) 로 합치고 unlock_src·unlock_conf를 붙인다.
--   화면 판정은 site/assets/evorules.js unlockCond·acquireRoute 한 곳(잠김 칩·「획득 조건」 상자·무료 분류가 같이 따라온다).
CREATE TABLE IF NOT EXISTS fc_evolution_unlock_supplement (
  game_version TEXT NOT NULL,
  evo_id       INTEGER NOT NULL,
  unlock_text  TEXT NOT NULL,          -- fut.gg·EA와 같은 영문 문형(evorules.js가 그 문형으로 판정한다)
  source       TEXT NOT NULL,
  confidence   TEXT NOT NULL,
  is_void      INTEGER NOT NULL DEFAULT 0,
  added        TEXT NOT NULL,
  PRIMARY KEY (game_version, evo_id)
);
INSERT OR IGNORE INTO fc_evolution_unlock_supplement (game_version, evo_id, unlock_text, source, confidence, added) VALUES
 ('FC27', 2606, 'Unlocked via the Token Store for 125 tokens',
  'fut.gg /token-store/ (2026-10-23 열람) 「S2 Champs EVO Token」 Champions Token 125 · 2026-10-22T07:00Z~12-03 · 구매 한도 1 — 진화 생성 시각(2026-10-22T07:00:28Z)과 일치 · futmind 진화 랩 목록에 없음(해금형 정황) · 사용자 지적(챔스 토큰)',
  'C — 정황 2개(판매 시작 시각 일치 · 진화 랩 목록 부재) + 사용자 관찰. fut.gg 상품의 evolutionId가 null이라 1차 연결 확인 없음',
  '2026-10-23');
INSERT INTO _migration_log (run_at, v1_path, note) VALUES
 ('2026-10-23', '122-evo-unlock-supplement',
  'fc_evolution_unlock_supplement 신설 — fut.gg가 비워 둔 해금 경로 보충(Composed Stopper 2606 = 챔피언스 토큰 125 · 등급 C) · export가 catalog.unlock_text에 합침 · 화면 「획득 조건」 상자');
