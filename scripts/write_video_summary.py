#!/usr/bin/env python3
"""영상 요약 적재 — JSON 파일을 받아 `match_videos.summary`/`key_points`를 채운다 (2026-09-15 신설).

왜 스크립트로 빼는가: 요약 작성은 회차마다 반복되고 79편처럼 대량이면 배치로 나눠 넣어야 한다.
매번 임시 파이썬을 쓰면 confidence 꼬리말 규약(auto-caption·번역 병기 명기)이 빠질 수 있다 —
꼬리말을 여기서 **한 곳에서** 붙인다.

입력 JSON 형태:
    {"<video_id>": {"summary": "...", "key_points": ["...", "..."]}, ...}

⛔ 이미 요약이 있는 행은 `--force` 없이는 건드리지 않는다(덮어쓰기 방지).

사용:
    .venv/bin/python scripts/write_video_summary.py /tmp/batch1.json
    .venv/bin/python scripts/write_video_summary.py /tmp/fix.json --force
"""
import argparse
import datetime as dt
import json
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core import DB                                     # noqa: E402

TAIL = ("[요약 {d}] summary/key_points는 **전사 원문을 읽고 쓴 것**이다(영상 미시청). "
        "⚠️ auto-caption 오인식 가능 — 인물명·수치는 실측과 교차검증 필요(docs/30 대조표). "
        "인용은 원문+한국어 번역 병기(불변규칙 11).")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("json_path")
    ap.add_argument("--pulled", default=dt.date.today().isoformat())
    ap.add_argument("--force", action="store_true", help="기존 요약도 덮어쓴다")
    a = ap.parse_args()

    data = json.loads(Path(a.json_path).read_text(encoding="utf-8"))
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("BEGIN IMMEDIATE")
    tail = TAIL.format(d=a.pulled)
    n, skip, miss = 0, [], []
    for vid, d in data.items():
        row = cur.execute(
            "SELECT id, summary, confidence FROM match_videos WHERE video_id=?", (vid,)).fetchone()
        if not row:
            miss.append(vid)
            continue
        if row["summary"] and not a.force:
            skip.append(vid)
            continue
        conf = row["confidence"] or ""
        if tail not in conf:
            conf = (conf + " · " + tail).strip(" ·")
        cur.execute("UPDATE match_videos SET summary=?, key_points=?, confidence=? WHERE id=?",
                    (d["summary"], "\n".join(d["key_points"]), conf, row["id"]))
        n += 1
    con.commit()
    done, tot = con.execute(
        "SELECT SUM(summary IS NOT NULL), COUNT(*) FROM match_videos").fetchone()
    print(f"적재 {n}편 · 기존 보존 {len(skip)} · 미등록 {miss or 0}")
    print(f"진행률 {done}/{tot}편 ({done / tot:.0%}) · 남음 {tot - done}")


if __name__ == "__main__":
    main()
