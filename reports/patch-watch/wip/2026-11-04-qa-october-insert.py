#!/usr/bin/env python3
"""2026-11-04 패치 감시 — EA Steam 공식 Q&A 정리 2건 적재.
⑴ 10-30 2차 게임플레이 Discord Q&A 정리(「Gameplay Developer Q&A Responses - October」 · 11-02 게시) 4행
⑵ FUT Developer Q&A 정리(10-14 게시 · 지금까지 검토 기록 없음) 2행
game_system_changes FC27 6행. INSERT만(불변규칙 2). 두 번 돌리면 중복 — 적재 전 change 앞 40자로 존재 검사."""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from core.db import connect  # noqa: E402

TODAY = "2026-11-04"
SRC_GP = "https://steamcommunity.com/app/4080220/discussions/0/565924099166300274/ (「FC 27 - Gameplay Developer Q&A Responses - October」 · 작성자 EA_Vendcera(EA 커뮤니티 매니저) · 2026-11-02 게시 · 공식 Discord 2차 게임플레이 Q&A(10-30) 정리 11문답)"
SRC_FUT = "https://steamcommunity.com/app/4080220/discussions/0/562544805318581878/ (「FC 27 - FUT Developer Q&A Responses」 · 작성자 EA_Vendcera(EA 커뮤니티 매니저) · 2026-10-14 게시 · 공식 Discord FUT Q&A 정리 21문답)"
CONF_GP = "A (EA 1차 — EA 커뮤니티 매니저가 개발자 답변을 정리한 공식 전사 · 2026-11-04 직접 열람) · 단일 공식 정리라 교차검증 대상 없음(번역본·현지어 정리 미발견)"
CONF_FUT = "A (EA 1차 — EA 커뮤니티 매니저가 개발자 답변을 정리한 공식 전사 · 2026-11-04 직접 열람) · 단일 공식 정리 · 일정 약속 없음"
ROWS = [
 dict(area="tactics",
  change="⭐⭐ EA 게임플레이 개발팀이 2차 Discord Q&A(10-30 · 11-02 게시 정리)에서 **수비 깊이 95 조사를 「게임플레이 팀의 현재 최우선 과제」라고 밝혔다** — 여러 접근을 **실제로 테스트 중**이다. 1차 Q&A(#69 · 10-09)의 「게임이 자리 잡을 시간을 두는 중」에서 **입장이 바뀌었다**. 다만 수비 접근(defensive approach)이 위치 시스템 전체와 묶여 있어 v1.2.0의 풀백 위치·오프사이드 인지 변경(#67)과 충돌하지 않게 신중히 시험한다고 했고 **일정은 없다**. 같은 Q&A에서 포메이션 다양성: FC26은 두 포메이션 쏠림, FC27은 UT 전체에서 **주로 8개 포메이션**이 쓰이고 상위 디비전에는 더 인기 있는 포메이션이 있다(EA 내부 데이터).",
  evidence="Q1 「Nerf 95 depth」(95 depth를 너프하라) · A1 「We are working on a few different approaches to make 95 depth feel balanced and fair for all players and we are currently testing them actively. This investigation is the top priority for the Gameplay team right now.」(95 depth가 모든 플레이어에게 균형 잡히고 공정하게 느껴지도록 몇 가지 다른 접근을 작업 중이며 현재 활발히 테스트하고 있다. 이 조사가 지금 게임플레이 팀의 최우선 과제다.) · 「we want to make sure that any changes we make to 95 depth don't affect the changes we've made to keep the defensive line solid」(95 depth에 가하는 변경이 수비 라인을 견고하게 유지하려고 한 변경에 영향을 주지 않도록 하려 한다) · A11 「In FC 27, our data shows players are predominantly using eight formations across the entire player base in Ultimate Team.」(FC27에서 우리 데이터는 얼티밋 팀 전체 플레이어가 주로 8개 포메이션을 쓰고 있음을 보여준다.) ⚠️ Q5의 「95 depth 상대 팀이 스태미나를 더 잃는다」는 질문자 주장이고 EA는 답하지 않았다 — D.",
  impact="⑴ **높은 라인 너프가 「검토」(#69)에서 「최우선·테스트 중」으로 올라갔다(A).** v1.2.0(#67)에 들어간다는 말은 없다 — 그 이후 패치 가능성이 크다(추론). ⑵ AVL FC27 전술 정본(`team_tactic_setups` #46 · Balanced/Balanced/라인 52)은 직접 대상이 아니다. 고라인·오프사이드 트랩 프리셋 강화 판단(보류 건)에는 #68·#69의 리스크 병기를 유지하고 **「다음 패치에서 깊이 상한·트랩 효율이 바뀔 공산이 더 커졌다」**로 강도를 올린다. ⑶ 포메이션 8종 분산은 메타 서술일 뿐 처방 근거가 아니다. ⑷ 3선(CDM) 역할·포커스 언급 0 → 3선 정본 재검토 사유 아님. ⛔ 처방·정본 변경 없음(#45 원칙 — 패치 적용 확인 전 바꾸지 않는다).",
  source=SRC_GP, confidence=CONF_GP),
 dict(area="engine",
  change="EA 2차 Discord Q&A(10-30)의 패스·전환 답변: ⑴ **땅볼 패스가 리시버를 예상 밖 방향으로 리드하는 경우**와 **측면으로 가로지르는 스루 패스가 예상과 다른 리시버를 겨냥하는 경우**를 인정하고 조사 중(저수준 패스 시스템이라 신중) ⑵ **스루 패스 보정 축소(#71) 때문에 플레이어가 스루 패스를 덜 쓰고 드리븐(핑) 패스를 더 쓰는** 밸런스 이동을 EA가 데이터로 확인하고 감시 중 — 패스 튜닝 약속은 없음 ⑶ 선수 전환은 L1/LB와 오른쪽 스틱을 **별개 메커니즘으로 따로 조사** 중(v1.2.0의 루즈볼 전환 수정 #67과 별개). 모두 일정 없음.",
  evidence="A2 「We do see some cases where ground passes lead the receiver in an unexpected way, and some cases where through passes made laterally across the pitch target a different receiver than expected.」(땅볼 패스가 리시버를 예상 밖 방식으로 리드하는 경우와, 측면으로 가로지르는 스루 패스가 예상과 다른 리시버를 겨냥하는 경우가 실제로 있다.) · A4 「Because of the changes to through pass assistance in FC 27, players are using through passes less and driven passes more, which is a shift in game balance that we are monitoring closely.」(FC27의 스루 패스 보정 변경 때문에 플레이어가 스루 패스를 덜, 드리븐 패스를 더 쓰고 있고, 이는 우리가 면밀히 감시하는 게임 밸런스 이동이다.) · A5 「Right stick switching works differently from L1/LB switching, so we have to approach these two mechanics independently in our investigations.」(오른쪽 스틱 전환은 L1/LB 전환과 다르게 작동하므로 두 메커니즘을 조사에서 따로 다뤄야 한다.)",
  impact="⑴ #71(스루 패스 수동화 · FC26→FC27 버전 차이)의 **결과가 EA 데이터로 확인됐다**(A) — 에메리식 수직 전환을 FC27에서 재현할 때 **스루 패스보다 드리븐 패스(핑드 패스 · #22·#60 PlayStyle 축)가 실효 수단**이라는 판단을 지지한다. 다만 핑 패스 너프 요구가 있고 EA가 「감시 중」이라 패치 리스크가 있다. ⑵ 측면 가로지르는 스루 패스의 리시버 오지정은 측면 전환 처방(Wide 빌드업)을 실행할 때의 조작 리스크로만 기록한다. ⑶ 3선 역할 무관.",
  source=SRC_GP, confidence=CONF_GP),
 dict(area="goalkeeping",
  change="EA 2차 Discord Q&A(10-30)에서 **니어포스트 슛이 일부 각도에서 지나치게 효과적**이라고 인정하고 **슈팅과 GK 위치잡기 양쪽**에서 관련 해법을 작업 중이라고 답했다(일정 없음). #68의 「슈팅 정확도·GK 위치잡기」 조사 항목의 구체 증상이며 **v1.2.0 항목에는 없다**.",
  evidence="Q3 「So no nerf to low driven near post?」(그럼 낮게 깔아 차는 니어포스트 슛 너프는 없나?) · A3 「We are aware that near post shots are too effective from some angles and we are working on some related solutions in both shooting and goalkeeper positioning to address this.」(일부 각도에서 니어포스트 슛이 지나치게 효과적이라는 것을 알고 있으며, 이를 해결하려고 슈팅과 골키퍼 위치잡기 양쪽에서 관련 해법을 작업 중이다.)",
  impact="⑴ FC27 v1.1.0 시점 **GK 니어포스트 약점은 EA 인정 사실(A)** — #73(EA 1차 자료의 GK 변경 서술 0건)·#78(FC26 TU 1.1.0의 니어포스트 반응 개선 전례)과 함께 본다. 수정 전까지 GK 카드 비교에서 니어포스트 실점은 **카드 차이보다 엔진 공통 약점**일 수 있다. ⑵ GK 선택·진화 처방은 바꾸지 않는다(수정 예고 · 일정 없음). ⑶ 3선 역할 무관.",
  source=SRC_GP, confidence=CONF_GP),
 dict(area="attributes",
  change="EA 2차 Discord Q&A(10-30)에서 **공격수가 수비수보다 태클·인터셉트를 잘하는 등 포지션에 비해 지나치게 효과적인 상황**을 해결하려고 「적극적으로 작업 중」이라고 답했다(설계 원칙: 선수는 실제 포지션에 맞게 느껴져야 한다). 키 큰 선수와 작은 선수의 몸싸움 균형도 다시 조사 중이라고 했다(#70의 후속 · 같은 입장 반복). 일정 없음.",
  evidence="A6 「One of the design principles we have every year is that players should feel appropriate for the position they play in the real world.」(매년 지키는 설계 원칙 하나는 선수가 실제로 뛰는 포지션에 맞게 느껴져야 한다는 것이다.) · 「When we have situations where players are more effective than expected, like attackers making tackles, it is something we want to address.」(공격수가 태클을 해내는 것처럼 선수가 기대보다 효과적인 상황이 있으면 우리가 고치고 싶은 부분이다.) · A8 「We are currently investigating the balance of tall vs. short players, especially in physical challenges.」(특히 몸싸움에서 키 큰 선수와 작은 선수의 균형을 현재 조사하고 있다.)",
  impact="⑴ #46(저수비 스탯 선수의 자동 인터셉트)에 대해 1차 Q&A(#71)는 「균형을 익히는 중」이라는 일반론이었는데, 이번에는 **「적극 작업 중」으로 수정 의사를 밝혔다(A · 일정 없음)**. ⇒ #46 impact(한시적)의 「수정 예고 없음」은 **「수정 의사 표명 · 일정 없음」으로 읽는다**(기존 행은 고치지 않고 이 행으로 덧붙인다). ⑵ 3선(CDM) 함의: 수정이 들어가면 **수비 스탯(인터셉트·태클·수비 인지)의 상대 가치가 오른다** — 볼 탈취형 3선(카마라 dm_holding/Defend)에 불리하지 않은 방향이다. 단 역할·포커스 동작 변경이 아니므로 **3선 정본 재검토 사유는 아니다**(사용자 판단 사안 · 정본 변경 없음). ⑶ 체격 균형은 #70 결론(힘만 보는 피지컬 진화 가성비 한 단계 낮춤) 유지.",
  source=SRC_GP, confidence=CONF_GP),
 dict(area="evolution",
  change="EA FUT Q&A(10-14 게시 정리)에서 **FC27 진화 상향 폭을 지나치게 줄였다고 인정했다** — FC26에서 진화 쪽으로 쏠린 균형을 출시 때 의도적으로 낮췄는데 「너무 많이 당긴 것 같다」고 했고, 목표는 **평균 플레이어 스쿼드에 진화 카드 몇 장이 늘 있는 상태**라고 밝혔다. 또 예년처럼 시즌이 진행되면서 **동시 진행 진화 슬롯 수를 늘릴 계획**이다(일정 없음).",
  evidence="A2 「in FC26, we felt that balance had shifted too heavily towards Evolutions, so we made some changes at launch to give other progression systems, including the Transfer Market and campaigns, more room to shine. That said, we recognize that we've likely pulled back a bit too far.」(FC26에서는 균형이 진화 쪽으로 너무 기울었다고 느껴 출시 때 이적 시장·캠페인 등 다른 성장 경로가 빛날 여지를 주도록 바꿨다. 다만 아마 너무 많이 당긴 것 같다고 인정한다.) · 「We think the ideal balance is that the average player has a few Evolutions in their squad at any given time.」(이상적인 균형은 평균적인 플레이어의 스쿼드에 언제나 진화 카드가 몇 장 있는 상태라고 본다.) · A7 「we have plans to increase the number of Evolutions you can have active and make progress on simultaneously as the year goes on.」(시즌이 진행되면서 동시에 활성화·진행할 수 있는 진화 수를 늘릴 계획이 있다.)",
  impact="⑴ ⭐ 버전 차이(A): **FC27 진화는 FC26보다 의도적으로 약하게 출발**했다 — FC26 진화 처방·가성비 판단을 FC27로 전용하지 않는다. ⑵ EA가 상향 의사를 밝혔다 → 시즌 중반 이후 진화 카탈로그의 상한이 올라갈 공산이 있다(추론). 지금 약한 진화에 핵심 카드를 소모하는 판단은 「더 강한 진화가 나올 수 있다」를 리스크로 병기한다. ⑶ 진화 슬롯 확대는 진행 동시성 계획에 영향(일정 없음). 3선 역할 무관.",
  source=SRC_FUT, confidence=CONF_FUT),
 dict(area="tactics",
  change="EA FUT Q&A(10-14 게시 정리)에서 **경기 중 커스텀 전술을 바꿀 때 선수 포지션이 바뀌는 버그**(FUT·감독 커리어에서 새 포메이션으로 전환할 때 선수가 제자리를 벗어나 배치됨)를 「레이더에 있다 · 해결 방법을 보고 있다」고 인정했다(일정 없음). v1.1.0(#64)의 **새 전술 저장 버그 수정과는 다른 증상**이다(저장이 아니라 경기 중 전환).",
  evidence="Q11 「Fix the issue where players change positions when switching between Custom Tactics during a match in Ultimate Team」(얼티밋 팀에서 경기 중 커스텀 전술을 전환하면 선수 포지션이 바뀌는 문제를 고쳐 달라) · A11 「This is on our radar, and we're looking into how we can address it.」(이 문제를 인지하고 있으며 어떻게 해결할지 살펴보고 있다.) · Q14 「happens to me on manager career and fut whenever I switch to new formations」(감독 커리어와 FUT에서 새 포메이션으로 바꿀 때마다 일어난다) · A14 같은 답.",
  impact="⑴ AVL 경기 프리셋(`match_game_setups`)처럼 **경기 중 커스텀 전술을 갈아끼우는 운용**에서 전환 직후 선수 배치가 정본과 어긋날 수 있다(A · v1.1.0 수정 대상 아님). ⇒ 전환 직후 포메이션 화면에서 슬롯을 확인하는 절차를 권장으로 병기한다. ⑵ 3선 함의: 전환 시 RDM/LDM 자리가 뒤바뀌면 카마라(RDM dm_holding/Defend)·고메스(LDM dm_dlp/Roaming) 배치가 뒤집힐 수 있다 — **역할 동작 변경이 아니라 배치 버그**이므로 정본 재검토 사유는 아니다(정본 변경 없음). ⑶ 이 행은 10-14 게시 글을 11-04에야 검토한 것이다 — Steam Q&A 고정글은 EA 뉴스 색인 밖이라 `patch_watch_index.py`가 잡지 못한다.",
  source=SRC_FUT, confidence=CONF_FUT),
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
