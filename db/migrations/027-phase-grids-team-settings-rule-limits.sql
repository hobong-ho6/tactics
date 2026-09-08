-- 027 — 2026-09-08 프로젝트 점검 후속(사용자 지시 2·3·5·7번).
--
-- ⑴ [3번] player_matches 국면 분리 그리드: cells_poss/cells_def(+map25_*) — WhoScored 이벤트에서
--     보유 국면(패스·터치·슛)과 수비 국면(수비액션 8종)을 따로 5×5로 센다. 히트맵(map25)은 터치 총합이라
--     공수 국면이 한 장에 섞여 있었다(docs/10 「방법론 한계」 2026-07-02 명시, 이후 미보완).
--     계산은 core.whoscored.phase_cells만 쓴다. 기존 행은 이벤트 원자료가 없어 NULL(결손) — 다음 경기부터.
-- ⑵ [2번] team_match_stats.def_x_v/def_x_o — 수비액션 x 평균(라인 높이 프록시). 라인 높이 실측은 지금까지 0이었다.
-- ⑶ [2번] match_game_setups.rule_note — core.team_settings 규칙과의 일치/편차 기록(G15). 값은
--     scripts/migrate_027_rule_note.py가 채운다(규칙 계산은 SQL로 못 한다).
-- ⑷ [7번] reproduction_limits — FC26 설정 축으로 표현할 수 없는 실축 요소의 정본 목록.
--     docs/11·12·20에 산문으로 흩어져 있던 것을 표로 모아 화면에 「재현 불가 N건」으로 노출한다.
-- ⑸ [5번] 처방 정합 결함 정정 — 게이트 확장(G8·G12)이 잡은 실물:
--     ㉠ match_player_prescriptions 교체 6행이 슬롯 역할군 밖(cm_b2b를 RCB·LM·ST·LAM·RM에) → 그 슬롯의
--        slot_canon_roles 정본 역할로 교체(원래 rationale이 「fit 산출 안 함, 슬롯만 기록」이라 자리표시였다).
--     ㉡ CHE fc26:opt 선발 12명(3-4-2-1 11 + 5-4-1의 RB 귀스토) → RB starter=0.
--     ㉢ CHE fc26:opt:LDM/RDM 4행 — 3-4-2-1에 없는 슬롯(docs/00 「입력 불가 처방」 사고의 잔재) → kind에
--        -deprecated 접미(team_tactic_setups 선례). 값은 보존.
--     ⛔ 위 정정 대상 테이블은 G14 보호 대상이 아니다(편집이 정상 작업인 테이블). 이력은 rationale 덧붙임으로 남긴다.
PRAGMA foreign_keys = ON;
BEGIN;

ALTER TABLE player_matches ADD COLUMN cells_poss TEXT;     -- 보유 국면 5×5 카운트 CSV (core.whoscored.POSS_TYPES)
ALTER TABLE player_matches ADD COLUMN cells_def TEXT;      -- 수비 국면 5×5 카운트 CSV (core.whoscored.DEF_TYPES)
ALTER TABLE player_matches ADD COLUMN map25_poss TEXT;     -- encode(cells_poss)
ALTER TABLE player_matches ADD COLUMN map25_def TEXT;      -- encode(cells_def)
ALTER TABLE player_matches ADD COLUMN phase_source TEXT;   -- 'WhoScored matchId=… 이벤트 n건' — 국면 그리드의 provenance

ALTER TABLE team_match_stats ADD COLUMN def_x_v REAL;      -- 우리 수비액션 x 평균 (자기 공격 방향 0~100)
ALTER TABLE team_match_stats ADD COLUMN def_x_o REAL;      -- 상대 수비액션 x 평균
ALTER TABLE team_match_stats ADD COLUMN def_x_method TEXT; -- core.whoscored.DEF_X_METHOD

ALTER TABLE match_game_setups ADD COLUMN rule_note TEXT;   -- 'RULE' | 'DIVERGE: <사유>' | 'NO-STATS: <결손>'

CREATE TABLE reproduction_limits(
  id INTEGER PRIMARY KEY,
  game_version TEXT NOT NULL REFERENCES game_versions(code),
  regime_id INTEGER REFERENCES regimes(id),       -- NULL = 전 체제 공통
  axis TEXT NOT NULL,                              -- manager_profiles.axis 어휘 (pressing/buildup/formation/…)
  real_feature TEXT NOT NULL,                      -- 실축에서 관측·요구되는 것
  limitation TEXT NOT NULL,                        -- 게임 설정 축에 왜 없는가
  workaround TEXT,                                 -- 근사 수단(있으면)
  source TEXT NOT NULL, confidence TEXT NOT NULL,
  added TEXT NOT NULL
);

INSERT INTO reproduction_limits(game_version,regime_id,axis,real_feature,limitation,workaround,source,confidence,added) VALUES
('FC26',NULL,'role_demands','선수별 위치 성향의 정밀 재현','EA가 FC26에서 역할 구속을 의도적으로 풀었다("less constrained by their Roles") — (역할×포커스)→히트맵 사상에 고칠 수 없는 상한이 있다','적합 Δ0.02~0.05는 노이즈로 취급하고 숙련도 등 이산 근거로 가른다','docs/20 ① · EA Gameplay Deep Dive · obs#91','HIGH (EA 1차)','2026-09-08'),
('FC26',NULL,'pressing','존/맨 마킹 방식과 인계 규칙','FC26 팀 설정에 마킹 방식 축이 없다(수비접근 4종 + 라인 높이뿐)','맨투맨의 실측 서명(전방 볼회수·CB 전진)을 역할·포커스 조합으로 근사(obs#27 창발 방법론)','docs/12 「FC26 구현 함의」 #2 · obs#68','HIGH','2026-09-08'),
('FC26',NULL,'pressing','압박 트리거·카운터프레스 강도','압박 강도·트리거 슬라이더가 없다. Aggressive는 「즉시 카운터프레스+오프사이드 트랩」 묶음이라 분리 조절 불가','수비접근 단계 + 라인 높이로 근사, 카운터프레스 실측이 있을 때만 Aggressive','docs/11 「FC26 구현 함의」 #4 · obs#51','HIGH','2026-09-08'),
('FC26',NULL,'pressing','실측 PPDA 서열의 그대로 재현','Team Press가 수비 진영에서 너프됐다(2026-05-28) — 압박 강도→설정값 사상이 진영별로 비선형. 손실 순서 AVL < CHE < LIV, 크기는 EA 비공개','압박 국면을 상대 진영에 한정하는 프리셋 검토','docs/20 ⑥ · EA The World''s Game Update · obs#91','HIGH (방향) / 크기 미공개','2026-09-08'),
('FC26',NULL,'rotation','주행 부하·일정 밀도에 따른 강도 조절','시즌 누적 피로는 게임에 있으나 전술 설정 축이 아니다','기록만 남기고 재현 대상에서 제외(미결)','docs/11 #5 · docs/12 #3 · obs#56·#73','MEDIUM','2026-09-08'),
('FC26',NULL,'formation','공/수 국면별 포메이션 전환(4-2-3-1↔4-4-2, 3-4-2-1↔3-2-5/5-4-1)','FC26은 국면별 포메이션을 갖지 않는다 — 빌드업 스타일·수비접근이 국면을 대신한다','컴팩트=수비접근×라인×역할·포커스의 창발 속성으로 다룬다(obs#27). 국면 분리 실측(cells_poss/cells_def)으로 역할 선택을 국면별로 검증','docs/10 · obs#27·#153','HIGH','2026-09-08'),
('FC26',NULL,'set_pieces','세트피스 루틴(니어포스트 과부하·기만 러닝·롱스로)','세트피스 설계 축이 없다 — 키커·타깃 지정 수준','키커·세트피스 타깃 지정, 헤더 도착형 선수 배치','manager_profiles set_pieces(regime 1~3) · report 26','HIGH','2026-09-08'),
('FC26',2,'formation','3-4-2-1의 양 윙백','FC26 3-4-2-1의 와이드는 WM 타입이라 윙백 역할(fb_att_wb/fb_inverted)을 선택할 수 없다','5-4-1(FB 슬롯)로 우회하거나 WM 커널 중 전진형 선택 — 처방은 3-4-2-1 유지 중','docs/11 「FC26 구현 함의」 · obs#254','HIGH','2026-09-08'),
('FC26',2,'in_possession','2×10이 둘 다 중앙 하프스페이스에 서는 구조','3-4-2-1의 LAM/RAM은 CAM 타입이라 재현되지만 4-2-3-1 어휘로 옮기면 한 명은 WM 커널(터치라인 질량)로 번진다','3-4-2-1 유지 시 문제 없음. 4-2-3-1 변형 프리셋에서만 손실 — 코사인으로 측정 가능(미계산)','docs/11 #3 · obs#59','MEDIUM','2026-09-08'),
('FC26',3,'buildup','GK를 우회하는 다이렉트 빌드업(시퀀스당 패스 2.98)','GK의 기점 빈도는 역할 라벨에 없다 — Alisson·Mamardashvili 모두 GK Defend가 최적','빌드업 스타일로만 근사(규칙: 롱볼 비율·점유 → core.team_settings)','docs/12 obs#199 · obs#66','MEDIUM-HIGH','2026-09-08'),
('FC26',3,'role_demands','CB·미드필더가 상대 박스까지 따라 올라가는 맨마킹','cb_bpd/Aggressive가 상대 박스까지의 전진을 재현하는지 미검증이며, Team Press 너프(골대에 가까울수록 마킹 느슨)와 정면 충돌','—','docs/12 #5·#6 · obs#69','MEDIUM','2026-09-08'),
('FC26',4,'situational','하프타임·경기 중 포메이션 전환(4-1-4-1 → 4-4-2, 61분 3중 교체)','단일 정적 프리셋은 전·후반 차이를 담지 못한다','경기 전용 프리셋은 주도 국면 기준으로 하나만 기록하고 전환 시각을 rationale에 남긴다','docs/13 · report 21·33 · obs#498·#507','MEDIUM','2026-09-08');

-- ── ⑸㉠ 교체 6행: 슬롯 역할군 밖 자리표시 역할 → slot_canon_roles 정본 ──
UPDATE match_player_prescriptions SET role_id='cb_wideback', focus='Support',
  rationale = rationale || ' [2026-09-08 migration 027] 자리표시 cm_b2b가 RCB 슬롯 역할군(CB) 밖이라 게임에 입력 불가 — slot_canon_roles 정본(3-4-2-1 RCB)으로 교체. fit 미산출은 그대로.'
  WHERE report_id=26 AND player_id=63 AND pos_label='RCB' AND role_id='cm_b2b';
UPDATE match_player_prescriptions SET role_id='wm_wideplm', focus='Build-Up',
  rationale = rationale || ' [2026-09-08 migration 027] 자리표시 cm_b2b가 LM 슬롯 역할군(WM) 밖 — slot_canon_roles 정본(3-4-2-1 LM)으로 교체. fit 미산출은 그대로.'
  WHERE report_id=26 AND player_id=80 AND pos_label='LM' AND role_id='cm_b2b';
UPDATE match_player_prescriptions SET role_id='st_advanced', focus='Support',
  rationale = rationale || ' [2026-09-08 migration 027] 자리표시 cm_b2b가 ST 슬롯 역할군(ST) 밖 — slot_canon_roles 정본 ST로 교체. fit 미산출은 그대로.'
  WHERE report_id IN (27,29) AND pos_label='ST' AND role_id='cm_b2b';
UPDATE match_player_prescriptions SET role_id='cam_playmaker', focus='Roaming',
  rationale = rationale || ' [2026-09-08 migration 027] 자리표시 cm_b2b가 LAM 슬롯 역할군(CAM) 밖 — slot_canon_roles 정본(3-4-2-1 LAM)으로 교체. fit 미산출은 그대로.'
  WHERE report_id=27 AND player_id=97 AND pos_label='LAM' AND role_id='cm_b2b';
UPDATE match_player_prescriptions SET role_id='wm_widemid', focus='Defend',
  rationale = rationale || ' [2026-09-08 migration 027] 자리표시 cm_b2b가 RM 슬롯 역할군(WM) 밖 — slot_canon_roles 정본(4-1-4-1 RM)으로 교체. fit 미산출은 그대로.'
  WHERE report_id=29 AND player_id=154 AND pos_label='RM' AND role_id='cm_b2b';

-- ── ⑸㉡ CHE 선발 12명 → 11명 ──
UPDATE prescriptions SET starter=0,
  rationale = rationale || ' [2026-09-08 migration 027] starter 1→0: RB는 5-4-1 변형 슬롯이고 시즌 정본 인게임 포메이션은 3-4-2-1(FB 슬롯 없음) — 선발 12명이 되어 인게임 XI가 하나로 떨어지지 않았다(G8 확장 검사). 5-4-1 변형용 처방으로 보존.'
  WHERE id=259 AND regime_id=2 AND kind='fc26:opt:RB';

-- ── ⑸㉢ CHE LDM/RDM 4행 — 3-4-2-1에 없는 슬롯 ──
UPDATE prescriptions SET kind = kind || '-deprecated',
  rationale = rationale || ' [2026-09-08 migration 027] kind -deprecated: 3-4-2-1(FC26)에 LDM/RDM 슬롯이 없다(docs/00 「입력 불가 처방」 사고의 잔재 — 정합은 LCM/RCM 행이 담당). 값·근거 보존, 툴·게이트에서 배제.'
  WHERE regime_id=2 AND kind IN ('fc26:opt:LDM','fc26:opt:RDM');

INSERT INTO _migration_log(run_at, v1_path, note) VALUES
 (date('now'), '027-phase-grids-team-settings-rule-limits',
  '2026-09-08 점검 후속: 국면 분리 그리드 컬럼(player_matches.cells_poss/cells_def·map25_*·phase_source) · 라인 프록시(team_match_stats.def_x_v/o) · match_game_setups.rule_note(G15) · reproduction_limits 12행 신설 · 처방 정합 정정(mpp 교체 6행 역할군 정합, CHE RB starter 0, CHE LDM/RDM 4행 -deprecated). 기존 그리드 행은 이벤트 원자료가 없어 국면 컬럼 NULL — 다음 경기부터 채운다.');
COMMIT;
