# AC 밀란 — 26/27 전술 개요 · FC27 구현 · 베스트 11 (2026-11-18)

> 사용자 지시 「ac밀란도 동일하게 데이터 수집해서 추가해줘」(본머스·브라이턴과 같은 범위 — [선례](2026-11-18-opponents-bou-bha-che.md)).
> 범위: 개요 수준 + DB 상대 팀 등록(migration 136) + 베스트 11 FotMob 지표. ⚠️ 선수 실측(히트맵)은 수집하지 않아 적합도가 없다.
> 근거 등급(불변규칙 12): **C** = 실측 수치 기반 · **D** = 서술 해석 추론. 칸별 역할은 전부 D다.
> 조사: 서브에이전트(이탈리아어·포르투갈어(감독 모국어)·영어) · 선수 id·국적은 FotMob 스쿼드 API(2026-11-18).

## 한눈에 보기

| 항목 | 값 |
|---|---|
| 감독 | **후벵 아모림** — 2026-06-16 선임(알레그리 경질 · 맨유는 2026-01 경질) · 계약 2028/2029 출처 갈림 |
| 순위 | 세리에 A 11라운드 **4위** 승점 24(7승 3무 1패 · 23득점 13실점, 11-08) · 더비 3-1 승(10-31) |
| 유로파리그 | 1승 3패 28위 — **본머스 원정 0-3(10-22)** 포함 |
| 형태 | 8~9월 3-4-2-1 → 10-11부터 백4(표기 4-4-1-1). 보유 시 모드리치가 내려가 3-4-2-1, 리드 시 5-2-3 |
| FC27 팀 설정 | **4-2-3-1 Wide · Short Passing · Balanced · 58** |

## 전술 특성

- **빌드업**: GK부터 짧게, 점유로 압박을 유인한 뒤 수직 패스. 점유율 리그 3위인데 **공격 3선 터치는 뒤에서 2위**(Sky 10-31) — 최대 약점.
  Ultimo Uomo 「Nessuno correva dietro ai difensori.」(아무도 수비수 뒤로 뛰지 않았다 · 벤피카전 09-17).
- **압박**: **PPDA 11.25 리그 5위**(Corriere dello Sport 인용 · 9월 말 — 11월 갱신치 없음) → Balanced 구간(C). 볼이 측면으로 가면 여럿이 올라가는 측면 트랩 · 중앙이 빈다. 스프린트 경기당 120.2회 리그 1위(9월).
- **라인**: 초반 높고 리드 뒤 약 4m 내린다 → 전방 3과 후방 5 사이가 벌어진다.
- **패턴**: 오른쪽 라비오 + 모레이라 조합(더비 지배) · 풀리식 10번 = 압박 첫 줄.
- **약점**: 라인 뒤 칩 패스 · 측면 2대1 · 세트피스 수비 · 후반 체력 저하 · 레프트백 불안.
- **감독 발언**:
  - 「Com 4, ficamos mais abertos e os médios podem avançar mais, por isso experimentámos uma nova solução.」(백4면 우리가 더 열리고 미드필더가 더 전진할 수 있다, 그래서 새 해법을 시험했다 · Bola na Rede 10-11 — 이탈리아어 인터뷰의 포르투갈어 2차 표기)
  - 「la difesa a quattro è uno strumento per vincere le partite」(백4는 경기를 이기기 위한 도구다 · DAZN Italia 10-10)

## FC27 구현안

| 항목 | 값 | 등급 |
|---|---|---|
| 포메이션 | 4-2-3-1 Wide (표기 4-4-1-1과 칸 구성 동일 · 대안 3-4-2-1) | C(선발 표기)/D |
| 빌드업 | Short Passing (마무리 진입 약점 → Balanced도 검토) | C/D |
| 수비 접근 · 라인 | Balanced · 58 | C(PPDA) · D(라인) |

| 칸 | 역할 · 포커스 | 선수 | 메모 |
|---|---|---|---|
| GK | 스위퍼 키퍼 · Build-Up | 메냥 | 짧은 빌드업 · 라인 뒤 커버 |
| RB | 풀백 · Defend | 질라 | 안으로 좁혀 백3 |
| RCB | 스토퍼 · Balanced | 데 빈터 | 측면 트랩 때 전진 수비 |
| LCB | 볼 플레잉 센터백 · Build-Up | 파블로비치 | 왼발 |
| LB | 풀백 · Balanced | 디아와라 | 대안 무사 |
| LDM | 딥라잉 플레이메이커 · Defend | 모드리치 | 내려가 백3 형성 |
| RDM | 박스 크래셔 · Balanced | 라비오 | 리그 5골 · 2선 침투 |
| CAM | 섀도 스트라이커 · Attack | 풀리식 | 4골 · 압박 첫 줄 |
| RM | 인사이드 포워드 · Attack | 모레이라 | 왼발 오른쪽 · 4골 |
| LM | 인사이드 포워드 · Balanced | 알파조 시세 | 리그 5골 |
| ST | 어드밴스드 포워드 · Attack | 곤살루 하무스 | 내려와 받기 + 배후 · 득점력 지적 |

- 결장: 살레마커르스(발목 수술 · 2027 복귀) · 추쿠에제 · 토모리(햄스트링 · 11월 말 목표) · 로프터스치크 · 가비아. 로테이션: 무사 · 허친슨 · 자샤리 · 바르테사기 · 에스투피냔.

## 빌라 관점

| 볼 것 | 내용 |
|---|---|
| 마주칠 일 | 이번 시즌 빌라와 공식전 일정 없음 — 본머스가 10-22 유로파에서 3-0으로 이긴 상대(비교용) |
| 공략점 | 리드 뒤 내려앉아 벌어지는 3선-5선 간격 · 레프트백 쪽 측면 2대1 |

## 출처

- AC Milan 공식 제노아전 선발 2026-11-08 — https://www.acmilan.com/en/news/articles/serie-a/2026-11-08/genoa-vs-ac-milan-the-official-line-ups
- Sky Sport 순위·제노아전·더비 분석 2026-11-08 / 10-31 — https://sport.sky.it/calcio/serie-a/classifica-serie-a-2026-2027 · https://sport.sky.it/calcio/serie-a/partite/2026/giornata-11/genoa-milan/risultato-gol · https://sport.sky.it/calcio/serie-a/2026/10/31/milan-inter-derby-analisi-tattica-video-sky-tech
- Ultimo Uomo 2026-09-17 — https://ultimouomo.com/milan-benfica-amorim-pressing-atteggiamento-tattico-europa-league
- SempreMilan 더비 분석 — https://sempremilan.com/tactical-analysis-ac-milan-3-1-inter
- Pianeta Milan 11-01 · 부상 — https://www.pianetamilan.it/stagione/serie-a-news-e-risultati/amorim-spiega-la-svolta-tattica-del-derby-milan-inter-3-1-le-sue-parole/ · https://www.pianetamilan.it/news-milan/infortuni/infortunati-milan-le-ultime-su-pavlovic-tomori-loftus-cheek-e-gabbia/
- Milanisti Channel 09-24(PPDA) — https://www.milanistichannel.com/news-milan/con-amorim-si-pressa-il-dato-che-premia-e-sorprende-il-milan/
- DAZN IT 10-10 — https://www.dazn.com/it-IT/news/calcio/amorim-conferma-il-cambio-modulo-del-milan-anche-de-winter-approva/bk4urnw423c91av2x65p3ze8w
- Gianluca Di Marzio 11-08 — https://www.gianlucadimarzio.com/news-calcio/amorim-intervista-prepartita-genoa-milan-serie-a-8-novembre-2026-499297
- TMW 10-25 — https://www.tuttomercatoweb.com/serie-a/udinese-milan-formazioni-ufficiali-amorim-sorprende-diawara-1-2287190
- Bola na Rede 10-11 — https://bolanarede.pt/especial-bola-na-rede/atualidade/ruben-amorim-aborda-mudanca-para-linha-de-4-e-reage-ao-empate-do-ac-milan-nao-podemos-estar-satisfeitos-nao-podemos-perder-pontos-desta-forma/
- A Bola 06-15(선임) — https://www.abola.pt/noticias/rafael-leao-e-outras-duvidas-como-sera-o-milan-de-ruben-amorim-2026061516160993130
