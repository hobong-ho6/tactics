#!/usr/bin/env python3
"""EA FC 뉴스 색인 ↔ game_system_changes.source 차집합 (2026-10-22 신설 · FC27 시스템 검토 §7 조치 6).

왜: 패치 감시 회차가 「새 글이 있나」를 눈으로 훑어서, 10-13 Launch Feedback Update · 10-19 Archetypes · 10-22 Season 2가
    10-12 이후 열흘간 미적재였다. 색인 전수를 받아 우리 source URL과 **차집합**으로 대조하면 「확인했는데 없었다」와
    「확인하지 않았다」가 갈린다. 읽기 전용 — 적재는 패치 감시 회차가 사람이 읽고 한다(자동 INSERT 금지).

사용:
    python3 scripts/patch_watch_index.py            # 현행 버전(core.game_version.current)
    python3 scripts/patch_watch_index.py --gv FC27 --index-url https://www.ea.com/games/ea-sports-fc/fc-27/news
출력: 색인 글 목록(슬러그) · 적재됨/미적재 표시 · 미적재 목록(패치 감시 리포트 「확인한 URL」 절에 붙여 넣는다).
종료코드: 미적재 0이면 0, 있으면 2(스케줄 프롬프트가 분기할 수 있게) · 네트워크 실패 3(조용히 성공한 척하지 않는다).
"""
import argparse
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
        mark = "✅ 적재됨" if hit else ("— 무관(모드·구매 안내)" if off else "❌ 미적재")
        print(f"  {mark:12s} {s}")
        if not hit and not off:
            missing.append(s)
    print(f"\n미적재 {len(missing)}: " + (" · ".join(missing) if missing else "0 ✅"))
    sys.exit(2 if missing else 0)


if __name__ == "__main__":
    main()
