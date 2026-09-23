/* 카드 비교 **동작**의 정본 (2026-09-23 사용자 지시
   「내 구단에서 비교에 담기 동작이 지금 내 팀과 다르다 — 동일하게 적용하고,
    페이지마다 동작이 다른데 다 동일하게 쓸 수 있도록 개선」).

   ⛔⛔ 종전에는 「지금 내 팀」 탭 안의 지역 변수·지역 함수였고, 「내 구단」은 그걸 **눈으로 보고 다시 짰다.**
   그래서 같은 버튼이 탭마다 다르게 굴렀다 — 한쪽은 **비교 모드**(한 장 담으면 다음 클릭이 계속 담기),
   다른 쪽은 **토글**(다음 카드를 누르면 상세로 빠져나감)이었다.
   docs/70이 말하는 그 부류다: 규칙을 지역에 두고 주석으로 「공용」이라 적으면 파일 밖에는 닿지 않는다.
   ⇒ 여기 한 곳만 안다. 새 화면은 이 모듈을 **import**한다(⛔ 다시 짜지 않는다).

   동작 규약(2026-09-22 사용자 지시에서 확정, 여기서는 그대로 옮기기만 했다):
     · 한 장을 담는 순간 **비교 모드**가 켜지고, **비우기**(또는 마지막 한 장까지 빼기) 전에는 꺼지지 않는다.
     · 켜져 있는 동안 카드를 누르면 **상세가 아니라 담기/빼기**가 된다.
     · 두 장이 차면 그 다음 카드는 **오래된 쪽을 밀어낸다**.
     · 담긴 카드는 목록에서도 `.picked`로 표시한다.
     · 두 장일 때는 비교표가 머리 정보를 대신하므로 「담긴 칸」을 숨기고, 칸마다 ×로 **한 장만** 뺄 수 있다.

   사용:
     const CMP = cardCompare({
       side, root,                       // 사이드패널 엘리먼트 · 카드가 놓인 컨테이너
       byId: id => …,                    // 보유 카드 행 id → 카드 객체
       ctx: () => ({ … }),               // compareCards에 넘길 컨텍스트
       render: { compareCards, cmpSlots },
       onExit: () => { … },              // 비교를 끝냈을 때 사이드패널을 무엇으로 되돌릴지
     });
     CMP.active()        // 비교 모드인가 — 카드 클릭 핸들러가 이걸 보고 분기한다
     CMP.toggle(card)    // 담기/빼기
     CMP.start(card)     // 「비교에 담기」 버튼에서 호출(모드를 켜고 담는다)

   ⚠️ 담는 것은 **보유 카드 행 id**(`p.id`)다. 목록의 `data-p`는 **player_id**라 서로 다르다 —
      그냥 비교하면 엉뚱한 카드에 ✓가 붙는다(2026-09-22 실측: 음바예·캐시를 담았는데 오나나에 붙었다). */

export function cardCompare({ side, root, byId, ctx, render, onExit, pickedAttr = 'data-p' }) {
  let cmp = [];
  let mode = false;

  const clearMarks = () => root.querySelectorAll('.sel, .picked')
    .forEach(x => x.classList.remove('sel', 'picked'));

  const markPicked = () => {
    clearMarks();
    const pids = cmp.map(id => byId(id)?.player_id).filter(v => v != null).map(Number);
    for (const el of root.querySelectorAll(`[${pickedAttr}]`)) {
      if (!pids.includes(Number(el.getAttribute(pickedAttr)))) continue;
      el.classList.add('picked');
      el.closest('.fc-slot')?.classList.add('picked');     // 피치는 확대가 슬롯에서만 먹는다
      el.querySelector?.('.fc-card')?.classList.add('picked');
    }
  };

  const exit = () => { mode = false; cmp = []; clearMarks(); onExit(); };

  const draw = () => {
    const picked = cmp.map(byId).filter(Boolean);
    side.innerHTML = `<div class="cmp-pick"><b>카드 비교</b>
        <span class="cmp-mode">${picked.length < 2
          ? '목록에서 <b>비교할 카드를 누르세요</b>'
          : '카드를 더 누르면 <b>왼쪽 카드가 밀려납니다</b>'}</span>
        <button class="act" data-cmpclear>비우기</button></div>`
      + (picked.length === 2 ? render.compareCards(picked[0], picked[1], ctx()) : render.cmpSlots(picked));
    side.querySelector('[data-cmpclear]').addEventListener('click', exit);
    /* 비교표 머리에도 ×를 단다 — 한 장만 바꿔 끼울 때 「비우기 → 둘 다 다시 담기」를 안 하게. */
    side.querySelectorAll('.cmp-card').forEach((el, i) => {
      if (!picked[i]) return;
      el.insertAdjacentHTML('beforeend',
        `<button class="cmp-x" data-cmpdrop="${picked[i].id}" title="이 카드를 비교에서 뺀다">×</button>`);
    });
    side.querySelectorAll('[data-cmpdrop]').forEach(b => b.addEventListener('click', () => {
      cmp = cmp.filter(x => x !== Number(b.dataset.cmpdrop));
      if (cmp.length) draw(); else exit();
    }));
    markPicked();
    side.scrollTop = 0;
  };

  const toggle = p => {
    if (!p) return;
    cmp = cmp.includes(p.id) ? cmp.filter(x => x !== p.id) : [...cmp, p.id].slice(-2);
    if (cmp.length) draw(); else exit();
  };

  return {
    active: () => mode,
    has: id => cmp.includes(id),
    toggle,
    start: p => { mode = true; toggle(p); },   // 「비교에 담기」 버튼 — 여기서부터 카드 클릭 = 담기
    exit,
  };
}
