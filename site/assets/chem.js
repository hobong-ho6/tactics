/* 케미스트리 계산 — 화면 쪽 **단일 정본** (2026-09-26 신설).
 *
 * 왜 (사용자 지시 「케미 알고리즘 마저 처리해」):
 *   같은 계산이 `core/chem.py`(파이썬)와 `evolutions.html`(인라인 JS) 두 벌이었고,
 *   한때 **화면에만 아이콘·히어로 규칙이 없어** 같은 XI에 19점이나 갈렸다.
 *   상수는 export로 한 벌이 됐지만 **알고리즘은 주석으로만 묶여** 있었다 — 그건 ⑤문서 수준이라
 *   다음에 또 갈린다(불변규칙 13의 판정 기준).
 *
 * ⇒ ⑴ 화면 구현을 인라인에서 **이 파일 하나로** 빼고(가져다 쓰는 자리는 import만 한다)
 *   ⑵ **G27이 두 구현을 같은 입력에 돌려 결과를 대조한다**(node로 이 모듈을 그대로 부른다).
 *      갈리는 순간 커밋이 막힌다 — 이제 ③게이트다.
 *
 * ⛔ 기준선 표(`tiers`)를 여기 적지 않는다 — `core/chem.py CHEM`이 정본이고 export가 내보낸다.
 */
export const CHEM_KEYS = ['club', 'league', 'nation'];

const extraOf = (p, k) => {
  try {
    const e = typeof p.chem_extra === 'string' ? JSON.parse(p.chem_extra || '{}') : (p.chem_extra || {});
    return +((e || {})[k]) || 0;
  } catch (e) { return 0; }
};

/* 클럽·리그·국적별 링크 수. ⭐ 아이콘은 **스쿼드의 모든 리그에 +1**씩 얹는다(등급 B · FC27 유지). */
export function chemCounts(xi){
  const cnt = { club: {}, league: {}, nation: {} };
  for (const p of xi) for (const k of CHEM_KEYS){
    if (!p[k]) continue;
    cnt[k][p[k]] = (cnt[k][p[k]] || 0) + 1 + extraOf(p, k);
  }
  const icons = xi.filter(p => p.is_icon).length;
  if (icons) for (const lg in cnt.league) cnt.league[lg] += icons;
  return cnt;
}

/* 선수별 케미(0~3)와 합.
 * ⭐ 아이콘·히어로는 자리만 맞으면 **무조건 3**이다.
 * ⛔ **포지션이 맞아야 카운트에 든다** — 자리 안 맞는 선수는 본인이 0일 뿐 아니라 남의 링크에도
 *    기여하지 않는다. ⇒ **자리 맞는 XI만 넘긴다**(호출부가 거른다).
 * ⚠️⚠️ 이 값은 **하한이다 — 감독 케미를 넣지 않았다.** 감독은 국적·리그가 같은 선발에게 +1을 준다.
 */
export function chemOf(xi, tiers){
  const cnt = chemCounts(xi);
  const tier = (n, tb) => { for (const [need, pt] of tb || []) if (n >= need) return pt; return 0; };
  const per = xi.map(p => (p.is_icon || p.is_hero) ? 3
    : Math.min(3, CHEM_KEYS.reduce((s, k) => s + (p[k] ? tier(cnt[k][p[k]], (tiers || {})[k]) : 0), 0)));
  return { per, cnt, total: per.reduce((a, b) => a + b, 0) };
}
