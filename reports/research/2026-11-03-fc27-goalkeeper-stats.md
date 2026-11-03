# EA SPORTS FC 27 골키퍼(GK) 속성 — EA 정책 · 스탯 작용 · 좋은 값 (등급 표기 리포트)

- 작성: 2026-11-03 · 대상: FC27(배경으로 FC26 이월분) · 등급 규약: docs/22 §2.1 / 불변규칙 12
  — **A** EA 1차 · **B** 데이터마이닝(게임 데이터 추출 사이트) · **C** 통제 실측 · **D** 통설(D로 명시)
- 사전 확인: docs/22 §3 GK 표 · reports/research/2026-09-21-fc27-system-stats.md §8 · `game_system_changes` FC27 #47·#57·#61·#65·#67·#68(중복 회피)
- ⚠️ 로케일 주의: EA 페이지의 한국어·스페인어·이탈리아어·포르투갈어·일본어판은 **같은 영어 원문의 번역**이다. 여러 언어로 같은 문장을 확인했어도 **교차검증 1건으로 세지 않는다**. 독일어·프랑스어 URL은 본문이 영어 그대로였다.

---

## 0. 요약 (먼저 읽을 것)

1. **⭐⭐ GK OVR 산정식은 「GK 4속성 균등」이다 (C · FC27 · 우리 실측 n=83).** 고전 커뮤니티 표 **다이빙·핸들링·포지셔닝·반사신경 각 21% + 반응력 11% + 킥 5%**에 **+1**을 더하면 FC27 비특별 GK 카드 83장 중 **76장 정확(92%) · 83장 ±1(100%)**이다. 제약 없는 최소제곱으로도 23.5 / 22.2 / 21.0 / 20.2 / 10.3 / 4.2(%)가 나온다. 반면 **우리가 저장한 적합값(반사 39 · 포지셔닝 25 · 다이빙 18 · 핸들링 13 · 반응 5 · 킥 0)은 같은 표본에서 40장(48%)만 맞는다** — GK 4속성 사이 상관계수가 0.91~0.94라서 생긴 공선성 착시로 보인다. ⇒ `fc_position_ovr_weights` GK 행은 **다시 맞춰야 한다**(부모 세션 판단).
2. **OVR 기준으로는 반사신경이 「가장 중요한」 스탯이 아니다 (C).** OVR 1점당 기여는 GK 4속성이 같고, 반응력은 그 절반, 킥은 4분의 1이다. 스피드(가속·질주)는 OVR에 **들어가지 않는다**(속도 항 없이 92% 재현). 「카드 앞면 6개(SPD 포함)가 OVR을 만든다」는 설명은 틀렸다.
3. **FC27에서 EA가 GK 메커니즘을 바꿨다는 1차 서술은 0건이다 (A · 부재).** FC27 Gameplay Deep Dive(07-29)에는 GK 언급이 없고, PlayStyle 리밸런스 10종에도 GK PlayStyle이 없다. TU v1.0.1~v1.1.0에서 GK 관련 수정은 버그 수정뿐이다. ⇒ FC27 GK 엔진은 **FC26 최종 상태(TU 1.5.x)를 이어받았다고 보는 게 가장 그럴듯하다**(추정 · EA가 확인한 적은 없다).
4. **EA 밸런스 입장 (A · FC27).** 원문은 「We're pretty happy with the current balance between shooting and goalkeeping」(「슈팅과 골키핑 사이 현재 밸런스에 꽤 만족한다」 · 09-30)다. 우리가 앞서 적어 둔 「fairly happy」는 원문 표현이 아니다. 10-28 글에서는 「Assessing the accuracy of specific shot types alongside goalkeeper positioning」(「특정 슛 종류의 정확도를 골키퍼 위치 선정과 함께 평가 중」)으로 바뀌었는데, **v1.2.0 적용 목록에는 들어가지 않았다**(#68). 그 뒤로 새 1차 발언은 찾지 못했다(10-30 Discord Q&A 정리본은 공개되지 않았다).
5. **GK PlayStyle은 효과가 슛 종류별로 갈린다 (A 툴팁 + B 게임 데이터 · FC27).** Far Reach는 **먼 거리 슛**에만 작동하고, Footwork는 **낮은 궤적 슛**에 작동한다. 니어포스트 로우드리븐 메타에 직접 맞서는 것은 Footwork다. 1v1 Close Down은 전진 속도만 올리는 게 아니라 **근거리 슛 궤적 읽기와 반사·예측 세이브 애니메이션**도 준다. Cross Claimer는 **경합 상황에서 펀칭을 우선**하게 만든다(잡기가 아니다).
6. **키·AcceleRATE·반응력이 인게임에서 무엇을 하는지에 대한 FC27 근거는 A·B·C 모두 0건이다.** 「190cm 이상」, 「196~197cm」, 「반사 > 다이빙」 같은 기준은 전부 **D(통설)**다. Pro Clubs 분석 사이트도 「EA hasn't said exactly what height does for a keeper, and there's no reliable FC 27 testing yet」(「EA는 키가 골키퍼에게 정확히 무엇을 하는지 밝힌 적 없고, 믿을 만한 FC27 실측도 아직 없다」)라고 스스로 적었다.
7. **FUT 실사용 메타 (D).** 쓰이는 카드는 OVR 순서가 아니다. Joan García(86 · 193cm · **Rush Out(=1v1 Close Down)+**)와 Mamardashvili가 가장 많이 쓰이고, 쿠르투아(90)는 인기가 줄고 있다. 상위 GK에게 가장 흔한 PS+는 Far Reach+다.

---

## 1. EA 1차 (A) — 각 속성이 무엇을 하나

### 1.1 FC27 1차 자료에 GK 속성 정의가 있는가 — **없다 (A · 부재)**

| 문서 | 날짜 | GK 관련 내용 | 직접 읽음 |
|---|---|---|---|
| FC27 Gameplay Deep Dive (Gilliard Lopes) | 2026-07-29 | **0건** — goalkeeper·keeper·save·parry·rush out 언급 없음 | ✅ |
| What are PlayStyles (FC27) | 2026-09-25 | GK PlayStyle 6종의 **선수 유형 설명**만 있음(§1.3). 효과 수치 없음 | ✅ |
| Gameplay Developer Launch Update | 2026-09-30 | 슈팅 대 골키핑 밸런스 「pretty happy」(§1.4) | ✅ |
| Launch Feedback Update | 2026-10-13 | 「Monitoring shooting variety, especially around low driven shots near the post」(「특히 포스트 근처 로우드리븐 슛을 중심으로 슈팅 다양성을 감시 중」) — GK라는 단어는 없음(#57) | ✅ |
| TU v1.1.0 | 2026-10-27 | GK 관련은 버그 수정 4건뿐(PC 마우스 · Clubs 11v11에서 GK 2명 · 진화 미리보기 녹색 표시 #65 · 1v1에서 GK가 공을 오래 쥐는 문제) | ✅ |
| October Gameplay Developer Notes | 2026-10-28 | 「조사 중」 항목에 슛 정확도 + GK 위치 선정(#68) | ✅ |

⇒ **다이빙·핸들링·킥·반사신경·GK 포지셔닝의 작용을 FC27에서 EA가 직접 정의한 문장은 없다.** 반응력이 「작용 서술 0건」이었던 것(#25)과 같은 구조다.

### 1.2 FC26 1차 (A · FC26 — FC27 이월 여부는 확인되지 않았다)

FC26 Gameplay Deep Dive(2025-07-22 · 직접 읽음)의 GK 절:
- 목표: 「Our goal with Goalkeepers is to make them more consistent and reliable」(「골키퍼를 더 일관되고 믿을 수 있게 만드는 것이 목표다」).
- **Deflection Control**: 「Most deflections will now go out of bounds, toward teammates, or to open space away from opponents.」(「이제 대부분의 쳐낸 공은 라인 밖, 동료 쪽, 또는 상대에게서 떨어진 빈 공간으로 간다.」) — Deflector가 없는 GK에게도 적용되는 **기본값**이다. Competitive에서는 「All GK deflections try to get away from danger, reducing rebound goals」(「모든 GK 쳐내기가 위험 지역을 피해 리바운드 골을 줄인다」).
- **Goalkeeper Senses**: 「refined goalkeeper's ability to read shot trajectories」(「골키퍼의 슛 궤적 읽기 능력을 다듬었다」).
- **Technical**: 「improved base systems for goalkeeper handling, more consistent shot-stopping, and more reasonable decision making in one-on-one situations」(「GK 핸들링 기반 시스템 개선, 더 일관된 선방, 1대1에서 더 합리적인 판단」).
- **⭐ RL GK Positioning**: 「RL Positioning is only active in certain situations, and is only used to position the Goalkeeper. The system is not active when making a save or performing a catch.」(「RL 포지셔닝은 특정 상황에서만, 골키퍼 위치를 잡는 데만 쓰인다. 세이브나 캐치 동작 중에는 작동하지 않는다.」) — **GK 포지셔닝 속성이 이 RL 시스템의 입력인지는 밝히지 않았다**(열린 질문).
- **FC IQ 역할**: Ball-Playing Keeper 「supports build-up play as a passing option and stays on their line when their team is in defense」(「빌드업에서 패스 선택지가 되고, 수비 시에는 라인에 머문다」) · Sweeper Keeper 「focused on rushing and coming out to recover balls during defence. This Role will not come out to support play as much.」(「수비 시 뛰쳐나와 공을 회수하는 데 집중한다. 빌드업 지원으로는 그만큼 나오지 않는다.」)
- 이 글에는 GK **속성**(다이빙·반사 등)과 **키**에 대한 서술이 없다.

FC26 TU 중 GK 관련 항목(A · FC26 · EA 패치노트 원문 미러 fifauteam·futwiz에서 직접 읽음. EA 포럼 원문은 403이라 검색 스니펫으로만 확인):
- **1.1.0(2025-10-23)**: 「Improved goalkeeper reactions to near post shots.」(「니어포스트 슛에 대한 GK 반응 개선」) · 「Improved goalkeeper punches to be stronger and have more consistent ball trajectories.」(「GK 펀칭을 더 강하고 궤적이 일관되게」) · 원 공격수 쪽·자책골 방향 쳐내기 감소 · 쓸데없는 자동 전진 수정.
- **1.2.0(2025-11-11)**: 「Goalkeepers were sometimes punching on crosses when it would've been more beneficial to catch the ball.」(「잡는 편이 나을 크로스에서 펀칭하던 문제 수정」) · 드리블러 근처 다이빙 판단 개선 · 파포스트 원터치 슛에서 한쪽으로 과하게 쏠리던 문제 완화.
- **1.3.0(2025-12-02)**: 「Greatly reduced movement speed and amount of ground covered when using Manual Goalkeeper Movement in open play.」(「오픈 플레이 수동 GK 이동의 속도·이동 범위를 크게 줄였다」) · Rush To Center 제거 · 「Slightly increased auto save assistance range across all assistance levels.」(「모든 보조 단계에서 자동 세이브 보조 범위를 약간 넓혔다」) · 크로스 캐치 일관성 향상.
- **1.4.2(2026-02-03)**: 예측 세이브 중 공을 너무 정확하게 쳐내던 문제 수정.

⚠️ 이 항목들이 FC27에도 그대로 있는지는 **EA가 확인하지 않았다**. 다만 FC27 1차 자료에 GK 변경이 0건이라는 점(§1.1)과 맞물려 「이월」이 가장 그럴듯한 가정이다.

### 1.3 GK PlayStyle 6종 (A 툴팁 · FC27)

**EA FC27 「What are PlayStyles」**(2026-09-25 · 직접 읽음)에 실린 선수 유형 설명:
- 1v1 Close Down: 「more aggressive when coming out of the box to gather over-the-top balls or long through balls」(「넘어오는 공·긴 스루패스를 처리하려고 박스 밖으로 더 공격적으로 나온다」)
- Cross Claimer: 「often come off the line to claim high balls from dangerous areas」(「위험 지역의 높은 공을 처리하러 자주 라인을 떠난다」)
- Deflector: 「great deflection control to safer spaces」(「더 안전한 공간으로 쳐내는 컨트롤이 뛰어나다」)
- Far Reach: 「cover the net and extend their reach to save challenging shots」(「골문을 넓게 커버하고 리치를 늘려 어려운 슛을 막는다」)
- Far Throw: 「starting counter attacks with long throws」(「긴 스로로 역습을 시작한다」)
- Footwork: 「using their feet to make difficult saves」(「발로 어려운 선방을 한다」)
- PlayStyle의 일반 규모: 「slightly improves」(「약간 향상시킨다」) / PS+ 「furthers that improvement」(「그 향상을 더한다」). 수치는 없다(#50: 설계 목표 5~10%).

**EA FC27 선수 레이팅 페이지 툴팁**(쿠르투아 · 직접 읽음):
- 「Rush Out+」: 「Unique reflex saves, better close shot reads, greater rush speed」(「고유 반사 세이브, 더 나은 근거리 슛 읽기, 더 빠른 전진 속도」)
- 「Far Reach」: 「Unique far dive animations, better long shot saves」(「고유 원거리 다이빙 애니메이션, 더 나은 중거리 슛 선방」)
- ⚠️ **EA 화면끼리 이름이 다르다** — PlayStyles 글은 「1v1 Close Down」(일본어판 「1v1接近戦」)인데 레이팅 DB는 여전히 「Rush Out+」(일본어판 Joan García 페이지 「飛び出し+」 · 스니펫)다. #61의 「개명」은 **EA 안에서도 다 반영되지 않았다**.

### 1.4 EA의 GK 밸런스 발언 — 원문

| 날짜 | 원문 | 번역 | 등급 |
|---|---|---|---|
| 2026-09-30 | 「We've seen feedback that low driven shots, particularly towards the near post, can be stronger than other options.」 | 「로우드리븐 슛, 특히 니어포스트 쪽 슛이 다른 선택지보다 강할 수 있다는 피드백을 봤다.」 | A |
| 2026-09-30 | 「We're pretty happy with the current balance between shooting and goalkeeping, but we'll continue to monitor your feedback and our data for any potential outliers.」 | 「슈팅과 골키핑 사이 현재 밸런스에 꽤 만족하지만, 이상치가 있는지 피드백과 데이터를 계속 감시하겠다.」 | A |
| 2026-09-30 | 「One of our core philosophies is that players should be rewarded for earning a shot from a dangerous area.」 | 「위험 지역에서 슛 기회를 만들어 낸 플레이어는 보상받아야 한다는 것이 우리 핵심 철학 중 하나다.」 | A |
| 2026-10-13 | 「Monitoring shooting variety, especially around low driven shots near the post」 | 「특히 포스트 근처 로우드리븐 슛 중심으로 슈팅 다양성 감시 중」 | A(#57) |
| 2026-10-28 | 「Assessing the accuracy of specific shot types alongside goalkeeper positioning.」 | 「특정 슛 종류의 정확도를 골키퍼 위치 선정과 함께 평가 중.」 | A(#68) |

- 로케일판(같은 원문의 번역 · 교차검증 아님): 한국어 「현재 슈팅과 골키퍼 간의 균형에는 꽤 만족하고 있지만」 · 스페인어 「Estamos bastante satisfechos con el equilibrio actual entre los tiros y las opciones de los guardametas」(「슛과 골키퍼 선택지 사이 현재 균형에 상당히 만족한다」) · 이탈리아어 「Siamo abbastanza soddisfatti dell'attuale equilibrio tra tiri e portieri」(「슛과 골키퍼 사이 현재 균형에 꽤 만족한다」) · 포르투갈어 「Estamos bastante satisfeitos com o equilíbrio atual entre as finalizações e a atuação de goleiros e goleiras」(「슈팅과 골키퍼의 플레이 사이 현재 균형에 꽤 만족한다」). 독일어·프랑스어 URL의 10-28 글은 본문이 영어 그대로다.
- 2026-10-30 Discord Q&A는 공지만 있고 **정리본을 찾지 못했다**(EA Discord 채널 전용으로 보인다).

### 1.5 참고 — FC Online(넥슨) 공식 능력치 설명 (A · **FC Online 전용 · FC27 근거 아님**)

넥슨 고객센터 「게임 능력치 상세 안내」(게시일 표시 없음 · 직접 읽음). 옛 EA FIFA 능력치 설명 계보로 보이지만 **엔진이 다른 별개 게임**이라 FC27 근거로 쓰지 않는다. 비교용으로만 남긴다.
- GK 다이빙: 「빠르고 정확하게 다이빙을 하는 것과 1 대 1 상황에서 성공적인 다이빙을 하는데 영향」
- GK 핸들링: 「공을 쳐내는 것보다 손으로 잡도록 하는데 영향」
- GK 반응속도: 「공의 굴절에 더 잘 반응하며, 단거리 슛, 프리킥, 페널티 킥 등에 빠르게 반응」
- 반응 속도(일반): 「골키퍼의 경우, 높은 반응 속도 능력치를 갖고 있을 수록 더 빠르게 세이브 동작을 취할 수 있습니다」
- 키: 「높은 GK 다이빙 능력치와 높은 키를 갖고 있으면 골대 구석으로 향하는 슛을 막는데 도움」

---

## 2. 데이터마이닝 (B)

### 2.1 GK PlayStyle 효과 텍스트 (B · FC27 · fut.gg 게임 데이터 · 2026-11-03 직접 읽음)

| PlayStyle | 효과 원문 | 번역 | 보유 수(일반 / +) |
|---|---|---|---|
| Far Reach | 「Unique long diving distance jump animations and increased chances of saving long distance shots.」 | 「고유 장거리 다이빙 점프 애니메이션, **먼 거리 슛** 선방 확률 증가」 | 81 / 7 |
| Footwork | 「Exclusive foot save animations and increased performance against low trajectory shots.」 | 「전용 발 세이브 애니메이션, **낮은 궤적 슛** 대응력 증가」 | 390 / 2 |
| 1v1 Close Down (slug rush-out) | 「Unique reflex/anticipation save animations, increase in rush speed and improved read of close shot trajectories.」 | 「고유 반사·예측 세이브 애니메이션, 전진 속도 증가, **근거리 슛 궤적** 읽기 향상」 | 86 / 7 |
| Deflector | 「Unique animations when deflecting the ball. Increased power to parry shots into safer areas.」 | 「쳐낼 때 고유 애니메이션, 슛을 안전한 곳으로 쳐내는 힘 증가」 | 104 / 5 |
| Cross Claimer | 「…prioritization of punch animations in contested ball scenarios, and increased speed for coming out for crosses.」 | 「…경합 상황에서 **펀칭 애니메이션 우선**, 크로스에 나오는 속도 증가」(앞부분: 고유 펀칭 애니메이션, 손 힘·펀칭 볼 속도 증가) | 246 / 6 |

⇒ **슛 종류마다 맡는 PlayStyle이 다르다.** 이 텍스트는 EA 툴팁(§1.3)과 방향이 같다(같은 게임 데이터에서 나왔을 가능성이 커서 독립 교차검증은 아니다).

### 2.2 GK 역할·포커스 (B · FC27 · fut.gg /roles/gk · 스니펫)

Goalkeeper(Defend · Balanced) · Sweeper Keeper(Balanced · Build-Up) · Ball-Playing Keeper(Build-Up). Defend에서는 「won't rush out to collect long or loose balls」(「긴 공·루즈볼을 잡으러 나오지 않는다」). ⚠️ fut.gg 역할 엔드포인트에는 버전 인자가 없다는 점이 §8.4에서 이미 확인됐다 — 이 목록이 FC26 카탈로그를 다시 올린 것일 수 있다. BPK는 FC26 신설이다(§8.8).

### 2.3 GK OVR 산정식 — 공개된 것

- **EA는 공개하지 않았다.** sofifa 계산기(FC27 대상)는 입력란만 있고 가중치를 보여 주지 않는다(직접 읽음).
- fifauteam FIFA 19 가이드(2018 · 직접 읽음): 다이빙 24 · 핸들링 22 · 포지셔닝 22 · 반사 22 · 반응력 6 · 킥 4(%) + 국제 명성(IR) 보너스 최대 +3. 등급 **D**(데이터마이닝 근거가 제시되지 않았고 8년 전 버전이다).
- 「21/21/21/21/11/5」 표는 검색 결과에서 **출처 페이지를 찾지 못했다**. 오래 돌던 커뮤니티 표다(D). ⇒ 이 표의 FC27 타당성은 §3.1의 우리 실측(C)으로 처음 확인된다.
- GameBoost(반사 30 · 다이빙 25 · 핸들링 20 · 포지셔닝 15 · 킥 10)와 GlobeHour는 **사이트가 직접 만든 순위용 가중치**라고 스스로 밝혔다 — OVR 산정식이 아니다(D).

### 2.4 숨은 GK 속성

FC27에서 데이터마이닝으로 공개된 숨은 GK 속성은 **찾지 못했다.** fut.gg 카드 데이터에는 GK 5속성 + 반응력 + 키·체형·AcceleRATE 태그(예: 「Lengthy 200cm Unique」)가 있다.

---

## 3. 통제 실측 (C)

### 3.1 ⭐⭐ 우리 실측 — GK OVR 산정식 대조 (C · FC27 · 2026-11-03)

- 표본: `player_card_items` FC27 · best_pos=GK · is_special=0 → **83장**(Rare/일반 기본 카드). 읽기 전용 질의 · 스크립트 /tmp/cmp/gkfit.py.
- 비교(반올림 = floor(v+0.5)):

| 산정식 | 정확 일치 | ±1 | 평균 오차(예측−실제) |
|---|---|---|---|
| 고전 21/21/21/21/11/5 **+1** | **76/83 (92%)** | **83/83** | ≈0 |
| fifauteam FIFA19 24/22/22/22/6/4 +1 | 58/83 | 83/83 | — |
| 고전 표, 보정 없음 | 0/83 | 76/83 | −1.08 |
| **우리 저장값 18/13/25/39/5/0** (`fc_position_ovr_weights` 2026-10-02) | **40/83 (48%)** | 82/83 | −0.31 |
| GameBoost 순위용 30/25/20/15/10 | 33/83 | 73/83 | −0.65 |
| 고전 표 × 1.0125(곱하는 보정) | 70/83 | — | — |

- 제약 없는 최소제곱(절편 없음): 다이빙 23.5 · 핸들링 22.2 · 포지셔닝 21.0 · 반사 20.2 · 반응력 10.3 · 킥 4.2(%), 합 1.013 → **고전 표와 사실상 같다.**
- GK 4속성 사이 상관계수가 0.91~0.94다. 「비음수 + 합=1」 제약을 건 적합이 가중치를 반사신경 쪽으로 몰아도 오차가 크게 늘지 않는 **공선성 구조**다. 그래서 우리 저장값은 ±1 정도로는 맞지만(82/83) 정확히는 절반만 맞는다.
- 빗나간 7장(오블락 88 · 알리송 87 · 픽포드 85 · Cata Coll 85 · 마르티네스 85 · Paños 82 · Earps 82)은 **모두 실제가 예측보다 1~2 높은 유명 선수**다. 옛 「국제 명성 보너스」 가설과 방향이 맞는다(IR 값이 DB에 없어 검증하지 못했다).
- **「+1」 상수의 정체는 모른다.** 53 OVR 하위 카드에도 똑같이 붙으니 IR 보너스는 아니다. 덧셈 +1(76장)이 곱셈 1.25%(70장)보다 잘 맞는다.
- **스피드(가속·질주)는 OVR 항에 없어도 92%가 재현된다** → 카드 앞면 SPD는 OVR에 들어가지 않는다.
- 한계: 비특별 카드만 썼다. 진화·특별 카드의 `overall +N` 보상은 이 식을 따르지 않는다(그게 「진화 부풀림」의 정의다). 저장 적합에 쓴 fut.gg 220장과는 표본이 다르지만, 일부 겹칠 수 있다.

### 3.2 외부 통제 실측 — **FC26·FC27 모두 0건**

다음 검색어로 찾았지만 같은 GK의 스탯 하나만 바꾼 A/B 실험, 키 비교 실험, PlayStyle 유무 실험은 **하나도 나오지 않았다**: 영어(「tested」 · 「experiment」 · 「99 reflexes vs 99 diving」 · 「height test」 · 「Far Reach test」) · 한국어 · 일본어 · 독일어 · 스페인어 · 프랑스어 · 이탈리아어 · 포르투갈어.
- 가장 가까운 자료는 pro11.net의 Clubs **관측 데이터**(2026-10-08 스냅샷 · 상위 100클럽 중 인간 GK가 있는 35클럽 · GK 41명 · 키 중앙값 197cm · 사분위 192~197cm)다. **선택 분포이지 효과 측정이 아니다** → D로 분류한다.
- FC Online(넥슨)의 2018년 「피파온라인4 골키퍼 연구」(fmkorea · 직접 읽음)는 표본 수와 통제 방법을 밝히지 않았고, 신뢰도 「80%」도 작성자의 주관 표기다. 다른 게임이라 FC27 근거에서 제외한다.

---

## 4. 커뮤니티 통설 (D — 전부 D다)

- **우선 스탯**: 「reflexes and diving matter most — they decide how many shots your keeper saves」(「반사와 다이빙이 가장 중요하다 — 몇 개를 막을지 결정한다」 · GameBoost · D). 스페인어권도 같다: 「los reflejos y la estirada son lo que más pesa」(「반사와 다이빙이 가장 무겁다」 · 스니펫 · D). FCRatings(FC26)는 반대로 포지셔닝을 꼽는다: 「A Goalkeeper with great Positioning rarely needs elite Reflexes.」(「포지셔닝이 좋은 GK는 최상급 반사가 거의 필요 없다.」 · D). **통설끼리도 갈린다.**
- **키**: 「190cm 이상」, 「196~197cm(Clubs Shot Stopper 상한)」, 「210cm가 190cm보다 더 커버한다」(Playnews · D). 반대 사례: 칸(188cm) · 앙게러(175cm) 아이콘이 상위권이다. 한국어 FC Online 커뮤니티의 「190~195는 애매하다」 류 체감은 별개 게임 · D.
- **킥**: 볼플레잉·스위퍼일 때만 의미가 있다는 통설(D). OVR에서는 5%(C).
- **AcceleRATE**: 상위 GK 대부분이 Lengthy라는 관찰(fut.gg 목록)만 있다. GK에게 AcceleRATE가 작동하는지에 대한 근거는 없다(A·B·C 0).
- **PlayStyle 픽**: Operation Sports 티어 — 「S+ Tier: Far Reach and Rush Out; S-Tier: Deflector and Footwork; A-Tier: Cross Claimer」(D). Sportskeeda 표준 빌드: Footwork+ / Far Reach · Rush Out · Deflector · Cross Claimer · Far Throw(D). timesaver(10-31)는 로우드리븐 대응으로 Footwork만 꼽는다(D · 근거는 EA 툴팁).
- **메타 카드(FUT)**: FUTBIN 경기 수 기준 최다 사용 GK는 Joan García · Mamardashvili(fifantastic 10-07 · 직접 읽음). 원문 「Mamardashvili posee una valoración general inferior, pero sigue apareciendo entre los porteros con mayor número de partidos.」(「마마르다슈빌리는 OVR이 더 낮은데도 경기 수 최상위 GK에 계속 나온다.」 · D). FUTevolution은 Joan García를 「Budget Meta GK」로 보고 Rush Out+를 강점으로 든다(스니펫 · D). FUTMind 메타 점수 상위는 부폰·쿠르투아·돈나룸마 순이고 가장 흔한 PS+는 Far Reach+다(스니펫 · D).
- **불만 동향(EA 포럼 · D)**: 니어포스트에 대한 취약, 「low driven power shots and long range driven power shots」(「로우드리븐 파워슛과 중거리 드리븐 파워슛」)을 못 막는다는 글이 있다(10월 · 스니펫).

---

## 5. 속성 표

| 속성 | 무엇을 하나 | 근거 등급 | 출처 |
|---|---|---|---|
| GK 다이빙 | FC27 EA 정의 **없음**. 통설: 다이빙이 필요한 슛에 닿는 능력 | A(부재) · D | EA FC27 Deep Dive(0건) · fifauteam FC27 attributes |
| GK 핸들링 | FC27 EA 정의 없음. 통설: 쳐내지 않고 잡는 능력. FC26 TU1.2.0에서 「잡는 게 나은 크로스에서 펀칭」 수정(속성 언급은 없음) | A(부재) · A(FC26 거동) · D | EA · fifauteam FC26 TU |
| GK 킥 | FC27 정의 없음. 통설: 골킥·배급 거리·정확도. OVR 5% | A(부재) · **C(OVR)** | §3.1 |
| GK 반사신경 | FC27 정의 없음. 통설: 근거리 슛에 반응하는 속도. OVR 21%(4속성과 동률) | A(부재) · **C(OVR)** · D | §3.1 · fifauteam |
| GK 포지셔닝 | FC27 정의 없음. FC26 RL 포지셔닝은 위치 잡기에만 쓰이고 세이브 중에는 꺼진다(속성과의 연결은 밝히지 않음). OVR 21% | A(FC26 시스템) · **C(OVR)** · D | EA FC26 Deep Dive · §3.1 |
| 반응력 | FC25~27 EA 정의 없음(#25). **GK OVR에 11%** — 필드 선수보다 비중이 크다 | A(부재) · **C(OVR)** | #25 · §3.1 |
| 스피드(가속·질주) | **GK OVR에 들어가지 않는다.** 인게임 작용은 근거 없음(1v1 Close Down의 「rush speed」와는 별개) | **C(OVR 제외)** · D | §3.1 |
| 키·체중 | FC27 근거 없음. (FC Online 넥슨 공식: 키+다이빙 → 구석 슛 — 별개 게임) | 없음 · D | pro11 자인 · 넥슨 |
| 점프 | Clubs Shot Stopper+ 조건(점프 90)이 있다는 Clubs 사양(단일 출처) · FUT 작용은 근거 없음 | B(Clubs · 단일 출처) · D | pro11 ← Pro Clubs HQ |
| Far Reach | **먼 거리 슛** 선방 확률 + 원거리 다이빙 애니메이션 | A 툴팁 · B | EA 레이팅 · fut.gg |
| Footwork | **낮은 궤적 슛** 대응 + 발 세이브 애니메이션 | B · A(유형 설명) | fut.gg · EA PlayStyles |
| 1v1 Close Down(=Rush Out) | 전진 속도 + **근거리 슛 궤적 읽기** + 반사·예측 세이브 애니메이션 | A 툴팁 · B | EA 레이팅 「Rush Out+」 · fut.gg |
| Deflector | 안전 지역으로 쳐내는 힘(FC26 기본 쳐내기 제어 위에 더해짐) | A(FC26 기본) · B | EA FC26 Deep Dive · fut.gg |
| Cross Claimer | 경합 시 **펀칭 우선**, 펀칭 볼 속도·손 힘 증가, 크로스에 빨리 나옴 | B · A(유형 설명) | fut.gg · EA PlayStyles |
| Far Throw | 스로 거리·애니메이션 | A 툴팁 · B | EA 레이팅 |

---

## 6. 좋은 값 — 등급별로 나눠 본다

**A (EA 1차)** — 수치 기준은 **없다.** EA는 GK 속성이나 키의 임계값을 FC25~27 어디에서도 공개하지 않았다.

**B (게임 데이터)** — 값이 아니라 **PlayStyle 고르기 기준**이다.
- 실점 원인이 니어포스트·로우드리븐 슛이면 **Footwork**(낮은 궤적)가 정확히 맞는 처방이다. Far Reach는 먼 거리 슛 전용이라 이 메타에는 맞지 않는다.
- 1대1·스루패스 실점이 많으면 **1v1 Close Down** — 근거리 슛 읽기까지 준다.
- 크로스를 **잡아내길** 원하면 Cross Claimer는 오히려 펀칭을 늘린다(텍스트상 그렇다 · 실측 없음).
- PS+ 상한은 3개다(#13·#21). 보유 희소성: Footwork+ 2장 · Deflector+ 5장 · Cross Claimer+ 6장 · Far Reach+ 7장 · 1v1 Close Down+ 7장(fut.gg · 11-03).

**C (우리 실측)** — **OVR 계산용**이다(인게임 선방력이 아니다).
- OVR ≈ round(0.21·(다이빙+핸들링+포지셔닝+반사) + 0.11·반응력 + 0.05·킥) + 1 (+ 유명 선수는 +1~2).
- ⇒ 진화로 GK 4속성 중 어느 것을 +1 해도 OVR 기여는 같다. 반응력 +2 ≈ GK 속성 +1, 킥 +4 ≈ GK 속성 +1.
- ⇒ 진화 「부풀림」(표기 Δ − 세부 스탯 Δ)을 GK에서 계산할 때 현재 저장 가중치(반사 39%)를 쓰면 **반사 진화는 Δ를 과대평가하고, 핸들링·다이빙 진화는 과소평가한다**.

**D (통설 — 근거 없음을 명시한다)** — 키 190cm 이상(Clubs는 196~197cm) · 반사·다이빙 85 이상 우선 · 킥은 BPK/SK에서만 · PS는 Far Reach+ / 1v1 Close Down+ / Footwork / Deflector.

---

## 7. 통설 대 근거 — 충돌·기각

| # | 통설 | 충돌하는 근거 | 판정 |
|---|---|---|---|
| M1 | 「반사신경이 GK OVR에서 가장 무겁다(30~39%)」 — GameBoost 30% · **우리 저장값 39%** | 4속성 균등 21%가 92% 재현 · 저장값은 48% (C) | ⛔ 기각. 우리 `fc_position_ovr_weights` GK 행도 해당된다 |
| M2 | 「카드 앞면 6개(SPD 포함)가 합쳐져 GK OVR이 된다」(GameBoost · FIFPlay) | 속도 항 없이 92% 재현 · 반응력(앞면에 없음)이 11% (C) | ⛔ 기각 |
| M3 | 「킥은 OVR에 0」(우리 저장값) / 「10%」(GameBoost) | 약 5% (C) | ⛔ 둘 다 기각 |
| M4 | EA가 「fairly happy」라고 했다(우리 메모) | 원문은 「pretty happy」(A) | 표현 정정(뜻은 같다) |
| M5 | 「Far Reach는 모든 다이빙의 리치를 늘린다」 | EA 툴팁 「better long shot saves」 · fut.gg 「long distance shots」 (A·B) | ⚠️ 범위 축소: **먼 거리 슛**에 한정 |
| M6 | 「Cross Claimer는 크로스를 더 잘 잡는다」(가이드 다수) | fut.gg: 경합 시 **펀칭 우선**(B) · FC26 TU1.2.0은 반대로 「잡는 쪽」으로 기본값을 고쳤다(A · FC26) | ⚠️ 「잡기」가 아니라 「빨리 나와서 펀칭」 |
| M7 | 「1v1 Close Down(Rush Out)은 스위핑 전용」 | 툴팁: 반사 세이브 + 근거리 슛 읽기(A·B) | ⛔ 기각. Joan García 메타의 근거 후보(D) |
| M8 | 「GK 속성 설명 = EA 공식」(fifauteam · 일본어 note.com) | fifauteam은 「EA data reviewers」(EA 데이터 리뷰어용) 문서 계보 — §8.1과 같은 구조. note.com(2026-09-25)은 출처를 「FUTeam – FC27 Attributes」로 적은 **번역 복제**다 | ⛔ 엔진 근거로 사용 금지 · 다국어 교차검증 아님 |
| M9 | 「키가 클수록 더 막는다(210 > 190)」 | A·B·C 0건 · pro11이 스스로 「no reliable FC 27 testing」이라고 적었다 | D 유지(검증 불가) |
| M10 | 「FC27 Ball-Playing Keeper는 신규 역할」 | FC26 Deep Dive에 이미 있다(A · FC26) | ⛔ 기각(§8.8과 같다) |
| M11 | 「FC27에서 Rush Out이 1v1 Close Down으로 완전히 개명됐다」(#61) | EA 레이팅 DB는 「Rush Out+」 · JA 「飛び出し+」를 그대로 쓴다 | ⚠️ EA 화면끼리 이름이 엇갈린다 — 둘 다 같은 PlayStyle로 취급할 것 |

---

## 8. 열린 질문

1. **키·체형·AcceleRATE가 GK 세이브 범위나 속도에 작용하는가** — FC27 근거 0건. 프랙티스 아레나에서 같은 OVR·다른 키(예: 183 대 200)의 GK로 같은 위치·같은 슛을 N≥50번 차는 실측이 필요하다.
2. **GK 포지셔닝 속성이 FC26 RL 포지셔닝의 입력인가** — EA는 시스템만 설명했다.
3. **반응력이 GK에게 무엇을 하는가** — OVR 11%라는 것만 확실하다(C). 인게임 작용 서술은 A 0건(#25).
4. **OVR 「+1」 상수와 유명 선수 +1~2의 정체** — IR 값을 수집하면 닫을 수 있다(fut.gg에 IR 필드가 있는지 확인 필요).
5. **v1.2.0(11월 중순)에 GK 위치 선정 조정이 들어가는가** — 10-28 시점에는 「조사 중」이고 적용 목록 밖이다. 패치노트가 나오면 다시 확인해야 한다.
6. **10-30 Discord Q&A 정리본** — 공개된 곳을 찾지 못했다.
7. PlayStyle 「+」의 크기 — 「even better」(「더 좋다」) 표현만 있다. #50의 5~10%가 GK에도 적용되는지 모른다.

---

## 9. 출처 목록

표기: 언어 · 날짜 · **R**=직접 읽음 / **S**=검색 스니펫만 · 등급

**EA 1차 (A)**
1. https://www.ea.com/games/ea-sports-fc/fc-27/news/pitch-notes-fc27-gameplay-deep-dive · EN · 2026-07-29 · R · A(GK 0건)
2. https://www.ea.com/games/ea-sports-fc/fc-27/news/what-are-playstyles · EN · 2026-09-25 · R · A
3. https://www.ea.com/ja/games/ea-sports-fc/fc-27/news/what-are-playstyles · JA · 2026-09-25 · R · A(번역)
4. https://www.ea.com/games/ea-sports-fc/fc-27/news/fc-27-gameplay-developer-launch-update · EN · 2026-09-30 · R · A
5. https://www.ea.com/ko/games/ea-sports-fc/fc-27/news/fc-27-gameplay-developer-launch-update · KO · 2026-09-30 · R · A(번역)
6. https://www.ea.com/es/games/ea-sports-fc/fc-27/news/fc-27-gameplay-developer-launch-update · ES · 2026-09-30 · R · A(번역)
7. https://www.ea.com/it/games/ea-sports-fc/fc-27/news/fc-27-gameplay-developer-launch-update · IT · 2026-09-30 · R · A(번역)
8. https://www.ea.com/pt-br/games/ea-sports-fc/fc-27/news/fc-27-gameplay-developer-launch-update · PT · 2026-09-30 · R · A(번역)
9. https://www.ea.com/games/ea-sports-fc/fc-27/news/fc-27-launch-feedback-update · EN · 2026-10-13 · R · A
10. https://www.ea.com/games/ea-sports-fc/fc-27/news/fc27-title-update-v1-1-0 · EN · 2026-10-27 · R · A
11. https://www.ea.com/games/ea-sports-fc/fc-27/news/fc27-october-gameplay-developer-notes · EN · 2026-10-28 · R · A
12. https://www.ea.com/de/games/ea-sports-fc/fc-27/news/fc27-october-gameplay-developer-notes · DE URL(본문 EN) · 2026-10-28 · R · A
13. https://www.ea.com/fr/games/ea-sports-fc/fc-27/news/fc27-october-gameplay-developer-notes · FR URL(본문 EN) · 2026-10-28 · R · A
14. https://www.ea.com/games/ea-sports-fc/ratings/player-ratings/thibaut-courtois/192119 · EN · 날짜 없음(11-03 접속) · R · A(툴팁)
15. https://www.ea.com/de/games/ea-sports-fc/ratings/player-ratings/thibaut-courtois/192119 · DE · S · A(번역)
16. https://ea.com/ja/games/ea-sports-fc/ratings/player-ratings/joan-garcia/259532 · JA · S · A
17. https://www.ea.com/games/ea-sports-fc/fc-26/news/pitch-notes-fc26-gameplay-deep-dive · EN · 2025-07-22 · R · A(FC26)
18. https://forums.ea.com/blog/ea-sports-fc-game-info-hub-en/fc-26-v1-1-0-update-notes/12815780 · EN · 2025-10 · S(403) · A(FC26)
19. https://forums.ea.com/blog/ea-sports-fc-game-info-hub-en/ea-sports-fc-27-%E2%80%94-career-mode-developer-qa/13776351 · EN · 2026-10 · S · A(GK는 「pass it onto the gameplay team」(「게임플레이 팀에 전달하겠다」) 한 줄)
20. https://cs.nexon.com/helpBoard/popuphelpview/17492 · KO · 날짜 없음 · R · A(**FC Online 전용**)

**EA 패치노트 미러 (A 텍스트 · 2차 경로)**
21. https://fifauteam.com/fc-26-title-update/ · EN · 2025-10~2026-05 · R
22. https://www.futwiz.com/news/article/fc-26-title-update-full-notes-1-2-0/12658 · EN · 2025-11-10 · R
23. https://www.futwiz.com/news/article/fc-26-pitch-notes-v1-1-0/12502 · EN · 2025-10 · S

**데이터마이닝 (B)**
24. https://www.fut.gg/playstyles/far-reach/ · EN · 11-03 접속 · R
25. https://www.fut.gg/playstyles/footwork/ · EN · R
26. https://www.fut.gg/playstyles/rush-out/ · EN · R
27. https://www.fut.gg/playstyles/deflector/ · EN · R
28. https://www.fut.gg/playstyles/cross-claimer/ · EN · R
29. https://www.fut.gg/playstyles/ · EN · R
30. https://www.fut.gg/roles/gk/ · EN · S
31. https://www.pro11.net/best-shot-stopper-build/ · EN · 2026-11-01 갱신 · R · B(Clubs AP 비용 · 단일 출처 Pro Clubs HQ) / D(키 관측)

**통제 실측 (C)**
32. 우리 실측 — `db/tactics.db` player_card_items FC27 GK 83장 · /tmp/cmp/gkfit.py · 2026-11-03 · C

**통설·가이드 (D)**
33. https://fifauteam.com/fc-27-attributes/ · EN · 날짜 없음 · R
34. https://fifauteam.com/player-ratings-guide-fifa-19/ · EN · 2018 · R
35. https://sofifa.com/calculator?hl=en-US · EN · R(가중치 미표시)
36. https://www.eloascend.com/blog/ea-sports-fc/playstyles · EN · 2026-10-16 · R
37. https://timesaver.gg/blog/fc-27-low-driven-shot-how-to-do-it-near-post-nerf-status · EN · 2026-10-31 · R
38. https://gameboost.com/blog/best-goalkeepers-in-ea-fc-27 · EN · S
39. https://www.operationsports.com/here-are-the-best-playstyles-for-all-positions-in-ea-fc-27/ · EN · S
40. https://www.sportskeeda.com/esports/best-playstyles-roles-ea-fc-27 · EN · S
41. https://buffbuff.com/blog/fc-27-best-goalkeepers · EN · S
42. https://futmind.com/players/best/gk · EN · S
43. https://www.futevolution.com/reviews/fut27-joan-garcia-259532 · EN · S
44. https://tech.yahoo.com/gaming/articles/ea-fc-27-best-goalkeeper-120938316.html · EN · 2026-10 · S(403)
45. https://forums.ea.com/discussions/fc-27-general-discussion-en/goalkeepers---they-need-to-deal-with-2-types-of-shots-better-/13810164 · EN · 2026-10 · S
46. https://forums.ea.com/discussions/fc-27-feedback-en/fc-27-gameplay-feels-inconsistent-and-unresponsive-across-too-many-mechanisms/13763943 · EN · 2026-10 · S
47. https://www.playnews.gg/en/guides/tallest-players-ea-sports-fc-27-outfield-players-and-goalkeepers · EN · S
48. https://www.fcratings.com/articles/ea-sports-fc-26-attributes-explained · EN · S(FC26)
49. https://www.fifplay.com/fc-27-attributes/ · EN · S
50. https://www.si.com/soccer/best-goalkeepers-ea-fc-27-official-ratings · EN · S
51. https://timesaver.gg/blog/fc-27-archetypes-reset-october-22-ap-cost-changes · EN · S(Clubs)
52. https://fifantastic.com/futbolistas-mas-utilizados-fc-27/ · ES · 2026-10-07 · R
53. https://vandal.elespanol.com/guias/guia-ea-sports-fc-27-trucos-consejos-y-secretos/mejores-porteros · ES · S
54. https://proclubshq.com/blog/build-paragoles-fc-27-clubes-pro/ · ES · S
55. https://imiglioridififa.com/ea-fc-27-nuova-evoluzione-portiere-guardiano-come-blindare-la-porta-della-tua-squadra-goal-guardian/ · IT · S
56. https://gustacoins.com.br/blog/goleiros-baratos-ea-fc-27 · PT · S
57. https://blog.lojadocapita.com.br/2026/10/14/melhores-goleiros-ea-fc-27/ · PT · 2026-10-14 · S
58. https://www.dexerto.fr/wikis/ea-fc-27/meilleurs-builds-clubs-ea-fc-27/ · FR · S
59. https://www.redbull.com/fr-fr/ea-fc-27-meilleures-pepites-gardien · FR · S
60. https://earlygame.com/de/guides/fifa/ea-fc-27-poor-sophia-evolution-die-besten-torhueter-upgrades-anforderungen · DE · S
61. https://note.com/new_gate_green/n/nc220e7978534 · JA · 2026-09-25 · R(fifauteam 번역 복제)
62. https://www.redbull.com/jp-ja/ea-fc-27-ultimate-team-meilleures-cartes · JA · S
63. https://gall.dcinside.com/board/view/?id=fifaonline&no=1076485 · KO · 2018-08-26 · R(FC Online)
64. https://www.fmkorea.com/best/1134516246 · KO · 2018-07-02 · R(FC Online)
65. https://www.fmkorea.com/6781088087 · KO · 약 2.7년 전 · S(FC Online)

**접근 실패**: forums.ea.com 글 전부 403(스니펫으로만 확인) · FUTBIN PlayStyle 페이지 403 · Yahoo Tech 403 · EA 10-30 Discord Q&A 정리본은 미공개(Discord 전용 추정) · fut.gg는 이번에는 읽혔다(10-31 커밋에서는 Cloudflare 차단).
