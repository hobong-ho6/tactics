# HANDOFF — tactics

<!-- 구조 규칙(2026-10-14 v2): 헤더 15줄 안에 착수 조건 · 현재 상태 표 10행 이내 · 다음 할 일은 열린 항목만(항목당 2줄) · 세션 기록 최대 5개 · 목표 10~15KB · 상한 20KB(`wc -c`). 넘치면 지우지 말고 docs/handoff-context.md · docs/decisions.md로 포인터 압축. 절차 정본: .claude/skills/handoff/SKILL.md -->

- **담당자** 김호근 · **갱신** 2026-10-28(주간 매치워치) · **세션** 부모 세션(대화) + 서브에이전트·하위 세션 다수 — 바이킹전 D+1 · FC27 구현 검토·반영 · 경기 데이터 확장 · 디자인 개편(글래스·라이트) · **작업 PC** `AL02359162.local`(⚠️ iMac이 아님 — 예약은 PC별) · **브랜치** main · **WIP** 없음
- **마지막 커밋** = `git log -1`(이 문서를 갱신한 커밋) · 직전 `0d58a93` · **문서 버전** v2 · **분량** 15KB(목표 10~15 · 상한 20)
- 실축 감독 전술(**AVL/에메리(주) · CHE/알론소 · LIV/이라올라 · ATM/시메오네**)을 실측으로 분해해 FC26·FC27 전술로 재현. 규약 정본 `CLAUDE.md` · `docs/00-overview.md`.

> ⛔ **먼저 알 것**
> 1. **명시 스테이징만**(`git add -A` 금지 · `.claude/settings.json` PAT) · DB 변경은 `python3 scripts/ship.py -m "…"` 한 줄 · ⭐ **하위 세션은 커밋하지 않는다 — 부모가 `ship.py --collect <세션 id>`로 등록하고 모아서 ship**(CLAUDE.md 불변규칙 5 · 10-20) · migration 번호는 부모가 배정
> 2. git엔 `.db`가 없다 — pull 뒤 **`scripts/db_restore.sh`** · **반복 사고 규칙 정본은 [docs/70-lessons.md](docs/70-lessons.md)** · ⭐ **CHE·LIV·ATM 수집·업데이트 잠정 보류 — AVL만**(10-20 사용자 · 메모리 `che-atm-liv-collection-hold`)
> 3. 예약 정본은 `list_scheduled_tasks` · **PC마다 따로** → 회차마다 실재 확인(10-20 뉴캐슬 D+3 · 10-22 바이킹 D+2·D+3이 리포트엔 「있다」였지만 이 PC엔 없었다 → `AL02359162`에 재생성 · ⚠️ iMac에도 있으면 **중복 실행**) · 스케줄 세션이 같은 작업 트리를 쓴다 → 끝날 때까지 커밋 보류
> 4. yt-dlp는 이 PC에서 봇 차단 → **브라우저 pot 경로 + fetch/XHR 훅**(`window.fetch`를 감싸 `/api/timedtext` URL을 잡는다 · 뮤트 · `yt_transcript_json3.py`) · 영어권 알리송 표기는 **Alysson**(obs#1116)

---

## 현재 상태

| 영역 | 상태 | 정본 |
|---|---|---|
| 게이트 | **전항 통과(10-22)** · 10-22 확장: G8+(opt 선발 ≠ 정본·장기 부상 · AVL) · G1/G3/G5 현행 버전 루프 · G22 비현행 `loadKernels` 리터럴 금지 · G37 ⑸ 보유/비보유 형태(migration 116) · G21 출시 후 카드 스냅샷 · G23 국면 분 결손(`core/phase_minutes.py`) — 문구는 docs/00 | `gates.py` |
| 수집 범위 | **AVL만** — CHE·LIV·ATM 잠정 보류(예약 `match-watch-weekly` AVL만 · G37 AVL만) · 10-19 주간 회차 5경기(#57~#61) 리포트는 draft로 보존 | 메모리 · 예약 프롬프트 |
| 경기 분석 화면 | 요약·흐름·가설 판정·부상·포지션 스탯·전술 4칸·목차 + **10-22: 보유 그리드 Δ 열·운반(SS 실측 vs WS 추정)·모멘텀 차트** · 디자인 `theme.css`(글래스 크롬·불투명 패널·라이트 스킴 · `tokens.js`) | `match-report.html` · `matchviz.js` · [UX 리뷰](reports/research/2026-10-22-site-ux-review.md) |
| 영상 | 전사하면 같은 회차에 **전 편 요약**(G17) · 월요일 **채널 스윕**(UTV·Villans·1874 분석 영상) · 자막 포착은 **항상 뮤트** · 분류 정본 `resolve_kind` · 뉴캐슬전 40/40 요약 · UTV 분석 6편 · **10-28 스윕**: 신규 분석 0 · 건너뜀 10(프리뷰 7·예측 1·브이로그 1·회고 인터뷰 1 e1Catd-Ea1s) · 기수집 10 · ⚠️ **Jacob Horsfall 채널 소실**(`@jacobhorsfall` 404 · 기수집 4편 재생 불가 · 새 핸들 미확인 — 예약 프롬프트 4채널 목록 정리 필요) | `index_transcripts.py` · 예약 프롬프트|
| 경기 수집 | **10-28 주간 회차: AVL 새 경기 없음** — 최근 맨시티 10-24(#127 · 보고서 #63 complete) · 다음 본머스(EFL컵 10-28 19:45 UTC · SS 17118370 · 이번 회차 시점 notstarted) → 풀럼(10-31) → 바르사(UCL 11-03) · 판정 쟁점 10-28: AVL 판정할 차례 0(남은 12건 전부 보류 팀) · 10-26 #14·#30 감시 · #7 연장 · ⚠️ headless Playwright는 SofaScore 403 challenge → 브라우저 패널로 라운드 확인 | `reports/match-watch/` · `claim_issues.py --due` |
| FUT 구단 | 10-20 싱크 217장 · 진화 수집 병렬(WORKERS=6) · Excluded Rarity 실판정 · 진화·SBC 세트 **숨김** · 카드 포지션 이력(110 · 맥긴·퀜다·소보슬라이) · 케미 신호 증분(클럽 싱크 22분→5분) · **진행 중 헤밍스 Zoomaestro lv1(10-20)** · SBC 101 완료 기록(카드 미반영) | `fut_*` · club-sync 런북 |
| 전술 판단 | **FC27 시즌 정본 `optimal` #46 신설**(Balanced/Balanced/52 · 코드 7ZTFKBu$37p7) · opt:* 선발 11칸 정본 역할로 재지정(obs#1120 · 옛 GK/ST 행 `-deprecated`) · 사용자 판단 대기 5건(RDM obs#1080 · ST 포커스 3층 · LM 포커스/역할 · LB 저점유 운용 · FC27 `optimal:lead`) — 정본 [리서치](reports/research/2026-10-22-fc27-avl-implementation-review.md) §1.6 ㉡ | `team_tactic_setups` · `observations` |
| 이적 감시 | 10-17 21시 임시 클론 `3e2790b`는 **/tmp 소실·미푸시** — 원 작업트리 리포트 10-14~17 4건은 10-20 커밋에 실음 · CHE·LIV 이적 판단은 보류 | `reports/transfer-watch/` |
| 경기 데이터 | 10-22 확장: SS 48필드(실측 운반 `carries_ss`·GK 스위핑) · FotMob 경기별 선수 스탯 · WS 수신 `recv_*` · 보유/비보유 fit(119) · `match_momentum`(120) · 세트피스(117) · Understat 26/27 — **경기마다 필수 3종(SS 확장·FotMob·WS JSON 저장)은 G21이 막는다** | [결손 검토](reports/research/2026-10-22-match-data-gap-review.md) · match-watch §2 |
| 열린 결손 | 페네르바흐체 WS JSON 미보존 · offside 이벤트(SS 미제공) · `matches.event_id` FotMob id 3경기(#86·94·95) · `--acc` 라이트 4.7:1 · 이적 총평 `##` 머리글 노출(DB 산문 · prose.js 미해석) · 표 숫자 열 `.num` 훅만(JS 렌더 표 미적용) · 링크 결손 3건 · `ref_map25` 동률 · ATM regime 4 CAM 슬롯 없음 · 미분류 영상 62편(보류 팀) | `gaps.py links` · 리서치 §2.2 |

## 진행 중 작업 (WIP)

코드 WIP 없음 · 하위 세션 0(10-22 p2-migration 세션 종료·부모가 ship · `--collect-end` 완료).

## 다음 할 일

번호는 v1 체계 그대로(근거·경위 원문은 [handoff-context 「다음 할 일」](docs/handoff-context.md#다음-할-일)).

**P1**
- [ ] **⭐ FC27 슬롯 정본 판단 5건 — 사용자 보류(10-22 「실측 더 확보 후 결정」 · obs 기록)** — RDM·ST 포커스·LM·LB 운용·리드 프리셋. **재판정: 다음 AVL 공식전 2경기(맨시티 10-24 포함) 프리셋이 쌓이면 같은 표를 다시 낸다**(리서치 §1.2 형식 · RDM은 카마라 인게임 결과 병기 · LM은 루헤리 복귀 병기). 그 전엔 정본·인게임 코드 어느 쪽도 바꾸지 않는다
- [ ] **바이킹전 D+2·D+3**(예약) — 전술 블로그·The Villans 후속·Sky 「best minutes」 원문·avfc.co.uk 인터뷰·Sports Mole 3백 표기·감독 직함·맨시티전(10-24 12:30 BST) 명단으로 고메스 RB·밍스 잔류 재확인 → D+3에 complete 판정
- [ ] **카마라 RDM Build-Up 인게임 테스트 결과 받기**(obs#1080) — 결과·다음 2경기 실측으로 정본 변경 여부(새 행) 결정
- [ ] **헤밍스 Zoomaestro(2602) 단계 완료 기록** — lv1 시작 10-20(사용자는 부엔디아 추천 대신 헤밍스) · 단계마다 `complete` · 완주 OVR 65→72 · 다음 싱크 EA 실측 대조
- [ ] **SBC 101 카드 반영 확인** — 10-20 「기록만」 완료(낸 11장 모름) · 다음 클럽 싱크가 소모 카드를 잡는지 · 그 전 다른 SBC 제출 시 카드 겹침 주의
- [ ] **cron FotMob 부분/0바이트 원인** — 10-12·10-17 09/21시 0바이트, 10-16 21시는 AVL 8건 뒤 종료·예외 미기록. 팀별 종료코드/예외 기록과 실패 팀 재시도 구조 필요
- [ ] **★ FC27 라인 슬라이더 상하한 메뉴 실측(30분 · 플레이 불필요)** — Deep에서 31, Balanced에서 61, High에서 91 입력 가능 여부 + 구간 경계에서 Run Tracking 문구 변화 스크린샷 4장 → `core/team_settings.py` 구간 30/60/90 재정렬(새 규칙 버전 · G15 rule_note) · [검토](reports/research/2026-10-22-fc27-system-gap-review.md) §5
- [ ] **★ FC27 첫 인게임 캡처(T6·T7 재개)** — 현재 코드 `7ZTFKBu$37p7`로 비조작 3경기 캡처(Competitive 명기) → `ingame_captures` FC27 ≥3 · `v_kernel_fidelity` FC27 ≥1 · 대조군 코드 `xYJb3Bj37tdy`(meta:futgg-2026-10-22)
- [ ] **000⑶ 지모알로바 Creative Crossroads 3단계** — 마감 09-30 17:00 UTC 경과 · 적용 여부 미확인 → `fut_evolution_log` 대조 · 적용됐으면 연관 메뉴(런북 표) 한 회차에 닫기
- [ ] **000⑷⑸ FC27 고압박·라인 높이** — Team Press 자기 수비 3분의 1 무효 · `core/team_settings.py` 구간이 EA 1–30/31–60 밖 → FC27 슬라이더 실측 선행 · 정정은 새 행
- [ ] **000⑹ 10월 중순 리서치 재조사** — C·B등급 수집(First Touch↔볼컨 · 역할/포커스 이동량 · 스탯 선형/계단 · 반응력 실체)
- [ ] **0 인게임 A/B T6 = 캐시 falseback 단일 변수** — 1차 판별 「캐시 그리드가 안쪽(열1~2)으로 가는가」 · ⛔ 시뮬 승점 비교 금지(obs#702)
- [ ] **0-5 빌드업 축 괴리** Short Passing ↔ Balanced(`8ZUKLGXm48ac`) · GK 역할 Δ13.9 — `slot_canon_roles` 변경 전 A/B
- [ ] **0-3b 부상 축** — 마첸·파우 토레스 구단 공식 발표 · premierinjuries 등 미조회 · 바리오스 2소스 충돌 · 스쿼드 밖 5명
- [ ] **4 obs#449 ⓐ/ⓑ** 양 풀백 att_wb 역전 — 점유 국면 버킷당 2경기 후 판정 · 그때까지 obs#443 정본 유지
- [ ] **5 미결 이적 4건 개별 처리** — 실효 시한 도래분부터
- [ ] **20 C2/C6 풀백 비대칭 재판정**(obs#768) — obs#443 vs obs#95가 처음 갈림 · 인게임 A/B(T7 후보) 없이는 못 닫음
- [ ] **29 LIV 6번 축**(obs#778) — 맥 알리스터 같은 `pos_class` 2경기 채우면 재산출 · 그 전엔 어느 쪽도 처방 금지

**P2**
- [ ] **SBC 포메이션 결손 #101** — Chrome FUTBIN 스니펫(club-sync 런북 §6) · **빌라 밖 보유 카드(예: 알리 아메드)는 진화 경로 갱신이 멈춤** — 필요하면 `--club-ea`(값 없이)
- [ ] **0-6 예약 미복원 3건 재생성 판단** — `transfer-watch-daily`·`futgg-prices-daily`·`fc27-patch-watch`(사용자) · 재생성해도 회차마다 실재 확인
- [ ] **00⑴ 시세 수집 복구** — fut.gg Cloudflare 차단(10-13~14 클럽 싱크 전 회차 미갱신)
- [ ] **0-3c 재검증 이월 5건**(obs#792) · **0-4 선수 축 517행 후처리** · **6 아틀레틱 5-4-1 전환 시각**(WhoScored 타임라인)
- [ ] **6-1 G13 확장 2건 사전등록** · `measured:season*` 처방 48건 sample_n 불일치 재산출(사용자 판단 대기)
- [ ] **8 obs#353 학포 RM** · **9 경기 전용 처방 재판정 파이프라인 편입** · **30 ATM 백3/백4 프리셋 병기**(obs#775)
- [ ] **15 claims 미작성 98편 · PENDING 23건**(09-20) — 회차마다 같은 경기 국면 그리드로 닫기
- [ ] **전사 3편 `match_videos` 미등재** — `U4OewDAQMCk` · `QkA0fScs5s8` · `ofp0s7RaNoc`(제외 권장 · 사유 기록) · G17 `impl_claims` 1행 필수
- [ ] **PlayStyle 별칭(121)** — 다음 클럽 싱크에서 옛 이름 저장값이 화면에 정본으로 보이는지 · `patch_watch_index.py` 미적재 6건 판단(패치 감시 회차)
- [ ] **000⑵ 잔여** — DB `game_system_changes` #25 `autonomyIQ` impact 문구(별도 DB 작업)

**P3 · 판단 대기**
- [ ] **보류 해제 시(CHE·LIV·ATM)** — #57~#61 D+N · LIV 맨시티 #53 · ATM 알라베스 #54 D+N · 이적 판단(Scott 창·N'Guessan·런북 `2026-summer` 고정값) · followups `2026-10-19-pending-schedules.md`는 보류로 미등록
- [ ] 0-3d AVL 소스 2건(Aston Villa Review · Read Aston Villa 403) · 00⑶⑸ 역할 숙련도 대조·시각화 후속 · 11 병렬 중복 실행 가드 · 33 LIV LAM/RAM 슬롯
- [ ] 미해결 1 **ATM 포메이션 표기 충돌**(4-4-2 기울음 · 감독 발언 0건) · 삭제 후보 `reports/match-watch/2026-09-19-avl-tottenham.D1-findings.md`(전량 흡수됨)

## 주요 결정 (전문 [docs/decisions.md](docs/decisions.md))

- 10-22 FC27 시즌 정본 = `team_tactic_setups kind='optimal'`(#46 · Balanced/Balanced/52) · opt 선발은 정본 역할·가용 인원으로(G8+가 막는다) · 예약은 PC별로 실재 확인 · 영상 전사는 항상 뮤트
- 10-20 하위 세션 커밋 금지 · 부모가 모아서 ship(`ship.py --collect`) · CHE·LIV·ATM 잠정 보류 · 뉴캐슬전 D+3 미실시 · 스즈키 롱볼 → 설정 유지(obs#1081)
- 10-20 영상: 전사 즉시 전 편 요약(G17) · 월요일 채널 스윕 · 항상 뮤트 · 40자 초과 구현 주장 = 헤드라인+요점(migration 113)
- 10-20 진화 조건 판정은 fut.gg 유지(내부 계산 기각 — 낡은 포지션·신규 카탈로그 결손으로 조용한 누락) · 조회만 병렬화
- 10-19 진화 수집 대상 = 진화 조건 통과 빌라 카드(fut.gg 적용가능 API `club_id=2` 선확인 → 그 base만 경로) · 조회 실패 시 멈춤(`58cca1b`)
- 10-14 이전(HANDOFF v2 · `.db` git 제외 · 구조 제거 원칙 · 명시 스테이징 · 근거 등급 · docs/70 분리 등) → [docs/decisions.md](docs/decisions.md)

## 최근 세션 기록

- **10-22 · 부모 세션(대화) + 서브에이전트·하위 세션**(`ae96b01`~`0d58a93` 8커밋) — 바이킹전 D+1 보강(뮤트 전사 6 · obs#1114~1119 · D+2/D+3 예약) · FC27 구현 검토·반영(optimal #46 · opt 선발 재지정 · 게이트 6종) · 슬롯 정본 5건 사용자 보류(obs#1123) · 국면 분 백필·FC27 카드 · migration 116~121(형태·세트피스·setup_kind·보유 fit·모멘텀·PlayStyle 별칭) · SS 48필드·FotMob 경기 스탯·WS 수신 · FC27 시스템 #57~62 · 메타 대조군 #47~49 · 디자인 개편(글래스·가독성·라이트) · 경기 분석 새 지표 3종 · 리서치 4편(`reports/research/2026-10-22-*`)
- **10-20 · 부모 세션(대화) + 하위 4**(`56f7a63`~`5c71776` 17커밋) — 진화 수집 병렬(조건 판정 12→2초) · Excluded Rarity · 사이트 이름 「택틱스 랩」·로고 · 진화/SBC 숨김 · 카드 포지션 이력 · 케미 신호 증분(클럽 싱크 22분→5분) · 경기 분석 개편(가설 판정·흐름·부상 KST·포지션 스탯·전술 4칸·목차·범례) · 영상(오분류 수정·지시 한국어화·헤드라인·UTV 6편·뉴캐슬 35편 요약·채널 스윕·뮤트) · 카마라 Build-Up 후보 · 하위 세션 커밋 규칙 · 헤밍스 Zoomaestro 시작 · SBC 101 완료 기록
- **10-19 23시 · 주간 match-watch(스케줄)** — CHE 1·LIV 2·ATM 2 수집 · 리포트 #57~#61 draft · DB는 이후 커밋 덤프에 실렸고 리포트·전사 본문은 10-20 커밋에 실음 · D+3 예약 3건은 보류로 미등록
- **10-19 · 클럽 싱크 [선수+진화+sbc] + 진화 수집 빌라 한정**(`58cca1b`) — 보유 216 · Zoomaestro 비교(부엔디아 추천) · G34 우회 커밋
- 아카이브: 10-17 21시 이적 감시(`3e2790b` 미푸시 소실 · Endrick DEAD · Scott MEDIUM-HIGH) · 10-17 페네르바흐체 D+3 종결(`28da5f6` · #55 complete) · 10-17 클럽 싱크 2회(`b56a224`·`7c128e8`) · 10-17 09시 이적 감시 · 10-14 이전 → [handoff-context](docs/handoff-context.md#최근-작업) · `git log`

## 문서 맵

- 고정 작업 규칙 · 핵심 방법론 · 데이터 수집 결손 · 참고 문서 원문 → [docs/handoff-context.md](docs/handoff-context.md)(목차)
- 런북 `.claude/skills/{transfer-watch,match-watch,player-collect,club-sync}/SKILL.md` · DB/export/git docs/40 · 수집 docs/30 · 메커니즘 docs/22 · 인게임 docs/50
- 기록 공백 주의: 다른 세션이 코드만 push하고 HANDOFF를 안 고친 전례가 두 번(09-23 14커밋 · 10-14 22커밋) — 착수 시 `git log`를 정본으로
