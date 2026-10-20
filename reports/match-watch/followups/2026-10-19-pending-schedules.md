# 미등록 후속 추적 예약 3건 (2026-10-19 주간 수집 회차)

> ⚠️ 비대화형 스케줄 회차에서 `create_scheduled_task`가 **사람 승인 필요**로 거부됐다(3건 모두). 아래 내용을 그대로 `fireAt` 1회성 태스크로 등록하면 G34가 풀린다.
> ⛔ 등록 전까지 G34가 실패해 `ship.py`·`export.py`·`club_sync.py`가 멈춘다 — 이 회차의 DB 변경·리포트는 **미커밋 상태**로 작업 트리에 남아 있다(아래 「커밋 대기」).
> 같은 날 20:00 `mw-avl-newcastle-d3`(기존 예약)·21:00 `club-sync-daily`와 겹치지 않게 시각을 엇갈렸다.

| taskId | 제목 | fireAt | 경기 |
|---|---|---|---|
| mw-che-everton-d3 | 에버턴–첼시 D+3 종결 | 2026-10-20T20:40:00+09:00 | Everton 0-2 Chelsea · #57 |
| mw-atm-espanyol-d3 | 에스파뇰–아틀레티코 D+3 종결 | 2026-10-20T22:00:00+09:00 | Espanyol 0-1 Atlético · #59 |
| mw-liv-brentford-d3 | 브렌트퍼드–리버풀 D+3 종결 | 2026-10-20T22:50:00+09:00 | Brentford 1-2 Liverpool · #61 |

LASK전(#60, 10-14)·맨유전(#58, 10-13)은 수집 시점이 이미 D+5·D+6이라 남은 D+N이 없다(리포트 「## D+N 추적」 절).

## 공통 머리말(세 프롬프트 앞에 붙인다)

```text
작업 디렉터리 /Users/ad03230205/Documents/tactics 에서 `/match-watch` 런북 §2-1a 「경기 후 3일 추적」의 **D+3(마지막) 회차**를 수행한다. 답변은 한국어. 규칙은 CLAUDE.md · .claude/skills/match-watch/SKILL.md. 시작 전 DB가 없거나 낡았으면 `scripts/db_restore.sh`. 같은 날 다른 매치워치 예약과 21:00 클럽 싱크가 같은 작업 트리를 쓰므로 `git status`로 다른 세션의 미커밋 인덱스가 없는지 먼저 확인하고, 있으면 그 세션이 끝날 때까지 커밋을 보류한다.
산출 공통: 리포트에 `## D+3 추적 (2026-10-20) — 3일 추적 마지막 회차` 절 추가(기존 절 덮어쓰기 금지 · 당일 판정이 뒤집히면 「당일 판정 정정」 + obs) → G12 조건(필수 섹션·출전 선수 match_player_reports·경기 프리셋·선발 11 처방) 확인 후 match_reports status complete → manager_profiles 갱신 판정(덧붙임 또는 사유) → 새 전사는 index_transcripts.py → write_video_summary.py(impl_claims · 주장 없으면 {"axis":"none"}) → `python3 scripts/refresh_duty_applied.py` → `python3 scripts/ship.py -m "<메시지>" reports/match-watch/ reports/transcripts/` (⛔ git add -A 금지 · 메시지 끝 `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`). 다국어(불변규칙 10) · 외국어 인용 원문 「…」+한국어 번역(불변규칙 11) · 자막 인용은 auto-caption 명기.
```

## mw-che-everton-d3 — fireAt `2026-10-20T20:40:00+09:00`

```text
경기: Everton 0-2 Chelsea · PL 7R · 2026-10-17(첼시 원정). SofaScore event 16363884 · FotMob 5795478 · WhoScored 1983609 · matches #121 · match_reports #57(draft) · regime 2. 리포트 reports/match-watch/2026-10-17-che-everton.md(§1~§9 + 「## D+2 추적 (2026-10-19)」 먼저 읽기). 전사 8편 적재 완료(qm65lcoeEPg·dNQjlVTxyow·2awxA4CthJ4·qy3pG8Ztwx4·_D8IC3L2jC4·Vgb-8ydls6k·fPk9l5Gw9oI·GTdW_5roptc).
할 일: ⑴ 재시도 — The Athletic(Johnson·Twomey)·football.london 원문 · Spielverlagerung/TFA/Coaches' Voice · 새 전술 영상 · 스페인어·독일어(알론소)·포르투갈어(네투·주앙)·네덜란드어(하토)·프랑스어(라크루아)·에버턴 관점. ⑵ 닫을 질문: 포메이션 표기 충돌(FotMob 4-2-3-1 vs SI 3-4-2-1) · 하프타임 수정 실체(롱킥 직접 경로 vs F365 「강화일 뿐」) · 마르티네스 턱 골절 복귀 · 차바리아 검사 결과 · 퀜다 1분(히트맵 없음 → 처방 행 없음)이 complete 전환 시 G12 「선수처방누락」에 걸리는지 확인 후 처리. 커밋 메시지: "data(match-watch): CHE at Everton D+3 종결 — …".
```

## mw-atm-espanyol-d3 — fireAt `2026-10-20T22:00:00+09:00`

```text
경기: Espanyol 0-1 Atlético Madrid · 라리가 J9 · 2026-10-17(원정 · 89′ 바에나). SofaScore event 16421071 · FotMob 5868094 · WhoScored 1994184 · matches #125 · match_reports #59(draft) · regime 4. 리포트 reports/match-watch/2026-10-17-atm-espanyol.md(+ 같은 주 2026-10-13-atm-manutd.md #58 참고).
할 일: ⑴ 재시도 — Marca·AS 평점·크로니카(0건이었음) · Into the Calderón(403) · FutbolFantasy(451) · Marca 회견 영상 KmoKZ4Rqhqs 자막 · 스페인어 1차 + 카탈루냐어(에스파뇰)·한국어(이강인)·덴마크어(율만)·포르투갈어(카르도주). ⑵ 닫을 질문: FotMob 4-3-1-2 vs SofaScore 4-4-2(리포트는 4-4-2·이강인 세컨드 톱) · 67′ 로메로 교체 후 푸빌 CB 이동 여부(WhoScored 이벤트 좌표로 판정) · 로메로 내전근 결장 기간 · 카르도주 결장 사유(위장염 vs 휴식). 커밋 메시지: "data(match-watch): ATM at Espanyol D+3 종결 — …".
```

## mw-liv-brentford-d3 — fireAt `2026-10-20T22:50:00+09:00`

```text
경기: Brentford 1-2 Liverpool · PL 7R · 2026-10-17(원정 · 브렌트퍼드 퇴장 2: 45+8′ 야르몰류크·90+2′ 야넬트). SofaScore event 16363882 · FotMob 5795476 · WhoScored 1983607 · matches #123 · match_reports #61(draft) · regime 3. 리포트 reports/match-watch/2026-10-17-liv-brentford.md(+ 같은 주 2026-10-14-liv-lask.md #60 참고).
할 일: ⑴ 재시도 — 이라올라 회견 영상 자막(429였음: V5ptLTLy9IY · xp6xvEgV2RM · DAjJZGr1YFE · DjfdNs_yVEA · 4gKyYQo8uSE) · The Athletic·Echo 원본 · Tribuna·This Is Anfield(403) · FourFourTwo 응구모하 「두 번째 10번」 본문 · 스페인어·바스크(이라올라)·헝가리어(소보슬라이·케르케즈)·네덜란드어(프림퐁)·스웨덴어(이삭)·독일어(비르츠)·브렌트퍼드 관점. ⑵ 닫을 질문: 아라우호 HT 교체 사유 · 소보슬라이·프림퐁 결장 기간 · 52′ 이후 응구모하 위치(WhoScored 이벤트) · 이삭 st_target/st_poacher Δ0.000 tie-break. 커밋 메시지: "data(match-watch): LIV at Brentford D+3 종결 — …".
```

## 커밋 대기(이 회차 산출물 — 예약 등록 후 한 줄로 닫는다)

⚠️ 같은 시각 작업 트리에 **다른 세션의 미커밋 변경**(core/db.py 신설·scripts 70여 개 수정·전사 ~50편)이 있었다 — `reports/transcripts/` 디렉터리 통째로 넘기지 말고 이 회차 파일만 명시한다:

```bash
python3 scripts/ship.py -m "data(match-watch): 주간 2026-10-19 — CHE 에버턴·LIV LASK/브렌트퍼드·ATM 맨유/에스파뇰 5경기 수집 · 리포트 #57~#61 draft" reports/match-watch/2026-10-13-atm-manutd.md reports/match-watch/2026-10-14-liv-lask.md reports/match-watch/2026-10-17-atm-espanyol.md reports/match-watch/2026-10-17-che-everton.md reports/match-watch/2026-10-17-liv-brentford.md reports/match-watch/followups/2026-10-19-pending-schedules.md reports/transcripts/qm65lcoeEPg.en-orig.md reports/transcripts/dNQjlVTxyow.en-orig.md reports/transcripts/2awxA4CthJ4.en-orig.md reports/transcripts/qy3pG8Ztwx4.en-orig.md reports/transcripts/_D8IC3L2jC4.en-orig.md reports/transcripts/Vgb-8ydls6k.en-orig.md reports/transcripts/fPk9l5Gw9oI.en-orig.md reports/transcripts/GTdW_5roptc.en-orig.md reports/transcripts/S06UYKVkU-Q.en.md reports/transcripts/hLAykzL58Q4.de.md HANDOFF.md
```
