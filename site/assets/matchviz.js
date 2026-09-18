/* 경기 시각화 — 타임라인 · 팀 대조(버터플라이) · 하프 비교 (2026-09-18, 사용자 지시 「경기 분석 데이터를 타임라인에 맞춰 시각적으로」).
   dataviz 규약: 시리즈색 2개(우리 --viz-us / 상대 --viz-them, 다크 서피스 검증 통과) · 얇은 막대(≤24px, 데이터 끝 4px 라운드) ·
   2px 서피스 갭·링 · 격자 hairline · 값 라벨은 선택적, 호버 툴팁은 보조(표 뷰 = 기존 수치 표) · 텍스트는 시리즈색을 입지 않는다. */
const esc = s => String(s ?? '').replace(/[&<>"]/g, c => ({ '&':'&amp;', '<':'&lt;', '>':'&gt;', '"':'&quot;' }[c]));
const US = 'var(--viz-us)', THEM = 'var(--viz-them)', SURF = 'var(--panel)', GRID = 'var(--viz-grid)';
const num = v => (v == null || v === '' ? null : Number(v));
const fmt = (v, d = 0) => v == null ? '—' : Number(v).toLocaleString(undefined, { maximumFractionDigits: d, minimumFractionDigits: d });

/* ── 1. 타임라인 ── 0~90(+추가) 분. 스코어 국면을 옅은 띠로, 득점은 큰 점(우리 위·상대 아래), 교체/카드는 작은 표식. */
export function timeline(r, team, W = 900){
  const ev = (r.events || []).slice().sort((a, b) => a.minute - b.minute);
  if (!ev.length) return `<div class="vz wide"><h4>타임라인</h4><span class="dim" style="font-size:12px">이벤트 미수집 — match_events가 비어 있다(수집 회차가 채운다).</span></div>`;
  const end = Math.max(90, ...ev.map(e => e.minute)) + 2;
  const H = 176, L = 28, R = 20, x = m => L + (W - L - R) * (m / end), mid = 88;   // 득점 라벨(±12·±22)과 보조 표식(±40)을 겹치지 않게 띄운다
  // 스코어 국면 띠 — 득점류 이벤트로 (score_v, score_o) 궤적을 만든다
  const goals = ev.filter(e => /goal$/.test(e.kind) && e.score_v != null);
  let bands = '', sv = 0, so = 0, from = 0;
  const band = (a, b, state) => state === 'level' ? '' :
    `<rect x="${x(a)}" y="${mid - 22}" width="${x(b) - x(a)}" height="44" fill="${state === 'lead' ? US : THEM}" opacity=".10"/>`;
  for (const g of goals){ bands += band(from, g.minute, sv > so ? 'lead' : sv < so ? 'trail' : 'level'); sv = g.score_v; so = g.score_o; from = g.minute; }
  bands += band(from, end, sv > so ? 'lead' : sv < so ? 'trail' : 'level');
  const ticks = [0, 15, 30, 45, 60, 75, 90].filter(t => t <= end).map(t =>
    `<line x1="${x(t)}" x2="${x(t)}" y1="${mid - 30}" y2="${mid + 30}" stroke="${GRID}"/><text x="${x(t)}" y="${H - 6}" text-anchor="middle" class="dim sm">${t}′</text>`).join('');
  const half = `<line x1="${x(45)}" x2="${x(45)}" y1="${mid - 52}" y2="${mid + 52}" stroke="var(--line)"/><text x="${x(45)}" y="${mid - 58}" text-anchor="middle" class="dim sm">HT</text>`;
  const axis = `<line x1="${x(0)}" x2="${x(end)}" y1="${mid}" y2="${mid}" stroke="var(--line)"/>`;
  const KIND = { goal:'득점', own_goal:'자책골', penalty_goal:'PK 득점', penalty_miss:'PK 실축', sub:'교체', yellow:'경고', red:'퇴장', gk_change:'GK 교체', var:'VAR' };
  const who = e => e.player_name || '';
  const tip = e => `${e.minute}′ ${e.side === 'v' ? team : (r.opponent || '상대')} · ${KIND[e.kind] || e.kind}: ${who(e)}` +
    (e.assist_name ? ` (도움 ${e.assist_name})` : '') + (e.player_out_name ? ` ← ${e.player_out_name} OUT` : '') +
    (e.score_v != null ? ` · ${e.score_v}-${e.score_o}` : '') + (e.note ? ` — ${e.note}` : '');
  // 같은 분의 표식이 겹치지 않게 살짝 밀어낸다(보조 표식만)
  const seen = {};
  const marks = ev.map(e => {
    const up = e.side === 'v'; const cx = x(e.minute); const t = esc(tip(e));
    if (/goal$/.test(e.kind) || e.kind === 'penalty_miss'){
      const cy = up ? mid - 16 : mid + 16, col = up ? US : THEM;
      const lab = `${who(e)}${e.assist_name ? ` <tspan class="dim">(${esc(e.assist_name)})</tspan>` : ''}`;
      const score = e.score_v != null ? `<text x="${cx}" y="${up ? cy - 22 : cy + 30}" text-anchor="middle" class="sm"><tspan font-weight="700">${e.score_v}–${e.score_o}</tspan></text>` : '';
      return `<g class="hit" data-tip="${t}"><circle cx="${cx}" cy="${cy}" r="9" fill="${SURF}"/><circle cx="${cx}" cy="${cy}" r="7" fill="${col}"/>
        ${e.kind === 'own_goal' ? `<text x="${cx}" y="${cy + 3.5}" text-anchor="middle" class="sm" font-weight="700">OG</text>` : e.kind === 'penalty_miss' ? `<text x="${cx}" y="${cy + 3.5}" text-anchor="middle" class="sm">✕</text>` : ''}
        <text x="${cx}" y="${up ? cy - 12 : cy + 19}" text-anchor="middle" class="sm">${lab}</text>${score}</g>`;
    }
    const k = `${e.minute}|${e.side}`; seen[k] = (seen[k] || 0) + 1; const off = (seen[k] - 1) * 7;
    const cy = up ? mid - 42 - off : mid + 42 + off;
    if (e.kind === 'sub' || e.kind === 'gk_change')
      return `<g class="hit" data-tip="${t}"><rect x="${cx - 4}" y="${cy - 4}" width="8" height="8" rx="1.5" fill="${SURF}"/>
        <path d="M${cx - 3.5},${cy + 3} L${cx},${cy - 3.5} L${cx + 3.5},${cy + 3} Z" fill="${e.kind === 'gk_change' ? 'var(--warn)' : 'var(--dim)'}"/></g>`;
    if (e.kind === 'yellow' || e.kind === 'red')
      return `<g class="hit" data-tip="${t}"><rect x="${cx - 3}" y="${cy - 5}" width="6" height="10" rx="1" fill="${e.kind === 'red' ? 'var(--bad)' : 'var(--warn)'}"/></g>`;
    return `<g class="hit" data-tip="${t}"><circle cx="${cx}" cy="${cy}" r="3.5" fill="var(--dim)"/></g>`;
  }).join('');
  const nSub = ev.filter(e => e.kind === 'sub' || e.kind === 'gk_change').length, nCard = ev.filter(e => /yellow|red/.test(e.kind)).length;
  return `<div class="vz wide"><h4>타임라인 <span class="dim">— 득점 ${goals.length} · 교체 ${nSub} · 카드 ${nCard} · 위 = ${esc(team)}, 아래 = ${esc(r.opponent || '상대')}</span></h4>
    <svg width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" role="img" aria-label="경기 타임라인">${bands}${ticks}${half}${axis}
      <text x="${L}" y="${mid - 58}" class="dim sm">${esc(team)}</text><text x="${L}" y="${mid + 64}" class="dim sm">${esc(r.opponent || '상대')}</text>${marks}</svg>
    <div class="lg"><span><i style="background:${US}"></i>리드 구간</span><span><i style="background:${THEM}"></i>열세 구간</span><span>● 득점(도움)</span><span>▲ 교체 <span style="color:var(--warn)">▲</span> GK 교체</span><span><span style="color:var(--warn)">▮</span> 경고</span></div></div>`;
}

/* ── 2. 팀 대조 — 버터플라이. 한 행 = 한 지표, 가운데 라벨, 왼쪽 우리(주황) / 오른쪽 상대(파랑). 값은 막대 끝에 직접 라벨(행 수 ≤ 10). */
export function butterfly(r, team, W = 560){
  const v = k => num(r[k]);
  const rows = [
    { label:'점유율 %', a: v('possession'), b: v('possession') == null ? null : 100 - v('possession'), max: 100, d: 0 },
    { label:'xG', a: v('xg_v'), b: v('xg_o'), d: 2, seg: { a: v('xg_op_v'), b: v('xg_op_o'), name: '오픈플레이' } },
    { label:'슈팅', a: v('shots_v'), b: v('shots_o'), d: 0, seg: { a: v('sot_v'), b: v('sot_o'), name: '유효' } },
    { label:'빅찬스', a: v('bigch_v'), b: v('bigch_o'), d: 0 },
    { label:'코너', a: v('corners_v'), b: v('corners_o'), d: 0 },
    { label:'패스', a: v('passes_v'), b: v('passes_o'), d: 0 },
    { label:'크로스 성공/시도', a: v('cross_acc_v'), b: null, d: 0, aTot: v('cross_att_v') },
    { label:'롱볼 성공/시도', a: v('long_acc_v'), b: v('long_acc_o'), d: 0, aTot: v('long_att_v'), bTot: v('long_att_o') },
    { label:'PPDA (낮을수록 강한 압박)', a: v('ppda_v'), b: v('ppda_o'), d: 2, invert: true },
    { label:'수비 액션 평균 위치', a: v('def_x_v'), b: v('def_x_o'), d: 1, max: 100 },
  ].filter(x => x.a != null || x.b != null);
  if (!rows.length) return '';
  const rowH = 28, top = 22, H = top + rows.length * rowH + 8, C = W / 2, span = Math.max(90, C - 60 - 64), bar = 13;   // 가운데 라벨 폭 120 + 값 라벨 여백
  const svgRows = rows.map((x, i) => {
    const y = top + i * rowH, m = x.max ?? Math.max(x.a ?? 0, x.b ?? 0, x.aTot ?? 0, x.bTot ?? 0, 1e-9);
    const wa = span * ((x.aTot ?? x.a ?? 0) / m), wb = span * ((x.bTot ?? x.b ?? 0) / m);
    const seg = (side, val, total, col) => { if (val == null || total == null) return ''; const w = span * (val / m);
      return side === 'a' ? `<rect x="${C - 60 - w}" y="${y + 2}" width="${Math.max(0, w)}" height="${bar}" rx="3" fill="${col}"/>`
                          : `<rect x="${C + 60}" y="${y + 2}" width="${Math.max(0, w)}" height="${bar}" rx="3" fill="${col}"/>`; };
    const la = x.a != null ? `${fmt(x.a, x.d)}${x.aTot != null ? `/${fmt(x.aTot)}` : ''}` : '—', lb = x.b != null ? `${fmt(x.b, x.d)}${x.bTot != null ? `/${fmt(x.bTot)}` : ''}` : '—';
    const tipA = `${team} ${x.label}: ${la}` + (x.seg?.a != null ? ` (${x.seg.name} ${fmt(x.seg.a, x.d)})` : ''), tipB = `${r.opponent || '상대'} ${x.label}: ${lb}` + (x.seg?.b != null ? ` (${x.seg.name} ${fmt(x.seg.b, x.d)})` : '');
    return `<g>
      <text x="${C}" y="${y + 12}" text-anchor="middle" class="dim sm">${esc(x.label)}</text>
      <g class="hit" data-tip="${esc(tipA)}"><rect x="${C - 60 - span}" y="${y}" width="${span}" height="${bar + 4}" fill="transparent"/>
        ${x.a != null ? `<rect x="${C - 60 - wa}" y="${y + 2}" width="${Math.max(0, wa)}" height="${bar}" rx="3" fill="${US}" opacity="${x.aTot != null ? .35 : 1}"/>` : ''}
        ${x.aTot != null ? seg('a', x.a, x.aTot, US) : ''}${x.seg?.a != null ? seg('a', x.seg.a, x.a, 'rgba(0,0,0,.35)') : ''}
        <text x="${C - 66 - Math.max(wa, 0) - 4}" y="${y + 12}" text-anchor="end" class="sm">${la}</text></g>
      <g class="hit" data-tip="${esc(tipB)}"><rect x="${C + 60}" y="${y}" width="${span}" height="${bar + 4}" fill="transparent"/>
        ${x.b != null ? `<rect x="${C + 60}" y="${y + 2}" width="${Math.max(0, wb)}" height="${bar}" rx="3" fill="${THEM}" opacity="${x.bTot != null ? .35 : 1}"/>` : ''}
        ${x.bTot != null ? seg('b', x.b, x.bTot, THEM) : ''}${x.seg?.b != null ? seg('b', x.seg.b, x.b, 'rgba(0,0,0,.35)') : ''}
        <text x="${C + 66 + Math.max(wb, 0) + 4}" y="${y + 12}" class="sm">${lb}</text></g></g>`;
  }).join('');
  return `<div class="vz"><h4>팀 대조 <span class="dim">— 왼쪽 ${esc(team)} · 오른쪽 ${esc(r.opponent || '상대')}. xG·슈팅의 어두운 안쪽 = 오픈플레이·유효슈팅</span></h4>
    <svg width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" role="img" aria-label="팀 스탯 대조"><line x1="${C}" x2="${C}" y1="${top - 6}" y2="${H - 6}" stroke="${GRID}"/>${svgRows}</svg>
    <div class="lg"><span><i style="background:${US}"></i>${esc(team)}</span><span><i style="background:${THEM}"></i>${esc(r.opponent || '상대')}</span><span><i style="background:${US};opacity:.35"></i>시도(연한) / 성공(진한)</span></div></div>`;
}

/* ── 3. 하프 비교 — 전·후반 xG(그룹 막대)와 점유(미터). 분리 표본이 없으면 그리지 않는다. */
export function halves(r, team, W = 560){
  const ps = r.periods || []; if (!ps.length) return '';
  const H = 200, gw = Math.min(220, Math.max(130, (W - 120) / ps.length - 50)), x0 = 70, base = 160;
  const m = Math.max(...ps.flatMap(p => [num(p.xg_v) || 0, num(p.xg_o) || 0]), 0.5);
  const bars = ps.map((p, i) => { const gx = x0 + i * (gw + 60); const h = v => 110 * ((num(v) || 0) / m);
    const a = h(p.xg_v), b = h(p.xg_o); const poss = num(p.possession_v);
    return `<g>
      <text x="${gx + 36}" y="16" text-anchor="middle" class="dim">${p.period === '1H' ? '전반' : p.period === '2H' ? '후반' : p.period}</text>
      <g class="hit" data-tip="${esc(`${team} 전반 xG ${fmt(p.xg_v, 2)} · 슈팅 ${fmt(p.shots_v)}${p.ppda_v != null ? ` · PPDA ${fmt(p.ppda_v, 2)}` : ''}`)}"><rect x="${gx}" y="${base - a}" width="22" height="${a}" rx="3" fill="${US}"/><text x="${gx + 11}" y="${base - a - 4}" text-anchor="middle" class="sm">${fmt(p.xg_v, 2)}</text></g>
      <g class="hit" data-tip="${esc(`${r.opponent || '상대'} xG ${fmt(p.xg_o, 2)} · 슈팅 ${fmt(p.shots_o)}`)}"><rect x="${gx + 26}" y="${base - b}" width="22" height="${b}" rx="3" fill="${THEM}"/><text x="${gx + 37}" y="${base - b - 4}" text-anchor="middle" class="sm">${fmt(p.xg_o, 2)}</text></g>
      ${poss != null ? `<g class="hit" data-tip="${esc(`점유 ${team} ${fmt(poss)}% · ${r.opponent || '상대'} ${fmt(100 - poss)}%`)}"><rect x="${gx + 60}" y="${base - 26}" width="${gw - 60}" height="8" rx="4" fill="${THEM}" opacity=".35"/><rect x="${gx + 60}" y="${base - 26}" width="${(gw - 60) * poss / 100}" height="8" rx="4" fill="${US}"/><text x="${gx + 60}" y="${base - 4}" class="sm">점유 ${fmt(poss)}%</text></g>` : ''}
    </g>`; }).join('');
  return `<div class="vz"><h4>하프 비교 <span class="dim">— xG(막대)와 점유(띠)</span></h4>
    <svg width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" role="img" aria-label="하프별 비교"><line x1="${x0 - 10}" x2="${W - 20}" y1="${base}" y2="${base}" stroke="var(--line)"/><text x="${x0 - 14}" y="${base + 4}" text-anchor="end" class="dim sm">xG</text>${bars}</svg>
    <div class="lg"><span><i style="background:${US}"></i>${esc(team)}</span><span><i style="background:${THEM}"></i>${esc(r.opponent || '상대')}</span></div></div>`;
}


/* ── 4. xG 레이스 — 누적 xG 계단선(두 팀 한 축) + 득점 표식 + HT선. 축구 분석 사이트의 표준 형식(Understat·FotMob).
   ⚠️ 한 경기 안에서는 한 제공사 xG만 쓴다(match_shots.provider) — 제공사 혼합 금지. */
export function xgRace(r, team, W = 760){
  const shots = (r.shots || []).filter(s => s.xg != null).sort((a, b) => a.minute - b.minute);
  if (!shots.length) return `<div class="vz"><h4>xG 레이스</h4><span class="dim" style="font-size:12px">${(r.shots || []).length ? '이 대회는 제공사가 슛별 xG를 주지 않는다(친선·일부 컵)' : '슛 데이터 미수집'}.</span></div>`;
  const prov = shots[0].provider; const H = Math.round(W * 0.42), L = 36, R = 44, T = 18, B = 26;   // 슛 맵(105:68)과 같은 행 — 높이를 폭에 비례시켜 짝을 맞춘다
  const end = Math.max(90, ...shots.map(s => s.minute)) + 1;
  const tot = { v: 0, o: 0 }; const pts = { v: [[0, 0]], o: [[0, 0]] }; const goals = [];
  for (const s of shots){ tot[s.side] += s.xg; pts[s.side].push([s.minute, tot[s.side]]); if (s.outcome === 'goal') goals.push({ ...s, cum: tot[s.side] }); }
  const maxY = Math.max(tot.v, tot.o, 0.5) * 1.12;
  const x = m => L + (W - L - R) * (m / end), y = v => T + (H - T - B) * (1 - v / maxY);
  const step = (arr, col) => { let d = `M${x(0)},${y(0)}`; let py = 0;
    for (const [m, v] of arr.slice(1)){ d += ` H${x(m)} V${y(v)}`; py = v; } d += ` H${x(end)}`;
    return `<path d="${d}" fill="none" stroke="${col}" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/>`; };
  const ticks = [0, 15, 30, 45, 60, 75, 90].filter(t => t <= end).map(t => `<text x="${x(t)}" y="${H - 8}" text-anchor="middle" class="dim sm">${t}′</text>`).join('');
  const ys = [0, maxY / 2, maxY].map(v => `<line x1="${L}" x2="${W - R}" y1="${y(v)}" y2="${y(v)}" stroke="${GRID}"/><text x="${L - 6}" y="${y(v) + 3.5}" text-anchor="end" class="dim sm">${v.toFixed(1)}</text>`).join('');
  const gm = goals.map(g => { const col = g.side === 'v' ? US : THEM;
    return `<g class="hit" data-tip="${esc(`${g.minute}′ ${g.side === 'v' ? team : (r.opponent || '상대')} 득점 · ${g.player_name || ''} · 슛 xG ${fmt(g.xg, 2)} · 누적 ${fmt(g.cum, 2)}`)}">
      <circle cx="${x(g.minute)}" cy="${y(g.cum)}" r="7" fill="${SURF}"/><circle cx="${x(g.minute)}" cy="${y(g.cum)}" r="5" fill="${col}"/></g>`; }).join('');
  const endLab = (side, col) => `<text x="${W - R + 6}" y="${y(tot[side]) + 3.5}" class="sm"><tspan font-weight="700">${fmt(tot[side], 2)}</tspan></text>`;
  return `<div class="vz"><h4>xG 레이스 <span class="dim">— 누적 기대득점 · 점 = 득점 · ${esc(prov)} 모델</span></h4>
    <svg width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" role="img" aria-label="누적 xG">${ys}
      <line x1="${x(45)}" x2="${x(45)}" y1="${T}" y2="${H - B}" stroke="var(--line)"/><text x="${x(45)}" y="${T - 4}" text-anchor="middle" class="dim sm">HT</text>
      ${step(pts.o, THEM)}${step(pts.v, US)}${gm}${endLab('v', US)}${endLab('o', THEM)}${ticks}
      <rect class="xhair" x="${L}" y="${T}" width="${W - L - R}" height="${H - T - B}" fill="transparent" data-l="${L}" data-w="${W - L - R}" data-end="${end}"/></svg>
    <div class="lg"><span><i style="background:${US}"></i>${esc(team)} ${fmt(tot.v, 2)}</span><span><i style="background:${THEM}"></i>${esc(r.opponent || '상대')} ${fmt(tot.o, 2)}</span></div></div>`;
}

/* ── 5. 슛 맵 — 한 피치, 두 팀이 반대 골문을 공격(우리 → 오른쪽). 점 넓이 ∝ xG, 채움 = 득점, 테두리만 = 그 외. */
export function shotMap(r, team, W = 760){
  const shots = (r.shots || []); if (!shots.length) return '';
  const PW = 105, PH = 68, pad = 14, sc = (W - pad * 2) / PW, H = PH * sc + pad * 2 + 6;
  const X = v => pad + v * sc, Y = v => pad + v * sc;
  // 제공사 좌표 → 피치(m). SofaScore: x = 공격 골라인까지 거리(%), y = 폭(%) · FotMob: x 0~105(공격 방향), y 0~68
  const toPitch = s => { let px, py;
    if (s.provider === 'FotMob'){ px = s.x; py = s.y; } else { px = PW - (s.x ?? 50) / 100 * PW; py = (s.y ?? 50) / 100 * PH; }
    if (s.side === 'o'){ px = PW - px; py = PH - py; } return [px, py]; };
  const pitch = `<rect x="${X(0)}" y="${Y(0)}" width="${PW * sc}" height="${PH * sc}" fill="none" stroke="var(--line)"/>
    <line x1="${X(PW / 2)}" x2="${X(PW / 2)}" y1="${Y(0)}" y2="${Y(PH)}" stroke="var(--line)"/><circle cx="${X(PW / 2)}" cy="${Y(PH / 2)}" r="${9.15 * sc}" fill="none" stroke="var(--line)"/>
    ${[0, PW - 16.5].map(bx => `<rect x="${X(bx)}" y="${Y(PH / 2 - 20.16)}" width="${16.5 * sc}" height="${40.32 * sc}" fill="none" stroke="var(--line)"/>`).join('')}
    ${[0, PW - 5.5].map(bx => `<rect x="${X(bx)}" y="${Y(PH / 2 - 9.16)}" width="${5.5 * sc}" height="${18.32 * sc}" fill="none" stroke="var(--line)"/>`).join('')}`;
  const dots = shots.slice().sort((a, b) => (b.xg ?? 0) - (a.xg ?? 0)).map(s => { const [px, py] = toPitch(s); const col = s.side === 'v' ? US : THEM;
    const rr = s.xg == null ? 4 : 3 + 9 * Math.sqrt(s.xg); const goal = s.outcome === 'goal';
    const tip = `${s.minute}′ ${s.side === 'v' ? team : (r.opponent || '상대')} · ${s.player_name || ''} · ${{ goal:'득점', save:'선방', miss:'빗나감', block:'블록', post:'골대' }[s.outcome] || s.outcome}${s.xg != null ? ` · xG ${fmt(s.xg, 2)}` : ''}${s.situation ? ` · ${s.situation}` : ''}`;
    return `<g class="hit" data-tip="${esc(tip)}"><circle cx="${X(px)}" cy="${Y(py)}" r="${rr + 6}" fill="transparent"/>
      ${goal ? `<circle cx="${X(px)}" cy="${Y(py)}" r="${rr + 2}" fill="${SURF}"/><circle cx="${X(px)}" cy="${Y(py)}" r="${rr}" fill="${col}"/>`
             : `<circle cx="${X(px)}" cy="${Y(py)}" r="${rr}" fill="${col}" fill-opacity=".14" stroke="${col}" stroke-width="1.5"/>`}</g>`; }).join('');
  const n = side => shots.filter(s => s.side === side).length, g = side => shots.filter(s => s.side === side && s.outcome === 'goal').length;
  return `<div class="vz"><h4>슛 맵 <span class="dim">— ${esc(team)} → 오른쪽 골문 · ${esc(r.opponent || '상대')} → 왼쪽 · 점 크기 = xG · 채움 = 득점</span></h4>
    <svg width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" role="img" aria-label="슛 맵">${pitch}${dots}
      <text x="${X(PW) - 4}" y="${Y(PH) + 12}" text-anchor="end" class="dim sm">${esc(team)} 슛 ${n('v')} · 득점 ${g('v')}</text>
      <text x="${X(0) + 4}" y="${Y(PH) + 12}" class="dim sm">${esc(r.opponent || '상대')} 슛 ${n('o')} · 득점 ${g('o')}</text></svg></div>`;
}


/* ── 6. 선수 평점·출전 구간 (2026-09-18, 사용자 지시 「모든 메뉴의 텍스트를 시각적으로」의 마지막 항목).
   왼쪽 = 출전 구간 간트(선발은 0′부터, 교체는 투입 분부터 — 교체 이벤트로 구간을 만든다),
   오른쪽 = 평점 막대(축 5.5~10, 색은 사이트 공통 품질 어휘). 접점(hit_points)은 막대 끝에 숫자로 병기한다.
   ⛔ 평점과 분을 같은 축에 겹치지 않는다 — 구간은 시간축, 평점은 평점축으로 나란히 둔다. */
export function playerRows(r, team, W = 900){
  const ps = (r.players || []).slice();
  if (!ps.length) return '';
  const subs = (r.events || []).filter(e => e.kind === 'sub' || e.kind === 'gk_change');
  const inAt = {}, outAt = {};
  for (const e of subs){
    if (e.player_id != null) inAt[e.player_id] = e.minute; else if (e.player_name) inAt['n:' + e.player_name] = e.minute;
    if (e.player_out_id != null) outAt[e.player_out_id] = e.minute; else if (e.player_out_name) outAt['n:' + e.player_out_name] = e.minute;
  }
  const key = p => (p.player_id != null ? p.player_id : 'n:' + p.label);
  const end = Math.max(90, ...(r.events || []).map(e => e.minute));
  const rows = ps.map(p => { const k = key(p);
    const start = p.started ? 0 : (inAt[k] ?? (end - (p.minutes ?? 0)));
    const stop = outAt[k] ?? (p.started && p.minutes != null && p.minutes < end ? start + p.minutes : end);
    return { ...p, start: Math.max(0, start), stop: Math.min(end, Math.max(start, stop)) }; })
    .sort((a, b) => (b.started || 0) - (a.started || 0) || (b.rating ?? 0) - (a.rating ?? 0));
  const L = 118, GAP = 26, T = 30, rowH = 22, H = T + rows.length * rowH + 14;
  const ganttW = Math.round((W - L - GAP) * 0.52), ratW = W - L - GAP - ganttW;
  const gx = m => L + ganttW * (m / end);
  const rx0 = L + ganttW + GAP, lo = 5.5, hi = 10;
  const rx = v => rx0 + (ratW - 44) * ((Math.min(hi, Math.max(lo, v)) - lo) / (hi - lo));
  const col = v => v == null ? 'rgba(255,255,255,.25)' : v >= 7.5 ? 'var(--ok)' : v >= 6.5 ? 'var(--warn)' : 'var(--bad)';
  const ticks = [0, 15, 30, 45, 60, 75, 90].filter(t => t <= end).map(t =>
    `<line x1="${gx(t)}" x2="${gx(t)}" y1="${T - 8}" y2="${H - 8}" stroke="${GRID}"/><text x="${gx(t)}" y="${T - 12}" text-anchor="middle" font-size="10" fill="var(--dim)">${t}′</text>`).join('');
  const rticks = [6, 7, 8, 9].map(v =>
    `<line x1="${rx(v)}" x2="${rx(v)}" y1="${T - 8}" y2="${H - 8}" stroke="${GRID}"/><text x="${rx(v)}" y="${T - 12}" text-anchor="middle" font-size="10" fill="var(--dim)">${v}</text>`).join('');
  const body = rows.map((p, i) => { const y = T + i * rowH + 13;
    const tip = `${p.position ?? ''} ${p.label} · ${p.started ? '선발' : '교체'} · ${p.start}′~${p.stop}′(${p.minutes ?? '—'}분) · 평점 ${p.rating ?? '—'} · 접점 ${p.hit_points ?? '—'}`;
    return `<g class="hit" data-tip="${esc(tip)}" data-pid="${p.player_id ?? ''}" style="cursor:pointer">
      <text x="${L - 8}" y="${y + 4}" text-anchor="end" font-size="11" fill="var(--txt)">${esc(p.label)}</text>
      <text x="6" y="${y + 4}" font-size="9.5" fill="${p.started ? 'var(--acc)' : 'var(--dim)'}">${p.started ? '선발' : '교체'}</text>
      <text x="36" y="${y + 4}" font-size="9.5" fill="var(--dim)">${esc(p.position ?? '')}</text>
      <rect x="${gx(p.start)}" y="${y - 6}" width="${Math.max(2, gx(p.stop) - gx(p.start))}" height="12" rx="3" fill="${US}" fill-opacity="${p.started ? .8 : .45}"/>
      <text x="${gx(p.stop) + 5}" y="${y + 4}" font-size="9.5" fill="var(--dim)">${p.minutes ?? '—'}′</text>
      ${p.rating != null ? `<rect x="${rx0}" y="${y - 6}" width="${Math.max(2, rx(p.rating) - rx0)}" height="12" rx="3" fill="${col(p.rating)}" fill-opacity=".85"/>
        <text x="${rx(p.rating) + 6}" y="${y + 4}" font-size="10.5" font-weight="700" fill="var(--txt)">${p.rating}</text>
        <text x="${W - 6}" y="${y + 4}" text-anchor="end" font-size="9.5" fill="var(--dim)">접점 ${p.hit_points ?? '—'}</text>`
        : `<text x="${rx0}" y="${y + 4}" font-size="10" fill="var(--dim)">평점 미수집</text>`}</g>`; }).join('');
  return `<div class="vz wide"><h4>선수별 출전 구간·평점 <span class="dim">— 왼쪽: 언제 뛰었나 · 오른쪽: 평점(6.5 평범 · 7.5 상위) · 이름을 누르면 아래 상세가 열린다</span></h4>
    <svg width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" role="img" aria-label="선수별 출전 구간과 평점">
      <text x="${L}" y="${T - 12}" font-size="10" fill="var(--dim)">출전 구간</text>
      <text x="${rx0}" y="${T - 12}" font-size="10" fill="var(--dim)">평점</text>${ticks}${rticks}${body}</svg>
    <div class="lg"><span><i style="background:${US}"></i>선발 구간</span><span><i style="background:${US};opacity:.45"></i>교체 구간</span>
      <span><i style="background:var(--ok)"></i>7.5+</span><span><i style="background:var(--warn)"></i>6.5~7.5</span><span><i style="background:var(--bad)"></i>6.5 미만</span></div></div>`;
}

/* 컨테이너 렌더 + 호버 툴팁(마크가 히트 타깃, 값은 라벨·표로도 읽힌다).
   ⭐ SVG는 컨테이너 픽셀 폭으로 그린다(viewBox 확대 금지 — 넓은 화면에서 글자·점이 비대해진다). 창 크기가 바뀌면 다시 그린다. */
export function renderMatchViz(el, r, team){
  el.className = 'mviz';
  el.innerHTML = '<div class="vz wide" data-k="t"></div><div class="vz" data-k="x"></div><div class="vz" data-k="s"></div><div class="vz" data-k="b"></div><div class="vz" data-k="h"></div><div class="tip" hidden></div>';
  const tip = el.querySelector('.tip');
  const draw = () => {
    for (const box of el.querySelectorAll('.vz')){
      const w = Math.max(320, Math.floor(box.clientWidth - 26));      // 패널 패딩 12×2 + 테두리
      const k = box.dataset.k;
      const html = k === 't' ? timeline(r, team, Math.min(w, 1240)) : k === 'x' ? xgRace(r, team, Math.min(w, 720)) : k === 's' ? shotMap(r, team, Math.min(w, 720)) : k === 'b' ? butterfly(r, team, Math.min(w, 720)) : halves(r, team, Math.min(w, 720));
      // 각 함수는 <div class="vz …">…</div> 래퍼를 돌려준다 → 안쪽만 옮긴다
      const tmp = document.createElement('div'); tmp.innerHTML = html;
      const inner = tmp.firstElementChild;
      box.innerHTML = inner ? inner.innerHTML : ''; box.hidden = !inner;
    }
    el.querySelectorAll('.xhair').forEach(rc => {
      const shots = (r.shots || []).filter(s => s.xg != null).sort((a, b) => a.minute - b.minute);
      rc.addEventListener('pointermove', e => {
        const b = rc.getBoundingClientRect(); const m = Math.round(Math.max(0, Math.min(1, (e.clientX - b.left) / b.width)) * Number(rc.dataset.end));
        const cum = { v: 0, o: 0 }; for (const s of shots) if (s.minute <= m) cum[s.side] += s.xg;
        tip.textContent = `${m}′ · ${team} ${cum.v.toFixed(2)} · ${r.opponent || '상대'} ${cum.o.toFixed(2)}`; tip.hidden = false;
        tip.style.left = Math.min(e.clientX + 12, window.innerWidth - 300) + 'px'; tip.style.top = (e.clientY + 14) + 'px'; });
      rc.addEventListener('pointerleave', () => { tip.hidden = true; });
    });
    el.querySelectorAll('.hit').forEach(g => {
      g.addEventListener('pointerenter', () => { tip.textContent = g.dataset.tip; tip.hidden = false; });
      g.addEventListener('pointermove', e => { tip.style.left = Math.min(e.clientX + 12, window.innerWidth - 300) + 'px'; tip.style.top = (e.clientY + 14) + 'px'; });
      g.addEventListener('pointerleave', () => { tip.hidden = true; });
    });
  };
  draw();
  if (el._ro) el._ro.disconnect();
  let t = null; el._ro = new ResizeObserver(() => { clearTimeout(t); t = setTimeout(draw, 120); }); el._ro.observe(el);
}
