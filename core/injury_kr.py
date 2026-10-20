"""부상·복귀 예상·날짜 한국어 표기 정본 (2026-10-20 사용자 지시 「부상이랑 복귀 예상도 한국어와 한국 기준 date로 표기 변경」).

player_status(FotMob 스냅샷)의 영문 값을 화면용 한국어로 바꾼다. ⛔ 표에 없는 영문은 **지어내지 않고** 원문에
「(원문)」을 붙여 돌려준다 — 새 어휘가 나오면 여기 한 줄을 더한다. 이미 한국어로 적힌 행(사람이 쓴 서술)은 그대로 둔다.
원문은 export가 함께 내보내고 화면이 툴팁(data-tip)으로 보여준다(검증 가능성).

날짜: player_status.as_of·pulled는 **날짜만**(YYYY-MM-DD) 있는 값이라 시각 변환 없이 「YYYY년 M월 D일(요)」로 쓴다.
      UTC 타임스탬프(…T…Z)가 오면 KST(+9)로 바꾼 뒤 같은 형식으로 쓴다.
"""
import datetime as dt
import re

INJURY_KR = {
    "Hamstring injury": "햄스트링 부상", "Knee injury": "무릎 부상", "Knock": "타박",
    "Cruciate ligament injury": "십자인대 부상", "Ankle injury": "발목 부상", "Muscle injury": "근육 부상",
    "Physical discomfort": "몸 상태 이상(경미)", "Achilles tendon injury": "아킬레스건 부상", "Wrist injury": "손목 부상",
    "Illness": "질병", "Thigh injury": "허벅지 부상", "Injured": "부상", "Calf injury": "종아리 부상",
    "Back injury": "허리 부상", "Leg injury": "다리 부상", "Hip injury": "고관절 부상", "Groin injury": "사타구니 부상",
    "Calf discomfort": "종아리 불편감", "Broken jaw": "턱 골절", "out": "결장", "doubt": "출전 불투명",
    "return_expected": "복귀 예상",
}
RETURN_KR = {
    "Doubtful": "출전 불투명", "A few days": "수일", "About 1-2 weeks": "약 1~2주", "Back in training": "훈련 복귀",
}
MONTHS = {m: i for i, m in enumerate(["January", "February", "March", "April", "May", "June", "July", "August",
                                       "September", "October", "November", "December"], 1)}
WD = "월화수목금토일"
_HANGUL = re.compile(r"[가-힣]")


def _kr_or_raw(v, table):
    if v is None or v == "":
        return v
    if v in table:
        return table[v]
    if _HANGUL.search(v):           # 사람이 이미 한국어로 쓴 서술 — 손대지 않는다
        return v
    return f"{v} (원문)"


def injury_kr(v):
    return _kr_or_raw(v, INJURY_KR)


def return_kr(v):
    """복귀 예상 — 「October 2026」 → 「2026년 10월」, 정해진 어휘는 표, 나머지는 원문 표시."""
    if v and re.fullmatch(r"([A-Z][a-z]+) (\d{4})", v) and v.split()[0] in MONTHS:
        m, y = v.split()
        return f"{y}년 {MONTHS[m]}월"
    return _kr_or_raw(v, RETURN_KR)


def date_kr(v):
    """YYYY-MM-DD → 「2026년 10월 17일(토)」. UTC 타임스탬프는 KST로 바꾼 뒤 같은 형식. 못 읽으면 원문."""
    if not v:
        return v
    try:
        if "T" in v:
            d = dt.datetime.fromisoformat(v.replace("Z", "+00:00")).astimezone(dt.timezone(dt.timedelta(hours=9))).date()
        else:
            d = dt.date.fromisoformat(v[:10])
    except ValueError:
        return v
    return f"{d.year}년 {d.month}월 {d.day}일({WD[d.weekday()]})"
