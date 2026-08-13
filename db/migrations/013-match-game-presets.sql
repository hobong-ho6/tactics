-- 특정 경기만 FC에서 재현하는 프리셋. 시즌/감독 정본 처방과 완전히 분리한다.
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS match_game_setups(
  report_id INTEGER PRIMARY KEY REFERENCES match_reports(id) ON DELETE CASCADE,
  game_version TEXT NOT NULL REFERENCES game_versions(code),
  formation TEXT NOT NULL,
  build_up_style TEXT NOT NULL,
  defensive_approach TEXT NOT NULL,
  line_height INTEGER NOT NULL CHECK(line_height BETWEEN 0 AND 100),
  tactic_code TEXT,
  match_only INTEGER NOT NULL DEFAULT 1 CHECK(match_only=1),
  rationale TEXT NOT NULL,
  source TEXT NOT NULL,
  confidence TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS match_player_prescriptions(
  report_id INTEGER NOT NULL REFERENCES match_reports(id) ON DELETE CASCADE,
  player_id INTEGER NOT NULL REFERENCES players(id),
  game_version TEXT NOT NULL,
  pos_label TEXT NOT NULL,
  role_id TEXT NOT NULL,
  focus TEXT NOT NULL,
  fit_sim REAL,
  starter INTEGER NOT NULL DEFAULT 1,
  sort_order INTEGER,
  rationale TEXT NOT NULL,
  source TEXT NOT NULL,
  confidence TEXT NOT NULL,
  PRIMARY KEY(report_id,player_id),
  FOREIGN KEY(game_version,role_id,focus)
    REFERENCES game_role_focus(game_version,role_id,focus)
);

INSERT OR IGNORE INTO match_game_setups VALUES(
  1,'FC26','4-2-3-1 Wide','Counter','Balanced',45,NULL,1,
  'PSG전 한 경기 재현용. 낮은 점유에서 탈취 직후 적은 패스로 Madjo와 우측 McGinn을 찾은 직접 전환은 Counter에 대응한다. 중앙을 좁게 보호한 4-2-3-1/일시적 5-4-1과 스코어에 따른 라인 상승을 하나의 정적 설정으로 근사하기 위해 Balanced·45를 채택했다. 0-0과 1-2의 라인 높이 차이는 이 단일 프리셋이 완전히 담지 못한다.',
  'SofaScore event 16260286; match_reports.id=1; El País·AS 경기 분석; Emery 경기 후 기자회견',
  'MEDIUM — 선수 역할은 단일 경기 실측 커널, 팀 설정은 90분 지배적 패턴의 게임 번역. 실제 게임 내 tactic_code 미검증'
);

INSERT OR IGNORE INTO match_player_prescriptions VALUES
(1,19,'FC26','GK','gk_goalkeeper','Defend',0.966,1,1,'PSG전 실제 히트맵의 슬롯 제한 argmax. 후방 패스 옵션과 라인 수비를 재현.','SofaScore event 16260286 player heatmap/statistics','HIGH 실측 / MEDIUM 게임 번역 — 단일 경기'),
(1,6,'FC26','LB','fb_wingback','Balanced',0.759,1,2,'좌측 폭·전진과 긴 회복 수비를 함께 재현.','SofaScore event 16260286 player heatmap/statistics','HIGH 실측 / MEDIUM 게임 번역 — 단일 경기'),
(1,4,'FC26','LCB','cb_bpd','Build-Up',0.798,1,3,'좌측 전진 배급과 중앙 보호를 재현.','SofaScore event 16260286 player heatmap/statistics','HIGH 실측 / MEDIUM 게임 번역 — 단일 경기'),
(1,7,'FC26','RCB','cb_bpd','Aggressive',0.895,1,4,'좁은 중앙 보호와 간결한 전진 연결을 재현.','SofaScore event 16260286 player heatmap/statistics','HIGH 실측 / MEDIUM 게임 번역 — 단일 경기'),
(1,2,'FC26','RB','fb_wingback','Balanced',0.907,1,5,'우측 폭 유지와 회복 수비를 재현.','SofaScore event 16260286 player heatmap/statistics','HIGH 실측 / MEDIUM 게임 번역 — 단일 경기'),
(1,56,'FC26','LDM','dm_holding','Roaming',0.679,1,6,'좌측 피벗의 경합·전진 압박과 이동 범위를 재현.','SofaScore event 16260286 player heatmap/statistics','HIGH 실측 / MEDIUM 게임 번역 — 단일 경기'),
(1,12,'FC26','RDM','dm_holding','Ball-Winning',0.788,1,7,'우측 피벗의 중앙 스크린·차단을 재현.','SofaScore event 16260286 player heatmap/statistics','HIGH 실측 / MEDIUM 게임 번역 — 단일 경기'),
(1,30,'FC26','LM','wm_widemid','Support',0.788,1,8,'LAM 표기와 달리 왼쪽 안쪽·낮은 지원/압박 분포를 재현.','SofaScore event 16260286 player heatmap/statistics; Emery 발언','HIGH 실측 / MEDIUM 게임 번역 — 단일 경기'),
(1,14,'FC26','CAM','cam_playmaker','Roaming',0.623,1,9,'명목 CAM에서 낮게 내려온 중앙 연결자 움직임을 재현.','SofaScore event 16260286 player heatmap/statistics','HIGH 실측 / MEDIUM 게임 번역 — 단일 경기'),
(1,10,'FC26','RM','wm_winger','Attack',0.882,1,10,'RAM의 강한 우측 편향·전방 공급과 압박을 재현.','SofaScore event 16260286 player heatmap/statistics','HIGH 실측 / HIGH 게임 번역 — 단일 경기'),
(1,61,'FC26','ST','st_poacher','Attack',0.725,1,11,'등진 연결 시도보다 최종 위치의 반복 박스 침투와 슈팅 분포를 우선 재현.','SofaScore event 16260286 player heatmap/statistics; Emery 발언','HIGH 실측 / MEDIUM 게임 번역 — 단일 경기');

INSERT OR IGNORE INTO _migration_log VALUES('013-match-game-presets','2026-08-13',
  '경기 전용 FC 팀 설정과 선수 역할·포커스를 시즌 정본과 분리해 저장');
