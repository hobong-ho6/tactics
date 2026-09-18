/* 전술 갱신 히스토리 시각화 — 층별 4레인 타임라인 (2026-09-18, 사용자 지시 「리포트 전술 갱신 히스토리 시각화도 이어서」).
   dataviz 규약: 「언제 무엇이 바뀌었나」는 시간축 + **정체성(층)은 categorical 4색**(다크 서피스 검증 통과) ·
   같은 날 같은 층은 하나로 묶고 개수를 적는다 · 색만으로 읽히지 않게 레인 이름을 왼쪽에 고정 · 아래 목록이 표 뷰다. */
const esc = s => String(s ?? '').replace(/[&<>"]/g, c => ({ '&':'&amp;', '<':'&lt;', '>':'&gt;', '"':'&quot;' }[c]));
export const LANES = [
  { k: 'slot_canon', label: '슬롯 정본', col: '#3987e5' },
  { k: 'team_setup', label: '팀 설정',  col: '#d95926' },
  { k: 'starter',    label: '선발 처방', col: '#199e70' },
  { k: 'reflect',    label: '경기 반영', col: '#c98500' },
];
const DAY = 864e5;
const d2t = d => new Date(d + 'T00:00:00Z').getTime();

/* events: [{date, lane, title, detail}] — lane은 LANES.k. 클릭하면 onPick(date, lane)을 부른다. */
export function laneTimeline(events, { W = 900, onPickSel = null, today = new Date().toISOString().slice(0, 10) } = {}){
  if (!events.length) return '';
  const dates = events.map(e => d2t(e.date)).concat(d2t(today));
  const t0 = Math.min(...dates), t1 = Math.max(...dates), span = Math.max(DAY, t1 - t0);
  const L = 86, R = 18, T = 26, laneH = 34, H = T + LANES.length * laneH + 30;
  const x = t => L + (W - L - R) * ((t - t0) / span);
  /* 눈금 — 기간에 따라 주/월. 라벨이 겹치지 않게 최소 간격 70px를 확보한다. */
  const days = span / DAY, stepD = days > 120 ? 30 : days > 45 ? 14 : 7;
  const ticks = []; for (let t = t0; t <= t1 + 1; t += stepD * DAY) ticks.push(t);
  if ((W - L - R) / ticks.length < 70) ticks.length = Math.max(2, Math.floor((W - L - R) / 70));
  const grid = ticks.map(t => `<line x1="${x(t)}" x2="${x(t)}" y1="${T - 8}" y2="${H - 22}" stroke="var(--viz-grid)"/>
    <text x="${x(t)}" y="${T - 12}" text-anchor="middle" font-size="10" fill="var(--dim)">${new Date(t).toISOString().slice(5, 10)}</text>`).join('');
  const nowX = x(d2t(today));
  const nowLine = `<line x1="${nowX}" x2="${nowX}" y1="${T - 8}" y2="${H - 22}" stroke="var(--acc)" stroke-opacity=".5"/>
    <text x="${nowX}" y="${H - 8}" text-anchor="end" font-size="10" fill="var(--acc)">오늘</text>`;
  const body = LANES.map((ln, i) => { const y = T + i * laneH + 16;
    const mine = events.filter(e => e.lane === ln.k);
    const byDate = {}; for (const e of mine) (byDate[e.date] ??= []).push(e);
    const dots = Object.entries(byDate).map(([date, list]) => { const cx = x(d2t(date));
      const r = Math.min(11, 5 + Math.sqrt(list.length) * 2);
      const tip = `${date} · ${ln.label} ${list.length}건\n` + list.slice(0, 4).map(e => `· ${e.title}`).join('\n') + (list.length > 4 ? `\n… 외 ${list.length - 4}건` : '');
      return `<g class="hit" data-tip="${esc(tip)}" data-date="${date}" data-lane="${ln.k}" style="cursor:pointer">
        <circle cx="${cx}" cy="${y}" r="${r + 5}" fill="transparent"/>
        <circle cx="${cx}" cy="${y}" r="${r}" fill="var(--panel)"/><circle cx="${cx}" cy="${y}" r="${r - 2}" fill="${ln.col}" fill-opacity=".9"/>
        ${list.length > 1 ? `<text x="${cx}" y="${y + 3.5}" text-anchor="middle" font-size="9.5" font-weight="700" fill="#0b0f14">${list.length}</text>` : ''}</g>`; }).join('');
    const last = mine.length ? mine.map(e => e.date).sort().slice(-1)[0] : null;
    return `<g><line x1="${L}" x2="${W - R}" y1="${y}" y2="${y}" stroke="rgba(255,255,255,.06)"/>
      <text x="${L - 10}" y="${y + 4}" text-anchor="end" font-size="11" font-weight="600" fill="${ln.col}">${ln.label}</text>
      <text x="${L - 10}" y="${y + 15}" text-anchor="end" font-size="9" fill="var(--dim)">${mine.length}건${last ? ` · ${last.slice(5)}` : ''}</text>${dots}</g>`; }).join('');
  return `<svg width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" role="img" aria-label="전술 갱신 히스토리 타임라인">${grid}${nowLine}${body}</svg>
    <div class="lg">${LANES.map(l => `<span><i style="background:${l.col}"></i>${l.label}</span>`).join('')}
      <span class="dim">점 크기·숫자 = 그날 그 층의 건수 · 점을 누르면 아래 목록이 그 날짜로 좁혀진다</span></div>`;
}

export function mountTips(el, onPick){
  let tip = el.querySelector('.tip');
  if (!tip){ tip = document.createElement('div'); tip.className = 'tip'; tip.hidden = true; tip.style.whiteSpace = 'pre-line'; el.appendChild(tip); }
  el.querySelectorAll('.hit').forEach(g => {
    g.addEventListener('pointerenter', () => { tip.textContent = g.dataset.tip; tip.hidden = false; });
    g.addEventListener('pointermove', e => { tip.style.left = Math.min(e.clientX + 12, window.innerWidth - 320) + 'px'; tip.style.top = (e.clientY + 14) + 'px'; });
    g.addEventListener('pointerleave', () => { tip.hidden = true; });
    if (onPick) g.addEventListener('click', () => onPick(g.dataset.date, g.dataset.lane));
  });
}
