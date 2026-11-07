#!/usr/bin/env python3
"""EA FC 뉴스 색인 ↔ game_system_changes.source 차집합 (2026-10-22 신설 · FC27 시스템 검토 §7 조치 6).

왜: 패치 감시 회차가 「새 글이 있나」를 눈으로 훑어서, 10-13 Launch Feedback Update · 10-19 Archetypes · 10-22 Season 2가
    10-12 이후 열흘간 미적재였다. 색인 전수를 받아 우리 source URL과 **차집합**으로 대조하면 「확인했는데 없었다」와
    「확인하지 않았다」가 갈린다. 읽기 전용 — 적재는 패치 감시 회차가 사람이 읽고 한다(자동 INSERT 금지).

사용:
    python3 scripts/patch_watch_index.py            # 현행 버전(core.game_version.current)
    python3 scripts/patch_watch_index.py --gv FC27 --index-url https://www.ea.com/games/ea-sports-fc/fc-27/news
      + Steam 포럼 고정글(EA 개발자 Q&A 정리가 여기에만 올라온다 · 2026-11-04 추가)
출력: 색인 글 목록(슬러그) · 적재됨/미적재 표시 · 미적재 목록(패치 감시 리포트 「확인한 URL」 절에 붙여 넣는다).
종료코드: 미적재 0이면 0, 있으면 2(스케줄 프롬프트가 분기할 수 있게) · 네트워크 실패 3(조용히 성공한 척하지 않는다).
"""
import argparse
import html
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from core.db import connect as connect_db  # noqa: E402

UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}
INDEX = {"FC27": "https://www.ea.com/games/ea-sports-fc/fc-27/news", "FC26": "https://www.ea.com/games/ea-sports-fc/fc-26/news"}
# 게임 시스템과 무관한 글(모드 소개·구매 안내)은 「무관」으로 표시만 한다 — 적재 대상이 아니라고 색인에서 지우지는 않는다.
OFF_TOPIC = re.compile(r"editions-and-release-dates|dual-entitlement|club-membership|which-fc27-mode|how-to-get-started|authenticity$")
# 회차에서 원문을 읽고 「시스템 변경 없음」으로 판정한 글 — 판정 회차 리포트를 함께 적는다(다음 회차가 같은 글을 또 읽지 않게 · 10-29 future-stars 2회차).
REVIEWED = {
    "fc-27-future-stars": "FUT 프로모 한정 규칙 · 2026-10-12",
    "title-update-v1-0-3": "버그 수정만(밸런스 0) · 2026-10-29",
    "fc27-month-1-evolutions-rewards": "클럽 멤버 보상 진화 공지 · 2026-10-29",
    "fc-27-the-grounds-developer-launch-update": "The Grounds 모드 · 2026-10-29",
    "pitch-notes-fc27-the-grounds-deep-dive": "The Grounds 모드 · 2026-10-29",
    "fc-27-uefa-road-to-the-knockouts": "FUT 프로모 한정 규칙 · 2026-11-07",
}
# ⭐ 2026-11-04: EA 개발자 Q&A 정리는 뉴스 색인이 아니라 Steam 포럼 고정글에만 올라온다 — 1차 게임플레이 Q&A(10-09)는 10-31에,
# FUT Q&A(10-14)는 11-04에야 발견됐다(2회차 → 불변규칙 13 · 색인에 넣어 구조로 막는다). 고정글 + 「All Developer Q&A」 정리글의 링크를 함께 대조한다.
STEAM = {"FC27": "https://steamcommunity.com/app/4080220/discussions/0/"}
STEAM_OFF_TOPIC = re.compile(r"Price Range|Frequently Asked|Forum Now Supports|Community Guidelines|All Developer Q&A Responses Summarized")
STEAM_REVIEWED = {
    "588439600674183359": "커리어 모드 Q&A · 2026-11-04",
    "588440114694199316": "The Grounds·Clubs Q&A · 2026-11-04",
}


def steam_threads(url):
    """고정글과 Q&A 정리글이 가리키는 스레드 → {id: 제목}."""
    get = lambda u: urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=30).read().decode("utf-8", "ignore")
    body = get(url)
    out = {}
    for m in re.finditer(r'href="' + re.escape(url) + r'(\d+)/"', body):
        t = re.search(r'class="forum_topic_name[^"]*"[^>]*>(.*?)</div>', body[m.end():m.end() + 2000], re.S)
        title = html.unescape(re.sub(r"<[^>]+>|\s+", " ", t.group(1))).strip() if t else ""
        if title.startswith("PINNED:"):
            out[m.group(1)] = title[7:].strip()
    for tid, title in list(out.items()):
        if "All Developer Q&A" in title:
            for lid, ltitle in re.findall(r"discussions\\?/0\\?/(\d+)\\?/\](.*?)(?:\\n)?\[\\?/url\]", get(f"{url}{tid}/")):
                out.setdefault(lid, ltitle.strip())
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gv")
    ap.add_argument("--index-url")
    a = ap.parse_args()
    con = connect_db()
    gv = a.gv
    if not gv:
        from core.game_version import current
        gv = current(con)
    url = a.index_url or INDEX.get(gv)
    if not url:
        sys.exit(f"색인 URL을 모른다: {gv} — --index-url")
    try:
        body = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30).read().decode("utf-8", "ignore")
    except Exception as e:
        print(f"⛔ 색인 수신 실패({url}): {e} — 리포트에 「확인하지 못함」으로 적을 것")
        sys.exit(3)
    tag = url.rsplit("/", 2)[-2]                               # fc-27
    slugs = sorted(set(re.findall(rf"/{tag}/news/([a-z0-9-]+)", body)))
    srcs = [s or "" for (s,) in con.execute("SELECT source FROM game_system_changes WHERE game_version=?", (gv,))]
    joined = "\n".join(srcs)
    missing = []
    print(f"# EA 뉴스 색인 {gv} — {url} · 글 {len(slugs)} · game_system_changes {len(srcs)}행")
    for s in slugs:
        hit = s in joined
        off = bool(OFF_TOPIC.search(s))
        rev = REVIEWED.get(s)
        mark = "✅ 적재됨" if hit else ("— 무관(모드·구매 안내)" if off else (f"— 검토·비적재({rev})" if rev else "❌ 미적재"))
        print(f"  {mark:12s} {s}")
        if not hit and not off and not rev:
            missing.append(s)
    if gv in STEAM:
        try:
            threads = steam_threads(STEAM[gv])
        except Exception as e:
            print(f"⛔ Steam 고정글 수신 실패({STEAM[gv]}): {e} — 리포트에 「확인하지 못함」으로 적을 것")
            sys.exit(3)
        print(f"\n# Steam 포럼 고정글·Q&A 정리 — {STEAM[gv]} · 스레드 {len(threads)}")
        for tid, title in sorted(threads.items(), key=lambda kv: kv[1]):
            hit = tid in joined
            off = bool(STEAM_OFF_TOPIC.search(title))
            rev = STEAM_REVIEWED.get(tid)
            mark = "✅ 적재됨" if hit else ("— 무관(안내·목차)" if off else (f"— 검토·비적재({rev})" if rev else "❌ 미적재"))
            print(f"  {mark:12s} {tid} {title}")
            if not hit and not off and not rev:
                missing.append(f"steam:{tid}")
        if not threads:
            print("⛔ Steam 고정글 0건 — 페이지 구조가 바뀌었을 수 있다(확인하지 못함)")
            sys.exit(3)
    print(f"\n미적재 {len(missing)}: " + (" · ".join(missing) if missing else "0 ✅"))
    sys.exit(2 if missing else 0)


if __name__ == "__main__":
    main()
