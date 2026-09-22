#!/usr/bin/env python3
"""CSS 템플릿 리터럴 안에 백틱이 섞였는지 검사한다 (2026-09-22 신설).

왜: `site/assets/*.js`의 `export const XXX_CSS = \\`...\\`` 블록 주석에 코드 조각을 백틱으로 감싸는
실수를 **네 번** 했다(docs/70). 리터럴이 거기서 끝나 SyntaxError가 나고 **모듈 전체가 로드되지 않아**
화면이 통째로 먹통이 된다. 증상이 「문법 오류」가 아니라 「클릭이 안 된다」로 나타나 매번 오래 걸렸다.

사용: python3 scripts/check_css_literals.py   (실패 시 exit 1)
"""
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
bad = []
for f in sorted((ROOT / "site" / "assets").glob("*.js")):
    src = f.read_text(encoding="utf-8")
    for m in re.finditer(r"export const (\w*CSS) = `(.*?)\n`;", src, re.S):
        if "`" in m.group(2):
            line = src[:m.start()].count("\n") + 1
            bad.append(f"{f.relative_to(ROOT)}:{line} {m.group(1)} — 블록 안에 백틱")
print("CSS 리터럴 검사:", "⛔ " + " · ".join(bad) if bad else "✅ 이상 없음")
sys.exit(1 if bad else 0)
