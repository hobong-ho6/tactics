#!/usr/bin/env python3
"""migration 032 — `match_videos` 신설 (2026-09-15, 사용자 지시 「영상 요약·중요한 점을 웹에서 보게」).

왜:
  전사 139편은 `reports/transcripts/`에 있고, 거기서 나온 판정은 `observations`·`player_duties`에
  흩어져 있다. 그런데 **「어느 영상이 무슨 말을 했나」를 한 화면에서 볼 수 있는 곳이 없었다** —
  경기 리포트는 산문이고, 전사 원문은 30~60분짜리 자막 덩어리다.
  ⇒ 영상 1편 = 행 1개로 만들고 경기(`match_reports`)에 붙인다.

⛔ 설계 원칙 — **세 층을 섞지 않는다**:
  ⑴ `channel/title/published/url/transcript_path` = **파싱**(전사 헤더에서 기계적으로 뽑는다)
  ⑵ `obs_refs` = **이미 검증된 판정**(그 전사를 source로 인용한 observations — 발명 0)
  ⑶ `summary/key_points` = **사람이 전사를 읽고 쓴 요약**(쓴 회차를 source에 남긴다)
  ⇒ ⑶이 비어 있어도 ⑴⑵만으로 화면에 쓸 수 있다. 「요약 없음」과 「내용 없음」을 구분한다.

⚠️ 전사는 **유튜브 자동 생성 자막**이라 오인식이 있다(docs/30 「전사 오인식 대조표」 — Matty Cash↔Maatsen 등).
   `confidence`에 auto-caption을 명기하고, 인용은 원문+번역 병기(불변규칙 11).

재실행 안전: 테이블이 이미 있으면 아무것도 하지 않는다.
"""
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core import DB                                     # noqa: E402

DDL = """
CREATE TABLE IF NOT EXISTS match_videos(
  id INTEGER PRIMARY KEY,
  video_id TEXT NOT NULL,           -- 유튜브 id (전사 파일명의 앞부분)
  lang TEXT,                        -- 전사 언어 (en/es/pt/…)
  report_id INTEGER REFERENCES match_reports(id) ON DELETE SET NULL,  -- 경기 귀속(없으면 NULL = 시즌·선수 축)
  regime_id INTEGER REFERENCES regimes(id),   -- 팀 축 필터용 (불변규칙 6 — 팀은 team_code/regime로 조인)
  team_code TEXT REFERENCES teams(code),
  channel TEXT NOT NULL,            -- 채널명 (UTV | Aston Villa Fan Channel · The Villans · 1874 …)
  title TEXT,                       -- 영상 제목
  published TEXT,                   -- 게시일. '경' 접미가 붙은 추정치는 published_approx=1
  published_approx INTEGER NOT NULL DEFAULT 0,
  url TEXT,
  transcript_path TEXT,             -- reports/transcripts/{id}.{lang}.md
  kind TEXT,                        -- 경기반응 / 전술분석 / 선수스카우팅 / 감독회견 / 상대팀 / 프리시즌
  summary TEXT,                     -- ⑶ 사람이 쓴 핵심 요약 (NULL = 아직 안 씀)
  key_points TEXT,                  -- ⑶ 줄바꿈 구분 핵심 포인트
  obs_refs TEXT,                    -- ⑵ 이 전사를 인용한 observations id 목록(CSV) — 자동 산출
  source TEXT, confidence TEXT,
  UNIQUE(video_id, lang)
);
CREATE INDEX IF NOT EXISTS ix_match_videos_report ON match_videos(report_id);
CREATE INDEX IF NOT EXISTS ix_match_videos_team ON match_videos(team_code, published);
"""

con = sqlite3.connect(DB)
existed = con.execute(
    "SELECT 1 FROM sqlite_master WHERE type='table' AND name='match_videos'").fetchone()
con.executescript(DDL)
con.execute("INSERT OR IGNORE INTO _migration_log(run_at, v1_path, note) VALUES(?,?,?)",
            ("2026-09-15", "032-match-videos",
             "match_videos 신설 — 전사 1편 = 행 1개. 사용자 지시 2026-09-15 「UTV·The Villans 영상 주요 내용을 "
             "우리 페이지에서 보게」. 파싱(채널·제목·게시일) / 검증된 판정(obs_refs) / 사람 요약(summary) "
             "세 층을 컬럼으로 분리해 「요약 없음」과 「내용 없음」을 구분한다."))
con.commit()
print("이미 존재 — 변경 없음" if existed else "✅ match_videos 생성")
