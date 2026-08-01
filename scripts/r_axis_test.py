#!/usr/bin/env python3
"""R축(보완 관계) 검정 — 사전 등록(docs/60-r-axis-prereg.md) 그대로 실행.

원시 상관 금지 · 경기별 평균을 뺀 잔차만 쓴다(obs#95).
확증 5쌍은 player_duties에서 선정됐고 부호도 사전 등록돼 있다.
"""
import math
import sqlite3
import sys
from itertools import combinations

DB = "data/avl_analysis.db"
SEASON = "2025-26"
EXCLUDE_PLAYERS = {"일링"}          # 임대 표본 (사전 등록)
GATE_PLAYERS = ["왓킨스", "부엔디아", "캐시", "맥긴", "오나나", "마첸", "카마라"]  # obs#95의 7명

# 확증 세트: (라벨, 선수A, 선수B, 지표, 예측부호)  — 사전 등록 §1
CONFIRMATORY = [
    ("H1a 캐시×디뉴 (교대 전진)",   "캐시",   "디뉴",   "fwd",  -1),
    ("H1b 캐시×마첸 (교대 전진)",   "캐시",   "마첸",   "fwd",  -1),
    ("H2  콘사×캐시 (전진 뒤 커버)", "콘사",   "캐시",   "fwd",  -1),
    ("H3  디뉴×로저스 (폭 vs 인버티드)", "디뉴", "로저스", "left", -1),
    ("H4  왓킨스×로저스 (박스 비우기)",  "왓킨스", "로저스", "mid",  -1),
]
# obs#95 재현(확증 세트 아님 — 참고 보고)
OBS95 = [
    ("부엔디아×마첸", "부엔디아", "마첸", "fwd", +0.178, 20),
    ("부엔디아×캐시", "부엔디아", "캐시", "fwd", -0.314, 33),
    ("맥긴×캐시",     "맥긴",     "캐시", "fwd", +0.198, 32),
    ("맥긴×마첸",     "맥긴",     "마첸", "fwd", -0.572, 19),
    ("마첸×캐시",     "마첸",     "캐시", "fwd", -0.168, 21),
]

# ---------- 통계 유틸 (순수 파이썬) ----------

def betacf(a, b, x):
    tiny, eps = 1e-30, 3e-16
    qab, qap, qam = a + b, a + 1.0, a - 1.0
    c, d = 1.0, 1.0 - qab * x / qap
    if abs(d) < tiny:
        d = tiny
    d = 1.0 / d
    h = d
    for m in range(1, 300):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        c = 1.0 + aa / c
        if abs(d) < tiny:
            d = tiny
        if abs(c) < tiny:
            c = tiny
        d = 1.0 / d
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        c = 1.0 + aa / c
        if abs(d) < tiny:
            d = tiny
        if abs(c) < tiny:
            c = tiny
        d = 1.0 / d
        de = d * c
        h *= de
        if abs(de - 1.0) < eps:
            break
    return h


def betai(a, b, x):
    """정칙화 불완전 베타 I_x(a,b)."""
    if x <= 0.0:
        return 0.0
    if x >= 1.0:
        return 1.0
    lbeta = (math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
             + a * math.log(x) + b * math.log(1.0 - x))
    if x < (a + 1.0) / (a + b + 2.0):
        return math.exp(lbeta) * betacf(a, b, x) / a
    return 1.0 - math.exp(lbeta) * betacf(b, a, 1.0 - x) / b


def pearson(xs, ys):
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxy = sum((a - mx) * (b - my) for a, b in zip(xs, ys))
    sxx = sum((a - mx) ** 2 for a in xs)
    syy = sum((b - my) ** 2 for b in ys)
    if sxx == 0 or syy == 0:
        return 0.0
    return sxy / math.sqrt(sxx * syy)


def p_two_sided(r, n):
    if n <= 2:
        return 1.0
    if abs(r) >= 1.0:
        return 0.0
    df = n - 2
    t = r * math.sqrt(df / (1.0 - r * r))
    return betai(df / 2.0, 0.5, df / (df + t * t))


def p_one_sided(r, n, predicted_sign):
    """부호가 예측대로면 양측/2, 반대면 1 − 양측/2."""
    p2 = p_two_sided(r, n)
    same = (r < 0) if predicted_sign < 0 else (r > 0)
    return p2 / 2.0 if same else 1.0 - p2 / 2.0


def bh_fdr(pvals, q):
    """BH 절차 → 생존 인덱스 집합과 임계값."""
    m = len(pvals)
    order = sorted(range(m), key=lambda i: pvals[i])
    kmax = 0
    for rank, i in enumerate(order, start=1):
        if pvals[i] <= q * rank / m:
            kmax = rank
    survivors = set(order[:kmax])
    crit = q * kmax / m if kmax else q / m
    return survivors, crit


def ols(y, X):
    """정규방정식 OLS. X는 절편 포함 행렬(리스트의 리스트). 반환 (beta, rss)."""
    k = len(X[0])
    XtX = [[sum(X[r][i] * X[r][j] for r in range(len(X))) for j in range(k)] for i in range(k)]
    Xty = [sum(X[r][i] * y[r] for r in range(len(X))) for i in range(k)]
    # 가우스 소거
    M = [row[:] + [Xty[i]] for i, row in enumerate(XtX)]
    for c in range(k):
        piv = max(range(c, k), key=lambda r: abs(M[r][c]))
        if abs(M[piv][c]) < 1e-12:
            return None, None
        M[c], M[piv] = M[piv], M[c]
        pv = M[c][c]
        M[c] = [v / pv for v in M[c]]
        for r in range(k):
            if r != c and M[r][c] != 0:
                f = M[r][c]
                M[r] = [a - f * b for a, b in zip(M[r], M[c])]
    beta = [M[i][k] for i in range(k)]
    rss = sum((y[r] - sum(beta[i] * X[r][i] for i in range(k))) ** 2 for r in range(len(X)))
    return beta, rss


def f_test(rss0, rss1, n, k0, k1):
    df1, df2 = k1 - k0, n - k1
    if df2 <= 0 or rss1 <= 0:
        return None, None
    F = ((rss0 - rss1) / df1) / (rss1 / df2)
    p = betai(df2 / 2.0, df1 / 2.0, df2 / (df2 + df1 * F)) if F > 0 else 1.0
    return F, p

# ---------- 지표 ----------

def metrics(map25):
    v = [10.0 if ch in ("X", "x") else float(ch) for ch in map25]
    tot = sum(v)
    if tot <= 0:
        return None
    return {
        "fwd":  sum(v[0:10]) / tot,                       # 행 0~1 = 전방
        "left": sum(v[i] for i in range(0, 25, 5)) / tot,  # 열 0 = 왼쪽
        "mid":  sum(v[i] for i in range(25) if i % 5 in (1, 2, 3)) / tot,
    }

# ---------- 데이터 ----------

def load(conn, players=None):
    q = ("SELECT name_kr, event_id, map25, possession FROM player_match_grids "
         "WHERE team='AVL' AND season=? AND map25 IS NOT NULL")
    rows = conn.execute(q, (SEASON,)).fetchall()
    data = {}   # event_id -> {name: metrics}
    for name, eid, m25, poss in rows:
        if name in EXCLUDE_PLAYERS:
            continue
        if players is not None and name not in players:
            continue
        mm = metrics(m25)
        if mm:
            data.setdefault(eid, {})[name] = mm
    return {e: d for e, d in data.items() if len(d) >= 3}   # 3명 이상 기록된 경기만


def residuals(data, key):
    """event -> {name: 그 경기 평균을 뺀 잔차}"""
    out = {}
    for eid, d in data.items():
        mean = sum(v[key] for v in d.values()) / len(d)
        out[eid] = {n: v[key] - mean for n, v in d.items()}
    return out


def pair_series(res, a, b):
    xs, ys, eids = [], [], []
    for eid, d in res.items():
        if a in d and b in d:
            xs.append(d[a]); ys.append(d[b]); eids.append(eid)
    return xs, ys, eids

# ---------- 실행 ----------

def main():
    conn = sqlite3.connect(DB)

    # ── 회귀 게이트: obs#95의 7명으로 한정해 5쌍 재현
    print("=" * 78)
    print("회귀 게이트 — obs#95 7명 한정 재현 (사전 등록 §1)")
    print("=" * 78)
    gate = load(conn, players=set(GATE_PLAYERS))
    gres = residuals(gate, "fwd")
    gate_ok = True
    for label, a, b, _key, exp_r, exp_n in OBS95:
        xs, ys, _ = pair_series(gres, a, b)
        r = pearson(xs, ys) if len(xs) > 2 else float("nan")
        ok = (len(xs) == exp_n) and abs(r - exp_r) < 0.02
        gate_ok &= ok
        print(f"  {label:14s} n={len(xs):3d}(기대{exp_n:3d})  r={r:+.3f}(기대{exp_r:+.3f})  {'OK' if ok else '**불일치**'}")
    if not gate_ok:
        print("\n⚠️ 게이트 불일치 — 파이프라인이 obs#95를 재현하지 못한다. 검정을 중단한다.")
        sys.exit(1)
    print("  → 게이트 통과. 본 검정을 14명 전체로 진행한다.\n")

    # ── 본 검정 (14명 전체)
    full = load(conn)
    names = sorted({n for d in full.values() for n in d})
    print(f"본 표본: 선수 {len(names)}명 · 경기 {len(full)}경기 (3명 이상 기록)\n")

    res = {k: residuals(full, k) for k in ("fwd", "left", "mid")}

    print("=" * 78)
    print("ⓑ 확증 세트 — duties가 지목한 5쌍 (단측, 부호 사전 등록)")
    print("=" * 78)
    rows = []
    for label, a, b, key, sign in CONFIRMATORY:
        xs, ys, eids = pair_series(res[key], a, b)
        n = len(xs)
        r = pearson(xs, ys) if n > 2 else float("nan")
        p1 = p_one_sided(r, n, sign) if n > 2 else 1.0
        p2 = p_two_sided(r, n) if n > 2 else 1.0
        rows.append((label, key, n, r, p1, p2, sign, eids))
    surv, crit = bh_fdr([r[4] for r in rows], 0.10)
    print(f"{'가설':34s} {'지표':5s} {'n':>3s} {'잔차r':>7s} {'p(단측)':>8s} {'p(양측)':>8s}  판정")
    for i, (label, key, n, r, p1, p2, sign, _e) in enumerate(rows):
        mark = "FDR생존" if i in surv else "-"
        if p1 < 0.01:
            mark += " +Bonf"
        if n > 2 and ((r < 0) != (sign < 0)):
            mark += " ⚠️부호반대"
        print(f"{label:34s} {key:5s} {n:3d} {r:+7.3f} {p1:8.4f} {p2:8.4f}  {mark}")
    n_surv = len(surv)
    verdict_b = ("강한 지지" if n_surv >= 3 else "약한 지지" if n_surv == 2 else "미달")
    print(f"\n  FDR(q=0.10) 생존 {n_surv}/5 · 임계 p≤{crit:.4f} → ⓑ **{verdict_b}**")
    neg = sum(1 for r in rows if r[3] < 0)
    print(f"  방향만 보면 예측대로(음수) {neg}/5\n")

    # ── ⓐ 대조군: 보완 점수가 경기 결과를 더 설명하는가
    print("=" * 78)
    print("ⓐ 대조군 — 중첩 모형 (결과 ~ 점유율)  vs  (결과 ~ 점유율 + 보완점수 C)")
    print("=" * 78)
    # 쌍별 잔차곱을 쌍 내부에서 표준화한 뒤 −부호를 붙여 '보완이 일어난 정도'로
    prod = {}   # eid -> [표준화된 −곱, ...]
    for label, a, b, key, sign in CONFIRMATORY:
        xs, ys, eids = pair_series(res[key], a, b)
        if len(xs) < 3:
            continue
        vals = [-(x * y) for x, y in zip(xs, ys)]
        m = sum(vals) / len(vals)
        sd = math.sqrt(sum((v - m) ** 2 for v in vals) / (len(vals) - 1)) or 1.0
        for eid, v in zip(eids, vals):
            prod.setdefault(eid, []).append((v - m) / sd)

    stats = {e: (xv, xo, ps) for e, xv, xo, ps in conn.execute(
        "SELECT s.event_id, s.xg_v, s.xg_o, m.possession FROM team_match_stats s "
        "LEFT JOIN matches m ON m.id=s.event_id WHERE s.team='AVL'")}
    poss_grid = dict(conn.execute(
        "SELECT event_id, avg(possession) FROM player_match_grids "
        "WHERE team='AVL' AND season=? AND possession IS NOT NULL GROUP BY event_id", (SEASON,)))

    y, X, used = [], [], []
    for eid, vals in prod.items():
        if len(vals) < 2:            # 최소 2쌍 관측된 경기만 (사전 등록: '≥2쌍')
            continue
        st = stats.get(eid)
        poss = poss_grid.get(eid) or (st[2] if st else None)
        if not st or st[0] is None or st[1] is None or poss is None:
            continue
        y.append(st[0] - st[1])
        X.append([1.0, poss, sum(vals) / len(vals)])
        used.append(eid)
    n = len(y)
    print(f"  유효 경기 n={n} (확증 쌍 2개 이상 관측 + xG + 점유율 보유)")
    if n < 25:
        print("  → 사전 등록 검정력 하한(n≥25) 미달 = **ⓐ 미달**")
        verdict_a = False
    else:
        b0, rss0 = ols(y, [[r[0], r[1]] for r in X])
        b1, rss1 = ols(y, X)
        F, p = f_test(rss0, rss1, n, 2, 3)
        sy = sum((v - sum(y) / n) ** 2 for v in y)
        print(f"  대조 모형 R²={1 - rss0 / sy:.3f} → 보완 포함 R²={1 - rss1 / sy:.3f}")
        print(f"  C 계수 = {b1[2]:+.4f} (양수여야 통과) · F({1},{n - 3})={F:.3f} · p={p:.4f}")
        verdict_a = (b1[2] > 0) and (p < 0.05)
        print(f"  → ⓐ **{'통과' if verdict_a else '미달'}**")

    # ── 탐색: 91쌍 전수 (근거 아님, 다음 가설용)
    print("\n" + "=" * 78)
    print("탐색 — 전수 쌍 (⚠️ 근거 아님: 사전 등록 없이 고른 것은 다음 가설로만)")
    print("=" * 78)
    expl = []
    for key in ("fwd", "left", "mid"):
        for a, b in combinations(names, 2):
            xs, ys, _ = pair_series(res[key], a, b)
            if len(xs) >= 20:
                r = pearson(xs, ys)
                expl.append((p_two_sided(r, len(xs)), r, len(xs), key, a, b))
    expl.sort()
    print(f"  n≥20 쌍-지표 조합 {len(expl)}건 · 미보정 p<0.05 {sum(1 for e in expl if e[0] < 0.05)}건")
    for p, r, n_, key, a, b in expl[:8]:
        print(f"    {a}×{b:8s} {key:5s} n={n_:3d} r={r:+.3f} p={p:.4f}")

    # ── 처분 (사전 등록 §2 ⓓ)
    print("\n" + "=" * 78)
    if verdict_a and verdict_b == "강한 지지":
        print("처분: **R축 신설** (ⓐ 통과 + ⓑ 강한 지지)")
    elif verdict_b in ("강한 지지", "약한 지지"):
        print(f"처분: **소프트 유지** — ⓑ {verdict_b}이나 ⓐ 미달 → C6 수준에 머문다. 축 신설 안 함")
    else:
        print("처분: **R축 기각** (ⓑ 미달) — A축 선례. 표본만 보존한다")
    print("=" * 78)


if __name__ == "__main__":
    main()
