#!/usr/bin/env python3
"""2026-11-22 — 프리킥 세트피스 전술 메뉴 입력(#83 보강) 적재.
D 1행. INSERT만(불변규칙 2) · title로 중복 검사."""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from core.db import connect  # noqa: E402

TODAY = "2026-11-22"
ROW = dict(
 game_version="FC27", area="set_pieces",
 title="프리킥 세트피스 메뉴 입력은 코너와 방향이 다르다",
 change=("세트피스 전술 메뉴(#81·#83 보강 — 프리킥 입력). 메뉴는 코너와 같이 D-pad ↑로 연다. "
         "⭐ **프리킥 입력**: 인원 추가 ↑→↑ · 인원 제거 ↑→**→** · 니어포스트 런 ↑→**↓** · 파포스트 런 ↑→**←** · (수비) 라인 내리기 ↑→→ · (수비) 오프사이드 트랩 ↑→←. "
         "**코너 입력**(#83): 인원 추가 ↑→↑ · 인원 제거 ↑→↓ · 니어 ↑→← · 파 ↑→→. "
         "⇒ 인원 추가만 같고 **제거·니어·파는 프리킥과 코너에서 방향이 다르다**(코너에서 익힌 ↑→→가 프리킥에서는 파포스트 런이 아니라 인원 제거). "
         "프리킥 수비에는 대인/지역 전환이 없고 라인 내리기·오프사이드 트랩 두 개뿐. "
         "⛔ 여전히 미확인(#83): 인원 추가·제거가 몇 명을 움직이는지 · 기본 인원 · 선택 유지 범위."),
 evidence=("Pro Clubs HQ 조작 변경 글 본문(2026-11-22 HTML 직접 확인)의 프리킥 표: "
           "「Remove Player from Set Play」(「세트플레이에서 인원 제거」) = D-pad up 뒤 D-pad right · "
           "공격 시 「Run Near Post」(「니어포스트 런」) = D-pad up 뒤 D-pad down · "
           "공격 시 「Run Far Post」(「파포스트 런」) = D-pad up 뒤 D-pad left · "
           "수비 시 「Drop Back」(「라인 내리기」) = D-pad right · 「Offside Trap」(「오프사이드 트랩」) = D-pad left. "
           "같은 글 코너 표: 「Remove Player」(「인원 제거」) = D-pad down. "
           "11-21 회차에 검색 요약으로만 보였던 「프리킥 제거 ↑→→」 단서를 본문으로 확인. 코너 입력은 fifauteam 전사와 일치(#83), 프리킥 입력은 **이 한 출처뿐**."),
 impact=("세트피스 조작: 프리킥에서 코너 습관대로 ↑→→를 누르면 파포스트 런이 아니라 **인원 제거**가 된다 — 프리킥 세트플레이 지시 시 주의(조작 실수 방지). "
         "아스톤 빌라 세트피스 구현(키커·타깃 지정)은 팀 관리 화면 설정이라 영향 없음. "
         "3선(CDM) 역할·포커스 동작과 무관 — 아스톤 빌라 3선 정본 재검토 사유 아님. 인원 추가·제거 동작 설명은 여전히 없음(#83 미확인 목록 유지)."),
 source="https://proclubshq.com/blog/fc27-control-changes/ (Pro Clubs HQ 「What Changed in EA FC 27's Controls」 · 2026-08-16 게시 · 2026-10-15 갱신 · 인게임 Advanced 조작 페이지 전사 · 2026-11-22 본문 직접 확인)",
 confidence="D — 커뮤니티의 인게임 조작 목록 전사 1건(프리킥 입력은 교차 출처 없음 · 인게임 화면 미확인) · 동작(인원 수·유지)은 결손",
 recorded=TODAY,
)
con = connect()
if con.execute("select 1 from game_system_changes where title=?", (ROW["title"],)).fetchone():
    sys.exit("이미 있음 — 건너뜀")
cols = ",".join(ROW); q = ",".join("?" * len(ROW))
cur = con.execute(f"insert into game_system_changes({cols}) values({q})", tuple(ROW.values()))
con.commit(); print("inserted id", cur.lastrowid)
