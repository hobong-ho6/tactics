#!/usr/bin/env python3
"""영상 요약 적재 — JSON 파일을 받아 `match_videos.summary`/`key_points`와 `video_impl_claims`를 채운다.

(2026-09-15 신설 → 같은 날 **구현 주장(`impl_claims`) 수용으로 확장**, 사용자 승인 「요약 규약도 바꿔줘」)

왜 스크립트로 빼는가: 요약 작성은 회차마다 반복되고 79편처럼 대량이면 배치로 나눠 넣어야 한다.
매번 임시 파이썬을 쓰면 confidence 꼬리말 규약(auto-caption·번역 병기 명기)이 빠질 수 있다 —
꼬리말을 여기서 **한 곳에서** 붙인다.

⭐⭐ **요약만 쓰고 끝내지 않는다**(obs#762·763, docs/30 §영상·서사 소스 절차 **8단계**).
요약 101편을 세보니 역할 코드 8편·팀 설정 3축 0편이어서 **기계가 대조할 수 없었다.**
그래서 이제 요약과 **같은 회차에** 구현 주장을 행으로 받는다 — **G17이 결손을 막는다.**
⛔ 주장이 없는 영상도 `{"axis": "none"}` 한 행을 넣어 **「주장 없음」과 「미작성」을 구분한다.**

입력 JSON 형태:
    {"<video_id>": {
       "summary": "...",
       "key_points": ["...", "..."],
       "impl_claims": [
         {"axis": "role", "player": "만잠비", "role_id": "cm_playmaker", "focus": "Roaming",
          "quote": "원문 「…」(한국어 번역)", "verdict": "PENDING",
          "verdict_note": "실측 무결정 Δ0.004 — docs/30 7단계 ⑵ tie-break 대상"},
         {"axis": "team_axis", "team_code": "CHE", "field": "build_up_style", "value": "Counter",
          "verdict": "HELD", "verdict_note": "…재판정 조건…"},
         {"axis": "none"}
       ]}}

⛔ 이미 요약이 있는 행은 `--force` 없이는 건드리지 않는다(덮어쓰기 방지).
⛔ `player`를 이름으로 줄 때 **유일 일치가 아니면 넣지 않고 중단한다**(동일성 규약 — docs/30 §선수 동일성).
   다트로↔웨슬리 포파나 사고가 이름 검사만으로는 안 걸렸다. 해석 결과는 항상 출력해 검수 가능하게 둔다.

사용:
    .venv/bin/python scripts/write_video_summary.py /tmp/batch1.json
    .venv/bin/python scripts/write_video_summary.py /tmp/fix.json --force
    .venv/bin/python scripts/write_video_summary.py /tmp/claims.json --claims-only
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

AXES = ("role", "focus", "team_axis", "instruction", "limit", "none")
VERDICTS = ("APPLIED", "HELD", "REJECTED", "PENDING", "NA")


def resolve_player(con, name):
    """이름 → player_id. ⛔ 유일 일치가 아니면 예외(동일성 규약)."""
    rows = con.execute("""SELECT id, COALESCE(name_kr, name) n FROM players
                          WHERE name_kr=? OR name=?""", (name, name)).fetchall()
    if len(rows) == 1:
        return rows[0][0]
    raise SystemExit(f"⛔ 선수 이름 「{name}」이 유일하게 해석되지 않는다({len(rows)}건) — "
                     f"player_id를 직접 지정하라: {[dict(r) for r in rows]}")


def insert_claims(con, vid, claims, pulled):
    """구현 주장 적재. 재실행 안전 — 같은 영상의 기존 주장을 지우고 다시 넣는다(주장은 원장이 아니다)."""
    con.execute("DELETE FROM video_impl_claims WHERE video_id=?", (vid,))
    for c in claims:
        axis = c.get("axis")
        if axis not in AXES:
            raise SystemExit(f"⛔ {vid}: axis 어휘 이탈 「{axis}」 — 허용 {AXES}")
        verdict = c.get("verdict", "NA" if axis == "none" else "PENDING")
        if verdict not in VERDICTS:
            raise SystemExit(f"⛔ {vid}: verdict 어휘 이탈 「{verdict}」 — 허용 {VERDICTS}")
        if verdict in ("HELD", "REJECTED") and not (c.get("verdict_note") or "").strip():
            raise SystemExit(f"⛔ {vid}: {verdict}는 사유·재판정 조건이 필수다(docs/30 8단계)")
        pid = c.get("player_id")
        if pid is None and c.get("player"):
            pid = resolve_player(con, c["player"])
        con.execute("""INSERT INTO video_impl_claims
                       (video_id, axis, player_id, team_code, role_id, focus, field, value,
                        quote, verdict, verdict_note, source, confidence)
                       VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (vid, axis, pid, c.get("team_code"), c.get("role_id"), c.get("focus"),
                     c.get("field"), c.get("value"), c.get("quote"), verdict, c.get("verdict_note"),
                     c.get("source") or f"전사 원문 읽기 · scripts/write_video_summary.py, {pulled}",
                     c.get("confidence") or "auto-caption 전사 기반 — 인물명·수치는 실측 교차검증 필요"))
    return len(claims)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("json_path")
    ap.add_argument("--pulled", default=dt.date.today().isoformat())
    ap.add_argument("--force", action="store_true", help="기존 요약도 덮어쓴다")
    ap.add_argument("--claims-only", action="store_true",
                    help="요약은 건드리지 않고 impl_claims만 적재(기존 요약 101편 백필용)")
    a = ap.parse_args()

    data = json.loads(Path(a.json_path).read_text(encoding="utf-8"))
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("BEGIN IMMEDIATE")
    tail = TAIL.format(d=a.pulled)
    n, nc, skip, miss = 0, 0, [], []
    for vid, d in data.items():
        row = cur.execute(
            "SELECT id, summary, confidence FROM match_videos WHERE video_id=?", (vid,)).fetchone()
        if not row:
            miss.append(vid)
            continue
        if d.get("impl_claims") is not None:
            nc += insert_claims(cur, vid, d["impl_claims"], a.pulled)
        if a.claims_only:
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
    todo = con.execute("""SELECT COUNT(*) FROM match_videos v WHERE v.summary IS NOT NULL
                          AND NOT EXISTS(SELECT 1 FROM video_impl_claims c
                                         WHERE c.video_id=v.video_id)""").fetchone()[0]
    print(f"적재 요약 {n}편 · 구현 주장 {nc}행 · 기존 보존 {len(skip)} · 미등록 {miss or 0}")
    print(f"진행률 요약 {done}/{tot}편 ({done / tot:.0%}) · ⭐ **claims 미작성 {todo}편**(G17이 건수로 보고)")


if __name__ == "__main__":
    main()
