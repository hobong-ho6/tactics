/* 내 구단 시각화 — FC 인게임 스쿼드 화면 재현 (2026-09-20, 사용자 지시 「fc27 게임처럼 시각화해줘」).
   ⛔ **계산하지 않는다.** EA 싱크 실측(카드 아트·OVR·케미 스타일·개인 케미)과 인게임 전술(migration 054)을
      그대로 배치할 뿐이다 — 이 화면에서 추천·순위를 만들지 않는다(그건 다른 탭의 일이다).
   ⭐ 카드 아트에는 **OVR·포지션·이름이 이미 인쇄돼 있다** — 덮어쓰지 않는다(2026-09-18 실증: 금속 질감 위에
      다시 쓰면 확대할 때 자국이 남는다). 진화로 값이 달라진 카드만 **카드 밖에 배지**로 현재 OVR을 알린다.
   ⭐ 배치는 fut.gg 슬롯 순서 규약을 따른다(f4231a: 0 GK · 1 RB · 2 CB · 3 CB · 4 LB · 5 CDM · 6 CDM ·
      7 RM · 8 LM · 9 CAM · 10 ST, **우→좌**). */
const esc = s => String(s ?? '').replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

/* 4-2-3-1 (2) 좌표 — x: 0(좌)~100(우) · y: 0(우리 골문)~100(상대 골문). 슬롯 순서는 위 규약대로 우→좌. */
const SPOTS = [
  { x: 50, y: 5 },   // 0 GK
  { x: 86, y: 25 },  // 1 RB
  { x: 63, y: 18 },  // 2 CB(우)
  { x: 37, y: 18 },  // 3 CB(좌)
  { x: 14, y: 25 },  // 4 LB
  { x: 63, y: 44 },  // 5 CDM(우)
  { x: 37, y: 44 },  // 6 CDM(좌)
  { x: 87, y: 66 },  // 7 RM
  { x: 13, y: 66 },  // 8 LM
  { x: 50, y: 63 },  // 9 CAM
  { x: 50, y: 86 },  // 10 ST
];

const chemPips = n => `<span class="fc-pips">${[0, 1, 2].map(i =>
  `<i class="${i < (n ?? 0) ? 'on' : ''}"></i>`).join('')}</span>`;

/* 카드 한 장 — 아트가 있으면 아트, 없으면 대체 타일. */
function card(p, role, posName, { w = 92 } = {}) {
  if (!p) return `<div class="fc-card empty" style="width:${w}px">
      <div class="fc-art ph">비어 있음</div><div class="fc-pos">${esc(posName ?? '')}</div></div>`;
  const evolved = p.card_ovr != null && p.current_ovr != null && p.card_ovr !== p.current_ovr;
  const art = p.card_image_url
    ? `<img class="fc-art" src="${esc(p.card_image_url)}" alt="${esc(p.name)} 카드" loading="lazy">`
    : `<div class="fc-art ph"><b>${p.current_ovr ?? ''}</b><span>${esc(p.name)}</span></div>`;
  const chem = p.chem_style_ea
    ? `<img class="fc-chem" src="assets/chemstyles/${p.chem_style_ea}.png" alt="케미 스타일" loading="lazy">`
    : '';
  return `<div class="fc-card" style="width:${w}px" data-p="${esc(p.player_id ?? '')}"
       title="${esc(p.name)} · OVR ${p.current_ovr ?? '-'}${evolved ? ` (카드 인쇄 ${p.card_ovr})` : ''}${role ? ` · ${role.role_name}/${role.focus}` : ''}">
    <div class="fc-artwrap">${art}${chem}
      ${evolved ? `<span class="fc-evo">EVO ${p.current_ovr}</span>` : ''}</div>
    <div class="fc-name">${esc(p.name)}</div>
    ${posName ? `<div class="fc-pos">${esc(posName)}${chemPips(p.chem_points)}</div>` : chemPips(p.chem_points)}
    ${role ? `<div class="fc-role">${esc(role.role_name)}<small>${esc(role.focus)}</small></div>` : ''}
  </div>`;
}

/* ── 피치 + 선발 11 + 교체 명단. rows = [{player, role, posName}] 11개(슬롯 순서). */
export function fcPitch(xi, bench, meta = {}) {
  const spots = xi.map((r, i) => {
    const s = SPOTS[i] || { x: 50, y: 50 };
    return `<div class="fc-slot" style="left:${s.x}%;bottom:${s.y}%">${card(r.player, r.role, r.posName)}</div>`;
  }).join('');
  const benchCards = bench.map(r => card(r.player, null, r.player?.positions?.split(',')[0] ?? '', { w: 74 })).join('');
  const chem = meta.chemistry ?? null;
  return `
  <div class="fc-wrap">
    <div class="fc-head">
      <b>${esc(meta.squad_name ?? '내 스쿼드')}</b>
      <span class="chip">${esc(meta.formation ?? '')}</span>
      ${chem != null ? `<span class="chip ${chem >= 33 ? 'ok' : ''}">케미 ${chem}/33</span>` : ''}
      ${meta.build_up_style ? `<span class="chip dim">빌드업 ${esc(meta.build_up_style)}</span>` : ''}
      ${meta.defensive_approach ? `<span class="chip dim">수비 ${esc(meta.defensive_approach)}${meta.line_height != null ? ` · 라인 ${meta.line_height}` : ''}</span>` : ''}
    </div>
    <div class="fc-pitch">
      <div class="fc-lines" aria-hidden="true"></div>
      ${spots}
    </div>
    <div class="fc-bench"><h4>교체 <small>${bench.length}명</small></h4><div class="fc-benchrow">${benchCards}</div></div>
    <p class="fc-note">카드 아트에 인쇄된 OVR·포지션은 <b>건드리지 않는다</b> — 진화로 값이 달라진 카드만 <span class="fc-evo inline">EVO</span> 배지로 현재 OVR을 알린다.</p>
  </div>`;
}

export const FC_CSS = `
.fc-wrap{--fcg1:#0f3d24;--fcg2:#0a2e1b}
.fc-head{display:flex;gap:6px;align-items:center;flex-wrap:wrap;margin:0 0 8px}
.fc-head .chip.ok{border-color:var(--ok);color:var(--ok)}
.fc-pitch{position:relative;width:100%;aspect-ratio:3/4;min-height:520px;border-radius:10px;
  background:repeating-linear-gradient(0deg,var(--fcg1) 0 7%,var(--fcg2) 7% 14%);
  border:1px solid var(--line);overflow:hidden}
.fc-lines{position:absolute;inset:8px;border:2px solid rgba(255,255,255,.18);border-radius:4px}
.fc-lines::before{content:"";position:absolute;left:0;right:0;top:50%;border-top:2px solid rgba(255,255,255,.18)}
.fc-lines::after{content:"";position:absolute;left:50%;top:50%;width:22%;aspect-ratio:1;transform:translate(-50%,-50%);
  border:2px solid rgba(255,255,255,.18);border-radius:50%}
.fc-slot{position:absolute;transform:translate(-50%,50%)}
.fc-card{text-align:center;cursor:pointer}
.fc-card.empty{opacity:.45}
.fc-artwrap{position:relative;line-height:0}
.fc-art{width:100%;display:block;filter:drop-shadow(0 3px 6px rgba(0,0,0,.55))}
.fc-art.ph{display:flex;flex-direction:column;align-items:center;justify-content:center;aspect-ratio:3/4;
  background:var(--panel);border:1px solid var(--line);border-radius:6px;line-height:1.2;font-size:11px;color:var(--dim)}
.fc-art.ph b{font-size:20px;color:var(--txt)}
.fc-chem{position:absolute;right:-5px;top:14%;width:30%;filter:drop-shadow(0 2px 4px rgba(0,0,0,.6))}
.fc-evo{position:absolute;left:50%;bottom:-6px;transform:translateX(-50%);font-size:9.5px;font-weight:700;
  background:var(--ok);color:#06240f;border-radius:99px;padding:1px 6px;white-space:nowrap}
.fc-evo.inline{position:static;transform:none;display:inline-block}
.fc-name{font-size:11.5px;font-weight:700;margin-top:8px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.fc-pos{font-size:10px;color:var(--dim);display:flex;gap:4px;align-items:center;justify-content:center}
.fc-role{font-size:9.5px;color:var(--txt);opacity:.85;line-height:1.25}
.fc-role small{display:block;color:var(--dim)}
.fc-pips{display:inline-flex;gap:2px}
.fc-pips i{width:5px;height:5px;border-radius:50%;background:rgba(255,255,255,.22)}
.fc-pips i.on{background:var(--ok)}
.fc-bench{margin-top:14px}
.fc-bench h4{margin:0 0 6px;font-size:13px}
.fc-benchrow{display:flex;gap:10px;overflow-x:auto;padding-bottom:6px}
.fc-benchrow .fc-card{flex:0 0 auto}
.fc-note{font-size:11px;color:var(--dim);margin:10px 0 0}
@media (max-width:760px){.fc-pitch{min-height:440px}.fc-slot .fc-card{width:70px!important}}
`;
