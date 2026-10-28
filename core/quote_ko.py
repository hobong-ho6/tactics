"""외국어 인용 한국어 병기(불변규칙 11) — 검출·판정 단일 정본 (2026-10-28 신설).

규칙(CLAUDE.md 불변규칙 11): 원문 「…」 **바로 뒤 괄호에 한국어 번역**. 번역 없이 원문만 두지 않는다.
⛔ 2026-10-28 실측: 9-13 지시 이후에도 감독 프로필 11건 · 직무·obs 수백 건이 번역 없이 남아 있었다
   (「조심하자」로는 안 지켜진다 — 불변규칙 13) ⇒ 게이트 G42(새로 쓰거나 바뀐 행만) + 이 모듈.

판정:
  · 외국어 인용 = 「」 안에 한글이 없고, 라틴 문자 단어 2개 이상 또는 일본어·한자 4자 이상
  · 번역 있음 = 닫는 」 뒤(공백·「·」·「,」 무시)에 한글이 든 (…)/（…）가 오거나, 「— 「한글…」」 형태가 온다
  · 「」 안이 고유명 하나·약어 하나면 대상 아님(단어 2개 미만) · 코드·표·조건식 조각(| = < > { } · a_b · X(1))도 대상 아님
G14 연동: `only_translation_inserts(old, new)` — 바뀐 내용이 전부 「」 바로 뒤 한글 괄호 삽입이면 True
  (불변규칙 2의 「덧붙임만」 취지를 해치지 않는 유일한 중간 삽입이다).
"""
import re

__all__ = ["missing", "only_translation_inserts", "db_violations", "TEXT_FIELDS"]

QUOTE = re.compile(r"「([^「」]{1,1200})」")
HAN = re.compile(r"[가-힣]")
LATIN_WORD = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿĀ-ž'’]{2,}")
CJK = re.compile(r"[぀-ヿ一-鿿]")
DOMAIN = re.compile(r"\S+\.(?:com|net|org|de|es|it|fr|pt|nl|no|jp|co\.uk|tv)\b\S*")
CODE = re.compile(r"[|=<>{}]|[A-Za-z]_[A-Za-z]|\w\(\d")   # 코드·표·조건식 조각은 번역 대상이 아니다
AFTER_OK = re.compile(r"^[\s·,]{0,3}(?:[(（][^()（）]*[가-힣][^()（）]*[)）]|[—–-]\s*「[^」]*[가-힣])")
INSERT_OK = re.compile(r"^\s?[(（][^()（）]*[가-힣][^()（）]*[)）]$")
INSERT_PREFIX = re.compile(r"\s?[(（][^()（）]*[가-힣][^()（）]*[)）]")

# 검사 대상 텍스트 필드 — 서사·판정을 담는 표(화면·리포트로 나가는 산문)
TEXT_FIELDS = {
    "observations": ["claim", "evidence"],
    "player_duties": ["duties", "execution", "adherence", "game_role_implication", "sample_note"],
    "manager_profiles": ["content", "evidence"],
}


def _foreign(q):
    if HAN.search(q) or CODE.search(q):
        return False
    q = DOMAIN.sub("", q)
    words = [w for w in LATIN_WORD.findall(q) if any(c.islower() for c in w)]   # 약어(PL/EL)·도메인은 단어로 안 센다
    return len(words) >= 2 or len(CJK.findall(q)) >= 4


def missing(text):
    """[(start, end, quote)] — 번역이 붙지 않은 외국어 인용."""
    out = []
    if not text:
        return out
    for m in QUOTE.finditer(text):
        q = m.group(1)
        if _foreign(q) and not AFTER_OK.match(text[m.end():m.end() + 400]):
            out.append((m.start(), m.end(), q))
    return out


def only_translation_inserts(old, new):
    """old → new 변경이 「」 바로 뒤 한글 괄호 삽입뿐인가. 두 문자열을 나란히 훑는다(결정적 · difflib 정렬 오판 없음).
    「」 바로 뒤에서 new에 한글 괄호가 오고 old의 같은 자리에 그 괄호가 없으면 삽입으로 보고 건너뛴다."""
    if old is None or new is None or old == new:
        return old == new
    i = j = 0
    while j < len(new):
        if j > 0 and new[j - 1] == "」" and i > 0 and old[i - 1] == "」":
            m = INSERT_PREFIX.match(new, j)
            if m and not old.startswith(new[j:m.end()], i):
                j = m.end()
                continue
        if i < len(old) and old[i] == new[j]:
            i += 1
            j += 1
            continue
        return False
    return i == len(old)


def db_violations(con):
    """[\"table.field#key\"] — TEXT_FIELDS 전수에서 번역이 붙지 않은 외국어 인용(G42가 쓴다)."""
    out = []
    for t, fs in TEXT_FIELDS.items():
        key = "regime_id||':'||axis" if t == "manager_profiles" else "id"
        for r in con.execute(f"SELECT {key}, {', '.join(fs)} FROM {t}"):
            for f, x in zip(fs, r[1:]):
                if missing(x):
                    out.append(f"{t}.{f}#{r[0]}")
    return out
