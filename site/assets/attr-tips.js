/* FC 세부 속성(29종 + GK 5종) 설명 — **정본 한 벌**(2026-11-05 사용자 지시 「각 스탯별 설명을 모든 스탯이 나오는 곳에 툴팁으로」).

   ⭐ 근거 등급을 밝혀 쓴다(불변규칙 12): A = EA 1차 · B = 데이터마이닝 · C = 통제 실측 · D = 통설.
      버전도 밝힌다 — FIFA 23·FC25·FC26 문서를 FC27에 쓰는 것은 「이월 추정」이다.
      「이름 그대로」 = EA가 작용 방식을 밝히지 않아 속성 이름 이상으로 말할 근거가 없다는 뜻.
      근거 행 정본: game_system_changes(게임 시스템 → 시스템 분석) #12·#22·#23·#24·#26·#46·#52~#56·#88·#92~#96.

   ⭐ 화면마다 손으로 감싸지 않는다(규율 → 구조 · 불변규칙 13): 이 모듈을 불러오면(data.js가 모든 페이지에서 부른다)
      화면에 **속성 이름과 정확히 같은 글자**가 나타날 때마다 툴팁을 자동으로 붙인다(MutationObserver).
      이미 툴팁(.gl) 안에 있거나 입력·선택 상자 안이면 건드리지 않는다. 끄려면 조상에 data-no-attr-tip.
   ⚠️ 표기가 다른 이름(예: 「볼 컨트롤」)은 붙지 않는다 — 우리 화면의 정본 라벨(fut.gg 대응 한국어)만 키로 쓴다. */

export const ATTR_TIPS = {
  /* ── 속도 ── */
  '가속': '정지 상태에서 최고 속도까지 붙는 빠르기. FC27은 AcceleRATE 유형의 영향을 줄이고 가속·질주 속성 비중을 키웠다(A · FC27). AcceleRATE Explosive 판정 조건에도 들어간다(A · FC26).',
  '질주 속도': '최고 속도. FC27에서 비중이 커졌다(A · FC27). 수비 자세(조키) 이동 속도에는 영향이 없다(A · FIFA 23).',
  /* ── 슈팅 ── */
  '공격 위치 선정': '공 없을 때 득점 자리를 잡는 능력. 85 이상이면 밀착 마크를 당했을 때 침투 방향을 바꿔 공간을 만든다(A · FIFA 23 문턱 · FC26·27은 속성 언급 없음 → 이월 추정). 그 밖의 작용은 이름 그대로.',
  '결정력': '박스 안 발 슛의 정확도 — 이름 그대로(EA 작용 방식 미공개). 헤더·중거리는 별도 속성이다.',
  '슈팅력': '슛의 속도(힘). FC27은 슛 속도가 핵심 슈팅 속성과 입력 파워로만 정해진다 — 로우 드리븐 슛의 속도 보너스는 제거됐다(A · FC27).',
  '중거리슛': '박스 밖에서 때리는 슛의 정확도 — 이름 그대로(EA 작용 방식 미공개).',
  '발리 슛': '뜬 공을 바로 때리는 슛의 정확도 — 이름 그대로.',
  '페널티킥': '페널티킥 성공 능력 — 이름 그대로(PK 타이밍 원은 침착이 정한다 · A · FC25).',
  /* ── 패스 ── */
  '시야': '⚠️ FC25~FC27 EA 문서에 작용 서술이 없다(A 부재). 「스루패스 품질 요소」라는 1차 근거는 FIFA 21 전재본뿐이다.',
  '크로스': '측면에서 올리는 크로스의 정확도 — 이름 그대로.',
  '프리킥 정확도': '직접 프리킥의 정확도 — 이름 그대로.',
  '짧은 패스': '가까운 거리 패스의 정확도. 패스 능력치가 높을수록 땅볼 패스 정확도·속도 개선 효과가 크고, 긴 패스·커브와 함께 높으면 스루패스에 상황에 따라 커브가 들어간다(A · FC26 TU 1.5.0).',
  '긴 패스': '먼 거리 패스의 정확도. 짧은 패스·커브와 함께 높으면 스루패스에 커브가 들어간다(A · FC26).',
  '커브': '공에 회전을 거는 능력(감아차기·크로스 궤적). 짧은·긴 패스와 함께 높으면 스루패스에 커브가 들어간다(A · FC26).',
  /* ── 드리블 ── */
  '민첩성': '드리블 동작이 재생되는 속도·다음 동작으로 넘어가는 속도(A · FIFA 23 → FC27 이월 추정) · 오프밸런스 드리블(부딪혀도 이어 가기) 입력(A · FC27) · AcceleRATE 유형 판정(A). 「방향 전환·몸 돌리기가 빨라진다」는 EA 문서가 없다(D).',
  '균형 감각': '드리블 동작 전환 속도(A · FIFA 23) · 오프밸런스 드리블 입력(A · FC27). 「80 이상부터는 체감이 적다」는 통설(D).',
  '반응력': '드리블 동작 재생·전환 속도와 드리블 중 속도 유지(A · FIFA 23 — FC25~27 문서엔 서술 없음 → 이월 추정). 「세컨볼·리바운드 경합」·「AI 전용」은 기각된 통설. ⚠️ GK의 「반사신경」과 다른 속성이다(카드 REF에 안 들어간다 · GK OVR 약 11%).',
  '볼컨트롤': '드리블 터치 정확도·공이 몸에 붙는 거리(A · FIFA 23) + 퍼스트 터치 난이도(볼컨트롤·차단력·침착 복합 · A · FC26). FC27은 패서가 받는 선수의 트랩 오차를 줄여 주던 보정을 없애 본인 비중이 커졌다(A). 오프밸런스 드리블 입력에는 없다(A · FC27).',
  '드리블': '드리블 터치 정확도·공 밀착·동작 재생/전환 속도·드리블 중 속도 유지(A · FIFA 23) + 오프밸런스 드리블 입력(A · FC27). 공을 몰고 가는 거의 모든 판정에 들어가는 핵심 속성.',
  '침착': '퍼스트 터치 난이도 입력(A · FC26)과 페널티킥 타이밍 원 수축 속도(A · FC25) — EA가 밝힌 것은 이 둘뿐이다. 「압박을 느끼기 시작하는 거리」·골 결정력 효과는 기각된 통설.',
  /* ── 수비 ── */
  '차단력': '상대 패스를 끊어내는 능력 + 퍼스트 터치 입력(A · FC26). FC27은 수비 스탯이 낮은 선수의 인터셉트가 과하게 잘 되는 문제를 EA가 인정하고 수정 중(A).',
  '헤딩 정확도': '머리로 하는 슛·패스·걷어내기의 정확도 — 이름 그대로.',
  '수비 위치 선정': '막아야 할 자리를 미리 잡는 능력 — 이름 그대로(「좋으면 태클 자체가 줄어든다」는 통설 D). 수비 자세(조키) 속도는 수비 인지가 정한다(A · FIFA 23).',
  '스탠딩 태클': '서서 하는 태클의 성공률 — 이름 그대로. FC27은 포지션에 안 맞는 선수의 태클·인터셉트 과효를 수정 중(A).',
  '슬라이딩 태클': '미끄러지며 하는 태클의 성공률 — 이름 그대로.',
  /* ── 피지컬 ── */
  '점프': '점프 높이 — 이름 그대로. 공중볼 박스아웃은 점프가 아니라 두 선수의 힘 차이로 정해진다(A · FC26).',
  '체력': '경기 후반까지 능력치를 유지하는 지구력 — 이름 그대로.',
  '힘': '볼 지키기(쉴딩)·어깨싸움·공중볼 박스아웃(A · FC26 — 힘 차이가 클수록 약한 쪽이 더 자주 비틀거린다) + AcceleRATE Lengthy 판정(A). FC27 어깨싸움은 나란히 붙었을 때 가장 효과적(A).',
  '공격성': '볼 지키기·몸싸움에 힘과 함께 들어간다(A · FC26). 카드 PHY의 20%. 「압박 강도·반칙이 늘어난다」는 근거 없음(D).',
  /* ── GK ── */
  '다이빙': 'GK — 몸을 날려 먼 쪽 슛을 막는 선방 범위(이름 그대로 · D). 카드 DIV와 같은 값 · GK OVR 약 21%(C).',
  '핸들링': 'GK — 쳐내지 않고 잡아내는 능력(이름 그대로 · D). 카드 HAN과 같은 값 · GK OVR 약 21%(C).',
  '킥': 'GK — 골킥·펀트·롱킥 배급의 거리·정확도(이름 그대로). 카드 KIC와 같은 값 · GK OVR 약 5%(C).',
  '반사신경': 'GK — 가까운 거리·굴절 슛 반응. 반응력과 함께 「시야가 가린 슈팅」이 선방에 주는 영향을 정한다(A · FIFA 23). 카드 REF와 같은 값 · GK OVR 약 21%(C). ⚠️ 일반 속성 「반응력」과 다르다.',
  '포지셔닝': 'GK — 슛 각도를 좁히는 자리 잡기(이름 그대로). 카드 POS와 같은 값 · GK OVR 약 21%(C). ⚠️ 필드 선수의 공격·수비 위치 선정과 다른 속성이다.',
};

/* ── 자동 툴팁 ─────────────────────────────────────────── */
const SKIP = 'abbr.gl, .gl, select, option, textarea, input, script, style, [data-no-attr-tip]';
const esc = s => String(s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
function wrap(node){
  const t = node.nodeValue, key = t.trim();
  const tip = ATTR_TIPS[key];
  if (!tip) return;
  const p = node.parentElement;
  if (!p || p.closest(SKIP)) return;
  const ab = document.createElement('abbr');
  ab.className = 'gl'; ab.tabIndex = 0; ab.dataset.tip = tip; ab.title = tip;
  ab.textContent = key;
  const lead = t.slice(0, t.indexOf(key)), tail = t.slice(t.indexOf(key) + key.length);
  const frag = document.createDocumentFragment();
  if (lead) frag.append(lead);
  frag.append(ab);
  if (tail) frag.append(tail);
  node.replaceWith(frag);
}
function scan(root){
  if (!root || root.nodeType !== 1 && root.nodeType !== 9) return;
  const w = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {
    acceptNode: n => ATTR_TIPS[n.nodeValue.trim()] ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_REJECT });
  const hits = []; while (w.nextNode()) hits.push(w.currentNode);
  hits.forEach(wrap);
}
let pending = false;
function mount(){
  scan(document.body);
  new MutationObserver(() => {
    if (pending) return; pending = true;
    setTimeout(() => { pending = false; scan(document.body); }, 60);
  }).observe(document.body, { childList: true, subtree: true });
}
if (typeof document !== 'undefined' && !window.__attrTips){
  window.__attrTips = 1;
  if (document.body) mount(); else document.addEventListener('DOMContentLoaded', mount, { once: true });
  import('./glossary.js?v=20260913-selection-glossary').then(m => m.mountGlossaryTips && m.mountGlossaryTips()).catch(() => {});
}
