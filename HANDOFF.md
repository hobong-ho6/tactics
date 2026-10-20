# HANDOFF — tactics

<!-- 구조 규칙(2026-10-14 v2): 헤더 15줄 안에 착수 조건 · 현재 상태 표 10행 이내 · 다음 할 일은 열린 항목만(항목당 2줄) · 세션 기록 최대 5개 · 목표 10~15KB · 상한 20KB(`wc -c`). 넘치면 지우지 말고 docs/handoff-context.md · docs/decisions.md로 포인터 압축. 절차 정본: .claude/skills/handoff/SKILL.md -->

- **담당자** 김호근 · **갱신** 2026-10-20 · **세션** 부모 세션(대화) — 진화 수집 병렬 · 숨김 · 경기 분석 개편 · 영상 파이프라인 · 하위 세션 커밋 규칙 · **작업 PC** `AD03230205ui-iMac.local` · **브랜치** main · **WIP** 없음
- **마지막 커밋** = `git log -1`(이 문서를 갱신한 커밋) · 직전 `5c71776` · **문서 버전** v2 · **분량** 13KB(목표 10~15 · 상한 20)
- 실축 감독 전술(**AVL/에메리(주) · CHE/알론소 · LIV/이라올라 · ATM/시메오네**)을 실측으로 분해해 FC26·FC27 전술로 재현. 규약 정본 `CLAUDE.md` · `docs/00-overview.md`.

> ⛔ **먼저 알 것**
> 1. **명시 스테이징만**(`git add -A` 금지 · `.claude/settings.json` PAT) · DB 변경은 `python3 scripts/ship.py -m "…"` 한 줄 · ⭐ **하위 세션은 커밋하지 않는다 — 부모가 `ship.py --collect <세션 id>`로 등록하고 모아서 ship**(CLAUDE.md 불변규칙 5 · 10-20) · migration 번호는 부모가 배정
> 2. git엔 `.db`가 없다 — pull 뒤 **`scripts/db_restore.sh`** · **반복 사고 규칙 정본은 [docs/70-lessons.md](docs/70-lessons.md)** · ⭐ **CHE·LIV·ATM 수집·업데이트 잠정 보류 — AVL만**(10-20 사용자 · 메모리 `che-atm-liv-collection-hold`)
> 3. 예약 정본은 `list_scheduled_tasks` · **이 iMac 전용** → 회차마다 실재 확인(10-20 뉴캐슬 D+3 예약은 「있다」고 적혀 있었지만 미등록이었다) · 스케줄 세션이 같은 작업 트리를 쓴다 → 끝날 때까지 커밋 보류

---

## 현재 상태

| 영역 | 상태 | 정본 |
|---|---|---|
| 게이트 | **전항 통과(10-20)** · 신설 G37(경기 분석 정형 축 · AVL 10-14 이후) · G38(밑줄+툴팁 단일 경로) · G17 확장(id>342 새 전사 요약 누락 · 한국어 칸 · 40자 초과 헤드라인) | `gates.py` |
| 수집 범위 | **AVL만** — CHE·LIV·ATM 잠정 보류(예약 `match-watch-weekly` AVL만 · G37 AVL만) · 10-19 주간 회차 5경기(#57~#61) 리포트는 draft로 보존 | 메모리 · 예약 프롬프트 |
| 경기 분석 화면 | 요약·경기 흐름 3묶음·관전 메모 가설 판정(D+N 정정=새 행)·부상(한국어·KST)·포지션별 스탯 카드·전술 분석 4칸·상단 목차 · migration 109·111·112·113 | `match-report.html` · `load_match_extras.py` |
| 영상 | 전사하면 같은 회차에 **전 편 요약**(G17) · 월요일 **채널 스윕**(UTV·Villans·1874 분석 영상) · 자막 포착은 **항상 뮤트** · 분류 정본 `resolve_kind` · 뉴캐슬전 40/40 요약 · UTV 분석 6편 | `index_transcripts.py` · 예약 프롬프트 |
| 경기 수집 | AVL 뉴캐슬 #56 **draft · D+3 미실시**(사용자 결정 · 예약 미등록이었음) · 페네르바흐체 #55 complete | `reports/match-watch/2026-10-17-avl-newcastle.md` |
| FUT 구단 | 10-20 싱크 217장 · 진화 수집 병렬(WORKERS=6) · Excluded Rarity 실판정 · 진화·SBC 세트 **숨김** · 카드 포지션 이력(110 · 맥긴·퀜다·소보슬라이) · 케미 신호 증분(클럽 싱크 22분→5분) · **진행 중 헤밍스 Zoomaestro lv1(10-20)** · SBC 101 완료 기록(카드 미반영) | `fut_*` · club-sync 런북 |
| 전술 판단 | 카마라 RDM `dm_holding/Defend` → **`dm_dlp/Build-Up` 후보 · 인게임 테스트 중**(obs#1080) · 스즈키 롱볼 증가 → 팀 설정 **유지**(obs#1081 · Balanced/Balanced/52) | `observations` |
| 이적 감시 | 10-17 21시 임시 클론 `3e2790b`는 **/tmp 소실·미푸시** — 원 작업트리 리포트 10-14~17 4건은 10-20 커밋에 실음 · CHE·LIV 이적 판단은 보류 | `reports/transfer-watch/` |
| 열린 결손 | 링크 결손 3건 · `ref_map25` 동률 비결정 · ATM regime 4 CAM 슬롯 없음 · 다른 경기 미분류 영상 62편(대부분 보류 팀) | `gaps.py links` |

## 진행 중 작업 (WIP)

코드 WIP 없음 · 하위 세션 0(10-20 전부 종료·부모가 ship).

## 다음 할 일

번호는 v1 체계 그대로(근거·경위 원문은 [handoff-context 「다음 할 일」](docs/handoff-context.md#다음-할-일)).

**P1**
- [ ] **카마라 RDM Build-Up 인게임 테스트 결과 받기**(obs#1080) — 결과·다음 2경기 실측으로 정본 변경 여부(새 행) 결정
- [ ] **헤밍스 Zoomaestro(2602) 단계 완료 기록** — lv1 시작 10-20(사용자는 부엔디아 추천 대신 헤밍스) · 단계마다 `complete` · 완주 OVR 65→72 · 다음 싱크 EA 실측 대조
- [ ] **SBC 101 카드 반영 확인** — 10-20 「기록만」 완료(낸 11장 모름) · 다음 클럽 싱크가 소모 카드를 잡는지 · 그 전 다른 SBC 제출 시 카드 겹침 주의
- [ ] **cron FotMob 부분/0바이트 원인** — 10-12·10-17 09/21시 0바이트, 10-16 21시는 AVL 8건 뒤 종료·예외 미기록. 팀별 종료코드/예외 기록과 실패 팀 재시도 구조 필요
- [ ] **000⑴ 패치 감시 후속** — FC27 Launch Update 미적재 3건(ICON 국적 +2→+1 · Hero 리그 +2→+1 · Hall of FUT) EA 원문 대조 후 적재 → 케미 재검산 · 스크립트 `reports/patch-watch/wip/2026-09-21-launch-update-insert.py`
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
- [ ] **0-2 FC27 Role+/++ 수집** — fut.gg `/api/fut/roles/` FC27 → `migrate_fc27.py --roles --check`(미해결 2 · 출시 후라 이제 가능)
- [ ] **0-3c 재검증 이월 5건**(obs#792) · **0-4 선수 축 517행 후처리** · **6 아틀레틱 5-4-1 전환 시각**(WhoScored 타임라인)
- [ ] **6-1 G13 확장 2건 사전등록** · `measured:season*` 처방 48건 sample_n 불일치 재산출(사용자 판단 대기)
- [ ] **8 obs#353 학포 RM** · **9 경기 전용 처방 재판정 파이프라인 편입** · **30 ATM 백3/백4 프리셋 병기**(obs#775)
- [ ] **15 claims 미작성 98편 · PENDING 23건**(09-20) — 회차마다 같은 경기 국면 그리드로 닫기
- [ ] **전사 3편 `match_videos` 미등재** — `U4OewDAQMCk` · `QkA0fScs5s8` · `ofp0s7RaNoc`(제외 권장 · 사유 기록) · G17 `impl_claims` 1행 필수
- [ ] **000⑵ 잔여** — DB `game_system_changes` #25 `autonomyIQ` impact 문구(별도 DB 작업)

**P3 · 판단 대기**
- [ ] **보류 해제 시(CHE·LIV·ATM)** — #57~#61 D+N · LIV 맨시티 #53 · ATM 알라베스 #54 D+N · 이적 판단(Scott 창·N'Guessan·런북 `2026-summer` 고정값) · followups `2026-10-19-pending-schedules.md`는 보류로 미등록
- [ ] 0-3d AVL 소스 2건(Aston Villa Review · Read Aston Villa 403) · 00⑶⑸ 역할 숙련도 대조·시각화 후속 · 11 병렬 중복 실행 가드 · 33 LIV LAM/RAM 슬롯
- [ ] 미해결 1 **ATM 포메이션 표기 충돌**(4-4-2 기울음 · 감독 발언 0건) · 삭제 후보 `reports/match-watch/2026-09-19-avl-tottenham.D1-findings.md`(전량 흡수됨)

## 주요 결정 (전문 [docs/decisions.md](docs/decisions.md))

- 10-20 하위 세션 커밋 금지 · 부모가 모아서 ship(`ship.py --collect`) · CHE·LIV·ATM 잠정 보류 · 뉴캐슬전 D+3 미실시 · 스즈키 롱볼 → 설정 유지(obs#1081)
- 10-20 영상: 전사 즉시 전 편 요약(G17) · 월요일 채널 스윕 · 항상 뮤트 · 40자 초과 구현 주장 = 헤드라인+요점(migration 113)
- 10-20 진화 조건 판정은 fut.gg 유지(내부 계산 기각 — 낡은 포지션·신규 카탈로그 결손으로 조용한 누락) · 조회만 병렬화
- 10-19 진화 수집 대상 = 진화 조건 통과 빌라 카드(fut.gg 적용가능 API `club_id=2` 선확인 → 그 base만 경로) · 조회 실패 시 멈춤(`58cca1b`)
- 10-14 HANDOFF 구조 규칙 v2 — 지우지 않고 포인터 압축(종전 「300줄 · 완료 항목 지운다」 대체)
- 10-12 `.db` git 제외 · dump + `db_restore.sh`(`aba9dad`) · 예약은 enabled 9건만 복원
- 09-23 같은 문제 2번째면 구조 제거(불변규칙 13) · report 47 재점검 안 함
- 09-2x 진화 갈림길은 체감 기준 · 09-21 명시 스테이징 · 근거 등급 A~D(불변규칙 12)
- 09-20 반복 사고 규칙 docs/70 분리 · `pulled`/`scope` 토큰 규약 · 「조건 미충족」 억제 · 09-13 T6 단일 변수

## 최근 세션 기록

- **10-20 · 부모 세션(대화) + 하위 4**(`56f7a63`~`5c71776` 17커밋) — 진화 수집 병렬(조건 판정 12→2초) · Excluded Rarity · 사이트 이름 「택틱스 랩」·로고 · 진화/SBC 숨김 · 카드 포지션 이력 · 케미 신호 증분(클럽 싱크 22분→5분) · 경기 분석 개편(가설 판정·흐름·부상 KST·포지션 스탯·전술 4칸·목차·범례) · 영상(오분류 수정·지시 한국어화·헤드라인·UTV 6편·뉴캐슬 35편 요약·채널 스윕·뮤트) · 카마라 Build-Up 후보 · 하위 세션 커밋 규칙 · 헤밍스 Zoomaestro 시작 · SBC 101 완료 기록
- **10-19 23시 · 주간 match-watch(스케줄)** — CHE 1·LIV 2·ATM 2 수집 · 리포트 #57~#61 draft · DB는 이후 커밋 덤프에 실렸고 리포트·전사 본문은 10-20 커밋에 실음 · D+3 예약 3건은 보류로 미등록
- **10-19 · 클럽 싱크 [선수+진화+sbc] + 진화 수집 빌라 한정**(`58cca1b`) — 보유 216 · Zoomaestro 비교(부엔디아 추천) · G34 우회 커밋
- **10-17 21시 · 3팀 이적 감시**(임시 클론 `3e2790b` · 미푸시 · /tmp 소실) — Endrick `DEAD` · Scott `MEDIUM-HIGH`
- **10-17 · AVL 페네르바흐체 D+3 종결**(`28da5f6`) — #55 complete · obs#1046~1047
- 아카이브: 10-17 클럽 싱크 2회(`b56a224`·`7c128e8`) · 10-17 09시 이적 감시 · 10-14 이전 → [handoff-context](docs/handoff-context.md#최근-작업) · `git log`

## 문서 맵

- 고정 작업 규칙 · 핵심 방법론 · 데이터 수집 결손 · 참고 문서 원문 → [docs/handoff-context.md](docs/handoff-context.md)(목차)
- 런북 `.claude/skills/{transfer-watch,match-watch,player-collect,club-sync}/SKILL.md` · DB/export/git docs/40 · 수집 docs/30 · 메커니즘 docs/22 · 인게임 docs/50
- 기록 공백 주의: 다른 세션이 코드만 push하고 HANDOFF를 안 고친 전례가 두 번(09-23 14커밋 · 10-14 22커밋) — 착수 시 `git log`를 정본으로
