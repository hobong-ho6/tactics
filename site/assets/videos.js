/* 영상 분석 카드·목록 — 경기 분석·팀 리포트·선수 페이지의 단일 정본 (2026-10-28 · match-report.html에서 이관).
   ⛔ 화면마다 카드를 다시 짜지 않는다 — 세 화면이 이 모듈을 import한다(불변규칙 13 ② 단일 정본).
   데이터는 data/videos.json(core/export.py) — `all`(영상 전부) · `by_report`(경기 귀속) · `issues`(판정 쟁점). */
import { annotate, glTip } from './glossary.js';
import { roleLabel, focusLabel, claimLabel, humanize, VERDICT_KR, AXIS_KR } from './labels.js';
import { prose } from './prose.js';

const esc = value => String(value ?? '').replace(/[&<>"']/g, c =>
  ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));

/** data/videos.json — 없으면 null(구버전 데이터 호환) */
export const loadVideos = () => fetch(`data/videos.json?t=${Date.now()}`, { cache: 'no-store' })
  .then(r => r.ok ? r.json() : null).catch(() => null);

/* ── 이 경기 영상 분석 (2026-09-15, 사용자 지시 「UTV·The Villans 주요 내용을 우리 페이지에서」) ──
   세 층을 그대로 보여준다: 요약(사람) · 핵심 포인트(사람) · 관찰 기록(검증된 obs 원문).
   ⛔ 요약이 없는 영상도 숨기지 않는다 — 「요약 없음」과 「내용 없음」은 다르다(메타·obs는 그대로 쓸모 있다). */
const bold = t => t.replace(/\*\*([^*]+)\*\*/g, '<b>$1</b>');
export const VKIND = { 감독회견:'hi', 전술분석:'hi', 경기반응:'', 선수스카우팅:'mid', 상대팀:'mid', 프리시즌:'mid' };
export function renderVideoList(el, rows, { empty = '<p class="dim">영상 없음</p>', newestFirst = false, title = '영상 분석' } = {}){
  if (!rows.length){ el.innerHTML = empty; return; }
  const withSummary = rows.filter(v => v.summary).length;
  /* ⭐⭐ 감독 회견을 맨 위 별도 영역으로, 나머지는 **정보 등급** 순으로 배치한다
     (2026-09-22 사용자 지시 「감독회견은 중요하니 상단에 별도 영역 · 유용한 정보는 등급을 매겨 높은 것을 위로」).
     ⛔ 등급은 **원장 값으로만 계산한다** — 산문을 읽고 점수를 매기지 않는다:
        A = 구현에 **반영된**(APPLIED) 주장이 있다 · B = 유지(HELD)·판정 대기(PENDING) 주장이 있다
        C = 읽었고 **주장 없음**(axis='none') · D = 요약 미작성(전사만 있다)
     ⚠️ 등급은 「이 영상이 우리 구현을 얼마나 움직였나」이지 영상의 품질 평가가 아니다. */
  const gradeOf = v => {
    if (!v.summary) return 'D';
    const cs = v.impl_claims ?? [];
    if (cs.some(c => c.verdict === 'APPLIED')) return 'A';
    if (cs.some(c => c.verdict === 'HELD' || c.verdict === 'PENDING')) return 'B';
    return 'C';
  };
  const GRADE_WHY = {
    A: '구현에 반영된(APPLIED) 주장이 있다',
    B: '유지(HELD)·판정 대기(PENDING) 주장이 있다',
    C: '전사를 읽었고 구현에 닿는 주장이 없다',
    D: '요약 미작성 — 전사만 확보',
  };
  const RANK = { A: 0, B: 1, C: 2, D: 3 };
  const pressers = rows.filter(v => v.kind === '감독회견');
  const others = rows.filter(v => v.kind !== '감독회견')
    .map(v => ({ v, g: gradeOf(v) }))
    .sort((a, b) => RANK[a.g] - RANK[b.g]
      || (b.v.impl_claims ?? []).length - (a.v.impl_claims ?? []).length
      || (newestFirst ? -1 : 1) * String(a.v.published ?? '').localeCompare(String(b.v.published ?? '')));

  /* ⭐⭐ 2026-10-20 사용자 지시 「영상 분석 영역도 글이 너무 많아서 좀 더 잘 보이게」 — 40편이 큰 카드로 줄줄이 나왔다.
     ⇒ ⑴ 머리에 요약 작성/미작성·종류별 칩 집계 ⑵ 요약 있는 영상만 카드(핵심 한 줄 + 구현 주장 배지 · 전문은 펼치기)
        ⑶ 요약 미작성은 채널·제목·날짜 한 줄 목록으로 접는다(「요약 미작성」 문장을 카드마다 반복하지 않는다).
     ⛔ 숨기지 않는다 — 미작성도 건수와 목록이 그대로 있다. */
  const oneLine = v => { const k = (v.key_points || [])[0]; if (k) return k;
    const t = String(v.summary || '').replace(/\s+/g, ' ').trim(); const m = t.match(/^.*?[.!?。](\s|$)/); return (m ? m[0] : t).slice(0, 160); };
  const claimBadges = v => { const cs = v.impl_claims ?? []; if (!cs.length) return '';
    const c = cs.reduce((m, x) => (m[x.verdict] = (m[x.verdict] || 0) + 1, m), {});
    return Object.entries(c).map(([k, n]) => `<span class="badge ${VERDICT_CLS[k] ?? ''}" title="구현 주장 ${esc(VERDICT_KR[k] ?? k)}">${esc(VERDICT_KR[k] ?? k)} ${n}</span>`).join(' '); };
  const head = (v, g) => `${g ? `<span class="badge vgrade v${g}" title="${esc(GRADE_WHY[g])}">${g}</span>` : ''}
        <span class="badge ${VKIND[v.kind] ?? ''}">${esc(v.kind ?? '미분류')}</span>
        <b>${esc(v.channel)}</b> <span class="dim">${esc(v.published ?? '게시일 미기재')}${v.published_approx ? '경' : ''}</span>
        <a href="${esc(v.url)}" target="_blank" rel="noopener">유튜브 ↗</a>`;
  const card = (v, g) => `<article class="vidcard${g ? ' g' + g : ' presser'}">
      <header>${head(v, g)} ${claimBadges(v)}</header>
      <div class="vidtitle">${esc(v.title ?? '(제목 미기재)')}</div>
      <div class="vidone">${annotate(bold(esc(oneLine(v))))}</div>
      <details class="vidmore"><summary>요약 전문${v.key_points.length ? ` · 핵심 ${v.key_points.length}` : ''}${v.obs_points.length ? ` · 관찰 기록 ${v.obs_points.length}` : ''}${(v.impl_claims ?? []).length ? ` · 구현 주장 ${(v.impl_claims ?? []).length}` : ''}</summary>
        ${v.summary ? `<div class="vidsum">${prose(v.summary)}</div>` : ''}
        ${v.key_points.length ? `<ul class="vidpoints">${v.key_points.map(x => `<li>${annotate(bold(esc(x)))}</li>`).join('')}</ul>` : ''}
        ${v.obs_points.length ? v.obs_points.map(o => `<div class="kv" style="margin-top:6px"><b>관측 기록 #${o.id}</b> <span class="dim">${esc(o.scope)}</span></div>${prose(o.claim)}`).join('') : ''}
        ${claimsHtml(v)}</details>
    </article>`;
  const row = v => `<li><span class="badge ${VKIND[v.kind] ?? ''}">${esc(v.kind ?? '미분류')}</span>
      <b>${esc(v.channel)}</b> <a href="${esc(v.url)}" target="_blank" rel="noopener">${esc(v.title ?? '(제목 미기재)')}</a>
      <span class="dim">${esc(v.published ?? '')}</span></li>`;
  const kinds = rows.reduce((m, v) => (m[v.kind || '미분류'] = (m[v.kind || '미분류'] || 0) + 1, m), {});
  const done = rows.filter(v => v.summary), todo = rows.filter(v => !v.summary);
  const sec = (title, note, list) => list.length ? `<section class="vsec"><h3>${title} <small class="dim">${note}</small></h3>${list}</section>` : '';
  const pDone = pressers.filter(v => v.summary), oDone = others.filter(x => x.v.summary);
  el.innerHTML =
    `<div class="vidhead"><b>${rows.length}편</b>
       <span class="vidbar" title="요약 작성 ${withSummary} · 미작성 ${rows.length - withSummary}"><i style="flex:${withSummary}"></i><i class="todo" style="flex:${rows.length - withSummary}"></i></span>
       <small>요약 작성 <b>${withSummary}</b> · 미작성 <b>${rows.length - withSummary}</b></small>
       <span class="vidkinds">${Object.entries(kinds).sort((a, b) => b[1] - a[1]).map(([k, n]) => `<span class="badge ${VKIND[k] ?? ''}">${esc(k)} ${n}</span>`).join(' ')}</span></div>`
    + (pressers.length ? `<section class="vsec presserbox"><h3>🗣️ 감독 회견 <small class="dim">${pressers.length}편 — 1차 발언이라 가장 세다</small></h3>
        ${pDone.map(v => card(v, null)).join('')}
        ${pressers.length > pDone.length ? `<ul class="vidlist">${pressers.filter(v => !v.summary).map(row).join('')}</ul>` : ''}</section>` : '')
    + sec(title, `요약 있는 ${oDone.length}편 — 정보 등급順 · <b class="badge vgrade vA">A</b> 구현 반영 <b class="badge vgrade vB">B</b> 유지·판정 대기 <b class="badge vgrade vC">C</b> 주장 없음`,
          oDone.map(x => card(x.v, x.g)).join(''))
    + (todo.filter(v => v.kind !== '감독회견').length ? `<details class="vsec vidtodo"><summary><b>요약 미작성 ${todo.filter(v => v.kind !== '감독회견').length}편</b> <small class="dim">— 전사는 확보돼 있다 · 채널·제목·날짜만</small></summary>
        <ul class="vidlist">${todo.filter(v => v.kind !== '감독회견').map(row).join('')}</ul></details>` : '');
}
/* 구현 주장 — 「이 영상이 우리 구현의 무엇을 건드리는가」(docs/30 8단계 · migration 033).
   ⛔ 요약 산문에서 추출하지 않는다 — `video_impl_claims` 행을 그대로 그린다.
   ⭐ axis='none'(읽었고 주장 없음)과 빈 배열(아직 미작성)을 다르게 보여준다. */
export const VERDICT_CLS = { APPLIED:'hi', REJECTED:'', HELD:'mid', PENDING:'mid', NA:'' };
/* 코드값은 읽는 말로(labels.js) — 원문은 hover(title)에 남는다 */
export function claimTarget(c){
  if (c.axis === 'role')  return `${esc(c.player ?? '?')} → ${roleLabel(c.role_id, c.focus)}`;
  if (c.axis === 'focus') return `${esc(c.player ?? '?')} → 포커스 ${focusLabel(c.focus)}`;
  if (c.axis === 'none')  return '<span class="dim">전사를 읽었고 구현에 닿는 주장이 없다</span>';
  /* ⭐ 한국어 칸 우선(migration 112) — 원문 field·value는 툴팁. 없으면 종전 claimLabel(정형 코드 표). */
  /* ⭐ 긴 주장은 「헤드라인 + 요점」으로 읽힌다(migration 113 · 규칙 정본 core/claims.py · NN/g 결론 먼저·덩어리·점진 공개).
     한국어 전문(value_kr)과 영문 원문은 툴팁으로 — 지우지 않는다. */
  const pts = (() => { try { return c.points_kr ? JSON.parse(c.points_kr) : null; } catch (e) { return null; } })();
  const tip = `${c.value_kr ? '전문: ' + c.value_kr + '\n' : ''}원문: ${c.field ?? ''}${c.value ? ' = ' + c.value : ''}`;
  const body = c.field_kr && c.headline_kr
    ? glTip(`<b>${esc(c.field_kr)} · ${esc(c.headline_kr)}</b>`, tip)
      + (pts?.length ? `<ul class="claimpts">${pts.map(p => `<li>${esc(p)}</li>`).join('')}</ul>` : '')
    : c.field_kr ? glTip(`<b>${esc(c.field_kr)}</b>${c.value_kr ? `: ${esc(c.value_kr)}` : ''}`, tip)
    : claimLabel(c.field, c.value);
  return `${c.team_code ? esc(c.team_code) + ' ' : ''}${c.player ? esc(c.player) + ' ' : ''}${body}`;
}
/* ⭐ 판정 쟁점(migration 114) — 판정 대기 주장은 「무엇이 차면 판정하나 · 지금 몇/몇」을 붙인다.
   같은 쟁점의 주장은 여러 영상에 흩어져 있어도 한 번 판정으로 같이 닫힌다(scripts/claim_issues.py --close). */
export function issueLine(c){
  const i = c.issue; if (!i) return '';
  /* ⭐ 감시(watch, migration 115) — 정본 유지로 판정한 뒤 재판정 조건이 트리거로 걸려 있다 */
  const watch = i.phase === 'watch';
  const st = i.status === 'closed' ? `판정 완료 ${esc(i.closed ?? '')}`
           : i.hold ? '수집 보류 중'
           : watch ? (i.due ? '⭐ 재판정할 차례' : '유지 · 재판정 조건 감시 중')
           : i.due ? '⭐ 판정할 차례' : '판정 시점 대기';
  return `<div class="claimissue dim" style="font-size:12px;margin-top:2px">${watch ? '🔁' : '⏳'} 쟁점 #${i.id} 「${esc(i.title)}」 — ${watch ? '재판정 조건 ' : ''}${esc(i.trigger)} · <b>${st}</b></div>`;
}
export function claimsHtml(v){
  const cs = v.impl_claims ?? [];
  if (!cs.length){
    return v.summary
      ? '<p class="dim" style="font-size:12px;margin:6px 0 0">⏰ 구현 주장 미작성 — 요약은 있으나 어느 축을 건드리는지 아직 정형화되지 않았다(G17이 건수로 보고).</p>'
      : '';
  }
  return `<div class="vidclaims"><div class="kv" style="margin-bottom:4px"><b>이 영상이 게임 구현에 말하는 것 ${cs.length}건</b>
      <small class="dim">— 실측(히트맵·커널)이 판정하지 못하는 축은 영상·회견이 결정한다</small></div>`
    + cs.map(c => `<div class="vidclaim">
        <span class="badge ${VERDICT_CLS[c.verdict] ?? ''}" title="${esc(c.verdict)}">${esc(VERDICT_KR[c.verdict] ?? c.verdict)}</span>
        <span class="claimaxis">${esc(AXIS_KR[c.axis] ?? c.axis)}</span>
        <span class="claimtgt">${claimTarget(c)}</span>
        ${issueLine(c)}
        ${c.quote ? `<div class="claimquote">${annotate(bold(esc(c.quote)))}</div>` : ''}
        ${c.verdict_note ? `<details class="claimnote"><summary style="cursor:pointer;font-size:12px;color:var(--dim)">판정 메모 — 왜 이 판정인가</summary>${annotate(humanize(bold(esc(c.verdict_note))))}</details>` : ''}
      </div>`).join('') + '</div>';
}

