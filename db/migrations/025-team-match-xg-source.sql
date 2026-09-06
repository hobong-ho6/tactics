-- team_match_stats.xg_source 신설 — xG 계열의 제공사·스냅샷 provenance를 정형 필드로 옮긴다.
-- 사용자 지시 2026-09-06.
--
-- 왜: `xg_v`·`xg_o`·`xg_op_v`·`xg_op_o`는 제공사마다 절대값이 다르다(실측: ATM 아틀레틱전
-- FotMob 1.02–1.41 vs SofaScore 0.86–1.35). 지금까지 provenance는 `source` 산문에만 있었고,
-- 여러 경기를 가로질러 집계하면 제공사가 조용히 섞였다(obs#461 축 검정에서 발현, obs#463).
-- SKILL §3의 「같은 스냅샷 동시 수집」 규칙도 준수 여부를 질의할 수 없었다.
--
-- ⭐ 이 컬럼을 채우는 과정에서 obs#463의 진단이 틀렸음이 드러났다 — ATM 비야레알전은
-- 「제공사만 다른 정합 행」이 아니라 **행 내부에서 xg_v(SofaScore)와 xg_op_v(FotMob)가 갈린
-- 스냅샷 혼합**이었다. obs#337이 경고한 바로 그 결함이고, 부등식을 깨지 않아 G12를 통과했다.
-- 같은 패턴이 2행 더 있었다(ATM 말라가·LIV 뉴캐슬 — 제공사는 같고 스냅샷이 다르다).
--
-- 값 규약 (질의 가능하게 고정):
--   'FotMob'            xG 4종을 FotMob 한 응답에서 동시 수집 (SKILL §3 준수)
--   'SofaScore'         xG를 SofaScore statistics 한 응답에서 수집
--   'Media:<매체>'      경기 스탯 API가 아니라 기사에서 보충한 값
--   'MIXED: …'          ⚠️ xG 계열이 한 스냅샷에서 오지 않았다. 뒤에 어느 필드가 어디서 왔는지 적는다.
--                       **교차 경기 집계에서 제외 대상이다.**
--   'UNKNOWN'           source 산문으로 귀속을 특정할 수 없다 (결손이지 0이 아니다)
--   NULL                xg_v 자체가 없는 행
--
-- ⛔ 값은 하나도 덮어쓰지 않는다 — provenance만 기록한다(불변규칙 2).
--    MIXED 3행의 xG 재수집 여부는 사용자 판단 대기이며, 두 행은 리포트가 complete다.
PRAGMA foreign_keys = ON;
BEGIN;

ALTER TABLE team_match_stats ADD COLUMN xg_source TEXT;

-- ── 1) 기본값: xg_v가 있고 source에 FotMob이 없으면 SofaScore 단일 원천이다 (45행) ──
UPDATE team_match_stats SET xg_source = 'SofaScore'
 WHERE xg_v IS NOT NULL AND source NOT LIKE '%FotMob%';

-- ── 2) FotMob 단일 스냅샷 (xG 4종 동시 수집 — SKILL §3 준수) ──
-- ⚠️ event_id는 행마다 SofaScore id와 FotMob matchId가 섞여 있다(레거시) — 실제 저장된 값으로 지정한다.
UPDATE team_match_stats SET xg_source = 'FotMob'
 WHERE event_id IN (5795369,  -- AVL 08-23 브라이턴 (D+2 동일 스냅샷 전량 재수집)
                    5795372,  -- CHE 08-24 풀럼 (obs#338 결정 C, 동일 스냅샷)
                    16798240, -- CHE 08-27 루턴
                    16363254, -- LIV 08-29 포레스트
                    16416316, -- ATM 08-29 세비야
                    16363249, -- CHE 08-30 브라이턴
                    5795426,  -- AVL 08-31 아스날
                    16363261, -- LIV 09-04 입스위치
                    5795440,  -- AVL 09-05 헐
                    16416317) -- ATM 09-05 아틀레틱
   AND xg_v IS NOT NULL;

-- ── 3) ⚠️ 스냅샷 혼합 3행 ──
UPDATE team_match_stats SET xg_source =
 'MIXED: xg_v/xg_o=SofaScore@2026-08-24 · xg_op_v/xg_op_o=FotMob matchId=5868022@2026-08-25'
 WHERE event_id = 16416302 AND team_code = 'ATM';

UPDATE team_match_stats SET xg_source =
 'MIXED: xg_v/xg_o=FotMob matchId=5795371@2026-08-24 · xg_op_v/xg_op_o=FotMob 재수집@2026-08-25'
 WHERE event_id = 5795371 AND team_code = 'LIV';

UPDATE team_match_stats SET xg_source =
 'MIXED: xg_v/xg_o=FotMob matchId=5868012@2026-08-19 · xg_op_v/xg_op_o=FotMob 재수집@2026-08-25'
 WHERE event_id = 5868012 AND team_code = 'ATM';   -- 08-19 말라가 (행은 FotMob matchId로 저장돼 있다)

-- ── 4) 기사 보충 1행 (슈퍼컵 — 경기 스탯 API가 아니다) ──
UPDATE team_match_stats SET xg_source = 'Media:beIN Sports@2026-08-14'
 WHERE event_id = 16260286 AND team_code = 'AVL';

-- ── 5) 귀속 불명 2행 — 기본이 sofascore인데 「프리시즌 보강」으로 FotMob이 덧붙어
--       xG가 어느 쪽인지 산문으로 특정되지 않는다. 결손을 0으로 만들지 않는다(docs/30). ──
UPDATE team_match_stats SET xg_source = 'UNKNOWN'
 WHERE event_id IN (16284981, 16285002) AND xg_v IS NOT NULL;

INSERT OR IGNORE INTO _migration_log VALUES(
 '2026-09-06','025-team-match-xg-source',
 'team_match_stats.xg_source 추가 — xG 계열의 제공사·스냅샷 provenance를 정형화한다(사용자 지시 2026-09-06). '
 || '제공사별 절대값이 달라 교차 경기 집계에서 조용히 섞였다(obs#461 검정 중 발현). '
 || '백필 결과 61행 = SofaScore 45 · FotMob 10 · MIXED 3 · Media 1 · UNKNOWN 2. '
 || '⭐ 이 과정에서 obs#463의 진단이 틀렸음이 드러났다 — ATM 비야레알전은 제공사 차이가 아니라 '
 || '행 내부 스냅샷 혼합(xg_v=SofaScore / xg_op=FotMob)이고 obs#337이 경고한 결함이다. '
 || '같은 패턴 2행 추가 발견(ATM 말라가·LIV 뉴캐슬). 값은 덮어쓰지 않고 provenance만 기록했다.'
);
COMMIT;
