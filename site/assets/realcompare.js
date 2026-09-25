/* 실측 선수 비교 — 「선수 비교」 화면의 머리 대 머리 패널 (2026-09-24 신설,
   사용자 지시 「얼티밋팀에서 선수 비교하는것처럼 시각화하고 더 많은 데이터를 비교 … 제안도해줘」).

   ⛔⛔ **얼티밋팀(clubviz.js compareCards)과 축이 다르다.** 저쪽은 **카드 스탯**(EA가 준 숫자)을 비교하고
   여기는 **실축 실측**(경기에서 나온 값)을 비교한다. 같은 화면처럼 보이되 섞지 않는다 —
   카드 OVR과 리그 백분위를 한 표에 놓으면 둘 다 뜻을 잃는다.
   ⇒ 그래서 **CSS만 공유**하고(`.cmp-*`) 데이터 경로는 이 파일이 따로 갖는다.

   ⛔ 여기서 새 지표를 만들지 않는다. 전부 export된 실측을 그대로 읽는다:
     `player_stats`(전 기간 집계) · `season_stats`(시즌·대회별) · `form`(경기별 평점) ·
     `fbref`(리그 백분위) · `avg_positions`(평균 위치) · `duties`(임무 수행 판정) · 커널 적합(map25).

   ⚠️ 신체 정보는 `cards.json`(fut.gg 카드)에서 온다 — 게임 데이터지만 **키·몸무게·생일·주발은
      실제 사람의 값**이라 여기 쓴다. 출처를 화면에 밝힌다. */

const esc = s => String(s ?? '').replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const num = v => (v == null || v === '' || Number.isNaN(Number(v)) ? null : Number(v));

/* ── 원천 조회 — 전부 「없으면 null」이다. ⛔ 0으로 대체하지 않는다(결손과 0은 다르다). ───────── */
const cardOf = (cards, pid) => {
  const list = (cards || {})[String(pid)] || [];
  return list.find(c => c.is_base) || list[0] || null;
};
const ageOf = c => {
  const b = c?.birthdate && Date.parse(c.birthdate);
  return b ? Math.floor((Date.now() - b) / 31557600000) : null;
};
/* ⛔⛔ **랭킹 라벨과 실측 맵의 키가 다르다**(2026-09-24 실측: 랭킹 `알리송(신규)` ↔ `td.fbref` 키 `알리송`).
   그대로 조회하면 신규 영입이 **조용히 「데이터 없음」**으로 떨어진다. data.js의 `playerKey`와 같은 규칙으로 정규화한다.
   ⭐ 그리고 **가능하면 라벨이 아니라 `player_id`로 찾는다** — 라벨은 표기 규약이 바뀌면 또 깨진다(불변규칙 6). */
const normKey = v => String(v ?? '').normalize('NFC')
  .replace(/^영입·/, '').replace(/\((합류확정|신규|보유)\)$/, '').trim();
const byLabel = (map, label) => {
  if (!map) return null;
  if (map[label]) return map[label];
  const want = normKey(label);
  const hit = Object.keys(map).find(k => normKey(k) === want);
  return hit ? map[hit] : null;
};
const statsOf = (td, pid) => (td.player_stats || []).find(r => r.player_id === pid) || null;
const avgPosOf = (td, pid) => (td.avg_positions || []).find(r => r.player_id === pid) || null;
const dutyOf = (td, pid) => (td.duties || []).filter(r => r.player_id === pid).slice(-1)[0] || null;
/* ⭐ 선수 특성(`fotmob_traits`) — **상세 백분위와 모집단이 다르다**(포지션군 전체 대비). 섞지 않고 따로 쓴다.
   출전이 얇아 상세 백분위가 아예 없는 선수에게는 이게 유일한 비교 축이다
   (실측 2026-09-24: 뇨니 PL 26/27 3경기 38분 → 상세 0행 · 특성 6축). */
const traitsOf = (td, pid) => (td.traits || {})[String(pid)] || [];

/* 최근 폼 — `form`은 [날짜, 평점, 대회] 배열이다(오름차순). 뒤에서 n경기. */
const formOf = (td, label, n = 5) => {
  const rows = byLabel(td.form, label) || [];
  const tail = rows.slice(-n).filter(r => num(r[1]) != null);
  if (!tail.length) return null;
  return { rows: tail, avg: tail.reduce((t, r) => t + Number(r[1]), 0) / tail.length, all: rows };
};

/* 시즌 성적 — 같은 시즌의 대회를 **합산**한다(평점은 분 가중). ⚠️ 친선은 뺀다(체제·강도가 다르다). */
const seasonOf = (td, label, season) => {
  const rows = (byLabel(td.season_stats, label) || [])
    .filter(r => r.season === season && !/friendly/i.test(r.competition || ''));
  if (!rows.length) return null;
  const s = { n: 0, starts: 0, minutes: 0, goals: 0, assists: 0, rw: 0, rm: 0 };
  for (const r of rows) {
    s.n += num(r.n) || 0; s.starts += num(r.starts) || 0; s.minutes += num(r.minutes) || 0;
    s.goals += num(r.goals) || 0; s.assists += num(r.assists) || 0;
    if (num(r.avg_rating) != null && num(r.minutes)) { s.rw += r.avg_rating * r.minutes; s.rm += r.minutes; }
  }
  s.avg_rating = s.rm ? s.rw / s.rm : null;
  return s;
};

/* 리그 백분위 — 같은 선수의 **최신 시즌·최신 수집분**만 남긴다(과거 스냅샷이 섞이면 비교가 깨진다). */
const pctRows = (td, label, pid) => {
  /* ⭐ 행마다 `player_id`가 있으므로 그걸로 모은다 — 라벨 키 표기와 무관해진다. 없으면 라벨로 물러선다. */
  const rows = Object.values(td.fbref || {}).flat().filter(r => r.player_id === pid);
  return rows.length ? rows : (byLabel(td.fbref, label) || []);
};
/* ⛔⛔ **두 선수의 시즌을 맞춘다**(2026-09-24). 각자 「최신 시즌」을 쓰면 26/27 백분위와 25/26 백분위를
   한 표에 올리게 되는데, 백분위는 **그 시즌 그 리그 안의 상대값**이라 시즌이 다르면 비교가 성립하지 않는다.
   ⇒ **양쪽에 다 있는 가장 최근 시즌**을 고르고, 공통 시즌이 없으면 각자 최신을 쓰되 **화면에 경고**한다. */
const commonSeason = (ra, rb) => {
  const sa = new Set(ra.map(r => r.season)), sb = new Set(rb.map(r => r.season));
  const both = [...sa].filter(x => sb.has(x)).sort();
  return both.length ? both[both.length - 1] : null;
};
const pctPick = (rows, season) => {
  const use = season || rows.reduce((m, r) => (r.season > m ? r.season : m), '');
  const out = {};
  for (const r of rows) {
    if (r.season !== use) continue;
    const prev = out[r.metric_key];
    if (!prev || r.pulled > prev.pulled) out[r.metric_key] = r;
  }
  return out;
};

/* ── 조각 ─────────────────────────────────────────────────────────────────── */
const row = (k, va, vb, opt = {}) => {
  if (va == null && vb == null) return '';
  const fmt = opt.fmt || (v => (v == null ? '—' : v));
  const hi = opt.lowerIsBetter ? -1 : 1;
  const d = ((va ?? 0) - (vb ?? 0)) * hi;
  const mag = Math.abs((va ?? 0) - (vb ?? 0));
  const show = opt.dfmt ? opt.dfmt(mag) : mag;
  const step = opt.big ? ' big' : opt.mid ? ' mid' : '';
  return `<tr${opt.grp ? ' class="big"' : ''}>
    <td class="cmp-a ${d > 0 ? 'win' : d < 0 ? 'lose' : ''}">${fmt(va)}</td>
    <td class="cmp-k">${esc(k)}${opt.sub ? `<i>${esc(opt.sub)}</i>` : ''}${
      d ? `<b class="cmp-d ${d > 0 ? 'dA' : 'dB'}${step}">${d > 0 ? '◀' : '▶'}${show}</b>` : ''}</td>
    <td class="cmp-b ${d < 0 ? 'win' : d > 0 ? 'lose' : ''}">${fmt(vb)}</td></tr>`;
};

/* 백분위 막대 — 0~100이라 길이가 곧 뜻이다. 좌우 색은 경기 분석 규약(왼쪽 주황 · 오른쪽 파랑). */
const pctRow = (kr, ra, rb) => {
  const pa = num(ra?.percentile_per90), pb = num(rb?.percentile_per90);
  if (pa == null && pb == null) return '';
  const d = (pa ?? 0) - (pb ?? 0);
  const bar = (p, side) => `<span class="rc-bar ${side}"><i style="width:${Math.max(0, Math.min(100, p ?? 0))}%"></i>
    <em>${p == null ? '—' : p}</em></span>`;
  const v = r => (num(r?.per90) == null ? '' : `<small class="dim">${Number(r.per90).toFixed(2)}</small>`);
  return `<tr><td class="cmp-a ${d > 0 ? 'win' : d < 0 ? 'lose' : ''}">${bar(pa, 'a')} ${v(ra)}</td>
    <td class="cmp-k">${esc(kr)}${d ? `<b class="cmp-d ${d > 0 ? 'dA' : 'dB'}${Math.abs(d) >= 30 ? ' big' : Math.abs(d) >= 15 ? ' mid' : ''}">${d > 0 ? '◀' : '▶'}${Math.abs(d)}</b>` : ''}</td>
    <td class="cmp-b ${d < 0 ? 'win' : d > 0 ? 'lose' : ''}">${bar(pb, 'b')} ${v(rb)}</td></tr>`;
};

/* 최근 폼 스파크라인 — 경기당 평점. ⚠️ 축을 5.5~8.5로 고정한다(자동 축이면 두 선수 눈금이 달라진다). */
const spark = (f, side) => {
  if (!f) return '<span class="dim">기록 없음</span>';
  const lo = 5.5, hi = 8.5, w = 108, h = 30;
  const pts = f.rows.map((r, i) => {
    const x = f.rows.length > 1 ? (i / (f.rows.length - 1)) * (w - 6) + 3 : w / 2;
    const y = h - 3 - ((Math.max(lo, Math.min(hi, r[1])) - lo) / (hi - lo)) * (h - 6);
    return `${x.toFixed(1)},${y.toFixed(1)}`;
  }).join(' ');
  const col = side === 'a' ? 'var(--viz-us)' : 'var(--viz-them)';
  return `<svg class="rc-spark" viewBox="0 0 ${w} ${h}" role="img"
      aria-label="최근 ${f.rows.length}경기 평점 추이">
      <polyline points="${pts}" fill="none" stroke="${col}" stroke-width="2"/>
      ${f.rows.map((r, i) => { const x = f.rows.length > 1 ? (i / (f.rows.length - 1)) * (w - 6) + 3 : w / 2;
        const y = h - 3 - ((Math.max(lo, Math.min(hi, r[1])) - lo) / (hi - lo)) * (h - 6);
        return `<circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="2" fill="${col}"><title>${esc(r[0])} ${r[1]} ${esc(r[2] || '')}</title></circle>`;
      }).join('')}</svg>
    <b>${f.avg.toFixed(2)}</b> <small class="dim">최근 ${f.rows.length}경기</small>`;
};

/* 임무 수행 — `duties.adherence`는 긴 산문이라 **머리의 등급 토큰만** 칩으로 쓰고 본문은 툴팁에 넣는다.
   ⛔ 등급을 여기서 다시 판정하지 않는다 — 원장이 쓴 토큰을 읽을 뿐이다. */
const dutyChip = d => {
  if (!d?.adherence) return '<span class="dim">판정 없음</span>';
  const g = (String(d.adherence).match(/HIGH|MEDIUM|MID|LOW/) || ['—'])[0];
  const cls = g === 'HIGH' ? 'hi' : g === 'LOW' ? 'mid' : 'mid';
  return `<span class="chip ${cls}" title="${esc(String(d.adherence).slice(0, 400))}">${esc(g)}</span>`;
};
const DUTY_RANK = { HIGH: 2, MEDIUM: 1, MID: 1, LOW: 0 };
const dutyRank = d => DUTY_RANK[(String(d?.adherence || '').match(/HIGH|MEDIUM|MID|LOW/) || [])[0]] ?? null;

/* ── 성향 묶음 ────────────────────────────────────────────────────────────
   ⭐⭐ **백분위는 이미 방향이 정규화돼 있다**(2026-09-24 실측으로 확인). 볼 뺏김·파울·경고·
   드리블 돌파 허용·피실점은 **값이 낮은 선수일수록 백분위가 높다**(AVL 전원 대조: 볼 뺏김 값 하위 4명
   평균 백분위 100 ↔ 상위 4명 4.5). ⇒ **백분위는 언제나 「높을수록 좋다」**라 그대로 평균 낼 수 있다.
   ⛔ 여기서 지표에 가중을 주지 않는다 — 묶음 안에서는 **단순 평균**이다. 가중을 주면 그 가중이 곧
      결론이 되는데 그걸 뒷받침할 근거가 없다(불변규칙 12).
   ⚠️ 묶음 구성(어느 지표가 어느 성향인가)은 **판단값**이다. 화면에 구성 지표를 다 적어 검증 가능하게 둔다. */
const GROUPS = [
  { key: '전진·창출', emery: 'buildup', tip: '하프스페이스 전진과 기회 창출 — 포지셔널 전진이 기대는 축',
    keys: ['chances_created', 'expected_assists', 'big_chance_created_team_title', 'line_breaking_passes',
           'crosses_succeeeded', 'touches_opp_box', 'assists'] },
  { key: '마무리', emery: 'role_demands', tip: '슛으로 끝내는 빈도와 질',
    keys: ['expected_goals', 'non_penalty_xg', 'shots', 'ShotsOnTarget', 'goals', 'expected_goals_on_target', 'headed_shots'] },
  { key: '볼 간수·연결', emery: 'buildup', tip: '패스 성공·터치·롱볼 정확도 · 볼 뺏김(적을수록 백분위 높음)',
    keys: ['successful_passes', 'successful_passes_accuracy', 'touches', 'long_balls_accurate',
           'long_ball_succeeeded_accuracy', 'dispossessed'] },
  { key: '회수·수비', emery: 'rest_defense', tip: '되찾기·차단·태클 — 잔류 수비 구조를 지탱하는 축',
    keys: ['recoveries', 'interceptions', 'matchstats.headers.tackles', 'defensive_actions',
           'poss_won_att_3rd_team_title', 'blocked_shots', 'clearances', 'dribbled_past'] },
  { key: '듀얼·공중', emery: 'set_pieces', tip: '몸싸움과 공중 — 세트피스 양면과 직결',
    keys: ['duel_won', 'duel_won_percent', 'aerials_won', 'aerials_won_percent', 'fouls_won'] },
  { key: '돌파', emery: 'traits', tip: '드리블로 라인을 깨는 빈도',
    keys: ['dribbles_succeeded', 'won_contest_subtitle'] },
  { key: '활동량·스프린트', emery: 'pressing', tip: '뛴 거리·스프린트·최고속도 — 미드블록 강도와 압박 가담의 물리적 바탕',
    keys: ['physical_metrics_distance_covered', 'physical_metrics_number_of_sprints',
           'physical_metrics_running', 'physical_metrics_sprinting', 'physical_metrics_topspeed'] },
];
const groupScore = (pct, g) => {
  const vals = g.keys.map(k => num(pct[k]?.percentile_per90)).filter(v => v != null);
  return vals.length >= 2 ? { v: vals.reduce((t, x) => t + x, 0) / vals.length, n: vals.length } : null;
};

/* 레이더 — 두 선수를 겹쳐 그린다. ⛔ 축은 0~100 백분위로 **고정**한다(자동 축이면 모양이 거짓말을 한다). */
function radar(gs, a, b) {
  const R = 84, cx = 150, cy = 108, n = gs.length;
  if (n < 3) return '';
  const pt = (i, r) => { const ang = -Math.PI / 2 + (i / n) * Math.PI * 2;
    return [cx + Math.cos(ang) * r, cy + Math.sin(ang) * r]; };
  const poly = side => gs.map((g, i) => { const s = g[side]; return pt(i, ((s?.v ?? 0) / 100) * R).map(v => v.toFixed(1)).join(','); }).join(' ');
  const web = [25, 50, 75, 100].map(p => `<polygon points="${gs.map((_, i) => pt(i, (p / 100) * R).map(v => v.toFixed(1)).join(',')).join(' ')}"
      fill="none" stroke="var(--line)" stroke-width="1"/>`).join('');
  const labels = gs.map((g, i) => { const [x, y] = pt(i, R + 20);
    return `<text x="${x.toFixed(1)}" y="${y.toFixed(1)}" text-anchor="middle" dominant-baseline="middle"
      font-size="9.5" fill="currentColor" opacity=".75">${esc(g.key)}</text>`; }).join('');
  return `<svg class="rc-radar" viewBox="0 0 300 216" role="img" aria-label="성향 백분위 레이더">
      ${web}${labels}
      <polygon points="${poly('a')}" fill="var(--viz-us)" fill-opacity=".22" stroke="var(--viz-us)" stroke-width="2"/>
      <polygon points="${poly('b')}" fill="var(--viz-them)" fill-opacity=".22" stroke="var(--viz-them)" stroke-width="2"/>
    </svg>
    <div class="dim" style="font-size:11.5px;text-align:center">
      <b class="wA">■ ${esc(a.label)}</b> &nbsp; <b class="wB">■ ${esc(b.label)}</b> — 바깥일수록 리그 상위(0~100 백분위)</div>`;
}

/* ── 해석 ──────────────────────────────────────────────────────────────────
   ⛔⛔ **「누가 낫다」를 만들지 않는다**(2026-09-24 사용자 지시 — 「내가 선수를 고르는 입장은 아니지만 …
   같은 위치에 기용되더라도 맡는 역할이 다를 수 있고 … 에메리의 전술과 선수를 더 잘 이해할 수 있는 메뉴」).
   ⇒ 이 블록이 답하는 질문은 **「이 선수를 쓰면 이 자리가 어떻게 달라지나」**다.
   기준선은 **그 팀 감독의 정본 슬롯 역할**(`slot_canon`)이고, 차이는 전부 실측 수치로 뒷받침한다.
   ⛔ 감독 이름은 `ctx.manager`로 받는다 — 화면에 박아 두면 다른 팀에서 거짓말이 된다(불변규칙 7).
   ⚠️ 문장은 **해석**이다 — 어느 수치에서 나왔는지 같은 줄에 적는다. 수치 없는 단정은 쓰지 않는다. */
const GAP = 15;                  // 성향 묶음이 「갈렸다」고 보는 백분위 차 (그 아래는 노이즈)
function interpret(a, b, ctx) {
  const { A, B, slot } = ctx;
  /* ⛔⛔ **감독을 하드코딩하지 않는다**(2026-09-24 실측: 첼시 화면에 「에메리」가 찍혔다 — 첼시는 알론소다).
     불변규칙 7(팀 축을 섞지 말 것)의 화면판이다. 이름은 그 팀의 regime에서 받는다. */
  const MG = ctx.manager || '감독';
  const gs = GROUPS.map(g => ({ ...g, a: groupScore(A.pct, g), b: groupScore(B.pct, g) }));
  const both = gs.filter(g => g.a && g.b);
  const split = both.filter(g => Math.abs(g.a.v - g.b.v) >= GAP)
    .sort((x, y) => Math.abs(y.a.v - y.b.v) - Math.abs(x.a.v - x.b.v));

  const side = (g) => (g.a.v > g.b.v ? a : b);
  const lines = [];

  // ① 기준 자리 — 슬롯군 비교면 **둘의 자리가 애초에 다를 수 있다**. 그게 첫 번째 해석이다.
  const roleTxt = c => `${ctx.roleName(c.role)}/${c.focus}`;
  const canonTxt = c => (c ? `${ctx.roleName(c.role_id)}/${c.focus}` : null);
  const cA = ctx.canonA, cB = ctx.canonB, sA = ctx.slotA, sB = ctx.slotB;
  if (ctx.groupMode && sA?.pos !== sB?.pos) {
    lines.push({ tag: '기준 자리', axis: 'formation',
      text: `같은 <b>${esc(ctx.groupLabel)}군</b>이지만 실측상 가장 잘 맞는 자리가 다르다 — `
        + `<b>${esc(a.label)}</b>는 <b>${esc(sA.pos)}</b>, <b>${esc(b.label)}</b>는 <b>${esc(sB.pos)}</b>. `
        + `${esc(MG)}의 이 묶음은 <b>좌우가 대칭이 아니라서</b> 자리마다 요구가 갈린다(${esc(sA.pos)} 정본 <b>${esc(canonTxt(cA) || '—')}</b> ↔ ${esc(sB.pos)} 정본 <b>${esc(canonTxt(cB) || '—')}</b>).`,
      why: `커널 sim ${a.sim?.toFixed(3)}(x=${sA.x}) ↔ ${b.sim?.toFixed(3)}(x=${sB.x}) — 각자 묶음 안에서 가장 높은 자리` });
  }
  // ② 각자 자기 자리의 정본과 얼마나 맞나
  const fits = (c, canon) => canon && c.role === canon.role_id && c.focus === canon.focus;
  if (cA || cB) {
    const fa = fits(a, cA), fb = fits(b, cB);
    const same = cA && cB && cA.pos === cB.pos;
    lines.push({ tag: '정본 역할', axis: 'slot_canon',
      text: same
        ? (fa === fb
            ? (fa ? `둘 다 실측 적합이 정본 <b>${esc(canonTxt(cA))}</b>과 같다 — 이 자리의 <b>임무는 바뀌지 않고</b>, 차이는 아래 성향에서만 난다.`
                  : `둘 다 실측 적합이 정본 <b>${esc(canonTxt(cA))}</b>과 다르다(${esc(roleTxt(a))} · ${esc(roleTxt(b))}) — 누구를 넣어도 이 자리는 정본에서 벗어난다.`)
            : `<b>${esc((fa ? a : b).label)}</b>는 정본 <b>${esc(canonTxt(cA))}</b>과 같고, <b>${esc((fa ? b : a).label)}</b>는 <b>${esc(roleTxt(fa ? b : a))}</b>로 갈린다 — 후자를 쓰면 이 자리의 임무 자체가 바뀐다.`)
        : `<b>${esc(a.label)}</b>(${esc(sA?.pos || '')}) 실측 <b>${esc(roleTxt(a))}</b> ↔ 정본 <b>${esc(canonTxt(cA) || '—')}</b>${fa ? ' <b>일치</b>' : ' <b>이탈</b>'} · `
          + `<b>${esc(b.label)}</b>(${esc(sB?.pos || '')}) 실측 <b>${esc(roleTxt(b))}</b> ↔ 정본 <b>${esc(canonTxt(cB) || '—')}</b>${fb ? ' <b>일치</b>' : ' <b>이탈</b>'}`,
      why: [cA?.rationale && `${sA.pos}: ${String(cA.rationale).slice(0, 150)}`,
            !same && cB?.rationale && `${sB.pos}: ${String(cB.rationale).slice(0, 150)}`].filter(Boolean).join(' / ') });
  }

  // ② 평균 위치 — 「같은 자리인데 팀 모양이 달라지는」 가장 직접적인 증거.
  const POS_MIN = 3;        // ⛔ 1~2경기 평균 위치로 「몇 칸 더 높다」를 단정하지 않는다(2026-09-24 실측에서 n=1이 나왔다)
  if (A.pos && B.pos) {
    const thin = (A.pos.n ?? 0) < POS_MIN || (B.pos.n ?? 0) < POS_MIN;
    const dx = (A.pos.avg_x ?? 0) - (B.pos.avg_x ?? 0), dy = (A.pos.avg_y ?? 0) - (B.pos.avg_y ?? 0);
    if (thin) {
      lines.push({ tag: '평균 위치', axis: '',
        text: `실측 표본이 얇아(<b>${A.pos.n}경기 ↔ ${B.pos.n}경기</b>) <b>위치 차이를 해석하지 않는다</b> — 아래 표에 값은 그대로 두었다.`,
        why: `해석 기준 ${POS_MIN}경기 이상` });
    } else if (Math.abs(dx) >= 3 || Math.abs(dy) >= 4) {
      const hi = dx > 0 ? a : b, wide = dy > 0 ? a : b;
      const bits = [];
      if (Math.abs(dx) >= 3) bits.push(`<b>${esc(hi.label)}</b>가 <b>${Math.abs(dx).toFixed(1)}칸 더 높다</b>`);
      if (Math.abs(dy) >= 4) bits.push(`좌우 중심이 <b>${Math.abs(dy).toFixed(1)}칸</b> 다르다(<b>${esc(wide.label)}</b> 쪽이 큼)`);
      lines.push({ tag: '평균 위치', axis: 'formation',
        text: `${bits.join(' · ')} — 같은 슬롯이라도 <b>팀 모양이 달라진다</b>. 풀백 전진(C2)·더블 피벗 잔류와 맞물리는 지점이다.`,
        why: `x ${A.pos.avg_x?.toFixed(1)}(${A.pos.n}경기) ↔ ${B.pos.avg_x?.toFixed(1)}(${B.pos.n}경기) · y ${A.pos.avg_y?.toFixed(1)} ↔ ${B.pos.avg_y?.toFixed(1)}` });
    }
  }

  // ③ 성향 — 갈린 묶음마다 한 줄. ⛔ 갈리지 않은 묶음은 문장을 만들지 않는다.
  for (const g of split.slice(0, 4)) {
    const w = side(g), l = w === a ? b : a;
    lines.push({ tag: g.key, axis: g.emery,
      text: `<b>${esc(w.label)}</b>가 이 축에서 앞선다(백분위 ${g.a.v.toFixed(0)} ↔ ${g.b.v.toFixed(0)}) — `
        + `<b>${esc(w.label)}</b>를 쓰면 이 자리가 <b>${esc(g.key)}</b> 쪽으로 기울고, <b>${esc(l.label)}</b>를 쓰면 그 부담이 다른 자리로 옮겨간다.`,
      why: `${esc(g.tip)} · 지표 ${g.a.n}/${g.b.n}개 평균` });
  }
  if (!split.length && both.length)
    lines.push({ tag: '성향', axis: '', text: `성향 ${both.length}묶음 중 <b>${GAP}백분위 이상 갈린 축이 없다</b> — 둘은 이 자리를 <b>비슷한 방식으로</b> 수행한다.`, why: '' });

  // ④ 임무 수행 — 원장이 실측으로 쓴 판정.
  const ga = (String(A.duty?.adherence || '').match(/HIGH|MEDIUM|MID|LOW/) || [])[0];
  const gb = (String(B.duty?.adherence || '').match(/HIGH|MEDIUM|MID|LOW/) || [])[0];
  if (ga && gb && ga !== gb)
    lines.push({ tag: '임무 수행', axis: 'role_demands',
      text: `원장 판정이 <b>${esc(ga)} ↔ ${esc(gb)}</b>로 갈린다 — ${esc(MG)}가 이 자리에 요구하는 임무를 두 선수가 <b>같은 정도로 수행하지 않았다</b>는 실측 기록이다.`,
      why: '칩에 마우스를 올리면 판정 근거 전문이 나온다' });

  const axisNote = ax => {
    const p = (ctx.profile || []).find(r => r.axis === ax);
    return p ? `<span class="chip dim" title="${esc(String(p.content).slice(0, 500))}">${esc(MG)} ${esc(ax)}<i>?</i></span>` : '';
  };
  return `<h4>이 자리가 어떻게 달라지나 <small class="dim">— 우열이 아니라 <b>해석</b>이다</small></h4>
    <div class="cmp-verdict">
      ${(cA || cB) ? `<div class="cmp-vhead">
        ${cA ? `<b>${esc(sA?.pos || '')} 정본</b> <span class="dim">${esc(canonTxt(cA))}</span>` : ''}
        ${cB && cB.pos !== cA?.pos ? `<b style="margin-left:10px">${esc(sB?.pos || '')} 정본</b> <span class="dim">${esc(canonTxt(cB))}</span>` : ''}
        <span class="dim" style="flex-basis:100%;font-size:11px">${esc(MG)} 재현의 기준선(slot_canon) — 두 선수는 각자 자기 자리의 기준선에서 얼마나 벗어나는가</span></div>` : ''}
      <ul class="rc-read">${lines.map(l => `<li><span class="chip">${esc(l.tag)}</span> ${l.text}
        ${l.why ? `<br><small class="dim">${l.why}</small>` : ''} ${axisNote(l.axis)}</li>`).join('')}</ul>
      <p class="dim" style="font-size:11px;margin:8px 0 0">
        <b>이 블록은 「누가 낫다」를 말하지 않는다.</b> 같은 자리에 서도 두 선수가 맡는 임무·서는 높이·기대는 강점이 다르고,
        그 차이가 곧 <b>팀 전술의 차이</b>다. 그래서 답은 순위가 아니라 <b>「이 선수를 쓰면 이 자리가 이렇게 바뀐다」</b>이다.<br>
        기준선은 <b>${esc(MG)} 정본 슬롯 역할</b>(slot_canon)이고, 문장마다 <b>어느 실측에서 나왔는지</b>를 같은 줄에 적었다.
        「${esc(MG)} ○○」 칩에 마우스를 올리면 그 전술 축의 원장 서술이 나온다.<br>
        ⚠️ 성향 묶음(어느 지표가 어느 성향인가)은 <b>판단값</b>이다 — 구성 지표는 아래 표에 다 있으니 직접 검증할 수 있다.
        묶음 안에서는 <b>가중 없이 단순 평균</b>한다.<br>
        ⛔ 여기에 없는 것: 상대 팀·경기 맥락·부상·조합. 실측 표에 없는 축이다.</p>
    </div>
    <h4>성향 프로파일 <small class="dim">— 리그 백분위 묶음 평균(0~100)</small></h4>
    ${radar(both, a, b)}
    <table class="tbl cmp-tbl"><tbody>
      ${gs.map(g => g.a && g.b
        ? row(g.key, Math.round(g.a.v), Math.round(g.b.v), { sub: `${g.a.n}/${g.b.n}개 지표`, mid: Math.abs(g.a.v - g.b.v) >= GAP })
        : `<tr><td class="cmp-a dim">${g.a ? Math.round(g.a.v) : '—'}</td>
             <td class="cmp-k">${esc(g.key)}<i>${!Object.keys(A.pct).length || !Object.keys(B.pct).length
               ? '한쪽에 리그 백분위 수집분이 없다' : '공통 지표 2개 미만'}</i></td>
             <td class="cmp-b dim">${g.b ? Math.round(g.b.v) : '—'}</td></tr>`).join('')}
    </tbody></table>`;
}

/* ── 본체 ─────────────────────────────────────────────────────────────────── */
export function compareReal(a, b, ctx) {
  if (!a || !b) return '';
  const { td, cards, miniGrid } = ctx;
  const pack = c => ({
    card: cardOf(cards, c.player_id), stats: statsOf(td, c.player_id),
    form: formOf(td, c.label), season: seasonOf(td, c.label, ctx.seasonKey),
    praw: pctRows(td, c.label, c.player_id), traits: traitsOf(td, c.player_id), pos: avgPosOf(td, c.player_id), duty: dutyOf(td, c.player_id),
  });
  const A = pack(a), B = pack(b);
  const season = commonSeason(A.praw, B.praw);
  A.pct = pctPick(A.praw, season); B.pct = pctPick(B.praw, season);
  const seasonWarn = !season && A.praw.length && B.praw.length;
  const C = { ...ctx, A, B };

  const head = (c, P, side) => `<div class="cmp-card ${side}">
      ${P.card?.simple_card_url ? `<img src="${esc(P.card.simple_card_url)}" alt="">` : ''}
      <b>${esc(c.label)}</b>
      <span class="dim">${esc(P.card?.positions || c.pos_only || '')}</span>
      <span class="dim">${[ageOf(P.card) != null ? `${ageOf(P.card)}세` : null,
                           P.card?.height_cm ? `${P.card.height_cm}cm` : null,
                           P.card?.weight_kg ? `${P.card.weight_kg}kg` : null].filter(Boolean).join(' · ') || '신체 정보 없음'}</span>
      <span class="dim">${[P.card?.preferred_foot ? `${P.card.preferred_foot}발` : null,
                           P.card?.nation].filter(Boolean).join(' · ')}</span></div>`;

  const sa = A.stats, sb = B.stats;
  const s2 = (v) => (v == null ? null : Number(v));
  const aggRows = sa || sb ? [
    row('경기', s2(sa?.n), s2(sb?.n)),
    row('출전 시간', s2(sa?.minutes), s2(sb?.minutes), { sub: '분' }),
    row('평균 평점', s2(sa?.avg_rating), s2(sb?.avg_rating), { grp: true, fmt: v => (v == null ? '—' : v.toFixed(2)), dfmt: m => m.toFixed(2) }),
    row('xG', s2(sa?.xg_pg), s2(sb?.xg_pg), { sub: '경기당', fmt: v => (v == null ? '—' : v.toFixed(3)), dfmt: m => m.toFixed(3) }),
    row('xA', s2(sa?.xa_pg), s2(sb?.xa_pg), { sub: '경기당', fmt: v => (v == null ? '—' : v.toFixed(3)), dfmt: m => m.toFixed(3) }),
    row('키패스', s2(sa?.kp_pg), s2(sb?.kp_pg), { sub: '경기당', fmt: v => (v == null ? '—' : v.toFixed(2)), dfmt: m => m.toFixed(2) }),
    row('태클', s2(sa?.tk_pg), s2(sb?.tk_pg), { sub: '경기당', fmt: v => (v == null ? '—' : v.toFixed(2)), dfmt: m => m.toFixed(2) }),
    row('인터셉트', s2(sa?.ic_pg), s2(sb?.ic_pg), { sub: '경기당', fmt: v => (v == null ? '—' : v.toFixed(2)), dfmt: m => m.toFixed(2) }),
    row('듀얼 승', s2(sa?.dw_pg), s2(sb?.dw_pg), { sub: '경기당', fmt: v => (v == null ? '—' : v.toFixed(2)), dfmt: m => m.toFixed(2) }),
  ].join('') : '';

  const ss = A.season, sz = B.season;
  const seasonRows = ss || sz ? [
    row('경기', ss?.n, sz?.n), row('선발', ss?.starts, sz?.starts),
    row('출전 시간', ss?.minutes, sz?.minutes, { sub: '분' }),
    row('골', ss?.goals, sz?.goals, { grp: true }), row('도움', ss?.assists, sz?.assists, { grp: true }),
    row('평균 평점', ss?.avg_rating, sz?.avg_rating, { fmt: v => (v == null ? '—' : v.toFixed(2)), dfmt: m => m.toFixed(2), sub: '분 가중' }),
  ].join('') : '';

  /* 백분위 — 공통 지표를 **차이 큰 순**으로 세운다. 다 보여주면 눈이 흐려지므로 12개 + 펼치기. */
  const com = Object.keys(A.pct).filter(k => B.pct[k])
    .map(k => ({ k, kr: A.pct[k].metric_kr || A.pct[k].metric,
                 d: Math.abs((num(A.pct[k].percentile_per90) ?? 0) - (num(B.pct[k].percentile_per90) ?? 0)) }))
    .sort((x, y) => y.d - x.d);
  const pctTop = com.slice(0, 12).map(m => pctRow(m.kr, A.pct[m.k], B.pct[m.k])).join('');
  const pctRest = com.slice(12).map(m => pctRow(m.kr, A.pct[m.k], B.pct[m.k])).join('');
  const pctSeason = season || A.pct[com[0]?.k]?.season;

  const posCell = P => (P.pos ? `x ${P.pos.avg_x?.toFixed(1)} · y ${P.pos.avg_y?.toFixed(1)} <small class="dim">${P.pos.n}경기</small>`
    : '<span class="dim">없음</span>');

  return `<div class="cmp-head">${head(a, A, 'sA')}<span class="cmp-vs">vs</span>${head(b, B, 'sB')}</div>
    <p class="dim" style="font-size:11.5px;margin:8px 0">⛔ 여기 숫자는 전부 <b>실축 실측</b>이다 — 게임 카드 스탯이 아니다.
      신체 정보만 fut.gg 카드에서 왔다(키·몸무게·생일·주발은 실제 값).</p>

    ${interpret(a, b, C)}

    <h4>${ctx.groupMode ? `${esc(ctx.groupLabel)}군 적합` : `${esc(ctx.slot.pos)} 슬롯 적합`}
      <small class="dim">${ctx.groupMode
        ? '— 각자 <b>가장 잘 맞는 자리</b>의 커널 값이다(좌우 자리는 커널 x가 달라 sim이 갈린다)'
        : `— 커널 x=${ctx.slot.x} · ${esc(ctx.slot.slot_type)}군`}</small></h4>
    <table class="tbl cmp-tbl"><tbody>
      ${ctx.groupMode ? `<tr><td class="cmp-a"><b>${esc(ctx.slotA?.pos || '')}</b> <small class="dim">x=${ctx.slotA?.x}</small></td>
        <td class="cmp-k">기준 자리<i>묶음 안 최적</i></td>
        <td class="cmp-b"><b>${esc(ctx.slotB?.pos || '')}</b> <small class="dim">x=${ctx.slotB?.x}</small></td></tr>` : ''}
      ${row('적합 sim', a.sim, b.sim, { grp: true, fmt: v => (v == null ? '—' : v.toFixed(3)), dfmt: m => m.toFixed(3) })}
      <tr><td class="cmp-a">${esc(ctx.roleName(a.role))}/${esc(a.focus)}</td><td class="cmp-k">적합 역할·포커스</td>
          <td class="cmp-b">${esc(ctx.roleName(b.role))}/${esc(b.focus)}</td></tr>
      <tr><td class="cmp-a">${posCell(A)}</td><td class="cmp-k">평균 위치<i>실측 좌표</i></td><td class="cmp-b">${posCell(B)}</td></tr>
    </tbody></table>
    <div class="cmp-two" style="margin-top:6px">
      <div>${miniGrid(a.map25)}<br><small class="dim">${esc(a.note || '')}</small></div>
      <div>${miniGrid(b.map25)}<br><small class="dim">${esc(b.note || '')}</small></div></div>

    <h4>최근 폼 <small class="dim">— 경기별 평점(축 5.5~8.5 고정)</small></h4>
    <div class="cmp-two"><div>${spark(A.form, 'a')}</div><div>${spark(B.form, 'b')}</div></div>

    ${aggRows ? `<h4>전 기간 실측 집계 <small class="dim">— player_stats(전 대회 누적)</small></h4>
      <table class="tbl cmp-tbl"><tbody>${aggRows}</tbody></table>` : ''}

    ${seasonRows ? `<h4>${esc(ctx.seasonKey)} 시즌 <small class="dim">— 대회 합산 · 친선 제외</small></h4>
      <table class="tbl cmp-tbl"><tbody>${seasonRows}</tbody></table>` : ''}

    ${pctTop ? `<h4>리그 백분위 <small class="dim">— fbref ${seasonWarn ? '<b>시즌 혼합</b>' : esc(pctSeason || '')} · 90분당 · 같은 포지션 대비</small></h4>
      ${seasonWarn ? `<p class="dim" style="font-size:12px;margin:2px 0 6px">⛔ <b>공통 시즌이 없다</b> —
        ${esc(A.praw[0]?.season || '')} ↔ ${esc(B.praw[0]?.season || '')}로 각자 최신 시즌을 썼다.
        백분위는 <b>그 시즌 그 리그 안의 상대값</b>이라 시즌이 다르면 <b>직접 비교가 성립하지 않는다</b> — 경향으로만 읽을 것.</p>` : ''}
      <p class="dim" style="font-size:11.5px;margin:2px 0 6px">막대 길이 = <b>백분위</b>(100이 리그 최상위) · 막대 옆 작은 수 = 90분당 원값.
        ⭐ <b>포지션 대비 값</b>이라 역할이 다른 둘을 견주기에 이 축이 가장 공정하다. 차이 큰 순으로 세웠다.</p>
      <table class="tbl cmp-tbl"><tbody>${pctTop}</tbody></table>
      ${pctRest ? `<details style="margin-top:6px"><summary class="dim" style="font-size:12px;cursor:pointer">나머지 ${com.length - 12}개 지표 펼치기</summary>
        <table class="tbl cmp-tbl"><tbody>${pctRest}</tbody></table></details>` : ''}`
      : '<h4>리그 백분위</h4><p class="dim">두 선수의 공통 백분위 지표가 없다 — 수집 범위가 다르다.</p>'}

    ${(() => {
      /* 선수 특성 — 양쪽 다 있을 때만 그린다. ⛔ 위 「리그 백분위」와 **같은 표에 올리지 않는다**(모집단이 다르다). */
      const ta = Object.fromEntries(A.traits.map(t => [t.metric, t]));
      const tb = Object.fromEntries(B.traits.map(t => [t.metric, t]));
      const keys = Object.keys(ta).filter(k => tb[k]);
      if (!keys.length) return '';
      const thin = !Object.keys(A.pct).length || !Object.keys(B.pct).length;
      return `<h4>선수 특성 <small class="dim">— FotMob · ${esc(A.traits[0]?.pos_group || '')}</small></h4>
        <p class="dim" style="font-size:11.5px;margin:2px 0 6px">
          ${thin ? '⭐ <b>한쪽에 리그 백분위가 없어 이 축이 대신 선다.</b> 출전이 얇으면 FotMob이 상세 백분위를 만들지 않는다. ' : ''}
          ⛔ 위 「리그 백분위」와 <b>모집단이 다르다</b>(이쪽은 포지션군 전체 대비) — <b>같은 표로 읽지 말 것</b>.
          수집일 ${esc(A.traits[0]?.pulled || '')} ↔ ${esc(B.traits[0]?.pulled || '')}.</p>
        <table class="tbl cmp-tbl"><tbody>${keys
          .map(k => ({ k, kr: ta[k].metric_kr || k, d: Math.abs((ta[k].percentile ?? 0) - (tb[k].percentile ?? 0)) }))
          .sort((x, y) => y.d - x.d)
          .map(m => pctRow(m.kr, { percentile_per90: ta[m.k].percentile }, { percentile_per90: tb[m.k].percentile }))
          .join('')}</tbody></table>`;
    })()}

    <h4>임무 수행 <small class="dim">— duties(원장 판정 · 칩에 마우스를 올리면 근거)</small></h4>
    <div class="cmp-two"><div>${dutyChip(A.duty)}</div><div>${dutyChip(B.duty)}</div></div>
`;
}
