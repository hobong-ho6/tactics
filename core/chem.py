"""케미스트리 규칙 **단일 정본** (2026-09-26 신설).

왜 (사용자 지시 「동일한 기능을 나눠서 여러 군데서 사용하고 있는지 검수해봐」):
  같은 계산이 두 벌이었고 **규칙이 갈려 있었다** — `scripts/sbc_solve.py chem_total`에는 있는
  아이콘·히어로 규칙이 `site/evolutions.html chemOf`에는 **통째로 없었다**.
  ⇒ SBC 탭과 케미스트리 탭이 같은 스쿼드에 다른 점수를 낼 수 있었다(지금은 보유 아이콘·히어로가
    0명이라 값이 같아 보였을 뿐이다 — 한 장 들어오면 그날 조용히 갈린다).

⇒ 파이썬 쪽 계산을 여기로 모으고(불변규칙 4 「집계 로직은 core/만 쓴다」),
  **기준선 표는 export가 화면으로 내보낸다** — 화면이 같은 표를 다시 적지 않게 한다(불변규칙 13 ②).
⚠️ 알고리즘 자체는 언어가 달라 한 벌로 못 만든다. 대신 규칙을 이 파일 주석 하나로 고정하고,
   화면 구현은 여기를 옮긴 것임을 명시한다. 값이 갈리면 G27이 잡는다.
"""
import json

# FC27 케미 기준선 — 2026-09-25 조사에서 FC27 값과 일치 확인(등급 B).
# 화면은 이 표를 `export.py`가 내보낸 `chem_tiers`로 받는다 — 다시 적지 않는다.
CHEM = {"club": [(7, 3), (4, 2), (2, 1)],
        "league": [(8, 3), (5, 2), (3, 1)],
        "nation": [(8, 3), (5, 2), (2, 1)]}


def extra(p, k):
    """아이콘·히어로의 **추가 링크 기여**. ⛔ 규칙을 우리가 쓰지 않고 fut.gg 값(`chem_extra`)을 쓴다
       (migration 044와 같은 방침) — EA가 버전마다 바꾸기 때문이다.
       ⚠️ 실제로 바뀌었다: FC27 2026-09-14 런치 업데이트로 **아이콘 국적 +2 → +1 · 히어로 리그 +2 → +1**.
          값을 코드에 박았다면 그날 조용히 틀렸을 것이다(근거 등급 B)."""
    try:
        return int((json.loads(p["chem_extra"]) or {}).get(k) or 0) if p.get("chem_extra") else 0
    except Exception:                                    # noqa: BLE001
        return 0


def counts(xi):
    """클럽·리그·국적별 링크 수. ⭐ 아이콘은 **스쿼드의 모든 리그에 +1**씩 얹는다(등급 B · FC27 유지)."""
    cnt = {k: {} for k in CHEM}
    for p in xi:
        for k in CHEM:
            if p[k]:
                cnt[k][p[k]] = cnt[k].get(p[k], 0) + 1 + extra(p, k)
    icons = sum(1 for p in xi if p.get("is_icon"))
    if icons:
        for lg in cnt["league"]:
            cnt["league"][lg] += icons
    return cnt


def per_player(xi):
    """선수별 케미(0~3). ⭐ 아이콘·히어로는 자리만 맞으면 **무조건 3**이다.

    ⛔ **포지션이 맞아야 카운트에 든다** — 자리 안 맞는 선수는 본인이 0일 뿐 아니라
       **남의 링크에도 기여하지 않는다**(2026-09-25 조사: 「Out of position, they sit at 0
       and do not contribute links to teammates」). 그래서 이건 배치 문제다 —
       **자리가 맞는 선수만 `xi`에 담아 부른다.**
    """
    cnt = counts(xi)

    def tier(n, tb):
        for need, pt in tb:
            if n >= need:
                return pt
        return 0
    return [3 if (p.get("is_icon") or p.get("is_hero")) else
            min(3, sum(tier(cnt[k][p[k]], CHEM[k]) if p[k] else 0 for k in CHEM)) for p in xi]


def chem_total(xi):
    """팀 케미 합.

    ⚠️⚠️ **이 값은 하한이다 — 감독 케미를 넣지 않았다.** 감독은 국적·리그가 같은 선발에게 **+1**을
       주고(선수당 1점 상한) SBC 스쿼드에도 적용된다. 어느 감독을 쓸지는 우리가 모르므로 세지 않는다.
       ⇒ 우리가 「케미 부족」이라 해도 **실제로는 감독으로 메워질 수 있다**(화면이 그렇게 적는다)."""
    return sum(per_player(xi))
