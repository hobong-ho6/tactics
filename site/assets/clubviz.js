/* 내 구단 시각화 — FC 인게임 스쿼드 화면 재현 (2026-09-20, 사용자 지시 「fc27 게임처럼 시각화해줘」).
   ⛔ **계산하지 않는다.** EA 싱크 실측(카드 아트·OVR·케미 스타일·개인 케미)과 인게임 전술(migration 054)을
      그대로 배치할 뿐이다 — 이 화면에서 추천·순위를 만들지 않는다(그건 다른 탭의 일이다).
   ⭐ 카드 아트에는 **OVR·포지션·이름이 이미 인쇄돼 있다** — 덮어쓰지 않는다(2026-09-18 실증: 금속 질감 위에
      다시 쓰면 확대할 때 자국이 남는다). 진화로 값이 달라진 카드만 **카드 밖에 배지**로 현재 OVR을 알린다.
   ⭐ 배치는 fut.gg 슬롯 순서 규약을 따른다(f4231a: 0 GK · 1 RB · 2 CB · 3 CB · 4 LB · 5 CDM · 6 CDM ·
      7 RM · 8 LM · 9 CAM · 10 ST, **우→좌**). */
import { PLAYSTYLES } from './playstyle-icons.js';
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
.fc-pitch{position:relative;aspect-ratio:85/100;height:min(820px,calc(100vh - 210px));
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
.fc-card.sel .fc-artwrap{filter:drop-shadow(0 0 0 2px var(--ok))}
.fc-card.sel .fc-tag{border-color:var(--ok)}
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
.fc-evo{font-size:11px;font-weight:800;letter-spacing:.2px;background:var(--ok);color:#04220d;
  border-radius:99px;padding:1px 6px;white-space:nowrap;line-height:1.45}
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

function attrBlock(p) {
  const a = parse(p.attrs);
  if (!a) return '<p class="dim">상세 스탯 미수집(결손 — 0이 아니다).</p>';
  const stale = p.card_ovr != null && p.current_ovr != null && p.card_ovr !== p.current_ovr;
  const items = Object.entries(a).map(([k, v]) => `<div class="fc-attr"><span>${esc(k)}</span><b>${v}</b></div>`).join('');
  return `${stale ? `<p class="dim" style="margin:0 0 6px">⚠️ 이 29속성은 <b>기준 카드(OVR ${p.card_ovr})</b>의 값이라
      <b>진화 상승분이 빠져 있다</b> — 위 6대 스탯(현재 OVR ${p.current_ovr})과 어긋난다. EA는 진화 후 개별 속성을 공개하지 않는다.</p>` : ''}
    <div class="fc-attrs">${items}</div>`;
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
    ${bars ? `<div style="margin-top:6px">${bars}</div>`
           : '<p class="dim" style="font-size:11.5px;margin:6px 0 0">커뮤니티 투표 없음(결손 — 0표라는 뜻이지 비추천이 아니다).</p>'}
    <p class="dim" style="font-size:11.5px;margin:6px 0 0">⚠️ fut.gg 배지는 <b>등급이 아니라 그 스타일을 붙였을 때의 AcceleRATE</b>다(실측 확인).
      투표율은 <b>인기이지 정답이 아니다</b> — 위 역할 점수와 갈리면 역할 점수를 따른다.</p></div>`;
}

/* 스킬무브·약발·주발·AcceleRATE + Role+/++ (2026-09-21 사용자 지시 「스킬과 주발과 역할 정보를 추가해」).
   ⛔ Role+/++는 원장에 **raw ea_id**로 들어 있다(docs/21 ②) — `role_map`으로 이름을 붙이고,
      매핑에 없으면 지어내지 않고 id를 그대로 보여준다(결손을 감추지 않는다). */
const STARS = (n, max = 5) => n == null ? '—'
  : '★'.repeat(n) + `<span class="dim">${'★'.repeat(Math.max(0, max - n))}</span>`;

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
    <div class="fc-kv"><span>AcceleRATE</span><b>${esc(p.accelerate || '—')}</b></div>
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
    ${traitRow(p, ctx.role_map)}
    <h4>현재 카드 스탯</h4>${sixRow(cur, base)}
    ${psBlock(p.current_playstyles)}
    <h4>진화 상태 ${evoCountLabel(p, ctx.log)}</h4>${evoBlock(p, ctx.log)}
    <h4>적용된 케미스트리</h4>${chemBlock(p, ctx.chem_styles)}
    ${recoBlock(p, ctx.reco, ctx.chem_styles)}
    <h4>상세 스탯</h4>${attrBlock(p)}
  </div>`;
}

export const FC_DETAIL_CSS = `
/* ⚠️ 사이드 패널은 420px다 — 표를 그대로 두면 마지막 열이 패널 밖으로 밀려 잘린다
   (2026-09-20 사용자 지적 「케미스트리 색 변경 안 됨」의 실제 원인은 색이 아니라 **열 잘림**이었다).
   table-layout:fixed로 폭을 강제하고 숫자 열을 오른쪽에 고정한다. */
.fc-detail .tbl{width:100%;table-layout:fixed}
.fc-detail .tbl th,.fc-detail .tbl td{padding:3px 5px;font-size:12px;overflow:hidden;text-overflow:ellipsis}
.fc-chemtbl th:nth-child(n+2),.fc-chemtbl td:nth-child(n+2){width:58px;text-align:right}
.fc-detail h4{margin:14px 0 6px;font-size:13px}
.fc-pslist{display:flex;flex-wrap:wrap;gap:6px}
.fc-ps{display:inline-flex;align-items:center;gap:5px;font-size:12px;font-weight:600;
  background:var(--bg);border:1px solid var(--line);border-radius:99px;padding:3px 9px 3px 4px}
/* ⚠️ img에 background와 filter를 **함께 주지 않는다**(2026-09-21): filter는 배경까지 적용돼
   흰 배경이 검은 원이 된다. fut.gg PlayStyle 아이콘은 원본이 이미 흰 배경 + 검은 그림이라
   아무것도 덧칠할 필요가 없다 — 모서리만 둥글린다. */
.fc-ps img{width:19px;height:19px;display:block;border-radius:50%;background:#fff}
.fc-ps.plus{border-color:var(--ok)}
.fc-ps.plus i{font-style:normal;font-weight:800;color:var(--ok);margin-left:1px}
.fc-recotbl td{font-size:12px}
/* ⚠️ 네이티브 title 속성은 크롬에서 안 뜨다시피 한다(2026-09-21 사용자 지적) — 지연이 길고 hover 영역이 좁다.
   CSS 툴팁으로 바꾸고 tabindex를 줘 키보드 포커스로도 열리게 한다.
   ⛔ 이 블록은 템플릿 리터럴 안이다 — 주석에 백틱을 쓰면 리터럴이 거기서 끝나 파일이 깨진다(두 번 당했다). */
.fc-help{position:relative;border-bottom:1px dotted var(--dim);cursor:help;outline:none}
.fc-help i{font-style:normal;display:inline-block;margin-left:3px;width:13px;height:13px;line-height:13px;
  text-align:center;border-radius:50%;background:var(--line);color:var(--txt);font-size:9.5px;vertical-align:1px}
.fc-help::after{content:attr(data-tip);position:absolute;right:0;top:calc(100% + 6px);z-index:9;
  width:250px;padding:8px 10px;border-radius:8px;background:#0b1220;border:1px solid var(--line);
  color:var(--txt);font-size:11.5px;font-weight:400;line-height:1.5;text-align:left;white-space:normal;
  box-shadow:0 6px 18px rgba(0,0,0,.55);opacity:0;visibility:hidden;transition:opacity .12s}
.fc-help:hover::after,.fc-help:focus::after{opacity:1;visibility:visible}
.fc-vote{display:flex;align-items:center;gap:6px;font-size:11.5px;margin:3px 0}
.fc-vote span{flex:0 0 96px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.fc-vote i{flex:1;height:7px;border-radius:99px;background:var(--bg);overflow:hidden}
.fc-vote i b{display:block;height:100%;background:var(--acc);border-radius:99px}
.fc-vote em{flex:0 0 36px;text-align:right;font-style:normal;font-weight:700}
.fc-dhead{display:flex;gap:12px;align-items:flex-start}
.fc-dart{width:96px;flex:0 0 auto}
.fc-dhead h3{margin:0 0 2px;font-size:16px}
.fc-chemhead{display:flex;gap:8px;align-items:center;margin-bottom:6px}
.fc-chemhead img{width:26px;padding:4px;box-sizing:border-box;border-radius:50%;
  background:#fff;box-shadow:0 0 0 1px rgba(0,0,0,.5)}
.fc-attrs{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:2px 10px}
.fc-attr{display:flex;justify-content:space-between;font-size:12px;padding:2px 0;border-bottom:1px dotted var(--line)}
.fc-attr span{color:var(--dim)}
/* 케미 부스트 실제 적용값 — 표에서 즉시 눈에 들어와야 한다. */
.fc-boost{display:inline-block;min-width:34px;text-align:center;font-weight:800;font-size:12.5px;
  color:#062b12;background:var(--ok);border-radius:99px;padding:1px 8px}
.fc-boost.zero{color:var(--dim);background:transparent;border:1px solid var(--line);font-weight:600}
`;
