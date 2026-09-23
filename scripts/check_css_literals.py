#!/usr/bin/env python3
"""CSS를 JS 템플릿 리터럴에 담지 않았는지 검사한다 (2026-09-22 신설 · 2026-09-23 대상 교체).

왜: `site/assets/*.js`의 `export const XXX_CSS = \\`...\\`` 블록 주석에 코드 조각을 백틱으로 감싸는
실수를 **네 번** 했다(docs/70). 리터럴이 거기서 끝나 SyntaxError가 나고 **모듈 전체가 로드되지 않아**
화면이 통째로 먹통이 된다. 증상이 「문법 오류」가 아니라 「클릭이 안 된다」로 나타나 매번 오래 걸렸다.

⭐ 2026-09-23: **G22가 이 함수를 직접 부른다**(사용자 지시 「스크립트로 수행할 수 있는 것은 전환」).
   종전엔 검사기가 있는데도 **아무도 부르지 않아** 매 세션이 손으로 돌렸고, 잊으면 그대로 터졌다.
   ⇒ `scan()`을 import 가능하게 두고 `sys.exit`은 `__main__`에서만 한다(import 시 죽지 않게).

사용: python3 scripts/check_css_literals.py   (실패 시 exit 1)
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def scan():
    """위반 목록을 돌려준다(빈 리스트면 통과). ⛔ 여기서 종료하지 않는다 — 호출측이 판단한다.

    ⭐⭐ 2026-09-23에 검사 대상을 바꿨다: 종전엔 「CSS 리터럴 **안의** 백틱」을 찾았는데,
    그건 증상이지 원인이 아니었다(그래서 다섯 번 재발했다). 원인은 **CSS를 JS 문자열에 담는 것**이다.
    ⇒ 이제 `export const *CSS = ` 자체를 금지한다. CSS는 `.css` 파일로 두고 link로 건다 —
      거기서는 백틱이 그냥 글자라 이 사고가 **원리적으로 불가능**하다.
    ⚠️ 남아 있는 CSS 리터럴이 있으면 안의 백틱도 함께 잡는다(옮기기 전까지의 안전망)."""
    bad = []
    for f in sorted((ROOT / "site" / "assets").glob("*.js")):
        src = f.read_text(encoding="utf-8")
        for m in re.finditer(r"export const (\w*CSS) = `", src):
            line = src[:m.start()].count("\n") + 1
            bad.append(f"{f.relative_to(ROOT)}:{line} {m.group(1)} — CSS를 JS 템플릿 리터럴에 담았다. "
                       f".css 파일로 빼고 <link>로 걸 것(주석 속 백틱 한 글자에 모듈 전체가 죽는다)")
        for m in re.finditer(r"export const (\w*CSS) = `(.*?)\n`;", src, re.S):
            if "`" in m.group(2):
                line = src[:m.start()].count("\n") + 1
                bad.append(f"{f.relative_to(ROOT)}:{line} {m.group(1)} — 블록 안에 백틱")
    return bad


if __name__ == "__main__":
    bad = scan()
    print("CSS 리터럴 검사:", "⛔ " + " · ".join(bad) if bad else "✅ 이상 없음")
    sys.exit(1 if bad else 0)
