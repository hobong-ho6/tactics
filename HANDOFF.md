# HANDOFF — tactics

<!-- 구조 규칙(2026-10-14 v2): 헤더 15줄 안에 착수 조건 · 현재 상태 표 10행 이내 · 다음 할 일은 열린 항목만(항목당 2줄) · 세션 기록 최대 5개 · 목표 10~15KB · 상한 20KB(`wc -c`). 넘치면 지우지 말고 docs/handoff-context.md · docs/decisions.md로 포인터 압축. 절차 정본: .claude/skills/handoff/SKILL.md -->

- **담당자** 김호근 · **갱신** 2026-11-26 밤 · **세션** 부모 세션(대화) — 스위치백 다이너모 EFL 후보 검토 · 핸드오프 · **작업 PC** `AL02359162.local` · **브랜치** main · **WIP** 없음
- **마지막 커밋** = `git log -1`(이 문서를 갱신한 커밋) · 직전 `66d8c5d` · **문서 버전** v2 · **분량** 아래 「분량」 줄
- 실축 감독 전술(**AVL/에메리(주) · CHE/알론소 · LIV/이라올라 · ATM/시메오네**)을 실측으로 분해해 FC26·FC27 전술로 재현. 규약 정본 `CLAUDE.md`(불변규칙 1~14) · `docs/00-overview.md`.

> ⛔ **먼저 알 것**
> 1. **명시 스테이징만**(`git add -A` 금지) · DB 변경은 `python3 scripts/ship.py -m "…"` 한 줄 · **하위 세션은 커밋 안 함 — 부모가 `ship.py --collect <id>` 등록 후 모아서 ship · 끝나면 `--collect-end`** · migration 번호는 부모가 배정(최신 **140** — `ls db/migrations`가 정본 · 이 줄이 131로 낡아 있었다)
> 2. git엔 `.db`가 없다 — pull 뒤 `scripts/db_restore.sh` · 반복 사고 규칙 정본 [docs/70-lessons.md](docs/70-lessons.md) · **정기 수집은 AVL만** — CHE는 11-04 **1회성** 수집·정본 반영만(정기 수집 안 함) · LIV·ATM 보류(메모리 `che-atm-liv-collection-hold`)
> 3. 예약은 **PC마다 따로**(`list_scheduled_tasks`로 실재 확인 · 같은 작업 트리 → 스케줄 세션 중엔 커밋 보류) · ⭐ **새 불변규칙 14: 답변·리포트·화면은 결론 먼저 · 표/목록 · 인용 번역/원문 분리**(11-04)
> 4. yt-dlp는 봇 차단 → 브라우저 fetch/XHR 훅으로 `/api/timedtext` 응답 본문 포착 → COPY 버튼 실제 클릭 → `yt_transcript_json3.py VIDEO en /tmp/x.json3`(항상 뮤트) · ⭐ 패널이 숨겨진 스케줄 회차는 클립보드가 안 된다 → JS가 응답 본문을 **큰 반환값**으로 돌려주면 tool-results 파일로 떨어지니 그 파일에서 꺼낸다(11-23 5편 실증)

---

## 현재 상태

| 영역 | 상태 | 정본 |
|---|---|---|
| 게이트 | 전항 통과(11-05) · 11-04 추가: **G24 ⑸**(정본 표시 포메이션 `slots.is_canon` = 현행 optimal 포메이션) · **G23 `game_system_changes.title` 결손 0** · G12 메뉴 3칸 형식 · G37·G8+ 범위 **AVL·CHE** | `gates.py` |
| 경기 수집 | **11-24 UCL 갈라타사라이 원정 0-1 패** = matches #136 · 리포트 #72 draft · D+1·D+1 보강(11-25) · **D+2 수동(11-26)**: 필수 3채널 경기 후 영상 3편 전사·요약·주장 12행(전부 HELD) · 밍스 TNT 1차 발언 · **D+2 예약 회차(iMac · `9e3d9ef`)**: 터키어 분석 4편·부룩 회견·Tanswell X 에메리 원문 · **D+3 예약(11-27 20:00 · iMac)이 complete 판정** · 예약은 iMac에만 있다(AL02359162엔 0건) · 다음 **11-28 입스위치 원정** · 쟁점 #3 스즈키 GK 재판정(사용자 판단 대기) | `reports/match-watch/2026-11-24-avl-galatasaray.md` |
| 전술 정본 | AVL: optimal #46(4-2-3-1 Wide · Balanced/Balanced/52) · **3선 = RDM 홀딩/수비 · LDM 딥라잉/로밍 유지 + 계속 검토**(근거 `measured:pair:gomes/kamara` #1023·#1024 · 히트맵+경기 스탯) · 선발은 자동 산출(현재 LDM 고레츠카·RDM 고메스 — 사용자 「자동에 맡긴다」) · CHE: **optimal 신설 4-2-3-1 Wide · Balanced/Balanced/52**(LDM 딥라잉/빌드업 · 감시 쟁점 #91 = 다음 PL 3경기 3-4-2-1 복귀 시 재판단 · 수동 수집 때만) | `team_tactic_setups` · `slot_canon_roles` · [CHE 검토](reports/research/2026-11-04-che-season-review.md) |
| 사이트 UI | **11-04 전면 개편**(불변규칙 14): 메뉴 흐름 순서 · 「리포트」→「팀 전술」 · 허브=팀 대시보드 · 경기 분석 결론 카드 · 긴 패널 접기 · 팀 전술 39k→6.9k px · 게임 시스템 숫자 타일·영역 카드·**한 줄 제목**(migration 130)·인용 번역/원문 분리 · 이적 숫자 타일 · 스쿼드 표 접기 · 공용 부품 `data.js`(`matchScore`·`foldLong`·`mountPanelToc`)·`style.css` `ux-*` | `site/*.html` · `assets/data.js` |
| 게임 시스템 | `game_system_changes` 91행(전 행 `title`) · 11-04 코너·세트피스 #79~84 · 진화 포지션 조건은 보조 포지션 인정·제거 직후 재접속 #91(C) · **예약 `fc27-patch-watch` 매일 10:30 재생성(iMac) · 월요일 3선 역할 커뮤니티 체감** · TU v1.2.0(11월 중순) 대기 | `game.html` 시스템 분석 · `reports/patch-watch/` |
| 연구 | 11-04: [세트피스](reports/research/2026-11-04-avl-set-pieces.md)(맥피→팔 피엘데 · §9 반영) · [탄스웰 정리](reports/research/2026-11-04-tanswell-roundup.md) · 스타 퍼포머 기준 조사(대화만) | `reports/research/` |
| 이적 감시 | 11-26 AVL만 · 기준 창 2027년 1월 · **가르나초 1월 이탈 MEDIUM-HIGH**(`transfer_outgoing` #81 · 첫 `2027-winter` 행 · Romano 사우디 문의 + Tanswell 「bleak」 · 리콜·일방 해지 조항 없음 → 합의 해지만) · ⚠️ `core/export.py`가 `2026-summer`만 내보내 **이적 화면 미노출** · 디알로·포르브스·바에나·에이브러햄 3티어 · 에메리 재계약 미서명(맨유 건은 11-18 소멸) | `reports/transfer-watch/2026-11-26.md` |
| FUT 구단 | 11-25 전체 싱크(`4217a5e` · 보유 208장) · FC Pro Live 공개 8장 DB 반영(11-24 · 리포트 이번 커밋) · **11-26 migration 140** — 진화 보상 `alternative_positions`(포지션 추가 · Switchback Dynamo 2692 훈련 캠프형) 수용: `current_positions`·`positions_after` · 싱크가 EA 포지션 저장 — **11-26 저녁 싱크(`66d8c5d`)에서 보유 213/215장 채워짐 → 키 가정 확정** · 진화 내역은 아래 원장 블록 | `fut_*` · migration 140 · [FC Pro Live](reports/research/2026-11-24-fc-pro-live-cards.md) |
| 선수 상태 | 지모알로바 **훈련 중 어깨 부상(9월 초 · 복귀 미상)** — FotMob은 유스 부상 미추적(부재 증거로 쓰지 말 것) | `player_status` #1434 |
| 열린 결손 | 페네르바흐체 WS JSON 미보존 · offside(SS 미제공) · `matches.event_id` FotMob id 3경기 · FC25 커널 파일 404(game.html 무해) · 시세 fut.gg Cloudflare 차단 · 첼시 유튜브 자막 429 | `gaps.py links` |

<!-- evo-ledger:start -->
**진화 원장 (자동 · 최근 14일 + 진행 중 · 정본 DB `fut_evolution_log` · `ship.py`가 갱신)**

- 2026-11-27 · Cash ← Tempest Strike 5단계 · OVR 82→85 · 완료 2026-11-27
- 2026-11-27 · Cash ← Static Surge 5단계 · OVR 81→82 · 완료 2026-11-27
- 2026-11-25 · 가르나초 ← Slick Operator 3단계 · OVR 81→83 · 진행 중
- 2026-11-24 · 가르나초 ← Forked Lightning 4단계 · OVR 77→81 · 완료 2026-11-25
- 2026-11-24 · 맥긴 ← Cutting Edge 5단계 · OVR 83→87 · 완료 2026-11-24
- 2026-11-23 · 오나나 ← Lightning Rod 4단계 · OVR 81→84 · 진행 중
- 2026-11-22 · Cissé ← CB Roles++ 1단계 · OVR 86→86 · 완료 2026-11-22
- 2026-11-22 · Cissé ← Storm Wall 4단계 · OVR 80→86 · 완료 2026-11-22
- 2026-11-22 · Madjo ← ST Roles++ 1단계 · OVR 84→84 · 완료 2026-11-22
- 2026-11-22 · 바클리 ← CDM Roles++ 1단계 · OVR 85→85 · 완료 2026-11-22
- 2026-11-22 · 바클리 ← Full Overload 5단계 · OVR 83→85 · 완료 2026-11-22
- 2026-11-22 · 바클리 ← High Voltage 3단계 · OVR 82→83 · 완료 2026-11-22
- 2026-11-21 · Alysson ← Circuit Breaker 4단계 · OVR 83→86 · 완료 2026-11-21
- 2026-11-21 · 바클리 ← Static Charge 4단계 · OVR 77→82 · 완료 2026-11-21
- 2026-11-20 · John McGinn ← Glue or Genius [SP 28] 1단계 · OVR 84→84 · 완료 2026-11-20
- 2026-11-20 · Madjo ← Top Tier Striker 5단계 · OVR 81→84 · 완료 2026-11-20
- 2026-11-18 · Suzuki ← Feline Flex 2단계 · OVR 80→83 · 완료 2026-11-18
- 2026-11-17 · Alysson ← RM Roles++ 1단계 · OVR 83→83 · 완료 2026-11-17
- 2026-11-17 · Maatsen ← LB Roles++ 1단계 · OVR 83→83 · 완료 2026-11-17
- 2026-11-17 · 린델뢰프 ← Backline Bastion 4단계 · OVR 82→83 · 완료 2026-11-17
- 2026-11-17 · Alysson ← Right-Hand Drive 4단계 · OVR 80→83 · 완료 2026-11-17
- 2026-11-17 · Maatsen ← Streets Won't Forget 3단계 · OVR 79→83 · 완료 2026-11-17
- 2026-11-17 · Madjo ← Striker School 5단계 · OVR 65→81 · 완료 2026-11-17
<!-- evo-ledger:end -->

**분량**: 이 문서 약 17.7KB(목표 10~15 · 상한 20) — 11-26 밤 갱신(완료 1건 제거 · 세션 기록 5개 유지 · 초과분은 자동 진화 원장 블록).

## 진행 중 작업 (WIP)

없음. (11-24 Codex FC Pro Live의 「ship 승인 대기」는 해소 — DB 변경은 `2682e06` 덤프에 실렸고, 리포트·HANDOFF는 이 핸드오프 커밋에 실었다. `.claude/tmp_*` 3개는 다른 세션 임시 파일이라 커밋하지 않고 둔다.)

## 다음 할 일

번호는 v1 체계(경위 원문 [handoff-context 「다음 할 일」](docs/handoff-context.md#다음-할-일)).

**P1**
- [x] **갈라타사라이전 D+3 → complete**(`d904279`) — 구현 함의 2건(강팀 원정 라인 하강 프리셋 · RB 로테이션 하우드-벨리스 잔류형) **둘 다 미채택**(사용자 결정 11-28 · obs #1178)
- [ ] **스위치백 다이너모(2692 · 12-05 마감)** — 보유 EFL 중 조건 충족 0(카보레 OVR 75). 시장 후보 1순위 뭄바(LB · WF5 · 민첩 90·균형 91) · 2순위 케인 윌슨(RB · 가속 86 · Block 획득) — 구매·적용은 사용자 판단 · 시세 미확인
- [ ] **진화 완주 처리 2건** — 오나나 Lightning Rod · 가르나초 Slick Operator(11-26 싱크가 완주 추정 · `fut_club.py complete` 미처리)
- [ ] **가르나초 감시** — 1월 합의 해지·사우디 구단명 보도 시 HIGH 판정 · 10-31 풀럼전 출전 분 DB 9 ↔ Goal 3 SofaScore 재확인
- [ ] **FC27 슬롯 정본 보류 5건 + 3선 조합** — RDM(obs#1080 딥라잉 빌드업 인게임 테스트 대기 · 볼 지표: 키패스·역습 허용)·ST 포커스·LM·LB·lead · 바르사전 포함 표로 재판정(정본은 사용자 판단)
- [ ] **헤밍스 Zoomaestro(2602) 단계 완료** — 사용자 보고 시 `fut_club.py evolve/complete`(갈림길은 `--pick`) · 다음 싱크에서 지모알로바 약발 4→3·체력, **시세 빛나는 가드(로그만 기록 · 약발 3)·알리송 Marksman(Game Changer·개인기 +1★)** 실측 대조
- [ ] **★ FC27 라인 슬라이더 상하한 실측**(30분 · 플레이 불필요) → `core/team_settings.py` 구간 재정렬 · [검토](reports/research/2026-10-22-fc27-system-gap-review.md) §5
- [ ] **★ FC27 첫 인게임 캡처(T6·T7)** — 코드 `7ZTFKBu$37p7` 비조작 3경기 → `ingame_captures` FC27 ≥3 · 대조군 `xYJb3Bj37tdy`
- [ ] **세트피스 메뉴 「인원 추가·제거」 동작 실측** — 커뮤니티에도 설명 없음 · 코너 몇 번으로 확인 → `game_system_changes` C행(#83 미확인 목록)
- [ ] **cron FotMob 부분/0바이트 원인** — 팀별 종료코드·예외 기록 + 실패 팀 재시도 구조
- [ ] **000⑷⑸ FC27 고압박·라인** · **000⑹ 10월 중순 리서치 재조사** · **0 인게임 A/B T6 캐시 falseback** · **0-5 빌드업 축 괴리** · **0-3b 부상 축** · **4 obs#449** · **5 미결 이적 4건** · **20 풀백 비대칭(obs#768)** · **29 LIV 6번 축** — 각 원문은 handoff-context

**P2**
- [ ] **빌라 밖 보유 카드 진화 경로 갱신 멈춤** — 필요하면 `--club-ea`(값 없이)
- [ ] **예약 미복원 2건** — `transfer-watch-daily`·`futgg-prices-daily` 재생성 판단(`fc27-patch-watch`는 11-04 iMac 재생성)
- [ ] **시세 수집 복구** — fut.gg 가격 API Cloudflare 차단 · FUTWIZ 선수 페이지 대체
- [ ] **0-3c 재검증 이월 5건(obs#792)** · **0-4 선수 축 517행** · **6 아틀레틱 5-4-1** · **6-1 G13 확장** · `measured:season*` 48건 sample_n · **8 obs#353** · **9 경기 전용 처방 재판정** · **30 ATM 백3/백4**
- [ ] **15 claims 미작성·PENDING** · **전사 3편 match_videos 미등재**(`U4OewDAQMCk`·`QkA0fScs5s8`·`ofp0s7RaNoc`) · **PlayStyle 별칭(121) 화면 확인** · **카드 스텁 AcceleRATE·PlayStyle 채움(COALESCE)**
- [ ] **UI 남은 것** — 얼티밋팀 화면(탭 구조라 미개편) · 경기 분석 리포트 12k px(결론 카드 아래 상세 더 압축 여지) · `--acc` 라이트 대비 4.7:1 · 표 숫자 열 `.num`

**P3 · 판단 대기**
- [ ] **이적 화면 겨울 창 노출** — `core/export.py export_all(window='2026-summer')` 고정 → `2027-winter` 행(가르나초 #81)이 화면에 안 뜬다 · 창 선택/병합 방식은 사용자 판단
- [ ] **LIV·ATM 보류 해제 시** — #53·#54·#58~#61 D+N
- [ ] CHE 쟁점 #42·#65·#67·#69·#70(판정할 차례 아님) · 0-3d AVL 소스 2건 · 역할 숙련도 시각화 · 병렬 중복 실행 가드 · LIV LAM/RAM 슬롯
- [ ] 진화 예약 두 예약 충돌 경고 미검증 · 레어도 150 판 카드 값 그리기 · ATM 포메이션 표기 충돌

## 주요 결정 (전문 [docs/decisions.md](docs/decisions.md))

- 11-26 진화 포지션 보상은 B안(현재 포지션 칸 · 싱크 주 경로 · 사용자 선택) · 겨울 이적 행은 `window='2027-winter'`로 추가(화면 노출은 미결)
- 11-04 **불변규칙 14(가독성)** 신설 · CHE 1회성 수집·정본 반영(4-2-3-1 · 정기 수집 안 함) · 정본 포메이션 단일화(G24 ⑸ · migration 131) · 3선 선발은 자동 산출에 맡김 · 주앙 페드루(부상)는 선발 처방 유지
- 11-04 게임 시스템 `title` 칸(migration 130 · G23) · 예약 `fc27-patch-watch`(iMac) · 3선 역할 조합 상시 검토(메모리 `dm-role-pairing-ongoing-review`)
- 10-22 FC27 시즌 정본 = `kind='optimal'`(#46) · opt 선발은 정본 역할·가용 인원(G8+) · 영상 전사는 항상 뮤트
- 10-20 하위 세션 커밋 금지 · 부모가 모아서 ship · 진화 조건 판정은 fut.gg 유지 · 영상 전사 즉시 전 편 요약(G17)
- 10-19 이전 → [docs/decisions.md](docs/decisions.md)

## 최근 세션 기록

- **11-26 밤 · 부모 세션(대화 · `AL02359162`)** — 스위치백 다이너모 EFL 후보 검토(fut.gg EFL 1,955장 → 조건 충족 235 → 완주 투영 상위 4 · DB 변경 0 · 대화만) · iMac 저녁 싱크로 migration 140 포지션 키 확정
- **11-26 · 부모 세션(대화 · `AL02359162`)**(`2682e06`) — 갈라타사라이전 리포트 브리핑 · D+2 수동 보강(영상 3편 · 주장 12 · 밍스 1차) · 이적 감시(가르나초 MEDIUM-HIGH · 서브에이전트 스캔) · **G29 해소 B안**(migration 140 · evolve/complete/remove·싱크·export·라벨 · 임시 DB 검증) · FC Pro Live WIP 마무리
- **11-24 · Codex · FC Pro Live 카드 수집** — FC Pro Open 연계 공개 카드 8장 EA item ID·세부값 반영 · 유출 후보 16명은 미공개/C로만 보고 · Alysson이 AVL 선수임을 기본 카드 82968과 현행 스쿼드에서 확인 · 비공식 콘셉트는 86 RM, 발매 11-30~12-11 추정(정확한 날짜·이벤트 ID 미확인) · [리포트](reports/research/2026-11-24-fc-pro-live-cards.md)
- **11-17 · 스케줄 match-watch-weekly** — 새 경기 없음 · FotMob 선수 상태 AVL 갱신 · 채널 스윕 10편 전사(브라우저 json3 · 뮤트 · 클립보드는 `execCommand('copy')` 버튼 실제 클릭 → `pbpaste` — 비ASCII 바이트 손상 주의) · 요약·주장 44행(서브에이전트 3) · T1·duty 변경 0
- **11-04~05 · 부모 세션(대화 · iMac) + 첼시 하위 세션 + 서브에이전트**(`16b86d3`~`eff029c` 약 40커밋) — 클럽 싱크 [선수+sbc] · 호커스포커스 SBC · 스타 퍼포머 조사 · **바르셀로나전 관전 메모 실시간 기록 → 수집 루틴 4회차 예약** · 세트피스 코치 교체 리서치(§9 반영 · 18골=PL 정정) · FC27 코너·D-pad·Avoidance #79~84 · 3선 카마라·고메스 히트맵+스탯 검토 → 처방 기록 · **사이트 UI/UX 전면 개편** · 게임 시스템 한 줄 제목 90행 · CHE 4경기·정본 4-2-3-1·is_canon 단일화 · 이적 감시(에메리-맨유) · 탄스웰 정리(바르사 프리뷰 전사) · 지모알로바 진화 교체·부상 확인 · 시세 WIP 커밋
- 아카이브: 11-05 AL02359162 시세 빛나는 가드 검토(→`eff029c`) · 11-02 SBC GK 규칙·진화 예약 화면(migration 128)·dump 형식 고정(`671ed8c`~) · 10-29 본머스전 수집·Jauregizar 빈 카드 상세 API 보충 · 10-28 AVL 시즌 검토·선발 자동 산출·G42 번역 2,900건(`a2b2664`~) · 10-22 FC27 구현 검토·optimal #46·migration 116~121 · 10-20 진화 수집 병렬·하위 세션 커밋 규칙 · 10-19 주간 match-watch(#57~#61) · 10-17 이적 감시·페네르바흐체 D+3 · 10-14 이전 → [handoff-context](docs/handoff-context.md#최근-작업) · `git log`

## 문서 맵

- 고정 작업 규칙 · 핵심 방법론 · 데이터 수집 결손 · 참고 문서 원문 → [docs/handoff-context.md](docs/handoff-context.md)
- 런북 `.claude/skills/{transfer-watch,match-watch,player-collect,club-sync}/SKILL.md` · DB/export/git docs/40 · 수집 docs/30 · 메커니즘 docs/22 · 인게임 docs/50
- 기록 공백 주의: 다른 세션이 코드만 push하고 HANDOFF를 안 고친 전례가 세 번(09-23 · 10-14 · 10-30~11-01) — 착수 시 `git log`를 정본으로
