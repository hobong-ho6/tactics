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
from core.db import connect as connect_db  # noqa: E402  ⭐ DB 연결 정본(대기·작성 중 표시)

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
    # ⚠️ PL 전반 전술 채널(2026-10-21 수집 목록 추가) — 빌라 전용이 아니라 팀을 못 박지 않는다(제목 힌트로 귀속)
    "Jacob Horsfall": (None, "전술분석"),
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
    # ⭐ 2026-10-20 뉴캐슬전 「미분류」 18편에서 나온 채널(사용자 지시 「미분류 영상 기본 종류 규칙」).
    #    빌라 팬·팟캐스트 — 팀을 못 박고 기본은 경기반응(제목이 전술분석·회견이면 그쪽이 이긴다)
    "The 12th Man - An Aston Villa Podcast": ("AVL", "경기반응"),
    "We Are Villans": ("AVL", "경기반응"),
    "The Holy Trinity Show | Aston Villa": ("AVL", "경기반응"),
    "Justin Talks Villa": ("AVL", "경기반응"),
    "The Villa Park Podcast | Aston Villa": ("AVL", "경기반응"),
    "Aston Villa Colombia": ("AVL", "경기반응"),
    "Penno | Aston Villa": ("AVL", "경기반응"),
    "The Terrace View An Aston Villa Podcast": ("AVL", "경기반응"),
    # 뉴캐슬 팬 채널 — 관리 4팀 밖이라 팀은 None, 종류는 상대팀(상대 관점)
    "Two For Joy": (None, "상대팀"),
    "Everything Is Black & White - Newcastle United": (None, "상대팀"),
    "The Magpie Channel TV": (None, "상대팀"),
    "Newcastle Mania": (None, "상대팀"),
    "True Faith Newcastle United Podcast and Fan Channel": (None, "상대팀"),
    "Howay & Say": (None, "상대팀"),
    "GallowgateShots - NUFC": (None, "상대팀"),
    "Ever More - NUFC": (None, "상대팀"),
    "The Toon Review": (None, "상대팀"),
    # 중립 방송·통신 — 회견 전문을 올리는 채널은 감독회견
    "Sky Sports Premier League": (None, "경기반응"),
    "NBC Sports": (None, "경기반응"),
    "HaytersTV": (None, "감독회견"),
}
# 제목·메모에 나오는 상대팀 표기 → matches.opponent 매칭 키워드
OPPONENT_HINTS = {
    # 영어 표기
    "forest": "Nottingham", "nottingham": "Nottingham", "hull": "Hull",
    "arsenal": "Arsenal", "brugge": "Brugge", "brentford": "Brentford",
    "fulham": "Fulham", "luton": "Luton", "leeds": "Leeds", "villarreal": "Villarreal",
    "malaga": "Malaga", "sevilla": "Sevilla", "athletic": "Athletic",
    "liverpool": "Liverpool", "chelsea": "Chelsea", "newcastle": "Newcastle",
    "fenerbah": "Fenerbah", "viking": "Viking",
    # ⭐ 한국어 메모 표기 — 우리 전사 헤더는 「헐전 D+1」처럼 한글로 적는다(영어만 보면 70편이 미귀속)
    "헐": "Hull", "포레스트": "Nottingham", "노팅엄": "Nottingham", "아스날": "Arsenal",
    "브뤼헤": "Brugge", "브렌트포드": "Brentford", "풀럼": "Fulham", "루턴": "Luton",
    "리즈": "Leeds", "비야레알": "Villarreal", "말라가": "Malaga", "세비야": "Sevilla",
    "아틀레틱": "Athletic", "리버풀": "Liverpool", "첼시": "Chelsea", "뉴캐슬": "Newcastle",
    "소시에다드": "Sociedad", "레알 소시에다드": "Sociedad", "바이킹": "Viking",
    # 약어(리포트 제목에서 쓰는 3글자 코드)
    " ars": "Arsenal", " nffc": "Nottingham", " avl": None, " che": "Chelsea", " liv": "Liverpool",
}
# ⭐ 팀 미지정 채널(PL 전반 분석·중립 방송·상대팀 팬)의 **제목 단서 → 팀**(2026-10-21 사용자 승인 — 제목에 Villa·Emery가 있는데
#    team_code가 빈 영상 46편이 빌라 영상 목록에서 빠졌다). ⛔ 관리 4팀 중 **한 팀만** 걸릴 때만 붙인다 —
#    「Liverpool vs Aston Villa」처럼 둘이 걸리면 어느 팀 영상인지 모르니 비워 둔다. 「villa」는 Villarreal과 겹치지 않게 단어 경계.
TEAM_HINTS = {
    "AVL": r"\baston villa\b|\bvilla\b|\bemery\b|아스톤 빌라|빌라|에메리|ヴィラ|エメリ",
    "CHE": r"\bchelsea\b|\balonso\b|첼시|알론소",
    "LIV": r"\bliverpool\b|\biraola\b|리버풀|이라올라",
    "ATM": r"\batl[eé]tico\b|\batleti\b|\bsimeone\b|아틀레티코|시메오네",
}


# 「Barcola VS Atletico」처럼 vs·against 바로 뒤에만 나오는 팀은 **상대**다(그 영상은 다른 쪽 팀 이야기)
VS_BEFORE = r"(\bvs?\.?|\bversus|\bagainst|\bcontra)\s+$"


def guess_team(title):
    t = title or ""
    hits = {team: [m.start() for m in re.finditer(pat, t, re.I)] for team, pat in TEAM_HINTS.items()}
    hits = {team: pos for team, pos in hits.items() if pos}
    if len(hits) != 1:
        return None
    (team, pos), = hits.items()
    return None if all(re.search(VS_BEFORE, t[:i], re.I) for i in pos) else team


# ⭐⭐ 「감독회견」은 **명시어 또는 감독이 화자인 제목**일 때만(2026-10-20 사용자 지적 — 뉴캐슬전 「감독 회견 7편」이 전부 팬 반응 영상).
#    ⛔ 종전엔 이 패턴에 `reaction`·`경기 후`·`post-match`가 있어 「Match Reaction」이 아래 경기반응보다 먼저 잡혔다.
#    「Press Conference Reaction」(팬이 회견에 반응)은 회견이 아니다.
PRESSER = r"press ?conference|presser|rueda de prensa|conferencia de prensa|pressekonferenz|persconferentie|basın toplantısı|coletiva|記者会見|회견"
PRESSER_NOT = r"(press ?conference|presser)\s*reaction|reacting to|reacts? to"
MANAGER_SPEAKS = (r"(\b(unai emery|emery|xabi alonso|alonso|andoni iraola|iraola|simeone|jaissle|moyes|glasner|arteta|slot|maresca|howe|postecoglou|mourinho|frank)\b"
                  r"|에메리|알론소|이라올라|시메오네|아르테타)['’]?s?\s*"
                  r"(:|\bon\b|reaction|post[- ]?match|interview|speaks|경기 후|인터뷰|반응)")
# 구단 공식 채널의 「Reaction」·인터뷰는 감독·선수 1차 발언이다(팬 채널의 Match Reaction과 다르다)
OFFICIAL_CH = r"공식|football club|official|^liverpool fc$|^chelsea fc$"
OFFICIAL_SPEAKS = r"reaction|interview|\bon\b|🗣"
KIND_HINTS = [
    (r"post[- ]?match live|match ?reaction|instant reaction|full[- ]time thoughts", "경기반응"),
    # ⭐ 2026-10-20 UTV 분석 영상이 「경기반응」으로 묻히던 것(사용자 「UTV에 전술분석 영상이 많이 나오던데」) —
    #    선수 한 명을 다루는 「HOW <이름> IS/SCARES/IMPRESSED…」·영입 평가는 선수스카우팅, 감독·팀 운영은 전술분석
    (r"must sign|rating .*signings|^how [a-z]+ [a-z]+ (is |impressed|scares|transforms)|cheat code|why unai emery loves", "선수스카우팅"),
    (r"\btactical\b|best .*\bxi\b|how does (unai )?emery|tore .* apart|what we need to see from", "전술분석"),
    (r"scouting|스카우팅|why .* is (perfect|underrated)|fits into", "선수스카우팅"),
    (r"tactical analysis|전술 ?분석|build-?up|analysis:|taktik analiz|análisis táctico", "전술분석"),
    (r"outsmarted|tactics? (are |is )?wrong|tactical breakdown|tactics explained", "전술분석"),
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
        # 「—」가 있으면 그것만 구분자다 — 채널명 속 「 - 」(「All Villa No Filler - An Aston Villa Podcast」)에서 먼저 잘리던 것(2026-10-21)
        sp = re.split(r"\s+—\s+", body, maxsplit=1)
        if len(sp) == 1:
            sp = re.split(r"\s+[–]\s+|\s+-\s+", body, maxsplit=1)
        if len(sp) == 1:
            # ⭐ 구분자 없는 줄은 **수집 메모**다(「CHE-ARS 2026-09-06 D+2」) — 종전엔 이걸 채널로 넣어
            #    15편이 「채널=메모 · 제목 없음」으로 인덱스됐다(2026-10-21). 채널은 비워 _meta_backfill 폴백에 맡긴다.
            out["note"] = body
            d = re.search(r"(20\d\d)[-.](\d\d)[-.](\d\d)", body)
            if d:   # 메모 날짜는 수집 맥락(경기일 등)이라 게시일 근사로만 쓴다 — 보강 메타가 있으면 그쪽이 이긴다
                out["published"], out["approx"] = f"{d.group(1)}-{d.group(2)}-{d.group(3)}", 1
            break
        out["channel"] = sp[0].strip()
        rest = sp[1].strip()
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


# ⭐ 마지막 기본값(2026-10-20) — 제목·메모·채널 어디에도 단서가 없을 때. 스코어 표기·결과 단어가 있으면 경기 반응이다.
SCORE_FALLBACK = r"\b\d\s?[-–]\s?\d\b|victory|beaten|takeaways|warm down|opinión|análisis del partido"


def resolve_kind(title, note, channel):
    """종류 판정 정본 — 순서: 제목(회견 포함) → 메모(회견 제외) → 채널 기본값 → 스코어 기본값.
    ⭐ 상대 팬 채널(채널 기본값 「상대팀」)은 제목이 경기반응·무단서일 때 상대팀으로 둔다 — 회견·전술분석은 제목이 이긴다."""
    ch_kind = CHANNEL_TEAM.get((channel or "").strip(), (None, None))[1]
    k = guess_kind(title or "", channel=channel) or guess_kind(note or "", presser=False)
    if ch_kind == "상대팀" and k in (None, "경기반응"):
        return "상대팀"
    if k:
        return k
    if ch_kind:
        return ch_kind
    return "경기반응" if re.search(SCORE_FALLBACK, title or "", re.I) else None


def guess_kind(text, presser=True, channel=None):
    """presser=False면 회견 판정을 건너뛴다 — 우리 전사 머리 메모(note)는 「회견 언급」 같은 말을 담아 오분류를 부른다."""
    if presser and re.search(PRESSER, text, re.I) and not re.search(PRESSER_NOT, text, re.I):
        return "감독회견"
    if presser and re.search(MANAGER_SPEAKS, text, re.I):
        return "감독회견"
    if presser and channel and re.search(OFFICIAL_CH, channel, re.I) and re.search(OFFICIAL_SPEAKS, text, re.I) \
            and not re.search(r"post[- ]?match live", text, re.I):
        return "감독회견"
    for pat, kind in KIND_HINTS:
        if re.search(pat, text, re.I):
            return kind
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pulled", default=dt.date.today().isoformat())
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    con = connect_db(DB)
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
    chan_team = {}   # 채널이 못 박은 팀(없으면 None) — 저장된 경기 귀속으로 팀을 정할 때 채널 고정값을 덮지 않으려고
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
        team, _ = CHANNEL_TEAM.get((h["channel"] or "").strip(), (None, None))   # ⚠️ 채널명 끝 공백(「Justin Talks Villa 」)
        chan_team[vid] = team
        kind = resolve_kind(h['title'], h['note'], h['channel'])   # 회견 판정은 제목만 · 정본 resolve_kind
        blob = f"{h['title'] or ''} {h['note']}".lower()

        # 경기 귀속 — 상대팀 표기로 후보를 좁히고 **하나로 특정될 때만** 붙인다.
        #   ⑴ 게시일이 있으면 날짜 창(±4일)까지 걸어 좁힌다
        #   ⑵ 게시일이 없어도(구단 공식 회견 등 날짜 미기재) 팀+상대팀이 **유일**하면 붙인다
        #      — 「Forest defeat」는 AVL 09-12과 LIV 08-29 둘이라 팀이 없으면 여전히 미귀속이다
        report_id = None
        hits = {op for k, op in OPPONENT_HINTS.items() if op and k in blob}
        # 채널이 팀을 못 박지 않았으면 제목 팀 단서로 후보를 좁힌다 — 「Liverpool's Champions League win」이
        # 「liverpool」 상대팀 단서로 ATM-리버풀전(ATM 리포트)에 붙던 것(2026-10-21)
        scope = team or guess_team(h["title"])
        if hits:
            cand = [r for r in reports
                    if any(op.lower() in (r["opponent"] or "").lower() for op in hits)
                    and (scope is None or r["team_code"] == scope)]
            if h["published"]:
                pub = dt.date.fromisoformat(h["published"])
                cand = [r for r in cand
                        if abs((dt.date.fromisoformat(r["date"]) - pub).days) <= 4]
            if len(cand) == 1:
                report_id = cand[0]["id"]
                team = team or cand[0]["team_code"]
        if report_id is None:
            unlinked += 1
        team = team or guess_team(h["title"])   # 채널·경기 귀속으로 못 정한 것만 — 채널 고정값을 덮지 않는다

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
                # 추정이 「없음」인 건 충돌이 아니다(사람이 더 안다) — 종전엔 이것까지 100여 줄 찍혀 진짜 3건이 묻혔다(2026-10-21)
                if r["report_id"] is not None and r["report_id"] != ex["report_id"]:
                    conflicts.append((r["video_id"], ex["report_id"], r["report_id"]))
                r = {**r, "report_id": ex["report_id"]}
                # ⭐ 팀은 **저장된** 경기 귀속을 따른다(2026-10-21) — 종전엔 추정 귀속에서만 팀을 따와
                #    사람이 붙인 경기 귀속이 있는 영상 약 90편의 team_code가 비거나 추정 경기 쪽 팀으로 갈렸다.
                if chan_team.get(r["video_id"]) is None:
                    rt = cur.execute("""SELECT r.team_code, g.id FROM match_reports r
                                        LEFT JOIN regimes g ON g.team_code=r.team_code AND g.end IS NULL
                                        WHERE r.id=?""", (ex["report_id"],)).fetchone()
                    if rt:
                        r = {**r, "team_code": rt[0], "regime_id": rt[1]}
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
