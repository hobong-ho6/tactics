/* 데이터 로더 + 팀 상태. 모든 페이지가 공유한다.
   데이터는 site/data/*.json (scripts/export.py 산출물) — 손편집 금지. */

import { onSchemeChange } from './tokens.js';
import { setPlaystyleAliases } from './playstyle-icons.js';

const BASE = new URL('.', import.meta.url).href.replace(/assets\/$/, '');

async function j(path){
  // Generated JSON is a live projection of db/tactics.db. `no-store` plus a
  // unique URL also bypasses browsers/CDNs that ignore revalidation headers.
  const url = new URL('data/' + path, BASE);
  url.searchParams.set('_', Date.now().toString());
  const r = await fetch(url, { cache: 'no-store' });
  if (!r.ok) throw new Error(`${path} 로드 실패 (${r.status})`);
  return r.json();
}

/* ⭐ index.json을 읽을 때 PlayStyle 별칭 표(fc_playstyle_aliases → export `playstyle_aliases`)를 playstyle-icons.js에 주입한다 —
   화면이 옛 이름(Rush Out)을 공식 이름(1v1 Close Down)으로 푸는 길은 psLookup/psCanon 한 곳뿐이다(2026-10-22 · migration 121). */
export const loadIndex   = async () => { const idx = await j('index.json'); setPlaystyleAliases(idx.playstyle_aliases?.current || null); return idx; };
export const loadTeam    = code => j(`teams/${code}.json`);
export const loadKernels = gv => j(`kernels/${gv}.json`);
/* ⭐ 현행 게임 버전 — index.json의 game_versions.released로 정한다(core/game_version.current와 같은 규칙 · 2026-10-22).
   ⛔ 화면이 'FC26'/'FC27'을 「현행」이라는 뜻으로 박지 않는다(G22가 막는다). 특정 버전 비교는 loadKernels(gv)로. */
let _gvCache = null;
export async function currentGameVersion(){
  if (_gvCache) return _gvCache;
  const idx = await loadIndex();
  const today = new Date().toISOString().slice(0, 10);
  const live = (idx.game_versions || []).filter(v => v.released && v.released <= today)
    .sort((a, b) => a.released < b.released ? 1 : -1);
  _gvCache = live[0]?.code ?? null;
  if (!_gvCache) throw new Error('현행 게임 버전을 index.json에서 정할 수 없다');
  return _gvCache;
}
export const loadCurrentKernels = async () => loadKernels(await currentGameVersion());
export const loadGameStats = gv => j(`game_stats/${gv}.json`).catch(() => ({}));

/* ⭐⭐ 화면 공통 **정본 포메이션 슬롯** (2026-09-25 신설 · migration 063).
   ⛔⛔ 종전엔 7개 화면이 각자 `slots.filter(s => s.formation === slots[0].formation)`을 썼다 —
   즉 **어느 포메이션이 그려질지가 정렬 우연**이었다. 실측으로 터졌다: 아틀레티코는 slots에
   3-4-2-1 / 4-1-4-1 / 4-4-2 셋이 등록돼 있는데 3-4-2-1이 먼저 잡혀, 실측 정본(4-1-4-1)이 아닌
   포메이션이 그려졌고 **LAM·RAM 후보 0명 + FB 5명·DM 4명 실종**이 났다.
   ⇒ 정본은 DB의 `is_canon`이고, 화면은 **이 함수만** 부른다(CLAUDE.md 불변규칙 13 ②).
   ⚠️ 표시가 없는 옛 데이터에는 종전 규칙으로 물러선다 — 조용히 빈 화면이 되지 않게. */
export function canonSlots(teamData){
  const all = teamData?.slots || [];
  const canon = all.filter(s => s.is_canon);
  if (canon.length) return canon;
  return all.filter(s => s.formation === all[0]?.formation);
}
export const canonFormation = teamData => canonSlots(teamData)[0]?.formation ?? null;

/* 화면 공통 슬롯 후보 풀 — DB v_slot_candidates의 1:1 export.
   페이지가 squad + transfer를 각자 합치면 CONFIRMED 승격 중복이 재발하므로
   선수 목록을 만드는 모든 화면은 이 함수만 사용한다. */
const playerKey = value => String(value??'').normalize('NFC')
  .replace(/^영입·/, '').replace(/\((합류확정|신규|보유)\)$/, '');

export function slotCandidates(teamData, pos, { includeTransfers = true, includeDeparted = false } = {}){
  const departed = new Set((teamData.departed || []).map(playerKey));
  const rows = (teamData.slot_candidates || []).filter(q =>
    q.pos === pos
    && (includeTransfers || q.source_kind === 'squad')
    && (includeDeparted || !departed.has(playerKey(q.label))));
  const seen = new Set();
  return rows.filter(q => {
    const key = q.player_id != null ? `p:${q.player_id}` : `n:${q.name_en || q.label}`;
    if (seen.has(key)) return false;
    seen.add(key);
    return true;
  });
}

/* sofifa 새창 링크 — v1 SOFIFA 매핑의 후계. 라벨 접두(영입·)와 접미((합류확정) 등) 제거 후 조회 */
export function sofifaLink(label, GS, nameEn){
  const base = label.replace(/^영입·/, '').replace(/\((합류확정|신규|보유)\)$/, '');
  const g = GS[base];
  const kw = g?.sofifa_name || nameEn || base;   // sofifa 검색은 영문명으로 (한글 검색 불가)
  const url = g?.sofifa_id ? `https://sofifa.com/player/${g.sofifa_id}`
    : `https://sofifa.com/players?keyword=${encodeURIComponent(kw)}`;
  return `<a href="${url}" target="_blank" rel="noopener" title="sofifa에서 FC26 스탯 보기">FC26↗</a>`;
}
export function statLine(label, GS){
  const g = GS[label.replace(/^영입·/, '').replace(/\((합류확정|신규|보유)\)$/, '')];
  if (!g) return '';
  return `OVR <b>${g.ovr ?? '—'}</b>/${g.pot ?? '—'} · ${g.best_pos ?? ''} · ` +
    `<span class="dim">${_ps(g.playstyles).slice(0, 4).join('·') || '플레이스타일 미기재'}</span>`;
}
function _ps(v){
  if (!v) return [];
  try { const a = JSON.parse(v); return Array.isArray(a) ? a : []; }
  catch(e){ return String(v).split(/[;,]/).map(x => x.trim()).filter(Boolean); }
}

export function currentTeam(){
  try { return localStorage.getItem('tactics_team') || 'AVL'; } catch(e){ return 'AVL'; }
}
export function setCurrentTeam(code){
  try { localStorage.setItem('tactics_team', code); } catch(e){}
}

/* 공용 헤더 — 팀 스위처 + 페이지 네비.
   ⭐ 2026-10-04 사용자 지적 「얼티밋팀은 팀에 종속된 게 아닌데 팀 메뉴 아래 있다」 — 메뉴를 둘로 나눈다:
     · 팀 메뉴(TEAM_NAV): 고른 팀(regime)의 데이터를 보는 페이지 — 팀 버튼 아래 줄
     · 전체 메뉴(GLOBAL_NAV): 팀과 무관한 페이지(내 얼티밋 계정 · 게임 시스템 · 매뉴얼) — 오른쪽 위에 따로
   전체 메뉴를 보고 있을 때는 팀 버튼을 강조하지 않고, 팀을 누르면 그 팀 허브로 간다(팀 데이터를 보러 가는 동작이므로). */
/* ⭐ 2026-11-04 메뉴 정리(사용자 「전체 메뉴 구성 … 가독성·UI UX 개선」) — 흐름 순서(요약 → 경기 → 팀 전술 → 사람 → 비교 → 이적)로
   다시 배치하고, 모호했던 「리포트」를 「팀 전술」로 이름을 바꿨다(파일명은 그대로 · 링크 호환). 셋째 칸 = 마우스를 올리면 뜨는 설명. */
export const TEAM_NAV = [
  ['index.html', '허브', '팀 요약 · 최근 경기 · 메뉴 안내'],
  ['match-report.html', '경기 분석', '경기마다 실측·전술·게임 재현 프리셋'],
  ['report.html', '팀 전술', '시즌 게임 설정 시트 · 전술 정본 · 감독 프로필'],
  ['squad.html', '스쿼드', '자리별 베스트 XI와 후보 깊이'],
  ['player.html', '선수', '한 선수의 평가·경기 스탯·카드·진화'],
  ['compare.html', '선수 비교', '자리별 보유·영입 후보 적합 순위'],
  ['heatmap.html', '히트맵 비교', '실측 움직임 ↔ 게임 역할 그림 겹쳐 보기'],
  ['transfer.html', '이적', '영입 후보·유출 감시·수지'],
];
/* 라이트/다크 토글(2026-10-22 사용자 요청) — 선택·저장·적용은 theme-boot.js(head 동기 스크립트)가 한다.
   ⛔ 여기는 버튼만 그린다(스타일은 theme.css .themetog). */
const THEME_OPTS = [['auto', '자동', '기기 설정을 따른다'], ['light', '라이트', '항상 라이트'], ['dark', '다크', '항상 다크']];
function themeToggle(){
  const cur = window.tacticsTheme?.pref?.() || 'auto';
  return `<div class="themetog" role="group" aria-label="화면 모드">${THEME_OPTS.map(([v, l, t]) =>
    `<button data-theme-set="${v}" class="${v === cur ? 'on' : ''}" title="${t}" aria-pressed="${v === cur}">${l}</button>`).join('')}</div>`;
}
export const GLOBAL_NAV = [['evolutions.html', '얼티밋팀', '내 구단 · 진화 · SBC · 케미'], ['game.html', '게임 시스템', 'EA 확정 사실 · 역할 라이브러리 · 메타'],
  ['manual.html', '매뉴얼', '이 사이트의 용어와 읽는 법']];
export async function mountHeader(active){
  onSchemeChange();   // 라이트/다크 전환 시 새로 고침 — 캔버스(피치·열지도)는 다시 안 그려지므로(tokens.js)
  const idx = await loadIndex();
  const team = currentTeam();
  const isGlobal = GLOBAL_NAV.some(([h]) => h === active);
  const link = ([href, label, tip]) => `<a href="${href}" class="${href === active ? 'on' : ''}"${tip ? ` title="${tip}"` : ''}>${label}</a>`;
  const el = document.getElementById('hdr');
  el.innerHTML = `
    <div class="hrow">
      <a class="brand" href="index.html" title="허브로"><img src="assets/logo.svg" alt="">택틱스 랩</a>
      <div class="teams${isGlobal ? ' off' : ''}">${idx.regimes.map(r =>
        `<button data-t="${r.team_code}" class="${!isGlobal && r.team_code === team ? 'on' : ''}"${isGlobal ? ' title="팀 데이터 보기 — 그 팀 허브로 이동"' : ''}>${r.team_kr}</button>`).join('')}
      </div>
      <nav class="global" title="팀과 무관한 메뉴">${GLOBAL_NAV.map(link).join('')}</nav>
      ${themeToggle()}
    </div>
    <nav class="teamnav">${TEAM_NAV.map(link).join('')}</nav>`;
  el.querySelectorAll('button[data-theme-set]').forEach(b => b.addEventListener('click', () =>
    window.tacticsTheme?.set(b.dataset.themeSet)));
  el.querySelectorAll('button[data-t]').forEach(b => b.addEventListener('click', () => {
    setCurrentTeam(b.dataset.t);
    if (isGlobal) location.href = 'index.html'; else location.reload();
  }));
  /* 고정 헤더 높이를 CSS 변수(--hdr-h)로 — 고정 선택 막대·표 머리·목차 점프가 헤더 밑에 가리지 않게(theme.css · 2026-10-22).
     값만 넘기고 스타일은 전부 theme.css에 있다(CSS를 JS에 두지 않는다 — G22). */
  const setH = () => document.documentElement.style.setProperty('--hdr-h', `${el.offsetHeight}px`);
  setH();
  if (typeof ResizeObserver !== 'undefined') new ResizeObserver(setH).observe(el);
  return { idx, team, regime: idx.regimes.find(r => r.team_code === team) };
}

/* 경기 결과를 「우리 팀 기준」으로 — result는 홈-원정 순서로 저장된다(venue H·A·N · N은 홈 표기 순서).
   허브 최근 경기·경기 분석 결론 카드가 함께 쓰는 단일 정본(2026-11-04). → {us, them, res:'W'|'D'|'L'} 또는 null */
export function matchScore(m){
  const [h, a] = String(m?.result ?? '').split('-').map(Number);
  if (!Number.isFinite(h) || !Number.isFinite(a)) return null;
  const [us, them] = m.venue === 'A' ? [a, h] : [h, a];
  return { us, them, res: us > them ? 'W' : us < them ? 'L' : 'D' };
}
export const COMP_SHORT = {'Premier League':'PL', 'UEFA Champions League':'UCL', 'EFL Cup':'EFL컵', 'FA Cup':'FA컵',
  'UEFA Europa League':'UEL', 'UEFA Super Cup':'슈퍼컵'};

/* 긴 패널 접기(2026-11-04 · 불변규칙 14) — 높이가 max의 1.4배를 넘는 패널은 max까지만 보이고 아래에 「전체 보기」 버튼을 둔다.
   다시 그릴 때마다 불러도 된다(이전 버튼·상태를 지우고 새로 잰다). 스타일은 style.css .panel.folded · .fold-btn. */
export function foldLong(els, max = 640){
  for (const el of els){
    if (!el) continue;
    const prev = el.nextElementSibling;
    if (prev?.classList.contains('fold-btn')) prev.remove();
    el.classList.remove('folded');
    if (el.hidden || el.scrollHeight <= max * 1.4) continue;
    el.style.setProperty('--fold-h', `${max}px`);
    el.classList.add('folded');
    const b = document.createElement('button');
    b.type = 'button'; b.className = 'fold-btn';
    const label = () => el.classList.contains('folded') ? '전체 보기 ↓' : '접기 ↑';
    b.textContent = label();
    b.addEventListener('click', () => { el.classList.toggle('folded'); b.textContent = label();
      if (el.classList.contains('folded')) el.scrollIntoView({ block: 'start' }); });
    el.after(b);
  }
}

/* 페이지 목차(2026-11-04 · 불변규칙 14) — 패널 제목(h2 첫 글자 마디)으로 칩을 만들어 el에 넣는다. 패널에 id가 없으면 붙인다.
   경기 분석 화면은 자체 목차(buildToc)를 쓴다 — 이건 그 밖의 긴 화면용. */
export function mountPanelToc(el, panels){
  if (!el) return;
  const ps = [...panels].filter(p => p && !p.hidden && p.offsetParent !== null);
  el.innerHTML = '<span class="toc-lab">목차</span>' + ps.map((p, i) => {
    if (!p.id) p.id = 'pn' + i;
    const h = p.querySelector('h2');
    const t = (h?.childNodes[0]?.textContent ?? h?.textContent ?? '섹션').replace(/^[⭐\s]+/u, '').replace(/\s*[—-].*$/, '').trim().slice(0, 16);
    return `<a href="#${p.id}">${t}</a>`;
  }).join('');
}

/* GK 적합 표시 — obs#220. GK는 커널 적합이 변별력을 갖지 못한다: 측정된 GK들의 그리드가
   상호 코사인 ≥0.986이라 적합이 .96~.98 한 대역에 전원 수렴한다(폭 0.014). 숫자를 그대로
   노출하면 없는 우열을 읽게 되므로 GK 행은 평균 위치로 대체한다 — 변별은 여기서 나온다(폭 2.5).
   좌표 변환은 docs/30: 툴x = 100 − 소파y, 툴y = 소파x(= 골문에서의 전진 거리). */
export const isGkSlot = v => String(v ?? '').toUpperCase() === 'GK';

export function avgPos(teamData, playerId){
  if (playerId == null) return null;
  const a = (teamData.avg_positions || []).find(p => p.player_id === playerId);
  return a ? { x: +(100 - a.avg_y).toFixed(1), y: +a.avg_x.toFixed(1), n: a.n } : null;
}

/* GK가 아니면 null — 호출부가 기존 적합 표시를 그대로 쓴다.
   stored: transfer_targets처럼 좌표를 이미 들고 있는 행이면 그 값을 우선한다. */
export function gkPosCell(teamData, slotOrPos, playerId, stored){
  if (!isGkSlot(slotOrPos)) return null;
  const p = (stored && stored.y != null) ? stored : avgPos(teamData, playerId);
  const tip = 'GK는 커널 적합이 변별력을 갖지 못한다(obs#220) — 평균 위치로 표시한다';
  return p
    ? `<span title="${tip}">평균 위치 <b>y ${(+p.y).toFixed(1)}</b> <small class="dim">x ${(+p.x).toFixed(1)}${p.n ? ` · n=${p.n}` : ''}</small></span>`
    : `<small class="dim" title="${tip}">평균 위치 없음</small>`;
}

/* prescriptions에서 (kind 우선순위별) 선수 대표 그리드 고르기 */
export function gridOf(teamData, playerId, kinds){
  for (const k of kinds){
    const hit = teamData.prescriptions.find(p => p.player_id === playerId && p.kind === k && p.map25);
    if (hit) return hit;
  }
  return null;
}
