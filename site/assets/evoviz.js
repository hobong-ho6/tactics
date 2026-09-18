/* 진화 메뉴 시각화 — 마감 타임라인 · 6스탯 전후 덤벨 · 슬롯 준비도 (2026-09-18, 사용자 지시 「진화 메뉴 시각화도 이어서」).
   dataviz 규약: 크기·기간은 단일 색(정체성 아님) · 상태(강/중/약, 급함)는 사이트 공통 품질 색 · 값 라벨 병기(색만으로 읽히지 않게) ·
   한 그림에 한 축 · 표·카드(기존)는 그대로 남긴다. */
const esc = s => String(s ?? '').replace(/[&<>"]/g, c => ({ '&':'&amp;', '<':'&lt;', '>':'&gt;', '"':'&quot;' }[c]));
const US = 'var(--viz-us)', SURF = 'var(--panel)', GRID = 'var(--viz-grid)';
const QUAL = ['#ff6b6b', '#ffa06b', '#ffd54d', '#9fdb6a', '#4cd97b'];   // 약 → 강(사이트 평점·백분위와 같은 어휘)
const fmtD = t => String(t ?? '').slice(0, 10);

/* ── 1. 마감 타임라인 — 진화는 기간제라 「언제까지」가 1차 정보다. 막대 = 오늘 → 마감, D-7 이하는 경고색. */
export function deadlineChart(catalog, { W = 720, consumed = {} } = {}){
  const now = Date.now();
  const rows = (catalog || []).map(c => ({ c, end: new Date(c.end_submission_time || c.end_time || 0).getTime() }))
    .filter(r => r.end > 0).sort((a, b) => a.end - b.end);
  if (!rows.length) return '';
  /* ⚠️ 축 상한은 90일로 자른다 — 1년짜리 상시 진화(D-360+)가 섞여 있어 그대로 그리면 단기 진화가 전부 왼쪽 끝에 뭉친다.
     넘는 것은 막대 끝에 ▸를 붙이고 실제 D-값을 적는다(값을 숨기지 않는다). */
  const CAP = 90;
  const maxD = Math.min(CAP, Math.max(7, Math.ceil((rows[rows.length - 1].end - now) / 864e5)));
  const L = 168, R = 66, T = 24, rowH = 24, H = T + rows.length * rowH + 10;
  const x = d => L + (W - L - R) * (Math.min(maxD, Math.max(0, d)) / maxD);
  const ticks = []; const step = maxD > 60 ? 30 : maxD > 28 ? 14 : 7;
  for (let d = 0; d <= maxD; d += step) ticks.push(d);
  const grid = ticks.map(d => `<line x1="${x(d)}" x2="${x(d)}" y1="${T - 8}" y2="${H - 6}" stroke="${GRID}"/>
    <text x="${x(d)}" y="${T - 12}" text-anchor="middle" font-size="10" fill="var(--dim)">${d === 0 ? '오늘' : `D+${d}`}</text>`).join('');
  const body = rows.map((r, i) => { const y = T + i * rowH + 14, d = Math.ceil((r.end - now) / 864e5);
    const used = consumed[r.c.evo_id]; const urgent = d <= 7;
    const col = used?.exhausted ? 'rgba(255,255,255,.18)' : urgent ? 'var(--bad)' : d <= 30 ? 'var(--warn)' : US;
    const tip = `${r.c.name} · 마감 ${fmtD(r.c.end_submission_time || r.c.end_time)} (D-${d})` +
      `${r.c.repeatability > 1 ? ` · 반복 ${r.c.repeatability}회` : ' · 1회성'}${used ? ` · ${used.exhausted ? '소진' : `사용 ${used.count}`}` : ''}` +
      `${r.c.unlock_text ? ` · ${r.c.unlock_text}` : ''}`;
    return `<g class="hit" data-tip="${esc(tip)}">
      <text x="${L - 8}" y="${y + 4}" text-anchor="end" font-size="11" fill="${used?.exhausted ? 'var(--dim)' : 'var(--txt)'}">${esc(r.c.name.replace(/\s*\[[^\]]*\]\s*$/, ''))}</text>
      <rect x="${L}" y="${y - 6}" width="${Math.max(3, x(d) - L)}" height="12" rx="3" fill="${col}" fill-opacity="${used?.exhausted ? .3 : .85}"/>
      ${d > maxD ? `<path d="M${x(d) + 3},${y - 5} L${x(d) + 9},${y} L${x(d) + 3},${y + 5} Z" fill="${col}" fill-opacity=".6"/>` : ''}
      <text x="${x(d) + (d > maxD ? 14 : 6)}" y="${y + 4}" font-size="10" fill="${urgent ? 'var(--bad)' : 'var(--dim)'}">D-${d}</text></g>`; }).join('');
  return `<svg width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" role="img" aria-label="진화 마감 타임라인">${grid}${body}</svg>
    <div class="lg"><span><i style="background:${US}"></i>여유</span><span><i style="background:var(--warn)"></i>한 달 이내</span>
      <span><i style="background:var(--bad)"></i>일주일 이내</span><span><i style="background:rgba(255,255,255,.18)"></i>소진</span>
      <span class="dim">막대 길이 = 남은 기간(축 상한 ${maxD}일 · ▸는 그보다 먼 상시 진화)</span></div>`;
}

/* ── 2. 6스탯 전후 덤벨 — 경로 하나의 「적용 전 → 완주 후」. 점 크기 차이가 아니라 위치로 읽는다. */
export function sixDumbbell(before, after, { W = 420, gk = false } = {}){
  const K = gk ? ['DIV','HAN','KIC','REF','SPD','POS'] : ['PAC','SHO','PAS','DRI','DEF','PHY'];
  const pairs = K.map(k => ({ k, a: before?.[k], b: after?.[k] })).filter(p => p.a != null || p.b != null);
  if (!pairs.length) return '';
  const vals = pairs.flatMap(p => [p.a, p.b]).filter(v => v != null);
  const lo = Math.max(0, Math.min(...vals) - 6), hi = Math.min(99, Math.max(...vals) + 6);
  const L = 42, R = 52, T = 8, rowH = 22, H = T + pairs.length * rowH + 6;
  const x = v => L + (W - L - R) * ((v - lo) / Math.max(1, hi - lo));
  const body = pairs.map((p, i) => { const y = T + i * rowH + 12, d = (p.b ?? 0) - (p.a ?? 0);
    const line = p.a != null && p.b != null ? `<line x1="${x(p.a)}" x2="${x(p.b)}" y1="${y}" y2="${y}" stroke="${d > 0 ? 'var(--ok)' : 'rgba(255,255,255,.2)'}" stroke-width="3"/>` : '';
    return `<g class="hit" data-tip="${esc(`${p.k} ${p.a ?? '—'} → ${p.b ?? '—'}${d ? ` (${d > 0 ? '+' : ''}${d})` : ' 변화 없음'}`)}">
      <text x="${L - 8}" y="${y + 4}" text-anchor="end" font-size="10.5" fill="var(--dim)">${p.k}</text>${line}
      ${p.a != null ? `<circle cx="${x(p.a)}" cy="${y}" r="4.5" fill="${SURF}"/><circle cx="${x(p.a)}" cy="${y}" r="3" fill="rgba(255,255,255,.4)"/>` : ''}
      ${p.b != null ? `<circle cx="${x(p.b)}" cy="${y}" r="6" fill="${SURF}"/><circle cx="${x(p.b)}" cy="${y}" r="4.5" fill="${d > 0 ? 'var(--ok)' : US}"/>` : ''}
      <text x="${W - 8}" y="${y + 4}" text-anchor="end" font-size="10.5" fill="var(--txt)">${p.b ?? '—'}${d ? `<tspan fill="${d > 0 ? 'var(--ok)' : 'var(--bad)'}" font-size="9.5"> ${d > 0 ? '+' : ''}${d}</tspan>` : ''}</text></g>`; }).join('');
  return `<svg width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" role="img" aria-label="6스탯 적용 전후">${body}</svg>`;
}

/* ── 3. 슬롯 준비도 — 전술 구현 탭 요약. 슬롯마다 한 칸: 카드가 이미 처방 역할 Role++ / 진화로 도달 / 불가. */
export function readiness(rows, { W = 720 } = {}){
  if (!rows.length) return '';
  const STATE = [
    { k: 2, label: '카드가 이미 처방 역할', col: QUAL[4] },
    { k: 1, label: '진화로 도달 가능', col: QUAL[2] },
    { k: 0, label: '도달 못 함 — 대안 검토', col: QUAL[0] },
  ];
  const cell = 26, gap = 4, perRow = Math.max(6, Math.floor((W - 8) / (cell + gap)));
  const H = Math.ceil(rows.length / perRow) * (cell + gap) + 26;
  const cells = rows.map((r, i) => { const cx = (i % perRow) * (cell + gap), cy = Math.floor(i / perRow) * (cell + gap) + 16;
    const st = STATE.find(s => s.k === r.reach) ?? STATE[2];
    const tip = `${r.pos} · ${r.name ?? '처방 없음'} — ${st.label}${r.price != null ? ` · 시세 ${Number(r.price).toLocaleString()} 코인` : ' · 시세 미형성'}`;
    return `<g class="hit" data-tip="${esc(tip)}"><rect x="${cx}" y="${cy}" width="${cell}" height="${cell}" rx="5" fill="${st.col}" fill-opacity=".85"/>
      <text x="${cx + cell / 2}" y="${cy + cell / 2 + 3.5}" text-anchor="middle" font-size="9.5" font-weight="700" fill="#14100b">${esc(r.pos)}</text></g>`; }).join('');
  const n = k => rows.filter(r => r.reach === k).length;
  return `<svg width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" role="img" aria-label="슬롯 준비도">
      <text x="0" y="10" font-size="10.5" fill="var(--dim)">슬롯 ${rows.length}칸 — 색이 곧 상태다(칸 안은 슬롯 이름)</text>${cells}</svg>
    <div class="lg">${STATE.map(s => `<span><i style="background:${s.col}"></i>${s.label} ${n(s.k)}</span>`).join('')}</div>`;
}

export function mountTips(el){
  let tip = el.querySelector('.tip');
  if (!tip){ tip = document.createElement('div'); tip.className = 'tip'; tip.hidden = true; el.appendChild(tip); }
  el.querySelectorAll('.hit').forEach(g => {
    g.addEventListener('pointerenter', () => { tip.textContent = g.dataset.tip; tip.hidden = false; });
    g.addEventListener('pointermove', e => { tip.style.left = Math.min(e.clientX + 12, window.innerWidth - 300) + 'px'; tip.style.top = (e.clientY + 14) + 'px'; });
    g.addEventListener('pointerleave', () => { tip.hidden = true; });
  });
}
