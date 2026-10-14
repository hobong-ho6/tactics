# 주요 결정 — 전문

<!-- 2026-10-14 HANDOFF v2 압축 때 신설. 되돌리기 어렵거나 이후 작업의 전제가 되는 결정만 둔다. HANDOFF.md 「주요 결정」엔 한 줄씩만, 전문은 여기.
     인용 문단은 v1 HANDOFF 원문(docs/handoff-context.md)에서 그대로 옮겼다. 규약 자체의 정본은 CLAUDE.md 불변규칙 · docs/70-lessons.md이고, 여기는 「언제·왜 그렇게 정했나」의 색인이다. 최신을 맨 위에. -->

## 2026-10-14 · HANDOFF 구조 규칙 v2(포인터 압축)

- 사용자 지시(핸드오프 쓰는 전 프로젝트 동일 적용). 헤더 15줄 안에 착수 조건 · 현재 상태 표 10행 · 다음 할 일은 열린 것만 · 세션 기록 최대 5개 · **목표 10~15KB · 상한 20KB 하드**. 절차 정본은 `.claude/skills/handoff/SKILL.md` 「갱신 규칙」·「분량 조정」.
- v1 HANDOFF 원문은 `docs/handoff-context.md`로 옮겼다(지우지 않음). 종전 고정 작업 규칙 8 「HANDOFF는 300줄 이하로 유지한다. 완료된 항목·해소된 미해결은 **지운다**」는 이 규칙으로 대체됐다 — 지우지 않고 옮긴다.

## 2026-10-13 · 잭슨 Creative or Composed? 갈림길 재결정

- `f44eaf4` — Tiki Taka + First Touch로 obs#940의 가지 선택을 대체(커밋 메시지 기준 · 근거는 obs#940과 그 커밋). 아래 09-2x 「체감 기준」 결정과 같은 축.

## 2026-10-12 · `.db`를 git에서 뺀다 — dump만 나른다

> **ⓐ ⭐⭐ `.db`는 이제 git에 없다**(`aba9dad` · 사용자 결정 「①+② 둘 다」). DB 101.2MB로 GitHub 100MB 상한에 **두 번째** 막혀(1차 10-04 103.8MB)
> ① 케미 신호를 「바뀐 행만 저장」(migration 106 · `core/chem_signals.py` · 59,962→9,619행 · 16회차 스냅샷 전후 동일) ② `db/tactics.db`를 .gitignore로 —
> git은 `db/dump/`만 나르고 **각 PC는 `scripts/db_restore.sh`로 DB를 만든다**(97표 데이터·스키마 전부 원본과 일치 검증).
> ⛔ **다른 PC(`AD03230205ui-iMac`)는 pull하면 `db/tactics.db`가 지워진다 — 정상이다. 곧바로 `scripts/db_restore.sh`.**
> pull로 들어온 dump를 옛 DB로 덮으면 남의 데이터가 사라지므로 **G33·`db_dump.sh`가 스탬프(`db/dump/_stamp.txt` ↔ 로컬 `db/.dump_stamp`)로 막는다.**

## 2026-10-12 · 계정 전환 후 예약은 「enabled였던 9건만」 복원

> 옛 계정의 레지스트리 파일(`~/Library/Application Support/Claude/claude-code-sessions/<옛 계정>/…/scheduled-tasks.json`, 10-12 21:11 스냅샷)에서
> **enabled였던 9건만** 같은 cron·fireAt으로 재등록한 뒤 SKILL.md 원문을 바이트 단위로 되돌렸다(백업 `~/.claude/scheduled-tasks-backup-20261012/`).

- 꺼져 있던 `fc27-patch-watch` · `transfer-watch-daily` · `futgg-prices-daily`는 복원하지 않았다 — 다시 쓸지는 사용자 판단(HANDOFF 다음 할 일 0-6).

## 2026-09-23 · 같은 문제를 두 번째로 확인하면 「구조」를 없앤다

- 사용자 지시 「앞으로 동일한 문제를 확인하면 **바로 구조를 없애서 수정**해줘」. 정본은 CLAUDE.md 불변규칙 13 · `docs/70-lessons.md` 머리말(① 구조 제거 → ② 단일 정본 → ③ 게이트 → ④ 스크립트 → ⑤ 문서).

## 2026-09-23 · report 47(빌라-토트넘)은 재점검하지 않는다

> ⛔⛔ 리포트에 **「이 경기는 재점검하지 않는다」를 명시**했다 — PENDING 잔여 2건(#167 카마라·고메스 배급 ·
> #169 맥긴 러너 추적)은 **다른 경기의 누적 표본**이 조건이라 이 경기 안에서는 영원히 안 닫힌다.

## 2026-09-2x · 진화 갈림길은 「체감 기준」으로 고른다

> · ⭐⭐ **갈림길 옵션은 기준에 따라 뒤집힌다** — 속성 실이득 **옵션1=옵션2=+28**(OVR+5는 1단계 고정) · 역할 가중은 **42:28로 옵션1** · **체감·효율은 옵션2**(SHO 60→67 · 옵션1의 반응력은 근거 0 · 볼컨은 off-balance 입력에서 배제). 사용자가 **체감 기준** 채택.

- 갈림길 계산의 공통 기준은 docs/22 §6.2가 정본(09-23 ⓒ 통합).

## 2026-09-21 · 명시 스테이징만 — `git add -A` 금지

- `.claude/settings.json`(Figma PAT 등) 커밋 금지 파일 때문에 통째로 담으면 푸시가 차단되고, 동시 세션이 인덱스에 올려둔 변경이 함께 커밋돼 43줄이 지워진 실증이 있다. 정본: `.claude/skills/handoff/SKILL.md` 「스테이징 규칙」 · CLAUDE.md 불변규칙 5 · `scripts/ship.py`.

## 2026-09-21 · 게임 메커니즘 주장은 근거 등급(A~D)을 밝힌다

- 사용자 지시. 정본은 CLAUDE.md 불변규칙 12 · `game_system_changes` · docs/22 §2.1 · `reports/research/2026-09-21-fc27-system-stats.md`.

## 2026-09-20 · 반복 사고 규칙은 `docs/70-lessons.md`로 분리

- HANDOFF의 그 절만 100행이었다. ⛔ 다시 HANDOFF로 들여오지 않는다 — HANDOFF엔 링크만(handoff 스킬 「구조 규칙」).

## 2026-09-20 · `pulled`·`scope` 규약 — 마이그레이션 없이 토큰으로

> ✅ **`pulled`·`scope` 규약 docs/30 반영 완료**(09-20 사용자 지시, obs#883) — 마이그레이션 없이 기존 free-text 필드(`phase_source` · `team_match_stats.source`)에 토큰으로 적고, match-watch §3에 실행 단계를 넣었다.
> ⭐ **가능하면 `scope=full`로 받는다**(16종 화이트리스트면 카드·교체·세이브가 없어 「카드가 없다」류를 판정할 수 없다). ⏰ **전용 컬럼 + G12 확장은 사전등록 후보**(현재는 문자열 규약이라 기계 강제 없음).

## 2026-09-20 · 재판정 후보는 「조건 미충족」이면 억제 · 억제분은 따로 보고

> ✅ 조치: 사유에 **「조건 미충족」**이 있으면 억제 + 보고에 **근거 출처 표기**(시즌처방/경기전용/fit_role) + **억제분을 따로 보고**(「0건」과 「억제 3건」은 다른 상태다).

- 근거 obs#888(원인 ㉠~㉢은 `docs/handoff-context.md` 「진행 중 작업 (WIP)」).

## 2026-09-13 · 다음 인게임 A/B(T6)는 「캐시 falseback」 단일 변수

> 0. ⭐⭐ **P1 · 다음 인게임 A/B(T6) = 「캐시 falseback」 단일 변수**(2026-09-13 사용자 결정. ⛔ 2변수 동시 변경 계획은 폐기 — 귀속 불가, obs#702).

- ⛔ 시뮬 승점으로 전술 비교 금지(프레스티지를 측정하게 된다, obs#702) — 팀 설정 2축도 직접 플레이 A/B로만.
