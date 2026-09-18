/* 선수 화면 시각화 — 퍼센타일 피자 · 버전 덤벨 · 폼 리본 (2026-09-18, 사용자 지시 「선수 화면 시각화도 이어서」).
   dataviz 규약: 시리즈색은 역할별 고정(공격/창조·소유/수비 3색 — 다크 서피스 검증 통과) · 값 라벨은 선택적 · 표 뷰(기존 막대·표)는 남긴다.
   FBref/StatsBomb 스카우팅 리포트의 「피자 차트」 형식 — 조각 = 지표, 반지름 = 동포지션 백분위, 색 = 지표 묶음. */
const esc = s => String(s ?? '').replace(/[&<>"]/g, c => ({ '&':'&amp;', '<':'&lt;', '>':'&gt;', '"':'&quot;' }[c]));
export const GROUP_COL = { 공격: '#d95926', '창조·소유': '#3987e5', 수비: '#199e70', 선방: '#d95926', 배급: '#3987e5', 지배: '#199e70' };
const GROUPS = {
  field: [
    ['공격', ['non_penalty_xg', 'shots', 'ShotsOnTarget', 'touches_opp_box', 'goals', 'expected_goals_on_target', 'dribbles_succeeded', 'headed_shots']],
    ['창조·소유', ['expected_assists', 'chances_created', 'big_chance_created_team_title', 'successful_passes_accuracy', 'successful_passes', 'line_breaking_passes', 'long_balls_accurate', 'crosses_succeeeded', 'touches', 'dispossessed']],
    ['수비', ['matchstats.headers.tackles', 'interceptions', 'recoveries', 'defensive_actions', 'duel_won_percent', 'aerials_won_percent', 'clearances', 'blocked_shots', 'poss_won_att_3rd_team_title', 'dribbled_past']],
  ],
  gk: [
    ['선방', ['save_percentage', 'saves', 'goals_prevented', 'penalty_save_percent', 'goals_conceded']],
    ['배급', ['successful_passes_accuracy', 'long_ball_succeeeded_accuracy', 'long_balls_accurate', 'successful_passes', 'touches']],
    ['지배', ['keeper_high_claim', 'keeper_sweeper', 'clean_sheet_team_title', 'error_led_to_goal', 'aerials_won_percent']],
  ],
};
/* rows = fbref 행(metric_key·metric_kr·percentile_per90/percentile·stat_value). 묶음당 최대 5조각. */
export function pizza(rows, { W = 360, gk = false } = {}){
  const byKey = {}; for (const r of rows) byKey[r.metric_key] ??= r;
  const slices = [];
  for (const [g, keys] of GROUPS[gk ? 'gk' : 'field']){
    for (const k of keys){ const r = byKey[k]; if (r && slices.filter(s => s.g === g).length < 5) slices.push({ g, k, r, p: r.percentile_per90 ?? r.percentile ?? 0 }); }
  }
  if (slices.length < 4) return '';
  const H = W, cx = W / 2, cy = H / 2, R = W / 2 - 46, r0 = 18, n = slices.length, step = 2 * Math.PI / n;
  const pol = (a, r) => [cx + r * Math.cos(a), cy + r * Math.sin(a)];
  const wedge = (a0, a1, ri, ro) => { const [x0, y0] = pol(a0, ro), [x1, y1] = pol(a1, ro), [x2, y2] = pol(a1, ri), [x3, y3] = pol(a0, ri);
    return `M${x0},${y0} A${ro},${ro} 0 0 1 ${x1},${y1} L${x2},${y2} A${ri},${ri} 0 0 0 ${x3},${y3} Z`; };
  const gap = 0.018;   // 조각 사이 서피스 갭(라디안) — 테두리 대신 빈틈으로 가른다
  const parts = slices.map((s, i) => { const a0 = -Math.PI / 2 + i * step + gap, a1 = a0 + step - gap * 2, ro = r0 + (R - r0) * Math.max(.04, s.p / 100);
    const am = (a0 + a1) / 2; const [lx, ly] = pol(am, R + 14); const [vx, vy] = pol(am, Math.max(ro - 12, r0 + 10));
    const col = GROUP_COL[s.g];
    return `<g><path d="${wedge(a0, a1, r0, ro)}" fill="${col}" fill-opacity=".85"><title>${esc(s.r.metric_kr || s.k)} — 동포지션 백분위 ${s.p} · 시즌 ${esc(s.r.stat_value ?? '—')}${s.r.per90 != null ? ` · ${s.r.per90}/90` : ''}</title></path>
      <path d="${wedge(a0, a1, r0, R)}" fill="none" stroke="rgba(255,255,255,.06)"/>
      <text x="${vx}" y="${vy + 3.5}" text-anchor="middle" font-size="10" font-weight="700" fill="var(--txt)">${s.p}</text>
      <text x="${lx}" y="${ly + 3.5}" text-anchor="${Math.cos(am) > .2 ? 'start' : Math.cos(am) < -.2 ? 'end' : 'middle'}" font-size="10" fill="var(--dim)">${esc(s.r.metric_kr || s.k)}</text></g>`; }).join('');
  const rings = [25, 50, 75, 100].map(p => `<circle cx="${cx}" cy="${cy}" r="${r0 + (R - r0) * p / 100}" fill="none" stroke="rgba(255,255,255,.08)"/>`).join('');
  const groups = [...new Set(slices.map(s => s.g))];
  return `<svg width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" role="img" aria-label="리그 동포지션 백분위 피자" style="display:block;margin:0 auto">${rings}${parts}
      <circle cx="${cx}" cy="${cy}" r="${r0 - 2}" fill="var(--panel)"/></svg>
    <div class="lg" style="justify-content:center">${groups.map(g => `<span><i style="background:${GROUP_COL[g]}"></i>${esc(g)}</span>`).join('')}<span class="dim">반지름 = 백분위(안쪽 고리 25·50·75)</span></div>`;
}

/* 버전 덤벨 — 항목(OVR·6스탯)마다 한 줄, 시점(FC25 출시 → FC26 출시 → FC26 라이브 → FC27)을 점으로 잇는다. 최신 시점이 진하다. */
export function dumbbell(seq, keys, { W = 520 } = {}){
  if (!seq || seq.length < 2) return '';
  const rowH = 28, L = 56, R = 60, T = 24, H = T + keys.length * rowH + 6;
  const vals = keys.flatMap(([k]) => seq.map(s => s[k]).filter(v => v != null));
  const lo = Math.max(0, Math.min(...vals) - 6), hi = Math.min(99, Math.max(...vals) + 4);   // 값 대역에 붙여 점이 한쪽에 몰리지 않게
  const x = v => L + (W - L - R) * ((v - lo) / Math.max(1, hi - lo));
  const shade = i => 0.35 + 0.65 * (i / Math.max(1, seq.length - 1));
  const stepT = (hi - lo) > 40 ? 10 : 5; const ticks = []; for (let v = Math.ceil(lo / stepT) * stepT; v <= hi; v += stepT) ticks.push(v);
  const grid = ticks.map(v => `<line x1="${x(v)}" x2="${x(v)}" y1="${T - 6}" y2="${H - 4}" stroke="var(--viz-grid)"/><text x="${x(v)}" y="${T - 10}" text-anchor="middle" class="dim" font-size="10">${v}</text>`).join('');
  const rows = keys.map(([k, label], i) => { const y = T + i * rowH + 12; const pts = seq.map((s, j) => ({ v: s[k], j })).filter(p => p.v != null);
    if (!pts.length) return '';
    const xs = pts.map(p => x(p.v)); const line = pts.length > 1 ? `<line x1="${Math.min(...xs)}" x2="${Math.max(...xs)}" y1="${y}" y2="${y}" stroke="var(--viz-us)" stroke-opacity=".35" stroke-width="2"/>` : '';
    const dots = pts.map(p => `<g><circle cx="${x(p.v)}" cy="${y}" r="6.5" fill="var(--panel)"/><circle cx="${x(p.v)}" cy="${y}" r="4.5" fill="var(--viz-us)" fill-opacity="${shade(p.j)}"><title>${esc(seq[p.j]._label)} ${label} ${p.v}</title></circle></g>`).join('');
    const last = pts[pts.length - 1], first = pts[0]; const d = last.v - first.v;
    return `<g><text x="${L - 8}" y="${y + 3.5}" text-anchor="end" font-size="11" fill="var(--dim)">${esc(label)}</text>${line}${dots}
      <text x="${x(last.v) + 9}" y="${y + 3.5}" font-size="11" font-weight="700" fill="var(--txt)">${last.v}</text>
      ${d ? `<text x="${x(last.v) + 9 + 18}" y="${y + 3.5}" font-size="10" fill="${d > 0 ? 'var(--ok)' : 'var(--bad)'}">${d > 0 ? '+' : ''}${d}</text>` : ''}</g>`; }).join('');
  return `<svg width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" role="img" aria-label="버전별 스탯 변화">${grid}${rows}</svg>
    <div class="lg">${seq.map((s, j) => `<span><i style="background:var(--viz-us);opacity:${shade(j)}"></i>${esc(s._label)}</span>`).join('')}<span class="dim">Δ = 첫 시점 대비</span></div>`;
}

/* 폼 리본 — 경기별 평점. 6.5/7.5 기준선(띠), 시즌 경계(40일 이상 공백) 점선, 점 색 = 구간. 캡션 hover는 호출측이 붙인다. */
export function formRibbon(fm, { W = 520 } = {}){
  if (!fm || !fm.length) return '';
  const H = 130, L = 30, R = 12, T = 12, B = 24, min = 5.5, max = 9.5;
  const px = i => L + i * (W - L - R) / Math.max(1, fm.length - 1), py = r => T + (H - T - B) * (1 - (Math.min(max, Math.max(min, r)) - min) / (max - min));
  const band = (a, b, col) => `<rect x="${L}" y="${py(b)}" width="${W - L - R}" height="${py(a) - py(b)}" fill="${col}" opacity=".07"/>`;
  const bands = band(7.5, max, 'var(--ok)') + band(6.5, 7.5, 'var(--warn)') + band(min, 6.5, 'var(--bad)');
  const refs = [6.5, 7.5].map(v => `<line x1="${L}" x2="${W - R}" y1="${py(v)}" y2="${py(v)}" stroke="var(--viz-grid)"/><text x="${L - 6}" y="${py(v) + 3.5}" text-anchor="end" font-size="10" fill="var(--dim)">${v}</text>`).join('');
  const breaks = fm.map((f, i) => i > 0 && (new Date(f[0]) - new Date(fm[i - 1][0])) / 864e5 > 40 ? `<line x1="${(px(i) + px(i - 1)) / 2}" x2="${(px(i) + px(i - 1)) / 2}" y1="${T}" y2="${H - B}" stroke="var(--line)"/><text x="${px(i)}" y="${H - 8}" font-size="10" fill="var(--dim)">${f[0].slice(0, 7)}</text>` : '').join('');
  const line = `<polyline points="${fm.map((f, i) => `${px(i)},${py(f[1])}`).join(' ')}" fill="none" stroke="var(--txt)" stroke-opacity=".5" stroke-width="2" stroke-linejoin="round"/>`;
  const col = r => r >= 7.5 ? 'var(--ok)' : r >= 6.5 ? 'var(--warn)' : 'var(--bad)';
  const dots = fm.map((f, i) => `<circle cx="${px(i)}" cy="${py(f[1])}" r="6" fill="var(--panel)" pointer-events="none"/><circle cx="${px(i)}" cy="${py(f[1])}" r="4" fill="${col(f[1])}" pointer-events="none"/>`).join('');
  const hits = fm.map((f, i) => `<rect x="${px(i) - (W - L - R) / Math.max(1, fm.length - 1) / 2}" y="${T}" width="${(W - L - R) / Math.max(1, fm.length - 1)}" height="${H - T - B}" fill="transparent" data-i="${i}" style="cursor:pointer"/>`).join('');
  const first = fm[0][0], last = fm[fm.length - 1][0];
  return `<svg width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" role="img" aria-label="경기별 평점 추이">${bands}${refs}${breaks}${line}${dots}${hits}
      <text x="${L}" y="${H - 8}" font-size="10" fill="var(--dim)">${first}</text><text x="${W - R}" y="${H - 8}" text-anchor="end" font-size="10" fill="var(--dim)">${last}</text></svg>`;
}
