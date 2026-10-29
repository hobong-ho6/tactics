#!/usr/bin/env python3
"""2026-10-29 패치 감시 — EA Gameplay Developer Notes(October · 10-28) 적재.
game_system_changes FC27 2행. INSERT만(불변규칙 2). 두 번 돌리면 중복 — 적재 전 change 앞 40자로 존재 검사."""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from core.db import connect  # noqa: E402

TODAY = "2026-10-29"
SRC = "https://www.ea.com/games/ea-sports-fc/fc-27/news/fc27-october-gameplay-developer-notes (2026-10-28)"
LOC = "⚠️ ko·de·ja 로케일도 영어 본문만 제공 — 다국어 교차검증 불가(불변규칙 10 예외 사유 · #57·#63과 같음)."
ROWS = [
 dict(area="positioning",
  change="⭐⭐ EA October Gameplay Developer Notes(10-28) — 출시 후 **첫 게임플레이 밸런스 변경을 TU v1.2.0(11월 중순 · 정확한 날짜 미정)으로 예고**했다. 5항목: ⑴ **풀백이 수비 라인을 더 일관되게 유지**하고 실제 공격 위협이 있을 때만 침투를 따라간다(#45·#57의 수정) ⑵ 공격수의 **오프사이드 인지** 개선(라인을 읽고 온사이드 침투) ⑶ 공격 AI가 박스 주변 빈 공간으로 더 결단력 있게 지원 침투 ⑷ **킥오프 직후 수비 라인을 더 높게 유지**(킥오프 골 감소) ⑸ 루즈볼 자동 스위칭 수정(슬라이드 태클 뒤·헤딩 패스 뒤·빗나간 슛 뒤). ⚠️ **예고이지 적용이 아니다** — 10-29 현재 엔진은 v1.1.0 그대로(#63).",
  evidence="「Our next Title Update in mid-November will introduce our first set of gameplay balance changes for FC 27.」(11월 중순 다음 타이틀 업데이트가 FC 27의 첫 게임플레이 밸런스 변경을 도입한다.) · 「Fullbacks will hold their defensive line more consistently, moving to track runs when there's a genuine attacking threat.」(풀백은 수비 라인을 더 일관되게 유지하고, 실제 공격 위협이 있을 때 침투를 따라 움직인다.) · 「this behaviour may still occur occasionally, but overall consistency has been noticeably improved」(이 동작은 여전히 가끔 일어날 수 있지만 전체적인 일관성은 눈에 띄게 개선됐다) · 「the defensive line will hold a higher position after kick-off」(킥오프 뒤 수비 라인이 더 높은 위치를 유지한다) · 「we've refined attacking awareness to help attackers better recognise the defensive line」(공격수가 수비 라인을 더 잘 인식하도록 공격 인지를 다듬었다). " + LOC,
  impact="⭐ **v1.2.0 적용 전후가 갈리는 경계가 생긴다.** ⑴ #45·#57의 풀백 조기 하강이 고쳐지면 에메리 재현의 전제(높은 라인 + 풀백 라인 유지)가 엔진에서 복원된다 → limit #30(LB att_wb vs 윙백 유보)·obs#449 양 풀백 판정·FC27 슬롯 정본 보류 중 「LB 저점유 운용」은 **패치 뒤 실측으로 재판정**하고, 패치 전 표본과 섞지 않는다. ⑵ HANDOFF P1 「FC27 첫 인게임 캡처(T6·T7)」는 **v1.2.0 전에 찍으면 패치 전 기준선**이 된다 — 풀백 조기 하강을 고정 관측 항목(#45 impact)으로 함께 센다. ⑶ 리드 국면 Deep 프리셋의 「풀백이 CB보다 더 내려가는 부작용」(#57)은 패치 뒤 다시 센다. ⑷ 오프사이드 인지 개선은 상대 공격수에도 적용되므로 높은 라인의 오프사이드 트랩 효율이 떨어질 수 있다(EA 서술 범위 밖 추론 — 실측 전 처방 근거로 쓰지 않는다). ⛔ 처방·`team_tactic_setups` 정본은 **패치 적용 확인 전 바꾸지 않는다**(#45 원칙 유지).",
  source=SRC,
  confidence="A (EA 1차 · 2026-10-29 직접 열람) · 적용 여부는 미확인(예고) — v1.2.0 패치노트가 나오면 실제 반영 항목을 새 행으로 확정한다"),
 dict(area="tactics",
  change="EA가 같은 글에서 **v1.2.0에 넣지 않은 「조사 중」 3건**을 밝혔다: ⑴ **높은 수비 라인이 상대에게 지나친 압박을 주는 상황** ⑵ 체격·피지컬이 다른 선수 간 충돌 처리 ⑶ 특정 슛 종류의 정확도 + GK 위치. 함께 공개한 출시 1개월 실측: 슛은 줄고 득점 효율은 올랐다 · 패스 수는 약간 줄고 성공률은 올랐다(수동 수비 인터셉트는 약간 증가) · 태클 성공 증가 · **포메이션별 승률이 고르게 분포(편차 최소)**하고 FC26 대비 전술·역할 다양성이 늘었다.",
  evidence="「Situations where high defensive lines can put too much pressure on the opposition」(높은 수비 라인이 상대에게 지나친 압박을 줄 수 있는 상황) · 「Looking at how collisions between players of different sizes and physical attributes are handled」(체격·피지컬 속성이 다른 선수 간 충돌이 어떻게 처리되는지 보고 있다) · 「win rates by formation are evenly distributed with minimal variance」(포메이션별 승률은 편차가 최소로 고르게 분포한다) · 「manually-controlled defenders intercepting slightly more often」(수동 조작 수비수의 인터셉트가 약간 더 잦다). " + LOC + " ⚠️ 커뮤니티(outputlag · r/EASportsFC 정리)는 수비 깊이 95 라인 메타가 v1.2.0에 빠졌다고 지적한다 — **D(통설)** 이고, EA의 「high defensive lines」(높은 수비 라인) 조사 항목이 그것을 가리키는지는 EA가 밝히지 않았다.",
  impact="⑴ **높은 라인 너프 가능성이 EA 공식 조사 항목이 됐다(A · 일정 없음).** AVL FC27 정본 #46(Balanced/Balanced/라인 52)은 High 구간이 아니라 직접 대상은 아니지만, 압박·고라인 국면 프리셋(`optimal:lead` 등 보류 5건)을 High 쪽으로 옮기는 판단에는 「후속 패치에서 약화될 수 있다」는 리스크를 병기한다. 커뮤니티 95 depth 메타(D)는 처방 근거로 쓰지 않는다. ⑵ 포메이션 승률 평준화(A)는 「메타 포메이션으로 바꿔야 이긴다」는 근거가 약하다는 뜻 — 실축 재현 포메이션 유지 방침과 부딪히지 않는다. ⑶ 저수비 스탯 인터셉트 과효율(#46)은 v1.2.0 항목에도 조사 목록에도 없다 → #46 impact(한시적 · 수정 예고 없음) 유지. ⑷ 체격 충돌 조사는 피지컬 진화 선택(가성비)의 FC27 전제가 바뀔 수 있는 축 — 결과가 나오면 docs/22 §2.1과 진화 처방을 다시 본다.",
  source=SRC + " · https://outputlag.com/news/ea-fc-27s-first-gameplay-patch-lands-mid-november-and-the-95-depth-meta-isnt-in-it/ (커뮤니티 · D)",
  confidence="A (EA 1차 · 2026-10-29 직접 열람) — 95 depth 메타 부분만 D(통설 · 커뮤니티 정리)"),
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
