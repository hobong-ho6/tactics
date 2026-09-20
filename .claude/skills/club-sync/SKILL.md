---
name: club-sync
description: 내 얼티밋 구단 동기화 — fut.gg GG Club에서 현재 스쿼드·보유 카드·케미 스타일·진화 상태를 읽어 원장(fut_*)에 반영하고, 신규 카드 수집·케미 재계산·커밋까지 닫는다. /club-sync로 실행.
---

# fut.gg 구단 동기화 런북 (2026-09-19 신설, 사용자 지시 「스쿼드 동기화를 match-watch처럼 스킬로」)

작업 디렉터리: 저장소 루트. DB `db/tactics.db`. 규칙은 CLAUDE.md·HANDOFF.md.

## 0. 전제 — 로그인·싱크는 **사용자 몫**

- ⛔ **로그인 대행 금지.** fut.gg·EA 아이디/비밀번호 입력, 로그인 버튼 클릭, EA 접근 허용 클릭을 하지 않는다.
- 로그인이 안 돼 있으면 **사용자에게 요청하고 멈춘다**: 「브라우저 패널에서 fut.gg에 로그인해 주세요. 끝나면 알려주세요.」
- EA 구단 자동 수집은 FC Community API 승인 파트너 전용이라 우리가 직접 호출하지 않는다. **GG Club 페이지는 읽기만** 한다.
- ⭐ 「Sync Club」·「Refresh Now」 버튼은 **사용자 계정에 작업을 거는 동작**이다 — 누르기 전에 **승인을 받는다**
  (이번 세션에서 이미 「눌러줘」를 받았으면 그대로 진행하고, 아니면 물어본다).

## 1. 게이트

`python3 scripts/gates.py` 통과 확인. 실패면 중단하고 원인만 보고한다.

## 2. 브라우저로 GG Club 읽기 (in-app 브라우저)

1. `mcp__Claude_Browser__navigate` → `https://www.fut.gg/gg-club/my/players/`
2. 로그인 상태 확인 — 클럽이 안 보이면 §0대로 사용자에게 요청.
3. 최신화가 필요하면 「Sync Club」(또는 「Refresh Now」) 클릭 → **6~8초 대기**.
   ⚠️ 누른 직후 바로 읽으면 이전 데이터가 온다. 버튼 라벨이 `Sync Club` → `Refresh Now`로 바뀌면 반영된 것이다.
   ⚠️⚠️ **싱크에는 쿨다운이 있다**(2026-09-20 실측). 직전 싱크 뒤 약 **15분**은 버튼이 **아예 사라지고** 본문에 
   「**Available in N minutes**」만 뜬다. ⇒ 같은 회차에 두 번 싱크할 수 없다. **쿨다운이면 기다리거나 다음 회차로 넘긴다** — 
   ⛔ 버튼이 없다고 「로그인이 풀렸다」로 오판하지 말 것.
   ⭐ **읽기는 쿨다운과 무관하다** — 선수 목록·플레이스타일 조회는 언제든 되고, 마지막 싱크 시점의 값을 준다.
   ⭐ 버튼은 **뷰포트 1280px 이상**에서만 보인다(`max-xl:!hidden`). 좁으면 DOM에 있어도 크기가 0이라 클릭이 안 된다.
4. `fetch` 훅을 설치하고 **페이지를 전부 넘겨** 응답을 모은다(30장/페이지):
   ```js
   window.__c=[]; const of_=window.fetch;
   window.fetch=async(...a)=>{const r=await of_(...a); try{const u=(typeof a[0]==='string'?a[0]:a[0].url)||'';
     if(u.includes('/api/gg-club/players')) window.__c.push(await r.clone().json());}catch(e){} return r;};
   // 페이지 버튼(1,2,3…)을 2~3회 순회하며 2.5초씩 대기 → 중복 제거
   ```
   ⚠️ 한 번 순회로는 누락된다(실측). **같은 페이지를 두 번 이상** 밟아 unique 수가 더 안 늘 때까지 돈다.
5. 활성 스쿼드는 별도다: `/gg-club/my/squads/` → `/gg-club/my/` 로 SPA 이동하면
   `/api/gg-club/active-squad/`가 다시 불린다. `activeGroupPositions`에서 `positionIdx ↔ playerEaId`를 받는다.
   슬롯 순서(f4231a): `0 GK · 1 RB · 2 CB · 3 CB · 4 LB · 5 CDM · 6 CDM · 7 RM · 8 LM · 9 CAM · 10 ST` (우→좌).

## 3. 원장 반영

1. 캡처를 `[{"ea","n","ovr","six":[6],"cs","cp","gg","added","paid"}, …]` 형태로 `/tmp/ggclub-YYYYMMDD.json`에 저장.
2. `.venv/bin/python scripts/fut_club_sync.py /tmp/ggclub-YYYYMMDD.json --account main`
   - 신규는 추가, 기존은 OVR·6대 스탯·케미 스타일·개인 케미 갱신.
   - ⭐ **EA에 없는 보유 행은 「판 것」으로 보고 처분한다**(2026-09-20 사용자 지시 「판 선수는 확인 안 하고 없으면 업데이트하면 될 것 같고」).
     ⛔⛔ **단 예외가 하나 있다 — `fut_evolution_log`가 걸린 선수는 절대 자동 처분하지 않는다.**
     근거는 사용자 규칙이다: **「진화한 선수는 판매하지 않는다」.** 즉 진화 선수가 EA 목록에서 사라졌다면 그것은 매각이 아니라
     **다른 사정**(시장 등록·SBC 투입·일시적 누락)이고, 지우면 진화 이력까지 잃는다. ⇒ 그 경우만 **목록을 내고 사용자에게 확인**받는다.
     ⭐ 실증(2026-09-20): 맥긴이 EA 목록에서 빠졌는데 사용자가 「다시 스쿼드에 넣어둘 것」이라 해 보존했다 — 없다고 다 판 게 아니다.
   - ⭐ 「진화 완주로 보이는 선수」 보고가 뜨면 `fut_club.py complete`로 닫되, **어떤 진화였는지는 사용자에게 확인**한다
     (fut.gg는 경로를 주지 않는다 — 「GG Club tracks your players' final stats, but not the evolution path that created them.」).
     ⭐⭐ **단계는 3중 대조로 읽는다**(2026-09-20 실증 · obs#900): ⑴ **아이템 접미 `-N` = N단계 완료** ⑵ 6대 스탯 변화
     ⑶ 카탈로그 단계별 보상. 하나만 보면 단계가 어긋난다 — 09-19에 3단계를 4단계로 적은 사고가 이 대조로 잡혔다.
3. 활성 스쿼드 슬롯을 `fut_squad_slots`에 반영(11명 + 교체). 포메이션·감독 국적/리그가 바뀌었으면 `fut_squads`도 갱신.
4. 새로 들어온 카드가 있으면 `.venv/bin/python scripts/collect_futgg_cards.py --games 27`
   (국적·리그·클럽·29속성·심플카드 URL이 이때 채워진다 — 이게 없으면 케미·추천 계산에서 빠진다).

## 4. 완료 절차

`python3 scripts/gates.py` → `python3 scripts/export.py` → `scripts/db_dump.sh` →
`git add db/tactics.db db/dump/ site/data/ && git commit -m "data(fut): GG Club 싱크 YYYY-MM-DD — 신규 N·갱신 M" && git push`
⚠️ `git add -A` 금지 — 명시 스테이징만.

## 5. 종료 보고 (이 형식으로)

- **보유**: 총 N명(빌라 M명) · 신규 K명(이름·OVR) · 사라진 행 L명(**처분 여부 사용자 확인 요청**)
- **선발 XI**: 슬롯별 11명 + **팀 케미 n/33**. 직전과 달라졌으면 바뀐 자리를 짚는다.
- **케미 스타일**: 새로 붙인 것 / 우리 추천과 갈리는 칸.
- **진화**: 완주 추정·진행 중 목록.
- **화면 확인**: 진화·내 구단 → 케미스트리 탭에서 「지금 쓰는 스쿼드」가 갱신됐는지.

## ⭐⭐ 진화 적용 결과는 **EA 실측으로 더블체크**한다 (2026-09-20 실증)

⛔ **`player_evolutions.path_json`(fut.gg 계산 결과 카드)을 실측 대신 쓰면 틀린다.** 이미 두 부류로 터졌다:
- **OVR**: 루제리 카탈로그 표기 83 ↔ EA 실측 **80**(2026-09-19).
- **PlayStyle**: 루제리에 **Inventive**가 잘못 들어갔고(EA는 Whipped Pass+Jockey뿐), Alysson은 반대로 **두 개가 통째로 비어 있었다**
  (EA 실측 First Touch + Pinged Pass = 반복 배급 2·3단계 보상).

⇒ **검증 절차**: GG Club API `playerDef.playstyles` / `playstylesPlus`는 **숫자 id**로 온다.
id→이름 표는 fut.gg 웹앱 번들에서 받는다(케미 스타일과 같은 경로) — `e[e.NAME=ID]=\`NAME\`` 열거형 + `[P.NAME]:\`Label\`` 라벨표를 짝지으면 된다.
확인된 값 일부: `6 핑드 패스 · 9 휘핑 패스 · 10 자키 · 11 블록 · 12 인터셉트 · 13 앤티시페이트 · 14 슬라이드 태클 · 17 래피드 · 19 퍼스트 터치 · 37 게임 체인저 · 38 인벤티브`.
⭐ **기준 카드(`player_card_items.playstyles`)와 대조하면 「어디까지가 진화분인가」가 갈린다** — 루제리는 기준 Whipped Pass + 진화 Jockey로 EA가 완전히 설명됐다.

## ⭐ 진화 소진 규칙 (2026-09-20 사용자 지시)

**한 계정에서 쓴 진화는 다른 선수가 쓸 수 없다.** 반복형은 `repeatability` 횟수만큼만 쓸 수 있고, 그 횟수를 채우면 **소진**이다.
⇒ 소진된 진화는 **카탈로그·선수별 경로·전술 구현 탭 전부에서 빠지고** 각 선수의 최적 패스가 다시 매겨진다(`site/evolutions.html` `consumedMap`).

⛔⛔ **세는 단위는 「적용 횟수(run)」이지 로그 행 수가 아니다** — 2026-09-20에 이 둘을 혼동한 버그를 고쳤다:
- **1단계 행(`level=1`)만 센다.** 반복 배급은 4단계짜리라 한 번 밟아도 행이 4개 쌓인다 — 그대로 세면 1회가 4회가 되어 `repeatability=2`짜리가 첫 선수만으로 잠겼다.
- **`is_void=1` 행은 세지 않는다**(migration 053). 마조 Striker Glow Up은 실측으로 「적용된 적 없음」이 확인됐는데도 소진으로 잠겨 있었다.
- ⭐ **진행 중(`completed_at IS NULL`)도 센다** — 카드가 이미 그 경로에 묶였기 때문이다.

## 하지 말 것

- 로그인·EA 연동 대행, 비밀번호 입력 (§0)
- **진화 로그가 걸린 보유 행의 자동 삭제**(§3 예외), 진화 경로 추정 기입
- 처방·역할 가중 변경(그건 사용자 판단 사안이다)
- HANDOFF.md 갱신(사실 적재 회차라 불필요 — 구조가 바뀌었을 때만)
