"""Vervangt nav en footer van de handgeschreven pagina's (support/privacy, 5 talen)
door de gedeelde chrome uit site_common, zodat de hele site één navigatie heeft."""
import os, re, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from site_common import nav, footer, LANGS, ORDER
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
for lang in ORDER:
    for page in ("support.html", "privacy.html"):
        path = os.path.join(ROOT, LANGS[lang]["dir"], page)
        if not os.path.exists(path): continue
        s = open(path).read()
        s2 = re.sub(r"<nav class=\"nav\">.*?</nav>", lambda m: nav(lang, current=page), s, count=1, flags=re.S)
        s2 = re.sub(r"<footer>.*?</footer>\s*(<script defer src=\"[^\"]*lang\.js\"></script>\s*)?", lambda m: footer(lang) + "\n", s2, count=1, flags=re.S)
        if s2 != s:
            open(path, "w").write(s2); print("chrome vervangen:", os.path.relpath(path, ROOT))
