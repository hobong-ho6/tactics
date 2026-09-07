#!/usr/bin/env python3
"""yt-dlp가 봇 차단(「The page needs to be reloaded」)에 걸릴 때의 우회 경로.

브라우저에서 영상 페이지를 열고 플레이어가 자막(en)을 요청하게 한 뒤, 네트워크 목록에서
`/api/timedtext?...&pot=...&fmt=json3` URL을 그대로 복사해 넘긴다(pot 토큰은 영상·세션 단위라
다른 영상에 재사용할 수 없다). 산출물·형식은 scripts/yt_transcript.py와 동일.

사용법:
    python3 scripts/yt_transcript_json3.py VIDEO_ID LANG "TIMEDTEXT_URL" [제목메모]
"""
import json
import subprocess
import sys

from yt_transcript import OUT_DIR, to_markdown


def fetch_json3(url: str) -> dict:
    body = subprocess.run(["curl", "-s", url], check=True, capture_output=True).stdout
    if not body:
        sys.exit("빈 응답 — pot 토큰이 만료됐거나 다른 영상의 것이다. 브라우저에서 URL을 다시 잡아라.")
    return json.loads(body)


def parse_json3(data: dict) -> list[tuple[str, str]]:
    """(시작시각 hh:mm:ss, 줄) 목록 — 줄바꿈 전용 이벤트는 버린다."""
    cues: list[tuple[str, str]] = []
    for ev in data.get("events", []):
        text = "".join(seg.get("utf8", "") for seg in ev.get("segs", [])).replace("\n", " ").strip()
        if not text:
            continue
        sec = int(ev.get("tStartMs", 0)) // 1000
        cues.append((f"{sec // 3600:02d}:{sec % 3600 // 60:02d}:{sec % 60:02d}", text))
    return cues


def main() -> None:
    if len(sys.argv) < 4:
        sys.exit(__doc__)
    video_id, lang, url = sys.argv[1], sys.argv[2], sys.argv[3]
    note = sys.argv[4] if len(sys.argv) > 4 else ""
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    cues = parse_json3(fetch_json3(url))
    dest = OUT_DIR / f"{video_id}.{lang}.md"
    md = to_markdown(video_id, lang, note, cues).replace(
        "수집: scripts/yt_transcript.py", "수집: scripts/yt_transcript_json3.py(브라우저 pot 경로)")
    dest.write_text(md, encoding="utf-8")
    print(f"{dest} ({len(cues)} cues)")


if __name__ == "__main__":
    main()
