"""Homepage van rightsetfret.studioplanb.be in 5 talen (spec 2026-09-23, stijl B).
   python3 gen_site.py  →  index.html, en/index.html, fr/…, de/…, es/…"""
import json, os
from site_common import LANGS, ORDER, CHROME, APP_ID, esc, store_link, asset, head, nav, footer, badge, phone, qr_svg

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
  alts=dict(recept="Receptfiche met ingrediënten en stappen in RightSetFret", deelmenu="Het iOS-deelmenu met RightSetFret uitgelicht", import_="Sheet ‘Recept importeren’ met de invoerbronnen", kookmodus="Kookmodus met een stap en timer", collectie="Collectie met recepten en tags", frigo="Scherm ‘Wat kan ik koken?’ met ingrediënten uit de frigo", planning="Weekplanner met dieetkeuze", lijstje="Boodschappenlijst gesorteerd per winkelgang"),
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
  alts=dict(recept="Recipe card with ingredients and steps in RightSetFret", deelmenu="The iOS share sheet with RightSetFret highlighted", import_="‘Import recipe’ sheet with the input sources", kookmodus="Cooking mode with a step and timer", collectie="Collection with recipes and tags", frigo="‘What can I cook?’ screen with fridge ingredients", planning="Weekly planner with diet options", lijstje="Shopping list sorted by aisle"),
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
  alts=dict(recept="Fiche recette avec ingrédients et étapes dans RightSetFret", deelmenu="Le menu de partage iOS avec RightSetFret en évidence", import_="Feuille « Importer une recette » avec les sources", kookmodus="Mode cuisine avec une étape et un minuteur", collectie="Collection avec recettes et tags", frigo="Écran « Qu’est-ce que je peux cuisiner ? »", planning="Planificateur de la semaine avec choix du régime", lijstje="Liste de courses triée par rayon"),
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
  alts=dict(recept="Rezeptkarte mit Zutaten und Schritten in RightSetFret", deelmenu="Das iOS-Teilen-Menü mit RightSetFret hervorgehoben", import_="Blatt „Rezept importieren“ mit den Quellen", kookmodus="Kochmodus mit einem Schritt und Timer", collectie="Sammlung mit Rezepten und Tags", frigo="Bildschirm „Was kann ich kochen?“", planning="Wochenplaner mit Ernährungsauswahl", lijstje="Einkaufsliste nach Gang sortiert"),
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
  alts=dict(recept="Ficha de receta con ingredientes y pasos en RightSetFret", deelmenu="El menú de compartir de iOS con RightSetFret destacado", import_="Hoja «Importar receta» con las fuentes", kookmodus="Modo cocina con un paso y temporizador", collectie="Colección con recetas y etiquetas", frigo="Pantalla «¿Qué puedo cocinar?»", planning="Planificador semanal con opciones de dieta", lijstje="Lista de la compra ordenada por pasillo"),
 ),
}

SOURCE_ICONS = ["instagram", "tiktok", "youtube", "pinterest", "facebook", "web", "screenshot", "photo"]
FLOAT_ICONS = ["instagram", "tiktok", "youtube", "web", "photo"]
FEATURE_IMGS = ["collectie", "frigo", "planning", "lijstje"]
STAR = ' class="star"'

def render(lang):
    t = TEXT[lang]
    a = lambda p: asset(lang, p)
    alt = {l: f"{LANGS[l]['dir']}index.html" for l in ORDER}
    ct = f"web_home_{lang}"
    faq_ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": ans}} for q, ans in t["faq"]]}, ensure_ascii=False)
    app_ld = json.dumps({"@context": "https://schema.org", "@type": "SoftwareApplication", "name": "RightSetFret", "operatingSystem": "iOS", "applicationCategory": "LifestyleApplication",
                         "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"}, "aggregateRating": {"@type": "AggregateRating", "ratingValue": "5.0", "ratingCount": "1"},
                         "url": f"https://apps.apple.com/app/rightsetfret/id{APP_ID}"}, ensure_ascii=False)
    # Gedeelde recept-/lijst-links (rightsetfret://…) openen de app; zonder app blijft
    # deze pagina als nette terugval staan. Stond op de oude homepage; hier bewaard.
    deeplink = """<script>
(function(){
  var p = new URLSearchParams(location.search);
  var t = p.get('type'), scheme = null;
  if (t === 'recept' && p.get('id')) scheme = 'rightsetfret://recept?id=' + encodeURIComponent(p.get('id'));
  else if (t === 'lijst' && p.get('code')) scheme = 'rightsetfret://lijst?code=' + encodeURIComponent(p.get('code'));
  if (scheme) { setTimeout(function(){ window.location.href = scheme; }, 300); }
})();
</script>"""
    extra = deeplink + f'\n<script type="application/ld+json">{faq_ld}</script>\n<script type="application/ld+json">{app_ld}</script>'
    chips = "\n".join(f'            <li{STAR if ch.startswith("★") else ""}>{esc(ch)}</li>' for ch in t["chips"])
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
        save_html = f'<span class="save">{esc(save)}</span>' if save else ""
        plans += f'''        <div class="plan{" featured" if i == 1 else ""} reveal">
          {save_html}
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
