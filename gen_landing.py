#!/usr/bin/env python3
"""Genereert SEO-landingspagina's (Instagram / TikTok) voor nl, en, fr, de, es in de
website-repo, plus sitemap.xml en robots.txt. Bron van waarheid: dit script."""
import os, json, re, html
from site_common import head as sc_head, nav as sc_nav, footer as sc_footer, badge as sc_badge
ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = "https://rightsetfret.studioplanb.be"
APP_ID = "6784261188"

def store_link(ct):  # App Store-campagnelink (voeg later pt=<provider token> toe voor attributie in ASC)
    return f"https://apps.apple.com/app/apple-store/id{APP_ID}?ct={ct}&mt=8"

PIXEL = """<!-- Meta Pixel Code -->
<script>
!function(f,b,e,v,n,t,s)
{if(f.fbq)return;n=f.fbq=function(){n.callMethod?
n.callMethod.apply(n,arguments):n.queue.push(arguments)};
if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
n.queue=[];t=b.createElement(e);t.async=!0;
t.src=v;s=b.getElementsByTagName(e)[0];
s.parentNode.insertBefore(t,s)}(window, document,'script',
'https://connect.facebook.net/en_US/fbevents.js');
fbq('init', '1018910594260070');
fbq('track', 'PageView');
</script>
<noscript><img height="1" width="1" style="display:none"
src="https://www.facebook.com/tr?id=1018910594260070&ev=PageView&noscript=1"
/></noscript>
<!-- End Meta Pixel Code -->"""


L = {
 "nl": dict(dir="", code="NL", flag="🇳🇱", support="Support", privacy="Privacybeleid", privacy_nav="Privacy",
            badge_small="Download in de", badge_big="App Store", aria_dl="Download RightSetFret in de App Store",
            soon="Gratis te downloaden · 10 imports gratis · daarna 7 dagen gratis proberen",
            steps_title="Zo werkt het", steps_sub="Drie stappen, geen gedoe.",
            video_title="Zie het in actie", faq_title="Veelgestelde vragen",
            closing_title="Probeer het vanavond", closing_sub="Download RightSetFret en bewaar je eerste recept in minder dan een minuut.",
            closing_soon="Je recepten bekijken en exporteren blijft altijd gratis", legal="© 2026 PLAN B · Belgium",
            more="Lees ook", video="tutorial-import_tutorial.mp4", poster="tutorial-import_tutorial.jpg",
            also="Werkt net zo goed met TikTok, Pinterest, Facebook, YouTube, elke receptwebsite, een screenshot of een foto uit een tijdschrift.",
            also_q="Werkt dit ook met TikTok, YouTube of gewone websites?",
            also_a="Ja. RightSetFret importeert van Instagram, TikTok, Pinterest, Facebook en YouTube, van elke receptwebsite, en zelfs van een screenshot of een foto van een kookboek of tijdschrift. Plak de link of deel de foto — de fiche komt er hetzelfde uit."),
 "en": dict(dir="en/", code="EN", flag="🇬🇧", support="Support", privacy="Privacy Policy", privacy_nav="Privacy",
            badge_small="Download on the", badge_big="App Store", aria_dl="Download RightSetFret on the App Store",
            soon="Free to download · 10 free imports · then a 7-day free trial",
            steps_title="How it works", steps_sub="Three steps, no fuss.",
            video_title="See it in action", faq_title="Frequently asked questions",
            closing_title="Try it tonight", closing_sub="Download RightSetFret and save your first recipe in under a minute.",
            closing_soon="Viewing and exporting your recipes stays free forever", legal="© 2026 PLAN B · Belgium",
            more="Read next", video="en/tutorial-import_tutorial-en.mp4", poster="en/tutorial-import_tutorial-en.jpg",
            also="Works just as well with TikTok, Pinterest, Facebook, YouTube, any recipe website, a screenshot or a photo from a magazine.",
            also_q="Does it also work with TikTok, YouTube or regular websites?",
            also_a="Yes. RightSetFret imports from Instagram, TikTok, Pinterest, Facebook and YouTube, from any recipe website, and even from a screenshot or a photo of a cookbook or magazine. Paste the link or share the photo — the card comes out the same."),
 "fr": dict(dir="fr/", code="FR", flag="🇫🇷", support="Support", privacy="Politique de confidentialité", privacy_nav="Confidentialité",
            badge_small="Télécharger dans l’", badge_big="App Store", aria_dl="Télécharger RightSetFret dans l’App Store",
            soon="Téléchargement gratuit · 10 imports gratuits · puis 7 jours d’essai gratuit",
            steps_title="Comment ça marche", steps_sub="Trois étapes, zéro prise de tête.",
            video_title="En action", faq_title="Questions fréquentes",
            closing_title="Essaie-le ce soir", closing_sub="Télécharge RightSetFret et enregistre ta première recette en moins d’une minute.",
            closing_soon="Consulter et exporter tes recettes reste gratuit pour toujours", legal="© 2026 PLAN B · Belgium",
            more="À lire aussi", video="tutorial-import_tutorial.mp4", poster="tutorial-import_tutorial.jpg",
            also="Fonctionne aussi bien avec TikTok, Pinterest, Facebook, YouTube, n’importe quel site de recettes, une capture d’écran ou une photo de magazine.",
            also_q="Ça marche aussi avec TikTok, YouTube ou les sites web ?",
            also_a="Oui. RightSetFret importe depuis Instagram, TikTok, Pinterest, Facebook et YouTube, depuis n’importe quel site de recettes, et même depuis une capture d’écran ou une photo de livre ou de magazine. Colle le lien ou partage la photo — la fiche est la même."),
 "de": dict(dir="de/", code="DE", flag="🇩🇪", support="Support", privacy="Datenschutzerklärung", privacy_nav="Datenschutz",
            badge_small="Laden im", badge_big="App Store", aria_dl="RightSetFret im App Store laden",
            soon="Kostenlos laden · 10 Importe gratis · danach 7 Tage kostenlos testen",
            steps_title="So funktioniert’s", steps_sub="Drei Schritte, kein Aufwand.",
            video_title="In Aktion", faq_title="Häufige Fragen",
            closing_title="Probier’s heute Abend", closing_sub="Lade RightSetFret und speichere dein erstes Rezept in unter einer Minute.",
            closing_soon="Rezepte ansehen und exportieren bleibt für immer kostenlos", legal="© 2026 PLAN B · Belgium",
            more="Auch lesen", video="tutorial-import_tutorial.mp4", poster="tutorial-import_tutorial.jpg",
            also="Funktioniert genauso mit TikTok, Pinterest, Facebook, YouTube, jeder Rezept-Website, einem Screenshot oder einem Foto aus einer Zeitschrift.",
            also_q="Geht das auch mit TikTok, YouTube oder normalen Websites?",
            also_a="Ja. RightSetFret importiert aus Instagram, TikTok, Pinterest, Facebook und YouTube, von jeder Rezept-Website und sogar aus einem Screenshot oder einem Foto aus Kochbuch oder Zeitschrift. Link einfügen oder Foto teilen – die Karte sieht gleich aus."),
 "es": dict(dir="es/", code="ES", flag="🇪🇸", support="Soporte", privacy="Política de privacidad", privacy_nav="Privacidad",
            badge_small="Descargar en el", badge_big="App Store", aria_dl="Descargar RightSetFret en el App Store",
            soon="Descarga gratis · 10 importaciones gratis · luego 7 días de prueba gratis",
            steps_title="Cómo funciona", steps_sub="Tres pasos, sin complicaciones.",
            video_title="En acción", faq_title="Preguntas frecuentes",
            closing_title="Pruébalo esta noche", closing_sub="Descarga RightSetFret y guarda tu primera receta en menos de un minuto.",
            closing_soon="Ver y exportar tus recetas es gratis para siempre", legal="© 2026 PLAN B · Belgium",
            more="Lee también", video="tutorial-import_tutorial.mp4", poster="tutorial-import_tutorial.jpg",
            also="Funciona igual de bien con TikTok, Pinterest, Facebook, YouTube, cualquier web de recetas, una captura de pantalla o una foto de una revista.",
            also_q="¿Funciona también con TikTok, YouTube o webs normales?",
            also_a="Sí. RightSetFret importa desde Instagram, TikTok, Pinterest, Facebook y YouTube, desde cualquier web de recetas e incluso desde una captura o una foto de un libro o revista. Pega el enlace o comparte la foto: la ficha queda igual."),
}

# Per pagina: slug per taal, teksten. {P} = platform-naam.
PAGES = {
 "instagram": {
  "nl": dict(slug="instagram-recept-opslaan.html", ct="web_ig_nl",
    title="Instagram-recept opslaan als receptfiche — RightSetFret",
    desc="Bewaar recepten van Instagram-reels in seconden als een nette receptfiche met ingrediënten, stappen en foto. Deel de reel met RightSetFret — klaar.",
    h1="Recepten van Instagram bewaren, in seconden",
    tagline="Zie je een reel met een recept? Deel hem met RightSetFret en je krijgt een nette fiche met ingrediënten, stappen en foto — in jouw taal. Geen screenshots meer, geen gescrol door bijschriften.",
    steps=[("📲","Tik op Delen onder de reel","Open de reel in Instagram, tik op het deel-icoon en kies RightSetFret in het deelmenu."),
           ("✨","Even wachten","RightSetFret leest de video, de gesproken tekst en het bijschrift en zet alles om in ingrediënten en stappen."),
           ("🍳","Koken maar","Je recept staat in je collectie: schaal de porties, zet ingrediënten op je lijstje of plan het in je week.")],
    faq=[("Moet ik de app openen om een reel te bewaren?","Nee. Delen vanuit Instagram is genoeg — RightSetFret verwerkt het recept op de achtergrond en meldt zich als de fiche klaar is."),
         ("Wat als de reel geen ingrediënten noemt?","RightSetFret combineert beeld, gesproken tekst en bijschrift. Ontbreekt er toch iets, dan vul je het zo aan in de fiche."),
         ("Is Instagram-recepten opslaan gratis?","De eerste 10 imports zijn gratis. Daarna kies je een abonnement met 7 dagen gratis proberen. Bewaarde recepten bekijken en exporteren blijft altijd gratis."),
         ("Bewaart RightSetFret de video?","Nee. De fiche verwijst naar de originele reel en de maker; de video zelf blijft op Instagram.")]),
  "en": dict(slug="save-instagram-recipes.html", ct="web_ig_en",
    title="Save Instagram recipes as recipe cards — RightSetFret",
    desc="Turn Instagram reels into clean recipe cards with ingredients, steps and a photo in seconds. Share the reel to RightSetFret — done.",
    h1="Save recipes from Instagram in seconds",
    tagline="Spotted a reel with a recipe? Share it to RightSetFret and get a clean card with ingredients, steps and a photo — in your language. No more screenshots, no more scrolling through captions.",
    steps=[("📲","Tap Share under the reel","Open the reel in Instagram, tap the share icon and pick RightSetFret in the share sheet."),
           ("✨","Give it a moment","RightSetFret reads the video, the spoken audio and the caption, and turns it all into ingredients and steps."),
           ("🍳","Start cooking","Your recipe is in your collection: scale the servings, add ingredients to your list or plan it into your week.")],
    faq=[("Do I have to open the app to save a reel?","No. Sharing from Instagram is enough — RightSetFret processes the recipe in the background and lets you know when the card is ready."),
         ("What if the reel doesn't list the ingredients?","RightSetFret combines the visuals, the spoken audio and the caption. If something is still missing, you add it to the card in a tap."),
         ("Is saving Instagram recipes free?","Your first 10 imports are free. After that you pick a subscription with a 7-day free trial. Viewing and exporting saved recipes stays free forever."),
         ("Does RightSetFret store the video?","No. The card links to the original reel and its creator; the video itself stays on Instagram.")]),
  "fr": dict(slug="enregistrer-recettes-instagram.html", ct="web_ig_fr",
    title="Enregistrer une recette Instagram en fiche recette — RightSetFret",
    desc="Transforme les reels Instagram en fiches recette claires avec ingrédients, étapes et photo, en quelques secondes. Partage le reel vers RightSetFret — c’est fait.",
    h1="Enregistre les recettes d’Instagram en quelques secondes",
    tagline="Tu vois passer un reel avec une recette ? Partage-le vers RightSetFret et tu obtiens une fiche soignée avec ingrédients, étapes et photo — dans ta langue. Fini les captures d’écran et les légendes à faire défiler.",
    steps=[("📲","Touche Partager sous le reel","Ouvre le reel dans Instagram, touche l’icône de partage et choisis RightSetFret dans le menu."),
           ("✨","Patiente un instant","RightSetFret lit la vidéo, la voix et la légende, et transforme le tout en ingrédients et en étapes."),
           ("🍳","À toi de cuisiner","Ta recette est dans ta collection : ajuste les portions, ajoute les ingrédients à ta liste ou planifie-la dans ta semaine.")],
    faq=[("Dois-je ouvrir l’app pour enregistrer un reel ?","Non. Partager depuis Instagram suffit — RightSetFret traite la recette en arrière-plan et te prévient quand la fiche est prête."),
         ("Et si le reel ne donne pas les ingrédients ?","RightSetFret combine l’image, la voix et la légende. S’il manque encore quelque chose, tu le complètes dans la fiche en un geste."),
         ("Enregistrer des recettes Instagram, c’est gratuit ?","Les 10 premiers imports sont gratuits. Ensuite tu choisis un abonnement avec 7 jours d’essai gratuit. Consulter et exporter tes recettes reste gratuit pour toujours."),
         ("RightSetFret conserve-t-il la vidéo ?","Non. La fiche renvoie vers le reel original et son auteur ; la vidéo reste sur Instagram.")]),

  "de": dict(slug="rezepte-aus-instagram-speichern.html", ct="web_ig_de",
    title="Instagram-Rezept als Rezeptkarte speichern — RightSetFret",
    desc="Verwandle Instagram-Reels in Sekunden in übersichtliche Rezeptkarten mit Zutaten, Schritten und Foto. Reel mit RightSetFret teilen – fertig.",
    h1="Rezepte aus Instagram in Sekunden speichern",
    tagline="Siehst du ein Reel mit einem Rezept? Teile es mit RightSetFret und du bekommst eine saubere Karte mit Zutaten, Schritten und Foto – in deiner Sprache. Keine Screenshots mehr, kein Scrollen durch Bildunterschriften.",
    steps=[("📲","Tippe unter dem Reel auf Teilen","Öffne das Reel in Instagram, tippe auf das Teilen-Symbol und wähle RightSetFret im Menü."),
           ("✨","Kurz warten","RightSetFret liest Video, Stimme und Bildunterschrift und macht daraus Zutaten und Schritte."),
           ("🍳","Loskochen","Dein Rezept ist in deiner Sammlung: Portionen anpassen, Zutaten auf die Liste setzen oder in die Woche einplanen.")],
    faq=[("Muss ich die App öffnen, um ein Reel zu speichern?","Nein. Teilen aus Instagram reicht – RightSetFret verarbeitet das Rezept im Hintergrund und meldet sich, wenn die Karte fertig ist."),
         ("Was, wenn das Reel keine Zutaten nennt?","RightSetFret kombiniert Bild, Stimme und Bildunterschrift. Fehlt trotzdem etwas, ergänzt du es in der Karte mit einem Tipp."),
         ("Ist das Speichern von Instagram-Rezepten kostenlos?","Die ersten 10 Importe sind gratis. Danach wählst du ein Abo mit 7 Tagen kostenlos testen. Gespeicherte Rezepte ansehen und exportieren bleibt für immer kostenlos."),
         ("Speichert RightSetFret das Video?","Nein. Die Karte verweist auf das Original-Reel und seine Urheberin oder seinen Urheber; das Video bleibt auf Instagram.")]),
  "es": dict(slug="guardar-recetas-de-instagram.html", ct="web_ig_es",
    title="Guardar una receta de Instagram como ficha — RightSetFret",
    desc="Convierte los reels de Instagram en fichas de receta claras con ingredientes, pasos y foto, en segundos. Comparte el reel con RightSetFret y listo.",
    h1="Guarda recetas de Instagram en segundos",
    tagline="¿Ves un reel con una receta? Compártelo con RightSetFret y tendrás una ficha clara con ingredientes, pasos y foto, en tu idioma. Se acabaron las capturas y el scroll por los pies de foto.",
    steps=[("📲","Toca Compartir bajo el reel","Abre el reel en Instagram, toca el icono de compartir y elige RightSetFret en el menú."),
           ("✨","Espera un momento","RightSetFret lee el vídeo, la voz y el pie de foto y los convierte en ingredientes y pasos."),
           ("🍳","A cocinar","Tu receta está en tu colección: ajusta las raciones, pon los ingredientes en tu lista o planifícala en tu semana.")],
    faq=[("¿Tengo que abrir la app para guardar un reel?","No. Compartir desde Instagram es suficiente: RightSetFret procesa la receta en segundo plano y te avisa cuando la ficha está lista."),
         ("¿Y si el reel no dice los ingredientes?","RightSetFret combina la imagen, la voz y el pie de foto. Si aun así falta algo, lo completas en la ficha con un toque."),
         ("¿Guardar recetas de Instagram es gratis?","Las primeras 10 importaciones son gratis. Luego eliges una suscripción con 7 días de prueba gratis. Ver y exportar tus recetas guardadas es gratis para siempre."),
         ("¿RightSetFret guarda el vídeo?","No. La ficha enlaza al reel original y a su autor; el vídeo se queda en Instagram.")]),
 },
 "tiktok": {
  "nl": dict(slug="tiktok-recept-bewaren.html", ct="web_tt_nl",
    title="TikTok-recept bewaren als receptfiche — RightSetFret",
    desc="Bewaar recepten van TikTok-video's in seconden als een nette receptfiche met ingrediënten, stappen en foto. Deel de video met RightSetFret — klaar.",
    h1="Recepten van TikTok bewaren, in seconden",
    tagline="Een TikTok met een recept dat je wil onthouden? Deel hem met RightSetFret en je krijgt een nette fiche met ingrediënten, stappen en foto — in jouw taal. Nooit meer een video terugzoeken.",
    steps=[("📲","Tik op Delen naast de video","Open de video in TikTok, tik op de deelpijl en kies RightSetFret in het deelmenu."),
           ("✨","Even wachten","RightSetFret leest de video, de gesproken tekst en het bijschrift en zet alles om in ingrediënten en stappen."),
           ("🍳","Koken maar","Je recept staat in je collectie: schaal de porties, zet ingrediënten op je lijstje of plan het in je week.")],
    faq=[("Moet ik de app openen om een TikTok te bewaren?","Nee. Delen vanuit TikTok is genoeg — RightSetFret verwerkt het recept op de achtergrond en meldt zich als de fiche klaar is."),
         ("Werkt het ook als de hoeveelheden alleen worden uitgesproken?","Ja. RightSetFret luistert naar de gesproken tekst en combineert die met beeld en bijschrift. Ontbreekt er iets, dan vul je het zo aan."),
         ("Is TikTok-recepten bewaren gratis?","De eerste 10 imports zijn gratis. Daarna kies je een abonnement met 7 dagen gratis proberen. Bewaarde recepten bekijken en exporteren blijft altijd gratis."),
         ("Bewaart RightSetFret de video?","Nee. De fiche verwijst naar de originele video en de maker; de video zelf blijft op TikTok.")]),
  "en": dict(slug="save-tiktok-recipes.html", ct="web_tt_en",
    title="Save TikTok recipes as recipe cards — RightSetFret",
    desc="Turn TikTok videos into clean recipe cards with ingredients, steps and a photo in seconds. Share the video to RightSetFret — done.",
    h1="Save recipes from TikTok in seconds",
    tagline="A TikTok with a recipe you want to keep? Share it to RightSetFret and get a clean card with ingredients, steps and a photo — in your language. Never dig through your liked videos again.",
    steps=[("📲","Tap Share next to the video","Open the video in TikTok, tap the share arrow and pick RightSetFret in the share sheet."),
           ("✨","Give it a moment","RightSetFret reads the video, the spoken audio and the caption, and turns it all into ingredients and steps."),
           ("🍳","Start cooking","Your recipe is in your collection: scale the servings, add ingredients to your list or plan it into your week.")],
    faq=[("Do I have to open the app to save a TikTok?","No. Sharing from TikTok is enough — RightSetFret processes the recipe in the background and lets you know when the card is ready."),
         ("Does it work when the amounts are only spoken?","Yes. RightSetFret listens to the spoken audio and combines it with the visuals and the caption. If something is missing, you add it in a tap."),
         ("Is saving TikTok recipes free?","Your first 10 imports are free. After that you pick a subscription with a 7-day free trial. Viewing and exporting saved recipes stays free forever."),
         ("Does RightSetFret store the video?","No. The card links to the original video and its creator; the video itself stays on TikTok.")]),
  "fr": dict(slug="enregistrer-recettes-tiktok.html", ct="web_tt_fr",
    title="Enregistrer une recette TikTok en fiche recette — RightSetFret",
    desc="Transforme les vidéos TikTok en fiches recette claires avec ingrédients, étapes et photo, en quelques secondes. Partage la vidéo vers RightSetFret — c’est fait.",
    h1="Enregistre les recettes de TikTok en quelques secondes",
    tagline="Un TikTok avec une recette à retenir ? Partage-le vers RightSetFret et tu obtiens une fiche soignée avec ingrédients, étapes et photo — dans ta langue. Fini de fouiller dans tes vidéos aimées.",
    steps=[("📲","Touche Partager à côté de la vidéo","Ouvre la vidéo dans TikTok, touche la flèche de partage et choisis RightSetFret dans le menu."),
           ("✨","Patiente un instant","RightSetFret lit la vidéo, la voix et la légende, et transforme le tout en ingrédients et en étapes."),
           ("🍳","À toi de cuisiner","Ta recette est dans ta collection : ajuste les portions, ajoute les ingrédients à ta liste ou planifie-la dans ta semaine.")],
    faq=[("Dois-je ouvrir l’app pour enregistrer un TikTok ?","Non. Partager depuis TikTok suffit — RightSetFret traite la recette en arrière-plan et te prévient quand la fiche est prête."),
         ("Ça marche si les quantités sont seulement dites à l’oral ?","Oui. RightSetFret écoute la voix et la combine avec l’image et la légende. S’il manque quelque chose, tu le complètes en un geste."),
         ("Enregistrer des recettes TikTok, c’est gratuit ?","Les 10 premiers imports sont gratuits. Ensuite tu choisis un abonnement avec 7 jours d’essai gratuit. Consulter et exporter tes recettes reste gratuit pour toujours."),
         ("RightSetFret conserve-t-il la vidéo ?","Non. La fiche renvoie vers la vidéo originale et son auteur ; la vidéo reste sur TikTok.")]),

  "de": dict(slug="rezepte-aus-tiktok-speichern.html", ct="web_tt_de",
    title="TikTok-Rezept als Rezeptkarte speichern — RightSetFret",
    desc="Verwandle TikTok-Videos in Sekunden in übersichtliche Rezeptkarten mit Zutaten, Schritten und Foto. Video mit RightSetFret teilen – fertig.",
    h1="Rezepte aus TikTok in Sekunden speichern",
    tagline="Ein TikTok mit einem Rezept, das du dir merken willst? Teile es mit RightSetFret und du bekommst eine saubere Karte mit Zutaten, Schritten und Foto – in deiner Sprache. Nie wieder in gelikten Videos wühlen.",
    steps=[("📲","Tippe neben dem Video auf Teilen","Öffne das Video in TikTok, tippe auf den Teilen-Pfeil und wähle RightSetFret im Menü."),
           ("✨","Kurz warten","RightSetFret liest Video, Stimme und Bildunterschrift und macht daraus Zutaten und Schritte."),
           ("🍳","Loskochen","Dein Rezept ist in deiner Sammlung: Portionen anpassen, Zutaten auf die Liste setzen oder in die Woche einplanen.")],
    faq=[("Muss ich die App öffnen, um ein TikTok zu speichern?","Nein. Teilen aus TikTok reicht – RightSetFret verarbeitet das Rezept im Hintergrund und meldet sich, wenn die Karte fertig ist."),
         ("Klappt es, wenn die Mengen nur gesprochen werden?","Ja. RightSetFret hört die Stimme und kombiniert sie mit Bild und Bildunterschrift. Fehlt etwas, ergänzt du es mit einem Tipp."),
         ("Ist das Speichern von TikTok-Rezepten kostenlos?","Die ersten 10 Importe sind gratis. Danach wählst du ein Abo mit 7 Tagen kostenlos testen. Gespeicherte Rezepte ansehen und exportieren bleibt für immer kostenlos."),
         ("Speichert RightSetFret das Video?","Nein. Die Karte verweist auf das Originalvideo und seine Urheberin oder seinen Urheber; das Video bleibt auf TikTok.")]),
  "es": dict(slug="guardar-recetas-de-tiktok.html", ct="web_tt_es",
    title="Guardar una receta de TikTok como ficha — RightSetFret",
    desc="Convierte los vídeos de TikTok en fichas de receta claras con ingredientes, pasos y foto, en segundos. Comparte el vídeo con RightSetFret y listo.",
    h1="Guarda recetas de TikTok en segundos",
    tagline="¿Un TikTok con una receta que quieres recordar? Compártelo con RightSetFret y tendrás una ficha clara con ingredientes, pasos y foto, en tu idioma. Nunca más rebuscar entre tus vídeos guardados.",
    steps=[("📲","Toca Compartir junto al vídeo","Abre el vídeo en TikTok, toca la flecha de compartir y elige RightSetFret en el menú."),
           ("✨","Espera un momento","RightSetFret lee el vídeo, la voz y el pie de foto y los convierte en ingredientes y pasos."),
           ("🍳","A cocinar","Tu receta está en tu colección: ajusta las raciones, pon los ingredientes en tu lista o planifícala en tu semana.")],
    faq=[("¿Tengo que abrir la app para guardar un TikTok?","No. Compartir desde TikTok es suficiente: RightSetFret procesa la receta en segundo plano y te avisa cuando la ficha está lista."),
         ("¿Funciona si las cantidades solo se dicen en voz alta?","Sí. RightSetFret escucha la voz y la combina con la imagen y el pie de foto. Si falta algo, lo completas con un toque."),
         ("¿Guardar recetas de TikTok es gratis?","Las primeras 10 importaciones son gratis. Luego eliges una suscripción con 7 días de prueba gratis. Ver y exportar tus recetas guardadas es gratis para siempre."),
         ("¿RightSetFret guarda el vídeo?","No. La ficha enlaza al vídeo original y a su autor; el vídeo se queda en TikTok.")]),
 },
}
LANG_NAMES = [("nl","🇳🇱","Nederlands","/"),("en","🇬🇧","English","/en/"),("fr","🇫🇷","Français","/fr/"),("de","🇩🇪","Deutsch","/de/"),("es","🇪🇸","Español","/es/")]

def url(lang, slug): return f"{SITE}/{L[lang]['dir']}{slug}"

def render(kind, lang):
    p = PAGES[kind][lang]; l = L[lang]; other = "tiktok" if kind == "instagram" else "instagram"
    asset = "" if lang == "nl" else "/"            # subfolders verwijzen naar root-assets zoals en/index.html
    hreflang = "\n".join(f'<link rel="alternate" hreflang="{lg}" href="{url(lg, PAGES[kind][lg]["slug"])}">' for lg in ("nl","en","fr","de","es"))
    hreflang += f'\n<link rel="alternate" hreflang="x-default" href="{url("nl", PAGES[kind]["nl"]["slug"])}">'
    CUR = ' aria-current="page"'
    langlist = "\n".join(f'                    <li><a href="{path}" hreflang="{lg}"{CUR if lg==lang else ""}><span class="flag">{fl}</span> {nm}</a></li>' for lg,fl,nm,path in LANG_NAMES)
    steps = "\n".join(f'''        <div class="card">
            <div class="emoji">{e}</div>
            <h3>{i+1}. {html.escape(t)}</h3>
            <p>{html.escape(b)}</p>
        </div>''' for i,(e,t,b) in enumerate(p["steps"]))
    faqs = p["faq"] + [(l["also_q"], l["also_a"])]
    faq_html = "\n".join(f'''        <h3 style="font-family:Georgia,serif;font-size:18px;margin-top:18px;">{html.escape(q)}</h3>
        <p>{html.escape(a)}</p>''' for q,a in faqs)
    faq_ld = json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faqs]}, ensure_ascii=False)
    app_ld = json.dumps({"@context":"https://schema.org","@type":"SoftwareApplication","name":"RightSetFret","operatingSystem":"iOS","applicationCategory":"LifestyleApplication",
                         "offers":{"@type":"Offer","price":"0","priceCurrency":"EUR"},"url":f"https://apps.apple.com/app/rightsetfret/id{APP_ID}"}, ensure_ascii=False)
    alt = {lg: f"{L[lg]['dir']}{PAGES[kind][lg]['slug']}" for lg in ("nl","en","fr","de","es")}
    extra = f'<script type="application/ld+json">{faq_ld}</script>\n<script type="application/ld+json">{app_ld}</script>'
    head_html = sc_head(lang, p["title"], p["desc"], p["slug"], alt, extra=extra)
    nav_html = sc_nav(lang, current=p["slug"])
    badge = sc_badge(lang, p["ct"])
    return f'''{head_html}
<body>
{nav_html}

<header class="hero">
    <img class="icon" src="{asset}app-icon.png" alt="RightSetFret">
    <h1>{html.escape(p["h1"])}</h1>
    <p class="tagline">{html.escape(p["tagline"])}</p>
    <p class="tagline">{html.escape(l["also"])}</p>
    <div class="cta">
        {badge}
        <a class="btn btn-ghost" href="#stappen">{l["steps_title"]}</a>
    </div>
    <p class="soon">{l["soon"]}</p>
</header>

<main class="wrap features" id="stappen">
    <h2 class="section-title">{l["steps_title"]}</h2>
    <p class="section-sub">{l["steps_sub"]}</p>
    <div class="grid">
{steps}
    </div>
</main>

<section class="wrap tutorials">
    <h2 class="section-title">{l["video_title"]}</h2>
    <div class="grid tutorial-grid" style="grid-template-columns: minmax(0, 360px); justify-content: center;">
        <div class="tutorial">
            <video src="{asset}{l["video"]}" poster="{asset}{l["poster"]}" controls playsinline preload="none"></video>
        </div>
    </div>
</section>

<section class="wrap">
    <article class="doc">
        <h2>{l["faq_title"]}</h2>
{faq_html}
        <p style="margin-top:26px;"><strong>{l["more"]}:</strong> <a href="{PAGES[other][lang]["slug"]}">{html.escape(PAGES[other][lang]["h1"])}</a></p>
    </article>
</section>

<section class="closing">
    <h2 class="section-title">{l["closing_title"]}</h2>
    <p class="section-sub">{l["closing_sub"]}</p>
    <div class="cta">
        {badge}
    </div>
    <p class="soon">{l["closing_soon"]}</p>
</section>

{sc_footer(lang)}
</body>
</html>
'''

written = []
for kind in PAGES:
    for lang in ("nl","en","fr","de","es"):
        p = PAGES[kind][lang]; path = os.path.join(ROOT, L[lang]["dir"], p["slug"])
        open(path, "w").write(render(kind, lang)); written.append(url(lang, p["slug"]))
# sitemap + robots
existing = [f"{SITE}/", f"{SITE}/support.html", f"{SITE}/privacy.html"] + [f"{SITE}/{d}/" for d in ("en","fr","de","es")] + [f"{SITE}/{d}/{f}" for d in ("en","fr","de","es") for f in ("support.html","privacy.html") if os.path.exists(os.path.join(ROOT,d,f))]
urls = existing + written
open(os.path.join(ROOT,"sitemap.xml"),"w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(f"  <url><loc>{u}</loc></url>" for u in urls) + "\n</urlset>\n")
open(os.path.join(ROOT,"robots.txt"),"w").write(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
print("\n".join(written)); print("sitemap:", len(urls), "urls")
