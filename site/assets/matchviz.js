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
  return bfly(r, team, W, '팀 대조', 'xG·슈팅의 어두운 안쪽 = 오픈플레이·유효슈팅', [
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
  ]);
}

/* ── 2b. 수비·경합 프로필 (2026-09-22 신설) — 「어디서 공을 되찾았나 / 얼마나 밀렸나」.
   PPDA·라인 높이만으로는 **압박 성공**과 **후퇴 방어**가 구분되지 않는다. 다섯 행이 그것을 가른다.
   ⚠️⚠️ **점유 보정이 없다.** 클리어 37은 「수비를 잘했다」가 아니라 **점유 36%의 부산물**일 수 있고,
        태클 수는 상대가 드리블을 얼마나 거는가(= 상대 스타일)의 함수다. 캡션에 그 사실을 박아 둔다.
   ⭐ 팀 대조와 한 카드에 합치지 않는다 — 15행이 되면 460px 카드에서 막대가 뭉개진다. */
export function duels(r, team, W = 560){
  const v = k => num(r[k]);
  return bfly(r, team, W, '수비 · 경합', '⚠️ 점유 보정 없음 — 점유가 낮으면 클리어·태클이 저절로 늘어난다', [
    { label:'태클', a: v('tackles_v'), b: v('tackles_o'), d: 0 },
    { label:'인터셉트', a: v('interceptions_v'), b: v('interceptions_o'), d: 0 },
    { label:'클리어', a: v('clearances_v'), b: v('clearances_o'), d: 0 },
    { label:'공중전 승/시도', a: v('aerial_won_v'), b: v('aerial_won_o'), d: 0, aTot: v('aerial_att_v'), bTot: v('aerial_att_o') },
    { label:'드리블 성공/시도', a: v('dribble_succ_v'), b: v('dribble_succ_o'), d: 0, aTot: v('dribble_att_v'), bTot: v('dribble_att_o') },
  ]);
}

/* 버터플라이 렌더러 — 팀 대조와 수비·경합이 공유한다(같은 모양이면 같은 코드로 그린다). */
function bfly(r, team, W, title, note, rows0){
  const rows = rows0.filter(x => x.a != null || x.b != null);
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
  return `<div class="vz"><h4>${esc(title)} <span class="dim">— 왼쪽 ${esc(team)} · 오른쪽 ${esc(r.opponent || '상대')}. ${esc(note)}</span></h4>
    <svg width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" role="img" aria-label="${esc(title)}"><line x1="${C}" x2="${C}" y1="${top - 6}" y2="${H - 6}" stroke="${GRID}"/>${svgRows}</svg>
    <div class="lg"><span><i style="background:${US}"></i>${esc(team)}</span><span><i style="background:${THEM}"></i>${esc(r.opponent || '상대')}</span><span><i style="background:${US};opacity:.35"></i>시도(연한) / 성공(진한)</span></div></div>`;
}

/* ── 6. 결정력 — xG → xGOT → 실득점 (2026-09-22 신설).
   「기회를 못 만든 경기」와 「마무리·선방에서 갈린 경기」를 가른다. 한 줄에 세 점을 놓아
   만든 기회의 질(xG) → 골문에 도달한 시점의 질(xGOT) → 결과(득점)를 눈으로 잇는다.
   ⛔⛔ **유효슛을 `outcome`으로 판정하지 말 것.** FotMob 행은 **블록슛까지 `save`로 접어** 둔다
        (5경기 표본: save 62건 중 43건이 xgot=0). ⇒ **`xgot > 0`이 유효슛**이고, 7경기에서
        그 개수가 `team_match_stats.sot`와 정확히 일치하는 것으로 검증했다.
   ⚠️ `xgot = 0`은 결손이 아니라 **「유효슛이 아님」의 확정값**이다. 결손은 `null`(12경기 전량).
   ⚠️ xGOT−xG는 **슈터의 마무리**지 우리 GK 성적이 아니다 — GK 축은 「상대 xGOT − 실점」으로 따로 적는다. */
export function finishing(r, team, W = 560){
  const S = (r.shots || []).filter(s => s.xgot != null);
  if (!S.length) return `<div class="vz"><h4>결정력</h4><span class="dim" style="font-size:12px">xGOT 미수집 — 제공사가 슛별 xGOT를 주지 않은 회차다(결손이지 0이 아니다).</span></div>`;
  const agg = side => { const on = S.filter(s => s.side === side && s.xgot > 0);
    return { sot: on.length, xg: on.reduce((t, s) => t + (num(s.xg) || 0), 0),
             xgot: on.reduce((t, s) => t + num(s.xgot), 0),
             goals: S.filter(s => s.side === side && s.outcome === 'goal').length }; };
  const A = agg('v'), B = agg('o');
  const maxX = Math.max(A.xgot, B.xgot, A.xg, B.xg, 0.5) * 1.15;
  const H = 330, L = 74, R = 58, T = 40, rowY = [T + 62, T + 176];   // 460px 카드를 채우는 비율
  const x = v => L + (W - L - R) * (v / maxX);
  const ticks = [0, maxX / 2, maxX].map(v =>
    `<line x1="${x(v)}" x2="${x(v)}" y1="${T}" y2="${H - 46}" stroke="${GRID}"/><text x="${x(v)}" y="${H - 30}" text-anchor="middle" class="dim sm">${v.toFixed(1)}</text>`).join('');
  const line = (d, y, col, name) => {
    const gain = d.xgot - d.xg;
    const tip = `${name} · 유효슛 ${d.sot} · xG ${fmt(d.xg, 2)} → xGOT ${fmt(d.xgot, 2)} (마무리 ${gain >= 0 ? '+' : ''}${fmt(gain, 2)}) → 득점 ${d.goals}`;
    return `<g class="hit" data-tip="${esc(tip)}">
      <text x="${L - 8}" y="${y + 4}" text-anchor="end" class="dim sm">${esc(name)}</text>
      <line x1="${x(Math.min(d.xg, d.xgot))}" x2="${x(Math.max(d.xg, d.xgot))}" y1="${y}" y2="${y}" stroke="${col}" stroke-width="4" opacity=".5"/>
      <circle cx="${x(d.xg)}" cy="${y}" r="8" fill="${SURF}" stroke="${col}" stroke-width="2"/>
      <circle cx="${x(d.xgot)}" cy="${y}" r="8" fill="${col}"/>
      <line x1="${x(d.goals)}" x2="${x(d.goals)}" y1="${y - 18}" y2="${y + 18}" stroke="var(--fg)" stroke-width="2"/>
      <text x="${x(d.xg)}" y="${y - 16}" text-anchor="middle" class="sm">${fmt(d.xg, 2)}</text>
      <text x="${x(d.xgot)}" y="${y + 25}" text-anchor="middle" class="sm"><tspan font-weight="700">${fmt(d.xgot, 2)}</tspan></text>
      <text x="${W - R + 6}" y="${y + 4}" class="sm"><tspan font-weight="700">${d.goals}골</tspan></text></g>`;
  };
  const gain = A.xgot - A.xg, gk = B.xgot - B.goals;
  return `<div class="vz"><h4>결정력 <span class="dim">— 빈 원 xG → 채운 원 xGOT → 세로선 실득점. 유효슛만(xGOT&gt;0)</span></h4>
    <svg width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" role="img" aria-label="결정력">${ticks}
      ${line(A, rowY[0], US, team)}${line(B, rowY[1], THEM, r.opponent || '상대')}</svg>
    <div class="lg"><span><b>${esc(team)} 마무리 ${gain >= 0 ? '+' : ''}${fmt(gain, 2)}</b> (xGOT−xG · 슈터 축)</span>
      <span>GK 선방 기여 <b>${fmt(gk, 2)}</b> (상대 xGOT ${fmt(B.xgot, 2)} − 실점 ${B.goals} · <b>다른 지표다</b>)</span></div></div>`;
}

/* ── 7. 슛 상황 분해 (2026-09-22 신설) — 슛·xG가 오픈플레이·세트피스·역습·PK 중 어디서 나왔나.
   「세트피스로 먹고사는가」를 경기 단위로 닫는다(에메리·시메오네 축의 핵심 질문).
   ⚠️⚠️ **어휘가 정규화되어 있지 않다** — 한 컬럼에 제공사 두 계열이 섞여 16종이 관측된다
        (`corner`/`FromCorner` · `regular`/`RegularPlay` · `fast-break`/`FastBreak` …).
        ⇒ 소문자화 + 구분자 제거 후 매핑한다. `assisted`는 SofaScore의 **오픈플레이 어시스트 슛**이라
        `regular`와 같은 칸이다(따로 세면 오픈플레이가 쪼개져 세트피스 비중이 부풀어 보인다).
   ⚠️ 슛당 평균 xG는 n=1~3에서 무의미하다 — **총합만** 쓴다. */
const SIT_KEY = s => { const k = String(s || '').toLowerCase().replace(/[-_ ]/g, '');
  return /penalty/.test(k) ? 'pk' : /corner|setpiece|freekick|throwin/.test(k) ? 'set'
       : /fastbreak|counter/.test(k) ? 'tr' : 'op'; };
const SIT_NAME = { op:'오픈플레이', set:'세트피스', tr:'역습', pk:'페널티' };
const SIT_ORDER = ['op', 'set', 'tr', 'pk'];
export function shotSituations(r, team, W = 560){
  const S = r.shots || []; if (!S.length) return '';
  const hasXg = S.some(s => s.xg != null);
  const side = sd => { const arr = S.filter(s => s.side === sd);
    return { n: arr.length, parts: SIT_ORDER.map(k => { const g = arr.filter(s => SIT_KEY(s.situation) === k);
      return { k, n: g.length, xg: g.reduce((t, s) => t + (num(s.xg) || 0), 0) }; }).filter(p => p.n) }; };
  const A = side('v'), B = side('o');
  if (!A.n && !B.n) return '';
  const H = 330, L = 74, R = 24, T = 40, barH = 72, rowY = [T + 24, T + 164];   // 460px 카드를 채우는 비율
  const span = W - L - R;
  const COL = { op:.95, set:.62, tr:.38, pk:.2 };      // 같은 팀색의 밝기 단계 — 시리즈색은 팀이 정한다
  const bar = (d, y, col, name) => {
    if (!d.n) return `<text x="${L}" y="${y + 20}" class="dim sm">슛 없음</text>`;
    let cx = L;
    const segs = d.parts.map(p => { const w = span * (p.n / d.n); const x0 = cx; cx += w;
      const tip = `${name} · ${SIT_NAME[p.k]} ${p.n}슛 (슛 ${Math.round(p.n / d.n * 100)}%)` + (hasXg ? ` · xG ${fmt(p.xg, 2)}` : '');
      /* ⭐ 안쪽 진한 띠 = 그 칸의 **xG 몫**. 높이를 팀 총 xG 대비 비율로 잡으면
         「폭(슛 비중) vs 높이(xG 비중)」가 바로 비교된다 — 띠가 폭보다 높으면 **기회의 질이 좋았던 칸**이다.
         ⛔ 최댓값 기준으로 정규화하면 1등 칸이 늘 꽉 차 「100%」로 오독된다. */
      const xgTot = d.parts.reduce((t, q) => t + q.xg, 0);
      const xgH = hasXg && xgTot > 0 ? barH * (p.xg / xgTot) : 0;
      return `<g class="hit" data-tip="${esc(tip)}">
        <rect x="${x0}" y="${y}" width="${Math.max(0, w - 1.5)}" height="${barH}" rx="3" fill="${col}" opacity="${COL[p.k]}"/>
        ${xgH ? `<rect x="${x0}" y="${y + barH - xgH}" width="${Math.max(0, w - 1.5)}" height="${xgH}" fill="rgba(0,0,0,.34)"/>` : ''}
        ${w > 34 ? `<text x="${x0 + w / 2}" y="${y + barH / 2 + 4}" text-anchor="middle" class="sm">${p.n}</text>` : ''}</g>`; }).join('');
    return `<text x="${L - 8}" y="${y + barH / 2 + 4}" text-anchor="end" class="dim sm">${esc(name)}</text>${segs}
      <text x="${L}" y="${y - 5}" class="dim sm">${d.n}슛${hasXg ? ` · xG ${fmt(d.parts.reduce((t, p) => t + p.xg, 0), 2)}` : ''}</text>`;
  };
  const lg = SIT_ORDER.map(k => `<span><i style="background:${US};opacity:${COL[k]}"></i>${SIT_NAME[k]}</span>`).join('');
  return `<div class="vz"><h4>슛이 나온 상황 <span class="dim">— 막대 길이 = 슛 비중${hasXg ? ' · 아래 어두운 띠 높이 = xG 비중 (띠가 폭보다 높으면 질 좋은 기회)' : ' · ⚠️ 이 회차는 슛별 xG 미제공'}</span></h4>
    <svg width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" role="img" aria-label="슛 상황 분해">
      ${bar(A, rowY[0], US, team)}${bar(B, rowY[1], THEM, r.opponent || '상대')}</svg>
    <div class="lg">${lg}</div></div>`;
}

/* ── 8. 스코어 국면별 xG 레이트 (2026-09-22 신설) — 「리드하면 내려앉는가」를 수치로.
   타임라인이 국면 띠는 그리지만 **수치가 없어** 「내려앉았다」가 늘 인상 평가였다.
   ⚠️⚠️ 국면이 짧으면 분당 값이 폭발한다 ⇒ **구간 분(n)을 항상 병기하고 15분 미만은 흐리게** 처리한다.
   ⚠️ 리드 구간의 낮은 xG는 전술 선택일 수도, 상대가 몰아쳐 공을 못 잡은 결과일 수도 있다 — 점유와 함께 읽는다.
   ⭐ 국면은 `player_matches.stats_json`의 phase_* 가 아니라 **`match_events`에서 다시 만든다**
      (phase_*는 리포트 38~45에만 있고 최근 회차엔 없다 — events 쪽이 커버리지가 넓다). */
export function scoreStateXg(r, team, W = 560){
  const ev = (r.events || []).filter(e => /goal$/.test(e.kind) && e.score_v != null).sort((a, b) => a.minute - b.minute);
  const shots = (r.shots || []).filter(s => s.xg != null);
  if (!shots.length) return '';
  const end = Math.max(90, ...(r.events || []).map(e => e.minute), ...shots.map(s => s.minute));
  const segs = []; let sv = 0, so = 0, from = 0;
  const st = () => sv > so ? 'lead' : sv < so ? 'trail' : 'level';
  for (const e of ev){ segs.push({ s: st(), a: from, b: e.minute }); sv = e.score_v; so = e.score_o; from = e.minute; }
  segs.push({ s: st(), a: from, b: end });
  const B = { lead: { min: 0, v: 0, o: 0 }, level: { min: 0, v: 0, o: 0 }, trail: { min: 0, v: 0, o: 0 } };
  for (const g of segs) B[g.s].min += Math.max(0, g.b - g.a);
  for (const s of shots){ const g = segs.find(q => s.minute >= q.a && s.minute < q.b) || segs[segs.length - 1];
    B[g.s][s.side] += num(s.xg); }
  const keys = ['lead', 'level', 'trail'].filter(k => B[k].min > 0);
  if (keys.length < 2) return '';        // 한 국면뿐이면 비교가 아니다
  const NAME = { lead:'리드', level:'동점', trail:'열세' };
  const rate = (k, sd) => B[k].min ? B[k][sd] / B[k].min * 10 : 0;     // 10분당 xG
  const maxY = Math.max(0.1, ...keys.flatMap(k => [rate(k, 'v'), rate(k, 'o')])) * 1.2;
  const H = 210, T = 26, base = H - 44, L = 40, R = 16;
  const totalMin = keys.reduce((t, k) => t + B[k].min, 0);
  let cx = L; const inner = W - L - R;
  const groups = keys.map(k => {
    const gw = inner * (B[k].min / totalMin), x0 = cx; cx += gw;
    const thin = B[k].min < 15;
    const bw = Math.min(26, Math.max(10, gw / 2 - 8));
    const h = v => (base - T) * (v / maxY);
    const one = (sd, col, off) => { const v = rate(k, sd), hh = h(v);
      return `<g class="hit" data-tip="${esc(`${NAME[k]} 구간 ${B[k].min}분 · ${sd === 'v' ? team : (r.opponent || '상대')} xG ${fmt(B[k][sd], 2)} = 10분당 ${fmt(v, 2)}${thin ? ' ⚠️ 15분 미만 표본' : ''}`)}">
        <rect x="${x0 + gw / 2 + off}" y="${base - hh}" width="${bw}" height="${Math.max(0, hh)}" rx="3" fill="${col}" fill-opacity="${thin ? .35 : 1}"/>
        <text x="${x0 + gw / 2 + off + bw / 2}" y="${base - hh - 4}" text-anchor="middle" class="sm">${fmt(v, 2)}</text></g>`; };
    return `<g>${one('v', US, -bw - 2)}${one('o', THEM, 2)}
      <text x="${x0 + gw / 2}" y="${base + 15}" text-anchor="middle" class="dim sm">${NAME[k]}</text>
      <text x="${x0 + gw / 2}" y="${base + 27}" text-anchor="middle" class="dim sm">${B[k].min}분${thin ? ' ⚠️' : ''}</text>
      <line x1="${x0}" x2="${x0}" y1="${T}" y2="${base}" stroke="${GRID}"/></g>`;
  }).join('');
  return `<div class="vz"><h4>스코어 국면별 xG <span class="dim">— 막대 폭이 아니라 <b>높이</b>가 10분당 xG · 구간 폭 ∝ 그 국면 지속 분</span></h4>
    <svg width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" role="img" aria-label="스코어 국면별 xG">
      <line x1="${L}" x2="${W - R}" y1="${base}" y2="${base}" stroke="var(--line)"/>
      <text x="${L - 6}" y="${T + 8}" text-anchor="end" class="dim sm">${maxY.toFixed(1)}</text>
      <text x="${L - 6}" y="${base + 3}" text-anchor="end" class="dim sm">0</text>${groups}</svg>
    <div class="lg"><span><i style="background:${US}"></i>${esc(team)}</span><span><i style="background:${THEM}"></i>${esc(r.opponent || '상대')}</span>
      <span>⚠️ 15분 미만 구간은 흐리게 — 분당 값이 튄다</span></div></div>`;
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
  /* ⚠️ 행 높이 22px·라벨 118px이면 17명에서 표가 화면을 잡아먹는다(2026-09-22 사용자 지적).
     행을 17px로 줄이고 라벨·여백도 함께 줄인다 — 막대는 그대로라 읽는 데 지장 없다. */
  const L = 104, GAP = 20, T = 24, rowH = 17, H = T + rows.length * rowH + 10;
  const ganttW = Math.round((W - L - GAP) * 0.52), ratW = W - L - GAP - ganttW;
  const gx = m => L + ganttW * (m / end);
  const rx0 = L + ganttW + GAP, lo = 5.5, hi = 10;
  const rx = v => rx0 + (ratW - 44) * ((Math.min(hi, Math.max(lo, v)) - lo) / (hi - lo));
  const col = v => v == null ? 'rgba(255,255,255,.25)' : v >= 7.5 ? 'var(--ok)' : v >= 6.5 ? 'var(--warn)' : 'var(--bad)';
  const ticks = [0, 15, 30, 45, 60, 75, 90].filter(t => t <= end).map(t =>
    `<line x1="${gx(t)}" x2="${gx(t)}" y1="${T - 8}" y2="${H - 8}" stroke="${GRID}"/><text x="${gx(t)}" y="${T - 12}" text-anchor="middle" font-size="10" fill="var(--dim)">${t}′</text>`).join('');
  const rticks = [6, 7, 8, 9].map(v =>
    `<line x1="${rx(v)}" x2="${rx(v)}" y1="${T - 8}" y2="${H - 8}" stroke="${GRID}"/><text x="${rx(v)}" y="${T - 12}" text-anchor="middle" font-size="10" fill="var(--dim)">${v}</text>`).join('');
  const body = rows.map((p, i) => { const y = T + i * rowH + 11;
    const tip = `${p.position ?? ''} ${p.label} · ${p.started ? '선발' : '교체'} · ${p.start}′~${p.stop}′(${p.minutes ?? '—'}분) · 평점 ${p.rating ?? '—'} · 접점 ${p.hit_points ?? '—'}`;
    return `<g class="hit" data-tip="${esc(tip)}" data-pid="${p.player_id ?? ''}" style="cursor:pointer">
      <text x="${L - 8}" y="${y + 3.5}" text-anchor="end" font-size="10" fill="var(--txt)">${esc(p.label)}</text>
      <text x="4" y="${y + 3.5}" font-size="8.5" fill="${p.started ? 'var(--acc)' : 'var(--dim)'}">${p.started ? '선발' : '교체'}</text>
      <text x="30" y="${y + 3.5}" font-size="8.5" fill="var(--dim)">${esc(p.position ?? '')}</text>
      <rect x="${gx(p.start)}" y="${y - 5}" width="${Math.max(2, gx(p.stop) - gx(p.start))}" height="10" rx="3" fill="${US}" fill-opacity="${p.started ? .8 : .45}"/>
      <text x="${gx(p.stop) + 4}" y="${y + 3.5}" font-size="8.5" fill="var(--dim)">${p.minutes ?? '—'}′</text>
      ${p.rating != null ? `<rect x="${rx0}" y="${y - 5}" width="${Math.max(2, rx(p.rating) - rx0)}" height="10" rx="3" fill="${col(p.rating)}" fill-opacity=".85"/>
        <text x="${rx(p.rating) + 5}" y="${y + 3.5}" font-size="9.5" font-weight="700" fill="var(--txt)">${p.rating}</text>
        <text x="${W - 6}" y="${y + 3.5}" text-anchor="end" font-size="8.5" fill="var(--dim)">접점 ${p.hit_points ?? '—'}</text>`
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
  /* 순서 = 읽는 순서다: 흐름(타임라인) → 기회의 양(xG 레이스·슛 맵) → 기회의 질(결정력·상황) →
     국면(스코어 국면·하프) → 팀 대조 → 수비·경합. ⛔ 원자료가 없는 카드는 draw()가 숨긴다. */
  el.innerHTML = ['t|wide','x','s','f','q','c','h','b','d']
    .map(k => `<div class="vz${k.includes('|wide') ? ' wide' : ''}" data-k="${k[0]}"></div>`).join('')
    + '<div class="tip" hidden></div>';
  const tip = el.querySelector('.tip');
  const draw = () => {
    for (const box of el.querySelectorAll('.vz')){
      const w = Math.max(320, Math.floor(box.clientWidth - 26));      // 패널 패딩 12×2 + 테두리
      const k = box.dataset.k;
      const w2 = Math.min(w, 720);
      const html = k === 't' ? timeline(r, team, Math.min(w, 1240))
        : k === 'x' ? xgRace(r, team, w2) : k === 's' ? shotMap(r, team, w2)
        : k === 'f' ? finishing(r, team, w2) : k === 'q' ? shotSituations(r, team, w2)
        : k === 'c' ? scoreStateXg(r, team, w2) : k === 'h' ? halves(r, team, w2)
        : k === 'b' ? butterfly(r, team, w2) : duels(r, team, w2);
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
