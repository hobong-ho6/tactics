#!/usr/bin/env python3
"""전사 인덱서 — `reports/transcripts/*.md` 헤더를 파싱해 `match_videos`를 채운다 (2026-09-15 신설).

⛔ **발명하지 않는다.** 이 스크립트가 쓰는 값은 두 종류뿐이다:
  ⑴ 전사 파일 헤더에서 **파싱**한 것 — 채널·제목·게시일·URL·언어
  ⑵ `observations.source`가 그 전사 경로를 인용하고 있는지로 산출한 `obs_refs`
  ⇒ `summary`·`key_points`(사람이 전사를 읽고 쓰는 층)는 **건드리지 않는다**(재실행해도 보존).

전사 헤더 형태(2종):
    # 전사(자동 생성 자막) — {video_id} ({lang})
    > {채널} — {제목} ({게시일} 게시, {길이}, {메모})      ← 큐레이션된 형태
    > 원본: https://www.youtube.com/watch?v={id} · 수집: …   ← 메타 없는 형태(채널 미상)

경기 귀속(`report_id`)은 **추정하지 않는다** — 헤더 메모나 제목에 상대팀이 명시되고 그 팀의
`match_reports`가 날짜 창(±4일) 안에 하나로 특정될 때만 붙인다. 애매하면 NULL로 두고 보고한다.

사용:
    .venv/bin/python scripts/index_transcripts.py --dry-run
    .venv/bin/python scripts/index_transcripts.py
"""
import argparse
import datetime as dt
import json
import re
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from core import DB                                     # noqa: E402

TX = ROOT / "reports" / "transcripts"
# ⭐ 헤더에 채널이 없는 전사의 **보강 메타**(scripts/backfill_transcript_meta.py가 유튜브 원천에서 받아 쌓는다).
#    ⛔ 전사 파일을 고치지 않기 위한 폴백이다 — 원본은 「수집 당시 그대로」 남고 보강분은 자기 provenance를 갖는다.
META_BACKFILL = TX / "_meta_backfill.json"

# 채널 → (팀 코드, 종류 기본값). 팀 팬채널은 팀이 확정된다.
CHANNEL_TEAM = {
    "UTV | Aston Villa Fan Channel": ("AVL", "경기반응"),
    "UTV": ("AVL", "경기반응"),
    "The Villans": ("AVL", "선수스카우팅"),
    "1874 : The Aston Villa Channel": ("AVL", "경기반응"),
    "1874": ("AVL", "경기반응"),
    "Villa in NOIR": ("AVL", "전술분석"),
    # 구단 공식 채널 — 팀이 확정되고 종류는 회견이 기본이다
    "AVFC 공식": ("AVL", "감독회견"),
    "첼시 구단 공식": ("CHE", "감독회견"),
    "리버풀 공식": ("LIV", "감독회견"),
    # ⚠️ 팀 전용 분석 채널 — 팀을 못 박지 않으면 **자기 팀 이름이 상대팀 힌트로 오작동한다**
    #    (실증: 「The Liverpool FC TV」의 LIV-포레스트전 분석이 「liverpool」 힌트 때문에
    #     ATM-리버풀전(r38)에 붙었다 — 2026-09-15 적발)
    "The Liverpool FC TV": ("LIV", "전술분석"),
    "Hull City Fan Central": (None, "상대팀"),
    "Forest Fan TV": (None, "상대팀"),
    "AFTV(아스날 팬)": (None, "상대팀"),
    # ⭐ 2026-09-15 보강 54편에서 새로 드러난 채널 — 팀 축을 못 박아 상대팀 힌트 오작동을 막는다
    "UTV": ("AVL", "경기반응"),
    "UP THE VILLA": ("AVL", "경기반응"),
    "All Villa No Filler - An Aston Villa Podcast": ("AVL", "경기반응"),
    "Footy Post-Game Hub": ("AVL", "감독회견"),
    "Mango Talks Ball": ("AVL", "경기반응"),
    "Liverpool FC": ("LIV", "감독회견"),
    "This Is Anfield": ("LIV", "감독회견"),
    "AnfieldArmyNews": ("LIV", "감독회견"),
    "Anfield Index Extra": ("LIV", "전술분석"),
    "David Lynch - Liverpool FC": ("LIV", "전술분석"),
    "Red Tactics with Neil": ("LIV", "전술분석"),
    "The Golden Sky | Liverpool FC Fan Channel": ("LIV", "전술분석"),
    "RLC Chelsea": ("CHE", "전술분석"),
    "MightyBluesNews": ("CHE", "감독회견"),
    "Atlético Stats": ("ATM", "전술분석"),
    "Pase Atras TV": ("ATM", "전술분석"),
    "ATLÉTICO DE MADRID NOTICIAS DE HOY": ("ATM", "감독회견"),
    "Diario AS": ("ATM", "감독회견"),
    # ⛔ 팀 축이 없는 채널(중립·게임 재현·상대팀)은 None으로 둔다 — 잘못된 팀 부여가 더 나쁘다
    "Brom Squad Gaming": (None, "게임재현"),
    "Geografifa": (None, "게임재현"),
    "BeanymanSports": (None, "감독회견"),
    "talkSPORT": (None, "경기반응"),
    "Mundo Deportivo": (None, "감독회견"),
    "LockyLeeds": (None, "상대팀"),
}
# 제목·메모에 나오는 상대팀 표기 → matches.opponent 매칭 키워드
OPPONENT_HINTS = {
    # 영어 표기
    "forest": "Nottingham", "nottingham": "Nottingham", "hull": "Hull",
    "arsenal": "Arsenal", "brugge": "Brugge", "brentford": "Brentford",
    "fulham": "Fulham", "luton": "Luton", "leeds": "Leeds", "villarreal": "Villarreal",
    "malaga": "Malaga", "sevilla": "Sevilla", "athletic": "Athletic",
    "liverpool": "Liverpool", "chelsea": "Chelsea", "newcastle": "Newcastle",
    # ⭐ 한국어 메모 표기 — 우리 전사 헤더는 「헐전 D+1」처럼 한글로 적는다(영어만 보면 70편이 미귀속)
    "헐": "Hull", "포레스트": "Nottingham", "노팅엄": "Nottingham", "아스날": "Arsenal",
    "브뤼헤": "Brugge", "브렌트포드": "Brentford", "풀럼": "Fulham", "루턴": "Luton",
    "리즈": "Leeds", "비야레알": "Villarreal", "말라가": "Malaga", "세비야": "Sevilla",
    "아틀레틱": "Athletic", "리버풀": "Liverpool", "첼시": "Chelsea", "뉴캐슬": "Newcastle",
    "소시에다드": "Sociedad", "레알 소시에다드": "Sociedad",
    # 약어(리포트 제목에서 쓰는 3글자 코드)
    " ars": "Arsenal", " nffc": "Nottingham", " avl": None, " che": "Chelsea", " liv": "Liverpool",
}
KIND_HINTS = [
    (r"회견|press ?conference|persconferentie|reaction|경기 후|post-?match", "감독회견"),
    (r"scouting|스카우팅|why .* is (perfect|underrated)|fits into", "선수스카우팅"),
    (r"tactical analysis|전술 ?분석|build-?up|analysis:", "전술분석"),
    (r"things we learned|reaction|review|fall to|defeat|draw at|win", "경기반응"),
    (r"preseason|프리시즌|pre-?season", "프리시즌"),
    (r"EA FC ?2\d|career mode|recreated in|tactics recreated", "게임재현"),
]


def parse_header(path: Path):
    """전사 파일 → dict(채널·제목·게시일·근사여부·url·메모). 메타 없으면 channel=None."""
    txt = path.read_text(encoding="utf-8", errors="ignore")[:1200]
    out = {"channel": None, "title": None, "published": None, "approx": 0,
           "url": None, "note": ""}
    m = re.search(r"watch\?v=([\w-]{6,})", txt)
    vid = path.name.split(".")[0]
    out["url"] = f"https://www.youtube.com/watch?v={m.group(1) if m else vid}"
    for line in txt.split("\n"):
        if not line.startswith("> ") or "원본:" in line or line.startswith("> ⚠️"):
            continue
        body = line[2:].strip()
        # {채널} — {제목} ({메타}) / {채널} - {제목}
        sp = re.split(r"\s+[—–]\s+|\s+-\s+", body, maxsplit=1)
        out["channel"] = sp[0].strip()
        rest = sp[1].strip() if len(sp) > 1 else ""
        mm = re.match(r"(.*?)\s*\(([^()]*)\)\s*$", rest)
        if mm:
            out["title"], out["note"] = mm.group(1).strip(), mm.group(2).strip()
        else:
            out["title"] = rest or None
        blob = f"{rest} {out['note']}"
        d = re.search(r"(20\d\d)[-.](\d\d)[-.](\d\d)", blob)
        if d:
            out["published"] = f"{d.group(1)}-{d.group(2)}-{d.group(3)}"
            out["approx"] = 1 if re.search(re.escape(d.group(0)) + r"\s*경", blob) else 0
        else:  # '2026-08 초' 같은 월 단위 표기
            mo = re.search(r"(20\d\d)[-.](\d\d)(?!\d)", blob)
            if mo:
                out["published"] = f"{mo.group(1)}-{mo.group(2)}-01"
                out["approx"] = 1
        break
    return out


def guess_kind(text):
    for pat, kind in KIND_HINTS:
        if re.search(pat, text, re.I):
            return kind
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pulled", default=dt.date.today().isoformat())
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    # 경기 리포트 색인 — (team_code, date) → report_id
    reports = [dict(r) for r in con.execute("""
        SELECT mr.id, mr.team_code, m.date, m.opponent
        FROM match_reports mr JOIN matches m ON m.id=mr.match_id""")]
    # 전사 경로를 인용한 obs
    obs_src = [dict(r) for r in con.execute(
        "SELECT id, source FROM observations WHERE source LIKE '%reports/transcripts/%'")]

    backfill = (json.loads(META_BACKFILL.read_text(encoding="utf-8"))
                if META_BACKFILL.exists() else {})
    rows, no_meta, unlinked, backfilled = [], [], 0, 0
    for path in sorted(TX.glob("*.md")):
        parts = path.name.split(".")
        vid, lang = parts[0], (parts[1] if len(parts) > 2 else None)
        h = parse_header(path)
        if not h["channel"]:
            # ⭐ 유튜브 원천 보강분으로 폴백(2026-09-15). 없으면 여전히 채널 미상으로 제외한다.
            b = backfill.get(vid)
            if b and b.get("channel"):
                h = {**h, "channel": b["channel"], "title": b.get("title"),
                     "published": b.get("published"), "approx": 0,
                     "note": (h.get("note") or "") + " [메타 보강: YouTube 원천]"}
                backfilled += 1
            else:
                no_meta.append(path.name)
                continue
        team, kind = CHANNEL_TEAM.get(h["channel"], (None, None))
        kind = guess_kind(f"{h['title'] or ''} {h['note']}") or kind
        blob = f"{h['title'] or ''} {h['note']}".lower()

        # 경기 귀속 — 상대팀 표기로 후보를 좁히고 **하나로 특정될 때만** 붙인다.
        #   ⑴ 게시일이 있으면 날짜 창(±4일)까지 걸어 좁힌다
        #   ⑵ 게시일이 없어도(구단 공식 회견 등 날짜 미기재) 팀+상대팀이 **유일**하면 붙인다
        #      — 「Forest defeat」는 AVL 09-12과 LIV 08-29 둘이라 팀이 없으면 여전히 미귀속이다
        report_id = None
        hits = {op for k, op in OPPONENT_HINTS.items() if op and k in blob}
        if hits:
            cand = [r for r in reports
                    if any(op.lower() in (r["opponent"] or "").lower() for op in hits)
                    and (team is None or r["team_code"] == team)]
            if h["published"]:
                pub = dt.date.fromisoformat(h["published"])
                cand = [r for r in cand
                        if abs((dt.date.fromisoformat(r["date"]) - pub).days) <= 4]
            if len(cand) == 1:
                report_id = cand[0]["id"]
                team = team or cand[0]["team_code"]
        if report_id is None:
            unlinked += 1

        rel = str(path.relative_to(ROOT))
        refs = sorted(o["id"] for o in obs_src if f"{vid}." in o["source"])
        rid = con.execute("SELECT id FROM regimes WHERE team_code=? AND end IS NULL",
                          (team,)).fetchone() if team else None
        rows.append(dict(
            video_id=vid, lang=lang, report_id=report_id,
            regime_id=rid["id"] if rid else None, team_code=team,
            channel=h["channel"], title=h["title"], published=h["published"],
            published_approx=h["approx"], url=h["url"], transcript_path=rel, kind=kind,
            obs_refs=",".join(map(str, refs)) or None,
            source=(f"{'전사 헤더 파싱' if '[메타 보강' not in (h['note'] or '') else 'YouTube 원천 보강(oEmbed 채널·제목 + uploadDate 게시일)'}"
                    f" + observations 역인용 산출 (scripts/index_transcripts.py, {a.pulled})"),
            confidence=("MEDIUM-HIGH(메타) — 채널·제목·게시일은 전사 헤더 파싱값이다. "
                        "⚠️ 전사 본문은 **유튜브 자동 생성 자막**이라 오인식이 있다(docs/30 대조표) — "
                        "인용 시 auto-caption 명기·원문+번역 병기(불변규칙 11). "
                        "경기 귀속은 상대팀 표기+날짜 창으로 단일 특정된 건만 붙였다."),
        ))

    print(f"전사 {len(rows) + len(no_meta)}편 · 인덱스 {len(rows)}"
          f"(헤더 {len(rows) - backfilled} + **보강 {backfilled}**) · "
          f"메타 없음 {len(no_meta)} · 경기 미귀속 {unlinked}")
    if a.dry_run:
        for r in rows[:15]:
            print(f"  {r['video_id']:<14} {(r['channel'] or '')[:28]:<28} "
                  f"{r['published'] or '----':<10} report={r['report_id'] or '-':<4} "
                  f"obs={r['obs_refs'] or '-'}")
        print(f"\n메타 없음(채널 미상, 인덱스 제외): {', '.join(no_meta[:12])}"
              + (" …" if len(no_meta) > 12 else ""))
        return

    # ⛔ summary/key_points는 UPDATE 대상에서 제외한다(사람이 쓴 층 보존)
    ins = upd = 0
    conflicts = []
    for r in rows:
        ex = cur.execute("SELECT id, report_id FROM match_videos WHERE video_id=? AND lang IS ?",
                         (r["video_id"], r["lang"])).fetchone()
        cols = [k for k in r if k not in ("video_id", "lang")]
        if ex:
            # ⛔ `report_id`는 **채움 전용**이다 — 사람이 고친 경기 귀속을 휴리스틱이 덮으면
            #    같은 오류가 회차마다 되살아난다(2026-09-15 The Liverpool FC TV 오귀속 수습 후 규칙화).
            #    내 추정과 저장값이 다르면 덮지 않고 **보고**한다.
            if ex["report_id"] is not None:
                if r["report_id"] != ex["report_id"]:
                    conflicts.append((r["video_id"], ex["report_id"], r["report_id"]))
                r = {**r, "report_id": ex["report_id"]}
            cur.execute(f"UPDATE match_videos SET {', '.join(f'{c}=:{c}' for c in cols)} WHERE id=:_id",
                        {**r, "_id": ex["id"]})
            upd += 1
        else:
            keys = list(r)
            cur.execute(f"INSERT INTO match_videos({','.join(keys)}) VALUES({','.join(f':{k}' for k in keys)})", r)
            ins += 1
    con.commit()
    print(f"신규 {ins} · 갱신 {upd} (summary/key_points·기존 report_id는 보존)")
    if conflicts:
        print("⚠️ 경기 귀속 추정이 저장값과 다름 — 덮지 않았다(사람이 판정): "
              + ", ".join(f"{v}: 저장 r{a} ↔ 추정 r{b}" for v, a, b in conflicts))
    print("다음: python3 scripts/gates.py && python3 scripts/export.py && scripts/db_dump.sh")


if __name__ == "__main__":
    main()
