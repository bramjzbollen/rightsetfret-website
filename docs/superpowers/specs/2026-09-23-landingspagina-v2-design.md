# Landingspagina v2 — ontwerp (23-09-2026)

Repo: `bramjzbollen/rightsetfret-website` (GitHub Pages, deploy bij push naar `main`). Doel: **downloads uit BE/NL** — één belofte boven de vouw, echte app-schermen, eerlijke sociale bewijzen. Stijlrichting **B "Modern app-landing"** (gekozen 23-09): wit, luchtig, vette sans-serif kop, één grote telefoon in het midden, zachte oranje gloed.

## 1. Scope

- Nieuwe homepage in **5 talen** (nl root, `/en/`, `/fr/`, `/de/`, `/es/`), gegenereerd uit één sjabloon.
- Nieuwe stylesheet `styles.css` (vervangt de huidige) — ook de landingspagina's (Instagram/TikTok), `support.html` en `privacy.html` renderen ermee, dus hun bestaande klassen (`.doc`, `.nav`, `.lang`, `.appstore-badge`, `.card`, `.grid`, `.tutorial`, `.closing`) blijven bestaan in de nieuwe stylesheet.
- Verse app-schermen uit de simulator (build 100) als beeldmateriaal.
- Buiten scope: de tekst van support/privacy, nieuwe talen, een blog, de `pt=`-provider-token (blijft een losse actie in App Store Connect).

## 2. Ontwerptaal

| | |
|---|---|
| Achtergrond | `#ffffff`; secties afwisselend met `#f7f5f1` (warm grijs) |
| Tekst | ink `#111111`, secundair `#5f5a54` |
| Accent | oranje `#c96b2a` (knoppen, badges, highlights), hover `#a9541f`; gloed `radial-gradient(rgba(201,107,42,.28) → transparent)` |
| Typografie | systeemstack `-apple-system, "SF Pro Text", Inter, "Segoe UI", Roboto, sans-serif` (geen webfonts → snel, geen FOUT). Kop h1 `clamp(40px, 7vw, 72px)`, weight 800, letter-spacing −0.02em, line-height 1.02. h2 `clamp(28px, 4vw, 44px)`. Body 17px/1.55. |
| Ritme | container max 1120px, gutter 20px; sectie-padding 96px desktop / 64px mobiel; radius 16px (kaarten) / 999px (knoppen) |
| Knoppen | primair zwart (`#111`) met wit Apple-logo + "Download in de App Store"; secundair ghost (rand `#e5e2dd`) |
| Telefoonkader | CSS-component `.phone`: verhouding 1206:2622, radius 44px, bezel 10px `#1b1b1b`, Dynamic Island, schaduw `0 30px 60px rgba(0,0,0,.18)`; scherm = `<img>` met `object-fit: cover` |
| Beweging | fade-up bij scrollen (IntersectionObserver, 24px/500ms), zwevende bron-chips in de hero (6s ease-in-out loop). Alles uit onder `prefers-reduced-motion: reduce`. |
| Toegankelijkheid | contrast ≥ 4.5:1, focus-ringen zichtbaar, `alt` op elk scherm, FAQ als `<details>/<summary>` (toetsenbord), taalmenu `aria-expanded` (bestaand `lang.js`) |

## 3. Secties (van boven naar onder)

1. **Nav** (sticky, `backdrop-filter: blur(12px)`, 64px): logo + "RightSetFret" links; midden: Functies · Zo werkt het · Prijs · FAQ (anchors); rechts: taalmenu (bestaand) + knop "Download". Mobiel (< 820px): logo, taal, Download.
2. **Hero**: kop "Van reel naar recept in 5 seconden." · sub: "Zie je een recept op Instagram, TikTok of YouTube? Deel het met RightSetFret en je hebt een nette fiche — ingrediënten, stappen en foto, in jouw taal." · App Store-knop + ghost "Bekijk hoe het werkt" (→ #video) · vertrouwensrij van 5 chips: 10 imports gratis · 7 dagen gratis proberen · ★ 5,0 App Store · In 5 talen · Gemaakt in België · gecentreerde telefoon (`recept.jpg`) met oranje gloed eronder; rond de telefoon 5 zwevende chips met icoon+naam (Instagram, TikTok, YouTube, Website, Foto).
3. **Bronnen-strip**: label "Werkt met alles waar je recepten tegenkomt" + rij van 8 items (Instagram · TikTok · YouTube · Pinterest · Facebook · Websites · Screenshot · Foto van kookboek of tijdschrift), inline-SVG-iconen in grijs; horizontaal scrollbaar op mobiel.
4. **Zo werkt het** (`#zo-werkt-het`): 3 kolommen, elk een telefoonkader + nummer + titel + zin: 1 Deel de reel (`deelmenu.jpg`) · 2 Even wachten (`import.jpg`) · 3 Koken maar (`kookmodus.jpg`). Mobiel: onder elkaar.
5. **Functies** (`#functies`): 4 rijen, afwisselend scherm links/rechts, elk met kicker, h3, 2 zinnen, 3 bullets: Collectie die zichzelf ordent (`collectie.jpg`) · "Wat kan ik koken?" (`frigo.jpg`) · Je week gepland door AI (`planning.jpg`) · Boodschappen op de looproute van jouw winkel, gedeeld met je gezin (`lijstje.jpg`). Daaronder 2 compacte kaartjes: Drie thema's · Kookmodus met timers.
6. **Video** (`#video`): "Zie het in 40 seconden" · promo-video per taal in een telefoonkader, `preload="none"`, poster, `controls`; gecentreerd, max 360px breed.
7. **Waarom RightSetFret**: 2 kolommen: links portret (rond, 160px) + naam "Bram Bollen · Genk, België" + 3 zinnen (voorzet in §6, door Bram aan te passen); rechts kaart "★ 5,0 in de App Store" + "Beoordelingen en recensies — RightSetFret" link naar de store. **Zolang er geen portretfoto is, staat op die plek het app-icoon** (geen stockfoto, geen verzonnen persoon).
8. **Prijs** (`#prijs`): kop "Begin gratis. Blijf als het bevalt." · 3 kaarten: Maandelijks €3,99 · **Jaarlijks €22,99** (uitgelicht, badge "Bespaar 52 %", "= €1,92 per maand") · Levenslang €69,99 (eenmalig) · onder: "10 imports gratis om te starten · 7 dagen gratis proberen · annuleer wanneer je wil · je recepten bekijken en exporteren blijft altijd gratis". Prijzen per taal identiek (€), en-US toont "€3.99" (App Store rekent lokaal af — voetnoot).
9. **FAQ** (`#faq`): 6 `<details>`: Moet ik een account maken? (Nee — pas nodig voor sync, gezinslijst en community) · Werkt het zonder de app te openen? · Wat als de reel geen ingrediënten noemt? · Bewaart RightSetFret de video? · Wat is gratis en wat niet? · Op welke toestellen werkt het? (iPhone, iOS 26 of nieuwer; iPad via iPhone-app) — plus FAQPage-JSON-LD.
10. **Slot-CTA + footer**: "Bewaar vanavond je eerste recept." · App Store-knop · QR-code (SVG, inline gegenereerd uit de campagnelink) met "Scan met je iPhone" · footer: Lees ook (Instagram-/TikTok-pagina) · Support · Privacy · Instagram · © 2026 PLAN B · Belgium.

Campagnelinks: `https://apps.apple.com/app/apple-store/id6784261188?ct=web_home_<lang>&mt=8` (hero en slot; `pt=` later toevoegen in de generator).

## 4. Beeldmateriaal

Verse schermen uit de simulator "iPhone 17 Pro" met build 100 (1206×2622), met `xcrun simctl io <udid> screenshot`, daarna verkleind naar 780px breed als JPEG (kwaliteit 82, ≈ 100–150 KB) in `img/`:
`recept.jpg` (receptfiche, Steak tartaar) · `collectie.jpg` (Collectie met 4+ recepten, zonder startkaart) · `frigo.jpg` (Frigo/"Wat kan ik koken?") · `planning.jpg` · `lijstje.jpg` · `kookmodus.jpg` · `import.jpg` (sheet "Recept importeren") · `deelmenu.jpg` (uit de bestaande asset `tutorial-share-sheet` in de app-repo).
Voor de andere talen worden dezelfde (Nederlandstalige) schermen gebruikt — de app is meertalig, maar aparte screenshot-sets per taal zijn een vervolgstap.

## 5. Techniek

- `gen_site.py` in de repo-root: één Python-sjabloon (f-strings, `html.escape`) met een `TEXT[lang]`-woordenboek voor nl/en/fr/de/es → schrijft `index.html`, `en/index.html`, … Bestaande `gen_landing.py` blijft voor de landingspagina's; beide gebruiken dezelfde nav/footer-fragmenten (gedeelde module `site_common.py`) zodat alle pagina's één navigatie hebben.
- `styles.css` volledig nieuw (≈ 500 regels), `lang.js` ongewijzigd, `reveal.js` (nieuw, 20 regels) voor de scroll-animatie.
- Geen build-stap, geen framework, geen externe fonts of scripts (behalve de bestaande Meta-pixel).
- Head per pagina blijft: `<title>`, description, canonical, hreflang ×5 + x-default, OG-tags (og:image = `img/og-home.jpg` 1200×630, gemaakt van `recept.jpg` op oranje gloed), favicon, JSON-LD SoftwareApplication + FAQPage, Meta-pixel.
- `sitemap.xml` blijft; nieuwe `img/`-map.

## 6. Voorzet "Waarom RightSetFret" (nl; Bram past aan)

> Ik bewaarde recepten als screenshots en vond ze nooit terug. Dus bouwde ik de app die ik zelf miste: deel een reel, en het recept staat netjes in je kookboek — met boodschappenlijst en weekplanning erbij. RightSetFret maak ik in Genk, met veel input van de eerste kokers die hem gebruiken.

## 7. Kwaliteitscontrole

- `python3 gen_site.py` genereert 5 pagina's zonder fouten; `python3 -m html.parser`-check op elke pagina (geen open tags); interne-linkcheck (alle `href` zonder `http` bestaan in de repo).
- Visuele controle in de browser op 390px en 1280px voor nl en en: geen horizontale scroll, hero-knop boven de vouw op 390×844, telefoonkaders zonder vervorming.
- Afbeeldingen ≤ 200 KB per stuk, totale homepage-payload (zonder video) ≤ 1,5 MB.
- Lighthouse-achtige checks handmatig: `alt`-teksten, kopvolgorde h1→h2→h3, contrast van chips en secundaire tekst.
- Na merge: live-URL's (5 talen) geven 200; hreflang-koppen wijzen naar bestaande pagina's.
