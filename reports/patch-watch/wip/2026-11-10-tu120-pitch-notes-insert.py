#!/usr/bin/env python3
"""2026-11-10 패치 감시 — EA 「Title Update v1.2.0 Pitch Notes」(11-09 게시 · 11-10 배포 시작) 적재.
game_system_changes FC27 5행. INSERT만(불변규칙 2). 두 번 돌리면 중복 — 적재 전 title로 존재 검사."""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from core.db import connect  # noqa: E402

TODAY = "2026-11-10"
SRC = "https://www.ea.com/games/ea-sports-fc/fc-27/news/update-v1-2-pitch-notes (「EA SPORTS FC 27 | Title Update v1.2.0 Pitch Notes」 · 2026-11-09 게시 · 11-10 배포 시작)"
CONF = ("A (EA 1차 · 2026-11-10 직접 열람) · 프리뷰 성격의 Pitch Notes — 전체 패치노트(11-10 예정)는 이 회차에 열람하지 못함"
        "(forums.ea.com 403) · 배포 직후라 인게임 적용은 미실측")
ROWS = [
 dict(area="tactics", title="TU 1.2.0 수비 깊이 95 너프 — 극단 고라인이 더 빨리 내려선다",
  change="⭐⭐ v1.2.0과 함께 **라이브 튜닝으로 극단적인 수비 라인 높이(95 depth)의 수비수 위치를 조정**했다 — 수비수가 **더 일찍 내려서되**, 다른 전술보다는 여전히 높은 라인을 유지한다. #85(「최우선 과제 · 일정 없음」)가 **v1.2.0 시점에 실제로 반영됐다**. 타이틀 업데이트 파일이 아니라 서버 쪽 라이브 튜닝이다.",
  evidence="「we've adjusted how defenders position themselves with extreme defensive line heights. Defenders will now drop off sooner while still maintaining a higher line than other tactics.」(극단적인 수비 라인 높이에서 수비수가 자리 잡는 방식을 조정했다. 이제 수비수는 더 일찍 내려서면서도 다른 전술보다 높은 라인을 유지한다.) · 「Note that this will be released as a Live Tuning Update alongside Title Update v1.2.0.」(이 변경은 v1.2.0과 함께 라이브 튜닝 업데이트로 배포된다.) · 수치(어느 깊이부터 「극단」인지)는 밝히지 않았다.",
  impact="⑴ AVL FC27 전술 정본(`team_tactic_setups` #46 · Balanced/Balanced/라인 52)은 「극단」 구간이 아니라 **직접 대상이 아닐 공산이 크다**(EA가 경계값을 밝히지 않음 — 추론). ⑵ #68·#69·#85에서 병기한 「고라인·오프사이드 트랩 프리셋 강화 리스크」가 **현실화됐다** — 보류 중인 High 쪽 국면 프리셋 판단은 패치 뒤 실측으로만 한다. ⑶ 상대가 95 depth를 쓰는 경기의 체감(빌드업이 막히는 정도)이 바뀌므로 11-10 이후 인게임 관측을 이전 표본과 섞지 않는다. ⑷ 3선(CDM) 역할·포커스 언급 0. ⛔ 처방·정본 변경 없음.",
  source=SRC, confidence=CONF),
 dict(area="positioning", title="TU 1.2.0 풀백 라인 유지·오프사이드 인지 개선 반영",
  change="⭐⭐ #67 예고 5항목 중 위치 항목이 **v1.2.0에 실제로 들어갔다**: ⑴ 수비 시 **풀백이 너무 깊이 내려가던 동작을 고쳐 훨씬 단단한 수비 라인을 유지**한다(#45·#57의 수정) ⑵ 공격수가 **상대 수비 라인을 더 잘 읽고 온사이드를 유지하는 침투**를 한다 ⑶ AI 동료가 **박스 주변 공간을 노리는 목적 있는 지원 침투**를 더 한다. 오프사이드 자체를 없애려는 것이 아니라 공격 기회를 늘리려는 조정이라고 밝혔다.",
  evidence="「fullbacks would sometimes drop too deep while defending. We've adjusted and improved this behaviour so fullbacks now hold a much firmer and solid defensive line.」(풀백이 수비 중 가끔 너무 깊이 내려갔다. 이 동작을 조정·개선해 이제 풀백은 훨씬 단단하고 견고한 수비 라인을 유지한다.) · 「your attacking players will now do a better job at reading the opponent's defensive line, and make more effective runs to stay onside.」(공격수는 이제 상대 수비 라인을 더 잘 읽고 온사이드를 유지하는 더 효과적인 침투를 한다.) · 「AI teammates will make more purposeful supporting runs and better capitalise on space around the box.」(AI 동료는 더 목적 있는 지원 침투를 하고 박스 주변 공간을 더 잘 활용한다.)",
  impact="⭐ **#67 impact의 「v1.2.0 전후 경계」가 확정됐다(11-10).** ⑴ 에메리 재현 전제(높은 라인 + 풀백 라인 유지)가 엔진에서 복원될 근거(A) — limit #30(LB att_wb vs 윙백 유보)·obs#449 양 풀백 판정·FC27 슬롯 정본 보류 중 「LB 저점유 운용」은 **패치 뒤 실측으로 재판정**한다. ⑵ 11-10 이전 인게임 캡처·관측은 **패치 전 기준선**으로 따로 둔다. ⑶ 상대 공격수의 온사이드 침투 개선은 AVL 오프사이드 트랩 효율을 떨어뜨릴 수 있다(추론 · 실측 전 처방 근거로 쓰지 않음). ⑷ 3선(CDM) 역할·포커스 변경은 없다 — 풀백·공격수·지원 침투 한정. ⛔ 처방·`team_tactic_setups` 정본은 실측 전 바꾸지 않는다(#45 원칙).",
  source=SRC, confidence=CONF),
 dict(area="positioning", title="TU 1.2.0 킥오프 라인·딥 프리킥 위치·루즈볼 전환 수정",
  change="v1.2.0 재개 국면·조작 수정 3건: ⑴ **킥오프 직후 수비 라인이 조금 더 높게** 선다 — 킥오프에서 곧장 박스로 드리블하는 상대를 막기 쉬워진다(#67 ⑷ 반영) ⑵ 버그 수정: **깊은 위치의 프리킥 뒤 수비수가 제자리를 벗어나 있던 문제** 수정(세트피스) ⑶ **루즈볼 자동 전환** 개선 — 동료의 슬라이딩 태클 직후, 헤딩 패스 뒤, 슛이 빗나간 뒤(#67 ⑸ 반영). L1/LB·오른쪽 스틱 전환 별도 조사(#86)는 이번에 언급 없음.",
  evidence="「The defensive line now holds a slightly higher position right after kick-off, making it easier to defend against opponents looking to dribble directly into the box.」(킥오프 직후 수비 라인이 조금 더 높은 위치를 유지해, 곧장 박스로 드리블하려는 상대를 막기 쉬워진다.) · 「Fixed an issue where defenders would be out of position after a deep free kick.」(깊은 프리킥 뒤 수비수가 제자리를 벗어나 있던 문제를 고쳤다.) · 「improved auto-switching across several loose ball scenarios, including after a teammate completes a slide tackle, following a headed pass, and after a shot misses the target.」(동료가 슬라이딩 태클을 마친 뒤, 헤딩 패스 뒤, 슛이 빗나간 뒤 등 여러 루즈볼 상황의 자동 전환을 개선했다.)",
  impact="⑴ 킥오프 실점(#57 재확인 항목)은 패치 뒤 다시 센다. ⑵ 깊은 프리킥 뒤 수비 위치 버그는 세트피스 수비 관측을 패치 전후로 나눠야 한다는 뜻 — 세트피스 메뉴 「인원 추가·제거」(#83 미확인 목록) 설명은 **이번에도 없다**. ⑶ 3선 역할 무관.",
  source=SRC, confidence=CONF),
 dict(area="meta", title="TU 1.2.0 얼티밋팀 전술·라인업 저장 버그 수정",
  change="v1.2.0 얼티밋팀 수정: ⑴ **전술(Tactics)·라인업 편집 화면에서 전술 설정이나 교체가 저장·표시되지 않던 여러 버그** 수정 ⑵ 다중 선택 진화의 최종 확인 팝업에 취소 옵션이 없던 문제 수정 ⑶ 일부 진화 완료 시 3단계 모두 능력치 증가가 +0으로 보이던 **표시 전용** 버그 수정(실제 상승분은 정상 적용됐었다) ⑷ 간소화 SBC에서 선택하지 않은 카드가 선택된 것처럼 보이던 표시 버그 수정.",
  evidence="「Resolved several issues on the Tactics and Edit Lineup screens, including bugs that prevented tactical setups or player substitutions from saving or displaying correctly.」(전술·라인업 편집 화면의 여러 문제를 해결했다 — 전술 설정이나 선수 교체가 제대로 저장·표시되지 않던 버그 포함.) · 「This was only a visual issue and did not impact the earned upgrades.」(이는 표시 문제일 뿐이었고 얻은 업그레이드에는 영향이 없었다.)",
  impact="⑴ 11-10 이전에 클럽 싱크·인게임에서 「전술 공유 코드는 맞는데 경기에서 다르게 뛴다」류 관측이 있었다면 **저장 버그 가능성**을 함께 적는다(경기 중 전술 전환 포지션 버그 #90과는 별개 항목 — 그쪽 수정 언급은 이번에 없다)(사후 판정 근거로는 쓰지 않는다). 패치 뒤 첫 싱크에서 `fut_squads` 전술이 저장값과 일치하는지 재확인한다. ⑵ 진화 +0 표시는 실제 상승에 영향이 없으므로 원장(fut_evo_*) 정정 사유가 아니다. ⑶ 3선 역할 무관.",
  source=SRC, confidence=CONF),
 dict(area="tactics", title="전술 다양성 평가에 단서 — 상위권 쏠림 인정 · 어센틱 마킹 슬라이더",
  change="⑴ EA가 #68·#85의 「포메이션 승률 고른 분포·FC26보다 다양」 평가에 **단서를 달았다** — 그 판단은 **작년 같은 시기 FC26 경기 데이터와의 비교**였고, 실축처럼 **특히 상위권에서는 흔한 전술을 공유하는 것이 자연스럽다**고 인정했다. 전술 정체성과 경쟁 균형의 조정은 계속 감시한다(구체 조치 없음). ⑵ 어센틱 게임플레이: **팀 위치잡기 마킹 슬라이더 50 초과 값이 종전보다 더 느슨하게 압박**하도록 조정, 우천 시 볼 물리(터치가 너무 무겁던 것) 조정 ⑶ 버그: 킥오프·토너먼트·커리어의 CPU **수비 공격성 슬라이더**가 제대로 작동하지 않던 문제 수정.",
  evidence="「Our initial assessment was based on a comparison of FC 26 match data during the same time last year.」(처음 평가는 작년 같은 시기 FC26 경기 데이터와의 비교에 근거했다.) · 「just like real-world football, players can naturally share common tactics on the pitch, especially at higher levels.」(실제 축구처럼, 특히 높은 수준에서는 플레이어들이 자연스럽게 흔한 전술을 공유할 수 있다.) · 「settings above 50 result in a more relaxed approach when closing down attackers compared to before.」(50을 넘는 설정은 종전보다 공격수에게 다가가는 압박이 더 느슨해진다.)",
  impact="⑴ #68 impact ⑵의 「포메이션 승률 평준화 → 메타 포메이션으로 바꿀 근거 약함」은 **EA 자신이 FC26 상대 비교라고 범위를 좁혔으므로** 강도를 낮춰 읽는다 — 다만 실축 재현 포메이션을 유지한다는 원칙은 그대로. ⑵ 어센틱 슬라이더·CPU 슬라이더는 FUT 대전과 무관 — 커리어·오프라인 관측에만 해당. ⑶ 3선 역할 무관.",
  source=SRC, confidence=CONF),
]

con = connect()
added = []
for r in ROWS:
    if con.execute("SELECT 1 FROM game_system_changes WHERE title=?", (r["title"],)).fetchone():
        print("SKIP 존재:", r["title"]); continue
    cur = con.execute("INSERT INTO game_system_changes(game_version,area,title,change,evidence,impact,source,confidence,recorded)"
                      " VALUES('FC27',?,?,?,?,?,?,?,?)",
                      (r["area"], r["title"], r["change"], r["evidence"], r["impact"], r["source"], r["confidence"], TODAY))
    added.append((cur.lastrowid, r["title"]))
con.commit()
for i, t in added:
    print(f"#{i} {t}")
