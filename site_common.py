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
    canonical = f"{SITE}/{LANGS[lang]['dir']}{path}"
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
    CUR = ' aria-current="page"'
    items = "\n".join(
        f'                    <li><a href="{LANGS[l]["path"]}" hreflang="{l}"{CUR if l == lang else ""}><span class="flag">{LANGS[l]["flag"]}</span> {LANGS[l]["name"]}</a></li>'
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
