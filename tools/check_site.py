"""Controleert alle HTML-pagina's: sluitende tags, interne links, afbeeldingsgroottes."""
import os, sys, html.parser, glob
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
VOID = {"meta", "link", "img", "br", "hr", "input", "source", "path", "rect", "circle"}
errors = []

class Checker(html.parser.HTMLParser):
    def __init__(self, path): super().__init__(); self.stack = []; self.path = path; self.hrefs = []
    def handle_starttag(self, tag, attrs):
        if tag not in VOID: self.stack.append(tag)
        for k, v in attrs:
            if k in ("href", "src") and v: self.hrefs.append(v)
    def handle_startendtag(self, tag, attrs):
        for k, v in attrs:
            if k in ("href", "src") and v: self.hrefs.append(v)
    def handle_endtag(self, tag):
        if tag in VOID: return
        if self.stack and self.stack[-1] == tag: self.stack.pop()
        else: errors.append(f"{self.path}: </{tag}> zonder open tag (stack {self.stack[-3:]})")

for page in sorted(glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True)):
    if "/.superpowers/" in page or "/docs/" in page: continue
    rel = os.path.relpath(page, ROOT); base = os.path.dirname(page)
    c = Checker(rel); c.feed(open(page).read())
    if c.stack: errors.append(f"{rel}: niet gesloten: {c.stack}")
    for h in c.hrefs:
        if h.startswith(("http", "mailto:", "#", "data:")): continue
        target = h.split("#")[0].split("?")[0]
        if not target: continue
        p = os.path.join(ROOT, target.lstrip("/")) if target.startswith("/") else os.path.join(base, target)
        if not os.path.exists(p): errors.append(f"{rel}: dode link {h}")
for img in glob.glob(os.path.join(ROOT, "img", "*.jpg")):
    kb = os.path.getsize(img) // 1024
    if kb > 200: errors.append(f"{os.path.relpath(img, ROOT)}: {kb} KB > 200 KB")
for e in errors: print("FOUT", e)
print("OK" if not errors else f"{len(errors)} fouten"); sys.exit(1 if errors else 0)
