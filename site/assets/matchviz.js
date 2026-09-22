/* 경기 시각화 — 타임라인 · 팀 대조(버터플라이) · 하프 비교 (2026-09-18, 사용자 지시 「경기 분석 데이터를 타임라인에 맞춰 시각적으로」).
   dataviz 규약: 시리즈색 2개(우리 --viz-us / 상대 --viz-them, 다크 서피스 검증 통과) · 얇은 막대(≤24px, 데이터 끝 4px 라운드) ·
   2px 서피스 갭·링 · 격자 hairline · 값 라벨은 선택적, 호버 툴팁은 보조(표 뷰 = 기존 수치 표) · 텍스트는 시리즈색을 입지 않는다. */
const esc = s => String(s ?? '').replace(/[&<>"]/g, c => ({ '&':'&amp;', '<':'&lt;', '>':'&gt;', '"':'&quot;' }[c]));
const US = 'var(--viz-us)', THEM = 'var(--viz-them)', SURF = 'var(--panel)', GRID = 'var(--viz-grid)';
const num = v => (v == null || v === '' ? null : Number(v));
const fmt = (v, d = 0) => v == null ? '—' : Number(v).toLocaleString(undefined, { maximumFractionDigits: d, minimumFractionDigits: d });

/* ── 지표 설명 (2026-09-22 사용자 지시 「각 지표에 툴팁 · 축이 뭘 의미하는지 · 해석하는 법」).
   ⛔ 여기서 새 정의를 만들지 않는다 — 제공사(Opta/FotMob)와 docs/30의 정의를 그대로 옮긴다.
   ⚠️ 해석 문장에는 **오독 조건**을 같이 적는다. 「높으면 좋다」만 적으면 점유·상대 스타일에
      좌우되는 지표(클리어·태클)가 실력처럼 읽힌다. */
const HELP = {
  'xG': 'Expected Goals — 그 슛이 득점이 될 확률의 합. 0.3이면 「비슷한 위치·상황의 슛 10개 중 3개가 들어간다」는 뜻이다. 골보다 표본 잡음이 적어 한 경기의 기회 생산량을 재는 데 쓴다.',
  'xGOT': 'Expected Goals on Target — 슛이 **골문에 도달한 시점**의 코스·속도까지 반영한 값. 유효슛에만 존재한다(빗나간 슛은 0). xGOT − xG = 슈터가 코스로 벌어들인 몫 = 마무리.',
  '점유율 %': '팀이 공을 가진 시간 비중. ⚠️ 높다고 우세가 아니다 — 후퇴 수비를 택한 상대에게 공을 떠넘긴 결과일 수 있다.',
  '슈팅': '전체 슈팅 수. 안쪽 진한 부분이 유효슈팅(골문 안으로 향한 슛).',
  '빅찬스': 'Opta 정의의 「넣어야 했던 기회」 — 1대1, 골문 정면 근거리 등. 슛 수·xG와 달리 사람이 판정하는 지표다.',
  '코너': '코너킥 획득 수. 세트피스 의존도를 볼 때 슛 상황 분해와 함께 읽는다.',
  '패스': '시도한 패스 총수. 점유율과 강하게 같이 움직인다.',
  '크로스 성공/시도': '측면에서 박스로 올린 패스. 성공은 같은 팀이 받은 경우다.',
  '롱볼 성공/시도': '긴 전진 패스. 빌드업 설정(Long Ball ↔ Short Passing) 판정의 원자료다(docs/20 팀 설정 매핑 규칙).',
  'PPDA (낮을수록 강한 압박)': 'Passes Per Defensive Action — 상대가 수비 액션 하나를 당하기까지 허용한 패스 수. **낮을수록 강한 압박**이다. ⚠️ 점유가 극단적으로 높으면 분모가 말라 값이 부풀어 오른다(점유 74% 인플레).',
  '수비 액션 평균 위치': '태클·인터셉트 등 수비 액션이 일어난 지점의 평균 x(0=우리 골라인, 100=상대 골라인). 라인 높이의 프록시다 — 라인 높이 설정값 자체가 아니다.',
  '태클': '상대에게 걸어 공을 뺏으려 한 시도. ⚠️ 상대가 드리블을 많이 걸수록 늘어난다 — **상대 스타일의 함수**다.',
  '인터셉트': '상대 패스를 길에서 끊은 횟수. 태클과 달리 「읽고 미리 섰다」에 가깝다.',
  '클리어': '위험 지역에서 걷어낸 횟수. ⚠️ 많다고 잘 막은 게 아니다 — **점유가 낮으면 저절로 늘어난다**.',
  '공중전 승/시도': '공중 경합 승/시도. 세트피스 수비·타깃맨 공략의 원자료.',
  '드리블 성공/시도': '상대를 제치려 한 시도와 성공. 우리 값이 높으면 개인 돌파로 전진했다는 뜻이다.',
};
const READ = {
  finishing: '읽는 법 — 빈 원에서 채운 원으로 <b>오른쪽</b>으로 갔으면 코스가 좋았다(마무리 이득), <b>왼쪽</b>이면 골문 정면으로 약하게 찼다. 세로선(득점)이 채운 원보다 오른쪽이면 <b>골키퍼를 뚫은 것</b>, 왼쪽이면 <b>상대 GK가 막아낸 것</b>이다.',
  situations: '읽는 법 — 막대 <b>폭</b>은 슛 비중, 안쪽 어두운 띠 <b>높이</b>는 xG 비중이다. 띠가 폭보다 높으면 <b>적은 슛으로 좋은 기회</b>를 만든 칸이고, 낮으면 <b>슛만 많고 질은 낮은</b> 칸이다.',
  scoreState: '읽는 법 — 구간 <b>폭</b>은 그 국면이 이어진 분, 막대 <b>높이</b>는 10분당 xG다. 리드 구간에서 우리 막대가 내려가고 상대 막대가 올라가면 <b>내려앉았다</b>는 신호다. ⚠️ 상대가 몰아쳐 공을 못 잡은 결과일 수도 있으니 점유와 함께 읽는다.',
  butterfly: '읽는 법 — 가운데 선 기준 왼쪽이 우리, 오른쪽이 상대다. 막대 길이는 <b>그 행 안에서만</b> 비교한다(행마다 축이 다르다). PPDA만 <b>낮은 쪽이 강한 압박</b>이다.',
  duels: '읽는 법 — 이 다섯 행은 <b>점유 보정이 없다</b>. 점유가 낮은 팀은 클리어·태클이 저절로 늘고, 점유가 높은 팀은 드리블 시도가 늘어난다. <b>많다/적다가 아니라 어느 쪽 수치인지</b>로 읽는다.',
  timeline: '읽는 법 — 옅은 띠가 스코어 국면(주황=리드, 파랑=열세)이다. 띠가 바뀌는 지점 전후로 교체·카드가 몰렸다면 <b>국면에 반응한 조정</b>이다.',
  xgRace: '읽는 법 — 계단이 <b>가파르면</b> 그 구간에 기회가 몰린 것이다. 점(득점)이 계단 낮은 곳에 있으면 <b>적은 기회로 넣은 것</b>, 계단이 높은데 점이 없으면 <b>기회를 날린 구간</b>이다.',
  shotMap: '읽는 법 — 점이 클수록 xG가 높다(= 좋은 기회). 박스 밖 작은 점이 많으면 <b>안으로 못 들어가 밖에서 쏜</b> 경기다.',
  halves: '읽는 법 — 전·후반 막대 높이가 xG다. 후반에 우리 막대가 낮아지고 상대가 높아졌다면 <b>체력·교체·국면</b> 중 무엇이 원인인지 타임라인과 국면별 xG로 확인한다.',
};
/* h4에 다는 ? — 툴팁 배선은 renderMatchViz의 `.hit`가 그대로 처리한다(새 배선을 만들지 않는다). */
const q = tip => `<span class="hit vzq" data-tip="${esc(tip)}" tabindex="0">?</span>`;
const readLine = k => READ[k] ? `<span class="vz-read">${READ[k]}</span>` : '';

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
  return `<div class="vz wide"><h4>타임라인 ${q('가로축은 경기 분(0~90+)이다. 옅은 띠는 스코어 국면(주황=우리 리드, 파랑=열세, 색 없음=동점), 위쪽 표식이 우리 팀·아래쪽이 상대다.')} <span class="dim">— 득점 ${goals.length} · 교체 ${nSub} · 카드 ${nCard} · 위 = ${esc(team)}, 아래 = ${esc(r.opponent || '상대')}</span></h4>
    <svg width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" role="img" aria-label="경기 타임라인">${bands}${ticks}${half}${axis}
      <text x="${L}" y="${mid - 58}" class="dim sm">${esc(team)}</text><text x="${L}" y="${mid + 64}" class="dim sm">${esc(r.opponent || '상대')}</text>${marks}</svg>
    <div class="lg"><span><i style="background:${US}"></i>리드 구간</span><span><i style="background:${THEM}"></i>열세 구간</span><span>● 득점(도움)</span><span>▲ 교체 <span style="color:var(--warn)">▲</span> GK 교체</span><span><span style="color:var(--warn)">▮</span> 경고</span>${readLine('timeline')}</div></div>`;
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
  ], 'butterfly');
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
  ], 'duels');
}

/* 버터플라이 렌더러 — 팀 대조와 수비·경합이 공유한다(같은 모양이면 같은 코드로 그린다). */
function bfly(r, team, W, title, note, rows0, readKey){
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
    const hp = HELP[x.label];
    return `<g>
      ${hp ? `<g class="hit" data-tip="${esc(hp)}"><rect x="${C - 60}" y="${y}" width="120" height="${bar + 4}" fill="transparent"/>
          <text x="${C}" y="${y + 12}" text-anchor="middle" class="dim sm">${esc(x.label)}<tspan dx="3" fill="var(--acc)">?</tspan></text></g>`
        : `<text x="${C}" y="${y + 12}" text-anchor="middle" class="dim sm">${esc(x.label)}</text>`}
      <g class="hit" data-tip="${esc(tipA)}"><rect x="${C - 60 - span}" y="${y}" width="${span}" height="${bar + 4}" fill="transparent"/>
        ${x.a != null ? `<rect x="${C - 60 - wa}" y="${y + 2}" width="${Math.max(0, wa)}" height="${bar}" rx="3" fill="${US}" opacity="${x.aTot != null ? .35 : 1}"/>` : ''}
        ${x.aTot != null ? seg('a', x.a, x.aTot, US) : ''}${x.seg?.a != null ? seg('a', x.seg.a, x.a, 'rgba(0,0,0,.35)') : ''}
        <text x="${C - 66 - Math.max(wa, 0) - 4}" y="${y + 12}" text-anchor="end" class="sm">${la}</text></g>
      <g class="hit" data-tip="${esc(tipB)}"><rect x="${C + 60}" y="${y}" width="${span}" height="${bar + 4}" fill="transparent"/>
        ${x.b != null ? `<rect x="${C + 60}" y="${y + 2}" width="${Math.max(0, wb)}" height="${bar}" rx="3" fill="${THEM}" opacity="${x.bTot != null ? .35 : 1}"/>` : ''}
        ${x.bTot != null ? seg('b', x.b, x.bTot, THEM) : ''}${x.seg?.b != null ? seg('b', x.seg.b, x.b, 'rgba(0,0,0,.35)') : ''}
        <text x="${C + 66 + Math.max(wb, 0) + 4}" y="${y + 12}" class="sm">${lb}</text></g></g>`;
  }).join('');
  return `<div class="vz"><h4>${esc(title)} ${q('가운데 라벨이 지표명이고, 왼쪽 막대가 우리·오른쪽이 상대다. ⛔ 행마다 축이 달라 **같은 행 안에서만** 길이를 비교한다. 각 지표명에 마우스를 올리면 그 지표의 정의가 나온다.')}
      <span class="dim">— 왼쪽 ${esc(team)} · 오른쪽 ${esc(r.opponent || '상대')}. ${esc(note)}</span></h4>
    <svg width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" role="img" aria-label="${esc(title)}"><line x1="${C}" x2="${C}" y1="${top - 6}" y2="${H - 6}" stroke="${GRID}"/>${svgRows}</svg>
    <div class="lg"><span><i style="background:${US}"></i>${esc(team)}</span><span><i style="background:${THEM}"></i>${esc(r.opponent || '상대')}</span><span><i style="background:${US};opacity:.35"></i>시도(연한) / 성공(진한)</span>${readLine(readKey)}</div></div>`;
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
  /* ⛔ **득점도 같은 축에 찍힌다** — xG·xGOT·득점은 전부 「골 개수」 단위라 한 축에 놓을 수 있다.
     종전에는 축 최댓값을 xG·xGOT로만 잡아 **3골짜리 세로선이 축 밖으로 밀려** 오른쪽 끝에 붙었다
     (2026-09-22 사용자 지적 「가로선이 뭔지 모르겠다」 — 축이 안 맞아 읽히지 않았던 것). */
  const maxX = Math.max(A.xgot, B.xgot, A.xg, B.xg, A.goals, B.goals, 0.5) * 1.15;
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
      <text x="${x(d.goals)}" y="${y - 23}" text-anchor="middle" class="sm" fill="var(--fg)">${d.goals}골</text>
      <text x="${x(d.xg)}" y="${y - 16}" text-anchor="middle" class="sm">${fmt(d.xg, 2)}</text>
      <text x="${x(d.xgot)}" y="${y + 25}" text-anchor="middle" class="sm"><tspan font-weight="700">${fmt(d.xgot, 2)}</tspan></text>
      </g>`;
  };
  const gain = A.xgot - A.xg, gk = B.xgot - B.goals;
  return `<div class="vz"><h4>결정력 ${q(`${HELP.xG}\n\n${HELP.xGOT}\n\n가로축은 셋 다 같은 단위(골 개수)라 한 축에 놓을 수 있다 — 빈 원 xG · 채운 원 xGOT · 세로선 실득점.`)}
      <span class="dim">— 가로축: 골 개수 단위</span></h4>
    <svg width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" role="img" aria-label="결정력">${ticks}
      <text x="${(L + W - R) / 2}" y="${H - 8}" text-anchor="middle" class="dim sm">xG · xGOT · 득점 (골 개수)</text>
      ${line(A, rowY[0], US, team)}${line(B, rowY[1], THEM, r.opponent || '상대')}</svg>
    <div class="lg"><span>○ xG</span><span>● xGOT</span><span>│ 실득점</span>
      <span><b>${esc(team)} 마무리 ${gain >= 0 ? '+' : ''}${fmt(gain, 2)}</b> (xGOT−xG · 슈터 축)</span>
      <span>GK 선방 기여 <b>${fmt(gk, 2)}</b> (상대 xGOT ${fmt(B.xgot, 2)} − 실점 ${B.goals} · <b>다른 지표다</b>)</span>
      ${readLine('finishing')}</div></div>`;
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
  return `<div class="vz"><h4>슛이 나온 상황 ${q(`슛을 만든 국면으로 나눈 것이다. 오픈플레이 = 흐름 속 · 세트피스 = 코너·프리킥·스로인 · 역습 = 속공 · 페널티.\n\n가로축은 그 팀의 슛 100%를 채운 비율이고(두 팀의 막대 길이는 서로 비교하지 않는다), 안쪽 어두운 띠 높이는 그 칸이 가져간 xG 비중이다.\n\n${HELP.xG}`)}
      <span class="dim">— 가로: 그 팀 슛의 100%${hasXg ? ' · 세로 띠: xG 비중' : ' · ⚠️ 이 회차는 슛별 xG 미제공'}</span></h4>
    <svg width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" role="img" aria-label="슛 상황 분해">
      ${bar(A, rowY[0], US, team)}${bar(B, rowY[1], THEM, r.opponent || '상대')}</svg>
    <div class="lg">${lg}${readLine('situations')}</div></div>`;
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
  return `<div class="vz"><h4>스코어 국면별 xG ${q(`경기를 스코어 상태(리드·동점·열세)로 잘라 각 구간의 기회 생산 속도를 잰다.\n\n세로축은 10분당 xG다 — 구간 길이가 달라도 비교되게 분당으로 환산했다. 구간의 가로 폭은 그 국면이 이어진 분이다.\n\n${HELP.xG}`)}
      <span class="dim">— 세로: 10분당 xG · 가로 폭: 국면 지속 분</span></h4>
    <svg width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" role="img" aria-label="스코어 국면별 xG">
      <line x1="${L}" x2="${W - R}" y1="${base}" y2="${base}" stroke="var(--line)"/>
      <text x="${L - 6}" y="${T + 8}" text-anchor="end" class="dim sm">${maxY.toFixed(1)}</text>
      <text x="${L - 6}" y="${base + 3}" text-anchor="end" class="dim sm">0</text>${groups}</svg>
    <div class="lg"><span><i style="background:${US}"></i>${esc(team)}</span><span><i style="background:${THEM}"></i>${esc(r.opponent || '상대')}</span>
      <span>⚠️ 15분 미만 구간은 흐리게 — 분당 값이 튄다</span>${readLine('scoreState')}</div></div>`;
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
  return `<div class="vz"><h4>하프 비교 ${q(`전반·후반을 나눠 각 반의 xG와 점유를 본다. 막대 높이가 xG, 아래 띠가 점유 비중이다.\n\n${HELP.xG}`)} <span class="dim">— xG(막대)와 점유(띠)</span></h4>
    <svg width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" role="img" aria-label="하프별 비교"><line x1="${x0 - 10}" x2="${W - 20}" y1="${base}" y2="${base}" stroke="var(--line)"/><text x="${x0 - 14}" y="${base + 4}" text-anchor="end" class="dim sm">xG</text>${bars}</svg>
    <div class="lg"><span><i style="background:${US}"></i>${esc(team)}</span><span><i style="background:${THEM}"></i>${esc(r.opponent || '상대')}</span>${readLine('halves')}</div></div>`;
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
  return `<div class="vz"><h4>xG 레이스 ${q(`가로축은 경기 분, 세로축은 그 시점까지 쌓인 누적 xG다. 슛이 나올 때마다 계단이 한 칸 올라간다.\n\n${HELP.xG}`)} <span class="dim">— 누적 기대득점 · 점 = 득점 · ${esc(prov)} 모델</span></h4>
    <svg width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" role="img" aria-label="누적 xG">${ys}
      <line x1="${x(45)}" x2="${x(45)}" y1="${T}" y2="${H - B}" stroke="var(--line)"/><text x="${x(45)}" y="${T - 4}" text-anchor="middle" class="dim sm">HT</text>
      ${step(pts.o, THEM)}${step(pts.v, US)}${gm}${endLab('v', US)}${endLab('o', THEM)}${ticks}
      <rect class="xhair" x="${L}" y="${T}" width="${W - L - R}" height="${H - T - B}" fill="transparent" data-l="${L}" data-w="${W - L - R}" data-end="${end}"/></svg>
    <div class="lg"><span><i style="background:${US}"></i>${esc(team)} ${fmt(tot.v, 2)}</span><span><i style="background:${THEM}"></i>${esc(r.opponent || '상대')} ${fmt(tot.o, 2)}</span>${readLine('xgRace')}</div></div>`;
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
  return `<div class="vz"><h4>슛 맵 ${q(`슛이 일어난 지점을 피치 위에 찍은 것이다. 두 팀이 서로 반대 골문을 공격하도록 그린다 — 우리는 오른쪽 골문.\n\n점의 크기가 그 슛의 xG다.\n\n${HELP.xG}`)} <span class="dim">— ${esc(team)} → 오른쪽 골문 · ${esc(r.opponent || '상대')} → 왼쪽 · 점 크기 = xG · 채움 = 득점</span></h4>
    <svg width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" role="img" aria-label="슛 맵">${pitch}${dots}
      <text x="${X(PW) - 4}" y="${Y(PH) + 12}" text-anchor="end" class="dim sm">${esc(team)} 슛 ${n('v')} · 득점 ${g('v')}</text>
      <text x="${X(0) + 4}" y="${Y(PH) + 12}" class="dim sm">${esc(r.opponent || '상대')} 슛 ${n('o')} · 득점 ${g('o')}</text></svg>
    <div class="lg">${readLine('shotMap')}</div></div>`;
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
  /* ⚠️⚠️ 행 높이를 22 → 17 → **14px**로 줄인다(2026-09-22 사용자 지적 2회 — 17px도 여전히 컸다).
     17명 × 14 + 머리 = 270px 안쪽. 막대는 8px로 낮추되 색·길이는 그대로라 읽는 데 지장 없다. */
  const L = 132, GAP = 18, T = 22, rowH = 14, barH = 8, H = T + rows.length * rowH + 8;
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
    /* ⛔ 라벨을 「선발(x=4) · 포지션(x=30) · 이름(오른쪽 정렬)」 세 칸으로 나눠 그리면
       **글자 폭을 모르는 채 자리를 고정**하는 셈이라 긴 이름·긴 포지션에서 겹친다
       (2026-09-22 사용자 지적: 「LDM주앙 고메스」·「LB마테오 루헤리」).
       ⇒ **한 줄로 왼쪽 정렬**해 이어 쓰면 겹칠 자리가 없다. 넘치는 만큼은 잘라내고 전문은 툴팁에 둔다. */
    const cut = (t, n) => { t = String(t ?? ''); return t.length > n ? t.slice(0, n - 1) + '…' : t; };
    const pos = cut(String(p.position ?? '').replace(/\s*\(.*$/, ''), 5);   // 「RDM(명단 등록 교체)」의 괄호는 툴팁으로
    return `<g class="hit" data-tip="${esc(tip)}" data-pid="${p.player_id ?? ''}" style="cursor:pointer">
      <text x="4" y="${y + 3}" font-size="9" fill="var(--txt)"><tspan fill="${p.started ? 'var(--acc)' : 'var(--dim)'}" font-size="8">${p.started ? '선발' : '교체'}</tspan>
        <tspan fill="var(--dim)" font-size="8" dx="3">${esc(pos)}</tspan><tspan dx="4">${esc(cut(p.label, 9))}</tspan></text>
      <rect x="${gx(p.start)}" y="${y - barH / 2}" width="${Math.max(2, gx(p.stop) - gx(p.start))}" height="${barH}" rx="2.5" fill="${US}" fill-opacity="${p.started ? .8 : .45}"/>
      <text x="${gx(p.stop) + 4}" y="${y + 3}" font-size="8" fill="var(--dim)">${p.minutes ?? '—'}′</text>
      ${p.rating != null ? `<rect x="${rx0}" y="${y - barH / 2}" width="${Math.max(2, rx(p.rating) - rx0)}" height="${barH}" rx="2.5" fill="${col(p.rating)}" fill-opacity=".85"/>
        <text x="${rx(p.rating) + 5}" y="${y + 3}" font-size="9" font-weight="700" fill="var(--txt)">${p.rating}</text>
        <text x="${W - 6}" y="${y + 3}" text-anchor="end" font-size="8" fill="var(--dim)">접점 ${p.hit_points ?? '—'}</text>`
        : `<text x="${rx0}" y="${y + 3}" font-size="9" fill="var(--dim)">평점 미수집</text>`}</g>`; }).join('');
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
