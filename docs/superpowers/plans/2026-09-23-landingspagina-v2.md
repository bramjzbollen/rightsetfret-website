# Landingspagina v2 — implementatieplan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Een professionele app-landingspagina (stijl B) in 5 talen met verse app-schermen, gegenereerd uit één sjabloon, live op rightsetfret.studioplanb.be.

**Architecture:** Statische site zonder build-stap. `site_common.py` levert de gedeelde fragmenten (head, nav, footer, App Store-knop, telefoonkader); `gen_site.py` rendert de homepage per taal uit een `TEXT`-woordenboek; `gen_landing.py` (bestaand) gaat dezelfde fragmenten gebruiken. Eén nieuwe `styles.css` bedient alle pagina's; `reveal.js` doet de scroll-animatie. Spec: [`docs/superpowers/specs/2026-09-23-landingspagina-v2-design.md`](../specs/2026-09-23-landingspagina-v2-design.md).

**Tech Stack:** HTML5/CSS3, vanilla JS (IntersectionObserver), Python 3 (generators, `qrcode` voor de QR-SVG, Pillow voor de OG-afbeelding), `xcrun simctl` + `sips` voor schermen, GitHub Pages.

---

## Werkomgeving

- Repo-clone: `/private/tmp/claude-501/…/scratchpad/rightsetfret-website`, branch `feat/landingspagina-v2` (van `main`). Alle paden hieronder zijn relatief aan de repo-root.
- Lokaal bekijken: `python3 -m http.server 8765 --bind 127.0.0.1` in de repo-root → `http://127.0.0.1:8765/`.
- Simulator: "iPhone 17 Pro" `6482C714-0CA5-498B-9A73-C6AF35BB4C5F` met build 100 geïnstalleerd (`/Users/brambollen/Library/Application Support/Claude/simulator-builds/7806442f5dc7a739/DerivedData/Build/Products/Debug-iphonesimulator/Receptenboek.app`).
- App-repo (voor de deelmenu-asset): `/Users/brambollen/Documents/PRIVE/Develop/Recipe`.
- Commit na elke taak; push + PR aan het eind; mergen doet de gebruiker (deploy = live).

---

### Taak 1: Schermen uit de simulator

**Files:**
- Create: `tools/convert_shots.sh`
- Create: `img/recept.jpg`, `img/collectie.jpg`, `img/frigo.jpg`, `img/planning.jpg`, `img/lijstje.jpg`, `img/kookmodus.jpg`, `img/import.jpg`, `img/deelmenu.jpg`

- [ ] **Stap 1: Conversiescript**

```bash
#!/usr/bin/env bash
# Zet ruwe simulator-PNG's (1206×2622) om naar 780px brede JPEG's voor de site.
#   tools/convert_shots.sh <rawdir>
set -euo pipefail
RAW="$1"; OUT="$(dirname "$0")/../img"; mkdir -p "$OUT"
for f in "$RAW"/*.png; do
  n=$(basename "$f" .png)
  sips -s format jpeg -s formatOptions 82 --resampleWidth 780 "$f" --out "$OUT/$n.jpg" >/dev/null
  printf "%-14s %6d KB\n" "$n.jpg" $(( $(stat -f%z "$OUT/$n.jpg") / 1024 ))
done
```

`chmod +x tools/convert_shots.sh`.

- [ ] **Stap 2: Schermen vastleggen**

Start de app (schone staat is niet nodig; de voorbeeldrecepten staan erin). Per scherm: navigeer in de simulator, dan `xcrun simctl io 6482C714-0CA5-498B-9A73-C6AF35BB4C5F screenshot <rawdir>/<naam>.png`.

| bestand | scherm | hoe |
|---|---|---|
| `collectie.png` | Collectie met 4 recepten, **zonder** startkaart en zonder tutorial | startkaart × tikken, tours overslaan |
| `recept.png` | receptfiche "Steak tartaar met Belgische kaviaar" | tik op de kaart |
| `kookmodus.png` | kookmodus, stap 1 | op de fiche: knop "Kookmodus"/koksmuts |
| `frigo.png` | tab Frigo | tabbalk |
| `planning.png` | tab Planning | tabbalk |
| `lijstje.png` | tab Lijstje (met minstens één ingrediënt: op de fiche eerst 🛒 tikken) | tabbalk |
| `import.png` | sheet "Recept importeren" | + rechtsboven in Collectie |

`deelmenu.png` = kopie van `/Users/brambollen/Documents/PRIVE/Develop/Recipe/ios/Receptenboek/Assets.xcassets/tutorial-share-sheet.imageset/tutorial-share-sheet.png` (760×443, liggend; wordt in een `.shot-wide`-kader getoond i.p.v. een telefoon).

- [ ] **Stap 3: Converteren en controleren**

Run: `tools/convert_shots.sh <rawdir>` → 7 regels, elk ≤ 200 KB. `deelmenu.png` apart: `sips -s format jpeg -s formatOptions 85 <pad> --out img/deelmenu.jpg`.

- [ ] **Stap 4: Commit**

```bash
git add tools/convert_shots.sh img/
git commit -m "Verse app-schermen (build 100) voor de landingspagina"
```

---

### Taak 2: `site_common.py` — gedeelde fragmenten

**Files:**
- Create: `site_common.py`
- Test: `tools/test_site_common.py`

- [ ] **Stap 1: Falende test**

```python
import sys, os, re
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import site_common as sc

def test_store_link_has_campaign_and_mt():
    assert sc.store_link("web_home_nl") == "https://apps.apple.com/app/apple-store/id6784261188?ct=web_home_nl&mt=8"

def test_asset_prefix_root_vs_subdir():
    assert sc.asset("nl", "styles.css") == "styles.css"
    assert sc.asset("en", "styles.css") == "/styles.css"

def test_nav_marks_current_language():
    html = sc.nav("fr", current="index.html")
    assert 'hreflang="fr" aria-current="page"' in html
    assert html.count("<li>") == 5

def test_qr_svg_is_inline_svg():
    svg = sc.qr_svg("https://example.com")
    assert svg.startswith("<svg") and svg.rstrip().endswith("</svg>")

def test_head_contains_hreflang_for_all_languages():
    h = sc.head("nl", title="T", desc="D", path="index.html", alt={"nl": "index.html", "en": "en/index.html", "fr": "fr/index.html", "de": "de/index.html", "es": "es/index.html"})
    assert h.count('rel="alternate" hreflang=') == 6  # 5 talen + x-default
    assert '<link rel="canonical" href="https://rightsetfret.studioplanb.be/index.html">' in h

if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn(); print("ok", name)
```

- [ ] **Stap 2: Draaien** — `python3 tools/test_site_common.py` → `ModuleNotFoundError: No module named 'site_common'`.

- [ ] **Stap 3: Implementatie**

```python
"""Gedeelde bouwstenen voor alle pagina's van rightsetfret.studioplanb.be.
Gebruikt door gen_site.py (homepage) en gen_landing.py (landingspagina's)."""
import html, io
import qrcode, qrcode.image.svg

SITE = "https://rightsetfret.studioplanb.be"
APP_ID = "6784261188"
PIXEL_ID = "1018910594260070"

LANGS = {
    "nl": dict(dir="", code="NL", flag="🇳🇱", name="Nederlands", path="/"),
    "en": dict(dir="en/", code="EN", flag="🇬🇧", name="English", path="/en/"),
    "fr": dict(dir="fr/", code="FR", flag="🇫🇷", name="Français", path="/fr/"),
    "de": dict(dir="de/", code="DE", flag="🇩🇪", name="Deutsch", path="/de/"),
    "es": dict(dir="es/", code="ES", flag="🇪🇸", name="Español", path="/es/"),
}
ORDER = ["nl", "en", "fr", "de", "es"]

# Vertalingen van de gedeelde chrome (nav/footer/knop).
CHROME = {
    "nl": dict(features="Functies", how="Zo werkt het", price="Prijs", faq="FAQ", download="Download", support="Support", privacy="Privacy",
               privacy_long="Privacybeleid", badge_small="Download in de", badge_big="App Store", aria_dl="Download RightSetFret in de App Store",
               read_also="Lees ook", ig_page="Recepten van Instagram bewaren", tt_page="Recepten van TikTok bewaren", legal="© 2026 PLAN B · Belgium", lang_aria="Taal"),
    "en": dict(features="Features", how="How it works", price="Pricing", faq="FAQ", download="Download", support="Support", privacy="Privacy",
               privacy_long="Privacy Policy", badge_small="Download on the", badge_big="App Store", aria_dl="Download RightSetFret on the App Store",
               read_also="Read next", ig_page="Save recipes from Instagram", tt_page="Save recipes from TikTok", legal="© 2026 PLAN B · Belgium", lang_aria="Language"),
    "fr": dict(features="Fonctions", how="Comment ça marche", price="Prix", faq="FAQ", download="Télécharger", support="Support", privacy="Confidentialité",
               privacy_long="Politique de confidentialité", badge_small="Télécharger dans l’", badge_big="App Store", aria_dl="Télécharger RightSetFret dans l’App Store",
               read_also="À lire aussi", ig_page="Enregistrer les recettes d’Instagram", tt_page="Enregistrer les recettes de TikTok", legal="© 2026 PLAN B · Belgium", lang_aria="Langue"),
    "de": dict(features="Funktionen", how="So funktioniert’s", price="Preis", faq="FAQ", download="Laden", support="Support", privacy="Datenschutz",
               privacy_long="Datenschutzerklärung", badge_small="Laden im", badge_big="App Store", aria_dl="RightSetFret im App Store laden",
               read_also="Auch lesen", ig_page="Rezepte aus Instagram speichern", tt_page="Rezepte aus TikTok speichern", legal="© 2026 PLAN B · Belgium", lang_aria="Sprache"),
    "es": dict(features="Funciones", how="Cómo funciona", price="Precio", faq="FAQ", download="Descargar", support="Soporte", privacy="Privacidad",
               privacy_long="Política de privacidad", badge_small="Descargar en el", badge_big="App Store", aria_dl="Descargar RightSetFret en el App Store",
               read_also="Lee también", ig_page="Guardar recetas de Instagram", tt_page="Guardar recetas de TikTok", legal="© 2026 PLAN B · Belgium", lang_aria="Idioma"),
}

# Landingspagina's per taal (de/es hebben er nog geen → Engelse variant).
LANDING = {
    "nl": ("instagram-recept-opslaan.html", "tiktok-recept-bewaren.html"),
    "en": ("save-instagram-recipes.html", "save-tiktok-recipes.html"),
    "fr": ("enregistrer-recettes-instagram.html", "enregistrer-recettes-tiktok.html"),
    "de": ("/en/save-instagram-recipes.html", "/en/save-tiktok-recipes.html"),
    "es": ("/en/save-instagram-recipes.html", "/en/save-tiktok-recipes.html"),
}

def esc(s): return html.escape(s, quote=True)

def store_link(ct):
    """App Store-campagnelink. Voeg later `&pt=<provider token>` toe (ASC › App Analytics › Campaigns)."""
    return f"https://apps.apple.com/app/apple-store/id{APP_ID}?ct={ct}&mt=8"

def asset(lang, path):
    """Root-assets: relatief vanaf de root, absoluut vanuit een taalmap (zoals de bestaande en/index.html doet)."""
    return path if lang == "nl" else "/" + path

def url(lang, path):
    return f"{SITE}/{LANGS[lang]['dir']}{path}"

APPLE_SVG = ('<svg viewBox="0 0 814 1000" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><path fill="currentColor" d="M788.1 340.9c-5.8 4.5-108.2 62.2-108.2 190.5 0 148.4 130.3 200.9 134.2 202.2-.6 3.2-20.7 71.9-68.7 141.9-42.8 61.6-87.5 123.1-155.5 123.1s-85.5-39.5-164-39.5c-76.5 0-103.7 40.8-165.9 40.8s-105.6-57-155.5-127C46.7 790.7 0 663 0 541.8c0-194.4 126.4-297.5 250.8-297.5 66.1 0 121.2 43.4 162.7 43.4 39.5 0 101.1-46 176.3-46 28.5 0 130.9 2.6 198.3 99.2zm-234-181.5c31.1-36.9 53.1-88.1 53.1-139.3 0-7.1-.6-14.3-1.9-20.1-50.6 1.9-110.8 33.7-147.1 75.8-28.5 32.4-55.1 83.6-55.1 135.5 0 7.8 1.3 15.6 1.9 18.1 3.2.6 8.4 1.3 13.6 1.3 45.4 0 102.5-30.4 135.5-71.3z"/></svg>')

IG_SVG = ('<svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><path fill="currentColor" d="M12 2.2c3.2 0 3.6 0 4.8.1 3.3.1 4.8 1.7 4.9 4.9.1 1.3.1 1.6.1 4.8s0 3.6-.1 4.8c-.1 3.2-1.7 4.8-4.9 4.9-1.3.1-1.6.1-4.8.1s-3.6 0-4.8-.1c-3.3-.1-4.8-1.7-4.9-4.9C2.2 15.6 2.2 15.2 2.2 12s0-3.6.1-4.8C2.4 3.9 4 2.4 7.2 2.3 8.4 2.2 8.8 2.2 12 2.2zM12 0C8.7 0 8.3 0 7.1.1 2.7.3.3 2.7.1 7.1 0 8.3 0 8.7 0 12s0 3.7.1 4.9c.2 4.4 2.6 6.8 7 7C8.3 24 8.7 24 12 24s3.7 0 4.9-.1c4.4-.2 6.8-2.6 7-7 .1-1.2.1-1.6.1-4.9s0-3.7-.1-4.9c-.2-4.4-2.6-6.8-7-7C15.7 0 15.3 0 12 0zm0 5.8a6.2 6.2 0 100 12.4 6.2 6.2 0 000-12.4zM12 16a4 4 0 110-8 4 4 0 010 8zm6.4-11.8a1.4 1.4 0 100 2.9 1.4 1.4 0 000-2.9z"/></svg>')

def badge(lang, ct):
    c = CHROME[lang]
    return (f'<a class="appstore-badge" href="{store_link(ct)}" aria-label="{esc(c["aria_dl"])}">{APPLE_SVG}'
            f'<span class="badge-text"><small>{esc(c["badge_small"])}</small><strong>{esc(c["badge_big"])}</strong></span></a>')

def pixel():
    return f"""<!-- Meta Pixel Code -->
<script>
!function(f,b,e,v,n,t,s)
{{if(f.fbq)return;n=f.fbq=function(){{n.callMethod?
n.callMethod.apply(n,arguments):n.queue.push(arguments)}};
if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
n.queue=[];t=b.createElement(e);t.async=!0;
t.src=v;s=b.getElementsByTagName(e)[0];
s.parentNode.insertBefore(t,s)}}(window, document,'script',
'https://connect.facebook.net/en_US/fbevents.js');
fbq('init', '{PIXEL_ID}');
fbq('track', 'PageView');
</script>
<noscript><img height="1" width="1" style="display:none"
src="https://www.facebook.com/tr?id={PIXEL_ID}&ev=PageView&noscript=1"
/></noscript>
<!-- End Meta Pixel Code -->"""

def head(lang, title, desc, path, alt, og_image="img/og-home.jpg", extra=""):
    """`alt` = {taal: pad-vanaf-root} voor hreflang; x-default = nl."""
    links = "\n".join(f'<link rel="alternate" hreflang="{l}" href="{SITE}/{p}">' for l, p in alt.items())
    links += f'\n<link rel="alternate" hreflang="x-default" href="{SITE}/{alt["nl"]}">'
    canonical = f"{SITE}/{LANGS[lang]['dir']}{path}" if path != "index.html" else f"{SITE}/{LANGS[lang]['dir']}index.html"
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{canonical}">
{links}
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE}/{og_image}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#ffffff">
<link rel="icon" type="image/png" href="{asset(lang, 'favicon.png')}">
<link rel="apple-touch-icon" href="{asset(lang, 'apple-touch-icon.png')}">
<link rel="stylesheet" href="{asset(lang, 'styles.css')}">
{extra}
{pixel()}
</head>"""

def nav(lang, current="index.html", ct="web_nav"):
    c = CHROME[lang]
    items = "\n".join(
        f'                    <li><a href="{LANGS[l]["path"]}" hreflang="{l}"{" aria-current=\"page\"" if l == lang else ""}><span class="flag">{LANGS[l]["flag"]}</span> {LANGS[l]["name"]}</a></li>'
        for l in ORDER)
    home = "index.html"
    return f"""<nav class="nav" id="top">
    <div class="wrap nav-inner">
        <a class="brand" href="{home}"><img class="logo" src="{asset(lang, 'app-icon.png')}" alt="" width="36" height="36"><span class="name">RightSetFret</span></a>
        <div class="nav-links">
            <a href="{home}#functies">{esc(c["features"])}</a>
            <a href="{home}#zo-werkt-het">{esc(c["how"])}</a>
            <a href="{home}#prijs">{esc(c["price"])}</a>
            <a href="{home}#faq">{esc(c["faq"])}</a>
        </div>
        <div class="nav-right">
            <div class="lang">
                <button type="button" class="lang-btn" aria-haspopup="true" aria-expanded="false" aria-label="{esc(c["lang_aria"])}"><span class="flag">{LANGS[lang]["flag"]}</span><span class="code">{LANGS[lang]["code"]}</span> <span class="chev">▾</span></button>
                <ul class="lang-list">
{items}
                </ul>
            </div>
            <a class="btn btn-primary btn-nav" href="{store_link(ct + '_' + lang)}">{esc(c["download"])}</a>
        </div>
    </div>
</nav>"""

def footer(lang):
    c = CHROME[lang]; ig, tt = LANDING[lang]
    return f"""<footer class="footer">
    <div class="wrap footer-inner">
        <div class="footer-links">
            <span class="footer-label">{esc(c["read_also"])}:</span>
            <a href="{ig}">{esc(c["ig_page"])}</a>
            <a href="{tt}">{esc(c["tt_page"])}</a>
        </div>
        <div class="footer-links">
            <a href="support.html">{esc(c["support"])}</a>
            <a href="privacy.html">{esc(c["privacy_long"])}</a>
            <a class="ig-link" href="https://instagram.com/rightsetfret" target="_blank" rel="noopener" aria-label="RightSetFret op Instagram (@rightsetfret)">{IG_SVG}</a>
        </div>
        <div class="legal">{esc(c["legal"])}</div>
    </div>
</footer>
<script defer src="{asset(lang, 'lang.js')}"></script>
<script defer src="{asset(lang, 'reveal.js')}"></script>"""

def phone(src, alt, cls=""):
    """CSS-telefoonkader met één scherm (780px brede JPEG)."""
    return (f'<div class="phone {cls}"><div class="phone-screen"><img src="{src}" alt="{esc(alt)}" loading="lazy" width="780" height="1696"></div></div>')

def qr_svg(link):
    img = qrcode.make(link, image_factory=qrcode.image.svg.SvgPathImage, box_size=10, border=1)
    buf = io.BytesIO(); img.save(buf)
    svg = buf.getvalue().decode()
    return svg[svg.index("<svg"):]
```

- [ ] **Stap 4: Draaien** — `python3 tools/test_site_common.py` → 5 × `ok`.

- [ ] **Stap 5: Commit**

```bash
git add site_common.py tools/test_site_common.py
git commit -m "site_common: gedeelde head/nav/footer/knop/QR voor alle pagina's"
```

---

### Taak 3: `styles.css` (nieuw) en `reveal.js`

**Files:**
- Modify: `styles.css` (volledig vervangen)
- Create: `reveal.js`

- [ ] **Stap 1: `styles.css`**

```css
/* RightSetFret — stijl B "modern app-landing" (spec 2026-09-23).
   Eén stylesheet voor homepage, landingspagina's, support en privacy. */
:root {
  --bg: #ffffff; --bg-soft: #f7f5f1; --ink: #111111; --ink-2: #5f5a54; --line: #e5e2dd;
  --accent: #c96b2a; --accent-dark: #a9541f; --accent-soft: #fbeee3;
  --radius: 16px; --maxw: 1120px;
  --font: -apple-system, "SF Pro Text", Inter, "Segoe UI", Roboto, sans-serif;
  --shadow: 0 8px 30px rgba(17,17,17,.08); --shadow-lg: 0 30px 60px rgba(17,17,17,.18);
}
*, *::before, *::after { box-sizing: border-box; }
html { scroll-behavior: smooth; -webkit-text-size-adjust: 100%; }
body { margin: 0; background: var(--bg); color: var(--ink); font-family: var(--font); font-size: 17px; line-height: 1.55; }
img, video, svg { max-width: 100%; display: block; }
a { color: var(--accent-dark); text-decoration: none; }
a:hover { text-decoration: underline; }
h1, h2, h3 { margin: 0; font-weight: 800; letter-spacing: -.02em; line-height: 1.05; }
h1 { font-size: clamp(40px, 7vw, 72px); }
h2 { font-size: clamp(28px, 4vw, 44px); }
h3 { font-size: 22px; letter-spacing: -.01em; line-height: 1.2; }
p { margin: 0; }
.wrap { max-width: var(--maxw); margin: 0 auto; padding: 0 20px; }
.section { padding: 96px 0; }
.section.soft { background: var(--bg-soft); }
.section-head { text-align: center; max-width: 720px; margin: 0 auto 48px; }
.section-head p { color: var(--ink-2); font-size: 19px; margin-top: 14px; }
.kicker { display: inline-block; font-size: 13px; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; color: var(--accent); margin-bottom: 12px; }
:focus-visible { outline: 3px solid var(--accent); outline-offset: 3px; border-radius: 6px; }

/* Knoppen */
.btn { display: inline-flex; align-items: center; gap: 10px; padding: 14px 22px; border-radius: 999px; font-weight: 700; font-size: 16px; border: 1px solid transparent; transition: transform .15s ease, background .15s ease; }
.btn:hover { text-decoration: none; transform: translateY(-1px); }
.btn-primary { background: var(--ink); color: #fff; }
.btn-primary:hover { background: #000; }
.btn-ghost { background: transparent; color: var(--ink); border-color: var(--line); }
.btn-ghost:hover { background: var(--bg-soft); }
.btn-nav { padding: 10px 16px; font-size: 14px; background: var(--accent); }
.btn-nav:hover { background: var(--accent-dark); }
.appstore-badge { display: inline-flex; align-items: center; gap: 10px; background: var(--ink); color: #fff; border-radius: 12px; padding: 10px 18px 10px 14px; line-height: 1.05; transition: transform .15s ease; }
.appstore-badge:hover { text-decoration: none; transform: translateY(-1px); }
.appstore-badge svg { width: 26px; height: 32px; }
.appstore-badge .badge-text { display: flex; flex-direction: column; text-align: left; }
.appstore-badge small { font-size: 11px; font-weight: 500; opacity: .85; }
.appstore-badge strong { font-size: 20px; font-weight: 700; }

/* Nav */
.nav { position: sticky; top: 0; z-index: 50; background: rgba(255,255,255,.78); backdrop-filter: saturate(160%) blur(12px); -webkit-backdrop-filter: saturate(160%) blur(12px); border-bottom: 1px solid rgba(0,0,0,.06); }
.nav-inner { display: flex; align-items: center; justify-content: space-between; gap: 20px; height: 64px; }
.brand { display: inline-flex; align-items: center; gap: 10px; color: var(--ink); font-weight: 800; font-size: 18px; letter-spacing: -.01em; }
.brand:hover { text-decoration: none; }
.brand .logo { width: 36px; height: 36px; border-radius: 9px; }
.nav-links { display: flex; gap: 26px; }
.nav-links a { color: var(--ink-2); font-weight: 600; font-size: 15px; }
.nav-links a:hover { color: var(--ink); text-decoration: none; }
.nav-right { display: flex; align-items: center; gap: 14px; }
.lang { position: relative; }
.lang-btn { display: inline-flex; align-items: center; gap: 6px; background: none; border: 0; cursor: pointer; font: inherit; font-size: 14px; font-weight: 600; color: var(--ink-2); padding: 6px 8px; border-radius: 8px; }
.lang-btn:hover { background: var(--bg-soft); color: var(--ink); }
.lang-btn .flag { font-size: 18px; line-height: 1; }
.lang-btn .chev { font-size: 11px; transition: transform .2s ease; }
.lang.open .lang-btn .chev { transform: rotate(180deg); }
.lang-list { position: absolute; right: 0; top: 100%; margin: 8px 0 0; padding: 6px; list-style: none; min-width: 180px; background: #fff; border: 1px solid var(--line); border-radius: 14px; box-shadow: var(--shadow); opacity: 0; visibility: hidden; transform: translateY(-6px); transition: opacity .18s ease, transform .18s ease, visibility .18s ease; z-index: 60; }
.lang.open .lang-list { opacity: 1; visibility: visible; transform: translateY(0); }
.lang-list li { margin: 0; }
.lang-list a { display: flex; align-items: center; gap: 10px; padding: 9px 12px; border-radius: 9px; color: var(--ink); font-size: 15px; }
.lang-list a:hover { background: var(--bg-soft); text-decoration: none; }
.lang-list a[aria-current="page"] { font-weight: 700; }
.lang-list .flag { font-size: 20px; }
@media (max-width: 820px) { .nav-links { display: none; } }

/* Hero */
.hero { position: relative; overflow: hidden; padding: 72px 0 0; text-align: center; }
.hero h1 { max-width: 860px; margin: 0 auto; }
.hero .sub { max-width: 640px; margin: 22px auto 0; font-size: 20px; color: var(--ink-2); }
.hero .cta { display: flex; gap: 14px; justify-content: center; align-items: center; flex-wrap: wrap; margin-top: 30px; }
.chips { display: flex; flex-wrap: wrap; justify-content: center; gap: 8px; margin: 26px auto 0; padding: 0; list-style: none; }
.chips li { font-size: 13px; font-weight: 600; color: var(--ink-2); background: var(--bg-soft); border: 1px solid var(--line); border-radius: 999px; padding: 6px 12px; }
.chips li.star { color: var(--accent-dark); background: var(--accent-soft); border-color: transparent; }
.hero-stage { position: relative; max-width: 760px; margin: 56px auto 0; padding-bottom: 40px; }
.hero-stage::before { content: ""; position: absolute; left: 50%; bottom: 0; width: 900px; height: 420px; transform: translateX(-50%); background: radial-gradient(50% 60% at 50% 100%, rgba(201,107,42,.30), rgba(201,107,42,0) 70%); pointer-events: none; }
.hero-stage .phone { margin: 0 auto; width: min(320px, 78vw); }
.float-chip { position: absolute; display: inline-flex; align-items: center; gap: 8px; background: #fff; border: 1px solid var(--line); border-radius: 999px; padding: 8px 14px; font-size: 14px; font-weight: 700; box-shadow: var(--shadow); animation: floaty 6s ease-in-out infinite; }
.float-chip svg { width: 18px; height: 18px; }
.float-chip.c1 { left: 4%; top: 14%; animation-delay: 0s; }
.float-chip.c2 { right: 4%; top: 22%; animation-delay: -1.2s; }
.float-chip.c3 { left: 8%; top: 52%; animation-delay: -2.4s; }
.float-chip.c4 { right: 6%; top: 60%; animation-delay: -3.6s; }
.float-chip.c5 { left: 18%; top: 84%; animation-delay: -4.8s; }
@keyframes floaty { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-10px); } }
@media (max-width: 640px) { .float-chip { display: none; } .hero { padding-top: 48px; } .hero .sub { font-size: 18px; } }

/* Telefoonkader */
.phone { position: relative; width: 100%; aspect-ratio: 1206 / 2622; border-radius: 12.5% / 5.75%; background: #1b1b1b; padding: 3.2%; box-shadow: var(--shadow-lg); }
.phone::before { content: ""; position: absolute; left: 50%; top: 4.2%; width: 30%; height: 3.1%; transform: translateX(-50%); background: #1b1b1b; border-radius: 999px; z-index: 2; }
.phone-screen { width: 100%; height: 100%; border-radius: 10.5% / 4.8%; overflow: hidden; background: #f4efe6; }
.phone-screen img { width: 100%; height: 100%; object-fit: cover; object-position: top; }
.shot-wide { border-radius: var(--radius); overflow: hidden; box-shadow: var(--shadow-lg); border: 1px solid var(--line); }

/* Bronnen-strip */
.sources { padding: 44px 0; border-top: 1px solid var(--line); border-bottom: 1px solid var(--line); }
.sources .label { text-align: center; color: var(--ink-2); font-size: 14px; font-weight: 600; margin-bottom: 18px; }
.sources ul { display: flex; gap: 10px; justify-content: center; list-style: none; margin: 0; padding: 0 20px; overflow-x: auto; scrollbar-width: none; }
.sources ul::-webkit-scrollbar { display: none; }
.sources li { flex: 0 0 auto; display: inline-flex; align-items: center; gap: 8px; color: var(--ink-2); font-weight: 600; font-size: 15px; padding: 10px 14px; border-radius: 12px; background: var(--bg-soft); }
.sources svg { width: 20px; height: 20px; }

/* Stappen */
.steps { display: grid; grid-template-columns: repeat(3, 1fr); gap: 32px; }
.step { text-align: center; }
.step .phone { width: min(260px, 70vw); margin: 0 auto 22px; }
.step .num { display: inline-grid; place-items: center; width: 36px; height: 36px; border-radius: 50%; background: var(--accent); color: #fff; font-weight: 800; margin-bottom: 12px; }
.step p { color: var(--ink-2); margin-top: 8px; }
@media (max-width: 820px) { .steps { grid-template-columns: 1fr; gap: 48px; } }

/* Functies */
.feature { display: grid; grid-template-columns: 1fr 1fr; gap: 64px; align-items: center; padding: 48px 0; }
.feature .phone { width: min(300px, 74vw); margin: 0 auto; }
.feature:nth-child(even) .feature-media { order: 2; }
.feature h3 { font-size: clamp(24px, 3vw, 32px); }
.feature p { color: var(--ink-2); margin-top: 14px; font-size: 18px; }
.feature ul { margin: 18px 0 0; padding: 0; list-style: none; }
.feature li { position: relative; padding-left: 28px; margin-bottom: 8px; }
.feature li::before { content: "✓"; position: absolute; left: 0; color: var(--accent); font-weight: 800; }
@media (max-width: 820px) { .feature { grid-template-columns: 1fr; gap: 28px; padding: 32px 0; } .feature:nth-child(even) .feature-media { order: 0; } }
.minis { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 24px; }
.mini { background: #fff; border: 1px solid var(--line); border-radius: var(--radius); padding: 24px; }
.mini h3 { font-size: 19px; margin-bottom: 8px; }
.mini p { color: var(--ink-2); }
@media (max-width: 640px) { .minis { grid-template-columns: 1fr; } }

/* Video */
.video-sec .phone { width: min(340px, 78vw); margin: 0 auto; }
.video-sec video { width: 100%; height: 100%; object-fit: cover; background: #000; }

/* Verhaal + rating */
.story { display: grid; grid-template-columns: 1.2fr .8fr; gap: 48px; align-items: center; }
.story .portrait { width: 120px; height: 120px; border-radius: 50%; object-fit: cover; margin-bottom: 20px; box-shadow: var(--shadow); }
.story blockquote { margin: 0; font-size: 21px; line-height: 1.45; }
.story .who { margin-top: 16px; color: var(--ink-2); font-weight: 600; }
.rating { background: #fff; border: 1px solid var(--line); border-radius: var(--radius); padding: 28px; text-align: center; box-shadow: var(--shadow); }
.rating .stars { font-size: 28px; color: var(--accent); letter-spacing: 2px; }
.rating .score { font-size: 44px; font-weight: 800; letter-spacing: -.02em; }
.rating p { color: var(--ink-2); }
@media (max-width: 820px) { .story { grid-template-columns: 1fr; } }

/* Prijs */
.plans { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }
.plan { position: relative; background: #fff; border: 1px solid var(--line); border-radius: var(--radius); padding: 28px; display: flex; flex-direction: column; }
.plan.featured { border-color: var(--accent); box-shadow: 0 16px 40px rgba(201,107,42,.18); }
.plan .save { position: absolute; top: -13px; left: 24px; background: var(--accent); color: #fff; font-size: 12px; font-weight: 800; padding: 4px 10px; border-radius: 999px; }
.plan .name { font-weight: 700; color: var(--ink-2); }
.plan .price { font-size: 40px; font-weight: 800; letter-spacing: -.02em; margin-top: 6px; }
.plan .per { color: var(--ink-2); font-size: 15px; }
.plan .note { color: var(--ink-2); font-size: 15px; margin: 14px 0 22px; flex: 1; }
.price-foot { text-align: center; color: var(--ink-2); margin-top: 28px; font-size: 15px; }
@media (max-width: 820px) { .plans { grid-template-columns: 1fr; } }

/* FAQ */
.faq { max-width: 760px; margin: 0 auto; }
.faq details { border-bottom: 1px solid var(--line); padding: 4px 0; }
.faq summary { cursor: pointer; list-style: none; display: flex; justify-content: space-between; align-items: center; gap: 16px; padding: 18px 0; font-weight: 700; font-size: 18px; }
.faq summary::-webkit-details-marker { display: none; }
.faq summary::after { content: "+"; font-size: 24px; color: var(--accent); flex: 0 0 auto; }
.faq details[open] summary::after { content: "–"; }
.faq .a { color: var(--ink-2); padding: 0 0 20px; max-width: 640px; }

/* Slot-CTA */
.cta-final { text-align: center; padding: 96px 0; background: var(--bg-soft); }
.cta-final .cta { display: flex; gap: 28px; justify-content: center; align-items: center; flex-wrap: wrap; margin-top: 30px; }
.qr { display: flex; flex-direction: column; align-items: center; gap: 8px; font-size: 13px; color: var(--ink-2); }
.qr svg { width: 112px; height: 112px; border: 1px solid var(--line); border-radius: 12px; padding: 6px; background: #fff; }
@media (max-width: 640px) { .qr { display: none; } }

/* Footer */
.footer { border-top: 1px solid var(--line); padding: 40px 0; font-size: 14px; color: var(--ink-2); }
.footer-inner { display: flex; flex-direction: column; gap: 14px; }
.footer-links { display: flex; flex-wrap: wrap; gap: 6px 18px; align-items: center; }
.footer-links a { color: var(--ink-2); }
.footer-label { font-weight: 700; }
.footer .ig-link { display: inline-flex; color: var(--ink-2); }
.footer .legal { color: #8a847c; }

/* Scroll-reveal */
.reveal { opacity: 0; transform: translateY(24px); transition: opacity .5s ease, transform .5s ease; }
.reveal.in { opacity: 1; transform: none; }
@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }
  .reveal { opacity: 1; transform: none; transition: none; }
  .float-chip { animation: none; }
  .btn, .appstore-badge { transition: none; }
}

/* ---- Landingspagina's, support en privacy (bestaande klassen, nieuwe look) ---- */
.hero .icon { width: 84px; height: 84px; border-radius: 20px; margin: 0 auto 24px; box-shadow: var(--shadow); }
.hero .tagline { max-width: 640px; margin: 18px auto 0; font-size: 19px; color: var(--ink-2); }
.hero .soon { margin-top: 18px; color: var(--ink-2); font-size: 14px; }
.hero-video { max-width: 320px; margin: 0 auto 34px; }
.hero-video video { width: 100%; border-radius: 28px; box-shadow: var(--shadow-lg); }
.features, .tutorials { padding: 72px 0; }
.section-title { text-align: center; font-size: clamp(28px, 4vw, 40px); margin: 0 0 8px; }
.section-sub { text-align: center; color: var(--ink-2); margin: 12px auto 36px; max-width: 640px; }
.grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }
.card { background: #fff; border: 1px solid var(--line); border-radius: var(--radius); padding: 24px; }
.card .emoji { font-size: 28px; }
.card h3 { font-size: 19px; margin: 12px 0 6px; }
.card p { color: var(--ink-2); font-size: 15px; }
.card .badge { display: inline-block; font-size: 11px; font-weight: 700; letter-spacing: .06em; text-transform: uppercase; color: var(--accent); background: var(--accent-soft); border-radius: 999px; padding: 2px 8px; margin-left: 6px; vertical-align: middle; }
.tutorial-grid { grid-template-columns: repeat(4, 1fr); }
.tutorial { text-align: center; }
.tutorial video { width: 100%; border-radius: 20px; box-shadow: var(--shadow); }
.tutorial h3 { font-size: 16px; margin-top: 12px; }
.closing { text-align: center; padding: 80px 20px; background: var(--bg-soft); }
.closing .cta { display: flex; justify-content: center; margin-top: 24px; }
.closing .soon { margin-top: 16px; color: var(--ink-2); font-size: 14px; }
@media (max-width: 820px) { .grid, .tutorial-grid { grid-template-columns: 1fr; } }
.doc { max-width: 760px; margin: 48px auto 80px; }
.doc h1 { font-size: clamp(30px, 5vw, 44px); margin-bottom: 6px; }
.doc .updated { color: var(--ink-2); font-size: 14px; margin-bottom: 26px; }
.doc h2 { font-size: 24px; margin: 32px 0 10px; }
.doc h3 { font-size: 18px; margin: 20px 0 6px; }
.doc p, .doc li { color: var(--ink); font-size: 17px; margin-bottom: 10px; }
.doc ul { margin: 10px 0; padding-left: 22px; }
.doc a { font-weight: 600; }
```

- [ ] **Stap 2: `reveal.js`**

```js
(function () {
  var els = document.querySelectorAll('.reveal');
  if (!('IntersectionObserver' in window) || window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    els.forEach(function (el) { el.classList.add('in'); });
    return;
  }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
    });
  }, { rootMargin: '0px 0px -10% 0px', threshold: 0.1 });
  els.forEach(function (el) { io.observe(el); });
})();
```

- [ ] **Stap 3: Controleer support/privacy met de nieuwe stylesheet**

`python3 -m http.server 8765` → `http://127.0.0.1:8765/support.html` en `/privacy.html` leesbaar (witte achtergrond, sans-serif, nav zonder gebroken lay-out). De oude nav-markup in die pagina's gebruikt `.nav > .brand/.links`; voeg daarom onderaan `styles.css` toe:

```css
/* Oude nav-markup (support/privacy/landingspagina's tot ze opnieuw gegenereerd zijn) */
.nav > .brand, .nav > .links { display: inline-flex; align-items: center; }
.nav > .brand { float: left; height: 64px; padding-left: 20px; }
.nav > .links { float: right; height: 64px; gap: 18px; padding-right: 20px; }
.nav > .links a { color: var(--ink-2); font-weight: 600; font-size: 15px; }
.nav::after { content: ""; display: table; clear: both; }
```

- [ ] **Stap 4: Commit**

```bash
git add styles.css reveal.js
git commit -m "Nieuwe stylesheet (stijl B) + scroll-reveal; oude pagina's blijven leesbaar"
```

---

### Taak 4: `gen_site.py` — homepage in 5 talen

**Files:**
- Create: `gen_site.py`
- Create: `img/og-home.jpg` (via `tools/make_og.py`)
- Create: `tools/make_og.py`
- Test: `tools/check_site.py` (Taak 5) gebruikt de output

- [ ] **Stap 1: OG-afbeelding**

```python
"""Maakt img/og-home.jpg (1200×630): receptscherm op een oranje gloed."""
from PIL import Image, ImageDraw, ImageFilter
W, H = 1200, 630
bg = Image.new("RGB", (W, H), "#ffffff")
glow = Image.new("RGB", (W, H), "#ffffff")
d = ImageDraw.Draw(glow); d.ellipse((350, 260, 850, 760), fill="#e9b78f")
glow = glow.filter(ImageFilter.GaussianBlur(90))
bg = Image.blend(bg, glow, 0.9)
shot = Image.open("img/recept.jpg").convert("RGB")
shot = shot.resize((300, int(300 * shot.height / shot.width)))
frame = Image.new("RGB", (shot.width + 24, shot.height + 24), "#1b1b1b")
frame.paste(shot, (12, 12))
mask = Image.new("L", frame.size, 0); ImageDraw.Draw(mask).rounded_rectangle((0, 0, frame.width, frame.height), 44, fill=255)
bg.paste(frame, ((W - frame.width) // 2, 70), mask)
bg.save("img/og-home.jpg", quality=86)
print("img/og-home.jpg", bg.size)
```

Run: `python3 tools/make_og.py` → `img/og-home.jpg (1200, 630)`.

- [ ] **Stap 2: Generator**

```python
"""Homepage van rightsetfret.studioplanb.be in 5 talen (spec 2026-09-23, stijl B).
   python3 gen_site.py  →  index.html, en/index.html, fr/…, de/…, es/…"""
import json, os
from site_common import *  # noqa

ROOT = os.path.dirname(os.path.abspath(__file__))

ICON = {  # inline SVG's (20px), monochroom
 "instagram": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor"/></svg>',
 "tiktok": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M14 3h3c.3 2.2 1.7 3.6 4 3.9v3c-1.5 0-2.9-.5-4-1.3V15a6 6 0 11-6-6v3a3 3 0 103 3V3z"/></svg>',
 "youtube": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M22 8.2c-.2-1.4-1.2-2.4-2.6-2.6C17.4 5.3 12 5.3 12 5.3s-5.4 0-7.4.3C3.2 5.8 2.2 6.8 2 8.2 1.7 10.1 1.7 12 1.7 12s0 1.9.3 3.8c.2 1.4 1.2 2.4 2.6 2.6 2 .3 7.4.3 7.4.3s5.4 0 7.4-.3c1.4-.2 2.4-1.2 2.6-2.6.3-1.9.3-3.8.3-3.8s0-1.9-.3-3.8zM10 15V9l5.2 3L10 15z"/></svg>',
 "pinterest": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 00-3.6 19.3c-.1-.8-.2-2 0-2.9l1.2-5s-.3-.6-.3-1.5c0-1.4.8-2.4 1.8-2.4.9 0 1.3.6 1.3 1.4 0 .9-.5 2.1-.8 3.3-.2 1 .5 1.8 1.5 1.8 1.8 0 3.1-1.9 3.1-4.5 0-2.4-1.7-4-4.1-4-2.8 0-4.5 2.1-4.5 4.3 0 .9.3 1.8.7 2.3l.1.4-.3 1.1c0 .2-.2.3-.4.2-1.2-.6-2-2.4-2-3.8 0-3.1 2.3-6 6.6-6 3.5 0 6.1 2.5 6.1 5.8 0 3.4-2.2 6.2-5.2 6.2-1 0-2-.5-2.3-1.1l-.6 2.4c-.2.9-.8 2-1.2 2.6A10 10 0 1012 2z"/></svg>',
 "facebook": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M14 8h3V4h-3c-2.8 0-4 1.7-4 4.5V11H7v4h3v7h4v-7h3l1-4h-4V8.7c0-.5.3-.7.7-.7z"/></svg>',
 "web": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 010 18M12 3a14 14 0 000 18"/></svg>',
 "screenshot": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="7" y="2" width="10" height="20" rx="2"/><path d="M11 18h2"/></svg>',
 "photo": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><circle cx="12" cy="12" r="3.5"/><path d="M8 5l1-2h6l1 2"/></svg>',
}

TEXT = {
 "nl": dict(
  title="RightSetFret — Van reel naar recept in 5 seconden",
  desc="Deel een recept van Instagram, TikTok of YouTube met RightSetFret en krijg meteen een nette receptfiche met ingrediënten, stappen en foto. Weekplanner en boodschappenlijst inbegrepen. 10 imports gratis.",
  h1="Van reel naar recept in 5 seconden.",
  sub="Zie je een recept op Instagram, TikTok of YouTube? Deel het met RightSetFret en je hebt een nette fiche — ingrediënten, stappen en foto, in jouw taal.",
  ghost="Bekijk hoe het werkt",
  chips=["10 imports gratis", "7 dagen gratis proberen", "★ 5,0 in de App Store", "In 5 talen", "Gemaakt in België"],
  floats=["Instagram", "TikTok", "YouTube", "Website", "Foto"],
  sources_label="Werkt met alles waar je recepten tegenkomt",
  sources=["Instagram", "TikTok", "YouTube", "Pinterest", "Facebook", "Websites", "Screenshot", "Foto van kookboek of tijdschrift"],
  steps_title="Zo werkt het", steps_sub="Drie stappen, geen gedoe.",
  steps=[("Deel de reel", "Tik op Delen in Instagram of TikTok en kies RightSetFret."),
         ("Even wachten", "RightSetFret leest video, stem en bijschrift en maakt er ingrediënten en stappen van."),
         ("Koken maar", "Kookmodus met timers, porties schalen, ingrediënten op je lijstje.")],
  features_title="Eén app voor je hele kookroutine", features_sub="Van “dat ziet er lekker uit” tot een gedekte tafel.",
  features=[("Collectie", "Een kookboek dat zichzelf ordent", "Elk recept krijgt automatisch slimme tags — keuken, dieet, seizoen, hoofdingrediënt — en je vindt alles terug met één zoekwoord.", ["Automatische tags en verzamelingen", "Zoeken op titel, ingrediënt of tag", "Porties aanpassen, alles schaalt mee"]),
            ("Frigo", "Wat kan ik koken?", "Geef in wat er in je frigo ligt en zie meteen welke recepten je vanavond op tafel zet. Synoniemen snapt hij ook: kip of kipfilet, sla of salade.", ["Werkt met wat je al in huis hebt", "Ontbrekende ingrediënten met één tik op je lijstje", "Voedingswaarde per portie"]),
            ("Planning", "Je week gepland door AI", "Kies je dieet — vegetarisch, koolhydraatarm, eiwitrijk, keto of een kcal-plafond — en RightSetFret stelt een week samen uit je eigen recepten.", ["Automatische variatie en alternatieven", "Dagtotalen voor calorieën en macro’s", "Boodschappenlijst in één keer"]),
            ("Lijstje", "Boodschappen op de looproute van jouw winkel", "Je lijst sorteert zichzelf op de gangen van jouw supermarkt en leert van hoe jij winkelt. Deel één lijst met je gezin — bij iedereen live.", ["Sorteert per winkel, leert mee", "Inspreken met je stem", "Gedeeld met je gezin via een code"])],
  minis=[("Drie thema’s, jouw stijl", "Basis, Modern of Klassiek — één tik in Instellingen."), ("Kookmodus met timers", "Stap voor stap, handsfree, met een timer per stap.")],
  video_title="Zie het in 40 seconden", video_sub="Van reel tot boodschappenlijst.",
  story_title="Waarom RightSetFret", story_name="Bram Bollen", story_place="Genk, België",
  story="Ik bewaarde recepten als screenshots en vond ze nooit terug. Dus bouwde ik de app die ik zelf miste: deel een reel, en het recept staat netjes in je kookboek — met boodschappenlijst en weekplanning erbij. RightSetFret maak ik in Genk, met veel input van de eerste kokers die hem gebruiken.",
  rating_label="in de App Store", rating_link="Beoordelingen en recensies", 
  price_title="Begin gratis. Blijf als het bevalt.", price_sub="Je eerste 10 imports zijn gratis. Daarna kies je wat bij je past.",
  plans=[("Maandelijks", "€3,99", "per maand", "Onbeperkt importeren, weekplanner, boodschappenlijst, gezin.", ""),
         ("Jaarlijks", "€22,99", "per jaar · = €1,92 per maand", "Alles van maandelijks, één keer per jaar betalen.", "Bespaar 52 %"),
         ("Levenslang", "€69,99", "eenmalig", "Voor altijd van jou, geen abonnement.", "")],
  plan_cta="Start 7 dagen gratis", plan_cta_life="Koop levenslang",
  price_foot="7 dagen gratis proberen · annuleer wanneer je wil · je recepten bekijken en exporteren blijft altijd gratis.",
  faq_title="Veelgestelde vragen",
  faq=[("Moet ik een account maken?", "Nee. Je begint meteen. Een account heb je pas nodig voor sync tussen toestellen, de gedeelde gezinslijst en de community."),
       ("Werkt het zonder de app te openen?", "Ja. Delen vanuit Instagram of TikTok is genoeg — RightSetFret verwerkt het recept op de achtergrond en meldt zich als de fiche klaar is."),
       ("Wat als de reel geen ingrediënten noemt?", "RightSetFret combineert beeld, gesproken tekst en bijschrift. Ontbreekt er toch iets, dan vul je het zo aan in de fiche."),
       ("Bewaart RightSetFret de video?", "Nee. De fiche verwijst naar de originele video en de maker; de video zelf blijft op het platform."),
       ("Wat is gratis en wat niet?", "De eerste 10 imports zijn gratis, handmatig recepten toevoegen is altijd gratis, en je collectie bekijken en exporteren blijft gratis. Onbeperkt importeren, de AI-weekplanner en gezinsdelen zitten in het abonnement — 7 dagen gratis te proberen."),
       ("Op welke toestellen werkt het?", "iPhone met iOS 26 of nieuwer. Op iPad draait de iPhone-versie.")],
  cta_title="Bewaar vanavond je eerste recept.", cta_sub="Gratis te downloaden. Klaar in minder dan een minuut.",
  qr_label="Scan met je iPhone", video="promo-nl.mp4", poster="promo-poster.jpg",
  alts=dict(recept="Receptfiche met ingrediënten en stappen in RightSetFret", deelmenu="Het iOS-deelmenu met RightSetFret uitgelicht", import_="Sheet ‘Recept importeren’ met de invoerbronnen", kookmodus="Kookmodus met een stap en timer", collectie="Collectie met recepten en tags", frigo="Scherm ‘Wat kan ik koken?’ met ingrediënten uit de frigo", planning="Weekplanning met maaltijden per dag", lijstje="Boodschappenlijst gesorteerd per winkelgang"),
 ),
 "en": dict(
  title="RightSetFret — From reel to recipe in 5 seconds",
  desc="Share a recipe from Instagram, TikTok or YouTube to RightSetFret and get a clean recipe card with ingredients, steps and a photo. Weekly planner and shopping list included. 10 free imports.",
  h1="From reel to recipe in 5 seconds.",
  sub="Spot a recipe on Instagram, TikTok or YouTube? Share it to RightSetFret and you have a clean card — ingredients, steps and photo, in your language.",
  ghost="See how it works",
  chips=["10 free imports", "7-day free trial", "★ 5.0 on the App Store", "In 5 languages", "Made in Belgium"],
  floats=["Instagram", "TikTok", "YouTube", "Website", "Photo"],
  sources_label="Works with everything you find recipes on",
  sources=["Instagram", "TikTok", "YouTube", "Pinterest", "Facebook", "Websites", "Screenshot", "Photo of a cookbook or magazine"],
  steps_title="How it works", steps_sub="Three steps, no fuss.",
  steps=[("Share the reel", "Tap Share in Instagram or TikTok and pick RightSetFret."),
         ("Give it a moment", "RightSetFret reads video, voice and caption and turns them into ingredients and steps."),
         ("Start cooking", "Cooking mode with timers, scalable servings, ingredients on your list.")],
  features_title="One app for your whole cooking routine", features_sub="From “that looks good” to dinner on the table.",
  features=[("Collection", "A cookbook that organises itself", "Every recipe gets smart tags automatically — cuisine, diet, season, main ingredient — and you find anything with one search word.", ["Automatic tags and collections", "Search by title, ingredient or tag", "Adjust servings, everything scales"]),
            ("Fridge", "What can I cook?", "Enter what’s in your fridge and instantly see which recipes you can make tonight. It understands synonyms too: chicken or chicken breast.", ["Works with what you already have", "Missing ingredients to your list in one tap", "Nutrition per serving"]),
            ("Planning", "Your week planned by AI", "Pick your diet — vegetarian, low-carb, high-protein, keto or a calorie cap — and RightSetFret builds a week from your own recipes.", ["Automatic variety and swaps", "Daily totals for calories and macros", "Shopping list in one go"]),
            ("List", "Groceries in your store’s aisle order", "Your list sorts itself by the aisles of your supermarket and learns how you shop. Share one list with your family — live for everyone.", ["Sorts per store, keeps learning", "Add items by voice", "Shared with your family via a code"])],
  minis=[("Three themes, your style", "Basic, Modern or Classic — one tap in Settings."), ("Cooking mode with timers", "Step by step, hands-free, with a timer per step.")],
  video_title="See it in 40 seconds", video_sub="From reel to shopping list.",
  story_title="Why RightSetFret", story_name="Bram Bollen", story_place="Genk, Belgium",
  story="I used to save recipes as screenshots and never found them again. So I built the app I was missing: share a reel, and the recipe sits neatly in your cookbook — with shopping list and weekly planning included. I make RightSetFret in Genk, with lots of input from the first cooks using it.",
  rating_label="on the App Store", rating_link="Ratings and reviews",
  price_title="Start free. Stay if you like it.", price_sub="Your first 10 imports are free. Then pick what suits you.",
  plans=[("Monthly", "€3.99", "per month", "Unlimited imports, weekly planner, shopping list, family.", ""),
         ("Yearly", "€22.99", "per year · = €1.92 per month", "Everything in monthly, paid once a year.", "Save 52%"),
         ("Lifetime", "€69.99", "one-time", "Yours forever, no subscription.", "")],
  plan_cta="Start 7 days free", plan_cta_life="Buy lifetime",
  price_foot="7-day free trial · cancel anytime · viewing and exporting your recipes stays free forever. Prices shown in EUR; the App Store charges in your local currency.",
  faq_title="Frequently asked questions",
  faq=[("Do I need an account?", "No. You start right away. An account is only needed for sync between devices, the shared family list and the community."),
       ("Does it work without opening the app?", "Yes. Sharing from Instagram or TikTok is enough — RightSetFret processes the recipe in the background and lets you know when the card is ready."),
       ("What if the reel doesn’t list the ingredients?", "RightSetFret combines visuals, spoken audio and caption. If something is still missing, you add it to the card in a tap."),
       ("Does RightSetFret store the video?", "No. The card links to the original video and its creator; the video itself stays on the platform."),
       ("What’s free and what isn’t?", "Your first 10 imports are free, adding recipes by hand is always free, and viewing and exporting your collection stays free. Unlimited imports, the AI weekly planner and family sharing are in the subscription — with a 7-day free trial."),
       ("Which devices does it run on?", "iPhone with iOS 26 or later. On iPad the iPhone version runs.")],
  cta_title="Save your first recipe tonight.", cta_sub="Free to download. Ready in under a minute.",
  qr_label="Scan with your iPhone", video="promo-en.mp4", poster="promo-en-poster.jpg",
  alts=dict(recept="Recipe card with ingredients and steps in RightSetFret", deelmenu="The iOS share sheet with RightSetFret highlighted", import_="‘Import recipe’ sheet with the input sources", kookmodus="Cooking mode with a step and timer", collectie="Collection with recipes and tags", frigo="‘What can I cook?’ screen with fridge ingredients", planning="Weekly plan with meals per day", lijstje="Shopping list sorted by aisle"),
 ),
 "fr": dict(
  title="RightSetFret — Du reel à la recette en 5 secondes",
  desc="Partage une recette d’Instagram, TikTok ou YouTube vers RightSetFret et obtiens une fiche recette claire avec ingrédients, étapes et photo. Planificateur de la semaine et liste de courses inclus. 10 imports gratuits.",
  h1="Du reel à la recette en 5 secondes.",
  sub="Tu vois une recette sur Instagram, TikTok ou YouTube ? Partage-la vers RightSetFret et tu as une fiche soignée — ingrédients, étapes et photo, dans ta langue.",
  ghost="Voir comment ça marche",
  chips=["10 imports gratuits", "7 jours d’essai gratuit", "★ 5,0 sur l’App Store", "En 5 langues", "Fait en Belgique"],
  floats=["Instagram", "TikTok", "YouTube", "Site web", "Photo"],
  sources_label="Fonctionne avec tout ce où tu trouves des recettes",
  sources=["Instagram", "TikTok", "YouTube", "Pinterest", "Facebook", "Sites web", "Capture d’écran", "Photo d’un livre ou d’un magazine"],
  steps_title="Comment ça marche", steps_sub="Trois étapes, zéro prise de tête.",
  steps=[("Partage le reel", "Touche Partager dans Instagram ou TikTok et choisis RightSetFret."),
         ("Patiente un instant", "RightSetFret lit la vidéo, la voix et la légende et en fait des ingrédients et des étapes."),
         ("À toi de cuisiner", "Mode cuisine avec minuteurs, portions ajustables, ingrédients sur ta liste.")],
  features_title="Une seule app pour toute ta routine cuisine", features_sub="De « ça a l’air bon » à la table dressée.",
  features=[("Collection", "Un livre de recettes qui se range tout seul", "Chaque recette reçoit automatiquement des tags — cuisine, régime, saison, ingrédient principal — et tu retrouves tout avec un seul mot.", ["Tags et collections automatiques", "Recherche par titre, ingrédient ou tag", "Ajuste les portions, tout suit"]),
            ("Frigo", "Qu’est-ce que je peux cuisiner ?", "Indique ce qu’il y a dans ton frigo et vois tout de suite quelles recettes tu peux faire ce soir. Il comprend aussi les synonymes.", ["Avec ce que tu as déjà", "Les ingrédients manquants sur ta liste en un geste", "Valeurs nutritionnelles par portion"]),
            ("Semaine", "Ta semaine planifiée par l’IA", "Choisis ton régime — végétarien, pauvre en glucides, riche en protéines, keto ou un plafond de kcal — et RightSetFret compose une semaine avec tes propres recettes.", ["Variété et alternatives automatiques", "Totaux journaliers calories et macros", "Liste de courses en une fois"]),
            ("Liste", "Les courses dans l’ordre des rayons de ton magasin", "Ta liste se trie selon les rayons de ton supermarché et apprend comment tu fais tes courses. Partage une liste avec ta famille — à jour pour tout le monde.", ["Trie par magasin, continue d’apprendre", "Ajoute à la voix", "Partagée avec ta famille via un code"])],
  minis=[("Trois thèmes, ton style", "Basique, Moderne ou Classique — un geste dans les réglages."), ("Mode cuisine avec minuteurs", "Étape par étape, mains libres, un minuteur par étape.")],
  video_title="Vois-le en 40 secondes", video_sub="Du reel à la liste de courses.",
  story_title="Pourquoi RightSetFret", story_name="Bram Bollen", story_place="Genk, Belgique",
  story="Je gardais mes recettes en captures d’écran et je ne les retrouvais jamais. Alors j’ai construit l’app qui me manquait : partage un reel, et la recette est rangée dans ton livre — avec liste de courses et planning de la semaine. Je fais RightSetFret à Genk, avec beaucoup de retours des premiers cuisiniers qui l’utilisent.",
  rating_label="sur l’App Store", rating_link="Notes et avis",
  price_title="Commence gratuitement. Reste si ça te plaît.", price_sub="Tes 10 premiers imports sont gratuits. Ensuite, choisis ce qui te convient.",
  plans=[("Mensuel", "3,99 €", "par mois", "Imports illimités, planning de la semaine, liste de courses, famille.", ""),
         ("Annuel", "22,99 €", "par an · = 1,92 € par mois", "Tout le mensuel, payé une fois par an.", "Économise 52 %"),
         ("À vie", "69,99 €", "une fois", "À toi pour toujours, sans abonnement.", "")],
  plan_cta="Commencer 7 jours gratuits", plan_cta_life="Acheter l’accès à vie",
  price_foot="7 jours d’essai gratuit · annule quand tu veux · consulter et exporter tes recettes reste gratuit pour toujours.",
  faq_title="Questions fréquentes",
  faq=[("Dois-je créer un compte ?", "Non. Tu commences tout de suite. Un compte n’est nécessaire que pour la synchronisation entre appareils, la liste familiale partagée et la communauté."),
       ("Ça marche sans ouvrir l’app ?", "Oui. Partager depuis Instagram ou TikTok suffit — RightSetFret traite la recette en arrière-plan et te prévient quand la fiche est prête."),
       ("Et si le reel ne donne pas les ingrédients ?", "RightSetFret combine l’image, la voix et la légende. S’il manque quelque chose, tu le complètes dans la fiche en un geste."),
       ("RightSetFret conserve-t-il la vidéo ?", "Non. La fiche renvoie vers la vidéo originale et son auteur ; la vidéo reste sur la plateforme."),
       ("Qu’est-ce qui est gratuit ?", "Les 10 premiers imports, l’ajout manuel de recettes, et consulter et exporter ta collection. Les imports illimités, le planning IA et le partage familial sont dans l’abonnement — 7 jours d’essai gratuit."),
       ("Sur quels appareils ?", "iPhone avec iOS 26 ou plus récent. Sur iPad, c’est la version iPhone qui tourne.")],
  cta_title="Enregistre ta première recette ce soir.", cta_sub="Téléchargement gratuit. Prêt en moins d’une minute.",
  qr_label="Scanne avec ton iPhone", video="promo-fr.mp4", poster="promo-fr-poster.jpg",
  alts=dict(recept="Fiche recette avec ingrédients et étapes dans RightSetFret", deelmenu="Le menu de partage iOS avec RightSetFret en évidence", import_="Feuille « Importer une recette » avec les sources", kookmodus="Mode cuisine avec une étape et un minuteur", collectie="Collection avec recettes et tags", frigo="Écran « Qu’est-ce que je peux cuisiner ? »", planning="Planning de la semaine avec les repas par jour", lijstje="Liste de courses triée par rayon"),
 ),
 "de": dict(
  title="RightSetFret — Vom Reel zum Rezept in 5 Sekunden",
  desc="Teile ein Rezept aus Instagram, TikTok oder YouTube mit RightSetFret und erhalte sofort eine übersichtliche Rezeptkarte mit Zutaten, Schritten und Foto. Wochenplaner und Einkaufsliste inklusive. 10 Importe gratis.",
  h1="Vom Reel zum Rezept in 5 Sekunden.",
  sub="Siehst du ein Rezept auf Instagram, TikTok oder YouTube? Teile es mit RightSetFret und du hast eine saubere Karte — Zutaten, Schritte und Foto, in deiner Sprache.",
  ghost="So funktioniert’s",
  chips=["10 Importe gratis", "7 Tage kostenlos testen", "★ 5,0 im App Store", "In 5 Sprachen", "Gemacht in Belgien"],
  floats=["Instagram", "TikTok", "YouTube", "Website", "Foto"],
  sources_label="Funktioniert mit allem, wo du Rezepte findest",
  sources=["Instagram", "TikTok", "YouTube", "Pinterest", "Facebook", "Websites", "Screenshot", "Foto aus Kochbuch oder Zeitschrift"],
  steps_title="So funktioniert’s", steps_sub="Drei Schritte, kein Aufwand.",
  steps=[("Teile das Reel", "Tippe in Instagram oder TikTok auf Teilen und wähle RightSetFret."),
         ("Kurz warten", "RightSetFret liest Video, Stimme und Bildunterschrift und macht daraus Zutaten und Schritte."),
         ("Loskochen", "Kochmodus mit Timern, skalierbare Portionen, Zutaten auf deiner Liste.")],
  features_title="Eine App für deine ganze Kochroutine", features_sub="Von „das sieht lecker aus“ bis zum gedeckten Tisch.",
  features=[("Sammlung", "Ein Kochbuch, das sich selbst ordnet", "Jedes Rezept bekommt automatisch Tags — Küche, Ernährung, Saison, Hauptzutat — und du findest alles mit einem Suchwort.", ["Automatische Tags und Sammlungen", "Suche nach Titel, Zutat oder Tag", "Portionen anpassen, alles skaliert mit"]),
            ("Kühlschrank", "Was kann ich kochen?", "Gib ein, was im Kühlschrank liegt, und sieh sofort, welche Rezepte du heute Abend machen kannst. Synonyme versteht es auch.", ["Mit dem, was du schon hast", "Fehlende Zutaten mit einem Tipp auf die Liste", "Nährwerte pro Portion"]),
            ("Planung", "Deine Woche, geplant von KI", "Wähle deine Ernährung — vegetarisch, Low Carb, proteinreich, Keto oder ein kcal-Limit — und RightSetFret stellt eine Woche aus deinen eigenen Rezepten zusammen.", ["Automatische Abwechslung und Alternativen", "Tagessummen für Kalorien und Makros", "Einkaufsliste in einem Rutsch"]),
            ("Liste", "Einkaufen nach dem Laufweg deines Ladens", "Deine Liste sortiert sich nach den Gängen deines Supermarkts und lernt, wie du einkaufst. Teile eine Liste mit deiner Familie — bei allen live.", ["Sortiert pro Laden, lernt mit", "Per Sprache hinzufügen", "Mit der Familie per Code geteilt"])],
  minis=[("Drei Themes, dein Stil", "Basis, Modern oder Klassisch — ein Tipp in den Einstellungen."), ("Kochmodus mit Timern", "Schritt für Schritt, freihändig, mit Timer pro Schritt.")],
  video_title="In 40 Sekunden sehen", video_sub="Vom Reel zur Einkaufsliste.",
  story_title="Warum RightSetFret", story_name="Bram Bollen", story_place="Genk, Belgien",
  story="Ich habe Rezepte als Screenshots gespeichert und nie wiedergefunden. Also habe ich die App gebaut, die mir fehlte: Reel teilen, und das Rezept liegt ordentlich in deinem Kochbuch — mit Einkaufsliste und Wochenplanung. RightSetFret entsteht in Genk, mit viel Feedback der ersten Köche, die es nutzen.",
  rating_label="im App Store", rating_link="Bewertungen und Rezensionen",
  price_title="Gratis starten. Bleiben, wenn es gefällt.", price_sub="Deine ersten 10 Importe sind gratis. Danach wählst du, was zu dir passt.",
  plans=[("Monatlich", "3,99 €", "pro Monat", "Unbegrenzt importieren, Wochenplaner, Einkaufsliste, Familie.", ""),
         ("Jährlich", "22,99 €", "pro Jahr · = 1,92 € pro Monat", "Alles aus Monatlich, einmal im Jahr bezahlt.", "Spare 52 %"),
         ("Lebenslang", "69,99 €", "einmalig", "Für immer deins, kein Abo.", "")],
  plan_cta="7 Tage gratis starten", plan_cta_life="Lebenslang kaufen",
  price_foot="7 Tage kostenlos testen · jederzeit kündbar · Rezepte ansehen und exportieren bleibt für immer kostenlos.",
  faq_title="Häufige Fragen",
  faq=[("Brauche ich ein Konto?", "Nein. Du legst sofort los. Ein Konto brauchst du nur für Sync zwischen Geräten, die geteilte Familienliste und die Community."),
       ("Geht es, ohne die App zu öffnen?", "Ja. Teilen aus Instagram oder TikTok reicht — RightSetFret verarbeitet das Rezept im Hintergrund und meldet sich, wenn die Karte fertig ist."),
       ("Was, wenn das Reel keine Zutaten nennt?", "RightSetFret kombiniert Bild, Stimme und Bildunterschrift. Fehlt trotzdem etwas, ergänzt du es in der Karte mit einem Tipp."),
       ("Speichert RightSetFret das Video?", "Nein. Die Karte verweist auf das Original und die Urheberin oder den Urheber; das Video bleibt auf der Plattform."),
       ("Was ist gratis und was nicht?", "Die ersten 10 Importe, Rezepte von Hand anlegen, und deine Sammlung ansehen und exportieren. Unbegrenzt importieren, der KI-Wochenplaner und Familienfreigabe sind im Abo — 7 Tage kostenlos testen."),
       ("Auf welchen Geräten läuft es?", "iPhone mit iOS 26 oder neuer. Auf dem iPad läuft die iPhone-Version.")],
  cta_title="Speichere heute Abend dein erstes Rezept.", cta_sub="Kostenlos laden. In unter einer Minute startklar.",
  qr_label="Mit dem iPhone scannen", video="promo-de.mp4", poster="promo-de-poster.jpg",
  alts=dict(recept="Rezeptkarte mit Zutaten und Schritten in RightSetFret", deelmenu="Das iOS-Teilen-Menü mit RightSetFret hervorgehoben", import_="Blatt „Rezept importieren“ mit den Quellen", kookmodus="Kochmodus mit einem Schritt und Timer", collectie="Sammlung mit Rezepten und Tags", frigo="Bildschirm „Was kann ich kochen?“", planning="Wochenplan mit Mahlzeiten pro Tag", lijstje="Einkaufsliste nach Gang sortiert"),
 ),
 "es": dict(
  title="RightSetFret — Del reel a la receta en 5 segundos",
  desc="Comparte una receta de Instagram, TikTok o YouTube con RightSetFret y obtén al momento una ficha de receta clara con ingredientes, pasos y foto. Planificador semanal y lista de la compra incluidos. 10 importaciones gratis.",
  h1="Del reel a la receta en 5 segundos.",
  sub="¿Ves una receta en Instagram, TikTok o YouTube? Compártela con RightSetFret y tendrás una ficha clara: ingredientes, pasos y foto, en tu idioma.",
  ghost="Mira cómo funciona",
  chips=["10 importaciones gratis", "7 días de prueba gratis", "★ 5,0 en el App Store", "En 5 idiomas", "Hecho en Bélgica"],
  floats=["Instagram", "TikTok", "YouTube", "Web", "Foto"],
  sources_label="Funciona con todo donde encuentres recetas",
  sources=["Instagram", "TikTok", "YouTube", "Pinterest", "Facebook", "Webs", "Captura de pantalla", "Foto de un libro o revista"],
  steps_title="Cómo funciona", steps_sub="Tres pasos, sin complicaciones.",
  steps=[("Comparte el reel", "Toca Compartir en Instagram o TikTok y elige RightSetFret."),
         ("Espera un momento", "RightSetFret lee el vídeo, la voz y el pie de foto y los convierte en ingredientes y pasos."),
         ("A cocinar", "Modo cocina con temporizadores, raciones ajustables, ingredientes en tu lista.")],
  features_title="Una sola app para toda tu rutina de cocina", features_sub="De «qué buena pinta» a la mesa puesta.",
  features=[("Colección", "Un recetario que se ordena solo", "Cada receta recibe etiquetas automáticas — cocina, dieta, temporada, ingrediente principal — y encuentras todo con una palabra.", ["Etiquetas y colecciones automáticas", "Busca por título, ingrediente o etiqueta", "Ajusta raciones y todo se adapta"]),
            ("Nevera", "¿Qué puedo cocinar?", "Indica lo que tienes en la nevera y ve al momento qué recetas puedes hacer esta noche. También entiende sinónimos.", ["Con lo que ya tienes en casa", "Lo que falta, a tu lista con un toque", "Valor nutricional por ración"]),
            ("Semana", "Tu semana planificada por IA", "Elige tu dieta — vegetariana, baja en carbohidratos, rica en proteínas, keto o un tope de kcal — y RightSetFret compone una semana con tus propias recetas.", ["Variedad y alternativas automáticas", "Totales diarios de calorías y macros", "Lista de la compra de una vez"]),
            ("Lista", "La compra en el orden de los pasillos de tu tienda", "Tu lista se ordena según los pasillos de tu supermercado y aprende cómo compras. Comparte una lista con tu familia, al día para todos.", ["Ordena por tienda y sigue aprendiendo", "Añade con la voz", "Compartida con tu familia con un código"])],
  minis=[("Tres temas, tu estilo", "Básico, Moderno o Clásico: un toque en Ajustes."), ("Modo cocina con temporizadores", "Paso a paso, manos libres, con un temporizador por paso.")],
  video_title="Míralo en 40 segundos", video_sub="Del reel a la lista de la compra.",
  story_title="Por qué RightSetFret", story_name="Bram Bollen", story_place="Genk, Bélgica",
  story="Guardaba recetas como capturas de pantalla y nunca las volvía a encontrar. Así que construí la app que me faltaba: comparte un reel y la receta queda ordenada en tu recetario, con lista de la compra y planificación semanal. Hago RightSetFret en Genk, con mucha ayuda de los primeros cocineros que la usan.",
  rating_label="en el App Store", rating_link="Valoraciones y reseñas",
  price_title="Empieza gratis. Quédate si te gusta.", price_sub="Tus primeras 10 importaciones son gratis. Luego eliges lo que te convenga.",
  plans=[("Mensual", "3,99 €", "al mes", "Importaciones ilimitadas, planificador semanal, lista de la compra, familia.", ""),
         ("Anual", "22,99 €", "al año · = 1,92 € al mes", "Todo lo del mensual, pagado una vez al año.", "Ahorra 52 %"),
         ("De por vida", "69,99 €", "pago único", "Tuyo para siempre, sin suscripción.", "")],
  plan_cta="Empezar 7 días gratis", plan_cta_life="Comprar de por vida",
  price_foot="7 días de prueba gratis · cancela cuando quieras · ver y exportar tus recetas es gratis para siempre.",
  faq_title="Preguntas frecuentes",
  faq=[("¿Necesito una cuenta?", "No. Empiezas al momento. Solo necesitas una cuenta para sincronizar entre dispositivos, la lista familiar compartida y la comunidad."),
       ("¿Funciona sin abrir la app?", "Sí. Compartir desde Instagram o TikTok es suficiente: RightSetFret procesa la receta en segundo plano y te avisa cuando la ficha está lista."),
       ("¿Y si el reel no dice los ingredientes?", "RightSetFret combina la imagen, la voz y el pie de foto. Si aun así falta algo, lo completas en la ficha con un toque."),
       ("¿RightSetFret guarda el vídeo?", "No. La ficha enlaza al vídeo original y a su autor; el vídeo se queda en la plataforma."),
       ("¿Qué es gratis y qué no?", "Las primeras 10 importaciones, añadir recetas a mano, y ver y exportar tu colección. Las importaciones ilimitadas, el planificador con IA y compartir en familia están en la suscripción, con 7 días de prueba gratis."),
       ("¿En qué dispositivos funciona?", "iPhone con iOS 26 o posterior. En iPad se ejecuta la versión para iPhone.")],
  cta_title="Guarda tu primera receta esta noche.", cta_sub="Descarga gratis. Listo en menos de un minuto.",
  qr_label="Escanea con tu iPhone", video="promo-es.mp4", poster="promo-es-poster.jpg",
  alts=dict(recept="Ficha de receta con ingredientes y pasos en RightSetFret", deelmenu="El menú de compartir de iOS con RightSetFret destacado", import_="Hoja «Importar receta» con las fuentes", kookmodus="Modo cocina con un paso y temporizador", collectie="Colección con recetas y etiquetas", frigo="Pantalla «¿Qué puedo cocinar?»", planning="Plan semanal con comidas por día", lijstje="Lista de la compra ordenada por pasillo"),
 ),
}

SOURCE_ICONS = ["instagram", "tiktok", "youtube", "pinterest", "facebook", "web", "screenshot", "photo"]
FLOAT_ICONS = ["instagram", "tiktok", "youtube", "web", "photo"]
FEATURE_IMGS = ["collectie", "frigo", "planning", "lijstje"]

def render(lang):
    t = TEXT[lang]; c = CHROME[lang]
    a = lambda p: asset(lang, p)
    alt = {l: f"{LANGS[l]['dir']}index.html" for l in ORDER}
    ct = f"web_home_{lang}"
    faq_ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": ans}} for q, ans in t["faq"]]}, ensure_ascii=False)
    app_ld = json.dumps({"@context": "https://schema.org", "@type": "SoftwareApplication", "name": "RightSetFret", "operatingSystem": "iOS", "applicationCategory": "LifestyleApplication",
                         "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"}, "aggregateRating": {"@type": "AggregateRating", "ratingValue": "5.0", "ratingCount": "1"},
                         "url": f"https://apps.apple.com/app/rightsetfret/id{APP_ID}"}, ensure_ascii=False)
    extra = f'<script type="application/ld+json">{faq_ld}</script>\n<script type="application/ld+json">{app_ld}</script>'
    chips = "\n".join(f'            <li{" class=\"star\"" if ch.startswith("★") else ""}>{esc(ch)}</li>' for ch in t["chips"])
    floats = "\n".join(f'            <span class="float-chip c{i+1}">{ICON[ic]}{esc(name)}</span>' for i, (ic, name) in enumerate(zip(FLOAT_ICONS, t["floats"])))
    sources = "\n".join(f'            <li>{ICON[ic]}<span>{esc(name)}</span></li>' for ic, name in zip(SOURCE_ICONS, t["sources"]))
    step_imgs = [("deelmenu", "wide"), ("import", ""), ("kookmodus", "")]
    steps = ""
    for i, ((title, text), (img, kind)) in enumerate(zip(t["steps"], step_imgs)):
        altkey = "import_" if img == "import" else img
        media = (f'<div class="shot-wide"><img src="{a("img/deelmenu.jpg")}" alt="{esc(t["alts"]["deelmenu"])}" loading="lazy" width="760" height="443"></div>'
                 if kind == "wide" else phone(a(f"img/{img}.jpg"), t["alts"][altkey]))
        steps += f'''        <div class="step reveal">
          {media}
          <div class="num">{i+1}</div>
          <h3>{esc(title)}</h3>
          <p>{esc(text)}</p>
        </div>\n'''
    features = ""
    for (kicker, title, text, bullets), img in zip(t["features"], FEATURE_IMGS):
        li = "".join(f"<li>{esc(b)}</li>" for b in bullets)
        features += f'''        <div class="feature reveal">
          <div class="feature-media">{phone(a(f"img/{img}.jpg"), t["alts"][img])}</div>
          <div class="feature-text"><span class="kicker">{esc(kicker)}</span><h3>{esc(title)}</h3><p>{esc(text)}</p><ul>{li}</ul></div>
        </div>\n'''
    minis = "\n".join(f'          <div class="mini reveal"><h3>{esc(h)}</h3><p>{esc(p)}</p></div>' for h, p in t["minis"])
    plans = ""
    for i, (name, price, per, note, save) in enumerate(t["plans"]):
        cta = t["plan_cta_life"] if i == 2 else t["plan_cta"]
        plans += f'''        <div class="plan{" featured" if i == 1 else ""} reveal">
          {f'<span class="save">{esc(save)}</span>' if save else ""}
          <div class="name">{esc(name)}</div>
          <div class="price">{esc(price)}</div>
          <div class="per">{esc(per)}</div>
          <p class="note">{esc(note)}</p>
          <a class="btn {"btn-primary" if i == 1 else "btn-ghost"}" href="{store_link(ct + "_prijs")}">{esc(cta)}</a>
        </div>\n'''
    faq = "\n".join(f'        <details><summary>{esc(q)}</summary><div class="a">{esc(ans)}</div></details>' for q, ans in t["faq"])
    store_page = f"https://apps.apple.com/app/rightsetfret/id{APP_ID}?see-all=reviews"
    return f'''{head(lang, t["title"], t["desc"], "index.html", alt, extra=extra)}
<body>
{nav(lang)}

<header class="hero">
    <div class="wrap">
        <h1>{esc(t["h1"])}</h1>
        <p class="sub">{esc(t["sub"])}</p>
        <div class="cta">
            {badge(lang, ct)}
            <a class="btn btn-ghost" href="#video">{esc(t["ghost"])}</a>
        </div>
        <ul class="chips">
{chips}
        </ul>
        <div class="hero-stage">
{floats}
            {phone(a("img/recept.jpg"), t["alts"]["recept"])}
        </div>
    </div>
</header>

<section class="sources">
    <div class="wrap">
        <div class="label">{esc(t["sources_label"])}</div>
        <ul>
{sources}
        </ul>
    </div>
</section>

<section class="section" id="zo-werkt-het">
    <div class="wrap">
        <div class="section-head"><h2>{esc(t["steps_title"])}</h2><p>{esc(t["steps_sub"])}</p></div>
        <div class="steps">
{steps}        </div>
    </div>
</section>

<section class="section soft" id="functies">
    <div class="wrap">
        <div class="section-head"><h2>{esc(t["features_title"])}</h2><p>{esc(t["features_sub"])}</p></div>
{features}        <div class="minis">
{minis}
        </div>
    </div>
</section>

<section class="section video-sec" id="video">
    <div class="wrap">
        <div class="section-head"><h2>{esc(t["video_title"])}</h2><p>{esc(t["video_sub"])}</p></div>
        <div class="phone reveal"><div class="phone-screen"><video src="{a(t["video"])}" poster="{a(t["poster"])}" controls playsinline preload="none"></video></div></div>
    </div>
</section>

<section class="section soft">
    <div class="wrap story">
        <div class="reveal">
            <span class="kicker">{esc(t["story_title"])}</span>
            <img class="portrait" src="{a("app-icon.png")}" alt="" width="120" height="120">
            <blockquote>“{esc(t["story"])}”</blockquote>
            <div class="who">{esc(t["story_name"])} · {esc(t["story_place"])}</div>
        </div>
        <div class="rating reveal">
            <div class="stars" aria-hidden="true">★★★★★</div>
            <div class="score">5,0</div>
            <p>{esc(t["rating_label"])}</p>
            <p><a href="{store_page}">{esc(t["rating_link"])} →</a></p>
        </div>
    </div>
</section>

<section class="section" id="prijs">
    <div class="wrap">
        <div class="section-head"><h2>{esc(t["price_title"])}</h2><p>{esc(t["price_sub"])}</p></div>
        <div class="plans">
{plans}        </div>
        <p class="price-foot">{esc(t["price_foot"])}</p>
    </div>
</section>

<section class="section soft" id="faq">
    <div class="wrap">
        <div class="section-head"><h2>{esc(t["faq_title"])}</h2></div>
        <div class="faq">
{faq}
        </div>
    </div>
</section>

<section class="cta-final">
    <div class="wrap">
        <h2>{esc(t["cta_title"])}</h2>
        <p class="sub" style="color:var(--ink-2);margin-top:12px;">{esc(t["cta_sub"])}</p>
        <div class="cta">
            {badge(lang, ct + "_slot")}
            <div class="qr">{qr_svg(store_link(ct + "_qr"))}<span>{esc(t["qr_label"])}</span></div>
        </div>
    </div>
</section>

{footer(lang)}
</body>
</html>
'''

if __name__ == "__main__":
    for lang in ORDER:
        path = os.path.join(ROOT, LANGS[lang]["dir"], "index.html")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f: f.write(render(lang))
        print("geschreven", os.path.relpath(path, ROOT))
```

- [ ] **Stap 3: Genereren** — `python3 gen_site.py` → 5 × `geschreven …`. Open `http://127.0.0.1:8765/` en `/en/`: hero met telefoon, chips, secties, video, prijs, FAQ, QR.

- [ ] **Stap 4: Commit**

```bash
git add gen_site.py tools/make_og.py img/og-home.jpg index.html en/index.html fr/index.html de/index.html es/index.html
git commit -m "Homepage v2 in 5 talen uit gen_site.py"
```

---

### Taak 5: Landingspagina's op de nieuwe chrome + controlescript

**Files:**
- Modify: `gen_landing.py` (head/nav/footer/badge uit `site_common`)
- Create: `tools/check_site.py`

- [ ] **Stap 1: `gen_landing.py` laten leunen op `site_common`**

Vervang in `gen_landing.py` de eigen `PIXEL`, `BADGE_SVG`, `IG_SVG`, `store_link`, `LANG_NAMES` en de `<head>…<nav>…</nav>`-opbouw en `<footer>` in `render()` door aanroepen van `site_common.head()`, `site_common.nav(lang, current=slug)`, `site_common.badge(lang, ct)` en `site_common.footer(lang)`; de `<script defer src="/lang.js">` onderaan vervalt (zit in `footer()`). Het `alt`-woordenboek voor `head()`: `{l: f"{L[l]['dir']}{PAGES[kind][l]['slug']}" for l in ("nl","en","fr")}`. Verder ongewijzigd (hero, stappen, video, FAQ, closing).

- [ ] **Stap 2: Controlescript**

```python
"""Controleert alle HTML-pagina's: sluitende tags, interne links, afbeeldingsgroottes."""
import os, re, sys, html.parser, glob
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
VOID = {"meta", "link", "img", "br", "hr", "input", "source", "path", "rect", "circle"}
errors = []

class Checker(html.parser.HTMLParser):
    def __init__(self, path): super().__init__(); self.stack = []; self.path = path; self.hrefs = []
    def handle_starttag(self, tag, attrs):
        if tag not in VOID: self.stack.append(tag)
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
```

- [ ] **Stap 3: Draaien** — `python3 gen_landing.py && python3 tools/check_site.py` → `OK`. Bekijk `/instagram-recept-opslaan.html` en `/en/save-tiktok-recipes.html` in de browser: nieuwe nav en footer, oude inhoud.

- [ ] **Stap 4: Commit**

```bash
git add gen_landing.py tools/check_site.py *.html en/*.html fr/*.html
git commit -m "Landingspagina's op de nieuwe chrome; check_site.py"
```

---

### Taak 6: Visuele controle, sitemap, PR

- [ ] **Stap 1: Responsief** — browser op 390×844 (mobiel) en 1280 breed voor `/` en `/en/`: geen horizontale scroll (`document.documentElement.scrollWidth <= window.innerWidth`), App Store-knop zichtbaar zonder scrollen op 390×844, telefoonkaders zonder vervorming, FAQ opent/sluit, taalmenu werkt.
- [ ] **Stap 2: Sitemap** — `python3 - <<'EOF'` … voeg niets toe (paden ongewijzigd); controleer alleen dat `sitemap.xml` de 5 index-URL's bevat: `grep -c "index.html\|studioplanb.be/</loc>\|/en/</loc>" sitemap.xml`.
- [ ] **Stap 3: Push + PR**

```bash
git push -u origin feat/landingspagina-v2
gh pr create --base main --head feat/landingspagina-v2 --title "Landingspagina v2: moderne app-landing in 5 talen" --body "Spec: docs/superpowers/specs/2026-09-23-landingspagina-v2-design.md. Nieuwe homepage (stijl B) met verse app-schermen, prijs, FAQ, QR; landingspagina's op dezelfde chrome; nieuwe stylesheet. Mergen = live."
```

- [ ] **Stap 4: Overdracht** — melden: PR-link, wat de gebruiker nog levert (portretfoto → `img/portret.jpg` + `gen_site.py` regel `portrait` aanpassen; eigen 3 zinnen in `TEXT[*]["story"]`; `pt=` in `site_common.store_link`).
