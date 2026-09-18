/* 스쿼드 시각화 — 베스트 XI 피치 · 슬롯 깊이(경쟁) 스트립 (2026-09-18, 사용자 지시 「스쿼드 화면 시각화도 이어서」).
   dataviz 규약: 크기 비교는 **단일 색 램프**(정체성이 아니라 크기라서 categorical을 쓰지 않는다) · 값 라벨은 선택적 ·
   한 그림에 한 축(⛔ 적합과 평점을 같은 축에 섞지 않는다 — GK는 별도 카드) · 표 뷰(아래 기존 표)는 남긴다. */
const esc = s => String(s ?? '').replace(/[&<>"]/g, c => ({ '&':'&amp;', '<':'&lt;', '>':'&gt;', '"':'&quot;' }[c]));
const US = 'var(--viz-us)', SURF = 'var(--panel)', GRID = 'var(--viz-grid)';
/* 단일 색 램프(파랑) — 어두울수록 낮고 밝을수록 높다. 크기 전용이라 팀색(주황)과 섞지 않는다. */
const RAMP = ['#16324f', '#1d4a74', '#256199', '#2e79bf', '#3987e5'];
const rampOf = t => RAMP[Math.max(0, Math.min(RAMP.length - 1, Math.round(t * (RAMP.length - 1))))];

/* ── 1. 베스트 XI 피치 — 슬롯 좌표에 1순위(또는 처방 선발)를 놓는다. 색 = 그 슬롯의 적합 강도, 부제 = 역할/포커스. */
export function pitchXI(rows, { W = 560, lo = 0.6, hi = 1 } = {}){
  const H = Math.round(W * 1.42), pad = 10;
  const X = px => pad + (W - pad * 2) * (px / 100), Y = py => H - pad - (H - pad * 2) * (py / 100);
  const line = (a) => `<path d="${a}" fill="none" stroke="var(--line)"/>`;
  const pitch = `<rect x="${X(0)}" y="${Y(100)}" width="${X(100) - X(0)}" height="${Y(0) - Y(100)}" rx="6" fill="rgba(255,255,255,.015)" stroke="var(--line)"/>
    ${line(`M${X(0)},${Y(50)} H${X(100)}`)}<circle cx="${X(50)}" cy="${Y(50)}" r="${(X(100) - X(0)) * 0.13}" fill="none" stroke="var(--line)"/>
    ${line(`M${X(21)},${Y(0)} V${Y(17)} H${X(79)} V${Y(0)}`)}${line(`M${X(37)},${Y(0)} V${Y(6)} H${X(63)} V${Y(0)}`)}
    ${line(`M${X(21)},${Y(100)} V${Y(83)} H${X(79)} V${Y(100)}`)}${line(`M${X(37)},${Y(100)} V${Y(94)} H${X(63)} V${Y(100)}`)}`;
  const chips = rows.map(r => { const t = r.isGk ? null : (r.top?.sim == null ? null : (r.top.sim - lo) / (hi - lo));
    const col = t == null ? 'rgba(255,255,255,.18)' : rampOf(t);
    const cw = Math.max(76, Math.min(104, (W - 40) / 5)), ch = 46;
    const cx = X(r.x) - cw / 2, cy = Y(r.y) - ch / 2;
    const name = r.top?.label ?? '공백';
    const sub = r.isGk ? (r.top?.rating != null ? `평점 ${r.top.rating}` : '적합 무변별')
                       : (r.top?.sim != null ? `${r.top.roleName ?? ''} ${r.top.sim.toFixed(3)}` : '실측 없음');
    const tip = `${r.pos} · ${name}${r.top?.shirt != null ? ` (${r.top.shirt}번)` : ''}` +
      (r.isGk ? ` · 평점 ${r.top?.rating ?? '—'} · GK는 커널 적합이 변별하지 못한다` : ` · ${r.top?.roleName ?? ''}/${r.top?.focus ?? ''} 적합 ${r.top?.sim?.toFixed(3) ?? '—'}`) +
      ` · 후보 ${r.cands.length}명${r.gap != null ? ` · 2순위와 격차 ${r.gap.toFixed(3)}` : ''}`;
    return `<g class="hit" data-tip="${esc(tip)}">
      <rect x="${cx}" y="${cy}" width="${cw}" height="${ch}" rx="7" fill="${SURF}" stroke="${col}" stroke-width="2"/>
      <rect x="${cx}" y="${cy}" width="${cw}" height="4" rx="2" fill="${col}"/>
      <text x="${cx + cw / 2}" y="${cy + 19}" text-anchor="middle" font-size="10" fill="var(--dim)">${esc(r.pos)}</text>
      <text x="${cx + cw / 2}" y="${cy + 31}" text-anchor="middle" font-size="11.5" font-weight="700" fill="var(--txt)">${esc(name)}</text>
      <text x="${cx + cw / 2}" y="${cy + 42}" text-anchor="middle" font-size="9.5" fill="var(--dim)">${esc(sub)}</text></g>`; }).join('');
  const legend = RAMP.map((c, i) => `<span><i style="background:${c}"></i>${i === 0 ? `약 ${lo.toFixed(2)}` : i === RAMP.length - 1 ? `강 ${hi.toFixed(2)}` : ''}</span>`).join('');
  return `<svg width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" role="img" aria-label="베스트 XI 피치">${pitch}${chips}</svg>
    <div class="lg">${legend}<span class="dim">색 = 슬롯 1순위의 커널 적합</span></div>`;
}

/* ── 2. 슬롯 깊이·경쟁 — 행 = 슬롯, 점 = 후보. x = 적합(또는 GK 카드에서는 평점). 1순위는 채운 점 + 이름,
   1~2순위 격차가 작으면(≤.05) 「경합」으로 표시한다(실측 무결정 구간과 같은 눈금). */
export function depthStrip(rows, { W = 720, key = 'sim', lo = 0.6, hi = 1, label = '커널 적합', tie = 0.05 } = {}){
  if (!rows.length) return '';
  const rowH = 30, L = 74, R = 118, T = 26, H = T + rows.length * rowH + 10;
  const x = v => L + (W - L - R) * ((v - lo) / (hi - lo));
  const ticks = []; const stepT = (hi - lo) > 1 ? 0.5 : 0.1;
  for (let v = lo; v <= hi + 1e-9; v += stepT) ticks.push(Math.round(v * 100) / 100);
  const grid = ticks.map(v => `<line x1="${x(v)}" x2="${x(v)}" y1="${T - 8}" y2="${H - 6}" stroke="${GRID}"/>
    <text x="${x(v)}" y="${T - 12}" text-anchor="middle" font-size="10" fill="var(--dim)">${v}</text>`).join('');
  const body = rows.map((r, i) => { const y = T + i * rowH + 15;
    const vals = r.cands.map(c => c[key]).filter(v => v != null);
    if (!vals.length) return `<g><text x="${L - 8}" y="${y + 4}" text-anchor="end" font-size="11" fill="var(--dim)">${esc(r.pos)}</text>
      <text x="${L + 6}" y="${y + 4}" font-size="11" fill="var(--dim)">실측 후보 없음 — 공백 슬롯</text></g>`;
    const top = r.cands.find(c => c[key] === Math.max(...vals));
    const spread = `<line x1="${x(Math.min(...vals))}" x2="${x(Math.max(...vals))}" y1="${y}" y2="${y}" stroke="rgba(255,255,255,.14)" stroke-width="2"/>`;
    const dots = r.cands.filter(c => c[key] != null).sort((a, b) => a[key] - b[key]).map(c => {
      const isTop = c === top, cx = x(c[key]);
      const tip = `${r.pos} · ${c.label}${c.shirt != null ? ` (${c.shirt}번)` : ''} · ${label} ${c[key].toFixed(key === 'sim' ? 3 : 2)}${c.roleName ? ` · ${c.roleName}/${c.focus}` : ''}${c.starter ? ' · 처방 선발' : ''}`;
      return `<g class="hit" data-tip="${esc(tip)}"><circle cx="${cx}" cy="${y}" r="9" fill="transparent"/>
        <circle cx="${cx}" cy="${y}" r="${isTop ? 6.5 : 5}" fill="${SURF}"/>
        <circle cx="${cx}" cy="${y}" r="${isTop ? 5 : 3.5}" fill="${isTop ? US : 'rgba(255,255,255,.34)'}"/>
        ${c.starter ? `<circle cx="${cx}" cy="${y}" r="8.5" fill="none" stroke="${US}" stroke-opacity=".55"/>` : ''}</g>`; }).join('');
    const gap = vals.length > 1 ? Math.max(...vals) - vals.slice().sort((a, b) => b - a)[1] : null;
    const tight = gap != null && gap <= tie;
    return `<g><text x="${L - 8}" y="${y + 4}" text-anchor="end" font-size="11" font-weight="600" fill="var(--txt)">${esc(r.pos)}</text>
      ${spread}${dots}
      <text x="${x(Math.max(...vals)) + 12}" y="${y + 4}" font-size="11" fill="var(--txt)">${esc(top.label)}</text>
      <text x="${W - 8}" y="${y + 4}" text-anchor="end" font-size="10" fill="${tight ? 'var(--warn)' : 'var(--dim)'}">${r.cands.length}명${gap != null ? ` · Δ${gap.toFixed(key === 'sim' ? 3 : 2)}${tight ? ' 경합' : ''}` : ''}</text></g>`; }).join('');
  return `<svg width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" role="img" aria-label="슬롯별 후보 ${label} 분포">
      <text x="${L - 8}" y="${T - 12}" text-anchor="end" font-size="10" fill="var(--dim)">${esc(label)}</text>${grid}${body}</svg>
    <div class="lg"><span><i style="background:${US}"></i>슬롯 1순위</span><span><i style="background:rgba(255,255,255,.34)"></i>그 밖 후보</span>
      <span class="dim">◎ = 게임 처방 선발 · Δ = 1~2순위 격차(${tie} 이하면 경합)</span></div>`;
}

/* 호버 툴팁 — 마크가 히트 타깃. 값은 라벨·표로도 읽힌다. */
export function mountTips(el){
  let tip = el.querySelector('.tip');
  if (!tip){ tip = document.createElement('div'); tip.className = 'tip'; tip.hidden = true; el.appendChild(tip); }
  el.querySelectorAll('.hit').forEach(g => {
    g.addEventListener('pointerenter', () => { tip.textContent = g.dataset.tip; tip.hidden = false; });
    g.addEventListener('pointermove', e => { tip.style.left = Math.min(e.clientX + 12, window.innerWidth - 300) + 'px'; tip.style.top = (e.clientY + 14) + 'px'; });
    g.addEventListener('pointerleave', () => { tip.hidden = true; });
  });
}
