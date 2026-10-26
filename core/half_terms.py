"""하프 표기 한국어화 정본 — 1H/2H/HT → 전반/후반/하프타임 (2026-10-26 사용자 지시 「기존 리포트도 한국어로」).

리포트·관찰·판정 문장에 제공사 구간 코드(1H/2H)와 HT가 그대로 섞여 「1H 2H가 뭐야?」가 나왔다. 규칙은 여기 하나다 —
게이트 G41이 이 모듈로 위반을 세고, 수집 회차는 문장을 넣기 전에 conv()를 거친다.

⛔ 바꾸지 않는 것:
  - 「…」 안쪽(외국어 원문 인용 보존 — 불변규칙 11)
  - 한글이 없고 영어 단어가 8개 이상인 값·줄(영어 원문 그 자체 — 예: player_matches.heat_note 영문 메모)
  - md의 ``` 블록·> 인용 줄
  - 코드값 표·열(SKIP_TABLES·SKIP_COLS — match_period_stats.period의 '1H'/'2H'는 하프 비교 카드가 읽는 코드다)
뒤따르는 조사는 받침에 맞춘다(전반·후반·하프타임 모두 받침 있음): 는→은 · 가→이 · 를→을 · 와→과 · 로→으로.
"""
import re

TOK = re.compile(r"(?<![A-Za-z0-9])(1H|2H|HT)(?![A-Za-z0-9])(는|가|를|와|로(?!서)|)")
KR = {"1H": "전반", "2H": "후반", "HT": "하프타임"}
_PP = {"는": "은", "가": "이", "를": "을", "와": "과", "로": "으로", "": ""}
SKIP_TABLES = {"match_period_stats"}
SKIP_COLS = {("video_impl_claims", "value"), ("video_impl_claims", "quote")}


def _plain(s):
    return TOK.sub(lambda m: KR[m.group(1)] + _PP[m.group(2)], s)


def _outside_quotes(s, fn):
    out, depth, buf = [], 0, ""
    for ch in s:
        if ch == "「":
            if depth == 0:
                out.append(fn(buf)); buf = ""
            depth += 1; buf += ch
        elif ch == "」" and depth:
            buf += ch; depth -= 1
            if depth == 0:
                out.append(buf); buf = ""
        else:
            buf += ch
    out.append(fn(buf) if depth == 0 else buf)
    return "".join(out)


def is_foreign(s):
    return not re.search("[가-힣]", s) and len(re.findall(r"[A-Za-z]{3,}", s)) >= 8


def conv(s):
    """DB 텍스트 한 값 — 「」 밖만 바꾼다. 영어 원문 값은 그대로."""
    if not isinstance(s, str) or is_foreign(s):
        return s
    return _outside_quotes(s, _plain)


def conv_md(text):
    """md 문서 — 줄 단위. ``` 블록·> 인용·영어 원문 줄은 그대로."""
    out, fence = [], False
    for line in text.split("\n"):
        if line.lstrip().startswith("```"):
            fence = not fence; out.append(line); continue
        if fence or line.lstrip().startswith(">") or is_foreign(line):
            out.append(line); continue
        out.append(_outside_quotes(line, _plain))
    return "\n".join(out)


def db_violations(con):
    """[(table, column, rowid)] — conv()가 바꿀 값이 남은 칸."""
    bad = []
    for (t,) in con.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall():
        if t in SKIP_TABLES or t.startswith("sqlite_"):
            continue
        for c in [r[1] for r in con.execute(f'PRAGMA table_info("{t}")')]:
            if (t, c) in SKIP_COLS:
                continue
            try:
                rows = con.execute(f'SELECT rowid, "{c}" FROM "{t}" WHERE "{c}" GLOB "*[12]H*" OR "{c}" GLOB "*HT*"').fetchall()
            except Exception:
                continue
            bad += [(t, c, rid) for rid, v in rows if isinstance(v, str) and conv(v) != v]
    return bad
