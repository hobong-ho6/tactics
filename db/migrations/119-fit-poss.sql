-- 119 경기 프리셋 선발의 **보유/비보유 분리 그리드 적합** (2026-10-22 경기 데이터 결손 검토 §2 「커널 fit 무결정 25/44 — 입력이 합산 map25 한 장」 · §5 #5).
--
-- 왜: match_player_prescriptions.fit_sim은 SofaScore 합산 히트맵(map25)과 역할 커널의 코사인이라 보유·비보유 위치가 섞인다.
--   WhoScored 국면 분리 그리드(player_matches.map25_poss/map25_def)가 이미 있는데 fit에 안 썼다 — 수집이 아니라 활용 결손.
-- 무엇: 같은 커널(core.kernel.Kernel)·같은 슬롯 x로 보유 그리드 fit(fit_sim_poss)·비보유 그리드 fit(fit_sim_def)을 병기한다.
--   alt_role_poss = 보유 그리드 1위 조합(기록 역할과 다르면 그것 · 같으면 2위) · fit_delta_poss = 보유 그리드 1·2위 격차.
--   ⛔ 역할 결정(role_id/focus)은 바꾸지 않는다 — 숫자만 병기(사용자 판단 축). 적재는 scripts/load_fit_poss.py.
ALTER TABLE match_player_prescriptions ADD COLUMN fit_sim_poss REAL;
ALTER TABLE match_player_prescriptions ADD COLUMN fit_sim_def REAL;
ALTER TABLE match_player_prescriptions ADD COLUMN alt_role_poss TEXT;
ALTER TABLE match_player_prescriptions ADD COLUMN fit_delta_poss REAL;
INSERT INTO _migration_log (run_at, v1_path, note) VALUES
 ('2026-10-22', '119-fit-poss',
  'match_player_prescriptions.fit_sim_poss·fit_sim_def·alt_role_poss·fit_delta_poss — 보유/비보유 분리 그리드(map25_poss/def) 커널 적합 병기 · core.kernel.Kernel.fit_split · scripts/load_fit_poss.py · 역할 결정 불변');
