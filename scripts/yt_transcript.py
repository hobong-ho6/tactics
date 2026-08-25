#!/usr/bin/env python3
"""유튜브 자동 생성 자막을 내려받아 정리된 전사 텍스트로 저장한다.

사용법:
    python3 scripts/yt_transcript.py VIDEO_ID LANG [제목메모]

- yt-dlp(brew 설치)로 자동 생성 자막(vtt)만 받는다 — 영상/음성은 받지 않는다.
- VTT의 롤링 중복(같은 줄이 두 큐에 반복)과 <c>/타임 태그를 제거한다.
- 산출물: reports/transcripts/VIDEO_ID.LANG.md ([mm:ss] 문단 단위).
- ⚠️ 자동 생성 자막은 오인식이 있다 — 인용 시 confidence에 auto-caption임을 명기.
"""
import html
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "reports" / "transcripts"


def fetch_vtt(video_id: str, lang: str, tmpdir: str) -> Path:
    subprocess.run(
        [
            "yt-dlp", "--skip-download", "--write-auto-subs",
            "--sub-langs", lang, "--sub-format", "vtt",
            "-o", video_id, f"https://www.youtube.com/watch?v={video_id}",
        ],
        cwd=tmpdir, check=True, capture_output=True,
    )
    matches = list(Path(tmpdir).glob(f"{video_id}*.vtt"))
    if not matches:
        sys.exit(f"자막 파일이 생성되지 않았다 (lang={lang}). --list-subs로 가용 언어를 확인하라.")
    return matches[0]


def parse_vtt(path: Path) -> list[tuple[str, str]]:
    """(시작시각, 줄) 목록 — 롤링 중복 제거."""
    cues: list[tuple[str, str]] = []
    ts = None
    prev_line = None
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        m = re.match(r"^(\d{2}:\d{2}:\d{2})\.\d{3} --> ", line)
        if m:
            ts = m.group(1)
            continue
        if not line or line.startswith(("WEBVTT", "Kind:", "Language:")):
            continue
        text = html.unescape(re.sub(r"<[^>]+>", "", line)).replace(" ", " ").strip()
        if not text or text == prev_line:
            continue
        prev_line = text
        cues.append((ts or "00:00:00", text))
    return cues


def to_markdown(video_id: str, lang: str, note: str, cues: list[tuple[str, str]]) -> str:
    out = [f"# 전사(자동 생성 자막) — {video_id} ({lang})", ""]
    if note:
        out += [f"> {note}", ""]
    out += [f"> 원본: https://www.youtube.com/watch?v={video_id} · 수집: scripts/yt_transcript.py",
            "> ⚠️ 유튜브 자동 생성 자막 — 오인식 가능. 인용 시 confidence에 auto-caption 명기.", ""]
    para: list[str] = []
    para_ts = None
    last_sec = None
    for ts, text in cues:
        h, m, s = (int(x) for x in ts.split(":"))
        sec = h * 3600 + m * 60 + s
        if para_ts is None:
            para_ts, last_sec = ts, sec
        # 30초 단위로 문단을 끊어 타임스탬프를 남긴다.
        if sec - last_sec >= 30:
            out.append(f"**[{para_ts[3:]}]** " + " ".join(para))
            out.append("")
            para, para_ts = [], ts
            last_sec = sec
        para.append(text)
    if para:
        out.append(f"**[{para_ts[3:]}]** " + " ".join(para))
    return "\n".join(out) + "\n"


def main() -> None:
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    video_id, lang = sys.argv[1], sys.argv[2]
    note = sys.argv[3] if len(sys.argv) > 3 else ""
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        vtt = fetch_vtt(video_id, lang, tmp)
        cues = parse_vtt(vtt)
    dest = OUT_DIR / f"{video_id}.{lang}.md"
    dest.write_text(to_markdown(video_id, lang, note, cues), encoding="utf-8")
    print(f"{dest} ({len(cues)} cues)")


if __name__ == "__main__":
    main()
