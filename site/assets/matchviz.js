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
  const rowH = 26, top = 22, H = top + rows.length * rowH + 8, C = W / 2, span = Math.max(90, C - 60 - 64), bar = 12;   // 가운데 라벨 폭 120 + 값 라벨 여백
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
  const H = 150, gw = Math.min(150, Math.max(110, (W - 140) / ps.length - 60)), x0 = 70, base = 118;
  const m = Math.max(...ps.flatMap(p => [num(p.xg_v) || 0, num(p.xg_o) || 0]), 0.5);
  const bars = ps.map((p, i) => { const gx = x0 + i * (gw + 60); const h = v => 70 * ((num(v) || 0) / m);
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

/* 컨테이너 렌더 + 호버 툴팁(마크가 히트 타깃, 값은 라벨·표로도 읽힌다).
   ⭐ SVG는 컨테이너 픽셀 폭으로 그린다(viewBox 확대 금지 — 넓은 화면에서 글자·점이 비대해진다). 창 크기가 바뀌면 다시 그린다. */
export function renderMatchViz(el, r, team){
  el.className = 'mviz';
  el.innerHTML = '<div class="vz wide" data-k="t"></div><div class="vz" data-k="b"></div><div class="vz" data-k="h"></div><div class="tip" hidden></div>';
  const tip = el.querySelector('.tip');
  const draw = () => {
    for (const box of el.querySelectorAll('.vz')){
      const w = Math.max(320, Math.floor(box.clientWidth - 26));      // 패널 패딩 12×2 + 테두리
      const k = box.dataset.k;
      const html = k === 't' ? timeline(r, team, Math.min(w, 1240)) : k === 'b' ? butterfly(r, team, Math.min(w, 760)) : halves(r, team, Math.min(w, 760));
      // 각 함수는 <div class="vz …">…</div> 래퍼를 돌려준다 → 안쪽만 옮긴다
      const tmp = document.createElement('div'); tmp.innerHTML = html;
      const inner = tmp.firstElementChild;
      box.innerHTML = inner ? inner.innerHTML : ''; box.hidden = !inner;
    }
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
