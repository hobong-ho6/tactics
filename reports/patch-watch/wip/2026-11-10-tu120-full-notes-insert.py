#!/usr/bin/env python3
"""2026-11-10 저녁 — EA 「Title Update v1.2.0」 전체 패치노트(11-10 게시 · 배포 완료) 적재.
오전 Pitch Notes 적재분(#99~#103)과 겹치지 않는 사실만 3행. INSERT만(불변규칙 2) · title로 중복 검사."""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from core.db import connect  # noqa: E402

TODAY = "2026-11-10"
SRC = "https://www.ea.com/games/ea-sports-fc/fc-27/news/fc27-title-update-v1-2-0 (「EA SPORTS FC 27 | Title Update v1.2.0」 전체 패치노트 · 2026-11-10 게시 · 「now live」)"
CONF = "A (EA 1차 · 2026-11-10 저녁 직접 열람 · 배포 완료 공지) · 인게임 적용은 미실측"
ROWS = [
 dict(area="positioning", title="TU 1.2.0 전체 노트 — 위치 수정은 「일부 상황 개선」 수준 · 킥오프 중앙 수비수",
  change="⭐ 전체 패치노트는 Pitch Notes(#100·#101)보다 **표현이 약하다**: 풀백 조기 하강·동료 오프사이드 모두 「Improved some cases」(일부 상황 개선)로 적었다 — Pitch Notes의 「훨씬 단단한 라인」은 프리뷰 표현이었다. 새로 드러난 항목: ⑴ 킥오프 직후 수비 라인이 박스 안으로 덜 물러서고 **수비수 한 명이 더 중앙에** 선다 ⑵ 특정 역습 상황에서 **박스 안 공격 AI 소폭 개선** ⑶ 버그: **패스가 나간 뒤 완료를 기다리며 동료가 침투를 멈추던 문제** 수정 ⑷ 버그: 헤딩 패스 뒤 조작 전환이 받는 선수로 넘어가지 않던 문제 수정(#101 루즈볼 전환과 같은 축).",
  evidence="「Improved some cases of fullbacks dropping too deep while defending.」(수비 중 풀백이 너무 깊이 내려가던 일부 상황을 개선했다.) · 「Improved some cases of AI teammates drifting offside.」(AI 동료가 오프사이드로 흘러가던 일부 상황을 개선했다.) · 「the defensive line will not drop back as far into the penalty box directly after a kick off and a defensive player will be lined up more centrally.」(킥오프 직후 수비 라인이 페널티 박스 안으로 그렇게 깊이 물러서지 않고, 수비수 한 명이 더 중앙에 선다.) · 「Teammates could sometimes stop their run after a pass is made while waiting for it to be completed.」(패스가 나간 뒤 완료를 기다리는 동안 동료가 침투를 멈추는 경우가 있었다.)",
  impact="⑴ #100의 「에메리 고라인·풀백 라인 유지 복원」 기대는 **「일부 상황」으로 낮춰 읽는다** — limit #30·obs#449 재판정은 여전히 패치 뒤 실측으로만 한다. ⑵ 패스 뒤 침투 정지 수정은 3-2-5 전방 5명의 오프더볼 침투에 유리한 방향(추론 · 미실측). ⑶ 3선(CDM) 역할·포커스 변경 언급 0. ⛔ 처방·정본 변경 없음.",
  source=SRC, confidence=CONF),
 dict(area="set_pieces", title="TU 1.2.0 코너 조준 표시 입력 지연·실 아웃 정지 버그 수정",
  change="세트피스·조작 버그 수정: ⑴ **온라인 경기에서 입력 지연이 코너킥 조준 표시에 영향**을 주던 문제 ⑵ [PC] 프리킥·코너에서 방향을 바꿀 때 표시가 늦게 움직이던 문제 ⑶ 드물게 **실 아웃(seal out) 동작 중 선수가 잠시 멈춰 서던** 문제 ⑷ 깊은 프리킥 뒤 수비 위치 이탈(#101과 같은 항목). 세트피스 전술 메뉴 「인원 추가·제거」(#83 미확인 목록) 설명은 **이번에도 없다**.",
  evidence="「Input delay could have impacted corner kick aiming indicators during online matches.」(온라인 경기 중 입력 지연이 코너킥 조준 표시에 영향을 줄 수 있었다.) · 「In rare cases, when performing a seal out, players could be temporarily frozen in place.」(드물게 실 아웃을 할 때 선수가 잠시 제자리에 멈출 수 있었다.)",
  impact="⑴ 11-10 이전 온라인 코너 조준 체감(빗나감)은 입력 지연 버그 가능성이 있어 패치 전 표본으로 분리한다. ⑵ AVL 세트피스 처방(코너 키커·타깃)은 그대로 — 조준 표시 수정이지 궤적 물리 변경이 아니다. ⑶ 3선 역할 무관.",
  source=SRC, confidence=CONF),
 dict(area="meta", title="TU 1.2.0 간소화 SBC 미선택 카드가 실제로 제출되던 버그 — 카드 반환",
  change="⭐ Pitch Notes(#102)는 간소화 SBC 문제를 「선택 안 한 카드가 선택된 것처럼 보인다」로 적었지만, 전체 노트는 **선택하지 않은 카드가 실제로 SBC에 들어갈 수 있었다**고 적었다 — 해당 카드는 **반환되고 대상자에게 인게임으로 연락**한다. 그 밖 FUT 수정: 새 전술이 잘못 저장돼 **선수가 엉뚱한 포지션으로 옮겨지던** 문제 · 전술 편집 변경이 저장되지 않던 문제(#102와 같은 축) · SBC 보관함 탭에 클럽 카드가 표시되던 문제 · 패스웨이 진화 보상 수령 뒤 메뉴가 로드되지 않던 문제 · 진화 보상 능력치 표시 오류(표시 전용).",
  evidence="「In certain situations when completing a Streamlined SBC, a Player Item that had not been selected for submission could have been added into the SBC.」(간소화 SBC를 완료할 때 제출하려고 선택하지 않은 선수 아이템이 SBC에 들어갈 수 있었다.) · 「Player Items impacted by this issue will be returned and affected players will be contacted in-game.」(이 문제로 영향을 받은 선수 아이템은 반환되며 대상자에게 인게임으로 연락한다.) · 「In some cases, new tactics could be saved incorrectly and some players could be moved into the wrong positions.」(새 전술이 잘못 저장돼 일부 선수가 엉뚱한 포지션으로 옮겨질 수 있었다.)",
  impact="⑴ 원장: 11-10 이전 간소화 SBC로 낸 세트에서 **의도하지 않은 카드가 사라졌다면** 이 버그일 수 있다 — EA 반환 카드는 다음 클럽 싱크에서 「처분 표시 되돌림」으로 잡힌다(원장 정정은 싱크 실측으로만). ⑵ 전술 저장 버그 수정 → 다음 싱크에서 `fut_squads` 포지션 배치가 의도와 같은지 재확인(#102 impact와 같은 조치). ⑶ 3선 역할 무관.",
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
