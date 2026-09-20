/* 내 구단 시각화 — FC 인게임 스쿼드 화면 재현 (2026-09-20, 사용자 지시 「fc27 게임처럼 시각화해줘」).
   ⛔ **계산하지 않는다.** EA 싱크 실측(카드 아트·OVR·케미 스타일·개인 케미)과 인게임 전술(migration 054)을
      그대로 배치할 뿐이다 — 이 화면에서 추천·순위를 만들지 않는다(그건 다른 탭의 일이다).
   ⭐ 카드 아트에는 **OVR·포지션·이름이 이미 인쇄돼 있다** — 덮어쓰지 않는다(2026-09-18 실증: 금속 질감 위에
      다시 쓰면 확대할 때 자국이 남는다). 진화로 값이 달라진 카드만 **카드 밖에 배지**로 현재 OVR을 알린다.
   ⭐ 배치는 fut.gg 슬롯 순서 규약을 따른다(f4231a: 0 GK · 1 RB · 2 CB · 3 CB · 4 LB · 5 CDM · 6 CDM ·
      7 RM · 8 LM · 9 CAM · 10 ST, **우→좌**). */
const esc = s => String(s ?? '').replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

/* 4-2-3-1 (2) 좌표 — x: 0(좌)~100(우) · y: 0(우리 골문)~100(상대 골문). 슬롯 순서는 위 규약대로 우→좌.
   ⚠️⚠️ **겹침 규칙**(2026-09-20, 브라우저에서 사각형 교차를 실제로 재서 고침 — 추정으로 하지 말 것):
   카드 한 장은 폭 = 피치 폭의 `--fccard`, 높이 = **피치 높이의 약 24%**다(카드 아트가 3:4보다 세로로
   길고 아래 pill이 붙는다). 따라서 두 슬롯은 다음 중 **하나 이상**을 만족해야 겹치지 않는다:
     · |Δy| ≥ 25   또는   · |Δx| ≥ 16(= --fccard)
   종전 좌표는 GK↔CB·CDM↔CAM·CAM↔ST 5쌍이 실제로 겹쳤다. 좌표를 바꿀 때 이 두 부등식을 다시 검산한다.
   그래서 CB·CDM을 x 37/63 → **34/66**으로 벌렸다(CAM·GK와 정확히 16 떨어진다). */
const SPOTS = [
  { x: 50, y: 4 },   // 0 GK
  { x: 86, y: 30 },  // 1 RB
  { x: 66, y: 25 },  // 2 CB(우)
  { x: 34, y: 25 },  // 3 CB(좌)
  { x: 14, y: 30 },  // 4 LB
  { x: 66, y: 50 },  // 5 CDM(우)
  { x: 34, y: 50 },  // 6 CDM(좌)
  { x: 87, y: 72 },  // 7 RM
  { x: 13, y: 72 },  // 8 LM
  { x: 50, y: 72 },  // 9 CAM
  { x: 50, y: 97 },  // 10 ST
];

const chemPips = n => `<span class="fc-pips">${[0, 1, 2].map(i =>
  `<i class="${i < (n ?? 0) ? 'on' : ''}"></i>`).join('')}</span>`;

/* 카드 한 장 — 아트가 있으면 아트, 없으면 대체 타일.
   ⭐ 이름을 카드 밖에 다시 쓰지 않는다(2026-09-20). 아트에 이미 인쇄돼 있어 중복이고, 그 한 줄 때문에
      카드 높이가 늘어 슬롯이 겹쳤다. 아트가 없는 대체 타일에만 이름을 넣는다. */
function card(p, role, posName, { bench = false } = {}) {
  if (!p) return `<div class="fc-card empty${bench ? ' bench' : ''}">
      <div class="fc-art ph">비어 있음</div><div class="fc-tag">${esc(posName ?? '')}</div></div>`;
  const evolved = p.card_ovr != null && p.current_ovr != null && p.card_ovr !== p.current_ovr;
  const art = p.card_image_url
    ? `<img class="fc-art" src="${esc(p.card_image_url)}" alt="${esc(p.name)} 카드" loading="lazy">`
    : `<div class="fc-art ph"><b>${p.current_ovr ?? ''}</b><span>${esc(p.name)}</span></div>`;
  const chem = p.chem_style_ea
    ? `<img class="fc-chem" src="assets/chemstyles/${p.chem_style_ea}.png" alt="케미 스타일" loading="lazy">`
    : '';
  /* ⚠️ 역할명은 pill에 넣지 않는다(2026-09-20 실측): 카드 폭이 피치의 16%라 「Advanced Forward」가
     「Advanc…」로 잘렸고, 안 잘리게 pill을 넓히면 옆 카드와 겹친다. 역할·포커스는 **사이드 패널**과
     툴팁에 온전히 있다 — 잘린 글자를 보여주느니 안 보여주는 편이 낫다. fut.gg도 카드 밑엔 포지션만 둔다. */
  const tag = `<div class="fc-tag">${posName ? `<b>${esc(posName)}</b>` : ''}${chemPips(p.chem_points)}</div>`;
  return `<div class="fc-card${bench ? ' bench' : ''}" data-p="${esc(p.player_id ?? '')}" tabindex="0"
       title="${esc(p.name)} · OVR ${p.current_ovr ?? '-'}${evolved ? ` (카드 인쇄 ${p.card_ovr})` : ''}${role ? ` · ${role.role_name}/${role.focus}` : ''}">
    <div class="fc-artwrap">${art}${chem}
      ${evolved ? `<span class="fc-evo">EVO ${p.current_ovr}</span>` : ''}</div>
    ${tag}
  </div>`;
}

/* ── 2단 레이아웃: 좌측 피치+벤치 / 우측 sticky 상세 패널.
   레이아웃 근거(2026-09-20, 사용자 지시 「fut.gg나 다른 사이트 참고해서 최적의 UX」): fut.gg Squad Builder를
   직접 열어 확인한 구성을 따랐다 — ⑴ 피치와 사이드 패널의 **2단**, ⑵ 카드가 피치 폭의 약 1/5로 **크다**,
   ⑶ 포지션은 카드 **아래 pill**. 종전에는 피치가 `aspect-ratio:3/4` + 본문 전체 폭이라 높이가 1,600px까지
   늘어 한 화면에 카드 한 장만 들어왔다 — 폭을 제한하고 카드를 %로 키워 11명이 한 화면에 들어온다.
   rows = [{player, role, posName}] 11개(슬롯 순서). */
export function fcPitch(xi, bench, meta = {}) {
  const spots = xi.map((r, i) => {
    const s = SPOTS[i] || { x: 50, y: 50 };
    return `<div class="fc-slot" style="left:${s.x}%;bottom:${s.y}%">${card(r.player, r.role, r.posName)}</div>`;
  }).join('');
  const benchCards = bench.map(r =>
    card(r.player, null, r.player?.positions?.split(',')[0] ?? '', { bench: true })).join('');
  return `
  <div class="fc-wrap">
    <div class="fc-layout">
      <div class="fc-main">
        <div class="fc-pitch">
          <div class="fc-lines" aria-hidden="true"></div>
          ${spots}
        </div>
        <div class="fc-bench"><h4>교체 <small>${bench.length}명</small></h4><div class="fc-benchrow">${benchCards}</div></div>
        <p class="fc-note">카드 아트에 인쇄된 OVR·포지션·이름은 <b>건드리지 않는다</b> — 진화로 값이 달라진 카드만 <span class="fc-evo inline">EVO</span> 배지로 현재 OVR을 알린다.</p>
      </div>
      <aside class="fc-side" id="fcside">${fcSideEmpty(meta, xi)}</aside>
    </div>
  </div>`;
}

/* 아무 카드도 고르지 않았을 때의 사이드 패널 — 빈 칸으로 두지 않고 **팀 설정 + 11칸 역할**을 보여준다.
   카드 pill에서 뺀 역할·포커스가 여기 온전히 들어간다(잘림 없이). */
export function fcSideEmpty(meta = {}, xi = []) {
  const rows = xi.filter(r => r.role).map(r => `<tr>
      <td><b>${esc(r.role.position_name)}</b></td>
      <td>${r.player ? esc(r.player.name) : '<span class="dim">—</span>'}</td>
      <td>${esc(r.role.role_name)}<br><small class="dim">${esc(r.role.focus)}</small></td></tr>`).join('');
  return `<div class="fc-sidebox">
    <h4 style="margin:0 0 8px">팀 설정 <small class="dim">인게임 실측</small></h4>
    <div class="fc-kv"><span>포메이션</span><b>${esc(meta.formation ?? '-')}</b></div>
    <div class="fc-kv"><span>빌드업</span><b>${esc(meta.build_up_style ?? '-')}</b></div>
    <div class="fc-kv"><span>수비 접근</span><b>${esc(meta.defensive_approach ?? '-')}</b></div>
    <div class="fc-kv"><span>라인 높이</span><b>${meta.line_height ?? '-'}${meta.is_custom_def ? ' <small class="dim">커스텀</small>' : ''}</b></div>
    <div class="fc-kv"><span>팀 케미</span><b class="${(meta.chemistry ?? 0) >= 33 ? 'up' : ''}">${meta.chemistry ?? '-'}/33</b></div>
    <p class="dim" style="font-size:12px;margin:10px 0 8px">카드를 누르면 <b>진화·현재 스탯·상세 스탯·적용 케미·프로필</b>이 여기 열린다.</p>
    ${rows ? `<h4 style="margin:12px 0 6px">11칸 역할 · 포커스</h4>
      <table class="tbl fc-roletbl"><tbody>${rows}</tbody></table>` : ''}
  </div>`;
}

export const FC_CSS = `
.fc-wrap{--fcg1:#0f3d24;--fcg2:#0a2e1b}
/* ⚠️ 칼럼을 1fr로 두면 안 된다(2026-09-20 사용자 지적 「중간에 공백이 많다」): 1fr은 남는 폭을 전부
   먹는데 .fc-main은 자기 최대 폭에서 멈추므로, 넓은 화면에서 **피치와 사이드 사이에 800px짜리 빈
   구멍**이 생겼다. 두 칼럼을 내용 폭 상한으로 묶고 justify-content로 가운데 모은다 — 남는 여백은
   가운데가 아니라 바깥에 생긴다. */
.fc-layout{display:grid;grid-template-columns:minmax(0,760px) minmax(340px,420px);
  gap:20px;align-items:start;justify-content:center}
.fc-main{min-width:0}
/* ⭐ 크기 규칙(2026-09-20) — 이 세 줄이 「비율이 안 맞고 정보가 작다」의 실제 해법이다:
   ⑴ **높이를 뷰포트에 맞춘다**(width:100%가 아니라 height 기준) — 폭은 비율에서 파생되므로
      화면이 낮으면 알아서 줄고, 높으면 720px까지 커진다. 종전엔 width:100%라 높이가 1,600px까지 늘었다.
   ⑵ 비율을 실제 잔디(68:105)가 아니라 **85:100**으로 넓힌다 — 같은 높이에서 폭이 커져 카드가 커진다.
      인게임 스쿼드 화면도 실측 비율이 아니라 이렇게 압축해 그린다.
   ⑶ 카드 폭은 **피치 폭의 %** 다(고정 px가 아니다). 카드가 작아 보이던 원인이 고정 92px였다.
   ⚠️ --fccard를 키울 때는 SPOTS 주석의 겹침 부등식을 다시 검산한다.
   ⭐ overflow:visible — GK(y4)·ST(y97) 카드는 잔디 밖으로 조금 나간다. 잘라내면 카드가 반쪽이 되므로
      자르지 않고, 대신 위아래 margin으로 이웃 요소와의 자리를 비워둔다. */
.fc-pitch{position:relative;aspect-ratio:85/100;height:min(760px,calc(100vh - 250px));
  width:auto;max-width:100%;margin:26px auto 48px;--fccard:16%;border-radius:10px;
  background:repeating-linear-gradient(0deg,var(--fcg1) 0 7%,var(--fcg2) 7% 14%);
  border:1px solid var(--line);overflow:visible}
.fc-lines{position:absolute;inset:8px;border:2px solid rgba(255,255,255,.18);border-radius:4px}
.fc-lines::before{content:"";position:absolute;left:0;right:0;top:50%;border-top:2px solid rgba(255,255,255,.18)}
.fc-lines::after{content:"";position:absolute;left:50%;top:50%;width:26%;aspect-ratio:1;transform:translate(-50%,-50%);
  border:2px solid rgba(255,255,255,.18);border-radius:50%}
.fc-slot{position:absolute;width:var(--fccard);transform:translate(-50%,50%)}
.fc-card{text-align:center;cursor:pointer;border-radius:8px;outline:none;transition:transform .12s}
.fc-card:hover,.fc-card:focus-visible{transform:translateY(-3px)}
.fc-card.sel .fc-artwrap{filter:drop-shadow(0 0 0 2px var(--ok))}
.fc-card.sel .fc-tag{border-color:var(--ok)}
.fc-card.empty{opacity:.45;cursor:default}
.fc-artwrap{position:relative;line-height:0}
.fc-art{width:100%;display:block;filter:drop-shadow(0 3px 6px rgba(0,0,0,.55))}
.fc-art.ph{display:flex;flex-direction:column;align-items:center;justify-content:center;aspect-ratio:3/4;
  background:var(--panel);border:1px solid var(--line);border-radius:6px;line-height:1.2;font-size:11px;color:var(--dim)}
.fc-art.ph b{font-size:20px;color:var(--txt)}
.fc-chem{position:absolute;right:-6%;top:12%;width:30%;filter:drop-shadow(0 2px 4px rgba(0,0,0,.6))}
.fc-evo{position:absolute;left:50%;top:-7px;transform:translateX(-50%);font-size:9.5px;font-weight:700;
  background:var(--ok);color:#06240f;border-radius:99px;padding:1px 6px;white-space:nowrap;z-index:2}
.fc-evo.inline{position:static;transform:none;display:inline-block}
/* 포지션·역할 pill — 카드 바로 아래 한 줄(fut.gg와 같은 자리). */
.fc-tag{display:inline-flex;gap:5px;align-items:center;justify-content:center;margin-top:-2px;
  background:rgba(4,10,7,.82);border:1px solid var(--line);border-radius:99px;padding:2px 8px;
  font-size:10px;line-height:1.5;max-width:100%}
.fc-tag b{font-weight:700}
.fc-tag span{color:var(--dim);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.fc-pips{display:inline-flex;gap:2px;flex:0 0 auto}
.fc-pips i{width:5px;height:5px;border-radius:50%;background:rgba(255,255,255,.22)}
.fc-pips i.on{background:var(--ok)}
.fc-bench{margin-top:14px}
.fc-bench h4{margin:0 0 6px;font-size:13px}
.fc-benchrow{display:flex;gap:10px;overflow-x:auto;padding:4px 0 8px}
.fc-benchrow .fc-card{flex:0 0 auto;width:92px}
.fc-note{font-size:11px;color:var(--dim);margin:10px 0 0}
/* 사이드 패널 — 스크롤을 따라다니고, 길면 자기 안에서만 스크롤한다. */
.fc-side{position:sticky;top:12px;max-height:calc(100vh - 24px);overflow:auto;
  background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:12px}
.fc-kv{display:flex;justify-content:space-between;gap:10px;font-size:12.5px;padding:4px 0;border-bottom:1px dotted var(--line)}
.fc-kv span{color:var(--dim)}
.fc-roletbl td{font-size:11.5px;padding:3px 6px;vertical-align:top}
/* 선택된 카드로 돌아가는 길 — 상세를 열면 사이드 맨 위에 「팀 설정으로」 버튼이 붙는다. */
.fc-back{font-size:11.5px;margin-bottom:8px}
@media (max-width:1060px){
  .fc-layout{grid-template-columns:1fr}
  .fc-main{max-width:none}
  .fc-side{position:static;max-height:none}
}
@media (max-width:560px){.fc-pitch{--fccard:19%;height:min(560px,calc(100vh - 170px))}.fc-tag span{display:none}}
`;

/* ── 카드 상세 패널 (2026-09-20, 사용자 지시 「전술·진화 상태·현재 카드 스탯·상세 스탯·적용 케미·선수 프로필을
      모두 확인할 수 있도록」) ─────────────────────────────────────────────────────────────
   ⛔ 여기서도 계산하지 않는다. 단 **케미 감쇠**만은 게임 규칙이라 적용해 보여준다(3점=full · 2점=2/3 · 1점=1/3).
   ⚠️ 29속성(`attrs`)은 **기준 카드**의 값이다 — 진화한 카드는 상승분이 빠져 있어 6대 스탯과 어긋난다.
      숨기지 않고 **어긋난다는 사실을 함께 적는다**(결손을 0으로 만들지 않는다). */
const SIX = ['PAC', 'SHO', 'PAS', 'DRI', 'DEF', 'PHY'];
const SIX_KR = { PAC: '속도', SHO: '슛', PAS: '패스', DRI: '드리블', DEF: '수비', PHY: '피지컬' };
const num = v => (v == null || v === '' ? null : Number(v));
const parse = j => { try { return typeof j === 'string' ? JSON.parse(j) : (j || null); } catch { return null; } };

function sixRow(cur, base) {
  return `<table class="tbl"><thead><tr><th>스탯</th>${SIX.map(k => `<th>${k}</th>`).join('')}</tr></thead>
    <tbody><tr><td class="dim">현재</td>${SIX.map(k => `<td><b>${cur?.[k] ?? '—'}</b></td>`).join('')}</tr>
    ${base ? `<tr><td class="dim">기준 카드</td>${SIX.map(k => {
      const d = num(cur?.[k]) != null && num(base?.[k]) != null ? num(cur[k]) - num(base[k]) : null;
      return `<td>${base?.[k] ?? '—'}${d ? ` <small class="${d > 0 ? 'up' : 'dim'}">${d > 0 ? '+' : ''}${d}</small>` : ''}</td>`;
    }).join('')}</tr>` : ''}</tbody></table>`;
}

/* 케미 스타일 부스트 — 개인 케미 점수만큼 감쇠해 보여준다. */
function chemBlock(p, styles) {
  const st = (styles || []).find(s => s.ea_id === p.chem_style_ea);
  if (!st) return '<p class="dim">케미 스타일 정보 없음</p>';
  /* `boosts`는 **속성→값 객체**다(배열이 아니다 — 2026-09-20 확인). 배열 형태도 들어올 수 있어 둘 다 받는다. */
  const raw0 = parse(st.boosts) || {};
  const pairs = Array.isArray(raw0)
    ? raw0.map(b => [b.attr ?? b.attribute ?? '', num(b.value) ?? 0])
    : Object.entries(raw0).map(([k, v]) => [k, num(v) ?? 0]);
  const cp = p.chem_points ?? 0;
  const scale = cp >= 3 ? 1 : cp === 2 ? 2 / 3 : cp === 1 ? 1 / 3 : 0;
  /* ⭐ 실제 적용값은 **이 패널에서 가장 중요한 숫자**다(2026-09-20 사용자 지시 「눈에 잘 띄지 않으니 색조정」).
     본문 색(--up)을 그대로 쓰면 스타일 표기값과 구분이 안 된다 — 초록 배경 pill로 띄운다. */
  const rows = pairs.sort((a, b) => b[1] - a[1]).map(([attr, raw]) => {
    const eff = Math.round(raw * scale);
    return `<tr><td>${esc(attr)}</td><td class="dim">+${raw}</td>
      <td><span class="fc-boost${eff > 0 ? '' : ' zero'}">${eff > 0 ? '+' + eff : '0'}</span></td></tr>`;
  }).join('');
  return `<div class="fc-chemhead">
      <img src="assets/chemstyles/${st.ea_id}.png" alt=""><b>${esc(st.name)}</b>
      <span class="chip ${cp >= 3 ? 'ok' : 'dim'}">개인 케미 ${cp}/3</span></div>
    ${cp === 0 ? '<p class="dim" style="margin:4px 0">⚠️ 개인 케미 0이라 <b>부스트가 전혀 적용되지 않는다</b>(붙여둬도 효과 0).</p>' : ''}
    <table class="tbl"><thead><tr><th>속성</th><th>스타일 표기</th><th>실제 적용</th></tr></thead><tbody>${rows}</tbody></table>`;
}

function evoBlock(p, log) {
  const mine = (log || []).filter(l => l.club_player_id === p.id).sort((a, b) => a.id - b.id);
  if (!mine.length) return '<p class="dim">적용한 진화 없음.</p>';
  return `<table class="tbl"><thead><tr><th>진화</th><th>단계</th><th>상태</th><th>OVR</th></tr></thead><tbody>
    ${mine.map(l => {
      const state = l.is_void ? '<span class="dim">무효</span>'
        : l.completed_at ? `완료 <small class="dim">${esc(l.completed_at)}</small>`
        : '<b class="up">진행 중</b>';
      return `<tr${l.is_void ? ' style="opacity:.5"' : ''}><td>${esc(l.evo_name)}</td><td>${l.level ?? '-'}</td>
        <td>${state}</td><td class="dim">${l.ovr_before ?? '-'} → ${l.ovr_after ?? '-'}</td></tr>`;
    }).join('')}</tbody></table>`;
}

function attrBlock(p) {
  const a = parse(p.attrs);
  if (!a) return '<p class="dim">상세 스탯 미수집(결손 — 0이 아니다).</p>';
  const stale = p.card_ovr != null && p.current_ovr != null && p.card_ovr !== p.current_ovr;
  const items = Object.entries(a).map(([k, v]) => `<div class="fc-attr"><span>${esc(k)}</span><b>${v}</b></div>`).join('');
  return `${stale ? `<p class="dim" style="margin:0 0 6px">⚠️ 이 29속성은 <b>기준 카드(OVR ${p.card_ovr})</b>의 값이라
      <b>진화 상승분이 빠져 있다</b> — 위 6대 스탯(현재 OVR ${p.current_ovr})과 어긋난다. EA는 진화 후 개별 속성을 공개하지 않는다.</p>` : ''}
    <div class="fc-attrs">${items}</div>`;
}

export function cardDetail(p, ctx = {}) {
  if (!p) return '';
  const cur = parse(p.current_six), base = parse(p.card_six) || null;
  const role = ctx.role;
  const prof = p.player_id
    ? `<a class="act" href="player.html?id=${p.player_id}">선수 프로필 열기 ↗</a>`
    : `<span class="chip dim">⚠️ 우리 DB에 등재되지 않은 선수 — 프로필 없음</span>`;
  return `<div class="fc-detail">
    <div class="fc-dhead">
      <img class="fc-dart" src="${esc(p.card_image_url || '')}" alt="">
      <div>
        <h3>${esc(p.name)} <small class="dim">OVR ${p.current_ovr ?? '-'}${p.card_ovr !== p.current_ovr ? ` <span class="up">(카드 인쇄 ${p.card_ovr})</span>` : ''}</small></h3>
        <div class="dim" style="font-size:12px">${esc(p.positions || '')} · ${esc(p.club || '')} · ${esc(p.league || '')} · ${esc(p.nation || '')}</div>
        <div style="margin-top:6px">${prof}</div>
      </div>
    </div>
    ${role ? `<h4>이 자리의 전술</h4><div class="plist"><button disabled>${esc(role.position_name)}</button>
      <button disabled>역할 <b>${esc(role.role_name)}</b></button><button disabled>포커스 <b>${esc(role.focus)}</b></button></div>
      ${ctx.team ? `<div class="plist" style="margin-top:4px"><button disabled>빌드업 ${esc(ctx.team.build_up_style)}</button>
      <button disabled>수비 ${esc(ctx.team.defensive_approach)}</button><button disabled>라인 ${ctx.team.line_height}</button></div>` : ''}` : ''}
    <h4>현재 카드 스탯</h4>${sixRow(cur, base)}
    ${p.current_playstyles ? `<p style="font-size:12px;margin:6px 0 0"><span class="dim">PlayStyle</span> <b>${esc(p.current_playstyles)}</b></p>` : ''}
    <h4>진화 상태 <small class="dim">${p.evo_count ?? 0}회</small></h4>${evoBlock(p, ctx.log)}
    <h4>적용된 케미스트리</h4>${chemBlock(p, ctx.chem_styles)}
    <h4>상세 스탯</h4>${attrBlock(p)}
  </div>`;
}

export const FC_DETAIL_CSS = `
.fc-detail h4{margin:14px 0 6px;font-size:13px}
.fc-dhead{display:flex;gap:12px;align-items:flex-start}
.fc-dart{width:96px;flex:0 0 auto}
.fc-dhead h3{margin:0 0 2px;font-size:16px}
.fc-chemhead{display:flex;gap:8px;align-items:center;margin-bottom:6px}
.fc-chemhead img{width:26px}
.fc-attrs{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:2px 10px}
.fc-attr{display:flex;justify-content:space-between;font-size:12px;padding:2px 0;border-bottom:1px dotted var(--line)}
.fc-attr span{color:var(--dim)}
/* 케미 부스트 실제 적용값 — 표에서 즉시 눈에 들어와야 한다. */
.fc-boost{display:inline-block;min-width:34px;text-align:center;font-weight:800;font-size:12.5px;
  color:#062b12;background:var(--ok);border-radius:99px;padding:1px 8px}
.fc-boost.zero{color:var(--dim);background:transparent;border:1px solid var(--line);font-weight:600}
`;
