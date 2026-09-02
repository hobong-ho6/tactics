/* FC26 세리머니 참고 데이터 — 정적 하드코딩(글로서리와 동일 패턴, DB 비대상).
   손편집 지점: 이 파일뿐. site/data/*.json과 무관 — export.py 대상 아님.
   출처: FIFPlay(fifplay.com/fc-26-celebrations) 2026-09-02 수집. PS 기준, Xbox는 버튼명만 다름(L1↔LB·R1↔RB·L2↔LT·R2↔RT·◯↔B·□↔X·△↔Y·R3 동일).
   방향 표기: ⇧위 ⇩아래 ⇦왼쪽 ⇨오른쪽(오른쪽 스틱 기준). "Flick A→B"는 A방향으로 튕긴 뒤 B방향으로 유지(hold).
*/
export const CATEGORIES = [
  { key: 'basic',  label: '기본 조작' },
  { key: 'running', label: '러닝 무브 — 뛰는 중 발동' },
  { key: 'finish',  label: '피니싱 무브 — 멈춘 뒤 발동' },
  { key: 'new26',   label: 'FC26 신규' },
  { key: 'pro',     label: '프로 언락 (클럽 모드)' },
  { key: 'eas',     label: 'EAS FC 언락' },
];

export const CELEBRATIONS = [
  // 기본 조작
  { cat: 'basic', name_kr: '시그니처 세리머니', name_en: 'Signature Celebration', ps: '△(X)', xbox: 'A', note: '선수 고유 세리머니 자동 발동' },
  { cat: 'basic', name_kr: '랜덤 세리머니', name_en: 'Random Celebration', ps: '◯', xbox: 'B', note: '보유 세리머니 중 무작위 발동' },
  { cat: 'basic', name_kr: '세리머니 취소', name_en: 'Cancel Celebration', ps: 'L1 + R1', xbox: 'LB + RB', note: '즉시 스킵' },

  // 러닝 무브 (뛰는 중 R스틱)
  { cat: 'running', name_kr: '엄지 빨기', name_en: 'Thumb Suck', ps: '□ 홀드', xbox: 'X 홀드' },
  { cat: 'running', name_kr: '팔 벌리기', name_en: 'Arms Out', ps: '□ 탭 → 홀드', xbox: 'X 탭 → 홀드' },
  { cat: 'running', name_kr: '손목 플릭', name_en: 'Wrist Flick', ps: '△ 탭 → 홀드', xbox: 'Y 탭 → 홀드' },
  { cat: 'running', name_kr: '비행기', name_en: 'Aeroplane', ps: 'R3 홀드', xbox: 'R3 홀드' },
  { cat: 'running', name_kr: '하늘 가리키기', name_en: 'Point to Sky', ps: 'R스틱 ⇧ 홀드', xbox: 'R스틱 ⇧ 홀드' },
  { cat: 'running', name_kr: '전화기', name_en: 'Telephone', ps: 'R스틱 ⇩ 홀드', xbox: 'R스틱 ⇩ 홀드' },
  { cat: 'running', name_kr: '안 들려?', name_en: 'Can You Hear Me?', ps: 'R스틱 ⇦ 홀드', xbox: 'R스틱 ⇦ 홀드' },
  { cat: 'running', name_kr: '손 벌리기', name_en: 'Hands Out', ps: 'R스틱 ⇨ 플릭 → ⇦ 홀드', xbox: '동일' },
  { cat: 'running', name_kr: '컴온!', name_en: 'Come On!', ps: 'R스틱 ⇦ 플릭 → ⇨ 홀드', xbox: '동일' },
  { cat: 'running', name_kr: '키스 날리기', name_en: 'Blow Kisses', ps: 'R스틱 ⇩ 플릭 → ⇧ 홀드', xbox: '동일' },
  { cat: 'running', name_kr: '양팔 스윙', name_en: 'Double Arm Swing', ps: 'R스틱 ⇧ 플릭 → ⇩ 홀드', xbox: '동일' },
  { cat: 'running', name_kr: '나는 새', name_en: 'Flying Bird', ps: 'R스틱 ⇨ 플릭 → ⇨ 홀드', xbox: '동일' },
  { cat: 'running', name_kr: '머리 감싸기', name_en: 'Hand on Head', ps: 'R스틱 ⇦ 플릭 → ⇦ 홀드', xbox: '동일' },
  { cat: 'running', name_kr: '하트', name_en: 'Heart Symbol', ps: 'R스틱 ⇩ 플릭 → ⇩ 홀드', xbox: '동일' },
  { cat: 'running', name_kr: '양팔 위로', name_en: 'Arms Pointing Up', ps: 'R스틱 ⇧ 플릭 → ⇧ 홀드', xbox: '동일' },
  { cat: 'running', name_kr: '풍차', name_en: 'Windmill', ps: 'R스틱 시계방향 회전', xbox: '동일' },
  { cat: 'running', name_kr: '한 팔 들기', name_en: 'One Arm Raised', ps: '◯ 홀드', xbox: 'B 홀드' },
  { cat: 'running', name_kr: '손가락 가리키기', name_en: 'Finger Points', ps: '◯ 탭 → 홀드', xbox: 'B 탭 → 홀드' },

  // FC26 신규
  { cat: 'new26', name_kr: '누구, 나?', name_en: 'Who, me?', ps: 'L1 홀드 + R스틱 ⇨ 홀드', xbox: 'LB + R스틱 ⇨' },
  { cat: 'new26', name_kr: '밴드 마스터', name_en: 'Band Master', ps: 'L1 홀드 + R스틱 ⇨⇧ 플릭', xbox: 'LB + R스틱 ⇨⇧' },
  { cat: 'new26', name_kr: '캬바레', name_en: 'Cabaret', ps: 'L2 홀드 + R스틱 ⇧ 홀드', xbox: 'LT + R스틱 ⇧' },
  { cat: 'new26', name_kr: '펄스(맥박 재기)', name_en: 'Pulse', ps: 'L2 홀드 + R스틱 ⇨⇦ 플릭', xbox: 'LT + R스틱 ⇨⇦', note: '샤키리 모티브 — 손목으로 맥박 확인 제스처' },
  { cat: 'new26', name_kr: '기타', name_en: 'Guitar', ps: 'L2 홀드 + 달리며 R스틱 시계방향 회전', xbox: '동일' },
  { cat: 'new26', name_kr: '올인원', name_en: 'All In One', ps: 'R1 홀드 + 달리며 R스틱 반시계 회전', xbox: 'RB + 동일' },
  { cat: 'new26', name_kr: '슬라이드 & 키스', name_en: 'Slides And Kisses', ps: 'R1 홀드 + R스틱 ⇩ 홀드', xbox: 'RB + R스틱 ⇩' },
  { cat: 'new26', name_kr: '팔 교차', name_en: 'Hands Crossed', ps: 'R2 홀드 + R스틱 ⇧ 홀드', xbox: 'RT + R스틱 ⇧' },
  { cat: 'new26', name_kr: '달리기', name_en: 'Run', ps: 'R2 홀드 + R스틱 ⇨⇦ 플릭', xbox: 'RT + R스틱 ⇨⇦' },
  { cat: 'new26', name_kr: '잠자기(낮잠)', name_en: 'Sleep / Nap', ps: 'R2 홀드 + R스틱 ⇦ 플릭', xbox: 'RT + R스틱 ⇦', note: '드러누워 자는 척 — 소스에 따라 ⇧두 번 플릭으로도 보고됨, 안 되면 병행 시도' },
  { cat: 'new26', name_kr: '하이킥', name_en: 'High Kick', ps: 'R1 홀드 + R스틱 ⇧ 홀드', xbox: 'RB + R스틱 ⇧', note: '이브라히모비치 모티브 — 동료가 쓰러지는 반응 연출' },
  { cat: 'new26', name_kr: '댄스', name_en: 'Dance', ps: 'L1 홀드 + R스틱 ⇧⇧ 플릭', xbox: 'LB + R스틱 ⇧⇧' },
  { cat: 'new26', name_kr: '치킨 댄스', name_en: 'Chicken Dance', ps: 'L1 홀드 + R스틱 ⇨⇨ 플릭', xbox: 'LB + R스틱 ⇨⇨' },
  { cat: 'new26', name_kr: '스트레치', name_en: 'Stretch', ps: 'R1 홀드 + R스틱 시계방향 회전', xbox: 'RB + 동일' },
  { cat: 'new26', name_kr: '그라운드 히트', name_en: 'Ground Hit', ps: 'R1 홀드 + R스틱 ⇩⇩ 플릭', xbox: 'RB + R스틱 ⇩⇩' },

  // 프로 언락(클럽 모드)
  { cat: 'pro', name_kr: '땅에 키스', name_en: 'Kiss The Ground', ps: 'R2 홀드 + R스틱 ⇨ 홀드', xbox: 'RT + R스틱 ⇨' },
  { cat: 'pro', name_kr: '주먹', name_en: 'Fists', ps: 'R2 홀드 + □ 더블탭', xbox: 'RT + X 더블탭' },
  { cat: 'pro', name_kr: '백플립', name_en: 'Backflips', ps: 'R2 홀드 + □ 더블탭', xbox: 'RT + X 더블탭' },
  { cat: 'pro', name_kr: '피스', name_en: 'Peace', ps: 'R1 홀드 + □ 더블탭', xbox: 'RB + X 더블탭' },
  { cat: 'pro', name_kr: '피전(비둘기)', name_en: 'Pigeon', ps: 'R1 홀드 + R3', xbox: 'RB + R3' },
  { cat: 'pro', name_kr: '기타 댄스', name_en: 'Guitar Dance', ps: 'R1 홀드 + R스틱 ⇧⇧ 플릭', xbox: 'RB + R스틱 ⇧⇧' },
  { cat: 'pro', name_kr: '호핑', name_en: 'Hopping', ps: 'R1 홀드 + R스틱 ⇨⇨ 플릭', xbox: 'RB + R스틱 ⇨⇨' },
  { cat: 'pro', name_kr: '릴랙스(오프라인 전용)', name_en: 'Relax', ps: 'R2 홀드 + R스틱 ⇦ 홀드', xbox: 'RT + R스틱 ⇦', note: '오프라인 전용' },
  { cat: 'pro', name_kr: '아이 오브 더 스톰', name_en: 'Eye of the Storm', ps: 'R1 홀드 + R스틱 반시계 회전', xbox: 'RB + 동일' },
  { cat: 'pro', name_kr: '무통제 백플립', name_en: 'Uncontrolled Backflip', ps: 'R2 홀드 + 달리며 R스틱 시계방향', xbox: 'RT + 동일' },
  { cat: 'pro', name_kr: '다트', name_en: 'Darts', ps: 'R2 홀드 + 달리며 R스틱 반시계', xbox: 'RT + 동일' },
  { cat: 'pro', name_kr: '눈과 팔', name_en: 'Eyes and Arms', ps: 'R2 홀드 + R스틱 ⇧⇧ 플릭', xbox: 'RT + R스틱 ⇧⇧' },
  { cat: 'pro', name_kr: '무릎 조정', name_en: 'Rowing on Knees', ps: 'R2 홀드 + R스틱 ⇦⇦ 플릭', xbox: 'RT + R스틱 ⇦⇦' },
  { cat: 'pro', name_kr: '아이스 스케이팅', name_en: 'Ice Skating', ps: 'R1 홀드 + R스틱 ⇩⇧ 플릭', xbox: 'RB + R스틱 ⇩⇧' },
  { cat: 'pro', name_kr: '골프 스윙', name_en: 'Golf Swing', ps: 'R1 홀드 + R스틱 ⇦⇨ 플릭', xbox: 'RB + R스틱 ⇦⇨' },
  { cat: 'pro', name_kr: '고글', name_en: 'Goggles', ps: 'R2 홀드 + R스틱 ⇧⇩ 플릭', xbox: 'RT + R스틱 ⇧⇩' },
  { cat: 'pro', name_kr: '댄스 3', name_en: 'Dance 3', ps: 'R2 홀드 + R스틱 ⇦⇨ 플릭', xbox: 'RT + R스틱 ⇦⇨' },
  { cat: 'pro', name_kr: '사진 찍기', name_en: 'Picture', ps: 'R2 홀드 + □', xbox: 'RT + X' },
  { cat: 'pro', name_kr: '요람 흔들기', name_en: 'Cradle Swing', ps: 'R2 홀드 + △', xbox: 'RT + Y' },
  { cat: 'pro', name_kr: '반지 키스', name_en: 'Kiss The Ring', ps: 'R2 홀드 + △ 더블탭', xbox: 'RT + Y 더블탭' },
  { cat: 'pro', name_kr: '슬라이드 살루트', name_en: 'Slide Salute', ps: 'R1 홀드 + R스틱 ⇨ 홀드', xbox: 'RB + R스틱 ⇨' },
  { cat: 'pro', name_kr: '마타도르', name_en: 'Matador', ps: 'R1(또는 R2) 홀드 + R스틱 ⇩⇧ 플릭', xbox: 'RB/RT + 동일' },
  { cat: 'pro', name_kr: '타임 체크(시계 확인)', name_en: 'Time Check', ps: 'R2 홀드 + R스틱 ⇨⇦ 플릭', xbox: 'RT + R스틱 ⇨⇦' },

  // EAS FC 언락
  { cat: 'eas', name_kr: 'KO', name_en: 'KO', ps: 'L1 홀드 + □ 더블탭', xbox: 'LB + X 더블탭' },
  { cat: 'eas', name_kr: '지금 여기서', name_en: 'Right Here Right Now', ps: 'R1 홀드 + ◯', xbox: 'RB + B' },
  { cat: 'eas', name_kr: '로우 피스트 펌프', name_en: 'Low Fist Pump', ps: 'L2 홀드 + R스틱 ⇧⇧ 플릭', xbox: 'LT + R스틱 ⇧⇧' },
  { cat: 'eas', name_kr: '스탠드 톨', name_en: 'Stand Tall', ps: 'R1 홀드 + R스틱 ⇦ 홀드', xbox: 'RB + R스틱 ⇦' },
  { cat: 'eas', name_kr: '팀버(쓰러지기)', name_en: 'Timber', ps: 'L2 홀드 + ◯', xbox: 'LT + B' },
  { cat: 'eas', name_kr: '락 온', name_en: 'Rock On', ps: 'L2 홀드 + R3', xbox: 'LT + R3' },
  { cat: 'eas', name_kr: '진정해(오프라인 전용)', name_en: 'Calm Down', ps: 'L1 홀드 + △ 더블탭', xbox: 'LB + Y 더블탭', note: '오프라인 전용' },
  { cat: 'eas', name_kr: '전화 받는 척', name_en: 'Phone It In', ps: 'L1 홀드 + R스틱 ⇧ 홀드', xbox: 'LB + R스틱 ⇧' },
  { cat: 'eas', name_kr: '해피 워크', name_en: 'Happy Walk', ps: 'L1 홀드 + R스틱 ⇩ 홀드', xbox: 'LB + R스틱 ⇩' },
  { cat: 'eas', name_kr: '프레데터', name_en: 'Predator', ps: 'L1 홀드 + R스틱 ⇩⇩ 플릭', xbox: 'LB + R스틱 ⇩⇩' },
  { cat: 'eas', name_kr: '게이머(컨트롤러 마임)', name_en: 'Gamer', ps: 'R1 홀드 + R스틱 ⇦⇦ 플릭', xbox: 'RB + R스틱 ⇦⇦' },
  { cat: 'eas', name_kr: '바이', name_en: 'Bye', ps: 'L1 홀드 + R3', xbox: 'LB + R3' },
];

/* 부가: 상황 트리거형(입력이 아니라 경기 상황이 조건) */
export const CONTEXT_CELEBRATIONS = [
  { name_kr: '마스코트 세리머니', name_en: 'Mascot Celebration', trigger: '홈 경기 + 마스코트 보유 팀 — 득점 후 터치라인 쪽 마스코트를 향해 달려가면 자동 발동' },
  { name_kr: '팬 상호작용', name_en: 'Fan Interaction', trigger: '홈 경기 한정 — R2+L2(RT+LT) 동시 입력 시 확률적으로 관중석 반응 연출' },
  { name_kr: '더비 승리 세리머니', name_en: 'Derby Win Celebration', trigger: '라이벌전에서 극장골로 승리 시 — 무릎 슬라이딩·엠블럼 가리키기 등 확률적 연출' },
  { name_kr: '역전골 세리머니', name_en: 'Comeback Goal', trigger: '2골차 이상 뒤지다 만든 득점 — 안도하며 무릎 꿇는 연출이 확률적으로 발동' },
];

export function mountCelebrationSearch(root){
  const esc = v => String(v??'').replace(/[&<>"']/g, ch => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch]));
  const hit = (c, q) => !q || (c.name_kr+c.name_en+(c.note||'')).toLowerCase().includes(q);

  function row(c){
    return `<tr><td><b>${esc(c.name_kr)}</b><br><small class="dim">${esc(c.name_en)}</small></td>
      <td class="mono">${esc(c.ps)}</td><td class="mono">${esc(c.xbox)}</td>
      <td class="dim" style="font-size:12px">${esc(c.note||'')}</td></tr>`;
  }

  function render(q){
    const query = (q||'').trim().toLowerCase();
    const groups = CATEGORIES.map(cat => {
      const rows = CELEBRATIONS.filter(c => c.cat === cat.key && hit(c, query));
      return { cat, rows };
    }).filter(g => g.rows.length);
    const anyQuery = query.length > 0;
    root.innerHTML = groups.map(g => `
      <details class="cele-group"${anyQuery ? ' open' : ''}>
        <summary><b>${esc(g.cat.label)}</b> <span class="badge">${g.rows.length}</span></summary>
        <table><tr><th>세리머니</th><th>PlayStation</th><th>Xbox</th><th>비고</th></tr>
          ${g.rows.map(row).join('')}
        </table>
      </details>`).join('') || '<p class="dim">일치하는 세리머니가 없습니다.</p>';
  }
  render('');
  return render;
}
