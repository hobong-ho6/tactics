-- team_match_stats에 PPDA를 정형 필드로 추가한다.
-- PPDA는 구현마다 정의(존 경계·수비액션 종류)가 달라 값만 저장하면 검증도 비교도 불가능하다.
-- 따라서 비율과 함께 **분자·분모·정의**를 저장해 재현 가능하게 만든다.
-- 함께, obs#206이 확보했으나 저장할 칸이 없어 산문에만 남아 있던 팀 단위
-- 공중볼·드리블·수비액션 지표도 같은 표에 정형화한다(DoD: 값을 산문에 묻지 않는다).
PRAGMA foreign_keys = ON;
BEGIN;

-- ── PPDA (규약: _v = team_code 팀, _o = 상대) ──
-- ppda_v = "우리가 얼마나 강하게 압박했나" = 상대 패스(ppda_num_v) / 우리 수비액션(ppda_den_v).
-- 낮을수록 강한 압박이다.
ALTER TABLE team_match_stats ADD COLUMN ppda_v REAL;
ALTER TABLE team_match_stats ADD COLUMN ppda_o REAL;
ALTER TABLE team_match_stats ADD COLUMN ppda_num_v INTEGER;   -- 분자: 상대가 자기 진영에서 시도한 패스
ALTER TABLE team_match_stats ADD COLUMN ppda_den_v INTEGER;   -- 분모: 우리 수비액션(상대 진영)
ALTER TABLE team_match_stats ADD COLUMN ppda_num_o INTEGER;
ALTER TABLE team_match_stats ADD COLUMN ppda_den_o INTEGER;
ALTER TABLE team_match_stats ADD COLUMN ppda_method TEXT;     -- 존 경계·수비액션 종류·원천. 없으면 값 비교 금지

-- ── 팀 단위 경합·수비 지표 (obs#206에서 확보, 저장 칸이 없었다) ──
ALTER TABLE team_match_stats ADD COLUMN aerial_won_v INTEGER;
ALTER TABLE team_match_stats ADD COLUMN aerial_att_v INTEGER;
ALTER TABLE team_match_stats ADD COLUMN aerial_won_o INTEGER;
ALTER TABLE team_match_stats ADD COLUMN aerial_att_o INTEGER;
ALTER TABLE team_match_stats ADD COLUMN dribble_succ_v INTEGER;
ALTER TABLE team_match_stats ADD COLUMN dribble_att_v INTEGER;
ALTER TABLE team_match_stats ADD COLUMN dribble_succ_o INTEGER;
ALTER TABLE team_match_stats ADD COLUMN dribble_att_o INTEGER;
ALTER TABLE team_match_stats ADD COLUMN tackles_v INTEGER;
ALTER TABLE team_match_stats ADD COLUMN tackles_o INTEGER;
ALTER TABLE team_match_stats ADD COLUMN interceptions_v INTEGER;
ALTER TABLE team_match_stats ADD COLUMN interceptions_o INTEGER;
ALTER TABLE team_match_stats ADD COLUMN clearances_v INTEGER;
ALTER TABLE team_match_stats ADD COLUMN clearances_o INTEGER;

-- ── 2026 UEFA Super Cup (AVL 1-2 PSG) 적재 ──
-- PPDA는 WhoScored(Opta) matchCentreData 이벤트 1588건에서 산출.
-- 경합·수비 지표는 FotMob matchDetails(matchId=5729447) 팀 스탯이며,
-- 태클·인터셉트·클리어·공중볼 승리 4개 항목은 WhoScored 이벤트 집계와 **정확히 일치**해 교차검증됐다.
UPDATE team_match_stats SET
  ppda_v = 12.59, ppda_num_v = 428, ppda_den_v = 34,
  ppda_o = 8.50,  ppda_num_o = 289, ppda_den_o = 34,
  ppda_method = '분자=상대가 자기 진영 3/5(x<60)에서 시도한 패스 · 분모=해당 팀 수비액션(Tackle·Interception·Challenge·Foul) 상대 진영 2/5(x>40). 원천=WhoScored matchCentreData(Opta) 이벤트 1588건, 2026-08-14 수집. ⚠️ PPDA는 구현마다 존 경계·액션 종류가 다르다 — 이 정의와 다른 출처의 PPDA를 직접 비교하지 말 것.',
  aerial_won_v = 4,  aerial_att_v = 12, aerial_won_o = 8, aerial_att_o = 12,
  dribble_succ_v = 10, dribble_att_v = 17,
  dribble_succ_o = 14, dribble_att_o = 21,
  tackles_v = 18, tackles_o = 23,
  interceptions_v = 6, interceptions_o = 9,
  clearances_v = 13, clearances_o = 28,
  source = source || ' / [2026-08-14 마이그레이션 015] PPDA=WhoScored matchCentreData(Opta) 이벤트 산출 · 경합/수비 지표=FotMob matchDetails matchId=5729447 (WhoScored 이벤트 집계로 교차검증)',
  confidence = confidence || ' / ⚠️ PPDA·경합·수비 지표는 SofaScore가 아니라 WhoScored(Opta)·FotMob 원천이다 — 같은 행의 SofaScore 필드와 provenance가 다르다. / 교차검증 결과: 태클 18·인터셉트 6·클리어 13·공중볼 승리 4는 WhoScored 이벤트 집계와 **정확히 일치**. 공중볼 시도 12는 FotMob 승률 33%에서 역산했고 WhoScored 집계와도 일치한다. / ⚠️ **드리블 시도만 두 원천이 갈린다** — FotMob 승률 59%로 역산하면 17이고 WhoScored TakeOn 이벤트 집계는 19다(성공 10은 양쪽 동일). 정의 차이(무산 시도의 분류)로 보이며, 팀 단위 블록의 원천 일관성을 위해 **FotMob 값 17을 채택**했다. 선수별 원천값은 player_matches.stats_json.whoscored에 있다.'
WHERE event_id = 16260286 AND team_code = 'AVL';

INSERT OR IGNORE INTO _migration_log VALUES(
 '015-team-match-ppda-and-duels','2026-08-14',
 'team_match_stats에 PPDA(비율+분자·분모·정의)와 팀 단위 공중볼·드리블·태클·인터셉트·클리어 컬럼 추가. 2026 슈퍼컵 값 적재(PPDA 빌라 12.59 / PSG 8.50)'
);
COMMIT;
