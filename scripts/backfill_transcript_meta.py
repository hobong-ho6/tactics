#!/usr/bin/env python3
"""메타 없는 전사의 채널·제목·게시일 보강 — YouTube 원천 조회 (2026-09-15 신설).

왜 (사용자 지시 2026-09-15 「메타 없는 전사 55편도 채널 보강해서 인덱스에 넣어줘」):
  `reports/transcripts/*.md` 139편 중 55편은 헤더에 `> 원본: …` 줄만 있어 **채널 미상**이었고,
  그래서 `index_transcripts.py`가 `match_videos`에 넣지 못했다(채널이 NOT NULL).

⛔ **내용으로 채널을 추측하지 않는다** — 유튜브 원천에서 직접 받는다:
  ⑴ 채널·제목 = **oEmbed**(`/oembed?url=…&format=json`) — curl 200, 인증 불필요
  ⑵ 게시일 = **watch 페이지의 `uploadDate`** JSON-LD 필드
  ⇒ 발명 0. 조회 실패분은 채우지 않고 보고한다(삭제된 영상 등).

⛔ **전사 파일을 고치지 않는다.** 보강분은 별도 파일 `reports/transcripts/_meta_backfill.json`에
   쌓고 `index_transcripts.py`가 **헤더에 채널이 없을 때만** 폴백으로 읽는다.
   ⇒ 원본 전사는 「수집 당시 그대로」 남고, 보강분은 **자기 provenance를 갖는다**(수집 방법·일자 기록).

사용:
    .venv/bin/python scripts/backfill_transcript_meta.py --dry-run
    .venv/bin/python scripts/backfill_transcript_meta.py
"""
import argparse
import datetime as dt
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from scripts.index_transcripts import parse_header, TX    # noqa: E402  같은 파서를 재사용한다

OUT = TX / "_meta_backfill.json"
UA = {"User-Agent": "Mozilla/5.0"}


def fetch(url, timeout=20):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout) as r:
        return r.read().decode("utf-8", "ignore")


def lookup(vid):
    """유튜브 원천 → dict(channel, title, published). 실패 시 None."""
    out = {}
    try:
        q = urllib.parse.quote(f"https://www.youtube.com/watch?v={vid}", safe="")
        d = json.loads(fetch(f"https://www.youtube.com/oembed?url={q}&format=json"))
        out["channel"] = (d.get("author_name") or "").strip()
        out["title"] = (d.get("title") or "").strip()
    except Exception as e:
        return None, f"oembed 실패: {type(e).__name__}"
    if not out["channel"]:
        return None, "채널명 빈 값"
    try:   # 게시일은 실패해도 진행한다(NULL 허용 — 결손과 0을 구분)
        m = re.search(r'"uploadDate":"(\d{4}-\d{2}-\d{2})', fetch(f"https://www.youtube.com/watch?v={vid}"))
        out["published"] = m.group(1) if m else None
    except Exception:
        out["published"] = None
    return out, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pulled", default=dt.date.today().isoformat())
    ap.add_argument("--sleep", type=float, default=0.4, help="요청 간격(초)")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    have = json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else {}
    targets = []
    for path in sorted(TX.glob("*.md")):
        if parse_header(path)["channel"]:
            continue                       # 헤더에 이미 채널이 있다 — 건드리지 않는다
        vid = path.name.split(".")[0]
        if vid in have:
            continue                       # 이미 보강됨(재실행 안전)
        targets.append((vid, path.name))
    print(f"메타 없는 전사 {len(targets) + len(have)}편 · 기존 보강 {len(have)} · 이번 대상 {len(targets)}")

    got, fail = {}, []
    for i, (vid, name) in enumerate(targets, 1):
        info, err = lookup(vid)
        if err:
            fail.append((vid, err))
        else:
            info["source"] = (f"YouTube oEmbed(채널·제목) + watch 페이지 uploadDate(게시일), "
                              f"{a.pulled} 조회 · scripts/backfill_transcript_meta.py")
            got[vid] = info
            print(f"  [{i:>2}/{len(targets)}] {vid:<14} {info['channel'][:34]:<34} "
                  f"{info['published'] or '----':<10} {(info['title'] or '')[:46]}")
        time.sleep(a.sleep)

    print(f"\n조회 성공 {len(got)} · 실패 {len(fail)}")
    if fail:
        print("⚠️ 실패(채우지 않음 — 삭제·비공개 영상 가능): " + ", ".join(f"{v}({e})" for v, e in fail))
    if a.dry_run:
        return
    have.update(got)
    OUT.write_text(json.dumps(have, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    print(f"→ {OUT.relative_to(ROOT)} ({len(have)}건)")
    print("다음: .venv/bin/python scripts/index_transcripts.py")


if __name__ == "__main__":
    main()
