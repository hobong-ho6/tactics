-- 042 — fc_meta_snapshots: 「지금 메타」 스냅샷 (2026-09-19, 사용자 지시 「DB에 설정 스냅샷 쌓아줘」).
--
-- 왜 별도 표인가: 우리 `team_tactic_setups`·`prescriptions`는 **실축 감독 재현**이고, 메타는 **커뮤니티·프로가 지금 뭘 쓰는가**다.
--   층을 섞으면 「에메리가 이렇게 한다」와 「메타가 이렇다」가 구분되지 않는다(불변규칙 7의 정신 — 축을 섞지 않는다).
-- ⭐ 메타는 패치마다 바뀌므로 **날짜별로 쌓고 덮지 않는다**(불변규칙 2). 화면은 최신 pulled만 읽는다.
-- kind: 'setting'(컨트롤러·게임 설정) · 'tactic'(포메이션·팀 설정 사용률).
-- priority: 1=먼저 바꿀 것(효과 크고 위험 낮음) · 2=적응 후 · 3=주의·비권장. ⛔ 우선순위는 **우리 판단**이고 출처의 주장이 아니다.
PRAGMA foreign_keys = ON;
BEGIN;
CREATE TABLE fc_meta_snapshots(
  id INTEGER PRIMARY KEY,
  game_version TEXT NOT NULL REFERENCES game_versions(code),
  pulled TEXT NOT NULL,
  kind TEXT NOT NULL CHECK(kind IN ('setting','tactic')),
  category TEXT NOT NULL,          -- passing / shooting / defending / switching / camera / control / formation / team_setting
  item TEXT NOT NULL,              -- 설정 이름 또는 포메이션 이름
  value TEXT,                      -- 권장값 또는 사용률 요약
  alternatives TEXT,               -- 갈리는 선택지·수치 범위
  scope TEXT,                      -- competitive / general / pro / community
  priority INTEGER CHECK(priority BETWEEN 1 AND 3),
  rationale TEXT,                  -- 왜 그런가(가능하면 FC27 시스템 변경과 연결)
  source TEXT NOT NULL, confidence TEXT NOT NULL,
  UNIQUE(game_version, pulled, kind, category, item)
);
CREATE INDEX ix_fc_meta_snapshots ON fc_meta_snapshots(game_version, pulled, kind);
COMMIT;
