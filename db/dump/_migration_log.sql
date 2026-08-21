INSERT INTO _migration_log VALUES('2026-08-11','/Users/ad03230205/Documents/tactics/data/avl_analysis.db','full rebuild');
INSERT INTO _migration_log VALUES('2026-08-13 04:44:41','/Users/user/Documents/tactics/data/avl_analysis.db','post-cutover repair: merged 142 appearances into player_matches; changed 116; migrate_v1.py bug fixed');
INSERT INTO _migration_log VALUES('012-match-reports','2026-08-13','경기별 심층 리포트와 선수별 전술 분석을 구조화하고 슈퍼컵 기준본을 등록');
INSERT INTO _migration_log VALUES('013-match-game-presets','2026-08-13','경기 전용 FC 팀 설정과 선수 역할·포커스를 시즌 정본과 분리해 저장');
INSERT INTO _migration_log VALUES('014-player-analysis-provenance-and-supercup-subs','2026-08-13','선수 분석 관찰 기간·표본 범위, 현재 스쿼드 누락 분석/평가, 슈퍼컵 교체 5명 원천·리포트·종료 XI 처방 보강');
INSERT INTO _migration_log VALUES('015-team-match-ppda-and-duels','2026-08-14','team_match_stats에 PPDA(비율+분자·분모·정의)와 팀 단위 공중볼·드리블·태클·인터셉트·클리어 컬럼 추가. 2026 슈퍼컵 값 적재(PPDA 빌라 12.59 / PSG 8.50)');
INSERT INTO _migration_log VALUES('016-players-understat-id','2026-08-21','players.understat_id 추가 — 축11 슛맵의 Understat 경로 (SofaScore·WhoScored·FBref 전부 403인 환경의 대체 원천)');
INSERT INTO _migration_log VALUES('017-shot-profile-penalties','2026-08-21','player_shot_profile에 penalties·npxg_sum 추가 — PK가 xG/슛(슛 선택 품질) 해석을 왜곡한다(콜 파머 0.137→0.099). 기존 SofaScore 9행은 PK 포함 여부 불명이라 NULL.');
INSERT INTO _migration_log VALUES('018-players-positions-alt','2026-08-21','primary_position을 FotMob 정규코드로 통일하고 원값(LCB·RB/DM 등 좌우·복합 표기)을 positions_alt에 보존한다');
