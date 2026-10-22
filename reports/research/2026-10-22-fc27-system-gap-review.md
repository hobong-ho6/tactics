# FC27 시스템 미파악 영역 검토 (2026-10-22)

> 읽기 전용 검토 — DB `game_system_changes`(FC27 44행 · 마지막 적재 2026-10-12) · `reproduction_limits`(FC27 16행) · docs/21·22 · `reports/research/2026-09-21-fc27-system-stats.md` · HANDOFF 000⑴⑷⑸⑹를 기준선으로 두고, 2026-10-12 이후 자료를 EA 1차·커뮤니티·한국어·독일어로 훑었다.
> 근거 등급은 불변규칙 12(A EA 1차 · B 데이터마이닝/fut.gg · C 통제 실측 · D 통설). 외국어 인용은 원문 「…」 뒤 괄호 번역. **DB에는 아무 행도 넣지 않았다** — ⒜ 표가 후보다.
> 오늘(10-22) 기준 EA 뉴스 색인: 10-13 「Launch Feedback Update」 · 10-19 「The Grounds Developer Archetypes Update」 · 10-22 「Season 2: FC Heritage」. 타이틀 업데이트는 v1.0.4(10-07)가 마지막이고 **게임플레이 밸런스 변경은 출시 후 0건**이다.

## 0. 한 줄 결론

- **새로 알게 된 것은 많지 않고, 「아직도 모르는 것」이 그대로다.** EA는 10-13에 풀백 하강·킥오프 골·저수비 스탯 인터셉트·로우드리븐·파울 5건을 「감시·조사 중」으로 재확인했을 뿐 수정 일정이 없다. 우리 #45·#46·#47(09-30 원문)은 그대로 유효하고, 10-13 원문은 **A등급 새 행 1건**으로 올릴 가치가 있다.
- 라인 높이 4구간(1–30/31–60/61–90/91–100)·빌드업 3종 정의는 **FC27에서 EA가 다시 쓴 적이 없다** — 커뮤니티 가이드(fifauteam·fctactics 등)가 FC25 표를 그대로 옮긴 것뿐이다. `core/team_settings.py`의 Deep ≤45·Balanced ≤62는 여전히 EA 구간 밖이고, 닫는 길은 인게임 슬라이더 실측뿐이다(§3 ⑵).
- 역할·포커스 목록은 fut.gg가 「31 Roles」라고 쓰지만 이름 기준 31 ≈ 우리 30(+ST 와이드PM 표기 차) · 포지션 기준 37로 **FC26과 전항 일치**가 재확인된다. ST 4역할의 포커스 목록(fut.gg 10-22 열람)이 우리 DB와 글자 그대로 같다.
- PlayStyle은 **36종**이 맞다(EA 페이지는 35개만 인쇄 — Power Shot 누락 · fut.gg 36). **Rush Out → 1v1 Close Down 개명**은 우리 카탈로그(docs/22 §3 · `fc_playstyle_ids` · `fut_club_players` 6장 「Rush Out」)에 아직 반영되지 않았다 — 어휘 드리프트 후보.
- 역할·포커스별 선수 이동량의 **통제 실측(C)은 10-22에도 영·독·한국어권 어디에도 없다.** 빌라 구현 판단 5건(RDM·ST·LM·LB·리드 프리셋)을 바꿀 새 근거는 **0건**이다.

## 1. 지금 아는 것 — 주제별 마지막 출처일

| 주제 | 우리 행 | 마지막 1차 출처 | 상태 |
|---|---|---|---|
| Team Press 수비 3분의 1 무효 · 수비수 압박 효율↓ | gsc #14 · #20 · limit #18 | Closed Beta Feedback Update 2026-09-03 (A) | 변동 없음 — 10-13 문서에 언급 없음 |
| 낮은 뎁스가 더 문자 그대로 반영 | gsc #14 | 09-03 (A) | 변동 없음 · 풀백 하강 현상과 같은 뿌리로 읽히나 EA가 연결한 적 없음 |
| 풀백 조기 하강(라인 깨짐) | gsc #45 · limit #30 | Gameplay Developer Launch Update 09-30 (A) | **10-13 재확인 — 미수정 · 일정 없음**(§2 ⒜1) |
| Triggered Runs 거리 제한 · ASA | gsc #10·#11·#19 · limit #29 | 09-03 (A) | 변동 없음 |
| 리시버 트랩 보정 제거(Pinged·Tiki Taka) | gsc #22 | Gameplay Deep Dive 09-xx (A) | **Incisive Pass도 같은 제거 대상** — 우리 행은 두 종만 적음(§2 ⒜4) |
| PlayStyle+ 상한 3 · 프로모 Role++ | gsc #13 · #21 · docs/22 §6.1 | Launch Update 09-14 (A · #21은 2차 인용) | 09-14 원문 확보 — 「Campaign Player Items … all of their position's Roles++」(§2 ⒜3) |
| 케미 ICON 국적 +1 · Hero 리그 +1 · Hall of FUT | gsc #28 (B) | 09-14 원문 미대조(HANDOFF 000⑴) | **원문 확보(A)** — 000⑴ 닫을 수 있음(§2 ⒜2) |
| 라인 높이 4구간 · 빌드업 3종 정의 | 리서치 §5.2·5.3 · `game_tactic_params` FC27 9행 | FC25 FC IQ Deep Dive (A · FC27 재확인 없음) | **변동 없음 — 여전히 FC25 전용**(§3 ⑵⑶) |
| 역할 숙련도 작용(긴급성) | 리서치 §4.3 | 09-03 (A) | 수치 0 · 통제 실측 0 (§3 ⑷) |
| AcceleRATE 임계 · 영향 축소 | gsc #12 · docs/20 ⑤ | 09-03 (A) | 남성 임계 변경 없음(§3 ⑸) |
| 스탯 선형/계단 · 반응력·침착·시야 | gsc #25·#26·#43·#55 | 09-21 조사 (A 부재 증거) | **10-22에도 새 B·C 0건** |
| 출시 초기 밸런스 동결 | gsc #18 · #47 | TU v1.0.4 10-07 (A) | 유지 — Season 2(10-22) 게임플레이 변경 없음 |

## 2. ⒜ 새로 알게 된 것 — `game_system_changes` 후보 행 (미삽입)

| # | area | 내용(원문 「…」 + 번역) | 출처 · 날짜 | 등급 | 우리 행과의 관계 | 빌라 구현 영향 |
|---|---|---|---|---|---|---|
| 1 | positioning | EA Launch Feedback Update: 「fullbacks are dropping too deep while defending, causing issues with defensive structure」(풀백이 수비 시 너무 깊이 내려와 수비 구조에 문제를 일으킨다) · 「Fullback positioning directly affects the overall balance of gameplay」(풀백 위치는 게임플레이 전체 균형에 직접 영향을 준다 — 변경에 신중하겠다) · 같은 문서가 킥오프 골·저수비 스탯 인터셉트·니어포스트 로우드리븐·파울 판정을 「monitoring / investigating」으로 유지 | ea.com `fc-27-launch-feedback-update` · 2026-10-13 | **A** | #45·#46·#47의 **재확인** — 「조사 중」이 13일 지나도 「조사 중」. 수정 일정 없음 | LB att_wb vs 윙백 A/B는 계속 유보(limit #30 유지). 리드 프리셋에 Deep을 쓸 때 풀백이 CB보다 더 내려가는 부작용을 셀 것 |
| 2 | meta | Launch Update 원문: 「ICONs will continue to receive full Chemistry when played in position and provide a +1 League link to every League. Their Nation contribution is being reduced from +2 to +1.」(아이콘은 자리에 맞으면 풀 케미를 받고 모든 리그에 +1 링크를 준다. 국적 기여는 +2에서 +1로 줄어든다) · Hero 「League contribution is being reduced from +2 to +1」(리그 기여 +2→+1) · 「Their +1 Nation contribution remains unchanged」(국적 +1 유지) · Hall of FUT 「will follow the same Chemistry rules as Heroes」(히어로와 같은 케미 규칙) | ea.com `pitch-notes-fc27-launch-update` · 2026-09-14 | **A** | #28(B · timesaver 2차)을 **A로 격상하는 새 행** — HANDOFF 000⑴ 「원문 대조 후 적재」 충족 | 케미 solver 상수 변경 없음(#28이 이미 반영) · 000⑴ 종료 |
| 3 | meta | 같은 문서: 「all Campaign Player Items will launch with all of their position's Roles++ unlocked」(모든 캠페인 선수 아이템은 해당 포지션의 Role++ 전부를 해제한 채 출시된다) · OTW도 동일 | 09-14 (A) | **A** | #21(2차 인용 MEDIUM)을 원문으로 보강 · 범위는 「Campaign Items」 — FUT Deep Dive의 「all special Items」(리서치 §4.4)와 합치면 스페셜 전체 | docs/22 §6.1 「역할 숙련은 판정 층에서 제외」 유지 |
| 4 | playstyles | Incisive Pass에서도 **리시버 트래핑 오차 감소가 제거**됐다 — 커뮤니티 정리 「FC 27 removes the previous reduction to the receiver's trapping error」(종전의 수신자 트래핑 오차 감소를 제거했다) · EA 공식 설명은 「More accurate through balls, more swerve curve, and faster precision passes」(스루패스 정확도·스워브 커브·정밀 패스 속도)로 수신자 효과 없음 | Operation Sports/timesaver 정리 · EA `what-are-playstyles` 09-25 | **B**(정리) + **A**(EA 설명에 수신자 효과 부재) | #22의 **확장** — 「패서가 리시버를 덮는 경로」가 Pinged·Tiki Taka·Incisive 3종 모두에서 끊김 | 처방 6.1 규약 그대로 · 바클리·고메스 「패서」 평가에 Incisive+ 가산 금지 명문화 |
| 5 | playstyles | PlayStyle 총수는 **36**(Scoring 8 · Passing 6 · Ball Control 5 · Defending 6 · Physical 5 · GK 6) · EA 페이지는 「36」이라 쓰고 35만 인쇄(**Power Shot 누락**) · fut.gg는 Power Shot 포함 36 · **Rush Out → 「1v1 Close Down」 개명**(fut.gg slug는 `rush-out` 유지) · 「Gamechanger」 한 단어 표기 | EA `what-are-playstyles` 09-25 (A) · fut.gg `/playstyles/` 10-22 열람 (B) | A/B | docs/22 §3 「Rush Out」 · `fc_playstyle_ids`(40행 · Flair·Trivela·Power Header·Aerial 등 FC24 잔존 이름 포함) · `fut_club_players` 「Rush Out」 6장 · `player_game_stats` FC27 「Rush Out」 3행 — **어휘 드리프트**(§5 조치 2) | 스즈키 GK PlayStyle 판정(obs 「1 대1 클로즈다운」)은 이미 새 이름을 쓰고 있어 표기 불일치만 정리하면 됨 |
| 6 | tactics | fut.gg 커뮤니티 전술 통계(실사용 스쿼드 추적): 4-2-3-1 Wide 사용 5%/프로 3% · 빌드업 Balanced 52/62% · 수비 Balanced 66/56% · **라인 60** · 대표 코드 `xYJb3Bj37tdy` · 역할 분포 ST Advanced Forward·Attack 72/80% · LM/RM Inside Forward·Balanced 60~62/67~73% · CAM Shadow Striker·Attack 40/53% vs Playmaker·Balanced 44/47% · DM Holding·Defend 30/40% vs DLP·Build-Up 37/33% · FB Fullback Defend/Balanced 80% 안팎 · CB Defender·Defend 89/93% · GK Goalkeeper·Defend 66/67% | fut.gg `/tactics/4-2-3-1-wide/` 10-22 열람 | **B**(사용 통계 · 효과 근거 아님) | 새 축 — 「메타 대조군」. `fut_tactics`엔 우리 코드만 있고 메타 코드는 없음 | 인게임 A/B의 **대조군 코드**로 쓸 수 있다(§3 ⑻). ⚠️ 메타는 「이기는 설정」이지 「에메리 재현」이 아니다 |
| 7 | meta | TU v1.0.4(10-07): 「There are no gameplay balance and tuning changes in this update」(이번 업데이트에 게임플레이 밸런스·튜닝 변경은 없다) · 10-22 Season 2 「FC Heritage」 문서도 게임플레이·역할·케미 언급 0 · 10-19 Archetypes 문서는 The Grounds 전용 | ea.com 10-07 · 10-19 · 10-22 | **A** | #47의 연장(v1.0.4까지 동결 확인) | 처방 재검토 주기 그대로 |

## 3. 열린 질문 8건 — 답 / 미답

| 질문 | 답 | 등급 | 남은 것 |
|---|---|---|---|
| ⑴ 출시 후 TU 중 Team Press·라인·역할·풀백·Triggered Runs·ASA·리시버 트랩 변경 | **0건** — v1.0.1(Authentic 조키 슬라이더만) · v1.0.3 · v1.0.4 전부 버그 픽스. 풀백 하강은 10-13 「감시 중」 | A | 다음 TU 공지 감시(패치 감시 회차) |
| ⑵ FC27 라인 높이 슬라이더 의미 | EA FC27 1차 서술은 「lower depth settings are more clearly reflected … defenders retreating sooner」(낮은 뎁스가 더 뚜렷이 반영 — 수비수가 더 일찍 물러난다)뿐. 4구간(1–30/31–60/61–90/91–100 · 기본 25/50/70/95)·Run Tracking·Pressure 묶음은 **FC25 문서**이고 fifauteam·fctactics·howtovideogame이 그대로 전재. 「95 depth」 유행은 Aggressive 기본값일 뿐 | A(FC25) · D(FC27 전재) | **인게임 슬라이더 상하한 실측**(Deep에서 31 이상 입력 가능한가 · Balanced에서 61 입력 가능한가) — docs/50 절차 1회 · 30분. 결과로 `team_settings.py` 구간을 30/60/90 경계로 재정렬(새 행·G15) |
| ⑶ 빌드업 3종 FC27 정의 | EA FC27 재서술 없음. 커뮤니티 정의는 FC25 원문 전재 — Short Passing 「Players come short to support the ball carrier」(볼 캐리어를 받치러 짧게 온다) · Balanced 「alternate between coming short and making forward runs」(짧게 오기와 전진 런을 번갈아) · Counter 「more forward runs … exploit space behind」(전진 런·배후 공간). 체감 「Balanced feels faster than last year」(작년보다 빠르게 느껴진다)는 D | A(FC25) · D | 위치 차이 통제 실측 0건. 우리 규칙(롱볼 비율·점유)은 EA 정의(전환 시간·비볼 방향)와 **다른 축**이라는 점은 변함없음 — 인게임 A/B에서 빌드업만 바꾼 비조작 선수 평균 위치 비교(T6과 같은 단일 변수 설계) |
| ⑷ Role+/++ 측정 가능 효과 · 비숙련 페널티 | EA: 「Role Familiarity then influences the urgency with which a player makes those available runs」(숙련도는 가능한 런을 얼마나 급하게 실행하는지에 영향) · Out of Position은 「simplified Role and less effective positioning」(단순화된 역할·덜 효과적인 포지셔닝). 수치 공개 0 · EA Help 문서 0 · 커뮤니티 통제 실측 0 | A(정성) | 6.1 규약(판정 층 제외) **유지가 맞다** — 스페셜·캠페인 아이템 Role++ 일괄 부여로 변별력 없음. 베이스 골드 카드(스즈키·헤밍스 등 진화 대상)에서만 의미 — 진화 갈림길 기준(§6.2)에 「Role++ 가지는 긴급성 축」으로만 적음 |
| ⑸ AcceleRATE FC27 | 남성 임계 변경 없음: Explosive 키 ≤182 · 민첩 ≥65 · 민첩−힘 ≥10 · 가속 ≥80 / Lengthy 키 ≥183 · 힘 ≥65 · 힘−민첩 ≥4 · 가속 ≥40 / 나머지 Controlled · 여성 Lengthy 172cm(#12) · 프로필 영향 축소(#12) · 케미 스타일로 유형이 바뀔 수 있고 경기 중 변동은 반영 안 됨 | A(FC26 임계) + A(FC27 축소) + B(케미 스타일 유형 변경) | docs/20 ⑤ 유지 · 적합 가중치로 쓰지 않는 결정 유지 |
| ⑹ PlayStyle FC26→FC27 목록 차이 | 삭제 0 · 신설 0 · **개명 1**(Rush Out→1v1 Close Down) · 표기 1(Gamechanger) · 리밸런스 10(#13) · Incisive 수신 효과 제거(⒜4) · 총 36 | A/B | §5 조치 2(어휘 정리) |
| ⑺ Role++ 드리프트 · 진화 부여 역할 | 진화는 「lower frequency … more tailored progression paths, with specific positional and Attribute requirements」(빈도↓ · 포지션·속성 요건이 붙은 맞춤 경로) — Role++ 부여 가지는 베이스 카드에만 가치(#49와 일치). Season 2 문서에 진화·역할 변경 없음 | A | 변동 없음 |
| ⑻ 전술 코드·커뮤니티 전술 DB | 코드는 12자 영숫자+기호(`$ # @ % & ?`) · EA 공개 API 없음 · fut.gg `/tactics/<formation>/`·`/tactics/codes/`가 실사용 스쿼드 통계와 대표 코드 제공 · FUTBIN 커뮤니티 전술 목록(코드·투표) · nealguides 프로 코드 표(코드가 재생성됨 — 「Original/New Code」) | B | **메타 대조군 적재**(§5 조치 4) — 우리 `fut_tactics`는 사용자 계정 pulled만 담는다 |

## 4. ⒝ 우리 행과 충돌

| 우리 행 | 충돌 내용 | 판정 |
|---|---|---|
| docs/22 §3 「Rush Out」 · `fc_playstyle_ids` 「Rush Out」·「Game Changer」·「Flair」·「Trivela」·「Power Header」·「Aerial」 · `fut_club_players` 「Rush Out」 6장 · `player_game_stats` FC27(09-10) 「Rush Out」 3행 | EA FC27 공식 명칭은 「1v1 Close Down」·「Gamechanger」. Flair·Trivela·Power Header·Aerial은 FC27 목록에 없는 이름(FC24~25 잔존) | **어휘 드리프트** — 삭제가 아니라 별칭 표를 둔다(obs#527 교훈: 파생 어휘는 정본 집합 + 게이트) |
| gsc #22 「핑드 패스·티키타카」 | Incisive Pass도 같은 제거 — 두 종만 적어 **불완전** | 새 행으로 확장(⒜4) · #22는 덮지 않음 |
| gsc #21 「프로모 선수 Role++」(MEDIUM · 2차) | 원문은 「Campaign Player Items」 + OTW(09-14) · 「all special Items」(FUT Deep Dive) | 새 행(A)으로 보강 — 내용 충돌 아님 |
| gsc #28 (B) | 09-14 원문 확보 | 새 행(A) — 000⑴ 종료 |
| `game_tactic_params` FC27 9행 · 리서치 §5.2 라인 구간 | FC27에서 EA 재확인 없음 — 커뮤니티 전재는 근거 격상이 아님 | **충돌 아님 · 미확정 유지** — ⑵ 실측 전까지 「FC25 승계(미검증)」 라벨 |
| fut.gg 「31 Roles」 vs 우리 37 role_id / 30 이름 | 셈 기준 차이(이름 vs 포지션×역할) · ST 4역할 포커스 목록은 글자 그대로 일치 | 충돌 아님 |

## 5. ⒞ 여전히 모름 · 조사 방법 (docs/50 형식 — 사용자 플레이 필요 항목 ★)

| 모르는 것 | 왜 모르나 | 판가름할 실측 | 비용 |
|---|---|---|---|
| ★ 라인 슬라이더 FC27 상하한·구간 전환점 | EA FC27 1차 없음 · 커뮤니티는 FC25 전재 | 전술 화면에서 Deep 선택 후 31 입력 시도 → Balanced 61 → High 91. 각 구간 경계에서 Run Tracking 문구가 바뀌는지 UI 직독 · 스크린샷 4장 | 30분 · 플레이 불필요(메뉴만) |
| ★ 빌드업 3종이 비조작 선수 평균 위치를 얼마나 바꾸나 | 통제 실측 0(영·독·한) | 같은 XI·같은 역할·같은 수비접근/라인에서 빌드업만 3회 바꿔 비조작 선수 10명 히트맵 → `ingame_heatmap_to_grid.py` → 보유 국면 평균 x 비교(T6 단일 변수 설계 · 승점 비교 금지 obs#702) | 3경기 × 3 = 9경기 |
| ★ 역할 vs 포커스 이동량(FC27) | 리서치 §4.5 — 공개 실측 0 | 한 칸(RDM)만 dm_holding/Defend ↔ dm_dlp/Build-Up ↔ dm_dlp/Roaming 바꿔 비조작 상태 평균 위치·국면 그리드 비교 → obs#1080 판정 입력 | 3경기 × 3 |
| ★ 풀백 하강 현상이 att_wb/Support와 wingback/Balanced에서 다른가 | EA 「조사 중」 · 커뮤니티 테스트 0 | LB만 바꿔 비보유 국면 LB−CB x 차이 측정(라인 깨짐 빈도) | 3경기 × 2 |
| ★ Team Press 발동 선(수비 3분의 1 경계)의 실제 위치 | A(규칙)만 있고 좌표 0 | 수동 Team Press를 볼 위치 x=30/35/40에서 눌러 AI 반응 유무 기록 | 1경기 |
| Role++ 긴급성 수치 | EA 미공개 · 측정 설계 자체가 어려움(아이템 2장 필요) | 베이스 vs Role++ 같은 선수(진화 전/후 카드) 같은 역할로 비조작 런 횟수 비교 — 진화 중 헤밍스(Zoomaestro)가 유일한 표본 | 진화 완주 뒤 2경기 |
| 스탯 계단(반응력·볼컨·침착·시야) | A 부재 · B·C 0(09-21 → 10-22 변동 없음) | 공개 자료로는 못 닫는다 — 11월 중순 재검색 1회 후 「부재 증거」로 고정 | 검색 1회 |

## 6. ⒟ 빌라 구현 결정에 영향 요약

- **바뀌는 것 없음.** RDM(홀딩→DLP) · ST 포커스 · LM 포커스/역할 · LB 저점유 운용 · 리드 프리셋 5건의 보류(obs#1123)를 뒤집을 새 1차·실측 근거가 10-22까지 0건이다.
- **메타와의 거리(참고)**: 커뮤니티 4-2-3-1 Wide는 CAM Shadow Striker·Attack(40~53%) · ST Advanced Forward·Attack(72~80%) · 양 FB Fullback Defend/Balanced · LM/RM Inside Forward·Balanced · 라인 60. 우리 정본(CAM Playmaker/Roaming · ST Advanced/Support · LB att_wb/Support · LM insidefwd/Balanced · 라인 52)은 **「이기는 설정」이 아니라 「에메리 재현」**이므로 메타 쏠림을 근거로 바꾸지 않는다 — 다만 인게임 A/B의 대조군 코드로는 유용하다.
- **limit #30(풀백 조기 하강)은 유효 기간이 길어졌다** — EA가 「신중」을 못 박았으니 Season 2 내 수정 가능성은 낮다. LB att_wb 재현 판정은 수정 전까지 유보한다는 09-30 결정 유지.
- **Incisive Pass 수신 효과 제거**(⒜4)로 6.1 규약의 「패서 PlayStyle로 리시버를 덮지 않는다」가 패스 PlayStyle 3종 전부에 적용된다 — 바클리·고메스·맥긴의 「연결」 평가에서 Incisive+ 가산을 쓰지 않는다.

## 7. ⒠ 우선 조치 8건

| # | 조치 | 어디 | 합격 기준 |
|---|---|---|---|
| 1 | `game_system_changes` 새 행 4(⒜1 10-13 재확인 A · ⒜2 케미 원문 A · ⒜3 Campaign Role++ A · ⒜4 Incisive 수신 제거 B/A) + ⒜5·⒜7 1행씩 — 원문·번역·출처·등급 | DB(부모 ship) | FC27 행 44→50 · HANDOFF 000⑴ 체크 |
| 2 | PlayStyle 어휘 별칭 표 — `fc_playstyle_ids`에 FC27 정본 이름 + 별칭(Rush Out↔1v1 Close Down · Game Changer↔Gamechanger) · docs/22 §3 GK 행 개명 · **G35 확장**: `fut_club_players.current_playstyles`·`player_game_stats.playstyles`의 이름이 정본∪별칭 밖이면 실패 | migration(번호 부모) · gates.py · docs/22 | 모르는 이름 0 · FC24 잔존 이름 5종은 별칭 표에 「FC27 없음」으로 표기 |
| 3 | ★ 라인 슬라이더 상하한 실측(메뉴만 · 30분) → `team_settings.py` 구간 30/60/90 재정렬(새 규칙 버전 · G15 rule_note) · `game_tactic_params` FC27에 구간 행 | docs/50 · core/team_settings.py | match_game_setups Deep 35~40 행 4건에 rule_note 「구간 밖(FC25 기준) · 재입력 필요」 |
| 4 | 메타 대조군 적재 — fut.gg `/tactics/<formation>/`의 대표 코드·3축·11칸 분포를 `fut_tactics`와 분리된 표(`meta_tactics` · source=fut.gg · pulled)로 주간 수집(club-sync 뒤) | 신규 스크립트 · migration | 4-2-3-1 Wide · 4-4-2 · 3-4-2-1 행 ≥1 · 코드 `xYJb3Bj37tdy` 존재 |
| 5 | ★ 인게임 A/B T6(캐시 falseback)·T7(RDM 3종) 재개 — FC27 C등급 0건을 깨는 첫 캡처 · 프리셋 Competitive 명기(#44) | docs/50 · ingame_captures | FC27 캡처 ≥ 3경기 · `v_kernel_fidelity` FC27 행 ≥ 1 |
| 6 | 패치 감시 회차에 EA 뉴스 색인(`/fc-27/news`) 전수 비교를 넣는다 — 10-13·10-19·10-22 3건이 10-12 이후 미적재였다 | `.claude/skills` 패치 감시 프롬프트 · `reports/patch-watch/` | 회차마다 「색인 vs gsc.source」 차집합 0 |
| 7 | 한국어·독일어·스페인어 재검색 기록 — 이번 회차 0건(검색어: 「FC27 역할 포커스 전술 분석」 「인벤 FC 27 전술 역할 빌드업 라인 높이」 「FC 27 Taktik Test Rollen Fokus Spielerbewegung gemessen」 「FC 27 táctica roles prueba movimiento」) · 인벤·DC 직접 열람은 미수행 | 이 문서 | 11월 재검색 시 같은 검색어 반복 금지 |
| 8 | `reproduction_limits` FC27 새 행 1 — 「Incisive·Pinged·Tiki Taka 수신 보정 제거로 패서 품질이 리시버 터치를 보상하지 않는다」(limit · 6.1 규약 근거) | DB | FC27 limits 16→17 |

## 8. 검색 기록 (0건 포함)

- EA 1차: `/fc-27/news` 색인 1쪽(09-25~10-22 14건) · Launch Feedback Update(10-13) · Launch Update(09-14) · what-are-playstyles(09-25) · Season 2 FC Heritage(10-22) — 전부 직접 열람.
- 영어 커뮤니티: timesaver.gg(roles 37 · playstyles 36 · 95 depth · launch feedback) · fifauteam(roles · tactics · accelerate · title update history) · fctactics · howtovideogame · games.gg · eldorado · fut.gg(`/roles/` `/roles/st/` `/playstyles/` `/tactics/4-2-3-1-wide/`) · Operation Sports · Insider Gaming · EA 포럼 풀백 스레드 — **통제 실측 0건**.
- 한국어: fmkorea PlayStyle 번역 정리 1건(EA 원문 번역 복제 — 교차검증 아님 · 불변규칙 12) · 인벤·DC·유튜브 「FC27 전술」 직접 열람 미수행(검색 0건).
- 독일어: giga.de · pcgames.de 리뷰(정성) · 스페인어: 0건.
- Reddit: 역할/포커스 테스트 스레드 검색 0건(「reddit EASportsFC FC 27 tested roles focus heatmap experiment」).
