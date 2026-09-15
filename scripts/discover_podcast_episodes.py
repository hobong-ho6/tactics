#!/usr/bin/env python3
"""팟캐스트 RSS = 「발견 계층」 — 전사 미보유 회차를 찾아 유튜브 id까지 해석한다 (2026-09-15 신설).

왜 (사용자 지시 2026-09-15, 조사 결과는 obs#757·758):
  ⭐ **유튜브는 「목록을 훑는」 경로가 나쁘다** — 채널 RSS(`/feeds/videos.xml?channel_id=`)는 **404**이고
     채널 페이지 스크랩은 **30편**이 한계다. 그래서 우리 커버리지가 새고 있었다:
     1874의 2026-08-24~09-14 **26편 중 보유 13편(50%)**.
  ⭐ **팟캐스트 RSS는 한 요청에 전량을 준다**(1874 1,061편). 게시일·초 단위 길이·안정 GUID도 정확하다.
  ⛔ 그런데 **본문(전사)은 팟캐스트에서 못 얻는다** — 조회한 피드 전부 `<podcast:transcript>` 0건, MP3뿐이고
     우리는 ASR이 없고 docs/30이 음성 청취를 금지한다.
  ⇒ **역할 분담: 목록·메타는 RSS, 본문은 유튜브.** 이 스크립트가 그 다리다.

동작:
  ⑴ 피드 파싱 → 회차 목록(제목·날짜·길이·GUID)
  ⑵ `match_videos`와 제목 정규화 대조 → 보유/미보유 판정
  ⑶ 미보유분은 **유튜브 사이트 검색**으로 후보를 찾고 **oEmbed로 검증**한다
     ⛔⛔ **검색 결과의 제목을 믿지 말 것** — 유튜브가 **한국어로 번역해 돌려준다**(실증: 「경기 리뷰: 헐 시티 0 대 0…」).
         반드시 oEmbed의 `author_name`이 그 채널과 같은지, 원제가 일치하는지로 확정한다.
  ⑷ 산출: 「전사 수집 대상」 목록 + 실행 명령 + 작업 큐 파일

⛔ 피드에 없는 것을 만들지 않는다. 유튜브에서 확정하지 못한 회차는 **「오디오 전용 가능」**으로 분리해 보고한다.

사용:
    .venv/bin/python scripts/discover_podcast_episodes.py --since 2026-08-24
    .venv/bin/python scripts/discover_podcast_episodes.py --since 2026-08-01 --write
"""
import argparse
import datetime as dt
import json
import re
import sqlite3
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from core import DB                                     # noqa: E402

UA = {"User-Agent": "Mozilla/5.0"}
QUEUE = ROOT / "reports" / "transcripts" / "_todo_from_podcast.json"
NS = {"itunes": "http://www.itunes.com/dtds/podcast-1.0.dtd",
      "pod": "https://podcastindex.org/namespace/1.0"}

# 채널 → (피드 URL, 상태). ⚠️ 상태는 2026-09-15 확인값이다.
#   ⛔ Holtecast(acast 5f6be89b…, 380편·라이브)는 **유튜브 채널이 2015년에 멈춰** 전사 경로가 없다 — 넣지 않는다.
FEEDS = {
    "1874 : The Aston Villa Channel": ("https://feeds.megaphone.fm/COMG3846388170", "live"),
    "UTV | Aston Villa Fan Channel": ("https://feed.podbean.com/upthevillapodcast/feed.xml", "live"),
    "The Villans": ("https://feed.podbean.com/thevillans/feed.xml", "dormant(2025-07)"),
}


def get(url, timeout=30):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout) as r:
        return r.read()


def norm(s):
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())


def parse_feed(url):
    root = ET.fromstring(get(url))
    out = []
    for it in root.findall(".//item"):
        title = (it.findtext("title") or "").strip()
        raw = (it.findtext("pubDate") or "")[:16].strip()
        try:
            date = dt.datetime.strptime(raw, "%a, %d %b %Y").date()
        except ValueError:
            continue
        dur = it.findtext("itunes:duration", namespaces=NS)
        out.append({"title": title, "date": date.isoformat(), "duration": dur,
                    "guid": (it.findtext("guid") or "").strip()})
    out.sort(key=lambda x: x["date"], reverse=True)
    return out


def yt_search(query, limit=6):
    """유튜브 사이트 검색 → [(video_id, 검색이 보여준 제목)]. ⚠️ 제목은 번역될 수 있다."""
    html = get("https://www.youtube.com/results?search_query=" + urllib.parse.quote(query)).decode("utf-8", "ignore")
    seen, out = set(), []
    for v, t in re.findall(r'"videoId":"([\w-]{11})".{0,600}?"title":\{"runs":\[\{"text":"([^"]{6,120})"', html):
        if v in seen:
            continue
        seen.add(v)
        out.append((v, t))
        if len(out) >= limit:
            break
    return out


def oembed(vid):
    """oEmbed = **정본 채널명·원제**. 검색 제목 대신 이걸로 확정한다."""
    q = urllib.parse.quote(f"https://www.youtube.com/watch?v={vid}", safe="")
    d = json.loads(get(f"https://www.youtube.com/oembed?url={q}&format=json"))
    return (d.get("author_name") or "").strip(), (d.get("title") or "").strip()


def resolve(channel, title):
    """그 채널의 그 회차에 해당하는 유튜브 id를 확정한다. 못 하면 (None, 사유)."""
    for v, _ in yt_search(f"{channel} {title}"):
        try:
            author, real = oembed(v)
        except Exception:
            continue
        if norm(author) != norm(channel):
            continue                       # 다른 채널 — 버린다
        a, b = norm(real), norm(title)
        if a[:34] == b[:34] or a in b or b in a:
            return v, real
        time.sleep(0.15)
    return None, "유튜브에서 같은 채널·같은 제목을 확정하지 못함(오디오 전용 가능)"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--since", default=(dt.date.today() - dt.timedelta(days=30)).isoformat())
    ap.add_argument("--channels", nargs="*", default=[], help="기본: FEEDS 전체")
    ap.add_argument("--no-resolve", action="store_true", help="유튜브 해석 생략(목록만)")
    ap.add_argument("--write", action="store_true", help="작업 큐 파일에 기록")
    ap.add_argument("--write-meta", action="store_true",
                    help="⭐ 보유분의 `published`가 NULL·근사치면 RSS의 정확한 날짜로 채운다(채움 전용)")
    a = ap.parse_args()

    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    todo, stats = [], {}
    meta_fixed = 0

    for channel, (url, state) in FEEDS.items():
        if a.channels and channel not in a.channels:
            continue
        try:
            eps = parse_feed(url)
        except Exception as e:
            print(f"\n## {channel}: 피드 실패 {type(e).__name__}")
            continue
        recent = [e for e in eps if e["date"] >= a.since]
        # ⛔ **채널로 한정하지 않는다** — 두 함정 때문이다(2026-09-15 실증):
        #    ⑴ 우리 DB의 채널명 표기가 갈린다(`1874` ↔ `1874 : The Aston Villa Channel`, `UTV` ↔ `UTV | …`)
        #    ⑵ **UTV 피드가 The Villans 회차도 배포한다**(협업 채널) — 채널로 자르면 보유분을 미보유로 센다
        #    ⇒ 제목은 전역으로 대조하고, 최종 확정은 **video_id**로 한다(아래 2차 판정).
        rows = con.execute("SELECT video_id, title, published, channel FROM match_videos").fetchall()
        mine = {norm(r["title"]): r for r in rows if r["title"]}
        have_ids = {r["video_id"] for r in rows}
        print(f"\n## {channel} [{state}] — 피드 {len(eps)}편 · {a.since} 이후 {len(recent)}편 · 전사 풀 {len(rows)}편")

        have, miss, audio, already = [], [], [], []
        for e in recent:
            k = norm(e["title"])
            # ⛔⛔ **정규화 키 최소 길이 가드**(2026-09-15 오염 실증) — `norm()`은 [a-z0-9]만 남기므로
            #    한글 제목(「CHE 풀럼전 사전 회견」)은 `che` 3글자로 줄어 **아무 제목에나 부분일치**한다.
            #    실제로 알론소 회견 행의 게시일이 1874 팟캐스트 날짜로 덮였다 ⇒ 12글자 미만 키는 부분일치에서 제외한다.
            MINKEY = 12
            hit = mine.get(k) if len(k) >= MINKEY else None
            if not hit and len(k) >= MINKEY:
                hit = next((r for kk, r in mine.items()
                            if len(kk) >= MINKEY and (kk[:30] == k[:30] or kk in k or k in kk)), None)
            if hit:
                have.append((e, hit))
                # ⭐ 채움 전용 메타 보정 — RSS 날짜가 더 정확하다(유튜브 헤더의 「…경」 추정치 대체)
                if a.write_meta and (not hit["published"] or hit["published"] != e["date"]):
                    con.execute("""UPDATE match_videos
                                   SET published=?, published_approx=0,
                                       confidence=COALESCE(confidence,'') || ?
                                   WHERE video_id=? AND (published IS NULL OR published_approx=1)""",
                                (e["date"],
                                 f" · ⭐ [2026-09-15] 게시일을 팟캐스트 RSS의 정확한 pubDate({e['date']})로 보정"
                                 f"(길이 {e['duration']}초 · GUID {e['guid'][:20]}).",
                                 hit["video_id"]))
                    meta_fixed += con.total_changes and 1 or 0
                continue
            if a.no_resolve:
                miss.append((e, None))
                continue
            vid, info = resolve(channel, e["title"])
            if vid and vid in have_ids:
                # ⭐ 2차 판정 — 제목 표기가 달라 1차에서 놓쳤지만 **그 id를 이미 갖고 있다**
                have.append((e, next(r for r in rows if r["video_id"] == vid)))
                already.append((e, vid))
            else:
                (miss if vid else audio).append((e, vid or info))
            time.sleep(0.3)

        print(f"   ✅ 보유 {len(have)}(제목일치 {len(have) - len(already)} + **id로 확정 {len(already)}**) · "
              f"🔻 미보유(유튜브 확정) {len(miss)} · ⛔ 유튜브 미확정 {len(audio)}")
        for e, vid in already:
            print(f"      ℹ️ 보유(제목 표기 차이) {vid} | 피드 「{e['title'][:44]}」")
        for e, vid in miss:
            print(f"      🔻 {e['date']} {vid or '(미해석)'} | {e['title'][:62]}")
            if vid:
                todo.append({"video_id": vid, "channel": channel, "title": e["title"],
                             "published": e["date"], "duration_sec": e["duration"],
                             "podcast_guid": e["guid"]})
        for e, why in audio:
            print(f"      ⛔ {e['date']} {e['title'][:58]} — {why[:44]}")
        stats[channel] = (len(have), len(miss), len(audio))

    if a.write_meta:
        con.commit()
        print(f"\n게시일 보정 {meta_fixed}행(채움 전용 — 기존 정확값은 건드리지 않음)")

    print(f"\n=== 전사 수집 대상 {len(todo)}편 ===")
    for t in todo:
        print(f"  .venv/bin/python scripts/yt_transcript.py {t['video_id']} en   # {t['title'][:54]}")
    if a.write and todo:
        old = json.loads(QUEUE.read_text(encoding="utf-8")) if QUEUE.exists() else []
        seen = {x["video_id"] for x in old}
        old += [t for t in todo if t["video_id"] not in seen]
        QUEUE.write_text(json.dumps(old, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(f"\n→ {QUEUE.relative_to(ROOT)} ({len(old)}건 누적)")
    print("\n전사 확보 후: .venv/bin/python scripts/index_transcripts.py")


if __name__ == "__main__":
    main()
