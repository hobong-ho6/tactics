"""영상 구현 주장(video_impl_claims) 읽기 층 규칙 정본 (2026-10-20 · migration 113).

왜: 자유 문구 주장(team_axis·instruction·limit)의 한국어 전문이 91자까지 길어져 배지 옆 굵은 두 줄로 읽혔다.
  사용자 지시 「40자가 넘는 구현 주장은 필요 내용만 요약해도 되지만 긴 내용을 어떻게 잘 전달할 수 있을지 검토해서 개선」.
  근거(NN/g): 화면 글은 훑어 읽히고 시선은 문장 앞 몇 단어에 머문다 → ① 결론 먼저인 짧은 헤드라인 ② 덩어리로 나눈 요점
  ③ 전문은 필요할 때(툴팁). ⇒ 40자를 넘으면 headline_kr(≤40) + points_kr(2~5개)를 필수로 한다.
⛔ 이 모듈 하나가 기준이다 — scripts/write_video_summary.py(적재 거부)와 scripts/gates.py G17(결손 차단)이 함께 쓴다.
"""
import json

FREE_AXES = ("team_axis", "instruction", "limit")   # 자유 문구 축 — 한국어 칸·헤드라인 규칙 대상
HEADLINE_MAX = 40
POINTS_MIN, POINTS_MAX = 1, 5


def needs_headline(value_kr):
    return len((value_kr or "").strip()) > HEADLINE_MAX


def problems(axis, value_kr, headline_kr, points_kr):
    """규칙 위반 목록(빈 목록 = 통과). points_kr는 JSON 문자열 또는 리스트."""
    if axis not in FREE_AXES or not needs_headline(value_kr):
        return []
    out = []
    h = (headline_kr or "").strip()
    if not h:
        out.append(f"전문이 {HEADLINE_MAX}자를 넘는데 headline_kr가 없다")
    elif len(h) > HEADLINE_MAX:
        out.append(f"headline_kr가 {len(h)}자 — {HEADLINE_MAX}자 이하로")
    pts = points_kr
    if isinstance(pts, str):
        try:
            pts = json.loads(pts)
        except ValueError:
            pts = None
    if not isinstance(pts, list) or not (POINTS_MIN <= len(pts) <= POINTS_MAX) \
            or not all(isinstance(p, str) and p.strip() for p in pts):
        out.append(f"points_kr는 {POINTS_MIN}~{POINTS_MAX}개 문자열 배열이어야 한다")
    return out
