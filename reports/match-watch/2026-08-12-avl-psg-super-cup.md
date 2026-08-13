# 2026-08-12 UEFA Super Cup — PSG 2-1 Aston Villa

> 수집일 2026-08-13 · SofaScore event `16260286` · 중립 경기 · 빌라 4-2-3-1

## 실측

- 빌라 점유율 **39%**, 슈팅 **15-12**, 유효슈팅 **4-6**, 빅찬스 **5-3**, 패스 **368-588**.
- 득점 국면: 0-0 20분 → 0-1 열세 25분 → 1-1 16분 → 1-2 열세 29분.
- 45분 이상 출전한 11명을 `player_matches`에 적재했다. 전원 평균 위치·히트맵·개별 스탯이 있고
  히트포인트 최저도 **33**이라 경기 단위 그리드로 유효하다.
- Brian Madjo는 72분, 1골, 6슈팅, 2키패스. John McGinn은 73분, 1도움, 4키패스.

| 선수 | 라인업 슬롯 | 평균 위치 기반 분류 | 평점 | 핵심 |
|---|---:|---:|---:|---|
| Marco Bizot | GK | GK | 6.6 | 4선방 |
| Matty Cash | RB | RB | 6.6 | 우측 수비 |
| Victor Lindelöf | RCB | RCB | 6.4 | 중앙 보호 |
| Pau Torres | LCB | LCB | 7.0 | 79분 |
| Ian Maatsen | LB | LB | 7.0 | 좌측 폭·전진 |
| Boubacar Kamara | RDM | RDM | 6.4 | 더블 피벗 |
| João Gomes | LDM | LDM | 6.1 | 더블 피벗 |
| John McGinn | RAM | RM | 7.1 | 우측 창출, 4키패스·1도움 |
| Emiliano Buendía | CAM | LDM | 6.3 | 명목 CAM이나 평균 위치는 중앙·낮음 |
| George Hemmings | LAM | LDM | 6.2 | 순수 윙어보다 좌측 하프스페이스 |
| Brian Madjo | ST | ST | 6.6 | 정통 9번·물리적 출구, 1골 |

`lineup_pos`는 실제 라인업 배열을 4-2-3-1 우→좌 순서로 사상한 원천 배치이고,
`pos_class`는 평균 위치 기반 사후 분류다. 둘이 다른 Buendía·Hemmings는 오류로 덮지 않고 나란히 보존한다.

## 전술 판정

- 명목 구조 `McGinn RAM — Buendía CAM — Hemmings LAM — Madjo ST`와
  `Kamara/Gomes` 더블 피벗은 확인됐다. 다만 세 공격형 미드필더는 유동적이었다.
- [El País 경기 분석](https://elpais.com/deportes/futbol/2026-08-12/el-psg-extiende-su-hegemonia-tras-vencer-la-supercopa-de-europa-ante-el-aston-villa.html)
  (2026-08-12)은 빌라가 중앙을 좁게 보호하고 전방에서 센터백을 압박한 뒤 짧고 직접적으로 전환했다고 서술한다.
- [AS의 Emery 경기 후 문답](https://as.com/futbol/internacional/unai-emery-habra-mas-cambios-f202608-n/)
  (2026-08-12)에서 Emery는 Madjo와 Hemmings를 해당 포지션에 맞춰 준비시켰다고 확인했다.
  따라서 두 선수의 배치는 라인업 표기 오류가 아니라 의도된 선택이다.
- Madjo는 등지고 연결하는 물리적 출구와 박스 침투를 함께 맡았고, McGinn은 오른쪽 하프스페이스에서
  반복적으로 공급했다. 경기 단위 FC 적합은 McGinn RM `wm_winger/Attack` **.882**,
  Madjo ST `st_poacher/Attack` **.725**다. 한 경기 값이므로 대표 적합으로 승격하지 않는다.

## obs#134~136 검증

- **obs#134 지지**: 자연 우측 윙어 대신 McGinn을 RAM에 세워 임시 해결했다. 그의 평균 y=15.81은
  실제로 강한 우측 편향이고 4키패스·1도움으로 기능했지만, 전문 우측 자원 영입 필요를 반증하지 않는다.
- **obs#135 검증 불가**: Endrick이 출전하지 않아 우측 적합성이나 9번 조건에 새 근거가 없다.
- **obs#136 검증 대상 아님**: 이 경기는 빌라의 수요만 보여줄 뿐 협상 단계·선수 의사를 말하지 않는다.

팬 관찰은 [r/avfc 경기 후 스레드](https://www.reddit.com/r/avfc/comments/1vmqcwz/post_match_thread_psg_21_aston_villa_uefa_super/)
(2026-08-12)에서 교차 확인했다. Madjo/Hemmings, McGinn, Kamara/Gomes 조합 호평은 반복됐지만
위치 판정에서는 SofaScore 원천값과 감독 발언보다 낮은 우선순위로만 사용했다. 경기 전 Reuters 기자회견은
영상 전체를 검토하지 못해 근거로 채택하지 않았다. 전문 전술 블로그·경기 후 전술 유튜브는 수집 시점에
검색되지 않아 미수행으로 남긴다.

## 데이터 출처와 한계

- SofaScore `/event`, `/lineups`, `/statistics`, `/incidents`, `/average-positions`,
  `/player/{id}/heatmap`, `/player/{id}/statistics`를 동일 오리진 Playwright 수집기로 사용했다.
- SofaScore가 이 경기 xG를 양 팀 모두 `0.00`으로 제공해 `team_match_stats.xg_v/xg_o`도 원천값 그대로 0이다.
  이를 실제 무위험 경기라는 뜻으로 해석하면 안 된다(빅찬스는 빌라 5, PSG 3).
- Madjo의 유효 표본은 이 경기 포함 **4경기**라 대표 역할 최소 기준 6경기에 아직 미달한다.
