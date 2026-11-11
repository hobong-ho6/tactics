#!/usr/bin/env python3
"""2026-11-11 — TU v1.2.0 배포 첫날(11-10~11) 커뮤니티 체감 적재 (사용자 요청 「이 패치에 대한 커뮤니티 반응이나 체감 수집」).
D 등급(의견) 3행. INSERT만(불변규칙 2) · title로 중복 검사."""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from core.db import connect  # noqa: E402

TODAY = "2026-11-11"
FMK = "https://www.fmkorea.com/index.php?mid=fifa_series&document_srl="
CONF_BASE = ("D — 커뮤니티 의견 · 패치 첫날(11-10 저녁~11-11 오전) · 표본 작고 실력대·모드 미상 · 통제 실측 0. "
             "다국어 검색(영·한·스·독·포·불·일) — 패치 뒤 체감은 한국어(에펨코리아)·영어(X)에만 있었고 스·독·포·불·일은 패치노트 요약 기사뿐. "
             "Reddit(접근 차단)·X(402 — 검색 요약만)·EA 포럼(403)은 본문 확인 못함.")
ROWS = [
 dict(area="tactics", title="TU 1.2.0 첫날 체감 — 95 깊이는 조금 물렸을 뿐 · 오히려 강해졌다는 말도",
  change="패치 첫날 체감은 **「너프가 체감되지 않거나 오히려 강해졌다」 쪽이 우세**하다. ⑴ 영어권(X @FutPoliceLeaks): 엘리트 디비전 첫 경기에서 95를 써 보니 **패치 뒤 더 효과적** — 밀집이 15~20m 뒤로 옮겨졌을 뿐이라는 평 · 역습 상대로 AI 수비가 침투를 더 잘 따라간다는 다른 게시물 ⑵ 에펨코리아가 전한 해외 반응: 「라인을 2 steps 뒤로 물린 것뿐」이라 역효과 · 원터치 2대1 스루 자체는 손대지 않았다 ⑶ 반대 의견: 「라인은 잘 내려가긴 한데」(26돌문) · 95 패치에 만족(메시레전등). 매체 평도 같은 쪽 — FUTFC 「a nudge rather than a nerf」(너프가 아니라 살짝 민 것) · MMOexp 「95 Depth remains a viable tactical option」(95 깊이는 여전히 쓸 만한 선택지).",
  evidence="「95 depth feels different, but I've found it more effective post-patch in Elite Division」(95 깊이는 느낌이 달라졌지만, 엘리트 디비전에서는 패치 뒤가 더 효과적이었다 — X @FutPoliceLeaks · 검색 요약만) · 「AI Defending track the runs」(AI 수비가 침투를 따라간다) — 「95 depth vs counter attacks」(95 깊이 대 역습) 게시물 · 검색 요약만 · 「It is a nudge rather than a nerf: stamina and the offside trap are untouched」(너프가 아니라 살짝 민 것이다 — 체력과 오프사이드 트랩은 그대로다 — futfc.gg 직접 열람) · 에펨코리아 「이번 패치로 스루패스 훨씬 더 쉬워졌다는게 해외쪽 반응」(10542493220 · 11-11 10:14 · 본문 열람) · 「라인은 잘 내려가긴 한데」(10541519400 · 11-10 23:14).",
  impact="⑴ #99(95 깊이 너프 · A)의 **효과 크기는 커뮤니티 체감상 작다** — EA가 라이브 튜닝으로 추가 조정할 여지가 있어(#99 자체가 라이브 튜닝) 다음 회차에 후속 튜닝 공지를 본다. ⑵ 빌라 정본 라인(52)은 95 구간이 아니라 직접 영향은 없다(추론). 상대가 95를 쓸 때의 뒷공간 공략 처방은 **패치 전과 같게 본다**. ⑶ 3선(CDM) 역할 무관. ⛔ 처방·정본 변경 없음.",
  source="X @FutPoliceLeaks 「FC 27 POST-PATCH FULLBACKS」 외(검색 요약 · 본문 미열람) · https://futfc.gg/fc-title-update/ (직접 열람) · " + FMK + "10542493220 · " + FMK + "10541519400 · https://www.mmoexp.com/News/ea-sports-fc-27-update-1-2-0-patch-notes-95-depth-kick-off-goals-and-sbc-card-returns.html",
  confidence=CONF_BASE + " X 게시물은 snippet_only."),
 dict(area="positioning", title="TU 1.2.0 첫날 체감 — 풀백은 나아졌는데 센터백이 튀어나가 뒷공간이 열린다",
  change="⭐ 패치 첫날 한국 커뮤니티에서 **독립 게시글 3건 + 댓글 다수가 같은 증상**을 적었다: 상대 공격형 미드필더가 공을 잡으면 **센터백 한 명이 자동으로 튀어나가** 뒷공간이 열리고, 로빙·느린 스루에도 센터백 반응이 늦다 · 예전엔 걸리던 오프사이드가 「전부 온사」. 풀백 쪽은 「풀백 옵사라인 정상화」·「풀백은 좋아졌지만 센백은 약해졌다」로 **개선 체감**. 그 밖 개선 체감: 공격수 자리 잡기가 훨씬 낫다 · 커서 전환이 빨라지고 공중볼 커서 반응이 좋아졌다(#101 루즈볼 전환 축). 반대로 영어권 X는 「Fullbacks are not fixed」(풀백은 안 고쳐졌다) · EA 패치 공지 답글에도 같은 불만.",
  evidence="에펨코리아 「상대격수가 공잡으면」 「자동으로 센백이 바로 튀어나감」(뚝전설 · 10541830991 · 11-11 00:34) · 「풀백 라인 조정했다면서」 「센백이 얼타지 왜」(싸부님 · 10541924393 · 11-11 01:06) · 댓글 「센백하나가 자꾸튀어나옴」(권성유망주) · 「패치 이후 종종 센백이 스루를 못따라가던데」(La7ve · 10542411705 · 11-11 09:32) · 「격수들 자리 잡는 건 훨씬 낫던데」(xxaabb · 10541749926 · 11-11 00:13) · 댓글 「풀백 옵사라인 정상화」(베일맘 · 10542214090) · 「Fullbacks are not fixed」(풀백은 고쳐지지 않았다 — X @FutPoliceLeaks · 검색 요약만).",
  impact="⑴ **빌라 적용 주의**: 에메리 고라인(정본 라인 52)에서 센터백 한 명이 공격형 미드필더에게 튀어나가는 증상이 사실이면 **뒷공간 실점 위험**이 커진다 — 패치 뒤 인게임 관측 때 「CB 전진 이탈」을 별도 항목으로 적는다(미실측 · 의견 단계). ⑵ #100·#104의 「풀백 라인 개선」은 한국 체감과 맞고 영어권 X와는 엇갈린다 — limit #30·obs#449 재판정은 **여전히 우리 실측으로만**. ⑶ 3선(CDM) 역할 언급 0 — 다만 센터백이 튀어나갈 때 메우는 쪽이 3선이라 홀딩(RDM) 커버 동작은 같은 관측에서 함께 본다(추론). ⛔ 처방·정본 변경 없음.",
  source=FMK + "10541830991 · " + FMK + "10541924393 · " + FMK + "10542411705 · " + FMK + "10541749926 · " + FMK + "10542214090 · X @FutPoliceLeaks(검색 요약 · 본문 미열람)",
  confidence=CONF_BASE + " 한국 3건은 본문 직접 열람 · 같은 게시판 같은 날이라 상호 독립성은 중간."),
 dict(area="meta", title="TU 1.2.0 첫날 체감 — 4-3-1-2 쏠림이 더 세졌다 · 문제는 라인보다 패스 차단",
  change="한국 커뮤니티 첫날 진단: **「라인 95가 문제가 아니라 패스가 잘 끊기는 것」**이 4-3-1-2 우위의 원인이고, 패치 뒤 **4-3-1-2가 오히려 더 세졌다**는 글이 여럿이다(풀백이 제자리를 지키며 4-3-1-2의 수비 위치가 좋아졌다는 해석 포함). 중앙 미드필더 3명의 패스 차단 때문에 안전한 역습 경로가 없다 · 윙어에게 가는 핑 패스도 풀백이 잘 끊는다. 윙 포메이션은 「패치 전에도 쓸 만했고 달라진 것 거의 없음」 vs 「윙백이 똑똑해져 윙이 나빠졌다」로 갈린다.",
  evidence="에펨코리아 「7판 돌려보니 라인 95가 문제가아니고 지금은 패스가 잘 끊겨서 4312가 유리할 수 밖에 없는 것 같다」(HaaIand · 10541325393 · 11-10 22:23 · 댓글: 3중미 커팅·풀백 핑 패스 차단) · 댓글 「4312가 더 사기된 느낌」(WIDE · 10542214090) · 「상대격수가 공잡으면」 글의 4312 추천(뚝전설 · 10541830991) · 윙: 「윙 그냥 패치전에도 쓸만했음」 vs 「구려졋대 윙백이 똑똑해져서」(10541757000 · 11-11 00:15).",
  impact="⑴ 빌라 정본(4-2-3-1 계열 · 측면 활용)은 4-3-1-2 메타와 다른 축이다 — 메타 쏠림 자체는 구현 판단을 바꾸지 않는다. ⑵ 「패스 차단이 강하다」는 체감은 빌드업 3선(LDM 딥라잉/로밍)의 짧은 전진 패스 성공률과 연결될 수 있다 — obs#1080 딥라잉 빌드업 테스트 때 **패치 후 표본**으로 따로 센다(추론 · 미실측). ⑶ 역할·포커스 동작 변경 주장은 없음. ⛔ 처방·정본 변경 없음.",
  source=FMK + "10541325393 · " + FMK + "10542214090 · " + FMK + "10541830991 · " + FMK + "10541757000",
  confidence=CONF_BASE + " 한국 4건 본문 직접 열람 · 영어권 동일 주장 미확인(단일 언어권)."),
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
