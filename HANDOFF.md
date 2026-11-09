# HANDOFF — tactics

<!-- 구조 규칙(2026-10-14 v2): 헤더 15줄 안에 착수 조건 · 현재 상태 표 10행 이내 · 다음 할 일은 열린 항목만(항목당 2줄) · 세션 기록 최대 5개 · 목표 10~15KB · 상한 20KB(`wc -c`). 넘치면 지우지 말고 docs/handoff-context.md · docs/decisions.md로 포인터 압축. 절차 정본: .claude/skills/handoff/SKILL.md -->

- **담당자** 김호근 · **갱신** 2026-11-09 · **세션** 스케줄 match-watch-weekly(11-09) · **작업 PC** `AD03230205ui-iMac.local` · **브랜치** main · **WIP** 없음
- **마지막 커밋** = `git log -1`(이 문서를 갱신한 커밋) · 직전 `eff029c` · **문서 버전** v2 · **분량** 아래 「분량」 줄
- 실축 감독 전술(**AVL/에메리(주) · CHE/알론소 · LIV/이라올라 · ATM/시메오네**)을 실측으로 분해해 FC26·FC27 전술로 재현. 규약 정본 `CLAUDE.md`(불변규칙 1~14) · `docs/00-overview.md`.

> ⛔ **먼저 알 것**
> 1. **명시 스테이징만**(`git add -A` 금지) · DB 변경은 `python3 scripts/ship.py -m "…"` 한 줄 · **하위 세션은 커밋 안 함 — 부모가 `ship.py --collect <id>` 등록 후 모아서 ship · 끝나면 `--collect-end`** · migration 번호는 부모가 배정(최신 **131**)
> 2. git엔 `.db`가 없다 — pull 뒤 `scripts/db_restore.sh` · 반복 사고 규칙 정본 [docs/70-lessons.md](docs/70-lessons.md) · **정기 수집은 AVL만** — CHE는 11-04 **1회성** 수집·정본 반영만(정기 수집 안 함) · LIV·ATM 보류(메모리 `che-atm-liv-collection-hold`)
> 3. 예약은 **PC마다 따로**(`list_scheduled_tasks`로 실재 확인 · 같은 작업 트리 → 스케줄 세션 중엔 커밋 보류) · ⭐ **새 불변규칙 14: 답변·리포트·화면은 결론 먼저 · 표/목록 · 인용 번역/원문 분리**(11-04)
> 4. yt-dlp는 봇 차단 → 브라우저 fetch/XHR 훅으로 `/api/timedtext` 응답 본문 포착 → COPY 버튼 실제 클릭 → `yt_transcript_json3.py VIDEO en /tmp/x.json3`(항상 뮤트)

---

## 현재 상태

| 영역 | 상태 | 정본 |
|---|---|---|
| 게이트 | 전항 통과(11-05) · 11-04 추가: **G24 ⑸**(정본 표시 포메이션 `slots.is_canon` = 현행 optimal 포메이션) · **G23 `game_system_changes.title` 결손 0** · G12 메뉴 3칸 형식 · G37·G8+ 범위 **AVL·CHE** | `gates.py` |
| 경기 수집 | AVL **맨유 원정 4-4(PL 10R 11-08 · matches #134 · 리포트 #70 draft)** 수집·D+1 완료(16명 · xG 2.88/3.55 · PPDA 13.5/9.21 · 수비 액션 평균 높이 31.2 · obs#1159 리드 막판 실점 · #1160 남는 RB) + 채널 스윕 2편 · **D+2(11-10 20:00)·D+3(11-11 20:00) 예약 실재(iMac · 11-09 대화 세션 등록)** | `reports/match-watch/2026-11-08-avl-manchester-united.md` |
| 전술 정본 | AVL: optimal #46(4-2-3-1 Wide · Balanced/Balanced/52) · **3선 = RDM 홀딩/수비 · LDM 딥라잉/로밍 유지 + 계속 검토**(근거 `measured:pair:gomes/kamara` #1023·#1024 · 히트맵+경기 스탯) · 선발은 자동 산출(현재 LDM 고레츠카·RDM 고메스 — 사용자 「자동에 맡긴다」) · CHE: **optimal 신설 4-2-3-1 Wide · Balanced/Balanced/52**(LDM 딥라잉/빌드업 · 감시 쟁점 #91 = 다음 PL 3경기 3-4-2-1 복귀 시 재판단 · 수동 수집 때만) | `team_tactic_setups` · `slot_canon_roles` · [CHE 검토](reports/research/2026-11-04-che-season-review.md) |
| 사이트 UI | **11-04 전면 개편**(불변규칙 14): 메뉴 흐름 순서 · 「리포트」→「팀 전술」 · 허브=팀 대시보드 · 경기 분석 결론 카드 · 긴 패널 접기 · 팀 전술 39k→6.9k px · 게임 시스템 숫자 타일·영역 카드·**한 줄 제목**(migration 130)·인용 번역/원문 분리 · 이적 숫자 타일 · 스쿼드 표 접기 · 공용 부품 `data.js`(`matchScore`·`foldLong`·`mountPanelToc`)·`style.css` `ux-*` | `site/*.html` · `assets/data.js` |
| 게임 시스템 | `game_system_changes` 91행(전 행 `title`) · 11-04 코너·세트피스 #79~84 · 진화 포지션 조건은 보조 포지션 인정·제거 직후 재접속 #91(C) · **예약 `fc27-patch-watch` 매일 10:30 재생성(iMac) · 월요일 3선 역할 커뮤니티 체감** · TU v1.2.0(11월 중순) 대기 | `game.html` 시스템 분석 · `reports/patch-watch/` |
| 연구 | 11-04: [세트피스](reports/research/2026-11-04-avl-set-pieces.md)(맥피→팔 피엘데 · §9 반영) · [탄스웰 정리](reports/research/2026-11-04-tanswell-roundup.md) · 스타 퍼포머 기준 조사(대화만) | `reports/research/` |
| 이적 감시 | 11-04 AVL만 · DB 변경 0 · **에메리 → 맨유 관심(1티어 · 접촉 0 · 11-08 맨유전 전후 확인)** · 누사·비베로스 MEDIUM 유지 · 1월 GK 수요(스즈키 아시안컵) | `reports/transfer-watch/2026-11-04.md` |
| FUT 구단 | 클럽 싱크 매일 10:00·21:00(iMac) · **진화 내역은 아래 「진화 원장」 블록(DB 자동 생성)** · 갤러리 브라이턴 B·토트넘 C · 호커스포커스 SBC 4-4-2(RS·LS 막힘) 해법 | `fut_*` · club-sync 런북 |
| 선수 상태 | 지모알로바 **훈련 중 어깨 부상(9월 초 · 복귀 미상)** — FotMob은 유스 부상 미추적(부재 증거로 쓰지 말 것) | `player_status` #1434 |
| 열린 결손 | 페네르바흐체 WS JSON 미보존 · offside(SS 미제공) · `matches.event_id` FotMob id 3경기 · FC25 커널 파일 404(game.html 무해) · 시세 fut.gg Cloudflare 차단 · 첼시 유튜브 자막 429 | `gaps.py links` |

<!-- evo-ledger:start -->
**진화 원장 (자동 · 최근 14일 + 진행 중 · 정본 DB `fut_evolution_log` · `ship.py`가 갱신)**

- 2026-11-08 · Cissé ← CB Roles++ 1단계 · OVR 84→84 · 완료 2026-11-08
- 2026-11-07 · Cissé ← Pamplona Grit [SP 16] 3단계 · OVR 80→84 · 완료 2026-11-07
- 2026-11-07 · Alysson ← Matchday Marksman 4단계 · OVR 80→83 · 완료 2026-11-07
- 2026-11-06 · 오나나 ← Strings of Fate 3단계 · OVR 81→82 · 완료 2026-11-06
- 2026-11-06 · Hemmings ← Strings of Fate 3단계 · OVR 81→82 · 완료 2026-11-06
- 2026-11-05 · Cissé ← Glow Guard 4단계 · OVR 73→80 · 완료 2026-11-07
- 2026-11-04 · Jamaldeen Jimoh-Aloba ← Channel Surfer [SP 11] 3단계 · OVR 80→83 · 완료 2026-11-05
- 2026-11-03 · 루제리 ← The Haunted Wall 4단계 · OVR 81→84 · 완료 2026-11-03
- 2026-11-03 · Richard Kone ← Two Faces of Fear 3단계 · OVR 80→81 · 완료 2026-11-03
- 2026-11-03 · Elia Caprile ← No Soul Shall Pass 2단계 · OVR 80→81 · 완료 2026-11-04
- 2026-11-02 · 하우드-벨리스 ← CB Roles++ 1단계 · OVR 83→83 · 완료 2026-11-02
- 2026-11-02 · Pau Torres ← CB Roles++ 1단계 · OVR 85→85 · 완료 2026-11-02
- 2026-11-02 · Cash ← RB Roles++ 1단계 · OVR 83→83 · 완료 2026-11-02
- 2026-11-01 · Mbaye ← RM Roles++ 1단계 · OVR 85→85 · 완료 2026-11-01
- 2026-11-01 · Mbaye ← LM Roles++ 1단계 · OVR 85→85 · 완료 2026-11-01
- 2026-11-01 · 맥긴 ← RM Roles++ 1단계 · OVR 83→83 · 완료 2026-11-01
- 2026-11-01 · 맥긴 ← LM Roles++ 1단계 · OVR 83→83 · 완료 2026-11-01
- 2026-11-01 · 루제리 ← LB Roles++ 1단계 · OVR 81→81 · 완료 2026-11-01
- 2026-11-01 · Pau Torres ← Luiz Legacy 3단계 · OVR 82→85 · 완료 2026-11-01
- 2026-10-31 · 부엔디아 ← False Seven 3단계 · OVR 80→81 · 완료 2026-10-31
- 2026-10-30 · Mbaye ← Wicked Winger 5단계 · OVR 76→85 · 완료 2026-10-31
- 2026-10-28 · Pau Torres ← Bone Builder 3단계 · OVR 81→82 · 완료 2026-10-30
- 2026-10-27 · Alysson ← Rise From the Grave 5단계 · OVR 70→80 · 완료 2026-10-29
- 2026-10-26 · Jamaldeen Jimoh-Aloba ← Witching Hour 3단계 · OVR 80→81 · 제거 2026-11-04
<!-- evo-ledger:end -->

**분량**: 이 문서 약 12.8KB(목표 10~15 · 상한 20) — 11-05 압축(19.98KB에서)(완료 항목 제거 · 세션 기록 병합).

## 진행 중 작업 (WIP)

없음. (11-05 `AL02359162` WIP였던 시세 진화 기록은 iMac 로컬 DB에 있어 `eff029c`로 커밋 — 다른 PC에서 다시 적지 않는다.)

## 다음 할 일

번호는 v1 체계(경위 원문 [handoff-context 「다음 할 일」](docs/handoff-context.md#다음-할-일)).

**P1**
- [ ] **바르셀로나전 D+2·D+3** — 예약이 돈다(iMac). D+3이 R4-H(야말 대응 · 탄스웰 경기 전 예상 + 감독 1차 발언 여부)·H2·만잠비 R1 최종 판정 + 구현 함의 「사용자 판단 대기」로 올린다(단 「상대에 따라 높은 DM 바꾸기」는 11-05 사용자 보류 — 올리지 않음)
- [ ] **에메리 → 맨유 감시** — 11-08 빌라–맨유전 전후 접촉 보도 확인(다음 이적 감시 회차 1순위) · 떠나면 체제(regime) 자체가 바뀐다
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
- [ ] **LIV·ATM 보류 해제 시** — #53·#54·#58~#61 D+N · 이적 판단(런북 `2026-summer` 고정값 → 1월 창이면 `core/export.py` window 인자)
- [ ] CHE 쟁점 #42·#65·#67·#69·#70(판정할 차례 아님) · 0-3d AVL 소스 2건 · 역할 숙련도 시각화 · 병렬 중복 실행 가드 · LIV LAM/RAM 슬롯
- [ ] 진화 예약 두 예약 충돌 경고 미검증 · 레어도 150 판 카드 값 그리기 · ATM 포메이션 표기 충돌

## 주요 결정 (전문 [docs/decisions.md](docs/decisions.md))

- 11-04 **불변규칙 14(가독성)** 신설 · CHE 1회성 수집·정본 반영(4-2-3-1 · 정기 수집 안 함) · 정본 포메이션 단일화(G24 ⑸ · migration 131) · 3선 선발은 자동 산출에 맡김 · 주앙 페드루(부상)는 선발 처방 유지
- 11-04 게임 시스템 `title` 칸(migration 130 · G23) · 예약 `fc27-patch-watch`(iMac) · 3선 역할 조합 상시 검토(메모리 `dm-role-pairing-ongoing-review`)
- 10-22 FC27 시즌 정본 = `kind='optimal'`(#46) · opt 선발은 정본 역할·가용 인원(G8+) · 영상 전사는 항상 뮤트
- 10-20 하위 세션 커밋 금지 · 부모가 모아서 ship · 진화 조건 판정은 fut.gg 유지 · 영상 전사 즉시 전 편 요약(G17)
- 10-19 이전 → [docs/decisions.md](docs/decisions.md)

## 최근 세션 기록

- **11-04~05 · 부모 세션(대화 · iMac) + 첼시 하위 세션 + 서브에이전트**(`16b86d3`~`eff029c` 약 40커밋) — 클럽 싱크 [선수+sbc] · 호커스포커스 SBC · 스타 퍼포머 조사 · **바르셀로나전 관전 메모 실시간 기록 → 수집 루틴 4회차 예약** · 세트피스 코치 교체 리서치(§9 반영 · 18골=PL 정정) · FC27 코너·D-pad·Avoidance #79~84 · 3선 카마라·고메스 히트맵+스탯 검토 → 처방 기록 · **사이트 UI/UX 전면 개편** · 게임 시스템 한 줄 제목 90행 · CHE 4경기·정본 4-2-3-1·is_canon 단일화 · 이적 감시(에메리-맨유) · 탄스웰 정리(바르사 프리뷰 전사) · 지모알로바 진화 교체·부상 확인 · 시세 WIP 커밋
- **11-05 · 부모 세션(대화 · `AL02359162`)** — 시세 빛나는 가드 검토(29속성 비교 → 마지막 제거 추천) · 원장 기록은 로컬만(→ iMac `eff029c`로 커밋)
- **11-02 · 부모 세션(대화)**(`671ed8c`~`05fb707`) — 클럽 싱크 [선수+sbc] · Pumpkin Seeds 포메이션 · SBC GK 규칙 버그 수정 · 진화 예약 화면(migration 128) · **dump 형식 고정**(`db_dump_sql.py`)
- **10-29 · 부모 세션 + 스케줄**(`2e762d1`~`893283b`) — 본머스전 관전 메모·수집 · 히트맵 5×5 칸+비중 % · Jauregizar 빈 카드 → 수집기 상세 API 보충
- 아카이브: 10-28 AVL 시즌 검토·선발 자동 산출·G42 번역 2,900건(`a2b2664`~) · 10-22 FC27 구현 검토·optimal #46·migration 116~121 · 10-20 진화 수집 병렬·하위 세션 커밋 규칙 · 10-19 주간 match-watch(#57~#61) · 10-17 이적 감시·페네르바흐체 D+3 · 10-14 이전 → [handoff-context](docs/handoff-context.md#최근-작업) · `git log`

## 문서 맵

- 고정 작업 규칙 · 핵심 방법론 · 데이터 수집 결손 · 참고 문서 원문 → [docs/handoff-context.md](docs/handoff-context.md)
- 런북 `.claude/skills/{transfer-watch,match-watch,player-collect,club-sync}/SKILL.md` · DB/export/git docs/40 · 수집 docs/30 · 메커니즘 docs/22 · 인게임 docs/50
- 기록 공백 주의: 다른 세션이 코드만 push하고 HANDOFF를 안 고친 전례가 세 번(09-23 · 10-14 · 10-30~11-01) — 착수 시 `git log`를 정본으로
