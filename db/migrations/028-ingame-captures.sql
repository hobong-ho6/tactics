-- 028 — ingame_captures: 인게임 히트맵 스크린샷 → 5×5 그리드 → 실측·커널 대조 결과 (2026-09-08, 사용자 지시 1번).
-- docs/50은 2026-07-05에 「체계적 검증 불가」로 폐기됐다. 이번에는 **경량 경로**만 연다 — PS Remote Play(macOS)
-- 스크린샷을 scripts/ingame_heatmap_to_grid.py로 읽어 코사인 하나를 남긴다. 판정(processing)은 하지 않고 기록만 한다.
-- v1의 ingame_checks(비어 있던 채 아카이브)와 다른 표다 — 그 표는 v2 DB에 없다.
PRAGMA foreign_keys = ON;
BEGIN;
CREATE TABLE ingame_captures(
  id INTEGER PRIMARY KEY,
  captured TEXT NOT NULL,                       -- YYYY-MM-DD
  game_version TEXT NOT NULL REFERENCES game_versions(code),
  regime_id INTEGER REFERENCES regimes(id),
  tactic_code TEXT,                             -- 그 경기에 쓴 FC 공유 코드(12자) — team_tactic_setups.tactic_code와 대조
  report_id INTEGER REFERENCES match_reports(id),  -- 경기 전용 프리셋을 재현한 경우
  player_id INTEGER REFERENCES players(id),
  image_path TEXT NOT NULL,
  attack_dir TEXT NOT NULL,                     -- up/down/left/right (스크린샷 안 공격 방향)
  box TEXT,                                     -- 피치 픽셀 상자 x0,y0,x1,y1
  cells TEXT NOT NULL,                          -- 25칸 가중치 CSV
  map25 TEXT NOT NULL,
  ref_kind TEXT,                                -- 'player:<id>:<kind>' | 'kernel:<role>/<focus>@x<n>'
  ref_map25 TEXT,
  cosine REAL,
  note TEXT, source TEXT NOT NULL, confidence TEXT NOT NULL
);
INSERT INTO _migration_log(run_at, v1_path, note) VALUES
 (date('now'), '028-ingame-captures',
  '인게임 히트맵 캡처 기록표 신설(사용자 지시 2026-09-08 1번). 경로 조사 결론: PS5→Mac은 PS Remote Play 창 스크린샷이 최단, PS App 자동 업로드(14일 보존)·USB(exFAT)가 대안. FC26 Match Facts 원자료 export는 없다(콘솔 세이브 export 불가). 전술 코드는 12자 서버 공유 코드로 화면 판독 후 team_tactic_setups.tactic_code에 기입.');
COMMIT;
