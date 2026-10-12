# 미등록 후속 추적 예약 4건 (2026-10-12 주간 수집 회차)

> ⚠️ 비대화형 스케줄 회차에서 `create_scheduled_task`가 **사람 승인 필요**로 거부됐다. 아래 프롬프트를 그대로 `fireAt` 1회성 태스크로 등록하거나, 시각이 지났으면 수동 실행한다.

## mw-che-bournemouth-d3 — fireAt `2026-10-13T21:00:00+09:00`

```text
저장소 `/Users/ad03230205/Documents/tactics`에서 match-watch §2-1a **경기 후 추적 D+3**를 수행한다(규약 정본: `CLAUDE.md` · `.claude/skills/match-watch/SKILL.md` §2-1a). 이 세션은 이전 대화를 기억하지 않으므로 아래 식별값만 쓴다.

**경기**: Chelsea 5-1 AFC Bournemouth (PL 6R, 홈)
- 날짜 2026-10-10 · SofaScore event `16363873` · FotMob matchId `5795467` · WhoScored matchId `1983593` · `matches#116` · `match_reports#52`(draft) · regime 2(CHE · 알론소)
- 리포트: `reports/match-watch/2026-10-10-che-bournemouth.md` — **같은 파일에 `## D+3 추적 (YYYY-MM-DD)` 절을 추가**한다. 기존 절은 덮어쓰지 않는다(뒤집히면 「당일 판정 정정」 + 정정 obs).
- 이미 한 것(2026-10-12 정기 회차 = D+2): 전사 N9BE_nz9-Ec(알론소 회견)·8qEWOs7EiWU(로제 회견)·qUuex1uVCU8(TM 전술) → `reports/transcripts/` · 요약·impl_claims 적재 · obs #991~993.
- 이미 미수행으로 남긴 것: Diario AS 스페인어 회견 9Ha1TPloj4I(자막 429 — 재시도 1순위) · chelseafc.com·football.london 원문 · The Athletic(Twomey·Johnson) · TFA/BTL/Spielverlagerung/Coaches' Voice · kicker·Marca·Relevo·AS · Daily Echo 원문 · 주앙 페드루·네투·에스테방 발언

**절차**
0. `scripts/db_restore.sh`가 필요한지 확인(DB 없으면) → `python3 scripts/gates.py` 통과 확인(실패 시 중단·보고).
1. 서사 재수집은 서브에이전트 1개에 위임(읽기·검색 전용 · DB 쓰기/git 금지 · DB 선조회 먼저 · 발행일·체제 검증 · 조회하지 않은 것 쓰지 말 것 · 영상은 채널·제목·게시일·URL + 직접시청/자막/요약 명기). 대상: 그 경기 45분+ 선수·양 팀 감독, **유튜브 전술 분석·전술 블로그 가중**, 상대팀 관점 포함. ⭐ 다국어(불변규칙 10): 영어 + 스페인어·독일어(알론소) + 포르투갈어(주앙 페드루·네투·에스테방) + 스페인어(차바리아·카이세도 에콰도르·마르티네스 아르헨) + 본머스 현지(Daily Echo). ⭐ 외국어 인용은 원문 「…」 + 한국어 번역(불변규칙 11), 전사 인용은 confidence에 auto-caption.
2. 새 영상 전사는 `python3 scripts/yt_transcript.py <id> <lang>`(429면 `--list-subs`로 트랙 확인, 봇 차단 시 yt_transcript_json3.py) → `.venv/bin/python scripts/backfill_transcript_meta.py` → `.venv/bin/python scripts/index_transcripts.py` → match_videos.report_id=52 확인 → `.venv/bin/python scripts/write_video_summary.py <json>`(video_id 키 딕셔너리 · key_points 리스트 · axis는 role/focus/team_axis/instruction/limit/none · instruction은 field·value 필수 · 주장 없으면 {"axis":"none"}).
3. 서사가 실측과 어긋나면 실측 채택 + 충돌 obs. 재판정 대상: ⑴ 아체암퐁 비보유 RB화(obs#992) ⑵ 헨더슨–카이세도 피벗 claim(PENDING) ⑶ 헨더슨 measured #516 1·2위 무결정(cm_playmaker/Roaming vs cm_halfwinger/Support Δ.021)
4. `python3 scripts/refresh_duty_applied.py` — CONFLICT·재판정 후보를 이 회차에 판정(HELD는 재판정 조건 필수).
5. **D+3 = 마지막 회차**: 추적을 닫고 `match_reports#52` status를 complete로 올릴지 판단(TEMPLATE 필수 섹션·선수 전원·경기 프리셋 충족 시만). 올리지 않으면 사유를 리포트에 적는다.
6. `python3 scripts/ship.py -F <메시지파일> reports/match-watch/ reports/transcripts/` (⛔ git add -A 금지 · 메시지 끝 `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`). 새 자료 0건이어도 시도한 검색어·언어를 리포트에 적고 커밋한다.
7. 종료 보고: 새 소스 수 · 새 obs · 판정 변경 · 미수행+사유.
```

## mw-atm-alaves-d3 — fireAt `2026-10-13T21:30:00+09:00`

```text
저장소 `/Users/ad03230205/Documents/tactics`에서 match-watch §2-1a **경기 후 추적 D+3**를 수행한다(규약 정본: `CLAUDE.md` · `.claude/skills/match-watch/SKILL.md` §2-1a). 이 세션은 이전 대화를 기억하지 않으므로 아래 식별값만 쓴다.

**경기**: Deportivo Alavés 1-2 Atlético Madrid (라리가 8R, 원정 Mendizorroza)
- 날짜 2026-10-10 · SofaScore event `16421056` · FotMob matchId `5868081` · WhoScored matchId `1994159` · `matches#118` · `match_reports#54`(draft) · regime 4(ATM · 시메오네)
- 리포트: `reports/match-watch/2026-10-10-atm-alaves.md` — **같은 파일에 `## D+3 추적 (YYYY-MM-DD)` 절을 추가**한다. 기존 절은 덮어쓰지 않는다(뒤집히면 「당일 판정 정정」 + 정정 obs).
- 이미 한 것(2026-10-12 정기 회차 = D+2): 전사 EJ9p5Xnovu0(시메오네 회견)·fvXLWhcPV60·nuNt6DzSbt0·eWT4LATTFyk·CUdb5pym94M·b6Cu_bmT3cw → `reports/transcripts/` · 요약·impl_claims 적재 · obs #996~998.
- 이미 미수행으로 남긴 것: AS·Marca·Relevo·MD 원문 · Olé 원문 · El Correo·Noticias de Gipuzkoa·ABC · Spielverlagerung·TFA · 르노르망 62′ 교체 사유 1차 발언

**절차**
0. `scripts/db_restore.sh`가 필요한지 확인(DB 없으면) → `python3 scripts/gates.py` 통과 확인(실패 시 중단·보고).
1. 서사 재수집은 서브에이전트 1개에 위임(읽기·검색 전용 · DB 쓰기/git 금지 · DB 선조회 먼저 · 발행일·체제 검증 · 조회하지 않은 것 쓰지 말 것 · 영상은 채널·제목·게시일·URL + 직접시청/자막/요약 명기). 대상: 그 경기 45분+ 선수·양 팀 감독, **유튜브 전술 분석·전술 블로그 가중**, 상대팀 관점 포함. ⭐ 다국어(불변규칙 10): 스페인어 1차 + 한국어(이강인) + 아르헨 스페인어(로메로·훌리안·줄리아노) + 프랑스어(J.데이비드) + 슬로바키아어(한츠코) + 노르웨이어(쇠를로트) + 독일어(그리말도) + 이탈리아어(루크먼) + 알라베스 현지 매체. ⚠️ 마이데일리 「압박」은 「insistíamos」 오역 — 쓰지 말 것. ⭐ 외국어 인용은 원문 「…」 + 한국어 번역(불변규칙 11), 전사 인용은 confidence에 auto-caption.
2. 새 영상 전사는 `python3 scripts/yt_transcript.py <id> <lang>`(429면 `--list-subs`로 트랙 확인, 봇 차단 시 yt_transcript_json3.py) → `.venv/bin/python scripts/backfill_transcript_meta.py` → `.venv/bin/python scripts/index_transcripts.py` → match_videos.report_id=54 확인 → `.venv/bin/python scripts/write_video_summary.py <json>`(video_id 키 딕셔너리 · key_points 리스트 · axis는 role/focus/team_axis/instruction/limit/none · instruction은 field·value 필수 · 주장 없으면 {"axis":"none"}).
3. 서사가 실측과 어긋나면 실측 채택 + 충돌 obs. 재판정 대상: ⑴ 「요렌테 3번째 CB」 서사 REJECTED 유지 여부(obs#996) ⑵ 줄리아노 하강 5백(obs#997) ⑶ 카르도소 좌측 커버 claim(PENDING) ⑷ 루크먼 좌측 표적 claim(PENDING)
4. `python3 scripts/refresh_duty_applied.py` — CONFLICT·재판정 후보를 이 회차에 판정(HELD는 재판정 조건 필수).
5. **D+3 = 마지막 회차**: 추적을 닫고 `match_reports#54` status를 complete로 올릴지 판단(TEMPLATE 필수 섹션·선수 전원·경기 프리셋 충족 시만). 올리지 않으면 사유를 리포트에 적는다.
6. `python3 scripts/ship.py -F <메시지파일> reports/match-watch/ reports/transcripts/` (⛔ git add -A 금지 · 메시지 끝 `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`). 새 자료 0건이어도 시도한 검색어·언어를 리포트에 적고 커밋한다.
7. 종료 보고: 새 소스 수 · 새 obs · 판정 변경 · 미수행+사유.
```

## mw-liv-mancity-d2 — fireAt `2026-10-13T22:00:00+09:00`

```text
저장소 `/Users/ad03230205/Documents/tactics`에서 match-watch §2-1a **경기 후 추적 D+2**를 수행한다(규약 정본: `CLAUDE.md` · `.claude/skills/match-watch/SKILL.md` §2-1a). 이 세션은 이전 대화를 기억하지 않으므로 아래 식별값만 쓴다.

**경기**: Liverpool 0-3 Manchester City (PL 6R, 홈 Anfield)
- 날짜 2026-10-11 · SofaScore event `16363878` · FotMob matchId `5795472` · WhoScored matchId `1983603` · `matches#117` · `match_reports#53`(draft) · regime 3(LIV · 이라올라)
- 리포트: `reports/match-watch/2026-10-11-liv-mancity.md` — **같은 파일에 `## D+2 추적 (YYYY-MM-DD)` 절을 추가**한다. 기존 절은 덮어쓰지 않는다(뒤집히면 「당일 판정 정정」 + 정정 obs).
- 이미 한 것(2026-10-12 정기 회차 = D+1): 전사 DEbyTQ7CAIk(이라올라 회견)·FOuawf9cGrg(Totally Football Show) → `reports/transcripts/` · 요약·impl_claims 적재 · obs #994~995.
- 이미 미수행으로 남긴 것: 자막 429: LiamOnLiverpool XXUsiOgdijY · LNobbins kAvxTbS5tFo·_Xb11BQYprA · David Lynch NxytPN1UqQU(재시도 1순위) · 스페인어 매체 차단(이라올라 원어 발언 0건) · Echo 페이월 · FourFourTwo 본문 · Pearce·Joyce·Andy Jones · MEN 시티판

**절차**
0. `scripts/db_restore.sh`가 필요한지 확인(DB 없으면) → `python3 scripts/gates.py` 통과 확인(실패 시 중단·보고).
1. 서사 재수집은 서브에이전트 1개에 위임(읽기·검색 전용 · DB 쓰기/git 금지 · DB 선조회 먼저 · 발행일·체제 검증 · 조회하지 않은 것 쓰지 말 것 · 영상은 채널·제목·게시일·URL + 직접시청/자막/요약 명기). 대상: 그 경기 45분+ 선수·양 팀 감독, **유튜브 전술 분석·전술 블로그 가중**, 상대팀 관점 포함. ⭐ 다국어(불변규칙 10): 영어 + 스페인어(이라올라 — 바스크 매체 El Correo·Diario Vasco 포함) + 우루과이 스페인어(아라우호) + 독일어(비르츠) + 프랑스어(바르콜라·자케) + 헝가리어(케르케즈) + 네덜란드어(그라벤베르흐) + 포르투갈어(알리송) + 아르헨(맥 알리스터) + 시티 관점. ⭐ 외국어 인용은 원문 「…」 + 한국어 번역(불변규칙 11), 전사 인용은 confidence에 auto-caption.
2. 새 영상 전사는 `python3 scripts/yt_transcript.py <id> <lang>`(429면 `--list-subs`로 트랙 확인, 봇 차단 시 yt_transcript_json3.py) → `.venv/bin/python scripts/backfill_transcript_meta.py` → `.venv/bin/python scripts/index_transcripts.py` → match_videos.report_id=53 확인 → `.venv/bin/python scripts/write_video_summary.py <json>`(video_id 키 딕셔너리 · key_points 리스트 · axis는 role/focus/team_axis/instruction/limit/none · instruction은 field·value 필수 · 주장 없으면 {"axis":"none"}).
3. 서사가 실측과 어긋나면 실측 채택 + 충돌 obs. 재판정 대상: ⑴ 11대11 고압박(obs#994) · claim LIV defensive_approach HELD(조건: 11대11 90분 2경기 PPDA≤8) ⑵ 퇴장=역습 차단 파울(obs#995) ⑶ 맥 알리스터 LDM 단일 경기 dm_dlp/Roaming .809(Δ.127) vs 정본 dm_holding/Ball-Winning
4. `python3 scripts/refresh_duty_applied.py` — CONFLICT·재판정 후보를 이 회차에 판정(HELD는 재판정 조건 필수).
5. D+2 회차 — 닫지 않는다(D+3 예약이 따로 있다).
6. `python3 scripts/ship.py -F <메시지파일> reports/match-watch/ reports/transcripts/` (⛔ git add -A 금지 · 메시지 끝 `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`). 새 자료 0건이어도 시도한 검색어·언어를 리포트에 적고 커밋한다.
7. 종료 보고: 새 소스 수 · 새 obs · 판정 변경 · 미수행+사유.
```

## mw-liv-mancity-d3 — fireAt `2026-10-14T22:00:00+09:00`

```text
저장소 `/Users/ad03230205/Documents/tactics`에서 match-watch §2-1a **경기 후 추적 D+3**를 수행한다(규약 정본: `CLAUDE.md` · `.claude/skills/match-watch/SKILL.md` §2-1a). 이 세션은 이전 대화를 기억하지 않으므로 아래 식별값만 쓴다.

**경기**: Liverpool 0-3 Manchester City (PL 6R, 홈 Anfield)
- 날짜 2026-10-11 · SofaScore event `16363878` · FotMob matchId `5795472` · WhoScored matchId `1983603` · `matches#117` · `match_reports#53`(draft) · regime 3(LIV · 이라올라)
- 리포트: `reports/match-watch/2026-10-11-liv-mancity.md` — **같은 파일에 `## D+3 추적 (YYYY-MM-DD)` 절을 추가**한다. 기존 절은 덮어쓰지 않는다(뒤집히면 「당일 판정 정정」 + 정정 obs).
- 이미 한 것(2026-10-12 정기 회차 = D+1): 전사 DEbyTQ7CAIk(이라올라 회견)·FOuawf9cGrg(Totally Football Show) → `reports/transcripts/` · 요약·impl_claims 적재 · obs #994~995.
- 이미 미수행으로 남긴 것: 자막 429: LiamOnLiverpool XXUsiOgdijY · LNobbins kAvxTbS5tFo·_Xb11BQYprA · David Lynch NxytPN1UqQU(재시도 1순위) · 스페인어 매체 차단(이라올라 원어 발언 0건) · Echo 페이월 · FourFourTwo 본문 · Pearce·Joyce·Andy Jones · MEN 시티판

**절차**
0. `scripts/db_restore.sh`가 필요한지 확인(DB 없으면) → `python3 scripts/gates.py` 통과 확인(실패 시 중단·보고).
1. 서사 재수집은 서브에이전트 1개에 위임(읽기·검색 전용 · DB 쓰기/git 금지 · DB 선조회 먼저 · 발행일·체제 검증 · 조회하지 않은 것 쓰지 말 것 · 영상은 채널·제목·게시일·URL + 직접시청/자막/요약 명기). 대상: 그 경기 45분+ 선수·양 팀 감독, **유튜브 전술 분석·전술 블로그 가중**, 상대팀 관점 포함. ⭐ 다국어(불변규칙 10): 영어 + 스페인어(이라올라 — 바스크 매체 El Correo·Diario Vasco 포함) + 우루과이 스페인어(아라우호) + 독일어(비르츠) + 프랑스어(바르콜라·자케) + 헝가리어(케르케즈) + 네덜란드어(그라벤베르흐) + 포르투갈어(알리송) + 아르헨(맥 알리스터) + 시티 관점. ⭐ 외국어 인용은 원문 「…」 + 한국어 번역(불변규칙 11), 전사 인용은 confidence에 auto-caption.
2. 새 영상 전사는 `python3 scripts/yt_transcript.py <id> <lang>`(429면 `--list-subs`로 트랙 확인, 봇 차단 시 yt_transcript_json3.py) → `.venv/bin/python scripts/backfill_transcript_meta.py` → `.venv/bin/python scripts/index_transcripts.py` → match_videos.report_id=53 확인 → `.venv/bin/python scripts/write_video_summary.py <json>`(video_id 키 딕셔너리 · key_points 리스트 · axis는 role/focus/team_axis/instruction/limit/none · instruction은 field·value 필수 · 주장 없으면 {"axis":"none"}).
3. 서사가 실측과 어긋나면 실측 채택 + 충돌 obs. 재판정 대상: ⑴ 11대11 고압박(obs#994) · claim LIV defensive_approach HELD(조건: 11대11 90분 2경기 PPDA≤8) ⑵ 퇴장=역습 차단 파울(obs#995) ⑶ 맥 알리스터 LDM 단일 경기 dm_dlp/Roaming .809(Δ.127) vs 정본 dm_holding/Ball-Winning
4. `python3 scripts/refresh_duty_applied.py` — CONFLICT·재판정 후보를 이 회차에 판정(HELD는 재판정 조건 필수).
5. **D+3 = 마지막 회차**: 추적을 닫고 `match_reports#53` status를 complete로 올릴지 판단(TEMPLATE 필수 섹션·선수 전원·경기 프리셋 충족 시만). 올리지 않으면 사유를 리포트에 적는다.
6. `python3 scripts/ship.py -F <메시지파일> reports/match-watch/ reports/transcripts/` (⛔ git add -A 금지 · 메시지 끝 `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`). 새 자료 0건이어도 시도한 검색어·언어를 리포트에 적고 커밋한다.
7. 종료 보고: 새 소스 수 · 새 obs · 판정 변경 · 미수행+사유.
```
