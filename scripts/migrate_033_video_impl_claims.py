#!/usr/bin/env python3
"""migration 033 — `video_impl_claims` 신설 (2026-09-15, 사용자 승인 「요약 규약도 바꿔줘」).

왜 (obs#762·763):
  요약 101편을 스캔했더니 **역할 코드 언급 8편 · 포커스 3편 · 팀 설정 3축 0편**이었다.
  요약은 자유 서술이라 「이 영상이 우리 구현의 무엇을 건드리는가」를 **기계가 볼 수 없었다.**
  그래서 obs#762의 결론이 나왔다 — 영상 obs 198건 중 구현을 실제로 바꾼 것은 3건뿐이고,
  진짜 결손은 「반영 안 됨」이 아니라 **「반영 대상이 무엇인지 DB가 말해주지 못함」**이었다.
  ⇒ `player_duties.applied_status`(migration 031)가 duty 축에 한 것을 **영상 축에 한다.**

⛔ **또 하나의 자유 텍스트 컬럼을 만들지 않는다.** 요약 안에 역할 코드를 적게 하는 규약으로는
   대조가 안 된다(정규식으로 재면 0%로 보이는 obs#738 부류가 반복된다). **행으로 받는다.**

설계:
  영상 1편 → 구현 주장 0..N행. 축(`axis`) 어휘로 무엇에 대한 주장인지 고정한다.

  | axis | 채우는 칼럼 | 뜻 |
  |---|---|---|
  | `role` | player_id + role_id(+focus) | 「그 선수를 이 역할로 본다」 |
  | `focus` | player_id + focus | 역할은 그대로, 포커스만 건드린다 |
  | `team_axis` | team_code + field + value | build_up_style / defensive_approach / line_height / formation |
  | `instruction` | player_id 또는 team_code + field + value | 인스트럭션·라이선스 축 |
  | `limit` | field(=reproduction_limits.axis) + value | 「게임이 이걸 재현 못 한다」 |
  | `none` | (없음) | ⭐ **요약을 읽었고 구현 주장이 없다** — 「아직 안 읽음」과 구분하는 명시 행 |

  ⭐ `none`이 이 설계의 핵심이다. 주장이 없는 영상(이적 소문·잡담)이 대다수인데,
     그걸 빈 값으로 두면 **「주장 없음」과 「미작성」이 DB에서 같은 모양**이 된다(migration 031이 고친 것과 같은 병).

  `verdict`는 **그 주장이 구현에 닿았는지**를 남긴다 — duties의 applied_status와 같은 사상이다.
  ⛔ 판정 없이 주장만 쌓지 않는다(G17이 막는다).

재실행 안전: 테이블이 이미 있으면 아무것도 하지 않는다.
"""
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core import DB                                     # noqa: E402

DDL = """
CREATE TABLE IF NOT EXISTS video_impl_claims(
  id INTEGER PRIMARY KEY,
  video_id TEXT NOT NULL,           -- match_videos.video_id (lang은 묶지 않는다 — 주장은 언어와 무관)
  axis TEXT NOT NULL,               -- role / focus / team_axis / instruction / limit / none
  player_id INTEGER REFERENCES players(id),
  team_code TEXT REFERENCES teams(code),
  role_id TEXT,                     -- 우리 역할 어휘(kernel role_group의 키) — ⛔ 자유 문자열 금지
  focus TEXT,                       -- Attack / Support / Balanced / Build-Up / Roaming / Ball-Winning / Aggressive …
  field TEXT,                       -- team_axis·instruction·limit에서 무엇을 건드리는가
  value TEXT,                       -- 그 필드의 주장값
  quote TEXT,                       -- ⭐ 전사 원문 인용(불변규칙 11 — 한국어 번역 병기)
  verdict TEXT NOT NULL,            -- APPLIED / HELD / REJECTED / PENDING / NA
  verdict_note TEXT,                -- ⛔ HELD·REJECTED는 사유·재판정 조건 필수(G17)
  source TEXT, confidence TEXT,
  added TEXT NOT NULL DEFAULT (date('now'))
);
CREATE INDEX IF NOT EXISTS ix_vic_video ON video_impl_claims(video_id);
CREATE INDEX IF NOT EXISTS ix_vic_axis ON video_impl_claims(axis, verdict);
CREATE INDEX IF NOT EXISTS ix_vic_player ON video_impl_claims(player_id);
"""

con = sqlite3.connect(DB)
existed = con.execute(
    "SELECT 1 FROM sqlite_master WHERE type='table' AND name='video_impl_claims'").fetchone()
con.executescript(DDL)
con.execute("INSERT OR IGNORE INTO _migration_log(run_at, v1_path, note) VALUES(?,?,?)",
            ("2026-09-15", "033-video-impl-claims",
             "video_impl_claims 신설 — 영상 요약을 **구현 어휘로 정형화**한다. 사용자 승인 2026-09-15 "
             "「요약 규약도 바꿔줘」(obs#762·763: 요약 101편 중 역할 코드 8편·팀 설정 3축 0편이라 "
             "기계 대조가 불가능했다). axis 어휘로 무엇에 대한 주장인지 고정하고, "
             "⭐ 주장이 없는 영상도 axis='none' 행으로 명시해 「주장 없음」과 「미작성」을 구분한다. "
             "G17이 판정 결손·어휘 이탈을 막는다."))
con.commit()
print("이미 있었음(변경 없음)" if existed else "video_impl_claims 생성")
print(f"컬럼: {[r[1] for r in con.execute('PRAGMA table_info(video_impl_claims)')]}")
con.close()
