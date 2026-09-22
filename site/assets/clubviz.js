/* 내 구단 시각화 — FC 인게임 스쿼드 화면 재현 (2026-09-20, 사용자 지시 「fc27 게임처럼 시각화해줘」).
   ⛔ **계산하지 않는다.** EA 싱크 실측(카드 아트·OVR·케미 스타일·개인 케미)과 인게임 전술(migration 054)을
      그대로 배치할 뿐이다 — 이 화면에서 추천·순위를 만들지 않는다(그건 다른 탭의 일이다).
   ⭐ 카드 아트에는 **OVR·포지션·이름이 이미 인쇄돼 있다** — 덮어쓰지 않는다(2026-09-18 실증: 금속 질감 위에
      다시 쓰면 확대할 때 자국이 남는다). 진화로 값이 달라진 카드만 **카드 밖에 배지**로 현재 OVR을 알린다.
   ⭐ 배치는 fut.gg 슬롯 순서 규약을 따른다(f4231a: 0 GK · 1 RB · 2 CB · 3 CB · 4 LB · 5 CDM · 6 CDM ·
      7 RM · 8 LM · 9 CAM · 10 ST, **우→좌**). */
import { PLAYSTYLES } from './playstyle-icons.js';
export { PLAYSTYLES };   // 화면들이 같은 사전을 쓰도록 재수출(설명·아이콘 중복 방지)
import { repaintEvoCard } from './evocard.js?v=20260921a';

const esc = s => String(s ?? '').replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

/* 4-2-3-1 (2) 좌표 — x: 0(좌)~100(우) · y: 0(우리 골문)~100(상대 골문). 슬롯 순서는 위 규약대로 우→좌.
   ⚠️⚠️ **겹침 규칙**(2026-09-20, 브라우저에서 사각형 교차를 실제로 재서 고침 — 추정으로 하지 말 것):
   카드 한 장은 폭 = 피치 폭의 `--fccard`, 높이 ≈ 피치 높이의 `ar×fccard×1.545 + 3%`다
   (카드 아트가 3:4보다 세로로 길고 아래 pill이 붙는다). 따라서 두 슬롯은 다음 중 **하나 이상**을
   만족해야 겹치지 않는다:  · |Δy| ≥ 카드높이%   또는   · |Δx| ≥ --fccard
   ⭐ 2026-09-21: 카드를 16% → **17.5%**로 키웠다(사용자 지시 「주발·포지션이 잘 안 보인다」).
   카드 높이%가 24 → 26으로 늘어 좌표를 다시 풀었다 — CB·CDM을 x 32/68로 벌려 CAM·GK와 18 띄우고,
   같은 열에 서는 CB↔CDM은 Δy 27로, CAM↔ST는 Δy 27로 잡았다. 좌표를 바꾸면 이 부등식을 다시 검산한다. */
const SPOTS = [
  { x: 50, y: 4 },   // 0 GK
  { x: 88, y: 28 },  // 1 RB
  { x: 68, y: 23 },  // 2 CB(우)
  { x: 32, y: 23 },  // 3 CB(좌)
  { x: 12, y: 28 },  // 4 LB
  { x: 68, y: 50 },  // 5 CDM(우)
  { x: 32, y: 50 },  // 6 CDM(좌)
  { x: 88, y: 72 },  // 7 RM
  { x: 12, y: 72 },  // 8 LM
  { x: 50, y: 70 },  // 9 CAM
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
  /* ⭐ 진화 카드는 **아트에 인쇄된 OVR·스탯을 현재 값으로 다시 그린다**(2026-09-21 사용자 지시
     「진화가 적용된 오버롤을 카드에 직접 보여줘」). 배지만으로는 작아서 읽히지 않았다.
     ⚠️ getImageData를 쓰므로 `crossorigin`이 필요하고, 그리기는 이미지 로드 뒤라 `paintEvoCards()`가
     나중에 캔버스로 바꿔 끼운다. 실패하면 원본 <img>가 그대로 남는다(빈 칸이 되지 않는다). */
  /* ⚠️ 진화 카드는 loading="lazy"를 쓰지 않는다(2026-09-21 실측): 화면 밖 카드는 로드가 미뤄져
     naturalWidth가 0이고, 그러면 다시 그리기가 영영 실행되지 않아 **인쇄된 옛 OVR이 그대로 남는다**.
     진화 카드는 스쿼드에 몇 장뿐이라 즉시 로드해도 부담이 없다. */
  const art = p.card_image_url
    ? `<img class="fc-art" src="${esc(p.card_image_url)}" alt="${esc(p.name)} 카드"
         ${evolved
            ? `crossorigin="anonymous" data-evo-ovr="${p.current_ovr}" data-evo-six="${esc(JSON.stringify(parse(p.current_six) || {}))}"`
            : 'loading="lazy"'}>`
    : `<div class="fc-art ph"><b>${p.current_ovr ?? ''}</b><span>${esc(p.name)}</span></div>`;
  const chem = p.chem_style_ea
    ? `<span class="fc-chem"><img src="assets/chemstyles/${p.chem_style_ea}.png" alt="케미 스타일" loading="lazy"></span>`
    : '';
  /* ⚠️ 역할명은 pill에 넣지 않는다(2026-09-20 실측): 카드 폭이 피치의 16%라 「Advanced Forward」가
     「Advanc…」로 잘렸고, 안 잘리게 pill을 넓히면 옆 카드와 겹친다. 역할·포커스는 **사이드 패널**과
     툴팁에 온전히 있다 — 잘린 글자를 보여주느니 안 보여주는 편이 낫다. fut.gg도 카드 밑엔 포지션만 둔다. */
  /* ⚠️ EVO 배지를 카드 아트 **위에 얹으면 안 된다**(2026-09-21 사용자 지적 「evo 뱃지가 다 잘려서 나옴」).
     fut.gg 카드 이미지는 위아래에 투명 여백이 있어 top:4%가 그림 밖이고, 거기 뜬 배지는 이웃 슬롯에
     가려 잘린다. 카드 **아래 pill 줄**로 내리면 항상 온전히 보이고 잘릴 자리가 없다. */
  /* ⭐ 배지는 「EVO 80」이 아니라 **인쇄값▸현재값**으로 쓴다(2026-09-21 사용자 지적
     「어떤 의미인지도 모르겠어」). 「EVO 80」은 기준이 빠져 80이 무엇 대비인지 알 수 없었다 —
     `78▸80`이면 카드에 찍힌 78이 진화로 80이 됐다는 사실이 숫자만으로 전달된다. */
  const tag = `<div class="fc-tag">${posName ? `<b>${esc(posName)}</b>` : ''}` +
    (evolved ? `<span class="fc-evo" title="카드에 인쇄된 OVR ${p.card_ovr} → 진화 적용 후 현재 ${p.current_ovr}">${p.card_ovr}▸${p.current_ovr}</span>` : '') +
    `${chemPips(p.chem_points)}</div>`;
  return `<div class="fc-card${bench ? ' bench' : ''}" data-p="${esc(p.player_id ?? '')}" tabindex="0"
       title="${esc(p.name)} · OVR ${p.current_ovr ?? '-'}${evolved ? ` (카드 인쇄 ${p.card_ovr})` : ''}${role ? ` · ${role.role_name}/${role.focus}` : ''}">
    <div class="fc-artwrap">${art}${chem}</div>
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
        <p class="fc-note">카드 아트에 인쇄된 OVR·포지션·이름은 <b>건드리지 않는다</b> —
          진화로 값이 달라진 카드에만 <span class="fc-evo inline">78▸80</span> 배지를 붙인다
          (<b>카드에 찍힌 OVR ▸ 진화 적용 후 현재 OVR</b>). 배지가 없으면 인쇄값이 곧 현재값이다.</p>
      </div>
      <aside class="fc-side" id="fcside">${fcSideEmpty(meta, xi)}</aside>
    </div>
  </div>`;
}

/* 진화 카드 아트를 현재 값으로 다시 그린다. fcPitch/벤치를 렌더한 **뒤에** 부른다.
   ⛔ 여기서 값을 만들지 않는다 — `data-evo-*`에 실어둔 원장 값을 그대로 그린다. */
export function paintEvoCards(root = document) {
  const SIXK = ['PAC', 'SHO', 'PAS', 'DRI', 'DEF', 'PHY'];
  const GKK = ['DIV', 'HAN', 'KIC', 'REF', 'SPD', 'POS'];
  root.querySelectorAll('img.fc-art[data-evo-ovr]').forEach(im => {
    const go = () => {
      const six = parse(im.getAttribute('data-evo-six')) || {};
      const keys = six.DIV != null ? GKK : SIXK;
      const cv = repaintEvoCard(im, {
        ovr: Number(im.getAttribute('data-evo-ovr')),
        six: keys.map(k => [k, six[k] ?? null]),
      });
      if (!cv) return;                       // 실패하면 원본을 그대로 둔다
      cv.className = 'fc-art';
      im.replaceWith(cv);
    };
    if (im.complete && im.naturalWidth) go();
    else im.addEventListener('load', go, { once: true });
  });
}

/* 가로 스크롤 영역을 마우스로 끌어서 민다(2026-09-20 사용자 지시 「교체영역 드래그로 스크롤」).
   ⚠️ 드래그가 끝날 때 click이 뒤따라 발생해 **카드 상세가 잘못 열린다** — 5px 넘게 움직였으면
   다음 click 한 번을 캡처 단계에서 삼킨다(그냥 클릭했을 때는 그대로 열려야 한다). */
export function enableDragScroll(el) {
  if (!el) return;
  let down = false, sx = 0, sl = 0, moved = 0;
  /* ⛔ `setPointerCapture`를 쓰면 안 된다(2026-09-21 사용자 지적 「교체 영역 카드를 눌러도 프로필이
     안 나온다」): 포인터가 컨테이너에 잡혀 pointerup이 카드가 아닌 컨테이너에서 끝나고, 브라우저가
     click을 **공통 조상에서** 발생시켜 카드의 click 핸들러가 영영 불리지 않는다.
     캡처 대신 window에 move/up을 달면 드래그도 되고 클릭도 산다. */
  el.addEventListener('pointerdown', e => {
    if (e.button !== 0) return;
    down = true; moved = 0; sx = e.clientX; sl = el.scrollLeft;
    el.classList.add('drag');
  });
  const move = e => {
    if (!down) return;
    const dx = e.clientX - sx;
    moved = Math.max(moved, Math.abs(dx));
    if (moved > 3) el.scrollLeft = sl - dx;   // 손떨림으로 스크롤이 튀지 않게 문턱을 둔다
  };
  const up = () => {
    if (!down) return;
    down = false; el.classList.remove('drag');
    /* 실제로 끌었을 때만 뒤따르는 click 한 번을 삼킨다. 단순 클릭(움직임 5px 이하)은 그대로 통과한다. */
    if (moved > 5) el.addEventListener('click',
      ev => { ev.stopPropagation(); ev.preventDefault(); }, { capture: true, once: true });
  };
  window.addEventListener('pointermove', move);
  window.addEventListener('pointerup', up);
  window.addEventListener('pointercancel', up);
}


/* 도움말 툴팁 — body에 띄운다. CSS ::after는 overflow:auto 컨테이너(사이드 패널)에서 잘린다.
   ⭐ 위임 방식이라 나중에 그려지는 요소에도 자동으로 붙는다(한 번만 호출하면 된다). */
export function enableHelpTips() {
  if (window.__helpTipOn) return;
  window.__helpTipOn = true;
  const tip = document.createElement('div');
  tip.className = 'helptip'; tip.hidden = true;
  document.body.appendChild(tip);
  const show = h => {
    tip.textContent = h.getAttribute('data-tip') || '';
    tip.hidden = false;
    const r = h.getBoundingClientRect();
    const w = Math.min(340, window.innerWidth - 24);
    tip.style.width = w + 'px';
    tip.style.left = Math.max(8, Math.min(r.left, window.innerWidth - w - 12)) + 'px';
    const below = r.bottom + 8;
    tip.style.top = (below + 160 > window.innerHeight ? Math.max(8, r.top - 8 - tip.offsetHeight) : below) + 'px';
  };
  document.addEventListener('pointerover', e => {
    const h = e.target.closest && e.target.closest('.fc-help[data-tip]');
    if (h) show(h);
  });
  document.addEventListener('pointerout', e => {
    if (e.target.closest && e.target.closest('.fc-help')) tip.hidden = true;
  });
  document.addEventListener('focusin', e => {
    const h = e.target.closest && e.target.closest('.fc-help[data-tip]');
    if (h) show(h);
  });
  document.addEventListener('focusout', () => { tip.hidden = true; });
}


/* ── 카드 비교 (2026-09-22 사용자 요청 「카드를 비교하는 기능도 추가」) ──────────────────
   두 카드를 나란히 놓고 **인게임 실전값**으로 견준다(실측 29속성 + 케미 부스트).
   ⛔ 여기서도 계산을 만들지 않는다 — 상세 패널과 **같은 규칙**으로 값을 뽑아 차이만 표시한다.
   ⚠️ 한쪽에만 있는 속성(GK↔필드)은 비교하지 않는다. */

/* ── 에메리 기준 우열 판정 (2026-09-22 사용자 요청 「같은 포지션끼리면 누가 더 나은지 + 근거」) ──
   ⛔ 새 기준을 발명하지 않는다 — **정본 슬롯 역할**(slot_canon_roles, 에메리 재현)의
      핵심 속성 가중(game_role_key_attrs)으로 두 카드를 같은 자로 잰다.
   ⚠️ 포지션이 겹치지 않으면 **판정하지 않는다** — 다른 자리의 선수를 한 잣대로 줄 세우면 틀린다.
   ⚠️ 적합도 차가 작으면 **「구분되지 않는다」**고 말한다(프로젝트 규약: 노이즈를 확정으로 승격시키지 않는다).
   ⛔ 케미는 빼고 **진화만 반영한 카드 자체 값**으로 잰다(비교 전체와 같은 기준). */
const CANON_FOR = { GK:['GK'], CB:['RCB','LCB'], RB:['RB'], LB:['LB'], RWB:['RB'], LWB:['LB'],
  CDM:['RDM','LDM'], CM:['RDM','LDM','CAM'], CAM:['CAM'], CF:['ST','CAM'],
  RM:['RM'], LM:['LM'], RW:['RM'], LW:['LM'], ST:['ST'] };

/* 이 자리가 무엇을 요구하는가 — 역할 설명이 있으면 쓰고, 없으면 가중 상위 속성으로 대신 말한다.
   ⛔ 설명을 지어내지 않는다 — 원장(game_role_focus.movement_kr)에 있으면 그것, 없으면 속성 나열이다. */
function roleDesc(c, ctx) {
  const f = (ctx.focus_rows || []).find(x => x.role_id === c.role_id && x.focus === c.focus);
  if (f && f.movement_kr) return String(f.movement_kr).replace(/\*\*/g, '').slice(0, 110);
  const w = {}; for (const r of (ctx.key_attrs || [])) if (r.role_id === c.role_id) w[r.attr] = r.weight;
  const top = Object.entries(w).sort((x, y) => y[1] - x[1]).slice(0, 4).map(x => x[0]);
  return top.length ? `핵심 속성: ${top.join(' · ')}` : '';
}

/* PlayStyle ↔ 속성 연결 (2026-09-22 사용자 제안 「포지션별로 패스가 중요하면 PlayStyle도 가중을」).
   ⛔⛔ **점수에는 넣지 않는다.** PlayStyle이 「적합도 몇 점어치인가」는 EA도 커뮤니티도 답한 적이 없고,
        내가 임의 계수를 만들면 근거 없는 가중이 숫자로 포장된다(불변규칙 12).
   ⇒ 대신 **「그 역할이 보는 속성을 건드리는 PlayStyle인가」**만 표시한다. 그건 EA의 PlayStyle 정의에서
      바로 읽히는 사실이라 지어낼 여지가 적다.
   ⚠️ 그래도 이 연결표 자체는 **판단값(MEDIUM)**이다 — EA 정의 문구(fut.gg /api/fut/playstyles/)를
      우리 29속성 어휘로 옮긴 것이고, EA가 "이 PS는 이 속성을 쓴다"고 명시한 게 아니다. */
export const PS_ATTRS = {   // ⭐ 화면들이 같은 연결표를 쓰도록 내보낸다(2026-09-22)
  'Incisive Pass': ['짧은 패스', '긴 패스', '커브', '시야'],
  'Pinged Pass': ['긴 패스'], 'Whipped Pass': ['크로스'], 'Tiki Taka': ['짧은 패스'],
  'Long Ball Pass': ['긴 패스'], 'Trivela': ['커브'],
  'First Touch': ['볼컨트롤'], 'Technical': ['드리블', '민첩성'], 'Trickster': ['드리블'],
  'Flair': ['드리블'], 'Press Proven': ['힘'], 'Rapid': ['질주 속도', '가속'],
  'Quick Step': ['가속'], 'Explosive Sprint': ['가속'],
  'Finesse Shot': ['커브', '결정력'], 'Power Shot': ['슈팅력'], 'Low Driven Shot': ['슈팅력', '결정력'],
  'Chip Shot': ['결정력'], 'Dead Ball': ['프리킥 정확도', '커브'], 'Power Header': ['헤딩 정확도'],
  'Precision Header': ['헤딩 정확도'], 'Game Changer': ['결정력'], 'Aerial': ['헤딩 정확도', '점프'],
  'Aerial Fortress': ['헤딩 정확도', '점프'], 'Bruiser': ['힘'], 'Enforcer': ['힘', '공격성'],
  'Jockey': ['수비 위치 선정', '차단력'], 'Block': ['차단력'], 'Intercept': ['차단력'],
  'Anticipate': ['수비 위치 선정', '스탠딩 태클'], 'Slide Tackle': ['슬라이딩 태클'],
  'Relentless': ['체력'], 'Acrobatic': ['민첩성'],
};

/* ⭐ FC27에서 **효과가 축소·제거된** PlayStyle — EA 1차(Gameplay Deep Dive) verbatim으로 확정된 것만.
   정본은 `game_system_changes` #13·#22(등급 A)와 docs/22 §6이다. 여기 목록을 늘리려면 그쪽에 행이 먼저 있어야 한다.
   ⚠️ 「없어졌다」가 아니라 「같은 슬롯값이 전년보다 싸졌다」는 뜻이라 tie-break에서 **반 표**로 센다. */
const PS_FC27_CUT = {
  'Rapid': '드리블 속도 보너스 축소 — EA 「가속 스탯이 더 중요해진다」',
  'Quick Step': '가속 보너스 축소 — EA 「가속 스탯이 더 중요해진다」',
  'Low Driven Shot': '슛 속도 부스트 제거(정확도만 잔존)',
  'Pinged Pass': '수신자 트랩 오차 감소 효과 제거 — 패스 속도 효과만 남음',
  'Tiki Taka': '애니 속도 보너스·수신자 트랩 오차 감소 제거',
  'Jockey': '보유자 보너스↓(비보유자 기본 조키 가속↑)',
};

const TIE_TIP = '스탯 적합도 차이가 1.0 미만이라 스탯으로는 우열을 못 정한 자리다(그 정도는 EA 값의 노이즈 폭). '
  + '이 구간에서는 아래 PlayStyle 표가 판정하는데, 그 표까지 같아서 남은 기준이 없다는 뜻이다. '
  + '「둘이 비슷하다」가 아니라 「이 잣대로는 못 가른다」로 읽을 것 — 케미·폼·상대는 애초에 이 점수에 없다.';

function emeryVerdict(a, b, ctx) {
  const canon = ctx.canon_roles || [], keyAttrs = ctx.key_attrs || [];
  if (!canon.length || !keyAttrs.length) return '';
  const pa = String(a.positions || '').split('/').map(x => x.trim()).filter(Boolean);
  const pb = String(b.positions || '').split('/').map(x => x.trim()).filter(Boolean);
  const common = pa.filter(x => pb.includes(x));
  if (!common.length) return `<div class="cmp-verdict none"><b>자리 비교 없음</b>
    <span class="dim">— 두 카드가 함께 설 수 있는 포지션이 없다(${esc(pa.join('/'))} ↔ ${esc(pb.join('/'))}).
    다른 자리의 선수를 한 잣대로 줄 세우면 틀린다.</span></div>`;
  /* 공통 포지션 중 **정본 슬롯이 있는 것**만 쓴다. */
  const cands = [];
  for (const pos of common) for (const cp of (CANON_FOR[pos] || [pos])) {
    const c = canon.find(x => x.pos === cp);
    if (c && !cands.some(x => x.pos === c.pos)) cands.push({ ...c, from: pos });
  }
  if (!cands.length) return '';
  const W = {}; for (const r of keyAttrs) (W[r.role_id] ??= {})[r.attr] = r.weight;
  const A = parse(a.current_attrs) || parse(a.attrs) || {};
  const B = parse(b.current_attrs) || parse(b.attrs) || {};
  const fit = (at, w) => { const den = Object.values(w).reduce((t, v) => t + v * 99, 0);
    return den ? Object.entries(w).reduce((t, [k, v]) => t + v * (at[k] ?? 0), 0) / den * 100 : 0; };
  /* ⭐ 그 역할의 **숙련(Role+/++)** 보유 여부 — 스탯과 다른 축이라 점수에 섞지 않고 따로 적는다.
     canon의 role_id(cam_playmaker)를 게임 표기(Playmaker)로 옮겨 role_map과 맞춘다. */
  /* game_roles.name_en은 비어 있다(2026-09-22 실측). FC27 role_map 이름과
     전 역할을 명시 매핑한다. 접미를 임의로 풀면 cm_dlp→"dlp"처럼 조용한 거짓 「숙련 없음」이 된다. */
  const ROLE_EN = {
    cam_classic10:'Classic 10', cam_halfwinger:'Half-Winger', cam_playmaker:'Playmaker', cam_shadow:'Shadow Striker',
    cb_bpd:'Ball-Playing Defender', cb_defender:'Defender', cb_stopper:'Stopper', cb_wideback:'Wide Back',
    cm_b2b:'Box-To-Box', cm_dlp:'Deep-Lying Playmaker', cm_halfwinger:'Half-Winger',
    cm_holding:'Holding', cm_playmaker:'Playmaker',
    dm_boxcrasher:'Box Crasher', dm_centrehalf:'Centre-Half', dm_dlp:'Deep-Lying Playmaker',
    dm_holding:'Holding', dm_widehalf:'Wide Half',
    fb_att_wb:'Attacking Wingback', fb_falseback:'Falseback', fb_fullback:'Fullback',
    fb_inverted:'Inverted Wingback', fb_wingback:'Wingback',
    gk_ballplaying:'Ball Playing Keeper', gk_goalkeeper:'Goalkeeper', gk_sweeper:'Sweeper Keeper',
    st_advanced:'Advanced Forward', st_false9:'False 9', st_poacher:'Poacher', st_target:'Target Forward',
    w_insidefwd:'Inside Forward', w_wideplm:'Wide Playmaker', w_winger:'Winger',
    wm_insidefwd:'Inside Forward', wm_widemid:'Wide Midfielder', wm_wideplm:'Wide Playmaker', wm_winger:'Winger'
  };
  const enName = rid => (ctx.roles || []).find(r => r.role_id === rid)?.name_en || ROLE_EN[rid] || '';
  const eaPos = pos => ({ LCB:'CB', RCB:'CB', CCB:'CB', LDM:'CDM', RDM:'CDM',
    LCM:'CM', RCM:'CM', LAM:'CAM', RAM:'CAM' })[pos] || pos;
  const roleMastery = (c, pos, rid) => {
    const want = enName(rid).toLowerCase().replace(/[^a-z0-9]/g, '');
    if (!want) return '?';                      // 이름을 못 옮겼다 — 「없음」과 구분한다
    let seen = false, unresolved = false;
    for (const kind of ['plusplus', 'plus']) {
      const ids = parse(kind === 'plus' ? c.current_roles_plus : c.current_roles_plus_plus);
      if (!Array.isArray(ids)) continue;
      seen = true;
      const hit = ids.some(id => {
        const r = (ctx.role_map || []).find(x => x.game_version === 'FC27'
          && Number(x.ea_id) === Number(id) && x.kind === kind);
        if (!r) { unresolved = true; return false; }
        return r.position_name === eaPos(pos) && r.name.toLowerCase().replace(/[^a-z0-9]/g, '') === want;
      });
      if (hit) return kind === 'plusplus' ? 'Role++' : 'Role+';
    }
    return !seen || unresolved ? '?' : null;
  };
  const rows = cands.map(c => {
    const w = W[c.role_id] || {};
    const fa = fit(A, w), fb = fit(B, w), d = fa - fb;
    const ma = roleMastery(a, c.pos, c.role_id), mb = roleMastery(b, c.pos, c.role_id);
    /* 이 역할이 보는 속성을 건드리는 PlayStyle만 추린다(점수 아님 — 위 PS_ATTRS 주석 참조). */
    const hot = new Set(Object.entries(w).filter(([, v]) => v >= 2).map(([k]) => k));
    const psHit = c2 => String(c2.current_playstyles || '').split(',').map(x => x.trim()).filter(Boolean)
      .map(nm => ({ nm: nm.replace(/\s*\+$/, ''), plus: /\+$/.test(nm) }))
      .filter(x => (PS_ATTRS[x.nm] || []).some(at => hot.has(at)))
      .map(x => ({ ...x, hits: (PS_ATTRS[x.nm] || []).filter(at => hot.has(at)),
                   cut: PS_FC27_CUT[x.nm] || null }));
    const pha = psHit(a), phb = psHit(b);
    /* PlayStyle 표 — **반 표/한 표만 세고 크기는 세지 않는다**(아래 PS_TIP 주석 참조). */
    const votes = arr => arr.reduce((t, x) => t + (x.cut ? .5 : 1), 0);
    /* ⚠️ PS+는 **표를 더하지 않는다** — FC27이 PS↔PS+ 격차를 좁혔다고 EA가 명시했다(「선수의 타고난
       속성에 더 큰 비중이 실린다」). 칩에 +만 붙여 보여준다. */
    const va = votes(pha), vb = votes(phb);
    /* ⭐ 근거는 **가중이 걸린 속성 전부**를 보여준다(2026-09-22 사용자 지적
       「캐시는 체력만 높은데 우위인 게 이상하다」) — 상위 3개만 띄우니 합이 왜 그렇게 나오는지
       설명되지 않았다. 각 항목의 **가중·값·기여 차이**를 모두 적어 합계가 눈으로 따라가지게 한다. */
    const why = Object.entries(w).sort((x, y) => y[1] - x[1])
      .map(([k, wt]) => { const va = A[k] ?? 0, vb = B[k] ?? 0;
        return { k, wt, va, vb, gap: va - vb, contrib: wt * (va - vb) }; });
    return { c, fa, fb, d, why, ma, mb, pha, phb, va, vb };
  }).sort((x, y) => Math.abs(y.d) - Math.abs(x.d));
  /* 칩 하나 = 한 표. FC27에서 깎인 것은 **½** 표시를 달고 그 이유를 툴팁에 적는다. */
  const psCell = (arr, cls, v) => arr.length
    ? `${arr.map(x => `<span class="chip ${cls}${x.cut ? ' cut' : ''}" title="${esc(x.hits.join(' · '))}${
         x.cut ? ` — FC27 ½표: ${esc(x.cut)}` : ''}">${esc(x.nm)}${x.plus ? '+' : ''}${x.cut ? ' ½' : ''}</span>`).join(' ')}
       <b class="cmp-votes">${v % 1 ? v.toFixed(1) : v}표</b>`
    : '<span class="dim">없음 <b class="cmp-votes">0표</b></span>';
  const body = rows.map(r => {
    /* ⭐⭐ 2층 판정 (2026-09-22 사용자 지시 「플레이스타일까지 고려해 누가 더 적합한지 기준을 세우자」).
       ⑴ **스탯이 주(主)다** — Δ≥1.0이면 스탯이 결정하고 PlayStyle은 표시만 한다.
       ⑵ Δ<1.0(실측 무결정)일 때만 **PlayStyle이 tie-break 권한**을 갖는다.
       왜 이 모양인가:
       · EA는 PlayStyle이 원 스탯과 어떻게 결합되는지(곱셈/임계/독립) **한 번도 명시한 적이 없다**
         (리포트 §3.2 · 부재 증거 A). ⇒ 「PS = 적합도 몇 점」을 만들면 근거 없는 수가 판단을 가장한다(불변규칙 12).
       · 반면 **순서 정보는 EA 1차로 있다**: FC27은 PS 보너스를 깎고 속성 비중을 올렸고(「Our goal … refine the
         balance between PlayStyles and Attributes」 A), Intercept는 **PS 없는 고스탯 선수만 골라 상향**해
         두 축이 같은 결과값에 합산됨을 드러냈다. ⇒ **같은 방향을 보지만, PS가 스탯 차이를 뒤집을 만큼은 아니다.**
       · 「주 축이 못 가르는 구간에서만 보조 축이 판정한다」는 이 저장소의 기존 규약이다
         (docs/30 7단계 — 커널 Δ≤.05에서 영상이 tie-break 권한을 갖는다). 같은 모양을 그대로 쓴다.
       ⚠️ 반 표(FC27 축소분)는 **판단값**이다 — 어느 PS가 깎였는지는 A등급이지만 「그래서 반값」은 내 배분이다. */
    const statTie = Math.abs(r.d) < 1.0;
    const psGap = r.va - r.vb;
    const byPs = statTie && Math.abs(psGap) >= 1;
    const tie = statTie && !byPs;
    const d2 = byPs ? psGap : r.d;
    const winner = d2 > 0 ? a.name : b.name;
    const side = d2 > 0 ? 'dA' : 'dB';
    const nA = r.why.filter(x => x.gap > 0).length, nB = r.why.filter(x => x.gap < 0).length;
    /* ⚠️ 비중 열을 오른쪽 끝에 두면 **오른쪽 선수의 값처럼 읽힌다**(2026-09-22 사용자 지적).
       비중은 어느 선수의 것도 아니라 **그 역할이 그 속성을 얼마나 보는가**이므로 가운데 속성명에 붙인다. */
    const top = `<table class="tbl cmp-wtbl"><thead><tr>
        <th>${esc(a.name)}</th><th>이 역할이 보는 속성 <small>(● = 역할 비중)</small></th><th>${esc(b.name)}</th></tr></thead><tbody>
      ${r.why.map(x => `<tr>
        <td class="cmp-a ${x.gap > 0 ? 'win' : x.gap < 0 ? 'lose' : ''}">${x.va}</td>
        <td class="cmp-k">${esc(x.k)} <i class="cmp-w">${'●'.repeat(Math.round(x.wt))}</i></td>
        <td class="cmp-b ${x.gap < 0 ? 'win' : x.gap > 0 ? 'lose' : ''}">${x.vb}</td></tr>`).join('')}
      </tbody></table>
      <p class="dim" style="font-size:11px;margin:4px 0 0">항목 우위 <b class="wA">${nA}</b> ↔ <b class="wB">${nB}</b> —
        ⚠️ <b>항목 수가 아니라 비중(●)을 곱한 합</b>이 적합도다. 비중 큰 한 칸이 작은 여러 칸을 뒤집을 수 있다.</p>`;
    return `<div class="cmp-vrow">
      <div class="cmp-vhead"><b>${esc(r.c.pos)}</b>
        <span class="dim">${esc(ctx.role_kr?.[r.c.role_id] || r.c.role_id)} / ${esc(r.c.focus)}</span>
        <span class="dim" style="flex-basis:100%;font-size:11px">${esc(roleDesc(r.c, ctx))}</span>
        ${tie ? `<span class="chip dim fc-help" tabindex="0" data-tip="${esc(TIE_TIP)}">구분되지 않음<i>?</i></span>`
              : `<span class="cmp-d ${side} mid">${esc(winner)} 우위<i>${byPs ? 'PlayStyle이 가름' : '스탯이 가름'}</i></span>`}</div>
      <div class="cmp-vfit"><span class="cmp-a">${r.fa.toFixed(1)}</span>
        <span class="cmp-k">적합도<i>스탯 기준</i></span><span class="cmp-b">${r.fb.toFixed(1)}</span></div>
      ${top ? `<div class="cmp-vwhy">${top}</div>` : ''}
      <div class="cmp-vfit" style="font-size:12px;margin-top:8px">
        <span class="cmp-a">${r.ma === '?' ? '<span class="dim">확인 불가</span>'
          : r.ma ? `<span class="chip wA">${r.ma}</span>` : '<span class="dim">숙련 없음</span>'}</span>
        <span class="cmp-k">이 역할 숙련<i>점수에 안 들어감</i></span>
        <span class="cmp-b">${r.mb === '?' ? '<span class="dim">확인 불가</span>'
          : r.mb ? `<span class="chip wB">${r.mb}</span>` : '<span class="dim">숙련 없음</span>'}</span></div>
      <div class="cmp-vfit" style="font-size:12px;margin-top:6px;align-items:start">
        <span class="cmp-a">${psCell(r.pha, 'wA', r.va)}</span>
        <span class="cmp-k">이 역할에 걸리는 PlayStyle<i>${statTie ? '이 자리는 여기서 갈린다' : '스탯이 이미 갈랐다 — 참고'}</i></span>
        <span class="cmp-b">${psCell(r.phb, 'wB', r.vb)}</span></div></div>`;
  }).join('');
  return `<h4>에메리 전술 기준 — 어느 쪽이 나은가</h4>
    <div class="cmp-verdict">${body}
    <p class="dim" style="font-size:11px;margin:8px 0 0">
      <b>판단 기준 — 2층이다.</b><br>
      <b>1층 스탯(주).</b> 적합도 = Σ(역할 핵심 속성 가중 × 속성값) ÷ 만점. 가중은 <b>정본 슬롯 역할</b>(에메리 재현)의
      것을 그대로 쓴다 — 여기서 새 기준을 만들지 않는다. <b>차이가 1.0 이상이면 이 층이 결정한다.</b><br>
      <b>2층 PlayStyle(동점 깨기).</b> 스탯 차이가 1.0 미만이면 노이즈라 우열을 못 정한다. 그때만
      <b>그 역할이 보는 속성(●● 이상)을 건드리는 PlayStyle</b>을 세어 <b>표 차이가 1표 이상이면</b> 그쪽을 택한다.
      FC27에서 EA가 효과를 깎은 것(래피드·퀵스텝·로드리븐·핑드패스·티키타카·자키)은 <b>½표</b>다.<br>
      ⭐ <b>왜 PlayStyle을 점수에 직접 더하지 않나</b> — EA는 PlayStyle이 원 스탯과 어떻게 결합되는지
      (곱셈·임계값·독립 판정) <b>한 번도 밝힌 적이 없다</b>. 대신 <b>순서</b>는 1차 자료로 확인된다: FC27은 PS 보너스를
      깎고 속성 비중을 올렸고(「refine the balance between PlayStyles and Attributes」 — 「플레이스타일과 스탯 사이의
      균형을 다듬는다」), 인터셉트는 <b>PS 없는 고스탯 선수만 골라 상향</b>해 두 축이 같은 결과에 합쳐짐을 드러냈다.
      ⇒ <b>같은 방향을 보되 스탯 차이를 뒤집지는 못한다</b> — 그래서 동점 구간에만 권한을 준다
      (커널 Δ≤.05에서 영상이 판정하는 기존 규약과 같은 모양).<br>
      ⚠️ ½표 배분과 PlayStyle↔속성 연결표는 <b>판단값</b>이다(어느 PS가 깎였는지까지는 EA 1차). 칩에 마우스를 올리면 근거가 나온다.<br>
      ⛔ <b>역할 숙련은 어느 층에도 넣지 않았다</b> — FC27이 스페셜 카드에 Role++를 일괄로 줘서 변별력이 없다.
      ⛔ 케미는 빼고 <b>진화만 반영한</b> 카드 자체 값이며, <b>이 카드가 그 자리에 얼마나 맞나</b>일 뿐
      경기력·폼·상대는 담지 않는다.</p></div>`;
}

/* 비교 담기 칸 — **지금 무엇이 담겼는지**를 이름만으로 알기 어려웠다(2026-09-22 사용자 지시
   「비교담기를 한 경우 지금 담겨져 있는 선수 정보를 확인할 수 있도록」).
   ⇒ 카드 아트·OVR(진화 전 병기)·포지션·신체까지 담은 칸 2개를 항상 그린다 — 빈 칸도 자리를 잡아
     「하나 더 담으면 열린다」가 문장이 아니라 **모양으로** 보이게. ⛔ 카드 아트는 인쇄값이라
     진화 카드는 OVR이 다를 수 있다 — 그래서 아트 위가 아니라 **옆에 현재 OVR**을 적는다. */
export function cmpSlots(picked) {
  const slot = (c, i) => c ? `<div class="cmp-slot fill s${i}">
      ${c.card_image_url ? `<img src="${esc(c.card_image_url)}" alt="">` : '<div class="cmp-slot-ph"></div>'}
      <div class="cmp-slot-t"><b>${esc(c.name)}</b>
        <span>OVR <b>${c.current_ovr ?? '-'}</b>${c.card_ovr != null && c.card_ovr !== c.current_ovr
          ? ` <em class="d-evo">진화 전 ${c.card_ovr}</em>` : ''}</span>
        <span class="dim">${esc(c.positions || '')}</span>
        ${physLine(c) ? `<span class="dim">${physLine(c)}</span>` : ''}</div>
      <button class="cmp-x" data-cmpdrop="${c.id}" title="이 카드를 비교에서 뺀다">×</button></div>`
    : `<div class="cmp-slot empty"><span class="dim">비어 있음<i>카드를 눌러 「비교에 담기」</i></span></div>`;
  return `<div class="cmp-slots">${slot(picked[0], 'A')}<span class="cmp-vs">vs</span>${slot(picked[1], 'B')}</div>`;
}

export function compareCards(a, b, ctx = {}) {
  if (!a || !b) return '';
  /* ⛔ 비교 기준은 **케미 제외 · 진화 반영**이다(2026-09-22 사용자 지시).
     `current_attrs`가 곧 그 값이다 — EA가 주는 카드 속성은 진화가 반영돼 있고 케미는 빠져 있다.
     케미를 섞으면 「카드 자체의 우열」이 아니라 「지금 붙인 스타일까지 낀 값」이 돼 비교가 흐려진다. */
  const A = parse(a.current_attrs) || parse(a.attrs) || {};
  const B = parse(b.current_attrs) || parse(b.attrs) || {};
  const sixA = parse(a.current_six) || {}, sixB = parse(b.current_six) || {};
  const head = (c, side) => `<div class="cmp-card ${side}">
      ${c.card_image_url ? `<img src="${esc(c.card_image_url)}" alt="">` : ''}
      <b>${esc(c.name)}</b>
      <span class="dim">OVR ${c.current_ovr ?? '-'}${c.card_ovr !== c.current_ovr ? ` <em class="d-evo">진화 전 ${c.card_ovr}</em>` : ''}</span>
      <span class="dim">${esc(c.positions || '')}</span>
      ${physLine(c) ? `<span class="dim">${physLine(c)}</span>` : ''}</div>`;
  /* ⭐ 차이를 **크고 색으로** 드러낸다(2026-09-22 사용자 지시).
     좌우 색은 경기 분석과 같은 규약을 쓴다 — 왼쪽 --viz-us(주황) · 오른쪽 --viz-them(파랑).
     차이가 클수록 배지를 키운다(5 이상 mid · 10 이상 big) — 눈으로 훑을 때 큰 격차가 먼저 걸린다. */
  const row = (k, va, vb, big) => {
    if (va == null && vb == null) return '';
    const d = (va ?? 0) - (vb ?? 0), mag = Math.abs(d);
    const step = mag >= 10 ? ' big' : mag >= 5 ? ' mid' : '';
    return `<tr${big ? ' class="big"' : ''}><td class="cmp-a ${d > 0 ? 'win' : d < 0 ? 'lose' : ''}">${va ?? '—'}</td>
      <td class="cmp-k">${esc(k)}${d ? `<b class="cmp-d ${d > 0 ? 'dA' : 'dB'}${step}">${d > 0 ? '◀' : '▶'}${mag}</b>` : ''}</td>
      <td class="cmp-b ${d < 0 ? 'win' : d > 0 ? 'lose' : ''}">${vb ?? '—'}</td></tr>`;
  };
  const sixRows = SIX.filter(k => sixA[k] != null || sixB[k] != null)
    .map(k => row(k, sixA[k], sixB[k], true)).join('');
  const keys = Object.keys(A).filter(k => B[k] != null);
  /* 위 6대 스탯 표와 **같은 기준**(fc_face_stats)으로 묶는다 — 어느 칸이 어느 face를 움직이는지
     한눈에 잇기 위해서다. 그룹 머리에 그 face의 실제 값도 같이 걸어 둔다. */
  const isGk = String(a.positions || '').includes('GK');
  const attrRows = groupByFace(keys, ctx.face_stats, isGk).map(gp => {
    const va = sixA[gp.abbr], vb = sixB[gp.abbr];
    return `<tr class="cmp-grp"><td class="cmp-a">${va ?? ''}</td>
        <td class="cmp-k">${esc(gp.abbr)}${SIX_KR[gp.abbr] ? ` <small>${SIX_KR[gp.abbr]}</small>` : ''}</td><td class="cmp-b">${vb ?? ''}</td></tr>`
      + gp.keys.map(k => row(k, A[k], B[k])).join('');
  }).join('');
  /* PlayStyle — 상세 패널과 같은 아이콘을 쓴다. 상대에게 없는 것만 초록으로 띄운다. */
  const psList = (c, other) => {
    const list = String(c.current_playstyles || '').split(',').map(x => x.trim()).filter(Boolean);
    if (!list.length) return '<span class="dim">없음</span>';
    return list.map(nm => {
      const plus = /\+$/.test(nm), base = nm.replace(/\s*\+$/, '');
      const d = PLAYSTYLES[base];
      const uniq = !other.includes(nm);
      return `<span class="fc-ps${plus ? ' plus' : ''}${uniq ? ' uniq' : ''}" title="${esc(base)}">
        ${d?.icon ? `<img src="${esc(d.icon)}" alt="" loading="lazy">` : ''}${esc(base)}${plus ? '<i>+</i>' : ''}</span>`;
    }).join('');
  };
  const pa = String(a.current_playstyles || '').split(',').map(x => x.trim());
  const pb = String(b.current_playstyles || '').split(',').map(x => x.trim());
  /* 역할 숙련 — raw id를 role_map으로 풀고 포지션을 붙인다(상세 패널과 같은 규칙). */
  const roles = (c, kind) => {
    const arr = parse(kind === 'plus' ? c.current_roles_plus : c.current_roles_plus_plus);
    if (!Array.isArray(arr)) return '<span class="dim">미수집</span>';
    if (!arr.length) return '<span class="dim">없음</span>';
    return arr.map(id => {
      const r = (ctx.role_map || []).find(x => x.game_version === 'FC27'
        && Number(x.ea_id) === Number(id) && x.kind === kind);
      return `<span class="chip">${r ? esc(r.position_name + ' ' + r.name) : '#' + id}</span>`;
    }).join(' ');
  };
  const winA = keys.filter(k => A[k] > B[k]).length, winB = keys.filter(k => B[k] > A[k]).length;
  const star = (c, k, max) => num(c[k]) == null ? '—'
    : `<span class="fc-star">${'★'.repeat(num(c[k]))}</span><span class="fc-star off">${'★'.repeat(Math.max(0, max - num(c[k])))}</span>`;
  return `<div class="fc-cmp">
    <div class="cmp-head">${head(a, 'sA')}<span class="cmp-vs">vs</span>${head(b, 'sB')}</div>
    <p class="dim" style="font-size:11.5px;margin:8px 0">29속성 기준 <b>${esc(a.name)} ${winA}개</b> ·
      <b>${esc(b.name)} ${winB}개</b> 우위. ⛔ <b>케미는 빼고 진화만 반영한</b> 카드 자체 값이다.</p>
    <table class="tbl cmp-tbl"><tbody>${sixRows}</tbody></table>

    <h4>PlayStyle</h4>
    <div class="cmp-two"><div class="fc-pslist">${psList(a, pb)}</div><div class="fc-pslist">${psList(b, pa)}</div></div>

    <h4>역할 숙련</h4>
    <div class="cmp-two">
      <div><div class="dim cmp-lab">Role++</div>${roles(a, 'plusplus')}<div class="dim cmp-lab">Role+</div>${roles(a, 'plus')}</div>
      <div><div class="dim cmp-lab">Role++</div>${roles(b, 'plusplus')}<div class="dim cmp-lab">Role+</div>${roles(b, 'plus')}</div>
    </div>

    <h4>스킬 · 주발 · 가속</h4>
    <table class="tbl cmp-tbl"><tbody>
      <tr><td class="cmp-a">${star(a, 'skill_moves', 5)}</td><td class="cmp-k">스킬무브</td><td class="cmp-b">${star(b, 'skill_moves', 5)}</td></tr>
      <tr><td class="cmp-a">${star(a, 'weak_foot', 5)}</td><td class="cmp-k">약발</td><td class="cmp-b">${star(b, 'weak_foot', 5)}</td></tr>
      <tr><td class="cmp-a">${esc(a.preferred_foot || '—')}</td><td class="cmp-k">주발</td><td class="cmp-b">${esc(b.preferred_foot || '—')}</td></tr>
      <tr><td class="cmp-a">${esc(a.accelerate || '—')}</td><td class="cmp-k">AcceleRATE</td><td class="cmp-b">${esc(b.accelerate || '—')}</td></tr>
    </tbody></table>

    <h4>체격</h4>
    <table class="tbl cmp-tbl"><tbody>
      ${row('키(cm)', a.height_cm, b.height_cm)}
      ${row('몸무게(kg)', a.weight_kg, b.weight_kg)}
    </tbody></table>
    <p class="dim" style="font-size:11px;margin:4px 0 0">⚠️ 키·몸무게는 <b>높다고 유리한 값이 아니다</b> —
      경합·속도에서 반대로 작동할 수 있어 색(초록)은 「큰 쪽」을 표시할 뿐이다.
      키는 AcceleRATE 판정에 관여한다(EA 1차).</p>

    ${emeryVerdict(a, b, ctx)}

    <h4>상세 스탯 <small class="dim">29속성</small></h4>
    <table class="tbl cmp-tbl"><tbody>${attrRows}</tbody></table>
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
/* ⭐ 2026-09-22: 전체적으로 좁게 쓰고 글씨가 작다는 지적 — 피치·사이드 모두 키웠다.
   사이드는 선수 프로필이 들어가는 칸이라 420 → **최대 560**까지 늘린다. */
.fc-layout{display:grid;grid-template-columns:minmax(0,820px) minmax(460px,660px);
  gap:24px;align-items:start;justify-content:center}
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
.fc-pitch{position:relative;aspect-ratio:85/100;height:min(880px,calc(100vh - 190px));
  width:auto;max-width:100%;margin:28px auto 52px;--fccard:17.5%;border-radius:10px;
  background:repeating-linear-gradient(0deg,var(--fcg1) 0 7%,var(--fcg2) 7% 14%);
  border:1px solid var(--line);overflow:visible}
.fc-lines{position:absolute;inset:8px;border:2px solid rgba(255,255,255,.18);border-radius:4px}
.fc-lines::before{content:"";position:absolute;left:0;right:0;top:50%;border-top:2px solid rgba(255,255,255,.18)}
.fc-lines::after{content:"";position:absolute;left:50%;top:50%;width:26%;aspect-ratio:1;transform:translate(-50%,-50%);
  border:2px solid rgba(255,255,255,.18);border-radius:50%}
.fc-slot{position:absolute;width:var(--fccard);transform:translate(-50%,50%)}
.fc-card{text-align:center;cursor:pointer;border-radius:8px;outline:none;transition:transform .12s}
.fc-card:hover,.fc-card:focus-visible{transform:translateY(-3px)}
/* ⭐ 선택 카드는 **키워서** 알린다(2026-09-22 사용자 지시) — 테두리만으로는 눈에 안 띄었다.
   ⛔ 확대는 **슬롯**에 건다. .fc-card에 transform을 주면 먹지 않는다(실측: 인라인으로 줘도
      getBoundingClientRect가 그대로였다) — 슬롯이 이미 translate(-50%,50%)를 쓰는 배치 박스라
      거기에 scale을 곱해야 한다. 벤치는 슬롯이 없어 카드에 직접 준다.
   ⚠️ 커지면 이웃과 겹치므로 z-index를 올려 **선택한 쪽이 위로** 오게 한다. */
.fc-slot.sel{z-index:5;transform:translate(-50%,50%) scale(1.28)}
.fc-card.sel .fc-artwrap{filter:drop-shadow(0 4px 10px rgba(0,0,0,.6))}
.fc-card.sel .fc-tag{border-color:var(--ok);background:rgba(4,30,14,.92)}
.fc-benchrow .fc-card.sel{transform:scale(1.18)}
/* 비교에 담긴 카드 — 선택(.sel)과 **다른 표시**를 쓴다. 담기는 상태이지 초점이 아니라서
   확대하면 피치가 흔들린다. 테두리 고리와 ✓만 붙인다. */
.fc-card.picked .fc-artwrap{filter:drop-shadow(0 0 0 2px var(--viz-us)) drop-shadow(0 4px 10px rgba(0,0,0,.6))}
.fc-card.picked::after{content:'✓';position:absolute;top:2px;left:2px;z-index:6;
  width:16px;height:16px;line-height:16px;text-align:center;border-radius:50%;
  background:var(--viz-us);color:#0b0f14;font-size:11px;font-weight:800}
.fc-slot.picked{z-index:4}
.fc-card.empty{opacity:.45;cursor:default}
.fc-artwrap{position:relative;line-height:0}
.fc-art{width:100%;display:block;filter:drop-shadow(0 3px 6px rgba(0,0,0,.55))}
.fc-art.ph{display:flex;flex-direction:column;align-items:center;justify-content:center;aspect-ratio:3/4;
  background:var(--panel);border:1px solid var(--line);border-radius:6px;line-height:1.2;font-size:11px;color:var(--dim)}
.fc-art.ph b{font-size:20px;color:var(--txt)}
/* 카드에 붙은 케미 스타일 아이콘 — 원본 PNG가 검은 실루엣이라 금색 카드 위에서 묻힌다.
   ⚠️ 초록 배경은 폐기했다(2026-09-20 사용자 지시 「녹색은 너무 안 어울려 · 좀 더 작게」).
   인게임과 같이 **어두운 원 + 흰 실루엣**으로 간다 — 카드의 금색과 싸우지 않는다.
   filter가 배경까지 반전시키므로 span으로 감싸고 **img에만** 반전을 건다. */
.fc-chem{position:absolute;right:-2%;top:8%;width:23%;aspect-ratio:1;border-radius:50%;
  background:#fff;box-shadow:0 0 0 1.5px rgba(0,0,0,.55),0 2px 5px rgba(0,0,0,.45);
  display:grid;place-items:center}
.fc-chem img{width:74%;display:block;filter:brightness(0)}
/* EVO 배지 — 카드 아래 pill 줄 안에 산다(위 card() 주석 참조). 떠 있지 않으므로 잘리지 않는다.
   ⚠️ 9.5px는 작아서 읽히지 않았다(2026-09-21) — 키우고 자간을 줘 숫자가 붙어 보이지 않게 한다. */
/* ⚠️ 밝은 초록 배경 + 어두운 글자는 11px에서 뭉개져 읽히지 않았다(2026-09-22 사용자 지적, 두 번째).
   카드 아래 pill 줄은 배경이 어두우므로 **어두운 pill + 밝은 초록 글자**가 대비가 가장 크다. */
.fc-evo{font-size:11px;font-weight:800;letter-spacing:.3px;
  background:rgba(3,18,9,.92);color:#5ee88a;border:1px solid rgba(94,232,138,.55);
  border-radius:99px;padding:1px 7px;white-space:nowrap;line-height:1.45}
.fc-evo.inline{display:inline-block}
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
/* 벤치 — 가로 스크롤 + 드래그로 밀 수 있다(enableDragScroll). */
.fc-benchrow{display:flex;gap:10px;overflow-x:auto;padding:4px 0 8px;cursor:grab}
.fc-benchrow.drag{cursor:grabbing;user-select:none}
.fc-benchrow.drag .fc-card{transform:none}
.fc-benchrow img{-webkit-user-drag:none;user-drag:none}
.fc-benchrow .fc-card{flex:0 0 auto;width:104px}
/* 벤치는 포지션 표기가 길다(CDM/CM/CAM) — pill이 카드보다 넓어지도록 두고 줄바꿈은 막는다. */
.fc-benchrow .fc-tag{max-width:none;font-size:9.5px;padding:2px 6px}
.fc-note{font-size:11px;color:var(--dim);margin:10px 0 0}
/* 사이드 패널 — 스크롤을 따라다니고, 길면 자기 안에서만 스크롤한다. */
.fc-side{position:sticky;top:12px;max-height:calc(100vh - 24px);overflow:auto;
  background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:16px 18px;font-size:13.5px}
.fc-kv{display:flex;justify-content:space-between;gap:12px;font-size:13.5px;padding:6px 0;border-bottom:1px dotted var(--line)}
.fc-kv span{color:var(--dim)}
.fc-roletbl td{font-size:12.5px;padding:5px 7px;vertical-align:top}
/* 선택된 카드로 돌아가는 길 — 상세를 열면 사이드 맨 위에 「팀 설정으로」 버튼이 붙는다. */
.fc-back{font-size:11.5px;margin-bottom:8px}
@media (max-width:1240px){
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
  /* ⚠️ 「표기」와 「적용」을 늘 두 열로 보이면 **개인 케미 3점에서는 항상 같은 값**이라 의미 없는 중복이다
     (2026-09-21 사용자 지적). 감쇠가 실제로 걸릴 때(1~2점)만 두 열로 가르고, 그 밖에는 한 열로 합친다. */
  const damped = scale !== 1;
  const sorted = pairs.sort((a, b) => b[1] - a[1]);
  const rows = sorted.map(([attr, raw]) => {
    const eff = Math.round(raw * scale);
    return `<tr><td>${esc(attr)}</td>` +
      (damped ? `<td class="dim">+${raw}</td>` : '') +
      `<td><span class="fc-boost${eff > 0 ? '' : ' zero'}">${eff > 0 ? '+' + eff : '0'}</span></td></tr>`;
  }).join('');
  return `<div class="fc-chemhead">
      <img src="assets/chemstyles/${st.ea_id}.png" alt=""><b>${esc(st.name)}</b>
      <span class="chip ${cp >= 3 ? 'ok' : 'dim'}">개인 케미 ${cp}/3</span></div>
    ${cp === 0 ? '<p class="dim" style="margin:4px 0">⚠️ 개인 케미 0이라 <b>부스트가 전혀 적용되지 않는다</b>(붙여둬도 효과 0).</p>' : ''}
    <table class="tbl fc-chemtbl"><thead><tr><th>속성</th>${damped ? '<th>표기</th>' : ''}<th>적용</th></tr></thead>
      <tbody>${rows}</tbody></table>
    ${damped
      ? `<p class="dim" style="font-size:11.5px;margin:4px 0 0">개인 케미 ${cp}/3이라 스타일 표기값의 <b>${cp === 2 ? '2/3' : '1/3'}</b>만 들어간다 — 왼쪽이 표기, 오른쪽이 실제.</p>`
      : `<p class="dim" style="font-size:11.5px;margin:4px 0 0">개인 케미 3/3이라 <b>표기값이 그대로 전부 적용된다</b>(감쇠 없음).</p>`}`;
}

/* PlayStyle — 이름만 쓰지 않고 아이콘을 붙인다(2026-09-20 사용자 지시 「플레이스타일도 아이콘으로」).
   아이콘·설명은 `assets/playstyle-icons.js`(fut.gg /api/fut/playstyles/ 원문)를 그대로 쓴다.
   ⚠️ 이름이 사전에 없으면 **아이콘 없이 이름만** 남긴다 — 빈 칸으로 만들지 않는다. */
function psBlock(csv) {
  if (!csv) return '';
  const items = String(csv).split(',').map(s => s.trim()).filter(Boolean).map(nm => {
    /* ⭐ PlayStyle+는 **이름 끝 `+`**로 표현된다(2026-09-20 확인 — `Dead Ball+`).
       사전은 `+` 없는 이름으로 키가 잡혀 있어, 떼고 조회하지 않으면 아이콘이 통째로 빠진다. */
    const plus = /\+$/.test(nm);
    const base = nm.replace(/\s*\+$/, '');
    const d = PLAYSTYLES[base];
    const tip = d ? (plus ? (d.plus || d.base) : d.base) || '' : base;
    return `<span class="fc-ps${plus ? ' plus' : ''}" title="${esc(base)}${plus ? '+' : ''} — ${esc(tip)}">
      ${d?.icon ? `<img src="${esc(d.icon)}" alt="" loading="lazy">` : ''}${esc(base)}${plus ? '<i>+</i>' : ''}</span>`;
  }).join('');
  return `<h4>PlayStyle</h4><div class="fc-pslist">${items}</div>`;
}

/* 「회」 = **밟은 단계 수**다(2026-09-21 사용자 결정 — 읽는 쪽 모델에 맞췄다. 4단계 완주 = 4회).
   ⚠️ **소진 판정은 다른 축**이다: 그건 「그 진화를 몇 번 적용했나」라서 1단계 기록만 센다
   (evolutions.html의 consumedMap). 여기 숫자를 소진 계산에 가져다 쓰면 반복형 잔여가 틀린다.
   ⛔ `evo_count`가 원장과 어긋나면 **원장(유효 로그 행 수)을 믿는다** — 스크립트가 +1 하는 값이라
   과거 재계산·중복 기록의 흔적이 남을 수 있다. */
function evoCountLabel(p, log) {
  const mine = (log || []).filter(l => l.club_player_id === p.id && !l.is_void);
  const n = mine.length || p.evo_count || 0;
  return `<small class="dim">${n}회 <span title="「회」는 밟은 단계 수다(4단계 완주 = 4회)">(단계)</span></small>`;
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

/* ⭐⭐ 진화 상승분을 **재구성**한다(2026-09-22 사용자 지시 「진화한 내역을 아니 진화 스탯을 알 수 있지 않아?」).
   EA는 진화 후 개별 속성을 공개하지 않지만, 우리는 ⑴ 기준 카드 29속성 ⑵ 밟은 진화·단계 기록
   ⑶ 카탈로그의 단계별 보상(속성·증가치·상한)을 갖고 있다 ⇒ 순서대로 캡을 씌워 더하면 복원된다.
   ⛔ 추정을 실측처럼 보이게 하지 않는다 — 재구성한 6대 스탯이 **EA 실측(current_six)과 일치하는지
      대조**해서, 맞으면 「검증됨」, 어긋나면 그 사실을 적고 기준 카드 값을 함께 남긴다.
   ⛔ 사용자가 고른 분기(upgradeOptions)가 있는 단계는 **무엇을 골랐는지 데이터에 없다** — 건너뛰고 알린다. */
/* ⭐⭐ **진화 상한 규칙 — 이 프로젝트에서 이 함수 하나만 안다**
   (2026-09-22, 사용자 지적 「각 메뉴가 개별적으로 업데이트되는가 — 동일한 상태를 갖도록」).
   같은 규칙을 화면마다 다시 짜면 **메뉴마다 다른 숫자**가 나온다. 적용 대상이 무엇이든 여기로 들어온다.
   ⛔ 상한을 이미 넘은 속성은 **그대로 둔다** — `Math.min(현재+증가, 상한)`이면 값이 **깎인다**
      (실증: 체력 82에 「+5(^76)」을 적용하면 76으로 내려갔다). 상한은 「여기까지만 올린다」는 뜻이다.
   ⚠️ 분기(`upgradeOptions`)가 2개 이상인 단계는 **적용하지 않는다** — 무엇을 골랐는지 모르면 추정이 된다.
      호출측이 `skipped`를 받아 화면에 밝힌다. */
export function applyEvoLevel(at, lv) {
  if ((lv.upgradeOptions || []).length > 1) return { ok: false, reason: '분기 선택 미기록' };
  for (const u of (lv.upgrades || [])) {
    const key = ATTR_KR[String(u.upgrade || '').replace(/^attribute_/, '')];
    if (!key || at[key] == null) continue;
    const cap = u.maxValue;
    at[key] = (cap != null && at[key] >= cap) ? at[key]
            : (cap != null ? Math.min(at[key] + u.value, cap) : at[key] + u.value);
  }
  return { ok: true };
}
/* 29속성 → 6대 스탯. 화면들이 각자 계산하지 않도록 내보낸다(구성식은 fc_face_stats가 정본). */
export function faceOf(at, faceRows, isGk = false) {
  const w = {};
  for (const r of faceRows || []) if (!!r.is_gk === !!isGk) (w[r.abbr] ??= {})[r.attr] = r.weight;
  const out = {};
  for (const k of Object.keys(w)) {
    const v = Object.entries(w[k]).reduce((t, [a, wt]) => t + wt * (at[a] ?? 0), 0);
    out[k] = Math.min(99, Math.floor(v + 0.501));
  }
  return out;
}

function evolvedAttrs(p, ctx) {
  const base = parse(p.attrs);
  if (!base) return null;
  const log = (ctx.log || []).filter(l => l.club_player_id === p.id && !l.is_void)
    .sort((a, b) => (a.applied_at || '').localeCompare(b.applied_at || '') || a.id - b.id);
  if (!log.length) return null;
  const cat = {}; for (const c of (ctx.catalog || [])) cat[c.evo_id] = c;
  const at = { ...base }; const applied = []; const skipped = [];
  for (const l of log) {
    const lv = (parse(cat[l.evo_id]?.levels) || []).find(x => Number(x.idx) === Number(l.level));
    if (!lv) { skipped.push(`${l.evo_name} ${l.level}단계(카탈로그 없음)`); continue; }
    const r = applyEvoLevel(at, lv);          // ⭐ 상한 규칙은 applyEvoLevel 하나만 안다
    if (!r.ok) { skipped.push(`${l.evo_name} ${l.level}단계(${r.reason})`); continue; }
    applied.push(`${l.evo_name} ${l.level}단계`);
  }
  return { at, base, applied, skipped };
}

/* EA 속성 키(영문 snake) → 우리 29속성 한글 키. 카탈로그 보상과 카드 속성을 잇는 유일한 다리다. */
export const ATTR_KR = {   // ⭐ 화면들이 같은 표를 쓰도록 내보낸다(2026-09-22)
  acceleration:'가속', sprint_speed:'질주 속도', positioning:'공격 위치 선정', finishing:'결정력',
  shot_power:'슈팅력', long_shots:'중거리슛', volleys:'발리 슛', penalties:'페널티킥',
  vision:'시야', crossing:'크로스', fk_accuracy:'프리킥 정확도', short_passing:'짧은 패스',
  long_passing:'긴 패스', curve:'커브', agility:'민첩성', balance:'균형 감각', reactions:'반응력',
  ball_control:'볼컨트롤', dribbling:'드리블', composure:'침착', interceptions:'차단력',
  heading_accuracy:'헤딩 정확도', def_awareness:'수비 위치 선정', standing_tackle:'스탠딩 태클',
  sliding_tackle:'슬라이딩 태클', jumping:'점프', stamina:'체력', strength:'힘', aggression:'공격성',
};

function attrBlock(p, ctx = {}) {
  const a0 = parse(p.attrs);
  /* ⭐⭐ 2026-09-22: GG Club이 **29속성을 EA 실측 그대로** 준다(사용자 질문에서 확인).
     ⇒ 실측이 있으면 그것이 정본이고, 재구성은 **검증용**으로만 쓴다(추정↔실측 대조 = 진화 기록 오류 탐지기).
     실측이 없을 때만(보호 중이거나 미수집) 재구성 추정을 보여주고 그 사실을 적는다. */
  const real = parse(p.current_attrs);
  if (!a0 && !real) return '<p class="dim">상세 스탯 미수집(결손 — 0이 아니다).</p>';
  const stale = p.card_ovr != null && p.current_ovr != null && p.card_ovr !== p.current_ovr;
  const rec = (stale && a0) ? evolvedAttrs(p, ctx) : null;
  const show = real || (rec ? rec.at : a0);
  if (real) {
    /* ⭐ 케미스트리까지 얹어 **인게임에서 실제로 뛰는 값**을 보여준다(2026-09-22 사용자 지시).
       EA가 주는 29속성은 **케미 미반영 카드값**이다 — 개인 케미로 감쇠한 부스트를 더해야 실전값이 된다.
       ⇒ 오른 몫을 둘로 갈라 색으로 구분한다: 진화 = 초록 · 케미 = 주황. */
    const st = (ctx.chem_styles || []).find(x => x.ea_id === p.chem_style_ea);
    const raw = st ? (parse(st.boosts) || {}) : {};
    const cp0 = p.chem_points ?? 0;
    const scale = cp0 >= 3 ? 1 : cp0 === 2 ? 2 / 3 : cp0 === 1 ? 1 / 3 : 0;
    const chemOf = k => Math.round((num(raw[k]) || 0) * scale);
    const one = k => { const v = real[k];
      const evo = a0 && a0[k] != null ? v - a0[k] : 0;
      const ch = chemOf(k);
      const fin = Math.min(99, v + ch);
      return `<div class="fc-attr"><span>${esc(k)}</span><b>${fin}` +
        (evo ? ` <small class="d-evo" title="진화 상승분">${evo > 0 ? '+' : ''}${evo}</small>` : '') +
        (ch ? ` <small class="d-chem" title="케미 스타일 ${esc(st?.name || '')} (개인 케미 ${cp0}/3)">+${ch}</small>` : '') +
        `</b></div>`; };
    /* 6대 스탯 카테고리로 묶는다 — 기준은 게임 구성식(`fc_face_stats`)이지 내 분류가 아니다.
       ⚠️ 머리의 수는 **바로 아래 칸들로 다시 계산한 값**이다. `current_six`를 그대로 쓰면
          케미가 빠진 카드값이라, 케미까지 얹은 아래 칸들과 어긋나 보인다(루제리 PAC 82 ↔ 가속·질주 88). */
    const fin0 = {}; for (const k of Object.keys(real)) fin0[k] = Math.min(99, real[k] + chemOf(k));
    const six0 = ctx.face_stats ? faceFrom(fin0, ctx.face_stats) : (parse(p.current_six) || {});
    const items0 = groupByFace(Object.keys(real), ctx.face_stats, String(p.positions || '').includes('GK'))
      .map(gp => `<div class="fc-agrp"><div class="fc-agrp-h">${esc(gp.abbr)}${
          SIX_KR[gp.abbr] ? ` ${SIX_KR[gp.abbr]}` : ''}${
          six0[gp.abbr] != null ? `<b>${six0[gp.abbr]}</b>` : ''}</div>
        <div class="fc-attrs">${gp.keys.map(one).join('')}</div></div>`).join('');
    const chemNote = st && scale > 0
      ? ` · <span class="d-chem">주황</span>은 케미 스타일 <b>${esc(st.name)}</b>(개인 케미 ${cp0}/3) 적용분이라 <b>인게임 실전값</b>이다`
      : (p.chem_style_ea ? ' · ⚠️ 개인 케미 0이라 케미 부스트는 <b>적용되지 않는다</b>' : '');
    /* 재구성이 가능하면 실측과 맞춰 본다 — 어긋나면 **진화 단계 기록이 틀린 것**이다. */
    let check = '';
    if (rec) {
      const diff = Object.keys(real).filter(k => rec.at[k] != null && rec.at[k] !== real[k]);
      /* ⚠️ 분기(upgradeOptions)를 건너뛴 단계가 있으면 어긋나는 게 당연하다 — 「기록 의심」이 아니라
         「대조 불가」다. 둘을 섞으면 멀쩡한 기록을 의심하게 된다. */
      check = rec.skipped.length
        ? `<span class="chip dim" title="${esc(rec.skipped.join(' · '))}">대조 불가 — 분기 선택이 기록돼 있지 않은 단계 ${rec.skipped.length}개</span>`
        : diff.length === 0
          ? '<span class="chip ok">진화 기록 검증됨 — 재구성과 실측이 전부 일치</span>'
          : `<span class="chip" style="border-color:var(--warn);color:var(--warn)">⚠️ 진화 기록 의심 — ${diff.length}개 어긋남(${esc(diff.slice(0, 4).join(', '))}${diff.length > 4 ? '…' : ''})</span>`;
    }
    return `<p class="dim" style="margin:0 0 6px;font-size:12px">EA 싱크 <b>실측</b>${stale && a0 ? ` · <span class="d-evo">초록</span>은 기준 카드(OVR ${p.card_ovr}) 대비 진화 상승분` : ''}${chemNote}. ${check}</p>
      ${items0}`;
  }
  /* 재구성 검증 — 복원한 속성으로 6대 스탯을 다시 계산해 EA 실측과 맞춰 본다. */
  let verdict = '';
  if (rec && ctx.face_stats) {
    const cur = parse(p.current_six) || {};
    const calc = faceFrom(rec.at, ctx.face_stats);
    const diff = SIX.filter(k => calc[k] != null && cur[k] != null && calc[k] !== cur[k]);
    verdict = diff.length === 0
      ? `<span class="chip ok">검증됨 — 재구성한 6대 스탯이 EA 실측과 6/6 일치</span>`
      : `<span class="chip" style="border-color:var(--warn);color:var(--warn)">⚠️ ${diff.length}개 불일치(${diff.map(k => `${k} 계산 ${calc[k]} ↔ 실측 ${cur[k]}`).join(' · ')})</span>`;
  }
  const one2 = k => { const v = show[k], d = rec && a0[k] != null ? v - a0[k] : 0;
    return `<div class="fc-attr"><span>${esc(k)}</span><b>${v}${d ? ` <small class="d-evo">${d > 0 ? '+' : ''}${d}</small>` : ''}</b></div>`; };
  const six1 = ctx.face_stats ? faceFrom(show, ctx.face_stats) : (parse(p.current_six) || {});
  const items = groupByFace(Object.keys(show), ctx.face_stats, String(p.positions || '').includes('GK'))
    .map(gp => `<div class="fc-agrp"><div class="fc-agrp-h">${esc(gp.abbr)}${
        SIX_KR[gp.abbr] ? ` ${SIX_KR[gp.abbr]}` : ''}${
        six1[gp.abbr] != null ? `<b>${six1[gp.abbr]}</b>` : ''}</div>
      <div class="fc-attrs">${gp.keys.map(one2).join('')}</div></div>`).join('');
  const head = !stale ? ''
    : rec && rec.applied.length
      ? `<p class="dim" style="margin:0 0 6px;font-size:12px">⭐ <b>진화 상승분을 반영한 추정치</b>다 —
          기준 카드(OVR ${p.card_ovr}) 29속성에 <b>${esc(rec.applied.join(' · '))}</b>의 보상을 상한까지 얹어 복원했다.
          <b class="up">+n</b>이 그 상승분이다. ${verdict}
          ${rec.skipped.length ? `<br>⛔ 반영하지 못한 단계: ${esc(rec.skipped.join(' · '))} — 그만큼 실제보다 낮게 나온다.` : ''}</p>`
      : `<p class="dim" style="margin:0 0 6px;font-size:12px">⚠️ 이 29속성은 <b>기준 카드(OVR ${p.card_ovr})</b>의 값이라
          <b>진화 상승분이 빠져 있다</b>(카탈로그에서 단계 보상을 찾지 못했다).</p>`;
  return head + items;
}

/* 상세 스탯을 **6대 스탯 카테고리로 묶는다**(2026-09-22 사용자 지시 「상세 스탯도 카테고리가 있어서
   구분할 수 있지 않아? 여기랑 같은 기준으로」 — 위 6대 스탯 표를 가리켰다).
   ⭐ 기준을 새로 만들지 않는다 — **`fc_face_stats`가 곧 그 기준**이다. 게임이 PAC를 계산할 때 쓰는
      구성식 그대로라, 여기서 묶은 카테고리와 위 표의 6대 스탯 값이 **같은 규칙**을 공유한다.
   ⚠️ 어느 face에도 안 걸리는 속성이 있을 수 있다(구성식에 안 들어가는 속성) — 버리지 않고
      「기타」로 모은다. 조용히 사라지면 29속성이 아니게 된다.
   ⚠️ `is_gk` 행은 필드 선수와 어휘가 겹치므로(가속·질주 속도) **카드에 맞는 쪽만** 쓴다. */
function groupByFace(keys, faceRows, isGk) {
  const rows = (faceRows || []).filter(r => !!r.is_gk === !!isGk);
  const order = [], of = {};
  for (const r of rows) { if (!order.includes(r.abbr)) order.push(r.abbr); of[r.attr] ??= r.abbr; }
  const g = new Map(order.map(k => [k, []]));
  const rest = [];
  for (const k of keys) { const f = of[k]; if (g.has(f)) g.get(f).push(k); else rest.push(k); }
  /* ⚠️ 순서는 **카드에 찍힌 순서(SIX)**로 고정한다 — export가 abbr 알파벳순으로 주는 바람에
     DEF가 맨 위로 올라와 위 6대 스탯 표와 줄이 어긋났다(2026-09-22 실측). */
  const rank = k => { const i = SIX.indexOf(k); return i < 0 ? 99 : i; };
  const out = order.filter(k => g.get(k).length).sort((x, y) => rank(x) - rank(y))
    .map(k => ({ abbr: k, keys: g.get(k) }));
  if (rest.length) out.push({ abbr: '기타', keys: rest });
  return out.length ? out : [{ abbr: '', keys }];
}

/* 29속성 → 6대 스탯(fc_face_stats 가중). 게임 반올림과 같게 floor(x+0.501). */
function faceFrom(at, faceRows) {
  const w = {};
  for (const r of faceRows) if (!r.is_gk) (w[r.abbr] ??= {})[r.attr] = r.weight;
  const out = {};
  for (const k of SIX) {
    if (!w[k]) continue;
    const v = Object.entries(w[k]).reduce((t, [a, wt]) => t + wt * (at[a] ?? 0), 0);
    out[k] = Math.min(99, Math.floor(v + 0.501));
  }
  return out;
}

/* 추천 케미 스타일 (2026-09-20 사용자 지시 「적용 케미에 추천 케미도 표시 — fut.gg 스코어와
   에메리 전술 구현에 필요한 케미 **두 가지 정보를 모두**」).
   ⑴ **에메리 기준**: 정본 슬롯 역할 가중 × 실제 상승분(상한 99 반영). 계산은 케미스트리 탭과 동일.
   ⑵ **메타 관습**: 커뮤니티 가이드 합의(fifauteam·nealguides 등). 우리 계산과 **다른 기준**이라 나란히 둔다.
   ⛔ fut.gg의 선수별 케미 등급·커뮤니티 투표율은 **아직 원장에 없다** — 없는 값을 지어내지 않고
      그 사실을 화면에 적는다(결손은 0이 아니다). */
function recoBlock(p, reco, styles) {
  if (!reco) return '';
  if (!reco.ranked?.length) return `<h4>추천 케미스트리</h4>
    <p class="dim">29속성 미수집이라 추천을 계산할 수 없다(결손 — 추천 없음이 아니다).</p>`;
  const nowName = (styles || []).find(s => s.ea_id === p.chem_style_ea)?.name;
  const basisKr = { slot: '정본 슬롯 역할(에메리 재현)', pres: '이 선수의 시즌 처방',
                    auto: `속성 기반 자동 선택 · 적합 ${reco.autoFit}%`, pos: '카드 주 포지션 기본 역할' }[reco.basis];
  /* ⚠️ 1·2위가 같은 점수면 「추천」은 사실상 임의 선택이다 — 프로젝트 규약(실측 무결정)대로 그 사실을 적는다. */
  const tied = reco.ranked.length > 1 && Math.round(reco.ranked[0].score) === Math.round(reco.ranked[1].score);
  const rows = reco.ranked.map((s, i) => {
    const same = nowName && s.name === nowName;
    return `<tr${i ? ' style="opacity:.62"' : ''}>
      <td>${i ? `<span class="dim">차선 ${i}</span>`
        : `<span class="fc-boost${tied ? ' zero' : ''}">${tied ? '동점' : '에메리 추천'}</span>`}</td>
      <td><b>${esc(s.name)}</b>${same ? ' <small class="dim">= 지금</small>' : ''}</td>
      <td style="text-align:right">${Math.round(s.score)}</td></tr>`;
  }).join('');
  /* ⭐ 「에메리 점수」가 무엇인지 표에서 바로 알 수 있어야 한다(2026-09-21 사용자 지시 「툴팁으로 설명」). */
  const SCORE_TIP = '이 자리의 정본 역할(에메리 재현)이 중요하게 보는 속성마다 가중치를 매기고, '
    + '그 케미 스타일이 실제로 올려주는 양(속성 상한 99를 넘는 몫은 버린다)을 곱해 합한 값입니다. '
    + '높을수록 이 역할 수행에 보탬이 큽니다. 절대 단위가 아니라 스타일끼리 비교하는 용도입니다.';
  const head = `<thead><tr><th></th><th>스타일</th>
    <th style="text-align:right"><span class="fc-help" tabindex="0" data-tip="${esc(SCORE_TIP)}">에메리 점수<i>?</i></span></th></tr></thead>`;
  const top = reco.ranked[0];
  const why = (top.top || []).map(x => `${x.a} +${x.gain}`).join(' · ');
  return `<h4>추천 케미스트리 <small class="dim">— 에메리 전술 기준</small></h4>
    <p class="dim" style="font-size:11.5px;margin:0 0 6px">기준 역할 <b>${esc(reco.roleKr || '—')}</b>
      <small>(${esc(basisKr || '')})</small></p>
    <table class="tbl fc-recotbl">${head}<tbody>${rows}</tbody></table>
    ${futggBlock(reco.futgg, nowName)}
    ${tied ? `<p class="dim" style="font-size:11.5px;margin:4px 0 0">⚠️ 상위 스타일이 <b>동점</b>이다 —
      이 역할 기준으로는 구분되지 않는다. 아래 fut.gg 신호(AcceleRATE·투표)나 취향으로 고르면 된다.</p>` : ''}
    <p class="dim" style="font-size:11.5px;margin:6px 0 0">점수 = Σ(역할 가중 × <b>실제 상승분</b>) —
      ${why ? esc(why) : '해당 역할 핵심 속성에 걸리는 상승 없음'}.
      ⚠️ 속성 상한 99라 이미 높은 칸에 붙는 부스트는 낭비로 빠진다.
      ${reco.bench ? '<br>⚠️ 교체 선수는 <b>투입 전까지 개인 케미가 0</b>이라 스타일 효과도 0이다.' : ''}</p>
`;
}

/* fut.gg 신호 (2026-09-21 수집, migration 055) — 우리 계산과 **다른 축**이라 따로 둔다.
   ⚠️⚠️ fut.gg의 스타일 옆 배지는 **케미 등급이 아니다**. 실측으로 확정했다(카마라 전 스타일 C /
   음바페 Sniper·Architect만 C) — 그 스타일을 붙였을 때의 **AcceleRATE**다. 「등급」으로 읽으면
   순위를 매기는 값으로 오해한다. 투표율은 **인기이지 정답이 아니다**. */
function futggBlock(fg, nowName) {
  if (!fg || !fg.rows?.length) return `<p class="dim" style="font-size:11.5px;margin:8px 0 0">
    <b>fut.gg 신호</b> — 이 카드는 아직 수집되지 않았다(결손).</p>`;
  const voted = fg.rows.filter(r => r.vote_pct != null).sort((a, b) => b.vote_pct - a.vote_pct).slice(0, 3);
  const bars = voted.map(r => `<div class="fc-vote"><span>${esc(r.style_name)}${r.style_name === nowName ? ' <small class="dim">= 지금</small>' : ''}</span>
      <i><b style="width:${Math.min(100, r.vote_pct)}%"></b></i><em>${r.vote_pct}%</em></div>`).join('');
  /* 현재 붙인 스타일의 AcceleRATE를 먼저 보여준다 — 스타일을 바꾸면 가속 타입이 바뀔 수 있다. */
  const cur = fg.rows.find(r => r.style_name === nowName);
  const byAccel = {};
  for (const r of fg.rows) if (r.accelerate) (byAccel[r.accelerate] ??= []).push(r.style_name);
  /* ⭐ 개수만 세면 「무엇을 붙여야 바뀌는지」를 알 수 없다(2026-09-21 사용자 지적).
     현재와 **다른** 타입을 만드는 스타일을 이름으로 적는다 — 그게 이 표의 유일한 행동 가능 정보다. */
  const curAccel = cur?.accelerate || null;
  const changers = Object.entries(byAccel).filter(([k]) => k !== curAccel)
    .sort((a, b) => b[1].length - a[1].length);
  const accelSummary = Object.entries(byAccel).sort((a, b) => b[1].length - a[1].length)
    .map(([k, v]) => `${k} ${v.length}종`).join(' · ');
  const changeHtml = !curAccel ? ''
    : changers.length
      ? `<div style="margin-top:4px">${changers.map(([k, v]) =>
          `<div class="fc-kv"><span>${esc(k)}로 바뀜</span><b style="font-weight:400;text-align:right;font-size:11.5px">${esc(v.join(', '))}</b></div>`).join('')}</div>`
      : `<p class="dim" style="font-size:11.5px;margin:4px 0 0">어떤 스타일을 붙여도 <b>${esc(curAccel)}</b> 그대로다 — 이 카드는 AcceleRATE가 바뀌지 않는다.</p>`;
  return `<div class="fc-futgg">
    <h4 style="margin:12px 0 6px">fut.gg 신호 <small class="dim">커뮤니티</small></h4>
    ${cur ? `<div class="fc-kv"><span>지금 스타일의 AcceleRATE</span><b>${esc(cur.accelerate || '—')}</b></div>` : ''}
    <div class="fc-kv"><span>스타일별 AcceleRATE</span><b style="font-weight:600">${esc(accelSummary || '—')}</b></div>
    ${changeHtml}
    ${bars ? `<div>${bars}</div>`
           : '<p class="dim" style="font-size:11.5px;margin:6px 0 0">커뮤니티 투표 없음(결손 — 0표라는 뜻이지 비추천이 아니다).</p>'}
    <p class="dim" style="font-size:11.5px;margin:6px 0 0">⚠️ fut.gg 배지는 <b>등급이 아니라 그 스타일을 붙였을 때의 AcceleRATE</b>다(실측 확인).
      투표율은 <b>인기이지 정답이 아니다</b> — 위 역할 점수와 갈리면 역할 점수를 따른다.</p></div>`;
}

/* 스킬무브·약발·주발·AcceleRATE + Role+/++ (2026-09-21 사용자 지시 「스킬과 주발과 역할 정보를 추가해」).
   ⛔ Role+/++는 원장에 **raw ea_id**로 들어 있다(docs/21 ②) — `role_map`으로 이름을 붙이고,
      매핑에 없으면 지어내지 않고 id를 그대로 보여준다(결손을 감추지 않는다). */
/* AcceleRATE 설명 — 값만 보여주면 뭘 뜻하는지 알 수 없다(2026-09-22 사용자 지시).
   ⚠️ 판정식은 EA가 공개한 적이 없다(커뮤니티 데이터마이닝) — **등급을 명시**해 적는다(불변규칙 12). */
const ACCEL_TIP = '가속 곡선의 유형이다. Explosive는 초반 몇 걸음이 빠르고 최고속 유지가 약하며, '
  + 'Lengthy는 출발이 느린 대신 길게 달릴수록 빨라진다. Controlled는 그 중간이다. '
  + '민첩성·밸런스가 힘보다 충분히 높고 가속이 일정 이상이면 Explosive, 반대로 힘이 크게 높으면 Lengthy, '
  + '그 밖에는 Controlled가 된다 — 그래서 케미 스타일로 힘·민첩성이 바뀌면 유형이 갈리기도 한다. '
  + '⚠️ 정확한 임계값은 EA 1차 자료에 없다(커뮤니티 해석, D등급). ⭐ FC27은 유형 간 차이를 줄이고 '
  + '가속·질주 속성 비중을 높였다(EA 1차, HIGH).';

/* 체격 한 줄 — 키·몸무게는 카드 표(player_card_items)에 있다.
   ⛔ 없으면 그 항목을 아예 빼고 쓴다 — 「—」를 나열하면 결손이 값처럼 보인다.
   ⚠️ 나이는 생년에서 계산한다(EA는 카드에 나이를 따로 주지 않는다). */
function physLine(p) {
  const bits = [];
  if (p.height_cm) bits.push(`${p.height_cm}cm`);
  if (p.weight_kg) bits.push(`${p.weight_kg}kg`);
  if (p.birthdate) {
    const d = new Date(p.birthdate);
    if (!isNaN(d)) {
      const n = new Date(); let age = n.getFullYear() - d.getFullYear();
      const m = n.getMonth() - d.getMonth();
      if (m < 0 || (m === 0 && n.getDate() < d.getDate())) age--;
      if (age > 0 && age < 60) bits.push(`${age}세`);
    }
  }
  return bits.join(' · ');
}

const STARS = (n, max = 5) => n == null ? '—'
  : `<span class="fc-star">${'★'.repeat(n)}</span><span class="fc-star off">${'★'.repeat(Math.max(0, max - n))}</span>`;

/* AcceleRATE 설명 — 유형·판정축·성능차를 한 곳에 모은다(2026-09-22 사용자 요청).
   ⭐ EA 1차로 확인된 것은 둘뿐이다(game_system_changes, HIGH):
      ⑴ FC27은 **3종으로 회귀**했고(Explosive/Controlled/Lengthy) **2차 속성은 힘(Strength)**이다.
      ⑵ FC27은 **유형 간 차이를 일부러 줄이고** 가속·질주 속성 비중을 높였다(여성 Lengthy 키 하한 172cm).
   ⛔ 구체 임계값과 구간별 속도 곡선은 **EA가 공개한 적이 없다** — 커뮤니티 해석(D등급)이고
      우리 원장에도 **통제 실측(C등급)·데이터마이닝(B등급)이 0건**이다(리서치 §한계, 재조사 10월 중순).
      ⇒ 처방 근거로 쓰지 않는다. */
function accelTable(p) {
  const at = parse(p.current_attrs) || parse(p.attrs) || {};
  const ag = at['민첩성'], st = at['힘'], ac = at['가속'];
  const gap = (ag != null && st != null) ? ag - st : null;
  const ROWS = [
    ['Explosive',  '민첩성 > 힘',  '초반 몇 걸음이 가장 빠르다. 최고속 유지는 약해 길게 달리면 따라잡힌다.'],
    ['Controlled', '민첩성 ≈ 힘',  '출발과 최고속이 고르다. 어느 쪽에도 크게 유리하거나 불리하지 않다.'],
    ['Lengthy',    '힘 > 민첩성',  '출발이 무겁지만 길게 달릴수록 빨라진다. 긴 공간 경합에 강하다.'],
  ];
  const cur = String(p.accelerate || '');
  return `<details class="fc-acc"><summary>AcceleRATE — 유형 차이와 판정 축</summary>
    <p class="dim" style="font-size:11.5px;margin:6px 0">이 카드: 민첩 <b>${ag ?? '—'}</b> · 힘 <b>${st ?? '—'}</b>
      ${gap != null ? `(민첩−힘 <b>${gap > 0 ? '+' : ''}${gap}</b>)` : ''} · 가속 <b>${ac ?? '—'}</b></p>
    <table class="tbl"><thead><tr><th>유형</th><th>판정 축</th><th>달리기 특성</th></tr></thead><tbody>
    ${ROWS.map(r => `<tr${cur && r[0] === cur ? ' style="background:rgba(94,232,138,.10)"' : ''}>
      <td><b>${r[0]}</b></td><td>${r[1]}</td><td class="dim">${r[2]}</td></tr>`).join('')}
    </tbody></table>
    <p class="dim" style="font-size:11.5px;margin:7px 0 0">
      ⭐ <b>EA 1차로 확인된 것</b>(HIGH): FC27은 <b>3종으로 회귀</b>했고 <b>2차 속성은 힘</b>이다 ·
      FC27은 <b>유형 간 차이를 일부러 줄이고</b> 가속·질주 속성 비중을 높였다(키도 관여 — 여성 Lengthy 하한 172cm).<br>
      ⛔ <b>구간별 속도 수치·정확한 임계값은 공개된 적이 없다.</b> 우리 원장에도 통제 실측·데이터마이닝이
      <b>0건</b>이라(FC27 출시 전 리서치) 「몇 m에서 몇 초」류를 말할 근거가 없다 — <b>재조사 10월 중순</b>.
      ⚠️ 몸무게가 판정에 들어간다는 근거는 찾지 못했다.<br>
      ⭐ 케미 스타일로 민첩·힘이 바뀌면 유형이 갈릴 수 있다 — 위 「fut.gg 신호」의 스타일별 AcceleRATE가 그 결과다.</p></details>`;
}

function traitRow(p, roleMap) {
  /* id 공간은 kind마다 갈린다(plus 1–49 · plusplus 101–149) — kind까지 맞춰 찾는다. */
  const names = (ids, kind) => {
    const arr = parse(ids); if (!Array.isArray(arr) || !arr.length) return [];
    /* ⚠️ 이름만 쓰면 **같은 이름이 중복으로 보인다** — 역할명은 포지션마다 별도 id다
       (16=CDM Deep-Lying Playmaker · 20=CM Deep-Lying Playmaker). 포지션을 앞에 붙여 구분한다. */
    return arr.map(id => {
      const r = (roleMap || []).find(x => x.ea_id === id && x.kind === kind);
      return r ? `${r.position_name} ${r.name}` : `#${id}`;
    });
  };
  const pp = names(p.current_roles_plus_plus, 'plusplus'), pl = names(p.current_roles_plus, 'plus');
  const foot = p.preferred_foot ? String(p.preferred_foot).replace('오른쪽', '오른발').replace('왼쪽', '왼발') : null;
  /* ⭐ 수행 가능 포지션과 그 포지션에서 고를 수 있는 역할(2026-09-21 사용자 지시 「선수의 역할이 없어
     수행할 수 있는 포지션과 역할도 추가」). Role+/++가 비어 있어도 **고를 수 있는 역할은 존재한다** —
     숙련(+)이 없을 뿐이다. 보유한 숙련은 굵게 표시해 구분한다. */
  const owned = new Set([...pp, ...pl]);
  const posRoles = String(p.positions || '').split('/').map(x => x.trim()).filter(Boolean).map(pos => {
    const list = (roleMap || []).filter(r => r.kind === 'plus' && r.position_name === pos);
    if (!list.length) return `<div class="fc-kv"><span>${esc(pos)}</span><b class="dim">역할 목록 미수집</b></div>`;
    const names = list.map(r => owned.has(`${r.position_name} ${r.name}`)
      ? `<b class="up">${esc(r.name)}+</b>` : esc(r.name)).join(', ');
    return `<div class="fc-kv"><span>${esc(pos)}</span><b style="font-weight:400;text-align:right">${names}</b></div>`;
  }).join('');
  return `<h4>수행 가능 포지션 · 역할</h4>
    ${posRoles || '<p class="dim">카드 포지션 미수집.</p>'}
    <p class="dim" style="font-size:11.5px;margin:4px 0 0">그 포지션에서 <b>고를 수 있는 역할 전부</b>다.
      <b class="up">굵은 초록+</b>는 이 카드가 <b>숙련(Role+/++)</b>을 가진 역할 — 없다고 못 쓰는 건 아니고 보너스가 없을 뿐이다.</p>
    <h4>스킬 · 주발 · 역할 숙련</h4>
    <div class="fc-kv"><span>스킬무브</span><b>${STARS(num(p.skill_moves))}</b></div>
    <div class="fc-kv"><span>약발</span><b>${STARS(num(p.weak_foot))}</b></div>
    <div class="fc-kv"><span>주발</span><b>${esc(foot || '—')}</b></div>
    <div class="fc-kv"><span class="fc-help" tabindex="0" data-tip="${esc(ACCEL_TIP)}">AcceleRATE<i>?</i></span><b>${esc(p.accelerate || '—')}</b></div>
    ${accelTable(p)}
    <div class="fc-kv"><span>Role++</span><b>${pp.length ? esc(pp.join(', ')) : '<span class="dim">없음</span>'}</b></div>
    <div class="fc-kv"><span>Role+</span><b>${pl.length ? esc(pl.join(', ')) : '<span class="dim">없음</span>'}</b></div>`;
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
      <div class="fc-dinfo">
        <h3>${esc(p.name)}</h3>
        <div class="fc-dovr"><b>${p.current_ovr ?? '-'}</b><span>OVR</span>
          ${p.card_ovr !== p.current_ovr ? `<em class="up">진화 전 ${p.card_ovr}</em>` : ''}</div>
        <div class="fc-dmeta">${esc(p.positions || '')} · ${esc(p.club || '')}<br>${esc(p.league || '')} · ${esc(p.nation || '')}
          ${physLine(p) ? `<br>${physLine(p)}` : ''}</div>
        <div class="fc-dsix">${SIX.map(k => `<span><i>${k}</i><b>${cur?.[k] ?? '—'}</b></span>`).join('')}</div>
        <div class="fc-dchips">
          ${p.chem_style_ea ? `<span class="chip">케미 ${p.chem_points ?? 0}/3</span>` : ''}
          ${/* ⚠️ 호출측이 횟수를 알고 있으면 그걸 쓴다(2026-09-22 사용자 지적 「진화 0회는 잘못된 정보」).
                 진화 경로 카드는 `p.id`(보유 행 id)가 없는 **가상 카드**라 로그로 셀 수 없었다. */''}
          <span class="chip">진화 ${ctx.evo_runs != null ? ctx.evo_runs
            : (ctx.log || []).filter(l => l.club_player_id === p.id && !l.is_void).length}회</span>
          ${num(p.skill_moves) ? `<span class="chip">스킬 ${num(p.skill_moves)}★</span>` : ''}
          ${num(p.weak_foot) ? `<span class="chip">약발 ${num(p.weak_foot)}★</span>` : ''}
          ${p.accelerate ? `<span class="chip dim">${esc(p.accelerate)}</span>` : ''}
        </div>
        <div style="margin-top:8px">${prof}</div>
      </div>
    </div>
    ${/* ⚠️ `position_name`이 비면 **빈 버튼**이 남는다 — 값이 있을 때만 칸을 만든다(2026-09-22). */''}
    ${role ? `<h4>이 자리의 전술</h4><div class="plist">${role.position_name ? `<button disabled>${esc(role.position_name)}</button>` : ''}
      <button disabled>역할 <b>${esc(role.role_name)}</b></button><button disabled>포커스 <b>${esc(role.focus)}</b></button></div>
      ${ctx.team ? `<div class="plist" style="margin-top:4px"><button disabled>빌드업 ${esc(ctx.team.build_up_style)}</button>
      <button disabled>수비 ${esc(ctx.team.defensive_approach)}</button><button disabled>라인 ${ctx.team.line_height}</button></div>` : ''}`
      /* ⭐ 처방이 없으면 **조용히 빼지 않는다**(2026-09-22 사용자 질문 「이 영역이 있는 선수와 없는 선수의 차이가 뭐야?」).
         빠진 이유가 화면에 없으면 「이 선수는 전술이 없다」로 오독된다 — 결손과 0은 다르다(obs#132). */
      : (ctx.no_role_note ? `<h4>이 자리의 전술</h4><p class="dim" style="font-size:12px;margin:0">
          ${esc(ctx.no_role_note)}</p>` : '')}
    <h4>상세 스탯</h4>${attrBlock(p, ctx)}
    ${traitRow(p, ctx.role_map)}
    <h4>현재 카드 스탯</h4>${sixRow(cur, base)}
    ${psBlock(p.current_playstyles)}
    <h4>진화 상태 ${evoCountLabel(p, ctx.log)}</h4>${evoBlock(p, ctx.log)}
    <h4>적용된 케미스트리</h4>${chemBlock(p, ctx.chem_styles)}
    ${recoBlock(p, ctx.reco, ctx.chem_styles)}

  </div>`;
}

export const FC_DETAIL_CSS = `
/* ⚠️ 사이드 패널은 420px다 — 표를 그대로 두면 마지막 열이 패널 밖으로 밀려 잘린다
   (2026-09-20 사용자 지적 「케미스트리 색 변경 안 됨」의 실제 원인은 색이 아니라 **열 잘림**이었다).
   table-layout:fixed로 폭을 강제하고 숫자 열을 오른쪽에 고정한다. */
.fc-detail .tbl{width:100%;table-layout:fixed}
.fc-detail .tbl th,.fc-detail .tbl td{padding:5px 7px;font-size:13px;overflow:hidden;text-overflow:ellipsis}
.fc-chemtbl th:nth-child(n+2),.fc-chemtbl td:nth-child(n+2){width:58px;text-align:right}
.fc-detail h4{margin:16px 0 7px;font-size:14.5px}
.fc-pslist{display:flex;flex-wrap:wrap;gap:6px}
.fc-ps{display:inline-flex;align-items:center;gap:6px;font-size:13px;font-weight:600;
  background:var(--bg);border:1px solid var(--line);border-radius:99px;padding:3px 9px 3px 4px}
/* ⚠️ img에 background와 filter를 **함께 주지 않는다**(2026-09-21): filter는 배경까지 적용돼
   흰 배경이 검은 원이 된다. fut.gg PlayStyle 아이콘은 원본이 이미 흰 배경 + 검은 그림이라
   아무것도 덧칠할 필요가 없다 — 모서리만 둥글린다. */
.fc-ps img{width:19px;height:19px;display:block;border-radius:50%;background:#fff}
.fc-ps.plus{border-color:var(--ok)}
.fc-ps.plus i{font-style:normal;font-weight:800;color:var(--ok);margin-left:1px}
.fc-recotbl td{font-size:12px}
/* ⛔ CSS ::after 툴팁은 **overflow:auto 안에서 잘린다** — 사이드 패널이 그래서 안 보였다
   (2026-09-22 사용자 지적 「에메리 점수 툴팁이 여전히 안 나와」). body에 띄우는 JS 툴팁으로 바꿨다. */
.fc-help{position:relative;border-bottom:1px dotted var(--dim);cursor:help;outline:none}
.fc-help i{font-style:normal;display:inline-block;margin-left:3px;width:13px;height:13px;line-height:13px;
  text-align:center;border-radius:50%;background:var(--line);color:var(--txt);font-size:9.5px;vertical-align:1px}
.fc-vote{display:flex;align-items:center;gap:6px;font-size:11.5px;margin:3px 0}
.fc-vote span{flex:0 0 96px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.fc-vote i{flex:1;height:7px;border-radius:99px;background:var(--bg);overflow:hidden}
.fc-vote i b{display:block;height:100%;background:var(--acc);border-radius:99px}
.fc-vote em{flex:0 0 36px;text-align:right;font-style:normal;font-weight:700}
/* 상세 헤더 — 카드 옆에 **한눈에 필요한 것**을 모은다(2026-09-22 사용자 지시 「재배치해서 더 잘 알 수 있게」):
   이름 → 큰 OVR(진화 전 병기) → 포지션·소속 → 6대 스탯 → 요약 칩(케미·진화·스킬·약발·가속). */
.fc-dhead{display:flex;gap:16px;align-items:flex-start}
.fc-dinfo{min-width:0;flex:1}
.fc-dovr{display:flex;align-items:baseline;gap:6px;margin:2px 0 6px}
.fc-dovr b{font-size:34px;line-height:1;font-weight:800}
.fc-dovr span{font-size:12px;color:var(--dim);letter-spacing:.5px}
.fc-dovr em{font-style:normal;font-size:12px;font-weight:700;margin-left:4px}
.fc-dmeta{font-size:12.5px;color:var(--dim);line-height:1.5}
.fc-dsix{display:grid;grid-template-columns:repeat(6,1fr);gap:4px;margin:10px 0 8px;text-align:center}
.fc-dsix i{display:block;font-style:normal;font-size:10px;color:var(--dim);letter-spacing:.3px}
.fc-dsix b{display:block;font-size:16px;font-weight:800;line-height:1.2}
.fc-dchips{display:flex;flex-wrap:wrap;gap:5px}
.fc-dchips .chip{font-size:11.5px}
.fc-dart{width:196px;flex:0 0 auto}
.fc-dhead h3{margin:0 0 4px;font-size:19px}
.fc-chemhead{display:flex;gap:8px;align-items:center;margin-bottom:6px}
.fc-chemhead img{width:26px;padding:4px;box-sizing:border-box;border-radius:50%;
  background:#fff;box-shadow:0 0 0 1px rgba(0,0,0,.5)}
/* 상세 스탯 카테고리 — 머리에 그 face의 실제 값을 걸어 「이 칸들이 이 수를 만든다」가 보이게 한다. */
.fc-agrp + .fc-agrp{margin-top:10px}
.fc-agrp-h{display:flex;align-items:baseline;gap:6px;font-size:11px;font-weight:800;letter-spacing:.06em;
  color:var(--acc);border-bottom:1px solid var(--line);padding-bottom:2px;margin-bottom:4px}
.fc-agrp-h b{font-size:14px;color:var(--fg)}
.fc-attrs{display:grid;grid-template-columns:repeat(auto-fill,minmax(170px,1fr));gap:3px 14px}
.fc-attr{display:flex;justify-content:space-between;font-size:13px;padding:3px 0;border-bottom:1px dotted var(--line)}
.fc-attr span{color:var(--dim)}
/* 상승분 색 구분 — 진화(초록) ↔ 케미(주황). 값이 둘 다 있으면 나란히 붙는다. */
.d-evo{color:var(--ok);font-weight:700}
.d-chem{color:var(--acc);font-weight:700}
.fc-acc{margin:6px 0 2px}
.fc-acc > summary{cursor:pointer;font-size:12px;color:var(--acc)}
.fc-acc .tbl{width:100%;table-layout:auto;margin-top:6px}
.fc-acc .tbl td,.fc-acc .tbl th{font-size:11.5px;padding:3px 6px}
/* 카드 비교 */
.cmp-head{display:grid;grid-template-columns:1fr auto 1fr;align-items:end;gap:10px;text-align:center}
.cmp-card{position:relative}
.cmp-card img{width:150px;display:block;margin:0 auto 6px}
.cmp-card b{display:block;font-size:15px}
.cmp-card span{display:block;font-size:11.5px}
.cmp-card em{font-style:normal;font-size:11px}
.cmp-vs{color:var(--dim);font-size:13px;font-weight:700;padding-bottom:26px}
.fc-cmp h4{margin:16px 0 7px;font-size:14px}
.cmp-tbl{width:100%;table-layout:fixed}
.cmp-tbl td{padding:4px 6px;font-size:13px}
.cmp-tbl tr.big td{font-size:15px;font-weight:800}
/* 상세 스탯 안의 카테고리 머리줄 — 값 칸에는 그 face의 실제 값이 들어가 위 6대 스탯 표와 이어진다. */
.cmp-tbl tr.cmp-grp td{border-top:1px solid var(--line);padding-top:8px;
  font-size:11px;font-weight:800;letter-spacing:.06em;color:var(--acc)}
.cmp-tbl tr.cmp-grp td.cmp-a,.cmp-tbl tr.cmp-grp td.cmp-b{font-size:13px;color:var(--dim)}
.cmp-k{text-align:center;color:var(--dim);font-size:11.5px;font-weight:400}
.cmp-k i{display:block;font-style:normal;font-size:9.5px;opacity:.65}
.cmp-a{text-align:right;font-weight:700} .cmp-b{text-align:left;font-weight:700}
.cmp-a.win{color:var(--viz-us)} .cmp-b.win{color:var(--viz-them)}
.cmp-a.lose,.cmp-b.lose{color:var(--dim);opacity:.65}
/* 차이 배지 — 클수록 커진다. 색은 이긴 쪽을 가리킨다(좌 주황 · 우 파랑). */
.cmp-d{display:inline-block;margin-left:6px;padding:0 6px;border-radius:99px;
  font-size:12px;font-weight:800;line-height:1.6;vertical-align:1px}
.cmp-d.dA{color:var(--viz-us);background:rgba(217,89,38,.16)}
.cmp-d.dB{color:var(--viz-them);background:rgba(57,135,229,.16)}
.cmp-d.mid{font-size:13.5px}
/* 무엇이 갈랐는지(스탯/PlayStyle)를 배지 안에 한 줄로 붙인다 — 판정 근거가 라벨과 떨어지면 안 읽힌다. */
.cmp-d i{display:block;font-style:normal;font-size:9px;font-weight:600;opacity:.8;line-height:1.3;margin-top:-1px}
/* FC27에서 효과가 깎인 PlayStyle(½표) — 칩을 흐리게 해 한 표짜리와 눈으로 갈린다. */
.cmp-vfit .chip.cut{opacity:.6;border-style:dashed}
.cmp-votes{display:inline-block;margin-left:5px;font-size:11px;opacity:.75;vertical-align:1px}
.cmp-d.big{font-size:15.5px;padding:1px 8px}
.cmp-card.sA b{color:var(--viz-us)} .cmp-card.sB b{color:var(--viz-them)}
/* 에메리 기준 판정 */
.cmp-verdict{border:1px solid var(--line);border-radius:9px;padding:10px 12px;background:rgba(255,255,255,.02)}
.cmp-verdict.none{font-size:12px}
.cmp-vrow + .cmp-vrow{margin-top:10px;padding-top:10px;border-top:1px dotted var(--line)}
.cmp-vhead{display:flex;flex-wrap:wrap;gap:6px;align-items:center;font-size:12.5px}
.cmp-vfit{display:grid;grid-template-columns:1fr auto 1fr;gap:6px;align-items:center;margin:5px 0 4px;font-size:17px;font-weight:800}
.cmp-vfit .cmp-k i{display:block;font-style:normal;font-size:9.5px;opacity:.7;font-weight:400}
.cmp-vwhy{display:flex;flex-wrap:wrap;gap:5px}
.cmp-vwhy .chip{font-size:11px}
/* ⛔ 역할 이름은 **한 칩 안에서 줄바꿈되면 안 된다** — 「CM Deep-Lying Playmaker」가 두 줄로 쪼개져
   앞줄이 다른 칩처럼 읽혔다(2026-09-22 사용자 지적). 칩 단위로만 줄을 바꾼다.
   ⚠️ nowrap만 걸면 칩이 컨테이너를 삐져나가므로 **칩 묶음을 flex-wrap**으로 감싼다. */
.cmp-two .chip{white-space:nowrap;display:inline-block}
.cmp-two > div{display:flex;flex-wrap:wrap;gap:4px;align-content:flex-start}
.cmp-two .cmp-lab{flex-basis:100%;margin-top:4px}
.cmp-vwhy .wA{border-color:var(--viz-us);color:var(--viz-us)}
.cmp-vwhy .wB{border-color:var(--viz-them);color:var(--viz-them)}
.cmp-wtbl{width:100%;table-layout:fixed;margin-top:6px}
.cmp-wtbl th{font-size:10.5px;color:var(--dim);font-weight:600;padding:2px 4px}
.cmp-wtbl td{padding:2px 4px;font-size:12px}
.cmp-wtbl th:nth-child(2){width:auto}
.cmp-w{color:var(--acc);font-size:9px;letter-spacing:1px;font-style:normal;margin-left:4px}
b.wA{color:var(--viz-us)} b.wB{color:var(--viz-them)}
.cmp-two{display:grid;grid-template-columns:1fr 1fr;gap:10px;align-items:start}
.cmp-two .fc-pslist{gap:5px}
.cmp-lab{font-size:10.5px;margin:2px 0 3px}
.fc-ps.uniq{border-color:var(--ok)}
.cmp-pick{display:flex;flex-wrap:wrap;gap:6px;align-items:center;margin-bottom:10px}
/* 비교 모드 안내 — 「지금 카드를 누르면 상세가 아니라 담기가 된다」를 그 자리에서 알린다. */
.cmp-mode{font-size:11.5px;color:var(--dim);margin-left:2px}
.cmp-mode b{color:var(--acc)}
/* 담긴 카드 확인 칸 — 좌우 색은 비교표와 같은 규약(좌 주황 · 우 파랑)이라 어느 열이 누구인지 이어진다. */
.cmp-slots{display:grid;grid-template-columns:1fr auto 1fr;gap:8px;align-items:stretch;margin-bottom:10px}
.cmp-slot{position:relative;display:flex;gap:8px;align-items:center;padding:7px 8px;
  border:1px solid var(--line);border-radius:9px;min-height:64px}
.cmp-slot.empty{justify-content:center;border-style:dashed;opacity:.65}
.cmp-slot.empty i{display:block;font-style:normal;font-size:10px;opacity:.8;margin-top:2px}
.cmp-slot img{width:44px;height:58px;object-fit:contain;flex:none}
.cmp-slot-ph{width:44px;height:58px;flex:none;border-radius:5px;background:rgba(255,255,255,.06)}
.cmp-slot-t{display:flex;flex-direction:column;gap:1px;font-size:11.5px;min-width:0}
.cmp-slot-t b{font-size:13px}
.cmp-slot.sA{border-color:var(--viz-us)} .cmp-slot.sA .cmp-slot-t>b{color:var(--viz-us)}
.cmp-slot.sB{border-color:var(--viz-them)} .cmp-slot.sB .cmp-slot-t>b{color:var(--viz-them)}
.cmp-vs{align-self:center;font-size:11px;color:var(--dim);font-weight:700}
.cmp-x{position:absolute;top:2px;right:4px;background:none;border:0;color:var(--dim);
  font-size:15px;line-height:1;cursor:pointer;padding:2px 4px}
.cmp-x:hover{color:var(--viz-them)}
/* 케미 부스트 실제 적용값 — 표에서 즉시 눈에 들어와야 한다. */
.fc-boost{display:inline-block;min-width:34px;text-align:center;font-weight:800;font-size:12.5px;
  color:#062b12;background:var(--ok);border-radius:99px;padding:1px 8px}
.fc-boost.zero{color:var(--dim);background:transparent;border:1px solid var(--line);font-weight:600}
.fc-star{color:#f5c542;letter-spacing:1px}
.fc-star.off{color:rgba(255,255,255,.18)}
.fc-votehead{font-size:11.5px;color:var(--dim);margin:8px 0 4px}
`;
