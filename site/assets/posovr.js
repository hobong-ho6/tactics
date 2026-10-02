/* 포지션별 OVR 산정식 — `core/position_ovr.py`를 옮긴 것이다(2026-10-02 · migration 091).
   ⛔ 가중치·포지션→그룹 표는 여기 적지 않는다 — export가 `EVO.ovr_model`({groups, weights, approx})로 준다.
   ⛔ 계산 규칙이 파이썬과 한 글자라도 다르면 게이트 G31이 막는다(같은 입력으로 대조).
   ⚠️ 가중치는 FC27 비진화 카드로 적합한 값이다(등급 C) — 절대값보다 진화 전후 **차이**로 쓴다. */
export function posOvrRaw(attrs, pos, model) {
  const w = model?.weights?.[model?.groups?.[pos]];
  if (!w || !attrs) return null;
  let s = 0, t = 0;
  for (const [k, v] of Object.entries(w)) {
    if (attrs[k] == null) return null;          // ⛔ 결손을 0으로 세지 않는다
    s += attrs[k] * v; t += v;
  }
  return t ? s / t : null;
}

export function posOvr(attrs, pos, model) {
  const v = posOvrRaw(attrs, pos, model);
  return v == null ? null : Math.floor(v + 0.5);
}
