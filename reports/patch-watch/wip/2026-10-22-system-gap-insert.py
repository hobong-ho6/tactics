#!/usr/bin/env python3
"""2026-10-22 FC27 시스템 미파악 검토(reports/research/2026-10-22-fc27-system-gap-review.md §2 ⒜ · §7 조치 1·8) 적재 스크립트.
game_system_changes FC27 6행 + reproduction_limits FC27 1행. INSERT만(불변규칙 2). 두 번 돌리면 중복 — 적재 전 change 앞 40자로 존재 검사."""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from core.db import connect  # noqa: E402

TODAY = "2026-10-22"
REVIEW = "reports/research/2026-10-22-fc27-system-gap-review.md"
ROWS = [
 dict(area="positioning",
  change="⭐ EA Launch Feedback Update(10-13) — **풀백 조기 하강은 13일이 지나도 「감시·조사 중」**이고 수정 일정이 없다. 킥오프 직후 골·저수비 스탯 인터셉트·니어포스트 로우드리븐·파울 판정도 같은 상태로 재확인됐다. #45·#46·#47의 재확인이며, 「풀백 위치는 게임플레이 전체 균형에 직접 영향을 주므로 변경에 신중하겠다」는 입장이 추가됐다.",
  evidence="en 「fullbacks are dropping too deep while defending, causing issues with defensive structure」(풀백이 수비 시 너무 깊이 내려와 수비 구조에 문제를 일으킨다) · 「Fullback positioning directly affects the overall balance of gameplay」(풀백 위치는 게임플레이 전체 균형에 직접 영향을 준다 — 그래서 변경에 신중하다) · 킥오프 골·인터셉트·로우드리븐·파울은 「monitoring / investigating」(감시 중·조사 중) 유지. ⚠️ de/pt-br 로케일도 영어 본문만 제공 — 교차검증 불가(불변규칙 10 예외 사유).",
  impact="limit #30(LB att_wb vs 윙백 A/B 결론 유보)의 유효 기간이 길어진다 — Season 2 안 수정 가능성 낮음. 리드 국면 프리셋에 Deep을 쓸 때 풀백이 CB보다 더 내려가는 부작용을 함께 센다. 빌라 구현 판단 5건(obs#1123 보류)을 바꿀 근거는 아니다.",
  source="https://www.ea.com/games/ea-sports-fc/fc-27/news/fc-27-launch-feedback-update (2026-10-13)",
  confidence="A (EA 1차 · 2026-10-22 직접 열람 · " + REVIEW + " §2 ⒜1)"),
 dict(area="meta",
  change="⭐ 케미스트리 개편 **EA 원문 확보(A)** — ICON 국적 기여 +2→+1(모든 리그 +1 링크·자리에 맞으면 풀 케미 유지) · Hero 리그 기여 +2→+1(국적 +1 유지) · Hall of FUT는 Hero와 같은 규칙. #28(B · timesaver 2차)을 1차로 격상한다 — HANDOFF 000⑴ 「원문 대조 후 적재」 충족.",
  evidence="「ICONs will continue to receive full Chemistry when played in position and provide a +1 League link to every League. Their Nation contribution is being reduced from +2 to +1.」(ICON은 자리에 맞게 기용되면 계속 풀 케미스트리를 받고 모든 리그에 +1 리그 링크를 제공한다. 국적 기여는 +2에서 +1로 축소된다.) · 「Heroes will also continue to receive full Chemistry when played in position, while their League contribution is being reduced from +2 to +1. Their +1 Nation contribution remains unchanged. Hall of FUT Items will follow the same Chemistry rules as Heroes.」(Hero 역시 자리에 맞게 기용되면 계속 풀 케미스트리를 받으며, 리그 기여는 +2에서 +1로 축소된다. 국적 +1 기여는 변하지 않는다. Hall of FUT 아이템은 Hero와 동일한 케미스트리 규칙을 따른다.)",
  impact="케미 상수 변경 없음 — sbc_solve.chem_total은 규칙 대신 fut.gg `player_card_items.chem_extra`를 읽으므로(#28 impact · migration 044 방침) 코드 수정이 없다. 재검산은 다음 /club-sync 회차의 케미 신호 수집이 그대로 수행한다. 000⑴ 종료.",
  source="https://www.ea.com/games/ea-sports-fc/fc-27/news/pitch-notes-fc27-launch-update (2026-09-14)",
  confidence="A (EA 1차 · 피치노트 원문 직접 확인 2026-09-21·10-22 · " + REVIEW + " §2 ⒜2)"),
 dict(area="meta",
  change="캠페인 선수 아이템은 **해당 포지션의 Role++ 전부를 해제한 채** 출시된다(OTW도 동일) — #21(2차 인용 MEDIUM)을 EA 원문으로 보강. 범위는 「Campaign Player Items」이며, FUT Deep Dive의 「all special Items」(리서치 §4.4)와 합치면 스페셜 전체.",
  evidence="「all Campaign Player Items will launch with all of their position's Roles++ unlocked」(모든 캠페인 선수 아이템은 해당 포지션의 Role++ 전부를 해제한 채 출시된다)",
  impact="docs/22 §6.1 「역할 숙련은 판정 층에서 제외」 유지 — 스페셜·캠페인 카드는 Role++가 일괄 부여돼 변별력이 없다. 베이스 골드 카드(스즈키·헤밍스 등 진화 대상)에서만 Role++가 의미를 가지므로, 진화 갈림길(§6.2)에서만 「Role++ 가지는 긴급성 축」으로 적는다.",
  source="https://www.ea.com/games/ea-sports-fc/fc-27/news/pitch-notes-fc27-launch-update (2026-09-14)",
  confidence="A (EA 1차 · " + REVIEW + " §2 ⒜3)"),
 dict(area="playstyles",
  change="⭐ **Incisive Pass에서도 리시버 트래핑 오차 감소가 제거**됐다 — #22(핑드 패스·티키타카)의 확장. 「패서의 PlayStyle로 리시버의 퍼스트 터치를 덮는」 경로가 패스 PlayStyle 3종 전부에서 끊겼다.",
  evidence="커뮤니티 정리 「FC 27 removes the previous reduction to the receiver's trapping error」(FC 27은 종전의 수신자 트래핑 오차 감소를 제거했다 · Operation Sports/timesaver · B) · EA 공식 설명은 「More accurate through balls, more swerve curve, and faster precision passes」(스루패스 정확도·스워브 커브·정밀 패스 속도)로 **수신자 효과가 없다**(EA what-are-playstyles 2026-09-25 · A — 부재 증거).",
  impact="docs/22 §6.1 규약(패서 PlayStyle로 리시버를 덮지 않는다)이 Pinged·Tiki Taka·Incisive 3종 전부에 적용된다 — 바클리·고메스·맥긴의 「연결」 평가에서 Incisive+ 가산을 쓰지 않는다. reproduction_limits FC27에 같은 취지의 한계 행을 둔다.",
  source="https://www.ea.com/games/ea-sports-fc/fc-27/news/what-are-playstyles (2026-09-25) · Operation Sports / timesaver.gg FC27 PlayStyle 정리 (2026-10-22 열람)",
  confidence="B(커뮤니티 정리) + A(EA 설명에 수신자 효과 부재) · " + REVIEW + " §2 ⒜4"),
 dict(area="playstyles",
  change="PlayStyle 총수 **36종 확정**(Scoring 8 · Passing 6 · Ball Control 5 · Defending 6 · Physical 5 · GK 6) · 삭제·신설 0 · **개명 1: Rush Out → 「1v1 Close Down」**(fut.gg slug는 rush-out 유지) · 표기 「Gamechanger」 한 단어. EA 페이지는 「36」이라 쓰고 35만 인쇄(Power Shot 누락) — fut.gg는 36.",
  evidence="EA what-are-playstyles(2026-09-25) 카테고리 표 + fut.gg /playstyles/ (2026-10-22 열람 · 36). 우리 카탈로그(docs/22 §3 · fc_playstyle_ids 31 「Rush Out」·37 「Game Changer」 · fut_club_players 「Rush Out」 46장 · player_game_stats FC27 10행)는 옛 이름 — 어휘 드리프트.",
  impact="저장 행은 고치지 않고 별칭 표 `fc_playstyle_aliases`(migration 121)로 잇는다 · 읽기는 core/playstyles.py · 화면은 playstyle-icons.js psLookup 한 곳 · G35 ⑵가 정본∪별칭 밖 이름을 막는다. FC24~25 잔존 이름(Flair·Trivela·Power Header·Aerial)은 canonical NULL로 「FC27 없음」 표기.",
  source="https://www.ea.com/games/ea-sports-fc/fc-27/news/what-are-playstyles (2026-09-25) · https://www.fut.gg/playstyles/ (2026-10-22)",
  confidence="A(EA 목록) / B(fut.gg 36 · slug) · " + REVIEW + " §2 ⒜5"),
 dict(area="meta",
  change="출시 초기 밸런스 동결이 **TU v1.0.4(10-07)까지 실행으로 확인**됐고, 10-19 Archetypes(The Grounds 전용)·10-22 Season 2 「FC Heritage」 문서에도 게임플레이·역할·케미 변경 언급이 0이다 — #47의 연장.",
  evidence="TU v1.0.4 「There are no gameplay balance and tuning changes in this update」(이번 업데이트에 게임플레이 밸런스·튜닝 변경은 없다) · Season 2 FC Heritage(10-22) 본문에 gameplay/roles/chemistry 변경 0건(직접 열람) · Archetypes(10-19)는 The Grounds 전용.",
  impact="처방 재검토 주기 그대로. 패치 감시 회차는 EA 뉴스 색인(/fc-27/news) 전수를 game_system_changes.source와 차집합으로 대조한다(scripts/patch_watch_index.py) — 10-13·10-19·10-22 3건이 10-12 이후 미적재였던 구조적 결손 대응.",
  source="https://www.ea.com/games/ea-sports-fc/fc-27/news/fc27-title-update-v1-0-4 (2026-10-07) · https://www.ea.com/games/ea-sports-fc/fc-27/news/fc-27-season-2-fc-heritage (2026-10-22) · https://www.ea.com/games/ea-sports-fc/fc-27/news/fc-27-the-grounds-developer-archetypes-update (2026-10-19)",
  confidence="A (EA 1차 · " + REVIEW + " §2 ⒜7)"),
]
LIMIT = dict(game_version="FC27", regime_id=1, axis="role_demands",
  real_feature="에메리 빌드업의 「연결」 품질 — 바클리·고메스·맥긴의 패스가 받는 선수(알리송·부엔디아)의 첫 터치를 돕는 실축 관계(바이킹전 오른쪽 삼각형 맥긴→고메스 16 · 맥긴→알리송 15)",
  limitation="FC27은 Pinged Pass·Tiki Taka·Incisive Pass 3종 모두에서 **수신자 트랩 오차 감소를 제거**했다(game_system_changes #22 + 2026-10-22 Incisive 확장 행). 패서의 PlayStyle 품질이 리시버의 퍼스트 터치를 보상하지 않으므로, 실축의 「좋은 패서 덕에 수신자가 편하게 받는다」 관계를 게임에서 패서 쪽 카드 선택으로 재현할 수 없다.",
  workaround="docs/22 §6.1 규약대로 리시버 쪽(First Touch·Technical) 카드·진화로 받는 품질을 올린다 · 패서 평가에 Incisive+/Pinged+/Tiki Taka+ 가산을 쓰지 않는다 · 처방 rationale에 「패서 PlayStyle은 전달력만」을 명기",
  source="game_system_changes #22 · 2026-10-22 Incisive 확장 행 · " + REVIEW + " §7 조치 8",
  confidence="A(EA 설명 부재 증거)+B(커뮤니티 정리)", added=TODAY)

con = connect()
ins = []
for r in ROWS:
    key = r["change"][:40]
    if con.execute("SELECT 1 FROM game_system_changes WHERE game_version='FC27' AND substr(change,1,40)=?", (key,)).fetchone():
        print("skip(exists):", key); continue
    cur = con.execute("INSERT INTO game_system_changes(game_version, area, change, evidence, impact, source, confidence, recorded) "
                      "VALUES('FC27', ?, ?, ?, ?, ?, ?, ?)", (r["area"], r["change"], r["evidence"], r["impact"], r["source"], r["confidence"], TODAY))
    ins.append(cur.lastrowid)
lk = LIMIT["limitation"][:40]
if con.execute("SELECT 1 FROM reproduction_limits WHERE game_version='FC27' AND substr(limitation,1,40)=?", (lk,)).fetchone():
    print("skip(limit exists)"); lim = None
else:
    cur = con.execute("INSERT INTO reproduction_limits(game_version, regime_id, axis, real_feature, limitation, workaround, source, confidence, added) "
                      "VALUES(:game_version,:regime_id,:axis,:real_feature,:limitation,:workaround,:source,:confidence,:added)", LIMIT)
    lim = cur.lastrowid
con.commit()
print("game_system_changes ids:", ins, "reproduction_limits id:", lim)
