# FC27 갤러리 — 커뮤니티 자료·세트 조사 (2026-10-03)

사용자 지시: 「갤러리쪽은 커뮤니티 자료나 커뮤니티에 돌아다니는 갤러리 세트들 참고해서 업데이트」.
정본 계산식은 `core/gallery.py`(tag_bonus)이고, 이 문서는 그 근거다. DB 기록은 `game_system_changes` #36(인게임 실측)·#37(이 조사)이다.

## 1. 근거 등급

| 근거 | 등급 | 내용 |
|---|---|---|
| 인게임 태그 용어집·세트 캡처 36장(사용자 PS 리모트) | A·C | 12종 태그 단계 원문(A). 아스톤 빌라 544점·스타터 4,113점을 1점 단위로 재현(C) |
| fut.gg 세트 페이지에 내장된 EA 형식 태그 정의(`capturedAt 2026-09-27`) | B | 21종 rules·tiers. 인게임으로 확인한 12종과 전부 일치 → 나머지 9종의 근거 |
| fut.gg 계산기 최적 조합 16건 | B− | 태그별 bonus = floor(pct×matchedScore) 전 건 일치. top-10 컷 9건 1점 단위 일치 |
| EA 피치노트 FUT 딥다이브(2026-08-02)·도움말 | A | 판매·SBC로 나간 아이템도 계속 집계, 임대 아이템 제외, 진화 아이템은 진화 전 원본 |
| timesaver·Red Bull·Prima·iGamesZone·mmoexp·futgenie 등 | — | fut.gg 표를 옮긴 것이라 **독립 출처가 아니다**. futgenie도 「fut.gg 계산을 정확히 재현한다」고 직접 밝힘 |
| 다국어 검색(독·스·이·프·한·일) | — | 현지 매체가 자체적으로 쓴 수치 0건. 인벤은 출시 기사만 있음 |

## 2. 반영한 규칙 (core/gallery.py)

1. **「다른 ○○」**: 서로 다른 값의 개수로 단계를 정한다. 보너스는 **값마다 점수가 가장 높은 카드 1장씩의 합**에만 붙는다(B). 종전에는 전체 카드에 붙여 과대 추정했다.
2. **「같은 ○○」**: 가장 큰 무리 하나에 붙는다. 동률이면 점수 합이 큰 쪽이다(B).
3. **「중복!」**: 같은 BASE_DEF_ID 중 **가장 큰 묶음 하나**에만 붙는다(B). 종전에는 중복된 카드 전부에 붙였다.
4. **가장 큰 태그 10개만 반영**: fut.gg 계산기 구현이다(B−). 인게임 프리미어 리그·라리가 화면에도 태그 칩이 정확히 10개였다.
5. **TOTW**: rarity 3(`RARE 3`) 기준이다. Iconic은 RARE 12, Heroic은 RARE 72다(B).
6. **Skilled·Ambidextrous**: 3–4 / 5–9 / 10+ 구간이며 우리 값과 같다. Red Bull의 3–5 / 6–9는 잘못 옮긴 값으로 본다(B).

## 3. 재현 검증

### fut.gg 계산기 16건
- 15건이 태그별 bonus까지 일치했다(top-10 컷 포함).
- 개인기·약발·홀로그램은 표본에 데이터가 없어 비교에서 뺐다.
- 불일치 1건은 히어로 세트다. fut.gg는 히어로를 모두 clubEaId 114605로 보아 「같은 클럽」을 건다. 인게임에서 확인되지 않아 반영하지 않았다.

### 인게임 스냅숏 6세트

원장 밖 카드는 퍼스트 오너로 가정했다.

| 세트 | 차이 |
|---|---|
| 아스톤 빌라 | 0 |
| 스쿼드 기초 | 0 |
| 스타터 세트 | +0.6% |
| 세리에 A | −2.1% |
| 프리미어 리그 | +4.0% |
| 라리가 | +10.5% |

남은 차이는 원장 밖 카드의 퍼스트 오너 여부를 모르기 때문으로 본다.

## 4. 미확인 — 인게임 캡처로 확정할 것
- **Different League 5–9장 구간이 1%인지 2%인지**: timesaver 스타터 S 캡처에서 167점(base의 1%)이 설명되지 않는다. 안 보이는 「다른 클럽」 1% 때문일 가능성도 있다.
- **히어로 카드의 클럽 처리**: 114605로 묶여 「같은 클럽」이 걸리는가.
- **홀로그램 태그**: 우리 원장에 홀로그램 여부가 없어 계산에서 뺐다. fut.gg 아이템의 hyper-cosmetic 값으로 채울 수 있다.
- **아이템 점수 배율(커뮤니티 역산 · D)**: 64 이하는 20, 65–74는 35, TOTW·히어로 등은 골드 기준 ×1.25, 아이콘 ×2.25(?), 홀로 ×1.5. 우리는 fut.gg `gradingScore`를 그대로 쓰므로 계산에 영향이 없다.

## 출처
- [fut.gg 갤러리](https://www.fut.gg/fut-gallery/) · [fut.gg 태그](https://www.fut.gg/fut-gallery/tags/)
- [EA 피치노트 FUT 딥다이브](https://www.ea.com/games/ea-sports-fc/fc-27/news/pitch-notes-fc27-fut-deep-dive)
- [timesaver 태그](https://timesaver.gg/blog/fc-27-first-owner-gallery-tags-500-percent-bonus) · [timesaver 적격성](https://timesaver.gg/blog/fc-27-gallery-players-not-counting-eligibility-rules)
- [Red Bull](https://www.redbull.com/int-en/fc-27-ultimate-team-gallery-tags) · [futgenie](https://www.futgenie.gg/posts/fut-gallery) · [neuralboost](https://neuralboost.gg/blog/fc-27-fut-gallery-explained-item-score-and-sets)
- 접근 제한: Reddit 403, futbin·futwiz Cloudflare 403. 우회하지 않았다.
