# FC27 카드 버전 축 신설 — 새 카드가 나오면 보이게 (2026-09-14)

사용자 지시: 「관리중인 선수들의 FC27에서 새로운 카드가 나오면 그 카드 정보도 확인할 수 있도록 수집하고 보여주는 방법 —
fut.gg나 futbin 같은 사이트를 참고」.

관련 obs: **#739**.

---

## 1. 경로 — fut.gg `all-versions` 한 번이면 끝난다

```
GET https://www.fut.gg/api/fut/players/v2/all-versions/{basePlayerEaId}/     → 200 (curl, 브라우저 불필요)
```

한 응답에 그 선수의 **전 버전·전 카드**가 들어온다 — OVR·6대 스탯·34속성·PlayStyles(+)·**Role+/++**·
스킬무브·약발·AcceleRATE·주발·키·몸무게·`createdAt`(공개일)·카드 이미지 경로.
희귀도 이름만 없어서 목록 API로 보충한다:

```
GET https://www.fut.gg/api/fut/players/v2/{game}/?ea_ids=…   → rarityName · club · cardImageUrl
```

- 엔드포인트는 선수 페이지의 실제 네트워크 요청에서 확인했다(추측 금지).
- futbin은 403 계열이라 쓰지 않는다(기존 판단 유지) — fut.gg가 200이고 provenance가 소스에 붙어 있다.

## 2. 저장 — `player_card_items` (migration 030)

⛔ **`player_game_stats`에 섞지 않았다.** 그 표는 「그 선수의 **능력치 정본**」이고 키가
`(game_version, roster_date, name_kr)`다. 프로모를 거기 넣으면

1. 같은 날 카드가 두 장이면 **UNIQUE에 걸리고**,
2. 시즌 분석 질의(`roster_date='2026-09-10'`)가 **조용히 프로모 능력치를 집어간다.**

⇒ 카드 아이템은 카드 표에. base 카드도 같이 넣어 한 선수의 카드 목록이 한 곳에서 끝난다.

| | |
|---|---|
| 키 | `(game_version, ea_item_id)` — 프로모는 base와 다른 eaId를 받는다 |
| 판별 | `is_base` · `rarity_ea_id` · `rarity_name` · `released_at`(= `createdAt`) |
| 안전장치 | 응답의 `basePlayerEaId`가 우리 eaId와 다르면 **적재하지 않고 보고**(09-14 다트로↔웨슬리 포파나 오염 실증) |

**현재 적재: FC27 96장 — 전부 base. 특별 카드는 아직 0장**이고 출시(2026-09-25) 이후 등장한다.
파이프라인 자체는 FC26으로 검증했다(AVL 25장: TOTW·FUT Birthday·Showdown·Fantasy FC·FC Pro Live 등 정상 회수).

⭐ 부수 발견: **FC26 특별 카드에는 `rolesPlusPlus`가 채워져 있다** — 역할 숙련 필드는 API에 이미 있고
**FC27만 비어 있다**(EA 미공개 확인, docs/21 ②). ⛔ 그래도 raw id로만 적재한다 —
카탈로그 없이 id→이름을 발명하지 않는다.

## 3. 표시 — 선수 「게임 스탯」 탭 상단 **카드 버전** 패널

- 카드 이미지 · OVR · 포지션 · 희귀도 배지 · 공개일 · 6대 스탯 · 스킬/약발/AcceleRATE/PS 수 · fut.gg 링크.
- 특별 카드에는 **기본 카드 대비 OVR Δ 칩**이 붙는다.
- 특별 카드가 없으면 그 사실을 적는다 — 「특별 0 (아직 없음 — FC27 출시 2026-09-25 이후 등장)」.
- ⛔ 패널 설명에 **「특별 카드 수치를 분석에 쓰지 않는다」**를 명시했다(능력치 정본은 아래 「게임 스탯」).

## 4. 운용

```bash
.venv/bin/python scripts/collect_futgg_cards.py --games 27      # 새 카드 확인·추가 (재실행 안전)
```

- `ON CONFLICT(game_version, ea_item_id) DO NOTHING` — 이미 있는 카드는 건너뛴다.
- 출시 후에는 **주간 정기 실행**(match-watch와 같은 회차)에 넣는 것을 권한다 — 사용자 판단 대기.

## 5. 곁가지로 고친 것

`player.html`의 주발 표기가 `{Left, Right}`만 매핑하고 있어, 09-14에 주발을 채우자(fut.gg는 `왼쪽/오른쪽`)
전원 `—`로 보였다. 매핑에 한글 어휘를 추가했다.
