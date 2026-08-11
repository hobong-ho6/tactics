/* 데이터 로더 + 팀 상태. 모든 페이지가 공유한다.
   데이터는 site/data/*.json (scripts/export.py 산출물) — 손편집 금지. */

const BASE = new URL('.', import.meta.url).href.replace(/assets\/$/, '');

async function j(path){
  const r = await fetch(BASE + 'data/' + path);
  if (!r.ok) throw new Error(`${path} 로드 실패 (${r.status})`);
  return r.json();
}

export const loadIndex   = () => j('index.json');
export const loadTeam    = code => j(`teams/${code}.json`);
export const loadKernels = gv => j(`kernels/${gv}.json`);
export const loadGameStats = gv => j(`game_stats/${gv}.json`).catch(() => ({}));

/* sofifa 새창 링크 — v1 SOFIFA 매핑의 후계. 라벨 접두(영입·)와 접미((합류확정) 등) 제거 후 조회 */
export function sofifaLink(label, GS){
  const base = label.replace(/^영입·/, '').replace(/\((합류확정|신규|보유)\)$/, '');
  const g = GS[base];
  const url = g?.sofifa_id ? `https://sofifa.com/player/${g.sofifa_id}`
    : `https://sofifa.com/players?keyword=${encodeURIComponent(base)}`;
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

/* 공용 헤더 — 팀 스위처 + 페이지 네비 */
export async function mountHeader(active){
  const idx = await loadIndex();
  const team = currentTeam();
  const nav = [
    ['index.html', '허브'], ['heatmap.html', '히트맵 비교'], ['squad.html', '스쿼드'],
    ['compare.html', '선수 비교'], ['transfer.html', '이적'], ['report.html', '리포트'],
    ['player.html', '선수'], ['game.html', '게임 시스템'], ['manual.html', '매뉴얼'],
  ];
  const el = document.getElementById('hdr');
  el.innerHTML = `
    <div class="teams">${idx.regimes.map(r =>
      `<button data-t="${r.team_code}" class="${r.team_code === team ? 'on' : ''}">${r.team_kr}</button>`).join('')}
    </div>
    <nav>${nav.map(([href, label]) =>
      `<a href="${href}" class="${href === active ? 'on' : ''}">${label}</a>`).join('')}
    </nav>`;
  el.querySelectorAll('button[data-t]').forEach(b => b.addEventListener('click', () => {
    setCurrentTeam(b.dataset.t); location.reload();
  }));
  return { idx, team, regime: idx.regimes.find(r => r.team_code === team) };
}

/* prescriptions에서 (kind 우선순위별) 선수 대표 그리드 고르기 */
export function gridOf(teamData, playerId, kinds){
  for (const k of kinds){
    const hit = teamData.prescriptions.find(p => p.player_id === playerId && p.kind === k && p.map25);
    if (hit) return hit;
  }
  return null;
}
