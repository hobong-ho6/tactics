#!/usr/bin/env python3
"""2026-11-17 — Steam 고정글 「FC 27 - FUT Developer Q&A Responses - November」(11-16 게시 · 11-13 Discord FUT Q&A 정리) 적재.
A 1행(FUT 경제·방침 — 게임 시스템 동작 변경 없음). INSERT만(불변규칙 2) · title로 중복 검사."""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from core.db import connect  # noqa: E402

TODAY = "2026-11-17"
URL = "https://steamcommunity.com/app/4080220/discussions/0/567051233471532410/"
ROW = dict(
 game_version="FC27", area="evolution",
 title="FUT 11월 Q&A — 진화 상향은 Thunderstruck부터 · 케미 유연성 과잉 축소 인정",
 change=("11-13 공식 Discord FUT 개발자 Q&A를 EA 커뮤니티 매니저가 Steam 고정글로 정리(14문답 · 11-16 게시). 11-11 FUT 개발자 노트(#110)의 「검토 중」 항목에 **시점**이 붙었다. "
         "⑴ **진화 과잉 하향 인정** — 진화 상향의 첫 의미 있는 변화는 **Thunderstruck 캠페인부터**, 이후 캠페인에서 추가 조정(Q7·Q8). 목표는 「평균 Rivals/Champions 스쿼드 선발에 진화 카드가 들어가는 것」. "
         "⑵ **스쿼드 다양성** — 아이콘 케미 하향·케미 부스트 레어리티 축소가 **과잉 교정이었을 수 있다**고 인정 · 케미 부스트 캠페인 확대 등 케미 유연성 확대를 조사(Q1·Q10). 다양성 요인으로 「gameplay balance」(게임플레이 밸런스)를 함께 꼽았지만 **구체적 게임플레이 조정 항목은 없음**. "
         "⑶ **간소화 SBC** — 높은 아이템 점수 SBC 일부에 **개별 챌린지·보상 복귀를 검토**(Q3·Q6 — #110 ⑷ 「복귀 계획 없음」에서 후퇴) · 일상 업그레이드 SBC 요구치 재조정 · 아이템 즐겨찾기(제출 방지) 추가 예정(Q14). "
         "⑷ **시즌 3** — Hall of FUT 갤러리 카드 업그레이드 진화(갤러리 토큰 상점 · Unleashed 수치까지는 아님) · 시즌 토큰 도입으로 게임 모드 보상 대폭 상향 · Champions TOTW 레드 픽 랭크 보장 복귀 · 캠페인 보장 팩(Q2·Q4·Q5·Q9·Q11·Q13). "
         "⑸ 질문자가 제기한 **오프사이드 트랩 남용**(Q13)은 답변에서 다루지 않았다(보상 부분만 답함)."),
 evidence=("「However, it's clear that we've overcorrected.」(하지만 우리가 과잉 교정했다는 것은 분명하다.) · "
           "「you can expect to see the first meaningful changes starting with our Thunderstruck campaign, with further adjustments coming in future campaigns.」(첫 의미 있는 변화는 Thunderstruck 캠페인부터 볼 수 있고, 이후 캠페인에서 추가 조정이 이어진다.) · "
           "「we realized that we might have overcorrected in this space and the team is investigating ways that we can increase chemistry flexibility」(이 영역에서 과잉 교정했을 수 있음을 깨달았고, 팀이 케미 유연성을 높일 방법을 조사하고 있다) · "
           "「the team is exploring bringing back individual challenges and their associated rewards for select SBCs with higher Item Score requirements.」(팀이 아이템 점수 요구치가 높은 일부 SBC에 개별 챌린지와 그 보상을 되돌리는 방안을 검토하고 있다.) · "
           "「we'll be introducing these changes gradually.」(이 변화들은 점진적으로 도입하겠다.)"),
 impact=("⑴ 진화 선택: 진화 상향 시점이 **Thunderstruck 캠페인**으로 특정됨 — 급하지 않은 진화 투입은 Thunderstruck 진화 카탈로그를 보고 결정할 근거(추론 · #110 ⑴ 보강). "
         "⑵ SBC: #110의 「개별 챌린지 보상 복귀 계획 없음」이 **고액 SBC 한정 복귀 검토**로 바뀜 — 시점 미정. "
         "⑶ 케미 유연성 확대 예고 — 리그·국가 테마 스쿼드 제약이 느슨해질 수 있음(시점 미정). "
         "⑷ 3선(CDM) 역할·포커스 동작 변경 언급 없음 · 아스톤 빌라 3선 정본 재검토 사유 아님. 오프사이드 트랩 남용은 EA 무응답 — 게임플레이 Q&A 쪽 후속을 본다."),
 source=URL + " (「FC 27 - FUT Developer Q&A Responses - November」 · 작성자 EA_Vendcera(EA 커뮤니티 매니저) · 2026-11-16 게시 · 공식 Discord FUT Q&A(11-13) 정리 14문답 · 2026-11-17 직접 열람)",
 confidence="A (EA 1차 — EA 커뮤니티 매니저가 개발자 답변을 정리한 공식 전사 · 2026-11-17 직접 열람) · 단일 공식 정리 · 대부분 「검토 중」·예고(Thunderstruck·시즌 3) — 실제 변경 미확인 · 인게임 영향 미실측",
 recorded=TODAY,
)
con = connect()
if con.execute("select 1 from game_system_changes where title=?", (ROW["title"],)).fetchone():
    sys.exit("이미 있음 — 건너뜀")
cols = ",".join(ROW); q = ",".join("?" * len(ROW))
cur = con.execute(f"insert into game_system_changes({cols}) values({q})", tuple(ROW.values()))
con.commit(); print("inserted id", cur.lastrowid)
