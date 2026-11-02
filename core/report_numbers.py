"""경기 리포트 숫자 표기 정본 — 높이·폭 좌표와 수비 높이에 「무엇의 숫자인지」를 붙인다 (2026-11-01 신설 · G43).

왜 (사용자 「여기 괄호안에 숫자는 뭐야」 → 「다른 경기 리포트도 같은 식으로 고쳐줘 그리고 높이나 폭을 숫자로
    보여주는건 좋은디 앞으로도 수집해줘」):
  원문 md의 「볼 소유 평균 위치(WS): 밍스 (42, 81)」가 DB 요약으로 옮겨지며 「밍스 (42,81)」만 남았고,
  수비 높이는 코드 변수명 `def_x`로 적혀 화면에서 읽을 수 없었다.

규칙:
  ⑴ 리포트 표(TABLES) 텍스트의 좌표 괄호 `(a, b)`는 **같은 줄 앞쪽에 라벨**(LABELS 중 하나)이 있어야 한다.
     라벨 형식 예: 「WS 볼 소유 평균 위치(앞뒤, 좌우 · 0~100 · 좌우 0 = 빌라 오른쪽) (55,31)」.
  ⑵ 좌표 약칭은 「이름(약칭)」으로 쓴다 — def_x → 「수비 액션 평균 높이(def_x)」 · ax/ay → 「높이(ax)」·「오른쪽 기준 폭(ay)」 ·
     툴x → 「왼쪽 기준 폭(툴x)」 · poss_x → 「볼 소유 평균 높이(poss_x)」 등(NAMES 표) — conv()/conv_md()가 바꾼다
     (def_x 정의: core/whoscored.def_x — 수비 액션 x 평균).
  ⑶ FROM 이후 리포트는 ⑶-a 보유 요약(tac_possession·key_points)에 라벨 붙은 좌표가 1개 이상 있고
     ⑶-b 45분+ 출전자 전원에 SofaScore 평균 위치(player_matches.avg_x·avg_y)가 있어야 한다.
     SofaScore가 평균 위치를 안 주는 경기는 confidence에 「평균 위치 미제공」(NO_AVG_POS)을 적어 면제한다.
"""
import re

# ⭐ 검사 범위 = 경기 리포트를 이루는 표의 **텍스트 열 전부**(2026-11-01 확장 — 요약 8열만 보다가 표 5개 ~1,100곳이 남아 있었다).
TABLES = ("match_reports", "match_tactical_changes", "match_player_reports", "match_game_setups",
          "match_player_prescriptions")
SUMMARY = ("tac_possession", "key_points")          # ⑶-a 「높이·폭 좌표 1개 이상」을 보는 열
COORD = re.compile(r"\(\s*\d{1,3}(?:\.\d+)?\s*,\s*\d{1,3}(?:\.\d+)?\s*\)")
LABELS = ("평균 위치", "볼 터치", "볼 소유", "좌표", "같은 기준", "앞뒤, 좌우")
# ⭐ 좌표 약칭 → 「이름(약칭)」(2026-11-01 · 2차: poss_x·툴x·tool_x·avg_x/y·x̄/ȳ 추가 — 사용자 「poss_x랑 툴x도 같이 정리해줘」).
#   좌우 축은 기준이 둘이라 **기준을 이름에 넣는다**: SofaScore·WhoScored y(ay·avg_y·ȳ)는 0 = 오른쪽, 툴x(tool_x = 100 − 소파 y)는 0 = 왼쪽.
#   (docs/30 좌표 규약 · 불변규칙 9). 앞뒤 축은 셋 다 0 = 우리 골.
NAMES = (("def_x", "수비 액션 평균 높이"), ("poss_x", "볼 소유 평균 높이"),
         ("avg_x", "높이"), ("avg_y", "오른쪽 기준 폭"), ("ax", "높이"), ("ay", "오른쪽 기준 폭"),
         ("tool_x", "왼쪽 기준 폭"), ("tool_y", "높이"), ("툴x", "왼쪽 기준 폭"), ("툴y", "높이"),
         ("x\u0304", "평균 높이"), ("y\u0304", "오른쪽 기준 평균 폭"), ("\u0233", "오른쪽 기준 평균 폭"))   # ȳ는 합성 문자(U+0233)로도 쓰인다
_TOK = re.compile("|".join(rf"(?<![A-Za-z0-9_가-힣]){re.escape(t)}" + ("" if t[-1] in "\u0304\u0233" else r"(?![A-Za-z0-9_])")
                           for t, _ in NAMES))   # x̄·ȳ는 숫자가 바로 붙어 쓰인다(「x̄56.4」)
_NAME = dict(NAMES)
FROM = "2026-11-01"
NO_AVG_POS = "평균 위치 미제공"


def conv(text):
    """기계적으로 바꿀 수 있는 것만 바꾼다 — 좌표 약칭(NAMES)에 이름을 붙인다. 좌표 괄호는 무엇의 좌표인지 사람이 적는다.
    이미 「이름(약칭)」이면 그대로 두고, 1차 이름(「폭(ay)」 등 기준이 빠진 것)은 지금 이름으로 올린다 — 여러 번 돌려도 같다."""
    if not isinstance(text, str):
        return text
    out, i = [], 0
    for m in _TOK.finditer(text):
        tok, name = m.group(0), _NAME[m.group(0)]
        st, en = m.start(), m.end()
        wrapped = st > 0 and text[st - 1] == "(" and text[en:en + 1] == ")"
        if wrapped:
            head = text[i:st - 1]
            if head.endswith(name):
                out.append(text[i:en]); i = en; continue
            last = name.split()[-1]                       # 1차 이름(「폭」·「높이」) → 지금 이름
            if head.endswith(last):
                out += [head[:-len(last)], name, "(", tok]; i = en; continue
        out += [text[i:st], f"{name}({tok})"]; i = en
    out.append(text[i:])
    return "".join(out)


_SKIP = re.compile(r"```.*?```|`[^`\n]*`|「[^」]*」", re.S)


def conv_md(text):
    """md 원문용 conv — 코드(```·`)와 원문 인용 「…」 안은 건드리지 않는다(식별자·원문 보존)."""
    out, i = [], 0
    for m in _SKIP.finditer(text):
        out += [conv(text[i:m.start()]), m.group(0)]
        i = m.end()
    out.append(conv(text[i:]))
    return "".join(out)


def _unlabeled_coords(text):
    out = []
    for line in str(text or "").splitlines():
        for m in COORD.finditer(line):
            if not any(lb in line[:m.start()] for lb in LABELS):
                out.append(m.group(0))
    return out


def _labeled_coords(text):
    return sum(len(COORD.findall(line)) for line in str(text or "").splitlines()
               if COORD.search(line) and any(lb in line for lb in LABELS))


def _text_cols(con, table):
    return [r[1] for r in con.execute(f"PRAGMA table_info({table})") if (r[2] or "").upper() in ("TEXT", "")]


def text_violations(text):
    """한 텍스트의 위반 사유 목록."""
    bad = [f"좌표 {x} 앞에 라벨 없음" for x in _unlabeled_coords(text)]
    if conv_md(text) != text:
        bad.append("좌표 약칭 이름 없음(conv()로 바꿀 것)")
    return bad


def db_violations(con):
    """[(table#rowid.col 또는 report_id, 사유)] — 비면 통과."""
    bad = []
    for t in TABLES:
        cols = _text_cols(con, t)
        for rid, *vals in con.execute(f"SELECT rowid, {', '.join(cols)} FROM {t}"):
            for c, v in zip(cols, vals):
                if isinstance(v, str):
                    bad += [(f"{t}#{rid}.{c}", why) for why in text_violations(v)]
    rows = con.execute(f"SELECT id, report_date, match_id, confidence, {', '.join(SUMMARY)} FROM match_reports").fetchall()
    for rid, date, mid, conf, *vals in rows:
        if str(date or "") < FROM:
            continue
        if not sum(_labeled_coords(v) for v in vals):
            bad.append((f"match_reports#{rid}", "보유 요약에 높이·폭 좌표 없음"))
        if mid is not None and NO_AVG_POS not in str(conf or ""):
            miss = con.execute("""SELECT COUNT(*) FROM player_matches WHERE match_id=? AND COALESCE(minutes,0)>=45
                                  AND (avg_x IS NULL OR avg_y IS NULL)""", (mid,)).fetchone()[0]
            if miss:
                bad.append((f"match_reports#{rid}", f"45분+ 출전자 {miss}명 SofaScore 평균 위치 결손"))
    return bad


def md_violations(root):
    """reports/match-watch/**/*.md 중 conv_md()가 바꿀 것이 남은 파일."""
    return [f for f in sorted(root.rglob("*.md")) if (t := f.read_text(encoding="utf-8", errors="ignore")) != conv_md(t)]
