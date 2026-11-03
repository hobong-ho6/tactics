-- 129 GK OVR 산정식 교정 (2026-11-03 사용자 「응 고쳐줘」 — 골키퍼 조사 gsc #72 뒤).
--
-- 왜: 2026-10-02 적합(scripts/fit_position_ovr.py · 「가중 합 1」 비음수 최소제곱)이 GK를 반사신경 39 · 포지셔닝 25 · 다이빙 18 · 핸들링 13 ·
--   반응력 5 · 킥 0으로 갈랐는데, FC27 비특별 기본 GK 카드 90장 중 **41장**만 맞았다. 네 GK 속성의 상관이 0.91~0.94라 비율이 흔들렸고,
--   실제 공식에는 **상수 +1**이 있어 가중 합 1 모양으로는 담을 수 없었다.
--   검증된 공식: OVR = round(0.21×(다이빙+핸들링+포지셔닝+반사신경) + 0.11×반응력 + 0.05×킥) + 1 — **83/90 정확 · 90/90 ±1**(등급 C ·
--   reports/research/2026-11-03-fc27-goalkeeper-stats.md · gsc #72). 출처 표(21/21/21/21/11/5)는 커뮤니티 고전 표(D)이고 일치는 우리 검산이다.
-- 어떻게: 새 회차(fitted 2026-11-03) GK 행을 **추가**한다(불변규칙 2 · 10-02 행은 남긴다). `_const` 행은 가중이 아니라 **더하는 OVR 점수**다
--   (core/position_ovr.CONST · posovr.js가 같은 규칙 · G31이 대조). core/position_ovr.load는 이제 그룹별 최신 회차를 고른다.
--   ⛔ fit_position_ovr.py는 GK를 다시 적합하지 않는다(건너뜀).
INSERT INTO fc_position_ovr_weights(game_version,pos_group,attr,weight_pct,fitted,sample_n,test_n,test_exact,test_within1,source,confidence) VALUES
 ('FC27','GK','다이빙',21,'2026-11-03',90,90,83,90,'GK 공식 검산(migration 129) — FC27 비특별 기본 GK 카드 90장 · round(0.21×4속성+0.11×반응력+0.05×킥)+1','C — 우리 검산 83/90 정확 · 표 자체는 커뮤니티 고전 표(D) · EA 비공개'),
 ('FC27','GK','핸들링',21,'2026-11-03',90,90,83,90,'GK 공식 검산(migration 129)','C'),
 ('FC27','GK','포지셔닝',21,'2026-11-03',90,90,83,90,'GK 공식 검산(migration 129)','C'),
 ('FC27','GK','반사신경',21,'2026-11-03',90,90,83,90,'GK 공식 검산(migration 129)','C'),
 ('FC27','GK','반응력',11,'2026-11-03',90,90,83,90,'GK 공식 검산(migration 129)','C'),
 ('FC27','GK','킥',5,'2026-11-03',90,90,83,90,'GK 공식 검산(migration 129)','C'),
 ('FC27','GK','_const',1,'2026-11-03',90,90,83,90,'GK 공식 상수 +1(가중 아님 · 더하는 OVR 점수)','C — 상수의 출처는 미상(국제 명성 보정과 별개로 전 카드에 붙는다)');
INSERT INTO _migration_log (run_at, v1_path, note) VALUES
 ('2026-11-03', '129-gk-ovr-formula',
  'GK OVR 산정식 교정 — 21/21/21/21/11/5 + 상수 1(83/90 정확 · 종전 적합 41/90) · _const 행 도입 · load()·export meta 그룹별 최신 회차 · fit_position_ovr.py GK 건너뜀');
