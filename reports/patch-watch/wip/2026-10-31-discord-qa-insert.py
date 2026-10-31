#!/usr/bin/env python3
"""2026-10-31 패치 감시 — EA 게임플레이 Discord Q&A 적재(스케줄 회차 fc27-discord-qa-1030-collect).
10-30 회차 전사는 10-31 현재 공개 경로에 없다 → **1차 게임플레이 Q&A(EA 커뮤니티 매니저가 Steam에 올린 공식 정리 · 10-09 게시)** 를 적재한다.
game_system_changes FC27 3행. INSERT만(불변규칙 2). 두 번 돌리면 중복 — 적재 전 change 앞 40자로 존재 검사."""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from core.db import connect  # noqa: E402

TODAY = "2026-10-31"
SRC = "https://steamcommunity.com/app/4080220/discussions/0/588440114694207040/ (「FC 27 - Gameplay Developer Q&A Responses」 · 작성자 EA_Vendcera(EA 커뮤니티 매니저) · 2026-10-09 17:12 UTC 게시 · 공식 Discord 1차 게임플레이 Q&A 정리)"
CONF = "A (EA 1차 — EA 커뮤니티 매니저가 개발자 답변을 정리한 공식 전사 · 2026-10-31 직접 열람) · ⚠️ 10-30 2차 Q&A가 아니라 **10-09 게시 1차 Q&A**다 · 단일 공식 정리라 교차검증 대상 없음(번역본·현지어 정리 미발견)"
ROWS = [
 dict(area="tactics",
  change="⭐⭐ EA 게임플레이 개발팀이 1차 Discord Q&A(10-09 게시 정리)에서 **커뮤니티의 「수비 깊이 95」 질문에 직접 답했다** — 오프사이드 트랩 남용을 막는 방법과 **수비 라인 깊이 재조정**을 보고 있지만, 대응법을 익힌 플레이어가 있고 밸런스 영향이 커서 **안정화 시간을 두는 중**이라고 했다(일정 없음). 같은 Q&A에서 ⑴ 풀백 라인 문제는 **「잠재적 해법을 찾아 테스트 중」**(10-09 시점 — 이것이 #67의 v1.2.0 풀백 항목으로 나왔다) ⑵ 킥오프는 **킥오프 직후 수비 라인이 얼마나 깊이 내려가는지** 감시 중이라고 답했다(#67 킥오프 항목의 원인 서술). ⇒ #68 「high defensive lines」(높은 수비 라인) 조사 항목과 **같은 축일 가능성이 높다**(EA가 두 글을 직접 연결하지는 않았다 — 연결은 추론).",
  evidence="질문 요지(Q7): 수비 깊이 95를 계속 유지해도 스태미나가 줄지 않는다. · 「We are looking at ways to prevent spamming offside traps as well as rebalancing the depth of the defensive line.」(오프사이드 트랩 남용을 막는 방법과 수비 라인 깊이를 재조정하는 방법을 보고 있다.) · 「We've seen certain players learn how to counter this strategy, so, because making a change here would also impact the balance of the game, we are giving time for the game to settle.」(일부 플레이어가 이 전략에 대응하는 법을 익히는 것을 봤고, 여기를 바꾸면 게임 밸런스에도 영향을 주므로 게임이 자리 잡을 시간을 두고 있다.) · Q4 「We have already identified a potential solution and we are currently testing it.」(이미 잠재적 해법을 찾았고 현재 테스트 중이다.) · Q2 「we are monitoring how deep the defensive line can drop after kick off」(킥오프 뒤 수비 라인이 얼마나 깊이 내려갈 수 있는지 감시하고 있다). ⚠️ 95 depth의 **스태미나 비소모 여부 자체에는 답하지 않았다** — 「95에서도 스태미나가 안 준다」는 질문자 주장이고 D(통설)로 둔다.",
  impact="⑴ **높은 라인·오프사이드 트랩 너프가 EA 개발자 입으로 확인된 검토 항목이 됐다(A · 일정 없음).** AVL FC27 전술 정본(`team_tactic_setups` #46 · Balanced/Balanced/라인 52)은 직접 대상이 아니다. 단 에메리 재현의 **오프사이드 트랩(높은 라인 + 라인 일제 전진)** 을 FC27에서 고라인 프리셋으로 강화하려는 판단(보류 5건 · `optimal:lead` 등)에는 「후속 패치에서 깊이 상한·트랩 효율이 깎일 수 있다」를 리스크로 병기한다(#68과 같은 결론을 A 근거로 보강). ⑵ 커뮤니티 95 depth 메타·「95에서 스태미나 비소모」는 D — 처방 근거로 쓰지 않는다. ⑶ 풀백 해법이 10-09에 이미 테스트 중이었다는 점은 #67(v1.2.0) 적용 가능성을 높이지만, 처방·`team_tactic_setups` 정본은 **패치 적용 확인 전 바꾸지 않는다**(#45 원칙).",
  source=SRC, confidence=CONF),
 dict(area="attributes",
  change="EA가 1차 Discord Q&A(10-09 게시 정리)에서 **「작고 가벼운 선수가 크고 힘센 선수를 공에서 밀어내는」 경우가 있다**고 인정하고 더 현실적인 균형을 검토 중이라고 답했다(질문은 여성 선수 키·민첩 대비 힘 문제). #68의 「체격·피지컬이 다른 선수 간 충돌 처리」 조사 항목의 구체 증상이다 — **v1.2.0 항목에는 없다**.",
  evidence="「In some instances a shorter, lighter player would push a taller, stronger player away from the ball.」(어떤 경우에는 더 작고 가벼운 선수가 더 크고 힘센 선수를 공에서 밀어낸다.) · 「We are currently looking into creating a more realistic balance in those situations.」(그런 상황에서 더 현실적인 균형을 만드는 것을 검토하고 있다.)",
  impact="⑴ FC27 현행(v1.1.0) 엔진에서 **힘(Strength)·키·체중의 몸싸움 우위가 기대만큼 작동하지 않는 경우가 있다**는 EA 인정(A · 「some instances」(어떤 경우에는) — 빈도·조건 미공개). ⇒ 진화 선택에서 **힘 증가만을 근거로 한 피지컬 진화의 가성비**는 수정 전까지 한 단계 낮춰 본다(docs/22 §2.1의 FC26 근거를 FC27에 전용할 때 이 행을 병기). ⑵ AVL 처방에서 체격형 선수(타깃형 ST·CB 몸싸움)의 역할 판단은 **바꾸지 않는다** — 증상 범위가 불명확하고 수정이 예고돼 있다. 수정 패치가 나오면 docs/22와 진화 처방을 다시 본다.",
  source=SRC, confidence=CONF),
 dict(area="engine",
  change="EA 1차 Discord Q&A(10-09 게시 정리)의 조작·AI 답변: ⑴ **FC27 스루 패스는 FC26보다 수동화**됐다(FC26은 보정이 커서 역습 기회가 과다) · 땅볼 패스도 튜닝이 약간 다르며 데이터상 플레이어가 인터셉트와 패스의 균형을 익히는 중 ⑵ **드리블은 역대 가장 반응이 빠르고**, 상위 숙련도에서 비현실적 사용(연속 방향 전환)이 나온다 — 반응성을 전반적으로 낮추지 않는 해법을 논의 중 ⑶ 선수 전환(오른쪽 스틱·L1)은 계속 개선 탐색 ⑷ Authentic 모드 CPU 공격 빈약 피드백을 검토 중. 모두 **일정 없음**.",
  evidence="「In FC26 through passes were more assisted creating too many counter attack opportunities. Through passes are now more manual to create more opportunities for users to express their skill.」(FC26에서는 스루 패스 보정이 더 커서 역습 기회가 너무 많았다. 이제 스루 패스는 더 수동이 되어 사용자가 실력을 드러낼 기회가 늘었다.) · 「our data shows that players are learning the balance between interceptions and passing」(데이터는 플레이어들이 인터셉트와 패스 사이의 균형을 익히고 있음을 보여준다) · 「in FC27 Dribbling is the most responsive ever. However, at a certain skill level Dribbling is so responsive that it allows the users to use the mechanic in unrealistic ways.」(FC27의 드리블은 역대 가장 반응이 빠르다. 다만 일정 숙련도에서는 반응이 너무 빨라 비현실적인 방식으로 쓸 수 있다.) · 「We are currently discussing potential solutions that don't reduce the responsiveness in general.」(반응성을 전반적으로 낮추지 않는 해법을 논의 중이다.)",
  impact="⑴ ⭐ 버전 차이(A): **스루 패스 보정 축소는 FC26→FC27 변경** — FC26 시절 「스루 패스 역습」 근거를 FC27 처방에 전용하지 않는다. 에메리 재현의 수직 전환(라인 사이 → 침투 스루)은 FC27에서 **조작 정확도에 더 의존**한다. ⑵ 저수비 스탯 인터셉트(#46)에 대해서는 「균형을 익히는 중」이라는 일반론뿐 — **수정 예고가 아니다** → #46 impact(한시적 · 수정 예고 없음) 유지. ⑶ 드리블·전환·Authentic AI는 AVL 전술 처방과 직접 관계 없음(조작·모드 축) — 기록만 한다.",
  source=SRC, confidence=CONF),
]

con = connect()
for r in ROWS:
    dup = con.execute("SELECT id FROM game_system_changes WHERE substr(change,1,40)=?", (r["change"][:40],)).fetchone()
    if dup:
        print("건너뜀(이미 있음) #", dup[0]); continue
    cur = con.execute("INSERT INTO game_system_changes(game_version,area,change,evidence,impact,source,confidence,recorded) VALUES('FC27',?,?,?,?,?,?,?)",
                      (r["area"], r["change"], r["evidence"], r["impact"], r["source"], r["confidence"], TODAY))
    print("적재 #", cur.lastrowid, r["area"])
con.commit()
