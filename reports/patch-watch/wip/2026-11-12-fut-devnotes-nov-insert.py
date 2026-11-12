#!/usr/bin/env python3
"""2026-11-12 — EA 「FUT Developer Notes - November」(11-11) 적재. A 1행(방침·검토 중 표명 — 실제 변경 아님).
INSERT만(불변규칙 2) · title로 중복 검사."""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from core.db import connect  # noqa: E402

TODAY = "2026-11-12"
URL = "https://www.ea.com/games/ea-sports-fc/fc-27/news/fc27-november-gameplay-developer-notes"
ROW = dict(
 game_version="FC27", area="meta",
 title="FUT 11월 개발자 노트 — 진화 보상 상향·스쿼드 다양성 게임플레이 조정 검토",
 change=("EA FUT 개발팀 11월 노트(11-11 · 주소는 gameplay지만 내용은 **FUT 경제 방침**). 실제 변경은 하나, 나머지는 **「검토 중」 표명**이다. "
         "⑴ **캠페인 카드 접근성 확대** — 11-06 UEFA Road to the Knockouts부터 이후 캠페인까지 일부 카드를 출시 시점에 얻기 쉽게 조정(실행 중). "
         "⑵ **진화(Evolutions)를 더 보상감 있게 미세조정** — 시즌 중 새 진화에서 조정을 시험(검토). "
         "⑶ **스쿼드 다양성** — 특정 유형 카드 쏠림을 인정하고, 다른 유형 선수·플레이 스타일이 경기장에서 더 효과적이도록 **게임플레이 조정을 검토**(구체 항목 없음 · 10월 게임플레이 노트·Q&A를 참조하라고만 함). "
         "⑷ **간소화 SBC** — 개별 챌린지 보상 팩 제거분을 아이템 점수 요구치에 반영했다고 설명 · **개별 챌린지 보상 복귀 계획 없음**. "
         "⑸ 같은 팩·픽에서 홀로그래픽판과 일반판이 함께 나오는 문제 — 조정 검토. "
         "⑹ 챔피언스 보상 — 경기당 코인 증가·토큰 상점 이용을 관찰 중(변경 없음). "
         "11-13 09:00 PT 디스코드 FUT Q&A 예고(정리는 Steam 고정글로 올라오는 전례)."),
 evidence=("「we're seeing positive indications that Campaign Player Items are more likely to feature in a player's squad when received from a pack」(팩에서 받은 캠페인 카드가 스쿼드에 들어갈 가능성이 높아졌다는 긍정 신호를 보고 있다) · "
           "「we see an opportunity to fine-tune Evolutions and make them feel more rewarding」(진화를 미세조정해 더 보상감 있게 만들 여지가 보인다) · "
           "「We're also exploring gameplay adjustments aimed at making different types of players and playing styles more effective on the pitch.」(다양한 유형의 선수와 플레이 스타일이 경기장에서 더 효과적이도록 하는 게임플레이 조정도 검토하고 있다.) · "
           "「while we don't currently have plans to bring back individual Challenge rewards」(현재 개별 챌린지 보상을 되돌릴 계획은 없지만) · "
           "「We're exploring adjustments to give us greater flexibility over when Holographic and standard versions of the same player can appear together」(같은 선수의 홀로그래픽판과 일반판이 함께 나올 수 있는 경우를 더 유연하게 조절하도록 조정을 검토하고 있다)"),
 impact=("⑴ 진화 선택: EA가 진화 보상 상향을 예고 — 새 진화가 이전보다 후해질 수 있으니 **급하지 않은 진화 투입은 다음 진화 카탈로그를 보고** 결정할 근거(추론). "
         "⑵ SBC: 개별 챌린지 보상은 돌아오지 않는다 — 간소화 SBC 가치 판단은 세트 최종 보상만으로 한다. "
         "⑶ 「스쿼드 다양성 게임플레이 조정」은 **대상·시점 미정** — 3선(CDM) 역할·포커스 동작 변경 언급 없음 · 정본 재검토 사유 아님. 다음 TU 노트에서 구체화되는지 본다. "
         "⑷ 11-13 디스코드 FUT Q&A 정리가 Steam 고정글로 올라오면 다음 회차에 대조."),
 source=URL + " (「EA SPORTS FC™ 27 | FUT Developer Notes - November」 · 2026-11-11 · 2026-11-12 직접 열람)",
 confidence="A (EA 1차 · 2026-11-11 게시 · 직접 열람) · 단 ⑴ 외에는 「검토 중」 표명이라 실제 변경·시점 미확정 · 인게임 영향 미실측",
 recorded=TODAY,
)
con = connect()
if con.execute("select 1 from game_system_changes where title=?", (ROW["title"],)).fetchone():
    sys.exit("이미 있음 — 건너뜀")
cols = ",".join(ROW); q = ",".join("?" * len(ROW))
cur = con.execute(f"insert into game_system_changes({cols}) values({q})", tuple(ROW.values()))
con.commit(); print("inserted id", cur.lastrowid)
