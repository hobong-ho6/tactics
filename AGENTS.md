# AGENTS.md — Codex CLI 진입점

**규약의 정본은 [CLAUDE.md](CLAUDE.md)와 [docs/00-overview.md](docs/00-overview.md)다. 먼저 읽어라.**
이 파일은 그것을 대체하지 않고, **에이전트 툴 없이 셸에서 돌릴 때 달라지는 것만** 적는다.
(2026-08-13 신설. 목표는 Claude Code와 Codex CLI **양쪽에서 동일하게** 돌아가는 것이다.)

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
절차는 [.claude/skills/hadoff/SKILL.md](.claude/skills/hadoff/SKILL.md)에 있고 **툴 중립이라 그대로 쓸 수 있다**.

## 2. 브라우저가 필요한 작업 — 스크립트로 대체한다

Claude Code에서는 MCP 브라우저 툴로 오리진 JS를 돌렸다. Codex에는 그 툴이 없으므로 아래를 쓴다.
**두 경로는 같은 값을 낸다**(2026-08-13 회귀 검증: 완비사카 25경기 `map25` 일치, RB 적합 `.932` 일치).

| 필요한 것 | Claude Code | Codex CLI |
|---|---|---|
| SofaScore 실측 | `mcp__Claude_Browser__javascript_tool` | `.venv/bin/python scripts/collect_sofascore.py <player_id> --from … --to …` |
| Fotmob 루머 | `preview_start` + `get_page_text` | `.venv/bin/python scripts/fetch_fotmob.py AVL CHE LIV` |
| 페이지 확인 | `preview_start {name:"heatmap"}` | `scripts/serve.sh` (기본 8123, `PORT=` 로 변경, HTML·JS·JSON 캐시 비활성) |

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
| 경기 실측·심층 리포트 | [.claude/skills/match-watch/SKILL.md](.claude/skills/match-watch/SKILL.md) | §2 수집을 `collect_sofascore.py`로. 완료본은 전술·선수 분석과 별도 경기 분석 메뉴 공개까지 포함. |

⚠️ **스킬 본문이 "메인 세션이 브라우저로"라고 쓴 부분은 Codex에서 스크립트로 읽는다** —
판정·DB 쓰기·리포트·커밋의 책임 분담은 그대로다.

## 4. DB 변경 후 고정 절차 (양쪽 동일)

```bash
python3 scripts/export.py     # site/data 재생성 (게이트 자동 강제)
scripts/db_dump.sh            # db/dump 재생성
git add db/tactics.db db/dump/ site/data/ reports/…   # ⛔ git add -A 금지
```

⛔ **`git add -A` 금지** — `.claude/settings.json`(Figma PAT)이 있어 푸시가 차단된다. 명시 스테이징만.

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
