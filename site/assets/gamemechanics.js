/* FC26 게임플레이 메커니즘 정적 참고 데이터 — 글로서리·세리머니와 동일 패턴(DB 비대상).
   손편집 지점: 이 파일뿐. 원본 서술은 docs/22-fc-gameplay-mechanics.md — 내용이 갈리면
   docs/22가 서사 정본이고 이 파일은 그 표를 사이트용으로 옮긴 것이다(수치·문구는 일치시킬 것).
   출처: FUT.GG·FUTBIN·Operation Sports·FIFAUTeam·EA FC Zone·RealSport101 (2026-09-02 수집).
*/

export const CONTROLS = {
  speed: [
    { label: '걷기', trigger: '왼쪽 스틱을 살짝만 기울임' },
    { label: '조깅', trigger: '왼쪽 스틱을 끝까지 기울이되 스프린트 버튼은 누르지 않음' },
    { label: '스프린트', trigger: '왼쪽 스틱을 끝까지 기울이고 R2/RT(스프린트)를 동시에 누름' },
  ],
  modifiers: [
    { btn: 'RB (R1)', attack: '피네스 모디파이어 · 스프린트/근접 컨트롤', defend: '동료 압박 지시(Teammate Contain)' },
    { btn: 'LB (L1)', attack: '오버래핑 런 / 트리거 런', defend: '선수 전환(Switch Player)' },
    { btn: 'LT (L2)', attack: '정밀 드리블 · 쉴딩', defend: '조키(Jockey, 크랩스텝 견제)' },
    { btn: 'RT (R2)', attack: '피네스 무브 · 고속 스프린트', defend: 'LT+RT 동시 = 고속 조키' },
  ],
  tips: [
    '피네스 슛: B+RB(○+R1). 로우드리븐 피네스: RB/R1 홀드 후 슛 더블탭.',
    '쉴딩: LT/L2 홀드로 볼과 수비수 사이에 몸을 넣는다 — 가만히 버티기보다 급턴·볼 굴리기와 결합할 때 효과적.',
    'LT+RB(L2+R1) 슬로우 드리블+급턴: 쉴딩 유지한 채 방향 전환 — Press Proven 보유 선수에게 특히 유효.',
    '게임플레이 프리셋: Competitive(빠른 패스·정밀 드리블, 온라인 UT/클럽 기본) vs Authentic(느리고 사실적, 오프라인 커리어 기본).',
  ],
};

export const STATS = [
  { key: 'PAC', name: '스피드', desc: '전력질주 속도 + 최고속도 도달 시간. 다른 스탯(드리블·포지셔닝)의 승수처럼 작동한다.', sub: '가속력(정지→최고속 도달 시간) · 질주속도(최고속)' },
  { key: 'SHO', name: '슈팅', desc: '득점 확률 전반을 결정한다.', sub: '결정력은 박스 안 발슛 정확도만 결정 — 헤더·중거리슛은 별도 속성' },
  { key: 'PAS', name: '패싱', desc: '빌드업·전환의 정확도를 결정한다.', sub: '시야(패스 선택지 인식) · 크로스 · 단패스 · 장패스 — 서로 독립적으로 작동' },
  { key: 'DRI', name: '드리블', desc: '볼을 몸에 붙이는 능력(뺏기 어려움). 스킬무브 별점과는 별개 축.', sub: '침착(Composure) — 골 결정 순간의 냉정함을 좌우' },
  { key: 'DEF', name: '수비', desc: '볼을 따내는 능력.', sub: '수비 위치선정이 실질 1티어 지표(좋으면 태클 자체가 줄어듦) · 적극성은 반칙·PK 리스크와 트레이드오프' },
  { key: 'PHY', name: '피지컬', desc: '몸싸움·지구력·공중볼 경합을 결정한다.', sub: '힘 · 체력 · 점프력 등이 개별 작동' },
];
export const STATS_NOTE = 'OVR은 포지션별 가중 평균이다 — CB는 수비+피지컬 비중이 크고 윙어는 스피드+드리블 비중이 커서, ' +
  '스피드만 극단으로 높고 패스가 약한 윙어는 OVR이 낮게, 수비+피지컬만 강한 CB는 스피드가 평범해도 OVR이 높게 나올 수 있다.';

export const PLAYSTYLE_CATEGORIES = [
  { key: 'scoring', label: '파이널서드(득점)' },
  { key: 'passing', label: '패스' },
  { key: 'ballcontrol', label: '볼 컨트롤' },
  { key: 'defending', label: '수비' },
  { key: 'physical', label: '피지컬' },
  { key: 'gk', label: '골키퍼' },
];

export const PLAYSTYLES = [
  // 파이널서드(득점)
  { cat: 'scoring', name_kr: '피네스 슛', name_en: 'Finesse Shot', trigger: '피네스 슛 입력(RB/R1 + 슛)', effect: '슛 속도·정확도·커브 향상' },
  { cat: 'scoring', name_kr: '로우드리븐 슛', name_en: 'Low Driven Shot', trigger: '로우드리븐 슛(RB/R1 홀드+슛 더블탭)', effect: '저구간 강슛의 속도·정확도 향상' },
  { cat: 'scoring', name_kr: '파워 슛', name_en: 'Power Shot', trigger: '슛 버튼 길게 충전', effect: '빌드업 속도·정확도 대폭 향상' },
  { cat: 'scoring', name_kr: '칩 슛', name_en: 'Chip Shot', trigger: '칩 슛(LB/L1+슛)', effect: '칩 슛 속도·정밀도 향상' },
  { cat: 'scoring', name_kr: '아크로바틱', name_en: 'Acrobatic', trigger: '발리 상황', effect: '발리 정확도 향상 + 전용 아크로바틱 애니메이션' },
  { cat: 'scoring', name_kr: '헤더 정밀', name_en: 'Precision Header', trigger: '헤더 상황(점프력 자체는 불변)', effect: '헤더 정확도 향상 + 전용 애니메이션' },
  { cat: 'scoring', name_kr: '게임체인저', name_en: 'Gamechanger', trigger: '트리벨라(바깥발) 슛 · 화려한 슛', effect: '트리벨라 슛 활성화 + 정확도 향상' },
  { cat: 'scoring', name_kr: '데드볼', name_en: 'Dead Ball', trigger: '세트피스(프리킥·코너)', effect: '세트피스 속도·정확도·파워 향상, 궤적 프리뷰 강화' },
  // 패스
  { cat: 'passing', name_kr: '핑드 패스', name_en: 'Pinged Pass', trigger: '모든 패스 유형', effect: '패스 속도 상승 + 동료가 받기 쉬워짐(트래핑 보정)' },
  { cat: 'passing', name_kr: '인사이시브 패스', name_en: 'Incisive Pass', trigger: '스루패스·정밀패스·감아차기패스', effect: '스루패스 정확도·정밀패스 속도·감아차기 커브 향상' },
  { cat: 'passing', name_kr: '롱볼 패스', name_en: 'Long Ball Pass', trigger: '롱볼·로빙패스', effect: '정확도·속도 향상 + 인터셉트 당할 확률 감소' },
  { cat: 'passing', name_kr: '휩드 패스', name_en: 'Whipped Pass', trigger: '크로스', effect: '정확도·속도·커브 향상' },
  { cat: 'passing', name_kr: '티키타카', name_en: 'Tiki Taka', trigger: '원터치·단패스 상황', effect: '첫터치·단패스 정확도 향상 + 조건 충족 시 자동 백힐' },
  { cat: 'passing', name_kr: '인벤티브', name_en: 'Inventive', trigger: '화려한 패스(스루패스 변형 등)', effect: '정확도 향상 + 전용 애니메이션' },
  // 볼 컨트롤
  { cat: 'ballcontrol', name_kr: '프레스 프루븐', name_en: 'Press Proven', trigger: '조깅 속도로 드리블 중(스프린트 버튼 안 누름)', effect: '근접 컨트롤 대폭 향상 + 피지컬 압박에 대한 쉴딩 효율 상승' },
  { cat: 'ballcontrol', name_kr: '퍼스트 터치', name_en: 'First Touch', trigger: '패스를 받는 순간', effect: '트래핑·첫 드리블 개시 속도 향상(터치가 가벼워짐)' },
  { cat: 'ballcontrol', name_kr: '래피드', name_en: 'Rapid', trigger: '스프린트 중 드리블', effect: '온볼 스프린트 속도 향상 + 스프린트/노크온 실수 확률 감소 (Press Proven의 정반대 축 — 조깅 vs 스프린트)' },
  { cat: 'ballcontrol', name_kr: '테크니컬', name_en: 'Technical', trigger: '넓은 회전 드리블', effect: '컨트롤드 스프린트 속도·와이드턴 정밀도 향상' },
  { cat: 'ballcontrol', name_kr: '트릭스터', name_en: 'Trickster', trigger: '스킬무브 입력', effect: '전용 스킬무브(Trickster Fake Shot 등) 해금' },
  // 수비
  { cat: 'defending', name_kr: '조키', name_en: 'Jockey', trigger: '조키(LT+RT/L2+R2)', effect: '스프린트 조키·전환 속도 향상' },
  { cat: 'defending', name_kr: '블록', name_en: 'Block', trigger: '슛/패스 블록 시도', effect: '블록 범위·성공률 향상' },
  { cat: 'defending', name_kr: '인터셉트', name_en: 'Intercept', trigger: '인터셉트 성공 시', effect: '인터셉트 리치 향상 + 성공 후 볼 소유 유지력 상승' },
  { cat: 'defending', name_kr: '앤티시페이트', name_en: 'Anticipate', trigger: '스탠딩 태클 시도', effect: '태클 성공률 향상 + 태클 후 발밑에 볼을 세우는 능력' },
  { cat: 'defending', name_kr: '슬라이드 태클', name_en: 'Slide Tackle', trigger: '슬라이딩 태클 시도', effect: '슬라이딩 태클 효율 향상 + 태클 후 볼 컨트롤 유지' },
  { cat: 'defending', name_kr: '에어리얼 포트리스', name_en: 'Aerial Fortress', trigger: '공중볼 경합', effect: '점프력·공중 지배력(경합 승률) 향상' },
  // 피지컬
  { cat: 'physical', name_kr: '브루저', name_en: 'Bruiser', trigger: '몸싸움 태클', effect: '상대를 몸으로 밀어내며 볼을 빼앗는 능력 향상' },
  { cat: 'physical', name_kr: '인포서', name_en: 'Enforcer', trigger: '어깨싸움(숄더 챌린지)·쉴딩', effect: '숄더 챌린지 활성화 + 쉴딩 능력 대폭 향상' },
  { cat: 'physical', name_kr: '퀵 스텝', name_en: 'Quick Step', trigger: '익스플로시브 스프린트 진입 순간', effect: '초반 가속력 향상' },
  { cat: 'physical', name_kr: '릴렌트리스', name_en: 'Relentless', trigger: '지속 압박·contain 전술', effect: '스태미나 회복 향상 + 압박 지속 시간 연장' },
  { cat: 'physical', name_kr: '롱스로우', name_en: 'Long Throw', trigger: '스로인', effect: '스로인 파워·최대 거리 향상' },
  // 골키퍼
  { cat: 'gk', name_kr: '파 리치', name_en: 'Far Reach', trigger: '원거리 선방(다이빙)', effect: '다이빙/점프 애니메이션 다양화 + 박스 밖 슛 대응력 향상' },
  { cat: 'gk', name_kr: '풋워크', name_en: 'Footwork', trigger: '발밑 선방', effect: '풋세이브 성능 향상 + 전용 애니메이션' },
  { cat: 'gk', name_kr: '크로스 클레이머', name_en: 'Cross Claimer', trigger: '크로스 캐칭', effect: '크로스 차단 속도 향상 + 전용 캐칭 애니메이션' },
  { cat: 'gk', name_kr: '러시 아웃', name_en: 'Rush Out', trigger: '박스 밖 스위핑(전진 저지)', effect: '박스 밖으로 뛰쳐나가는 속도 향상 + 반사/예측 전용 애니메이션' },
  { cat: 'gk', name_kr: '디플렉터', name_en: 'Deflector', trigger: '슛 저지(막지 못하는 상황)', effect: '쳐낸 볼이 위험 지역이 아니라 안전한 곳(동료 쪽)으로 향하도록 보정 + 전용 애니메이션' },
  { cat: 'gk', name_kr: '파 스로우', name_en: 'Far Throw', trigger: '골킥/배급', effect: '스로 파워·거리 향상' },
];
export const PLAYSTYLE_NOTE = '⚠️ FC26에서 Trivela·Flair·Power Header·Aerial 4종이 폐지되고 Enforcer 등 5종으로 재구성됐다 — 전작(FC25) 자료를 그대로 인용하지 말 것. ' +
  '⭐ 공통 원칙: PlayStyle은 대부분 패시브다 — 그 상황에서 자동으로 보정치가 얹힌다. +(플러스) 버전은 효과가 과장된 수준으로 강화된다(실존 선수의 특출난 능력치 반영, EA 비공개 수치). ' +
  '박스투박스 CM은 Pinged Pass+Press Proven, 풀백은 Bruiser+/Intercept+/Quick Step+/Pinged Pass+, 스트라이커는 Finesse Shot+/Low Driven+가 상위 빌드의 공통축.';

export function esc(v){ return String(v??'').replace(/[&<>"']/g, ch => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch])); }

/* 검색+카테고리 접기 공용 마운트 — celebrations/playstyles 공용 */
export function mountSearchableCatalog(root, { items, categories, matchText, renderRow, headerRow }){
  function render(q){
    const query = (q||'').trim().toLowerCase();
    const groups = categories.map(cat => {
      const rows = items.filter(it => it.cat === cat.key && (!query || matchText(it).toLowerCase().includes(query)));
      return { cat, rows };
    }).filter(g => g.rows.length);
    const anyQuery = query.length > 0;
    root.innerHTML = groups.map(g => `
      <details class="cele-group"${anyQuery ? ' open' : ''}>
        <summary><b>${esc(g.cat.label)}</b> <span class="badge">${g.rows.length}</span></summary>
        <table>${headerRow}${g.rows.map(renderRow).join('')}</table>
      </details>`).join('') || '<p class="dim">일치하는 항목이 없습니다.</p>';
  }
  render('');
  return render;
}
