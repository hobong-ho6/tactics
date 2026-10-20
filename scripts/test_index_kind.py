#!/usr/bin/env python3
"""영상 종류 판정 회귀 시험 (2026-10-20 · 「감독 회견 7편이 실제로는 팬 반응 영상」 사고).

    .venv/bin/python scripts/test_index_kind.py      # 실패하면 exit 1

index_transcripts.guess_kind의 「감독회견」 패턴을 넓히거나 좁힐 때 반드시 돌린다 —
실제로 오분류됐던 제목과, 그걸 고치다 거꾸로 깨졌던 제목(공식 채널 감독 Reaction)을 함께 고정한다.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from index_transcripts import guess_kind  # noqa: E402

CASES = [  # (제목, 채널, 기대)
    ("Toothless Performance | Newcastle United 0-1 Aston Villa | Match Reaction", "GallowgateShots - NUFC", "경기반응"),
    ("Match Reaction | Newcastle 0 - 1 Aston Villa | Manzambi Dagger", "Penno | Aston Villa", "경기반응"),
    ("JOAO GOMES UPDATE | UNAI EMERY PRESS CONFERENCE REACTION", "UTV | Aston Villa Fan Channel", "경기반응"),
    ("POST-MATCH LIVE | With Alan McInally, Ian Taylor and Ross Barkley", "Aston Villa Football Club", "경기반응"),
    ("Alonso Press Conference | 16/10/26", "Chelsea Football Club", "감독회견"),
    ("SIMEONE rueda de prensa completa tras el ATLÉTICO", "Diario AS", "감독회견"),
    ("Pressekonferenz nach LASK - FC Liverpool", "LASKOfficial", "감독회견"),
    ("Oliver Glasner's Reaction", "NFFC 공식", "감독회견"),
    ("Iraola's Reaction: Anfield atmosphere, Barcola fitness", "Liverpool FC", "감독회견"),
    ("\"FANTASTIC NIGHT!\" | Unai Emery on 6-0 win against Fenerbahçe", "Aston Villa Football Club", "감독회견"),
    ("FENERBAHÇE 0 – 6 ASTON VILLA | MAÇ ANLATIMI VE TAKTİK ANALİZ", "Dr. Hikmet Taflan", "전술분석"),
]

bad = [(t, c, e, guess_kind(t, channel=c)) for t, c, e in CASES if guess_kind(t, channel=c) != e]
for t, c, e, got in bad:
    print(f"❌ {t[:60]} ({c}) — 기대 {e} · 실제 {got}")
print(f"{'✅' if not bad else '⛔'} 영상 종류 판정 {len(CASES) - len(bad)}/{len(CASES)}")
sys.exit(1 if bad else 0)
