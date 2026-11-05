-- 133 내 구단 케미 스타일 검토 결론(2026-11-05 사용자 지시 「DB에도 케미스트리 제안 업데이트」 → 「응 진행해줘」).
--
-- 왜: 케미스트리 탭의 「최종 추천」은 커널 점수로 자동 계산된다. 같은 날 역할·스탯·실축 특성·사용자 운용을 함께 본 검토 결론(센터백 Shadow 유지 · 음바예 Hunter 유지 등)이
--   리포트 파일에만 있어 화면의 자동 추천과 엇갈려 보였다. ⇒ 검토 결론을 표로 두고 화면에 자동 추천과 나란히 보인다.
-- 어떻게: 선수(club_player)마다 검토 행을 **추가만** 한다 — 다시 검토하면 새 행(reviewed가 늦은 행이 정본). 스타일은 style_id(FC27)로 조인.
--   verdict: applied = 사용자가 이미 바꿨다 · keep = 지금 스타일 유지 · change = 바꾸기 권장. 벤치는 선발로 나설 때만 효과(gsc #98).
CREATE TABLE IF NOT EXISTS fut_chem_reviews(
  id INTEGER PRIMARY KEY,
  club_player_id INTEGER NOT NULL REFERENCES fut_club_players(id),
  game_version TEXT NOT NULL REFERENCES game_versions(code),
  role_id TEXT NOT NULL,            -- 검토 기준 역할(UT 전술 역할 · 벤치는 투입될 자리)
  style_id INTEGER NOT NULL,        -- 권장 스타일(fc_chemistry_styles.style_id)
  alt_style_id INTEGER,             -- 조건부 대안
  verdict TEXT NOT NULL CHECK(verdict IN ('applied','keep','change')),
  reason_kr TEXT NOT NULL,          -- 한 줄 이유
  report TEXT,                      -- 근거 리포트 경로
  reviewed TEXT NOT NULL
);
INSERT INTO fut_chem_reviews(club_player_id,game_version,role_id,style_id,alt_style_id,verdict,reason_kr,report,reviewed) VALUES(18,'FC27','gk_ballplaying',21,23,'applied','실축 롱볼 15.5/90 → 킥 +6 · 다이빙 +9. Shield(반사신경 +9·킥 +6)도 같은 점수','reports/research/2026-11-05-xi-chem-review.md','2026-11-05');
INSERT INTO fut_chem_reviews(club_player_id,game_version,role_id,style_id,alt_style_id,verdict,reason_kr,report,reviewed) VALUES(8,'FC27','fb_wingback',19,NULL,'applied','가장 약한 핵심이 가속 76·질주 77 → 속도 +6·+6. 슬라이딩 태클 PlayStyle에 슬라이딩 +9','reports/research/2026-11-05-xi-chem-review.md','2026-11-05');
INSERT INTO fut_chem_reviews(club_player_id,game_version,role_id,style_id,alt_style_id,verdict,reason_kr,report,reviewed) VALUES(143,'FC27','cb_bpd',19,9,'keep','Aggressive 포커스·속도 74·76 → 튀어나간 뒤 복귀 속도(수비 스타일 중 속도는 Shadow뿐). 볼 플레잉 1위 Powerhouse는 패스 가중 탓','reports/research/2026-11-05-xi-chem-review.md','2026-11-05');
INSERT INTO fut_chem_reviews(club_player_id,game_version,role_id,style_id,alt_style_id,verdict,reason_kr,report,reviewed) VALUES(9,'FC27','cb_bpd',19,9,'keep','속도 79·79가 약점이고 패스는 이미 85. 점유 위주 상대를 만나면 Powerhouse','reports/research/2026-11-05-xi-chem-review.md','2026-11-05');
INSERT INTO fut_chem_reviews(club_player_id,game_version,role_id,style_id,alt_style_id,verdict,reason_kr,report,reviewed) VALUES(49,'FC27','fb_att_wb',18,NULL,'keep','역할 1위(속도·크로스)','reports/research/2026-11-05-xi-chem-review.md','2026-11-05');
INSERT INTO fut_chem_reviews(club_player_id,game_version,role_id,style_id,alt_style_id,verdict,reason_kr,report,reviewed) VALUES(14,'FC27','dm_holding',13,9,'applied','공 몰고 가기(드리블·민첩 +6)와 수비(+24)를 함께 올리는 유일한 스타일. 홀딩↔딥라잉을 자주 오가면 Powerhouse','reports/research/2026-11-05-bench-chem-review.md','2026-11-05');
INSERT INTO fut_chem_reviews(club_player_id,game_version,role_id,style_id,alt_style_id,verdict,reason_kr,report,reviewed) VALUES(4,'FC27','dm_dlp',10,NULL,'applied','Engine은 딥라잉 핵심을 거의 안 올렸다(27 → 57). 패스·볼컨트롤·침착','reports/research/2026-11-05-xi-chem-review.md','2026-11-05');
INSERT INTO fut_chem_reviews(club_player_id,game_version,role_id,style_id,alt_style_id,verdict,reason_kr,report,reviewed) VALUES(82,'FC27','wm_winger',11,NULL,'keep','역할 1위(드리블·균형·크로스)','reports/research/2026-11-05-xi-chem-review.md','2026-11-05');
INSERT INTO fut_chem_reviews(club_player_id,game_version,role_id,style_id,alt_style_id,verdict,reason_kr,report,reviewed) VALUES(16,'FC27','wm_insidefwd',17,11,'keep','속도형(가속 92→98)·실축 xG 0.14·전진 운반 83m/90. 커널 1위 Finisher는 결정력 가중 탓 — 철회. 오래 몰고 크로스까지면 Engine','reports/research/2026-11-05-xi-chem-review.md','2026-11-05');
INSERT INTO fut_chem_reviews(club_player_id,game_version,role_id,style_id,alt_style_id,verdict,reason_kr,report,reviewed) VALUES(683,'FC27','cam_playmaker',10,7,'applied','실축 슈팅 3.7·크로스 0(90분당) · 볼컨트롤 첫 터치·공 밀착(A). LM 와이드 플레이메이커로 쓰면 Artist','reports/research/2026-11-05-manzambi-chem-artist-vs-maestro.md','2026-11-05');
INSERT INTO fut_chem_reviews(club_player_id,game_version,role_id,style_id,alt_style_id,verdict,reason_kr,report,reviewed) VALUES(848,'FC27','st_advanced',3,17,'keep','역할 점수 동점. 채널로 빠져 뒷공간을 노리는 쪽이면 Hunter(가속 81·질주 80이 약점)','reports/research/2026-11-05-xi-chem-review.md','2026-11-05');
INSERT INTO fut_chem_reviews(club_player_id,game_version,role_id,style_id,alt_style_id,verdict,reason_kr,report,reviewed) VALUES(51,'FC27','wm_insidefwd',17,NULL,'keep','속도형(가속 88·질주 85)·실축 xG 0.1 — 음바예와 같은 판단','reports/research/2026-11-05-bench-chem-review.md','2026-11-05');
INSERT INTO fut_chem_reviews(club_player_id,game_version,role_id,style_id,alt_style_id,verdict,reason_kr,report,reviewed) VALUES(79,'FC27','cb_bpd',19,18,'keep','질주 60·가속 61이 가장 약하다 → 속도 +6·+6과 수비 +18. 패스를 더 원하면 Catalyst(수비 상승 0)','reports/research/2026-11-05-bench-chem-review.md','2026-11-05');
INSERT INTO fut_chem_reviews(club_player_id,game_version,role_id,style_id,alt_style_id,verdict,reason_kr,report,reviewed) VALUES(30,'FC27','st_advanced',3,17,'keep','역할 1위(Hunter 동점)','reports/research/2026-11-05-bench-chem-review.md','2026-11-05');
INSERT INTO fut_chem_reviews(club_player_id,game_version,role_id,style_id,alt_style_id,verdict,reason_kr,report,reviewed) VALUES(1,'FC27','dm_holding',9,NULL,'keep','홀딩·딥라잉 두 역할 모두 1위','reports/research/2026-11-05-bench-chem-review.md','2026-11-05');
INSERT INTO fut_chem_reviews(club_player_id,game_version,role_id,style_id,alt_style_id,verdict,reason_kr,report,reviewed) VALUES(146,'FC27','wm_insidefwd',3,7,'change','측면질주 진화 뒤 측면 카드 · 가장 약한 핵심 결정력 79. CAM으로 쓰면 Artist. 실축 표본 105분','reports/research/2026-11-05-bench-chem-review.md','2026-11-05');
INSERT INTO fut_chem_reviews(club_player_id,game_version,role_id,style_id,alt_style_id,verdict,reason_kr,report,reviewed) VALUES(25,'FC27','wm_winger',11,NULL,'change','실축 드리블 시도 5.2·전진 운반 116m(90분당) — 드리블러. 지금 스타일 없음(27 → 54)','reports/research/2026-11-05-bench-chem-review.md','2026-11-05');
INSERT INTO fut_chem_reviews(club_player_id,game_version,role_id,style_id,alt_style_id,verdict,reason_kr,report,reviewed) VALUES(12,'FC27','fb_att_wb',18,11,'change','Anchor는 공격형 윙백 핵심을 거의 안 올린다(27 → 54). 안쪽으로 몰고 들어가는 역할이면 Engine','reports/research/2026-11-05-bench-chem-review.md','2026-11-05');
INSERT INTO fut_chem_reviews(club_player_id,game_version,role_id,style_id,alt_style_id,verdict,reason_kr,report,reviewed) VALUES(144,'FC27','dm_holding',9,19,'change','홀딩·딥라잉 모두 1위. RB로 쓰면 Shadow','reports/research/2026-11-05-bench-chem-review.md','2026-11-05');
INSERT INTO fut_chem_reviews(club_player_id,game_version,role_id,style_id,alt_style_id,verdict,reason_kr,report,reviewed) VALUES(48,'FC27','fb_wingback',19,NULL,'keep','역할 1위','reports/research/2026-11-05-bench-chem-review.md','2026-11-05');
INSERT INTO fut_chem_reviews(club_player_id,game_version,role_id,style_id,alt_style_id,verdict,reason_kr,report,reviewed) VALUES(132,'FC27','wm_insidefwd',17,7,'change','속도 76·69가 가장 약한 핵심 → Hunter로 AcceleRATE Controlled→Explosive. CAM으로 쓰면 Artist','reports/research/2026-11-05-bench-chem-review.md','2026-11-05');
INSERT INTO fut_chem_reviews(club_player_id,game_version,role_id,style_id,alt_style_id,verdict,reason_kr,report,reviewed) VALUES(27,'FC27','cb_bpd',19,9,'change','속도 71·67과 패스(시야 57·긴 패스 66)가 모두 약하다 — 센터백 판단(복귀 속도 우선)에 따라 Shadow. 빌드업을 맡기면 Powerhouse','reports/research/2026-11-05-bench-chem-review.md','2026-11-05');
INSERT INTO fut_chem_reviews(club_player_id,game_version,role_id,style_id,alt_style_id,verdict,reason_kr,report,reviewed) VALUES(31,'FC27','dm_holding',9,NULL,'change','가장 약한 핵심 차단 74·수비 위치 75·태클 76','reports/research/2026-11-05-bench-chem-review.md','2026-11-05');
INSERT INTO _migration_log (run_at, v1_path, note) VALUES ('2026-11-05','133-fut-chem-reviews','fut_chem_reviews 신설 · 선발 11 + 교체·리저브 12 검토 결론');
