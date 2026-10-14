# HANDOFF — tactics

<!-- 구조 규칙(2026-10-14 v2): 헤더 15줄 안에 착수 조건 · 현재 상태 표 10행 이내 · 다음 할 일은 열린 항목만(항목당 2줄) · 세션 기록 최대 5개 · 목표 10~15KB · 상한 20KB(`wc -c`). 넘치면 지우지 말고 docs/handoff-context.md · docs/decisions.md로 포인터 압축. 절차 정본: .claude/skills/handoff/SKILL.md -->

- **담당자** 김호근 · **갱신** 2026-10-14 23시 · **세션** HANDOFF v2 압축(데이터 세션 아님) · **작업 PC** `AD03230205ui-iMac.local` · **브랜치** main · **WIP** 없음
- **마지막 커밋** = `git log -1`(이 문서를 갱신한 커밋) · 직전 데이터 커밋 `9dd8025`(10-14 클럽 싱크 2회차) · **문서 버전** v2 · **분량** 10.4KB(목표 10~15 · 상한 20)
- 실축 감독 전술(**AVL/에메리(주) · CHE/알론소 · LIV/이라올라 · ATM/시메오네**)을 실측으로 분해해 FC26·FC27 전술로 재현. 규약 정본 `CLAUDE.md` · `docs/00-overview.md`.

> ⛔ **먼저 알 것**
> 1. **명시 스테이징만** — `.claude/settings.json`(Figma PAT 등) 커밋 금지 파일이 있어 `git add -A`·`.`이면 푸시가 막힌다 · 커밋 직전 `git diff --cached --stat` · DB 변경은 `python3 scripts/ship.py -m "…"` 한 줄(CLAUDE.md 불변규칙 5)
> 2. git엔 `.db`가 없다 — pull 뒤 **`scripts/db_restore.sh`**(낡으면 G33·`db_dump.sh`가 멈춘다) · **반복 사고 규칙 정본은 [docs/70-lessons.md](docs/70-lessons.md)** — 세션 시작 시 함께 읽고, 새 사고는 HANDOFF가 아니라 거기에
> 3. 예약 정본은 `list_scheduled_tasks`(CronList 아님) · **이 iMac 전용 · 3회 유실** → 회차마다 실재 확인 · 스케줄 세션이 같은 작업 트리·인덱스를 쓴다 → 그 세션이 끝날 때까지 커밋 보류 · `~/Documents` 경로는 PC마다 다르다(`AL02359162`는 `/Users/user/…`)

---

## 현재 상태

| 영역 | 상태 | 정본 |
|---|---|---|
| 최근 실행 | 10-14 10시 3팀 이적 감시 — cron FotMob 파일 `logs/fotmob-20261012-2100.txt` **0바이트**라 DB 선조회+공개 웹으로 대체 · 신규/갱신/STALE 0 · DB 무변동 · ⚠️ 리포트 `reports/transfer-watch/2026-10-14.md`는 **미커밋(그 실행 소유)** | [원문 블록](docs/handoff-context.md#현재-상태) |
| 이적 | Endrick `MEDIUM` · Alex Scott `MEDIUM-HIGH`(창 판단 대기) · Gilberto Mora `MEDIUM` · 미결 이적 4건(에메날로·르마르·바르가스·응게상) | `reports/transfer-watch/` · `transfers` |
| DB·git | `.db` git 제외(`aba9dad`) · `db/dump/`만 · 스탬프 G33 · 게이트 G1~G34 | [decisions](docs/decisions.md) · docs/40 |
| 경기 수집 | 10-10~11 3경기 적재(#52 CHE · #53 LIV · #54 ATM) · **#51 AVL·#52 CHE D+3 complete**(10-13) · ⚠️ LIV D+2·D+3 · ATM D+3 종결 커밋은 git log에 없다(미확인) | `match_reports` · `reports/match-watch/` |
| FUT 구단 | 10-14 2회차 보유 253 · 만잠비 아카데미 III 완료(드리블 · OVR 83) · 잭슨 갈림길 재결정 Tiki Taka + First Touch(`f44eaf4`) · ⚠️ 시세 미갱신(fut.gg Cloudflare 차단) | `fut_*` · `.claude/skills/club-sync/` |
| 자동화 | 10-12 복원 9건(정기 4 · 일회 5 — 일회는 10-13~14 시한 경과) · 브라우저 쓰는 `club-sync-daily`·`match-watch-weekly`는 「Run now」 선승인 필요 | [자동화 원문](docs/handoff-context.md#자동화) |
| 게임 시스템 | 패치 v1.0.5 없음(10-12) · ⏰ 10-17 PlayStyle+ Lab · 10-22 시즌 2(추정) · FC27 리서치는 C·B등급 0건 → 10월 중순 재조사 | `game_system_changes` · docs/22 |
| 열린 결손 | 링크 결손 3건(코나테·더글라스 루이스 소속 미상 · 엘리엇 포지션 충돌) · `ref_map25` 동률 비결정 버그 · ATM regime 4 CAM 슬롯 없음 · duty #246 억제 토큰 노트 잔존 | `gaps.py links` |
| 핸드오프 공백 | 10-12 23시(`0aad64e`) 이후 **22커밋**이 HANDOFF 블록 없이 쌓였다 — 위 표의 10-13~14 사실은 git log 기준 | `git log 0aad64e..` |

## 진행 중 작업 (WIP)

코드 WIP 없음. 미추적 `reports/transfer-watch/2026-10-14.md`는 10-14 10시 이적 감시 실행 소유 — 그 실행(또는 사용자)이 커밋한다.

## 다음 할 일

번호는 v1 체계 그대로(근거·경위 원문은 [handoff-context 「다음 할 일」](docs/handoff-context.md#다음-할-일)).

**P1**
- [ ] **이적 사용자 판단 3건** — Scott 창(`2027-winter` vs `2027-summer`) · N'Guessan 상태/승격 시점 · transfer-watch 런북의 낡은 `2026-summer` 고정값
- [ ] **cron FotMob 0바이트 원인** — `logs/fotmob-20261012-2100.txt` · 다음 이적 감시 전에 전수 스캔 경로 복구(미확인)
- [ ] **경기 D+N 미종결 확인** — LIV 맨시티(#53) D+2·D+3 · ATM 알라베스(#54) D+3 커밋 없음 → `list_task_runs`로 실행 여부부터
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
- [ ] 0-3d AVL 소스 2건(Aston Villa Review · Read Aston Villa 403) · 00⑶⑸ 역할 숙련도 대조·시각화 후속 · 11 병렬 중복 실행 가드 · 33 LIV LAM/RAM 슬롯
- [ ] 미해결 1 **ATM 포메이션 표기 충돌**(4-4-2 기울음 · 감독 발언 0건) · 삭제 후보 `reports/match-watch/2026-09-19-avl-tottenham.D1-findings.md`(전량 흡수됨)

## 주요 결정 (전문 [docs/decisions.md](docs/decisions.md))

- 10-14 HANDOFF 구조 규칙 v2 — 지우지 않고 포인터 압축(종전 「300줄 · 완료 항목 지운다」 대체)
- 10-12 `.db` git 제외 · dump + `db_restore.sh`(`aba9dad`) · 예약은 enabled 9건만 복원
- 09-23 같은 문제 2번째면 구조 제거(불변규칙 13) · report 47 재점검 안 함
- 09-2x 진화 갈림길은 체감 기준 · 09-21 명시 스테이징 · 근거 등급 A~D(불변규칙 12)
- 09-20 반복 사고 규칙 docs/70 분리 · `pulled`/`scope` 토큰 규약 · 「조건 미충족」 억제 · 09-13 T6 단일 변수

## 최근 세션 기록

- **10-14 10시 · 3팀 이적 감시**(블록 표기 PC `AL02359162.local`) — FotMob 0바이트 · 신규 0 · 리포트 미커밋 → [원문](docs/handoff-context.md#현재-상태)
- **10-12 23시 · 계정 전환 후 예약 복원 + 만잠비 아카데미 II**(`31a86ec`) — 레지스트리 0건 → 옛 계정 파일에서 9건 재등록 · 만잠비 OVR 82
- **10-12 20시 · 주간 경기 수집**(`3918bfe`) — 3경기 draft 적재 · CHE xG 4연속 열세(obs#991) · ATM 「요렌테 3번째 CB」 기각(obs#996) · duty #246 REJECTED
- **10-12 · 패치 감시 + 클럽 싱크 + DB 저장 구조 전환**(`aba9dad`·`dd811b4`·`51261ae`) — `.db` git 제외 · `fut_club.py evolve`는 `--completed` 필수
- **10-08 21시 · 3팀 이적 감시**(`ac8b38e`) — LIV 유출 3건 STALE · Alex Scott 신규 `MEDIUM-HIGH`
- 아카이브: 09-23 ㊱(토트넘전 6회차 종결 · 진화 갈림길 통합) 및 09-18~22 ㉕~㉟ → [handoff-context 「현재 상태」·「최근 작업」](docs/handoff-context.md#최근-작업) · 그 이전은 `git log`·`observations`

## 문서 맵

- 고정 작업 규칙 · 핵심 방법론 · 데이터 수집 결손 · 참고 문서 원문 → [docs/handoff-context.md](docs/handoff-context.md)(목차)
- 런북 `.claude/skills/{transfer-watch,match-watch,player-collect,club-sync}/SKILL.md` · DB/export/git docs/40 · 수집 docs/30 · 메커니즘 docs/22 · 인게임 docs/50
- 기록 공백 주의: 다른 세션이 코드만 push하고 HANDOFF를 안 고친 전례가 두 번(09-23 14커밋 · 10-14 22커밋) — 착수 시 `git log`를 정본으로
