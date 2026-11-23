# AGENTS.md — Codex CLI 진입점

**규약의 정본은 [CLAUDE.md](CLAUDE.md)와 [docs/00-overview.md](docs/00-overview.md)다. 먼저 읽어라.**
이 파일은 그것을 대체하지 않고, **에이전트 툴 없이 셸에서 돌릴 때 달라지는 것만** 적는다.
(2026-08-13 신설 · 11-23 보강(§1 · §2 · §3 · §7~9). 목표는 Claude Code와 Codex CLI **양쪽에서 동일하게** 돌아가는 것이다.)
사람이 한 번 해 둘 설정(설치 · `config.toml` · 브라우저 로그인 · 예약)은 [docs/codex-guide.md](docs/codex-guide.md).

## 0. 최초 1회 세팅

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/playwright install chromium
```

`.venv/`는 `.gitignore`에 있다. ⚠️ **머신마다 파이썬 버전이 다르다**(이 리포는 3.9.6과 3.14가 섞여 있었다) —
`__pycache__`를 커밋하지 말 것. 2026-08-13에 추적에서 제거했다.

## 1. 세션 시작·종료

CLAUDE.md와 동일하다 — 시작 시 `HANDOFF.md`를 먼저 읽고 한 줄 브리핑, 종료 시 갱신.
절차는 [.claude/skills/handoff/SKILL.md](.claude/skills/handoff/SKILL.md)에 있고 **툴 중립이라 그대로 쓸 수 있다**.

시작할 때 추가로(11-23):
1. **응답은 한국어** · 불변규칙 14(결론 먼저 · 표/목록) · 외국어 인용은 한국어 번역 병기(불변규칙 11).
2. [docs/70-lessons.md](docs/70-lessons.md)를 읽는다(재발 이력 규칙).
3. `git pull` 뒤에는 `scripts/db_restore.sh` — git에는 `.db`가 없고 `db/dump/`만 있다(불변규칙 1).
4. 미추적 `.claude/tmp_*` 등은 다른 세션(Claude 예약 회차 포함)의 작업분이다 — 알리고 손대지 않는다.
   HANDOFF 헤더 「같은 작업 트리 → 스케줄 세션 중엔 커밋 보류」를 지킨다.
5. Claude 자동 메모리(저장소 밖 `~/.claude/projects/-Users-user-Documents-tactics/memory/`)의 요지는 §9에 옮겨 두었다.

## 2. 브라우저가 필요한 작업 — 스크립트로 대체한다

Claude Code에서는 MCP 브라우저 툴로 오리진 JS를 돌렸다. Codex에는 그 툴이 없으므로 아래를 쓴다.
**두 경로는 같은 값을 낸다**(2026-08-13 회귀 검증: 완비사카 25경기 `map25` 일치, RB 적합 `.932` 일치).

| 필요한 것 | Claude Code | Codex CLI |
|---|---|---|
| SofaScore 실측 | `mcp__Claude_Browser__javascript_tool` | `.venv/bin/python scripts/collect_sofascore.py <player_id> --from … --to …` |
| Fotmob 루머 | `preview_start` + `get_page_text` | `.venv/bin/python scripts/fetch_fotmob.py AVL CHE LIV` |
| 페이지 확인 | `preview_start {name:"heatmap"}` | `scripts/serve.sh` (기본 8123, `PORT=` 로 변경, HTML·JS·JSON 캐시 비활성) |
| 보유 카드(club-sync 【선수】) | (11-20부터 스크립트) | `python3 scripts/club_sync.py 선수` — 공개 클럽 경로라 브라우저 불필요 |
| fut.gg GG Club 화면 · FUTWIZ 대체 조회(club-sync §2 · §6) | in-app 브라우저 패널(사용자 로그인 세션) | Codex **Chrome 플러그인**(`chrome@openai-bundled` · 사용자 Chrome의 로그인 세션 사용). 로그인이 안 돼 있으면 사용자에게 요청하고 멈춘다(로그인 대행 금지). FUTBIN은 어느 쪽이든 Cloudflare에 막힌다 |
| YouTube 자막(match-watch · HANDOFF 「먼저 알 것」 4) | 브라우저 fetch/XHR 훅 → `/api/timedtext` 본문 포착 | Codex Chrome 플러그인으로 같은 훅(항상 뮤트) → 응답 본문을 파일로 저장 → `yt_transcript_json3.py VIDEO en <파일>`. 셸 `yt-dlp`는 봇 차단 |
| SofaScore 경기 WS JSON · 팀 이벤트 목록(match-watch §1 · §6) | 브라우저 same-origin fetch | `collect_sofascore.py`가 덮지 않는 경로는 Chrome 플러그인으로 sofascore.com 오리진에서 fetch → JSON을 `reports/match-watch/data/`에 저장 후 파이썬으로 처리(불변규칙 4) |

⚠️ **왜 스크립트가 필요한가**: SofaScore API는 sofascore.com 오리진에서만 열리고 `curl`은 UA/Referer를
붙여도 **403**이다(docs/30 ②). Fotmob 루머 표는 **CSR**이라 정적 GET으로는 셸만 온다.
두 스크립트 다 Playwright의 실제 Chromium을 같은 오리진에 띄워 이 문제를 푼다.

수집 후 **인코딩·집계·커널은 `core/` 모듈만 쓴다**(불변규칙 4 — 재구현 금지):
`core.sofascore.parse_collected` → `core.aggregate.aggregate_rows` → `core.kernel.Kernel.best_fit_slot`.

## 3. 정기 작업 (스킬 = 런북)

`.claude/skills/`의 SKILL.md는 **Claude Code 전용 포맷이 아니라 읽고 따라 하는 절차서**다.
Codex에서는 슬래시 명령 대신 그 파일을 읽고 실행한다.

| 작업 | 런북 | Codex에서 달라지는 점 |
|---|---|---|
| 이적 감시 | [.claude/skills/transfer-watch/SKILL.md](.claude/skills/transfer-watch/SKILL.md) | §0의 **서브에이전트 3개 병렬**은 Codex에 대응물이 없다 → 순차 수행하거나 3회로 나눠 실행. §1 Fotmob은 위 스크립트로. |
| 경기 실측·심층 리포트 | [.claude/skills/match-watch/SKILL.md](.claude/skills/match-watch/SKILL.md) | §2 수집을 `collect_sofascore.py`로. 완료본은 전술·선수 분석과 별도 경기 분석 메뉴 공개까지 포함. 팀당 서브에이전트 · 영상 요약 묶음은 Codex 보조 에이전트(§7) 또는 순차. 자막은 §2 표 |
| FUT 클럽 싱크 | [.claude/skills/club-sync/SKILL.md](.claude/skills/club-sync/SKILL.md) | 인자 없이 불리면 `AskUserQuestion` 두 질문 대신 **채팅에 같은 두 질문**(수집 항목 `선수·진화·sbc·시세` 복수 선택 / 전술 안내 포함·안 함). 예약(`codex exec`)이면 묻지 말고 `전체`. 실행기 `python3 scripts/club_sync.py …`를 **한 번** 실행하고 끝날 때까지 기다린 뒤 로그를 한 번 읽는다(`run_in_background` 대체 · `sleep`+`tail` 반복 금지) |
| 한 선수 14축 수집 | [.claude/skills/player-collect/SKILL.md](.claude/skills/player-collect/SKILL.md) | SofaScore는 이미 Playwright 셸 경로(브라우저 MCP 불필요). 서사 수집 위임은 Codex 보조 에이전트(읽기 전용 · 브라우저 금지 규칙 그대로) |
| FC27 패치 감시 | Claude 예약 `fc27-patch-watch`(iMac · 저장소 밖 `~/.claude/scheduled-tasks/fc27-patch-watch/SKILL.md`) | 런북이 저장소 밖에 있다. Codex로 돌리려면 그 SKILL.md를 사람이 붙여 주거나 §8대로 프롬프트 파일을 만든다 |

⚠️ **스킬 본문이 "메인 세션이 브라우저로"라고 쓴 부분은 Codex에서 스크립트로 읽는다** —
판정·DB 쓰기·리포트·커밋의 책임 분담은 그대로다.

## 4. DB 변경 후 고정 절차 (양쪽 동일)

⭐ 11-23 갱신 — 정본은 CLAUDE.md 불변규칙 5다. **한 줄**로 한다:

```bash
python3 scripts/ship.py -m "<커밋 메시지>" [추가 경로…]   # 게이트 → export → dump → 명시 스테이징 → 커밋 → 푸시
```

- git에는 `.db`가 아니라 `db/dump/`만 싣는다(10-12부터). 위 스크립트가 dump·`site/data`를 함께 싣는다.
- ⛔ **`git add -A` 금지** — `.claude/settings.json`·`settings.local.json`(gitignore)에 클라우드 자격 증명·Figma PAT가 있다. 그 파일은 **읽지도 않는다**.
- 하위 작업(Codex 보조 에이전트 포함)은 커밋하지 않는다 — 메인 세션이 모아서 ship한다. Codex는 Claude식 「하위 세션」이 없으므로
  `ship.py --collect`는 쓰지 않는다. ⚠️ `ship.py`의 거부는 Claude 세션 id(`CLAUDE_CODE_HOST_SESSION_ID`)로만 걸리므로 **Codex는 막히지 않는다** —
  ship 전에 `db/.leases/collector.json`이 있으면(Claude 부모 세션이 모아서 커밋 중) 멈추고 사용자에게 알린다.

## 5. 정기 실행 (cron)

```bash
scripts/cron/install.sh            # 매일 09:00 / 21:00 등록 (멱등)
scripts/cron/install.sh --remove   # 해제
```

`scripts/cron/transfer-watch.sh`가 두 단계로 돈다: ⑴ Fotmob 3팀 수집(LLM 불필요, `logs/fotmob-*.txt`) →
⑵ `codex exec --sandbox danger-full-access`로 판정·DB·리포트·커밋(프롬프트는 `scripts/cron/transfer-watch-prompt.txt`).
codex가 없으면 ⑴만 하고 **그 사실을 로그에 남긴다** — 조용히 성공한 척하지 않는다.

`--full-auto`는 공식 문서상 deprecated이고 ChatGPT 앱 번들 CLI `0.147.0-alpha.6.5`에서는 제거됐다.
`--approve-for-me` smoke test는 통과했지만 실제 회차에서 `.git/FETCH_HEAD`가 차단돼 여러 PC 동기화에
쓸 수 없었다. 명시적 `--sandbox danger-full-access`로 `git fetch origin` 종료 0과 HEAD=origin/main을
확인했다. 이 모드는 저장소 밖에도 접근할 수 있으므로 **이 스크립트의 고정 프롬프트에만** 쓴다.
cron의 최소 PATH에서는 앱 번들을 못 찾을 수 있어
`/Applications/ChatGPT.app/Contents/Resources/codex`도 fallback으로 탐색한다.

### ✅ macOS TCC — 2026-08-14 검증 완료

**2026-08-13 실증**: cron 항목은 정상 등록·기동됐으나(11:00:01 실행 확인) 결과는
`bash: …/transfer-watch.sh: Operation not permitted`였다. cron이 TCC 샌드박스라 `~/Documents`를
읽지 못한다. **스크립트 문제가 아니다** — 같은 스크립트를 셸에서 직접 돌리면 정상 완료한다.

> 시스템 설정 → 개인정보 보호 및 보안 → **전체 디스크 접근 권한** → `+` → `⌘⇧G`로
> `/usr/sbin/cron` 추가 → 켜기

(이 저장소는 같은 TCC 문제를 이미 겪었다 — `.claude/launch.json`이 `/private/tmp` 미러를 서빙하는 이유가 그것이다.)
**2026-08-14 09:31:00 KST 실증**: `AD03230205ui-iMac.local`에서 2분 뒤 임시 `touch` probe가
저장소의 `logs/`에 marker를 만들었다. probe 행·marker만 제거했고, crontab은 09:00/21:00
`transfer-watch.sh` 각 1행을 유지한다. 이 PC의 검증 전 crontab은 비어 있어 정규 2행을 함께 설치했다.
따라서 TCC 이식 검증은 닫혔다. 새 PC에서는 같은 권한 설정 뒤 동일한 marker probe로 확인한다.

## 6. 이식 검증 상태 (미해결 0건)

- ~~**TCC 해제 후 cron 기동 재검증**~~ — 2026-08-14 임시 예약 probe가 저장소 marker를 생성해 완료.
- ~~**서브에이전트 병렬 스캔**~~ — Codex 보조 에이전트 3개(AVL/CHE/LIV)로 2026-08-13 실제 병렬
  스캔을 완료했다. 각 결과가 고정 4절·URL·발행일 형식으로 반환됨을 확인했다.
- ~~**실제 이적 감시 end-to-end**~~ — Fotmob 109행 → 순차 웹 크로스체크 → DB 근거 갱신 →
  export/dump/gates → 명시 스테이징 → push를 `afe002f`에서 완료했다.

## 7. Claude Code 전용 요소 → Codex 대응 (11-23)

| Claude Code | 쓰는 곳 | Codex에서 |
|---|---|---|
| `CLAUDE.md` 자동 로드 | 전부 | 이 파일 첫 줄대로 직접 읽는다 |
| 스킬 5개(`.claude/skills/{handoff,transfer-watch,match-watch,club-sync,player-collect}`) | 정기·수동 작업 | §3 표대로 SKILL.md를 읽고 따른다. `.agents/skills` 심볼릭 링크를 두면 Codex 스킬로도 뜬다(가이드 4절) |
| `Agent` 서브에이전트 | transfer-watch 스캔 · match-watch 팀별 · player-collect 서사 | Codex 보조 에이전트(08-13 3개 병렬 실증). 안 되면 순차. 판정·DB·커밋은 메인만 |
| 하위 세션 · `ship.py --collect` | 큰 작업 분할 | 없음 → 한 세션에서 순서대로. §4 주의 |
| `run_in_background` | club-sync 실행기 · ship `--wait` | 포그라운드로 끝까지 기다린다(실행기는 수 분). 10분을 넘길 일은 사용자 터미널에서 돌리게 안내 |
| `AskUserQuestion` | club-sync 메뉴 | 채팅에 번호 선택지(질문 구성은 런북 그대로) |
| Claude 브라우저 패널(`mcp__Claude_Browser__*`) | GG Club · FUTWIZ · 자막 · SofaScore WS | §2 표 — Playwright 스크립트 우선, 로그인·봇 검사가 필요한 곳은 Codex Chrome 플러그인 |
| 위젯(`show_widget`) — 불변규칙 8 히트맵 | 대화 속 5×5 그리드 | Codex `visualize` 플러그인으로 그리거나, HTML을 만들어 `scripts/serve.sh`로 띄워 링크를 준다. 규약(열0=좌측 · 행0=공격 방향 · 단일색 램프)은 같다 |
| `preview_start` + `.claude/launch.json` | 사이트 확인 | `scripts/serve.sh`(TCC 때문에 launch.json은 `/private/tmp` 미러를 쓴다 — 셸에선 불필요) |
| 데스크톱 예약(`scheduled-tasks` MCP · PC마다) | patch-watch · club-sync 10/21시 · match-watch 주간 · D+2/D+3 | §8 |
| 훅 | 없음(이 저장소는 훅을 쓰지 않는다) | — |
| Figma MCP(`figma@claude-plugins-official`) | 거의 안 씀 | Codex `config.toml`의 `[mcp_servers.figma]` |

## 8. 예약 작업

- 지금 예약은 **Claude 데스크톱 앱이 PC마다 따로** 돌린다(HANDOFF 「먼저 알 것」 3 · iMac). 확인은 Claude 쪽 `list_scheduled_tasks`.
  예약 본문은 저장소 밖 `~/.claude/scheduled-tasks/<이름>/SKILL.md`다.
- Codex로 옮길 때는 이적 감시(§5)와 같은 틀을 쓴다: `scripts/cron/<작업>.sh` + `<작업>-prompt.txt` → `codex exec --sandbox danger-full-access`.
  예약 본문을 `-prompt.txt`로 옮기고, 그 안의 Claude 도구 이름은 §7대로 바꾼다. ⚠️ 브라우저 로그인이 필요한 단계(GG Club)는 무인 실행에서 막힌다 — 런북의 「막히면 남은 것을 찍고 끝낸다」 규칙대로 둔다.
- ⛔ **같은 작업을 Claude 예약과 Codex cron에 동시에 걸지 않는다** — 같은 작업 트리·같은 DB에 두 회차가 겹친다. 옮기면 Claude 쪽 예약을 끈다.

## 9. Claude 메모리 요지 (저장소 밖 → 여기 옮김 · 11-23)

- `git add -A` 금지 — `.claude/settings.json`에 PAT. 작업 파일만 명시 스테이징.
- 빌라 영상 분석은 **UTVFANCHANNEL · TheVillans 채널을 항상 포함**(09-07 사용자 지시).
- 진화 추천 전에 `player_id` · 정본 역할 · 이전 맥락을 먼저 확인하고, 비교엔 세부 스탯 전체 · 키 · 몸무게 · 역할 · PlayStyle을 넣는다.
- 정기 수집은 **AVL만** — CHE는 11-04 1회성, LIV · ATM 보류.
- 3선(DM) 역할 조합은 상시 검토 대상.
