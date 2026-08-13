-- 경기 수집 결과를 전술·선수 분석과 게임 구현 판단까지 연결한다.
-- 원천 스탯은 matches/player_matches/team_match_stats에 남고,
-- 이 두 표는 경기별 해석과 보고서 메타데이터만 담당한다.
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS match_reports(
  id INTEGER PRIMARY KEY,
  event_id INTEGER NOT NULL,
  match_id INTEGER REFERENCES matches(id),
  regime_id INTEGER NOT NULL REFERENCES regimes(id),
  team_code TEXT NOT NULL REFERENCES teams(code),
  season TEXT REFERENCES seasons(code),
  report_date TEXT NOT NULL,
  title TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'draft' CHECK(status IN ('draft','complete')),
  tactical_description TEXT NOT NULL,
  tactical_features TEXT NOT NULL,
  tactical_changes TEXT NOT NULL,
  game_implications TEXT NOT NULL,
  report_path TEXT NOT NULL,
  source TEXT NOT NULL,
  confidence TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  UNIQUE(team_code,event_id)
);

CREATE TABLE IF NOT EXISTS match_player_reports(
  report_id INTEGER NOT NULL REFERENCES match_reports(id) ON DELETE CASCADE,
  player_id INTEGER NOT NULL REFERENCES players(id),
  position TEXT NOT NULL,
  tactical_role TEXT NOT NULL,
  characteristics TEXT NOT NULL,
  performance TEXT NOT NULL,
  game_implication TEXT NOT NULL,
  source TEXT NOT NULL,
  confidence TEXT NOT NULL,
  PRIMARY KEY(report_id,player_id)
);

-- 2026-08-12 슈퍼컵 심화 리포트를 새 구조의 첫 기준본으로 등록한다.
INSERT OR IGNORE INTO match_reports(
  id,event_id,match_id,regime_id,team_code,season,report_date,title,status,
  tactical_description,tactical_features,tactical_changes,game_implications,
  report_path,source,confidence,created_at,updated_at
) VALUES(
  1,16260286,68,1,'AVL','2026-27','2026-08-13',
  '2026-08-12 UEFA Super Cup — PSG 2-1 Aston Villa','complete',
  '명목 4-2-3-1에서 중앙을 좁게 보호하고 전방 압박 뒤 짧고 직접적으로 전환했다. McGinn이 자연 우측 윙어 대신 RAM 창출자, Madjo가 등진 연결과 박스 침투를 겸한 9번을 맡았다.',
  '비소유 때 중앙 컴팩트함과 센터백 압박|좌 Maatsen 전진·우 McGinn 공급의 비대칭|Kamara-Gomes 더블 피벗의 스크린·경합 분업|Madjo를 향한 직접 전환과 세 공격형 미드필더의 유동성',
  '0-0에는 중앙 보호와 전방 압박|0-1 열세 뒤 직접 전환과 우측 공급 강화|1-1 뒤 PSG 교체에 밀려 후방 공간 노출|1-2 열세에는 라인과 압박을 올려 박스 접근과 전환 위험이 함께 증가',
  'McGinn의 RM 임시 해법은 기능했지만 전문 우측 자원 결손을 해소하지 않는다|Hemmings는 LM 와이드 미드필더 Support 후보, Madjo는 포처 Attack 후보로 추적하되 단일 경기라 대표 처방은 유지|Kamara-Gomes 역할 분업과 Maatsen의 왕복 임무는 후속 공식전 표본으로 재검증',
  'reports/match-watch/2026-08-12-avl-psg-super-cup.md',
  'SofaScore event 16260286; Emery 경기 후 기자회견; El País; AS; UEFA; 경기 분석 영상·팟캐스트',
  'HIGH 원천 스탯·평균 위치·히트맵 / MEDIUM 전술 해석 — 공식전 단일 표본',
  '2026-08-13','2026-08-13'
);

INSERT OR IGNORE INTO match_player_reports VALUES
(1,19,'GK','후방 패스 옵션과 라인 수비 골키퍼','4선방과 짧은 배급으로 압박 탈출의 첫 연결점','4선방, 패스 23/30, 40터치, 10회수. 두 실점의 개인 책임은 영상 근거 부족','단일 경기 최근접 gk_goalkeeper/Defend .966; 대표 처방 변경 없음','SofaScore event 16260286; 경기 리포트','HIGH 스탯 / MEDIUM 역할'),
(1,2,'RB','우측 폭 유지와 회복 수비','전진보다 측면 균형과 마지막 선 복귀가 중심','32/42패스, 2/4경합, 2태클, 5클리어, 1키패스. 두 득점 장면의 간격 판단은 약점','fb_wingback/Balanced .907 지지; 공격형 포커스로 상향하지 않음','SofaScore event 16260286; 경기 리포트','HIGH 스탯 / MEDIUM 역할'),
(1,7,'RCB','좁은 중앙 보호와 안정 배급','위험 패스보다 라인 유지·간결한 연결','39/41패스, 1인터셉트, 2클리어, 8회수','cb_bpd/Aggressive .895 참고; 단일 경기라 대표 역할 유지','SofaScore event 16260286; 경기 리포트','HIGH 스탯 / MEDIUM 역할'),
(1,4,'LCB','좌측 전진 배급 센터백','왼쪽 빌드업 출구와 중앙 보호를 병행','23/26패스, 3/6경합, 2태클, 3클리어','cb_bpd/Build-Up .798이 기존 임무를 지지','SofaScore event 16260286; 경기 리포트','HIGH 스탯 / MEDIUM 역할'),
(1,6,'LB','좌측 폭·전진과 긴 회복 수비','팀의 가장 선명한 전진 폭 제공자이자 왕복 자원','27/35패스, 11/16경합, 4태클, 2키패스','fb_wingback/Balanced .759; 공격 일변도보다 Balanced 유지','SofaScore event 16260286; 경기 리포트','HIGH 스탯 / MEDIUM 역할'),
(1,12,'RDM','우측 피벗·중앙 스크린','배급과 차단을 우선하고 필요할 때 박스 앞까지 전진','19/21패스, 2인터셉트, 2슈팅(1유효)','dm_holding/Ball-Winning .788 참고; Gomes와 고정 분업인지는 보류','SofaScore event 16260286; 경기 리포트','HIGH 스탯 / MEDIUM 역할'),
(1,56,'LDM','좌측 피벗·경합과 압박','볼 회수와 접촉을 늘리며 전진 압박에 가담','12/18패스, 3/9경합, 3태클, 1슈팅','dm_holding/Roaming .679 참고; 패스 안정성 보완 필요','SofaScore event 16260286; 경기 리포트','HIGH 스탯 / MEDIUM 역할'),
(1,10,'RAM','우측 하프스페이스 창출자와 전방 압박','자연 RW가 아니지만 강한 우측 편향으로 공급을 전담','4/10패스, 4키패스, 1도움, 4/13경합','wm_winger/Attack .882; 임시 해법 성공이나 전문 우측 자원 결손은 유지','SofaScore event 16260286; 경기 리포트','HIGH 스탯 / HIGH 역할'),
(1,14,'CAM','낮게 내려오는 중앙 연결자','명목 10번보다 깊게 내려와 압박 아래 연결량을 담당','30/45패스, 63터치, 1키패스, 6/15경합, 2태클','cam_playmaker/Roaming .623; 낮은 위치가 반복되는지 후속 표본 필요','SofaScore event 16260286; 경기 리포트','HIGH 스탯 / MEDIUM 역할'),
(1,30,'LAM','왼쪽 안쪽 지원·압박 와이드 미드필더','터치라인 고정 윙어보다 낮고 안쪽에서 연결·회수','20/25패스, 1키패스, 3/9경합, 1태클, 2슈팅, 6회수','wm_widemid/Support .788 후보; 같은 위치 공식전 2경기 이상 추가 필요','SofaScore event 16260286; Emery 발언; 경기 리포트','HIGH 스탯 / MEDIUM 역할'),
(1,61,'ST','등진 연결과 배후·박스 침투를 겸한 9번','경합을 지배하기보다 반복 움직임과 실패 뒤 재시도가 강점','1골, 6슈팅(1유효), 2키패스, 9/14패스, 1/9경합','st_poacher/Attack .725 후보; 유효 표본 6경기 전까지 대표 처방 보류','SofaScore event 16260286; Emery 발언; 경기 리포트','HIGH 스탯 / MEDIUM 역할');

INSERT OR IGNORE INTO _migration_log VALUES('012-match-reports','2026-08-13',
  '경기별 심층 리포트와 선수별 전술 분석을 구조화하고 슈퍼컵 기준본을 등록');
