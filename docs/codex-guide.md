# Codex에서 tactics 돌리기 — 설정 가이드 (2026-11-23)

**결론**: 아래 1~5를 PC마다 한 번 하면 된다. 에이전트 규칙은 루트 `AGENTS.md`(→ 정본 `CLAUDE.md`)에 있고, 이 문서는 **사람이 할 설정**만 다룬다.

| 순서 | 할 일 | 시간 |
|---|---|---|
| 1 | Codex CLI 연결 | 1분 |
| 2 | 파이썬 환경 · DB 복원 | 5분 |
| 3 | `~/.codex/config.toml` 확인 | 1분 |
| 4 | 스킬 연결(선택) | 1분 |
| 5 | 첫 실행 점검 | 10분 |
| 6 | (선택) 예약을 Codex로 옮기기 | 작업당 10분 |

> ⛔ `.claude/settings.json` · `settings.local.json`(gitignore)에는 클라우드 자격 증명과 Figma PAT가 있다. 열어 보거나 복사하지 않는다. Codex는 이 값이 필요 없다(모델은 Codex 자체 설정 · Figma는 OAuth).

## 1. Codex CLI

ChatGPT 앱 번들에 들어 있다. 터미널에서 쓰려면 PATH에 연결한다.
```bash
sudo ln -sf "/Applications/ChatGPT.app/Contents/Resources/codex-cli/CodexCLI.app/Contents/MacOS/codex" /usr/local/bin/codex
```
앱의 Codex에서 쓸 거면 생략해도 된다(작업 폴더로 `~/Documents/tactics`를 연다).

## 2. 파이썬 환경 · DB

```bash
cd ~/Documents/tactics && python3 -m venv .venv && .venv/bin/pip install -r requirements.txt && .venv/bin/playwright install chromium
```
```bash
cd ~/Documents/tactics && git pull && scripts/db_restore.sh
```
git에는 `.db`가 없다(`db/dump/`만). pull할 때마다 `db_restore.sh`가 필요하다.

## 3. `~/.codex/config.toml`

필요한 것은 이미 있다(11-23 확인).
- `[projects."/Users/user/Documents/tactics"] trust_level = "trusted"`
- `[sandbox_workspace_write] network_access = true` — 수집 스크립트가 인터넷을 쓴다.
- `[mcp_servers.figma]` + `codex mcp login figma`(OAuth) — tactics에선 거의 안 쓴다.

새 PC라면 위 세 가지를 넣는다. Playwright Chromium이 샌드박스에서 안 뜨면 그 명령만 권한 상승을 승인한다.

## 4. 스킬 연결 (선택)

```bash
mkdir -p ~/Documents/tactics/.agents && ln -s ../.claude/skills ~/Documents/tactics/.agents/skills
```
`.agents/`는 `.gitignore`에 넣어 두었다(PC마다 만든다).

## 5. 첫 실행 점검

```bash
cd ~/Documents/tactics && codex
```

| # | 보낼 말 | 통과 기준 |
|---|---|---|
| 1 | 「핸드오프 확인하고 시작해」 | HANDOFF·`docs/70-lessons.md`를 읽고 **한국어 · 결론 먼저** 한 줄 브리핑 |
| 2 | 「AVL 정본 전술 요약해줘」 | DB를 조회해 답한다(기억으로 답하지 않음) · 표로 정리 |
| 3 | 「클럽 싱크」 | 인자 없으니 **두 질문(수집 항목 / 전술)**을 채팅에 낸다 |
| 4 | 「클럽 싱크 진화 --dry-run」 | `club_sync.py 진화 --dry-run`을 한 번 돌리고 계획만 보여 준다 |
| 5 | DB를 바꾸는 작은 요청 | `ship.py -m …` 한 줄로 끝내고 `git add -A`를 쓰지 않는다 |

브라우저 작업(GG Club 화면 · FUTWIZ · YouTube 자막)은 Codex **Chrome 플러그인**이 사용자 Chrome을 쓴다. 처음엔 Chrome에서 fut.gg에 직접 로그인해 둔다.

## 6. (선택) 예약을 Codex로 옮기기

지금 정기 작업은 둘로 나뉘어 돈다.

| 작업 | 지금 | Codex로 옮기면 |
|---|---|---|
| 이적 감시 09·21시 | **이미 cron + `codex exec`** (`scripts/cron/transfer-watch.sh`) | 그대로 |
| FC27 패치 감시 · 클럽 싱크 10·21시 · 경기 주간 · D+2/D+3 | Claude 데스크톱 예약(iMac · PC마다) | `scripts/cron/<작업>.sh` + `<작업>-prompt.txt`를 이적 감시와 같은 틀로 만든다 |

- 예약 본문은 Claude 쪽 `~/.claude/scheduled-tasks/<이름>/SKILL.md`에 있다. 그걸 `-prompt.txt`로 옮기면서 Claude 도구 이름을 `AGENTS.md` §7 표대로 바꾼다.
- cron은 macOS 「전체 디스크 접근 권한」에 `/usr/sbin/cron`이 있어야 `~/Documents`를 읽는다(`AGENTS.md` §5).
- ⛔ 옮긴 작업은 Claude 쪽 예약을 끈다 — 둘이 같은 DB에 겹쳐 쓴다.

## Codex에서 안 되는 것 · 대체

| 안 되는 것 | 대체 |
|---|---|
| 하위 세션 · `ship.py --collect` | 한 세션에서 순서대로. Claude 부모 세션이 모으는 중이면(`db/.leases/collector.json`) ship하지 않는다 |
| 대화 속 히트맵 위젯(불변규칙 8) | Codex `visualize` 플러그인 또는 HTML + `scripts/serve.sh` |
| Claude 브라우저 패널 | Playwright 스크립트 · Codex Chrome 플러그인 |
| Claude 자동 메모리 | 요지를 `AGENTS.md` §9에 옮겨 둠 |
