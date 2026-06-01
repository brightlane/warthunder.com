#!/usr/bin/env python3
"""
build.py — War Thunder Affiliate Site  v5.0
Site   : https://brightlane.github.io/warthunder/
Aff    : https://convert.ctypy.com/aff_c?offer_id=29176&aff_id=21885
Markets: AU, CA, FR, DE, KR, NZ, UK, US + ES, PT, IT, NL
Langs  : EN, FR, DE, KO, ES, PT, IT, NL
v5 upgrades vs v4:
  • 8 languages (was 4)
  • 300 keyword slugs (was 131)
  • 20 blog posts (was 12) with tables & richer content
  • Unique per-slug body copy variants (not just per-category)
  • Dark mode via CSS prefers-color-scheme
  • Mobile sticky CTA bar + hamburger nav
  • JS accordion FAQ (no layout shift)
  • Parallel page writes (ThreadPoolExecutor, 8 workers)
  • Split sitemap index → 4 sub-sitemaps
  • Nation vehicle tier tables (USA, Germany, Russia, Britain)
  • Geo pages with country-specific server / currency / store info
  • Skip-to-content + ARIA labels (accessibility)
  • SiteNavigationElement JSON-LD on every page
  • robots.txt explicitly allows GPTBot, ClaudeBot, anthropic-ai
  • --check flag verifies all sitemap URLs exist on disk
  • --lang XX to build a single language only
"""

import json, shutil, datetime, sys, os
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

# ── CONFIG ────────────────────────────────────────────────────────────────────
SITE_URL  = "https://brightlane.github.io/warthunder"
AFF_URL   = "https://convert.ctypy.com/aff_c?offer_id=29176&amp;aff_id=21885"
SITE_NAME = "WarThunder Guide"
TODAY     = datetime.date.today().isoformat()
YEAR      = str(datetime.date.today().year)
OUT       = Path("dist")
WORKERS   = 8

# ── CLI FLAGS ─────────────────────────────────────────────────────────────────
ONLY_LANG = None
DO_CHECK  = False
for arg in sys.argv[1:]:
    if arg.startswith("--lang="):
        ONLY_LANG = arg.split("=")[1]
    elif arg == "--check":
        DO_CHECK = True

# ── LANGUAGES ─────────────────────────────────────────────────────────────────
LANGUAGES = {
    "en": {
        "name":"English","dir":"ltr","locale":"en_US",
        "cta":"Play Free Now","dl":"Download Free",
        "see_all":"See All Guides",
        "nav_home":"Home","nav_review":"Review","nav_compare":"Compare","nav_blog":"Blog",
        "hero1":f"#1 FREE MILITARY GAME {YEAR}","hero2":"FLY. DRIVE. DOMINATE.",
        "hero_sub":f"The most realistic free military game of {YEAR}. Jets, tanks, warships — 100% free on PC, PS4/5 & Xbox.",
        "feat_title":"Why War Thunder?",
        "why":["100% Free|Download and play forever. No subscription, no hidden fees ever.",
               "2,000+ Vehicles|Planes, tanks, helicopters, warships — the largest free vehicle roster.",
               "Realistic Combat|Authentic physics & ballistics. Every vehicle built from real blueprints.",
               "Cross-Platform|PC (Steam & Gaijin), PS4/5, Xbox — cross-play across all platforms.",
               "Constant Updates|Multiple major updates per year with new maps, vehicles, events.",
               "100M+ Players|Massive active community. Find a match in seconds, 24/7."],
        "disc":"Affiliate disclosure: We earn a commission at no extra cost to you if you sign up via our links. War Thunder® is a trademark of Gaijin Entertainment.",
        "meta_home":f"Play War Thunder free in {YEAR}. Best free military game — 2,000+ aircraft, tanks & warships. PC, PS4/5, Xbox. No cost.",
        "faq_qs":[
            ("Is War Thunder really free?","Yes — 100% free to download and play on PC, PS4, PS5, and Xbox. Optional cosmetics exist but are never required to progress."),
            ("Is War Thunder pay-to-win?",f"No. Premium vehicles and time can speed progression, but skill is the primary factor. Top players compete in free vehicles in {YEAR}."),
            ("How many vehicles are in War Thunder?","Over 2,000 historically accurate aircraft, tanks, helicopters, and naval vessels spanning multiple nations and eras."),
            ("What platforms is War Thunder on?","PC (Steam & Gaijin.net), PlayStation 4, PlayStation 5, Xbox One, and Xbox Series X|S. Cross-play is supported."),
            ("How big is the War Thunder download?","Around 40–60 GB depending on platform and selected content packs."),
            ("Can I play War Thunder solo?","Yes — PvE (co-op) and solo missions are available alongside the main PvP modes."),
            ("What nations are in War Thunder?","USA, USSR, Germany, Great Britain, Japan, China, Italy, France, Sweden, Israel, and more — each with unique vehicle trees."),
            ("Is there a War Thunder mobile version?","War Thunder Mobile is a separate standalone game available on iOS and Android with its own vehicle roster."),
        ],
        "review_title":f"War Thunder Review {YEAR}: Is It Worth Playing?",
        "compare_title":f"War Thunder vs World of Tanks vs Crossout ({YEAR})",
        "blog_title":"War Thunder Guides & News",
        "privacy_title":"Privacy Policy",
        "terms_title":"Terms of Use",
        "related":"Related Guides",
        "skip":"Skip to content",
        "sticky_cta":f"War Thunder is 100% Free — Play Now",
    },
    "fr": {
        "name":"Français","dir":"ltr","locale":"fr_FR",
        "cta":"Jouer Gratuitement","dl":"Télécharger Gratuitement",
        "see_all":"Voir tous les guides",
        "nav_home":"Accueil","nav_review":"Avis","nav_compare":"Comparer","nav_blog":"Blog",
        "hero1":f"JEU MILITAIRE GRATUIT N°1 {YEAR}","hero2":"VOLEZ. CONDUISEZ. DOMINEZ.",
        "hero_sub":f"Le jeu militaire gratuit le plus réaliste de {YEAR}. Jets, chars, navires — 100% gratuit sur PC, PS4/5 et Xbox.",
        "feat_title":"Pourquoi War Thunder?",
        "why":["100% Gratuit|Téléchargez et jouez gratuitement pour toujours. Aucun abonnement ni frais cachés.",
               "2 000+ Véhicules|Avions, chars, hélicoptères, navires — le plus grand roster gratuit.",
               "Combat Réaliste|Physique et balistique authentiques. Chaque véhicule basé sur de vrais plans.",
               "Multi-Plateforme|PC, PS4/5, Xbox — jeu croisé activé.",
               "Mises à Jour Constantes|Plusieurs grandes mises à jour par an.",
               "100M+ Joueurs|Communauté massive. Trouvez un match en secondes."],
        "disc":"Divulgation d'affiliation: Nous gagnons une commission sans frais supplémentaires si vous vous inscrivez via nos liens. War Thunder® est une marque de Gaijin Entertainment.",
        "meta_home":f"Jouez à War Thunder gratuitement en {YEAR}. Meilleur jeu militaire gratuit — 2 000+ véhicules. PC, PS4/5, Xbox.",
        "faq_qs":[
            ("War Thunder est-il vraiment gratuit?","Oui — 100% gratuit sur PC, PS4, PS5 et Xbox. Des cosmétiques optionnels existent mais ne sont jamais nécessaires."),
            ("War Thunder est-il pay-to-win?","Non. Les véhicules premium peuvent accélérer la progression, mais le skill reste le facteur principal."),
            ("Combien de véhicules dans War Thunder?","Plus de 2 000 avions, chars, hélicoptères et navires historiquement précis."),
            ("Sur quelles plateformes?","PC (Steam & Gaijin.net), PS4, PS5, Xbox One, Xbox Series X|S avec jeu croisé."),
        ],
        "review_title":f"Avis War Thunder {YEAR}: Vaut-il la peine?",
        "compare_title":f"War Thunder vs World of Tanks vs Crossout ({YEAR})",
        "blog_title":"Guides & Actualités War Thunder",
        "privacy_title":"Politique de Confidentialité",
        "terms_title":"Conditions d'Utilisation",
        "related":"Guides connexes",
        "skip":"Aller au contenu",
        "sticky_cta":"War Thunder est 100% gratuit — Jouer maintenant",
    },
    "de": {
        "name":"Deutsch","dir":"ltr","locale":"de_DE",
        "cta":"Kostenlos Spielen","dl":"Kostenlos Herunterladen",
        "see_all":"Alle Guides anzeigen",
        "nav_home":"Startseite","nav_review":"Test","nav_compare":"Vergleich","nav_blog":"Blog",
        "hero1":f"#1 KOSTENLOSES MILITÄRSPIEL {YEAR}","hero2":"FLIEGEN. FAHREN. DOMINIEREN.",
        "hero_sub":f"Das realistischste kostenlose Militärspiel {YEAR}. Jets, Panzer, Kriegsschiffe — 100% kostenlos auf PC, PS4/5 & Xbox.",
        "feat_title":"Warum War Thunder?",
        "why":["100% Kostenlos|Für immer kostenlos herunterladen und spielen. Kein Abo, keine versteckten Gebühren.",
               "2.000+ Fahrzeuge|Flugzeuge, Panzer, Helikopter, Kriegsschiffe — der größte kostenlose Fuhrpark.",
               "Realistischer Kampf|Authentische Physik & Ballistik basierend auf echten Blaupausen.",
               "Plattformübergreifend|PC, PS4/5, Xbox — Crossplay auf allen Plattformen.",
               "Ständige Updates|Mehrere große Updates pro Jahr mit neuen Karten und Fahrzeugen.",
               "100M+ Spieler|Riesige Community. Finde jederzeit ein Match."],
        "disc":"Affiliate-Offenlegung: Wir erhalten eine Provision ohne Mehrkosten, wenn du dich über unsere Links anmeldest. War Thunder® ist eine Marke von Gaijin Entertainment.",
        "meta_home":f"Spiele War Thunder kostenlos in {YEAR}. Bestes kostenloses Militärspiel — 2.000+ Fahrzeuge. PC, PS4/5, Xbox.",
        "faq_qs":[
            ("Ist War Thunder wirklich kostenlos?","Ja — 100% kostenlos auf PC, PS4, PS5 und Xbox. Optionale Kosmetik existiert, ist aber nie nötig."),
            ("Ist War Thunder Pay-to-Win?","Nein. Premium-Fahrzeuge können das Vorankommen beschleunigen, aber Können ist der Hauptfaktor."),
            ("Wie viele Fahrzeuge gibt es?","Über 2.000 historisch genaue Flugzeuge, Panzer, Helikopter und Kriegsschiffe."),
            ("Auf welchen Plattformen?","PC (Steam & Gaijin.net), PS4, PS5, Xbox One, Xbox Series X|S mit Crossplay."),
        ],
        "review_title":f"War Thunder Test {YEAR}: Lohnt es sich?",
        "compare_title":f"War Thunder vs World of Tanks vs Crossout ({YEAR})",
        "blog_title":"War Thunder Guides & News",
        "privacy_title":"Datenschutzerklärung",
        "terms_title":"Nutzungsbedingungen",
        "related":"Ähnliche Guides",
        "skip":"Zum Inhalt springen",
        "sticky_cta":"War Thunder ist 100% kostenlos — Jetzt spielen",
    },
    "ko": {
        "name":"한국어","dir":"ltr","locale":"ko_KR",
        "cta":"무료로 플레이","dl":"무료 다운로드",
        "see_all":"모든 가이드 보기",
        "nav_home":"홈","nav_review":"리뷰","nav_compare":"비교","nav_blog":"블로그",
        "hero1":f"{YEAR}년 최고의 무료 전쟁 게임","hero2":"날아라. 달려라. 지배하라.",
        "hero_sub":f"{YEAR}년 가장 현실적인 무료 군사 게임. 전투기, 탱크, 전함 — PC, PS4/5, Xbox에서 100% 무료.",
        "feat_title":"워 선더를 선택하는 이유",
        "why":["100% 무료|영원히 무료로 다운로드 및 플레이. 구독료나 숨겨진 비용 없음.",
               "2,000개 이상 차량|전투기, 탱크, 헬리콥터, 전함 — 가장 큰 무료 차량 목록.",
               "현실적인 전투|실제 설계도 기반의 정확한 물리 및 탄도학.",
               "크로스 플랫폼|PC, PS4/5, Xbox — 모든 플랫폼 크로스플레이 지원.",
               "지속적인 업데이트|연간 여러 차례 대규모 업데이트.",
               "1억+ 플레이어|거대한 커뮤니티. 언제든지 매치 가능."],
        "disc":"제휴 공시: 링크를 통해 가입하시면 추가 비용 없이 수수료를 받습니다. War Thunder®는 Gaijin Entertainment의 상표입니다.",
        "meta_home":f"{YEAR}년 워 선더 무료 플레이. 최고의 무료 군사 게임 — 2,000개 이상 차량. PC, PS4/5, Xbox.",
        "faq_qs":[
            ("워 선더는 정말 무료인가요?","네 — PC, PS4, PS5, Xbox에서 100% 무료. 선택적 코스메틱이 있지만 필수는 아닙니다."),
            ("워 선더는 pay-to-win인가요?","아닙니다. 프리미엄이 진행 속도를 높일 수 있지만 실력이 주요 요소입니다."),
            ("차량이 몇 개나 있나요?","역사적으로 정확한 항공기, 탱크, 헬리콥터, 전함 2,000개 이상."),
            ("어떤 플랫폼에서 플레이 가능?","PC (Steam & Gaijin.net), PS4, PS5, Xbox One, Xbox Series X|S. 크로스플레이 지원."),
        ],
        "review_title":f"워 선더 리뷰 {YEAR}: 플레이할 가치 있나요?",
        "compare_title":f"워 선더 vs 월드 오브 탱크 vs 크로스아웃 ({YEAR})",
        "blog_title":"워 선더 가이드 & 뉴스",
        "privacy_title":"개인정보 처리방침",
        "terms_title":"이용약관",
        "related":"관련 가이드",
        "skip":"본문으로 이동",
        "sticky_cta":"워 선더는 100% 무료 — 지금 플레이",
    },
    "es": {
        "name":"Español","dir":"ltr","locale":"es_ES",
        "cta":"Jugar Gratis Ahora","dl":"Descargar Gratis",
        "see_all":"Ver todas las guías",
        "nav_home":"Inicio","nav_review":"Reseña","nav_compare":"Comparar","nav_blog":"Blog",
        "hero1":f"EL JUEGO MILITAR GRATUITO N°1 DE {YEAR}","hero2":"VUELA. CONDUCE. DOMINA.",
        "hero_sub":f"El juego militar gratuito más realista de {YEAR}. Jets, tanques, buques de guerra — 100% gratis en PC, PS4/5 y Xbox.",
        "feat_title":"¿Por qué War Thunder?",
        "why":["100% Gratis|Descarga y juega para siempre. Sin suscripción, sin tarifas ocultas.",
               "2.000+ Vehículos|Aviones, tanques, helicópteros, buques — el mayor roster gratuito.",
               "Combate Realista|Física y balística auténticas. Cada vehículo basado en planos reales.",
               "Multiplataforma|PC, PS4/5, Xbox — juego cruzado en todas las plataformas.",
               "Actualizaciones Constantes|Múltiples actualizaciones importantes por año.",
               "100M+ Jugadores|Comunidad masiva. Encuentra partida en segundos."],
        "disc":"Divulgación de afiliados: Ganamos una comisión sin costo adicional si te registras a través de nuestros enlaces. War Thunder® es una marca de Gaijin Entertainment.",
        "meta_home":f"Juega War Thunder gratis en {YEAR}. Mejor juego militar gratuito — 2.000+ vehículos. PC, PS4/5, Xbox.",
        "faq_qs":[
            ("¿War Thunder es realmente gratuito?","Sí — 100% gratis en PC, PS4, PS5 y Xbox. Los cosméticos opcionales existen pero nunca son necesarios."),
            ("¿War Thunder es pay-to-win?","No. Los vehículos premium pueden acelerar el progreso, pero la habilidad es el factor principal."),
            ("¿Cuántos vehículos tiene War Thunder?","Más de 2.000 aviones, tanques, helicópteros y buques históricamente precisos."),
            ("¿En qué plataformas está disponible?","PC (Steam y Gaijin.net), PS4, PS5, Xbox One y Xbox Series X|S con juego cruzado."),
        ],
        "review_title":f"Reseña de War Thunder {YEAR}: ¿Vale la pena?",
        "compare_title":f"War Thunder vs World of Tanks vs Crossout ({YEAR})",
        "blog_title":"Guías y Noticias de War Thunder",
        "privacy_title":"Política de Privacidad",
        "terms_title":"Términos de Uso",
        "related":"Guías relacionadas",
        "skip":"Saltar al contenido",
        "sticky_cta":"War Thunder es 100% gratis — Jugar ahora",
    },
    "pt": {
        "name":"Português","dir":"ltr","locale":"pt_BR",
        "cta":"Jogar Grátis Agora","dl":"Baixar Grátis",
        "see_all":"Ver todos os guias",
        "nav_home":"Início","nav_review":"Review","nav_compare":"Comparar","nav_blog":"Blog",
        "hero1":f"O JOGO MILITAR GRATUITO Nº1 DE {YEAR}","hero2":"VOLE. DIRIJA. DOMINE.",
        "hero_sub":f"O jogo militar gratuito mais realista de {YEAR}. Jatos, tanques, navios — 100% grátis no PC, PS4/5 e Xbox.",
        "feat_title":"Por que War Thunder?",
        "why":["100% Grátis|Baixe e jogue para sempre. Sem assinatura, sem taxas ocultas.",
               "2.000+ Veículos|Aviões, tanques, helicópteros, navios — o maior roster gratuito.",
               "Combate Realista|Física e balística autênticas. Cada veículo baseado em plantas reais.",
               "Multiplataforma|PC, PS4/5, Xbox — cross-play em todas as plataformas.",
               "Atualizações Constantes|Várias atualizações importantes por ano.",
               "100M+ Jogadores|Comunidade massiva. Encontre uma partida em segundos."],
        "disc":"Divulgação de afiliados: Ganhamos uma comissão sem custo extra se você se inscrever pelos nossos links. War Thunder® é uma marca da Gaijin Entertainment.",
        "meta_home":f"Jogue War Thunder grátis em {YEAR}. Melhor jogo militar gratuito — 2.000+ veículos. PC, PS4/5, Xbox.",
        "faq_qs":[
            ("War Thunder é realmente gratuito?","Sim — 100% grátis no PC, PS4, PS5 e Xbox. Cosméticos opcionais existem mas nunca são necessários."),
            ("War Thunder é pay-to-win?","Não. Veículos premium podem acelerar o progresso, mas a habilidade é o fator principal."),
            ("Quantos veículos tem War Thunder?","Mais de 2.000 aviões, tanques, helicópteros e navios historicamente precisos."),
            ("Em quais plataformas está disponível?","PC (Steam e Gaijin.net), PS4, PS5, Xbox One e Xbox Series X|S com cross-play."),
        ],
        "review_title":f"Review de War Thunder {YEAR}: Vale a pena?",
        "compare_title":f"War Thunder vs World of Tanks vs Crossout ({YEAR})",
        "blog_title":"Guias e Notícias de War Thunder",
        "privacy_title":"Política de Privacidade",
        "terms_title":"Termos de Uso",
        "related":"Guias relacionados",
        "skip":"Ir para o conteúdo",
        "sticky_cta":"War Thunder é 100% grátis — Jogar agora",
    },
    "it": {
        "name":"Italiano","dir":"ltr","locale":"it_IT",
        "cta":"Gioca Gratis Ora","dl":"Scarica Gratis",
        "see_all":"Vedi tutte le guide",
        "nav_home":"Home","nav_review":"Recensione","nav_compare":"Confronto","nav_blog":"Blog",
        "hero1":f"IL GIOCO MILITARE GRATUITO N°1 DEL {YEAR}","hero2":"VOLA. GUIDA. DOMINA.",
        "hero_sub":f"Il gioco militare gratuito più realistico del {YEAR}. Jet, carri armati, navi — 100% gratis su PC, PS4/5 e Xbox.",
        "feat_title":"Perché War Thunder?",
        "why":["100% Gratuito|Scarica e gioca per sempre. Nessun abbonamento, nessuna tariffa nascosta.",
               "2.000+ Veicoli|Aerei, carri armati, elicotteri, navi — il più grande roster gratuito.",
               "Combattimento Realistico|Fisica e balistica autentiche. Ogni veicolo basato su schemi reali.",
               "Multipiattaforma|PC, PS4/5, Xbox — cross-play su tutte le piattaforme.",
               "Aggiornamenti Costanti|Numerosi aggiornamenti importanti ogni anno.",
               "100M+ Giocatori|Enorme comunità. Trova una partita in secondi."],
        "disc":"Divulgazione affiliati: Guadagniamo una commissione senza costi aggiuntivi se ti iscrivi tramite i nostri link. War Thunder® è un marchio di Gaijin Entertainment.",
        "meta_home":f"Gioca a War Thunder gratis nel {YEAR}. Miglior gioco militare gratuito — 2.000+ veicoli. PC, PS4/5, Xbox.",
        "faq_qs":[
            ("War Thunder è davvero gratuito?","Sì — 100% gratis su PC, PS4, PS5 e Xbox. Cosmetici opzionali esistono ma non sono mai necessari."),
            ("War Thunder è pay-to-win?","No. I veicoli premium possono accelerare i progressi, ma l'abilità è il fattore principale."),
            ("Quanti veicoli ha War Thunder?","Oltre 2.000 aerei, carri armati, elicotteri e navi storicamente accurati."),
            ("Su quali piattaforme è disponibile?","PC (Steam e Gaijin.net), PS4, PS5, Xbox One e Xbox Series X|S con cross-play."),
        ],
        "review_title":f"Recensione War Thunder {YEAR}: Vale la pena?",
        "compare_title":f"War Thunder vs World of Tanks vs Crossout ({YEAR})",
        "blog_title":"Guide e Notizie su War Thunder",
        "privacy_title":"Informativa sulla Privacy",
        "terms_title":"Termini di Utilizzo",
        "related":"Guide correlate",
        "skip":"Vai al contenuto",
        "sticky_cta":"War Thunder è 100% gratuito — Gioca ora",
    },
    "nl": {
        "name":"Nederlands","dir":"ltr","locale":"nl_NL",
        "cta":"Speel Gratis Nu","dl":"Gratis Downloaden",
        "see_all":"Alle gidsen bekijken",
        "nav_home":"Home","nav_review":"Review","nav_compare":"Vergelijk","nav_blog":"Blog",
        "hero1":f"HET #1 GRATIS MILITAIRE SPEL VAN {YEAR}","hero2":"VLIEG. RIJD. DOMINEER.",
        "hero_sub":f"Het meest realistische gratis militaire spel van {YEAR}. Jets, tanks, oorlogsschepen — 100% gratis op PC, PS4/5 en Xbox.",
        "feat_title":"Waarom War Thunder?",
        "why":["100% Gratis|Download en speel voor altijd. Geen abonnement, geen verborgen kosten.",
               "2.000+ Voertuigen|Vliegtuigen, tanks, helikopters, schepen — de grootste gratis vloot.",
               "Realistisch Gevecht|Authentieke fysica en ballistiek. Elk voertuig op basis van echte blauwdrukken.",
               "Cross-Platform|PC, PS4/5, Xbox — cross-play op alle platforms.",
               "Constante Updates|Meerdere grote updates per jaar.",
               "100M+ Spelers|Enorme actieve community. Vind binnen seconden een match."],
        "disc":"Affiliate-openbaarmaking: We verdienen een commissie zonder extra kosten als je je aanmeldt via onze links. War Thunder® is een handelsmerk van Gaijin Entertainment.",
        "meta_home":f"Speel War Thunder gratis in {YEAR}. Beste gratis militaire spel — 2.000+ voertuigen. PC, PS4/5, Xbox.",
        "faq_qs":[
            ("Is War Thunder echt gratis?","Ja — 100% gratis op PC, PS4, PS5 en Xbox. Optionele cosmetica bestaan maar zijn nooit vereist."),
            ("Is War Thunder pay-to-win?","Nee. Premium voertuigen kunnen de voortgang versnellen, maar vaardigheid is de belangrijkste factor."),
            ("Hoeveel voertuigen heeft War Thunder?","Meer dan 2.000 historisch nauwkeurige vliegtuigen, tanks, helikopters en schepen."),
            ("Op welke platforms is het beschikbaar?","PC (Steam en Gaijin.net), PS4, PS5, Xbox One en Xbox Series X|S met cross-play."),
        ],
        "review_title":f"War Thunder Review {YEAR}: Is het de moeite waard?",
        "compare_title":f"War Thunder vs World of Tanks vs Crossout ({YEAR})",
        "blog_title":"War Thunder Gidsen & Nieuws",
        "privacy_title":"Privacybeleid",
        "terms_title":"Gebruiksvoorwaarden",
        "related":"Gerelateerde gidsen",
        "skip":"Ga naar inhoud",
        "sticky_cta":"War Thunder is 100% gratis — Speel nu",
    },
}

# ── GEO DETAILS (country-specific server / currency / store info) ─────────────
GEO_DETAILS = {
    "war-thunder-australia": {
        "country":"Australia","currency":"AUD","cluster":"Asia-Pacific (Sydney)",
        "ping":"15–40 ms typical","stores":["Steam","PlayStation Store AU","Microsoft Store AU"],
        "extra":"No geo-restrictions. GST included in store prices. PlayStation Network AU account required for PS store.",
    },
    "war-thunder-canada": {
        "country":"Canada","currency":"CAD","cluster":"North America (US East/West)",
        "ping":"20–60 ms typical","stores":["Steam","PlayStation Store CA","Microsoft Store CA"],
        "extra":"No geo-restrictions. Quebec French UI available. Canadian PSN account required for PS store.",
    },
    "war-thunder-uk": {
        "country":"United Kingdom","currency":"GBP","cluster":"Europe (Frankfurt/Amsterdam)",
        "ping":"10–35 ms typical","stores":["Steam","PlayStation Store UK","Microsoft Store UK"],
        "extra":"No geo-restrictions. VAT included in prices. UK PSN account required for PS store.",
    },
    "war-thunder-new-zealand": {
        "country":"New Zealand","currency":"NZD","cluster":"Asia-Pacific (Sydney)",
        "ping":"20–50 ms typical","stores":["Steam","PlayStation Store NZ","Microsoft Store NZ"],
        "extra":"No geo-restrictions. NZ PSN account required for PS store. Shares AU/NZ PlayStation region.",
    },
    "war-thunder-south-korea": {
        "country":"South Korea","currency":"KRW","cluster":"Asia-Pacific (Seoul/Tokyo)",
        "ping":"10–30 ms typical","stores":["Steam","PlayStation Store KR","Microsoft Store KR"],
        "extra":"No geo-restrictions. Korean UI fully supported. Korean PSN account required for PS store.",
    },
    "war-thunder-germany": {
        "country":"Germany","currency":"EUR","cluster":"Europe (Frankfurt)",
        "ping":"5–25 ms typical","stores":["Steam","PlayStation Store DE","Microsoft Store DE"],
        "extra":"No geo-restrictions. German localisation available. German USK rating: 12+.",
    },
    "war-thunder-france": {
        "country":"France","currency":"EUR","cluster":"Europe (Paris/Frankfurt)",
        "ping":"5–20 ms typical","stores":["Steam","PlayStation Store FR","Microsoft Store FR"],
        "extra":"No geo-restrictions. Full French localisation. French PSN account required for PS store.",
    },
    "war-thunder-usa": {
        "country":"United States","currency":"USD","cluster":"North America (US East/West/Central)",
        "ping":"10–50 ms typical","stores":["Steam","PlayStation Store US","Microsoft Store US","Gaijin.net"],
        "extra":"No geo-restrictions. Best server coverage in the game. All payment methods accepted.",
    },
    "war-thunder-spain": {
        "country":"Spain","currency":"EUR","cluster":"Europe (Madrid/Frankfurt)",
        "ping":"10–30 ms typical","stores":["Steam","PlayStation Store ES","Microsoft Store ES"],
        "extra":"No geo-restrictions. Spanish localisation available.",
    },
    "war-thunder-brazil": {
        "country":"Brazil","currency":"BRL","cluster":"South America (São Paulo)",
        "ping":"20–60 ms typical","stores":["Steam","PlayStation Store BR","Microsoft Store BR"],
        "extra":"No geo-restrictions. Steam has BRL pricing. Brazilian PSN region required for PS store.",
    },
    "war-thunder-italy": {
        "country":"Italy","currency":"EUR","cluster":"Europe (Milan/Frankfurt)",
        "ping":"8–25 ms typical","stores":["Steam","PlayStation Store IT","Microsoft Store IT"],
        "extra":"No geo-restrictions. Italian localisation available.",
    },
    "war-thunder-netherlands": {
        "country":"Netherlands","currency":"EUR","cluster":"Europe (Amsterdam)",
        "ping":"5–15 ms typical","stores":["Steam","PlayStation Store NL","Microsoft Store NL"],
        "extra":"No geo-restrictions. Dutch PSN account required for PS store. Excellent server proximity.",
    },
}

# ── NATION VEHICLE TABLES ─────────────────────────────────────────────────────
NATION_TABLES = {
    "war-thunder-usa-tanks": {
        "intro": f"The American ground forces tree in War Thunder {YEAR} is one of the most beginner-friendly. Excellent armour angles, reliable guns, and strong air support options.",
        "rows": [
            ("M2A4","1.0","Light Tank","Fast scout, learn the basics"),
            ("M4A1 Sherman","3.7","Medium Tank","Reliable all-rounder, solid first main tank"),
            ("M4A3E2 Jumbo","5.5","Heavy Tank","Extremely thick frontal armour"),
            ("M26 Pershing","6.3","Medium Tank","Post-WW2 transition vehicle, great gun"),
            ("M60","7.7","MBT","Cold War heavyweight, tough armour"),
            ("M1 Abrams","10.0","MBT","Top-tier powerhouse, excellent gun depression"),
            ("M1A2 SEP v2","11.3","MBT","Current US top tier, exceptional composite armour"),
        ],
    },
    "war-thunder-germany-tanks": {
        "intro": f"Germany's ground forces tree in War Thunder {YEAR} is famous for exceptional optics and high-penetration guns. Germany rewards patient, accurate players.",
        "rows": [
            ("Pz.II C","1.3","Light Tank","Fast early scout, learn spotting"),
            ("Pz.III J","3.7","Medium Tank","Balanced early-war medium"),
            ("Tiger I H","5.7","Heavy Tank","Iconic heavy — thick frontal armour"),
            ("Tiger II (H)","6.7","Heavy Tank","King Tiger — nearly impenetrable front"),
            ("Leopard 1","7.7","MBT","Mobility over armour, excellent gun"),
            ("Leopard 2A4","10.0","MBT","The benchmark German MBT"),
            ("Leopard 2A7V","11.7","MBT","Current German top tier, elite protection"),
        ],
    },
    "war-thunder-russia-tanks": {
        "intro": f"The Soviet/Russian ground forces tree in War Thunder {YEAR} features legendary sloped armour, autoloaders, and devastating firepower. Aggressive brawlers thrive here.",
        "rows": [
            ("BT-5","1.7","Light Tank","Extremely fast early scout"),
            ("T-34 (1940)","3.3","Medium Tank","The iconic WW2 medium — sloped armour"),
            ("KV-2","4.7","Heavy Tank","Derp cannon that can one-shot anything"),
            ("IS-2","6.3","Heavy Tank","152mm gun devastates anything it hits"),
            ("T-54 (1951)","7.7","MBT","Cold War powerhouse, great all-rounder"),
            ("T-72B3","10.0","MBT","Autoloader + reactive armour combination"),
            ("T-90M","11.3","MBT","Modern Russian top tier with Relikt ERA"),
        ],
    },
    "war-thunder-britain-tanks": {
        "intro": f"Britain's ground forces tree in War Thunder {YEAR} features unique two-plane stabilisers and excellent APDS rounds. Versatile at all tiers with strong historical vehicles.",
        "rows": [
            ("Crusader III","3.0","Cruiser Tank","Fast and maneuverable early vehicle"),
            ("Churchill III","4.7","Infantry Tank","Thick armour, slow but tough"),
            ("Comet I","5.3","Cruiser Tank","Excellent mobility + decent gun"),
            ("Centurion Mk.3","7.0","MBT","Two-plane stabiliser advantage"),
            ("Chieftain Mk.5","8.7","MBT","Strong frontal armour, great gun"),
            ("Challenger 2","10.3","MBT","Exceptional Chobham composite armour"),
            ("Challenger 2 TES","11.0","MBT","Urban kit with additional ERA protection"),
        ],
    },
}


# ── KEYWORDS (300 slugs) ──────────────────────────────────────────────────────
KEYWORDS = [
    # FREE WAR/MILITARY (30)
    ("free-war-games","Free War Games {y}","Best free war games {y} — play War Thunder free on PC, PS4/5, Xbox.","free"),
    ("free-war-games-pc","Free War Games PC {y}","Best free war games for PC in {y}. Download War Thunder free on Steam.","free"),
    ("free-war-games-ps4","Free War Games PS4 {y}","Best free war games for PS4 in {y}. War Thunder is 100% free on PS4.","free"),
    ("free-war-games-ps5","Free War Games PS5 {y}","Best free war games for PS5 in {y}. Download War Thunder free on PS5.","free"),
    ("free-war-games-xbox","Free War Games Xbox {y}","Best free war games for Xbox {y}. Play War Thunder free on Xbox.","free"),
    ("free-war-games-no-download","Free War Games No Download {y}","Play free war games online {y}. Comparison of browser vs download options.","free"),
    ("free-war-games-online","Free War Games Online {y}","Play free war games online {y}. Best browser and download options.","free"),
    ("free-war-games-steam","Free War Games Steam {y}","Best free war games on Steam {y}. War Thunder leads the list.","free"),
    ("free-military-games","Free Military Games {y}","Best free military games {y}. War Thunder tops the list on all platforms.","free"),
    ("free-military-games-pc","Free Military Games PC {y}","Top free military games for PC {y}. Download War Thunder on Steam.","free"),
    ("free-tank-games","Free Tank Games {y}","Best free tank games {y}. War Thunder offers the most realistic tank combat.","free"),
    ("free-tank-games-pc","Free Tank Games PC {y}","Top free tank games for PC {y}. Play War Thunder on Steam for free.","free"),
    ("free-tank-battle-games","Free Tank Battle Games {y}","Best free tank battle games {y}. War Thunder has 1,000+ historical tanks.","free"),
    ("free-ww2-games","Free WW2 Games {y}","Best free WW2 games {y}. War Thunder covers every major WW2 theater.","free"),
    ("free-ww2-games-pc","Free WW2 PC Games {y}","Top free WW2 games for PC {y}. Download War Thunder on Steam.","free"),
    ("free-ww2-tank-games","Free WW2 Tank Games {y}","Best free WW2 tank games {y}. War Thunder's ground forces go back to 1939.","free"),
    ("free-plane-games","Free Plane Games {y}","Best free plane games {y}. War Thunder offers 1,000+ historical aircraft.","free"),
    ("free-fighter-jet-games","Free Fighter Jet Games {y}","Best free fighter jet games {y}. War Thunder has jets from WW2 to modern era.","free"),
    ("free-dogfight-games","Free Dogfight Games {y}","Best free dogfight games {y}. War Thunder's air battles are the most realistic.","free"),
    ("free-ww2-plane-games","Free WW2 Plane Games {y}","Best free WW2 plane games {y}. Fly iconic WW2 aircraft in War Thunder.","free"),
    ("free-helicopter-games","Free Helicopter Games {y}","Best free helicopter games {y}. War Thunder has attack helicopters from all eras.","free"),
    ("free-warship-games","Free Warship Games {y}","Best free warship games {y}. War Thunder's naval forces span destroyers to battleships.","free"),
    ("free-naval-combat-games","Free Naval Combat Games {y}","Best free naval combat games {y}. War Thunder naval battles are uniquely realistic.","free"),
    ("free-battleship-games","Free Battleship Games {y}","Best free battleship games {y}. Command real WWII battleships in War Thunder.","free"),
    ("free-submarine-games","Free Submarine Games {y}","Best free submarine games {y}. Explore War Thunder's growing naval roster.","free"),
    ("free-pvp-war-games","Free PvP War Games {y}","Best free PvP war games {y}. War Thunder has millions of active PvP players.","free"),
    ("free-multiplayer-war-games","Free Multiplayer War Games {y}","Best free multiplayer war games {y}. War Thunder supports squads and clans.","free"),
    ("free-team-war-games","Free Team War Games {y}","Best free team war games {y}. Play War Thunder with friends in squad battles.","free"),
    ("free-co-op-war-games","Free Co-op War Games {y}","Best free co-op war games {y}. War Thunder's PvE mode is perfect for squads.","free"),
    ("free-open-world-war-games","Free Open World War Games {y}","Best free open-world military games {y}. War Thunder's maps span kilometres.","free"),
    # BEST INTENT (18)
    ("best-free-war-game","Best Free War Game {y}","What is the best free war game in {y}? War Thunder wins on vehicles, realism and content.","best"),
    ("best-free-war-games","Best Free War Games {y}","Ranking the best free war games {y}. War Thunder, Crossout, WoT compared.","best"),
    ("best-free-tank-game","Best Free Tank Game {y}","Best free tank game {y}: War Thunder vs World of Tanks full comparison.","best"),
    ("best-free-military-game","Best Free Military Game {y}","Best free military game {y}. War Thunder is #1 for realism and content.","best"),
    ("best-free-ww2-game","Best Free WW2 Game {y}","Best free WW2 game {y}. War Thunder covers air, land, and sea from 1939–1945.","best"),
    ("best-free-plane-game","Best Free Plane Game {y}","Best free plane game {y}: War Thunder leads with 1,000+ aircraft.","best"),
    ("best-free-games-steam","Best Free Games Steam {y}","Best free games on Steam {y}. War Thunder is a top-rated free-to-play title.","best"),
    ("best-free-ps5-games","Best Free PS5 Games {y}","Best free PS5 games {y}. War Thunder is one of the highest-rated free PS5 titles.","best"),
    ("best-free-ps4-games","Best Free PS4 Games {y}","Best free PS4 games {y}. War Thunder is 100% free with no PS Plus required.","best"),
    ("best-free-xbox-games","Best Free Xbox Games {y}","Best free Xbox games {y}. War Thunder needs no Xbox Game Pass subscription.","best"),
    ("best-free-games-no-ps-plus","Best Free PS5 Games No PS Plus {y}","Best free PS5 games without PS Plus {y}. War Thunder requires no subscription.","best"),
    ("best-free-games-no-xbox-live","Best Free Xbox Games No Gold {y}","Best free Xbox games without Xbox Live Gold {y}. War Thunder is fully free.","best"),
    ("best-free-flight-simulator","Best Free Flight Simulator {y}","Best free flight simulator {y}. War Thunder's air modes are the most accessible.","best"),
    ("best-free-naval-game","Best Free Naval Game {y}","Best free naval combat game {y}. War Thunder's naval branch is unmatched at no cost.","best"),
    ("best-war-games-2025","Best War Games 2025","Best war games to play in 2025 — free and paid options compared.","best"),
    ("best-war-games-2026","Best War Games 2026","Best war games to play in 2026 — top picks across all platforms.","best"),
    ("best-free-action-games","Best Free Action Games {y}","Best free action games {y}. War Thunder's fast-paced modes qualify as top action titles.","best"),
    ("best-free-strategy-games-military","Best Free Military Strategy Games {y}","Best free military strategy games {y}. War Thunder blends action and strategy.","best"),
    # SIMILAR / ALTERNATIVES (10)
    ("games-like-war-thunder","Games Like War Thunder {y}","Looking for games like War Thunder? Compare alternatives and find out why WT is still #1.","similar"),
    ("games-like-war-thunder-free","Free Games Like War Thunder {y}","Best free games like War Thunder {y}. Alternatives reviewed and compared.","similar"),
    ("games-like-world-of-tanks","Games Like World of Tanks {y}","Games like World of Tanks {y}. War Thunder is the top free alternative.","similar"),
    ("games-like-world-of-tanks-free","Free Games Like World of Tanks {y}","Free alternatives to World of Tanks {y}. War Thunder wins on realism.","similar"),
    ("games-like-battlefield-free","Free Games Like Battlefield {y}","Free games like Battlefield {y}. War Thunder offers similar large-scale battles.","similar"),
    ("games-like-call-of-duty-free","Free Games Like Call of Duty {y}","Free alternatives to CoD {y}. War Thunder is free on all the same platforms.","similar"),
    ("war-thunder-alternative","War Thunder Alternative {y}","Looking for a War Thunder alternative? See how it compares to WoT and Crossout.","similar"),
    ("war-thunder-alternatives-2025","War Thunder Alternatives 2025","Best War Thunder alternatives in 2025: free and paid options compared.","similar"),
    ("war-thunder-alternatives-2026","War Thunder Alternatives 2026","Best War Thunder alternatives in 2026: updated comparison guide.","similar"),
    ("world-of-warships-alternative","World of Warships Alternative {y}","Free World of Warships alternatives {y}. War Thunder naval is a top pick.","similar"),
    # WAR THUNDER SPECIFIC (45)
    ("is-war-thunder-free","Is War Thunder Free?","Yes — War Thunder is 100% free to download and play. Full details here.","wt"),
    ("is-war-thunder-pay-to-win","Is War Thunder Pay to Win?","Honest answer: is War Thunder pay-to-win in {y}? We break down the economy.","wt"),
    ("is-war-thunder-good","Is War Thunder Good {y}?","Is War Thunder worth playing in {y}? Full honest review.","wt"),
    ("is-war-thunder-dead","Is War Thunder Dead {y}?","Is War Thunder still active in {y}? Player count and server status.","wt"),
    ("war-thunder-download","War Thunder Download","How to download War Thunder free on PC, PS4/5 and Xbox. Step-by-step guide.","wt"),
    ("war-thunder-download-pc","War Thunder PC Download","Download War Thunder free on PC via Steam or Gaijin.net. Guide and tips.","wt"),
    ("war-thunder-download-ps4","War Thunder PS4 Download","Download War Thunder free on PS4. Step-by-step from the PlayStation Store.","wt"),
    ("war-thunder-download-ps5","War Thunder PS5 Download","Download War Thunder free on PS5. Guide and performance details.","wt"),
    ("war-thunder-download-xbox","War Thunder Xbox Download","Download War Thunder free on Xbox. Guide from the Microsoft Store.","wt"),
    ("war-thunder-review","War Thunder Review {y}","Full War Thunder review {y}. Gameplay, graphics, economy, verdict.","wt"),
    ("war-thunder-beginner-guide","War Thunder Beginner Guide {y}","New to War Thunder? Complete beginner guide for {y} — nations, modes, tips.","wt"),
    ("war-thunder-tips","War Thunder Tips {y}","Top War Thunder tips and tricks {y} to rank up faster.","wt"),
    ("war-thunder-best-nation","Best Nation War Thunder {y}","What is the best nation to start in War Thunder {y}? Full breakdown.","wt"),
    ("war-thunder-usa-tanks","War Thunder USA Tanks {y}","Best US tanks in War Thunder {y}. Full American ground forces guide.","nation"),
    ("war-thunder-germany-tanks","War Thunder Germany Tanks {y}","Best German tanks in War Thunder {y}. Germany ground forces guide.","nation"),
    ("war-thunder-russia-tanks","War Thunder Russia Tanks {y}","Best Soviet/Russian tanks in War Thunder {y}. USSR ground forces guide.","wt"),
    ("war-thunder-britain-tanks","War Thunder Britain Tanks {y}","Best British tanks in War Thunder {y}. UK ground forces guide.","nation"),
    ("war-thunder-japan-tanks","War Thunder Japan Tanks {y}","Best Japanese tanks in War Thunder {y}. Japan ground forces guide.","wt"),
    ("war-thunder-china-tanks","War Thunder China Tanks {y}","Best Chinese tanks in War Thunder {y}. China ground forces guide.","wt"),
    ("war-thunder-italy-tanks","War Thunder Italy Tanks {y}","Best Italian tanks in War Thunder {y}. Italy ground forces guide.","wt"),
    ("war-thunder-france-tree","War Thunder France Tech Tree {y}","Complete France tech tree guide {y}. Best French vehicles and tips.","wt"),
    ("war-thunder-sweden-tanks","War Thunder Sweden Tanks {y}","Best Swedish tanks in War Thunder {y}. Sweden ground forces guide.","wt"),
    ("war-thunder-silver-lions-farm","War Thunder Silver Lions Farm {y}","Best ways to farm Silver Lions in War Thunder {y}. Top economy tips.","wt"),
    ("war-thunder-golden-eagles-free","War Thunder Free Golden Eagles {y}","How to get free Golden Eagles in War Thunder {y}. Legit methods only.","wt"),
    ("war-thunder-rank-up-fast","Rank Up Fast War Thunder {y}","How to rank up fast in War Thunder {y}. RP farming and crew XP tips.","wt"),
    ("war-thunder-realistic-battles","War Thunder Realistic Battles Guide","War Thunder Realistic Battles guide: tips to dominate in RB mode.","wt"),
    ("war-thunder-simulator-battles","War Thunder Simulator Battles Guide","War Thunder Simulator Battles guide for beginners.","wt"),
    ("war-thunder-ground-forces","War Thunder Ground Forces Guide {y}","Complete War Thunder ground forces (tanks) guide for {y}.","wt"),
    ("war-thunder-air-forces","War Thunder Air Forces Guide {y}","Complete War Thunder aviation guide — aircraft and combat tips for {y}.","wt"),
    ("war-thunder-naval-forces","War Thunder Naval Forces Guide {y}","Complete War Thunder naval guide — ships, destroyers, battleships.","wt"),
    ("war-thunder-helicopters","War Thunder Helicopter Guide {y}","War Thunder helicopter guide {y}. Best helicopters and combat tactics.","wt"),
    ("war-thunder-best-plane","Best Plane War Thunder {y}","Best aircraft in War Thunder {y} at every Battle Rating.","wt"),
    ("war-thunder-best-tank","Best Tank War Thunder {y}","Best tanks in War Thunder {y} at every Battle Rating.","wt"),
    ("war-thunder-premium","War Thunder Premium {y}","Is War Thunder Premium worth it in {y}? What you get and whether to buy.","wt"),
    ("war-thunder-battle-pass","War Thunder Battle Pass {y}","War Thunder Battle Pass {y}: what's included, cost, and is it worth it?","wt"),
    ("war-thunder-crew-skills","War Thunder Crew Skills Guide {y}","Best crew skills to unlock first in War Thunder {y}. Full priority guide.","wt"),
    ("war-thunder-top-tier","War Thunder Top Tier Guide {y}","Guide to top-tier War Thunder in {y}. Nations, vehicles, and meta explained.","wt"),
    ("war-thunder-economy","War Thunder Economy Guide {y}","How War Thunder's economy works in {y}. SL, RP, GE explained.","wt"),
    ("war-thunder-squad","War Thunder Squadron Guide {y}","How to join and create squadrons in War Thunder {y}. Squad battles explained.","wt"),
    ("war-thunder-sound-mods","War Thunder Sound Mods {y}","Best War Thunder sound mods {y}. How to install and which to choose.","wt"),
    ("war-thunder-graphic-mods","War Thunder Graphic Mods {y}","Best War Thunder graphic mods {y}. Reshade, skins, and visual improvements.","wt"),
    ("war-thunder-air-rb","War Thunder Air RB Guide {y}","War Thunder Air Realistic Battles guide {y}. Tactics, energy fighting, tips.","wt"),
    ("war-thunder-ground-rb","War Thunder Ground RB Guide {y}","War Thunder Ground Realistic Battles guide {y}. Flanking, spotting, positioning.","wt"),
    ("war-thunder-events","War Thunder Events {y}","War Thunder major events {y}. How to earn free premium vehicles from events.","wt"),
    ("war-thunder-update-2026","War Thunder Updates {y}","What's new in War Thunder {y}? Latest patches, vehicles, and balance changes.","wt"),
    # VERSUS / COMPARISON (10)
    ("war-thunder-vs-world-of-tanks","War Thunder vs World of Tanks {y}","War Thunder vs World of Tanks {y}: which free tank game wins?","vs"),
    ("war-thunder-vs-crossout","War Thunder vs Crossout {y}","War Thunder vs Crossout {y}: which free vehicle combat game is better?","vs"),
    ("war-thunder-vs-battlefield","War Thunder vs Battlefield {y}","War Thunder vs Battlefield {y}: free vs paid military game comparison.","vs"),
    ("war-thunder-vs-call-of-duty","War Thunder vs Call of Duty {y}","War Thunder vs Call of Duty {y}: which military game should you play?","vs"),
    ("war-thunder-vs-enlisted","War Thunder vs Enlisted {y}","War Thunder vs Enlisted {y}: both free Gaijin games compared.","vs"),
    ("world-of-tanks-vs-war-thunder","World of Tanks vs War Thunder {y}","WoT vs War Thunder {y}: full comparison. Which is better for you?","vs"),
    ("war-thunder-vs-hell-let-loose","War Thunder vs Hell Let Loose {y}","War Thunder vs Hell Let Loose {y}: free vs paid WW2 game comparison.","vs"),
    ("war-thunder-vs-squad","War Thunder vs Squad {y}","War Thunder vs Squad {y}: which military game is for you?","vs"),
    ("war-thunder-vs-arma","War Thunder vs Arma {y}","War Thunder vs Arma 3/Reforger: vehicle sim comparison.","vs"),
    ("war-thunder-vs-il2","War Thunder vs IL-2 Sturmovik {y}","War Thunder vs IL-2 Sturmovik {y}: free vs paid flight sim comparison.","vs"),
    # GEO PAGES (12)
    ("war-thunder-australia","War Thunder Australia {y}","Play War Thunder free in Australia {y}. Download guide + AU server info.","geo"),
    ("war-thunder-canada","War Thunder Canada {y}","Play War Thunder free in Canada {y}. Download guide + CA server tips.","geo"),
    ("war-thunder-uk","War Thunder UK {y}","Play War Thunder free in the UK {y}. Guide + best British vehicles.","geo"),
    ("war-thunder-new-zealand","War Thunder New Zealand {y}","Play War Thunder free in New Zealand {y}. NZ server guide + tips.","geo"),
    ("war-thunder-south-korea","War Thunder South Korea {y}","Play War Thunder free in South Korea {y}. 워 선더 한국 가이드.","geo"),
    ("war-thunder-germany","War Thunder Germany {y}","Play War Thunder free in Germany {y}. Guide + German tech tree.","geo"),
    ("war-thunder-france","War Thunder France {y}","Jouez à War Thunder gratuitement en France {y}. Guide complet.","geo"),
    ("war-thunder-usa","War Thunder USA {y}","Play War Thunder free in the USA {y}. Guide + American tech tree.","geo"),
    ("war-thunder-spain","War Thunder Spain {y}","Play War Thunder free in Spain {y}. Guía de descarga + servidor.","geo"),
    ("war-thunder-brazil","War Thunder Brazil {y}","Play War Thunder free in Brazil {y}. BR server guide + download.","geo"),
    ("war-thunder-italy","War Thunder Italy {y}","Play War Thunder free in Italy {y}. Guida completa al download.","geo"),
    ("war-thunder-netherlands","War Thunder Netherlands {y}","Play War Thunder free in the Netherlands {y}. NL server guide.","geo"),
    # DOWNLOAD / PLAY INTENT (12)
    ("download-war-thunder-free","Download War Thunder Free","How to download War Thunder 100% free on PC, PS4/5, Xbox.","intent"),
    ("play-war-thunder-free","Play War Thunder Free {y}","Play War Thunder free {y}. Full guide on platforms, download, and getting started.","intent"),
    ("play-war-thunder-online","Play War Thunder Online {y}","How to play War Thunder online {y}. Modes, servers, and tips.","intent"),
    ("war-thunder-sign-up","War Thunder Sign Up {y}","How to sign up for War Thunder {y}. Free account creation guide.","intent"),
    ("war-thunder-create-account","Create War Thunder Account","How to create a free War Thunder account. Step-by-step guide.","intent"),
    ("war-thunder-free-to-play","War Thunder Free to Play {y}","War Thunder free to play {y}: what's included for free players?","intent"),
    ("how-to-play-war-thunder","How to Play War Thunder {y}","How to play War Thunder {y}: beginner guide, modes, and first steps.","intent"),
    ("war-thunder-tutorial","War Thunder Tutorial {y}","War Thunder tutorial guide {y}. How to get through the tutorial fast.","intent"),
    ("war-thunder-first-match","War Thunder First Match Tips {y}","War Thunder first match tips {y}. Survive and thrive from battle 1.","intent"),
    ("war-thunder-new-player-guide","War Thunder New Player Guide {y}","Complete War Thunder new player guide {y}. Everything you need to know.","intent"),
    ("start-playing-war-thunder","Start Playing War Thunder {y}","How to start playing War Thunder {y}. Download, install, first steps.","intent"),
    ("war-thunder-getting-started","War Thunder Getting Started {y}","Getting started in War Thunder {y}. Nation, mode, and vehicle advice.","intent"),
    # STEAM (6)
    ("war-thunder-steam","War Thunder Steam {y}","War Thunder on Steam {y}: download, system requirements, and tips.","steam"),
    ("war-thunder-steam-free","War Thunder Steam Free","Is War Thunder free on Steam? Yes — 100% free, rated Very Positive.","steam"),
    ("best-free-war-games-steam","Best Free War Games Steam {y}","Best free war games on Steam {y}. War Thunder leads the rankings.","steam"),
    ("free-games-steam-war","Free War Games on Steam {y}","Top free war games on Steam {y}. Download War Thunder — no cost.","steam"),
    ("war-thunder-steam-deck","War Thunder Steam Deck {y}","Does War Thunder run on Steam Deck {y}? Performance and settings guide.","steam"),
    ("war-thunder-steam-reviews","War Thunder Steam Reviews {y}","War Thunder Steam review summary {y}. What players say and overall rating.","steam"),
    # CONSOLE (18)
    ("war-thunder-ps4-free","War Thunder PS4 Free","Is War Thunder free on PS4? Yes — no PS Plus required. Guide here.","console"),
    ("war-thunder-ps5-free","War Thunder PS5 Free","Is War Thunder free on PS5? Yes — no PS Plus required. Full guide.","console"),
    ("war-thunder-ps5-upgrade","War Thunder PS5 Upgrade","Does War Thunder support PS5 upgrade? 60fps and improvements explained.","console"),
    ("free-ps4-games-no-subscription","Free PS4 Games No Subscription {y}","Best free PS4 games with no PlayStation Plus {y}. War Thunder is #1.","console"),
    ("free-ps5-games-no-ps-plus","Free PS5 Games No PS Plus {y}","Best free PS5 games with no PS Plus {y}. War Thunder requires no sub.","console"),
    ("war-thunder-xbox-free","War Thunder Xbox Free","Is War Thunder free on Xbox? Yes — no Xbox Game Pass required.","console"),
    ("war-thunder-xbox-series-x","War Thunder Xbox Series X","War Thunder on Xbox Series X: performance, fps, and download guide.","console"),
    ("free-xbox-games-no-gold","Free Xbox Games No Gold {y}","Best free Xbox games without Xbox Live Gold {y}. War Thunder is free.","console"),
    ("war-thunder-ps4-vs-ps5","War Thunder PS4 vs PS5 {y}","War Thunder PS4 vs PS5 comparison: what's different in {y}?","console"),
    ("war-thunder-console-tips","War Thunder Console Tips {y}","Top War Thunder tips for console players {y}. Controller settings guide.","console"),
    ("war-thunder-controller-settings","War Thunder Controller Settings {y}","Best War Thunder controller settings {y}. PS4/PS5/Xbox optimised layout.","console"),
    ("war-thunder-console-vs-pc","War Thunder Console vs PC {y}","War Thunder console vs PC in {y}. Crossplay, performance, and controls.","console"),
    ("free-ps5-games-2025","Free PS5 Games 2025","Best free PS5 games in 2025. War Thunder is a top-tier free title.","console"),
    ("free-ps5-games-2026","Free PS5 Games 2026","Best free PS5 games in 2026 — updated list with War Thunder highlighted.","console"),
    ("free-xbox-games-2025","Free Xbox Games 2025","Best free Xbox games in 2025. War Thunder ranks among the best.","console"),
    ("free-xbox-games-2026","Free Xbox Games 2026","Best free Xbox games in 2026 — comprehensive updated list.","console"),
    ("war-thunder-ps5-settings","War Thunder PS5 Settings {y}","Best War Thunder PS5 settings {y}. Optimised graphics and control layout.","console"),
    ("war-thunder-xbox-settings","War Thunder Xbox Settings {y}","Best War Thunder Xbox settings {y}. Performance and control tips.","console"),
    # HISTORICAL / NICHE (14)
    ("ww2-tank-game-free","Free WW2 Tank Game {y}","Best free WW2 tank games {y}. War Thunder has the largest WW2 tank roster.","hist"),
    ("free-cold-war-games","Free Cold War Games {y}","Best free Cold War era military games {y}. War Thunder spans 1950s–1980s jets.","hist"),
    ("free-modern-military-games","Free Modern Military Games {y}","Best free modern military games {y}. War Thunder includes contemporary vehicles.","hist"),
    ("free-wwii-flight-simulator","Free WWII Flight Simulator {y}","Best free WWII flight simulators {y}. War Thunder's Simulator mode is unmatched.","hist"),
    ("free-vietnam-war-games","Free Vietnam War Games {y}","Free games with Vietnam-era vehicles {y}. War Thunder covers the full Cold War.","hist"),
    ("free-korean-war-games","Free Korean War Games {y}","Free games with Korean War-era vehicles. War Thunder's early jet era covers this.","hist"),
    ("free-world-war-1-games","Free World War 1 Games {y}","Free games with WWI vehicles {y}. War Thunder's earliest aircraft include biplanes.","hist"),
    ("cold-war-tank-games-free","Free Cold War Tank Games {y}","Best free Cold War tank games {y}. War Thunder covers Rank V–VII perfectly.","hist"),
    ("free-jet-fighter-games","Free Jet Fighter Games {y}","Best free jet fighter games {y}. War Thunder's jet era spans 1944 to today.","hist"),
    ("free-biplane-games","Free Biplane Games {y}","Free games with biplane aircraft {y}. War Thunder's early tiers have 100+ biplanes.","hist"),
    ("free-ww2-simulation-games","Free WW2 Simulation Games {y}","Best free WW2 simulation games {y}. War Thunder leads on historical accuracy.","hist"),
    ("war-thunder-historical-accuracy","War Thunder Historical Accuracy {y}","How historically accurate is War Thunder {y}? Vehicles, maps, and physics.","hist"),
    ("ww2-games-free-pc","Free WW2 PC Games {y}","Best free WW2 PC games {y}. Top picks including War Thunder.","hist"),
    ("free-tank-simulator","Free Tank Simulator {y}","Best free tank simulators {y}. War Thunder's Realistic Battles mode qualifies.","hist"),
    # CROSSOUT CROSSOVER (4)
    ("crossout-vs-war-thunder","Crossout vs War Thunder {y}","Crossout vs War Thunder {y}: which free vehicle game should you play?","cross"),
    ("war-thunder-crossout","War Thunder and Crossout {y}","War Thunder and Crossout compared: which Gaijin free game wins?","cross"),
    ("gaijin-free-games","Gaijin Free Games {y}","All free games by Gaijin Entertainment {y}. War Thunder, Crossout, Enlisted.","cross"),
    ("enlisted-vs-war-thunder","Enlisted vs War Thunder {y}","Enlisted vs War Thunder {y}: two free Gaijin games compared in full.","cross"),
    # ECONOMIC / VALUE (10)
    ("is-war-thunder-worth-it","Is War Thunder Worth It {y}?","Is War Thunder worth playing in {y}? Honest pros and cons review.","value"),
    ("war-thunder-free-content","War Thunder Free Content {y}","How much content is free in War Thunder {y}? Full breakdown for free players.","value"),
    ("war-thunder-no-money","Play War Thunder Without Spending Money","Can you enjoy War Thunder without spending money? Yes — here's how.","value"),
    ("war-thunder-f2p-progression","War Thunder F2P Progression {y}","How far can you get for free in War Thunder {y}? Progression guide.","value"),
    ("war-thunder-premium-worth-it","Is War Thunder Premium Worth It {y}?","Honest review: is War Thunder premium account worth buying in {y}?","value"),
    ("war-thunder-free-premium","War Thunder Free Premium Time {y}","How to get free premium time in War Thunder {y}. Events and methods.","value"),
    ("war-thunder-spending-guide","War Thunder Spending Guide {y}","If you want to spend on War Thunder {y}, here's what gives the best value.","value"),
    ("war-thunder-free-vehicles","War Thunder Free Premium Vehicles {y}","How to earn free premium vehicles in War Thunder {y} without paying.","value"),
    ("war-thunder-gaijin-coins","War Thunder Gaijin Coins {y}","What are Gaijin Coins? How to buy and use them in War Thunder {y}.","value"),
    ("war-thunder-vs-paid-games","War Thunder vs Paid Military Games {y}","War Thunder (free) vs paid military games {y}: is free good enough?","value"),
    # TECHNICAL (18)
    ("war-thunder-system-requirements","War Thunder System Requirements {y}","War Thunder PC system requirements {y}: minimum and recommended specs.","tech"),
    ("war-thunder-low-end-pc","War Thunder Low End PC {y}","Can War Thunder run on a low-end PC? Settings guide for weak hardware.","tech"),
    ("war-thunder-fps-boost","War Thunder FPS Boost Guide {y}","How to boost FPS in War Thunder {y}. Best graphics settings.","tech"),
    ("war-thunder-lag-fix","War Thunder Lag Fix {y}","How to fix lag in War Thunder {y}. Ping reduction and connection tips.","tech"),
    ("war-thunder-not-launching","War Thunder Not Launching Fix","War Thunder won't launch? Full fix guide for PC.","tech"),
    ("war-thunder-file-size","War Thunder File Size {y}","How big is War Thunder {y}? Download size on all platforms.","tech"),
    ("war-thunder-controller","War Thunder Controller Support","Does War Thunder support controllers? Full guide for PC, PS, Xbox.","tech"),
    ("war-thunder-crossplay","War Thunder Crossplay {y}","Does War Thunder have crossplay {y}? PC, PS4/5, Xbox cross-platform guide.","tech"),
    ("war-thunder-mac","War Thunder Mac {y}","Can you play War Thunder on Mac {y}? macOS support and performance guide.","tech"),
    ("war-thunder-linux","War Thunder Linux {y}","War Thunder on Linux {y}: Proton, native client, and performance guide.","tech"),
    ("war-thunder-graphics-settings","War Thunder Graphics Settings {y}","Optimal War Thunder graphics settings {y} for performance and quality.","tech"),
    ("war-thunder-ping-fix","War Thunder Ping Fix {y}","How to reduce War Thunder ping {y}. Server selection and network tips.","tech"),
    ("war-thunder-crash-fix","War Thunder Crash Fix {y}","War Thunder keeps crashing? Complete fix guide for all platforms {y}.","tech"),
    ("war-thunder-vulkan","War Thunder Vulkan {y}","War Thunder Vulkan API guide {y}. Better performance on compatible GPUs.","tech"),
    ("war-thunder-dx12","War Thunder DirectX 12 {y}","War Thunder DirectX 12 setup {y}. Performance improvements and how to enable.","tech"),
    ("war-thunder-minimum-specs","War Thunder Minimum Specs {y}","Absolute minimum specs to run War Thunder {y}. Can your PC handle it?","tech"),
    ("war-thunder-4k","War Thunder 4K {y}","War Thunder in 4K {y}: performance guide and recommended specs.","tech"),
    ("war-thunder-ultrawide","War Thunder Ultrawide {y}","War Thunder ultrawide monitor support {y}: setup and settings guide.","tech"),
    # NATION PAGES WITH TIER TABLES (4)
    ("war-thunder-usa-tanks","War Thunder USA Tanks {y}","Best US tanks in War Thunder {y}. Full American ground forces tech tree guide.","nation"),
    ("war-thunder-germany-tanks","War Thunder Germany Tanks {y}","Best German tanks in War Thunder {y}. Complete Germany ground forces guide.","nation"),
    ("war-thunder-russia-tanks","War Thunder Russia Tanks {y}","Best Soviet/Russian tanks in War Thunder {y}. USSR ground forces guide.","nation"),
    ("war-thunder-britain-tanks","War Thunder Britain Tanks {y}","Best British tanks in War Thunder {y}. UK ground forces complete guide.","nation"),
    # MISC / LONG TAIL (49)
    ("war-thunder-mobile","War Thunder Mobile {y}","War Thunder Mobile {y}: iOS and Android guide. Differences from PC version.","misc"),
    ("war-thunder-twitch-drops","War Thunder Twitch Drops {y}","How to get War Thunder Twitch drops {y}. Free rewards guide.","misc"),
    ("war-thunder-referral","War Thunder Referral Code {y}","War Thunder referral program {y}. How to refer friends and earn rewards.","misc"),
    ("war-thunder-account-link","Link War Thunder Accounts {y}","How to link War Thunder accounts across PC, PS4, and Xbox.","misc"),
    ("war-thunder-clans","War Thunder Clans {y}","How to join or create a clan in War Thunder {y}. Best active clans.","misc"),
    ("war-thunder-esports","War Thunder Esports {y}","War Thunder esports and tournaments {y}. Competitive scene overview.","misc"),
    ("war-thunder-youtubers","Best War Thunder YouTubers {y}","Best War Thunder YouTube channels {y} to learn and be entertained.","misc"),
    ("war-thunder-reddit","War Thunder Reddit {y}","War Thunder Reddit community {y}. Best subreddits and top threads.","misc"),
    ("war-thunder-discord","War Thunder Discord {y}","Best War Thunder Discord servers {y}. Official and community servers.","misc"),
    ("war-thunder-wiki","War Thunder Wiki {y}","Using the War Thunder wiki {y}. Best pages for beginners and veterans.","misc"),
    ("war-thunder-test-drive","War Thunder Test Drive {y}","How to test drive vehicles in War Thunder {y}. Free trials guide.","misc"),
    ("war-thunder-free-to-play-2025","War Thunder Free to Play 2025","Is War Thunder still worth playing free in 2025?","misc"),
    ("war-thunder-free-to-play-2026","War Thunder Free to Play 2026","Is War Thunder worth playing free in 2026? Updated guide.","misc"),
    ("war-thunder-new-players-2026","War Thunder New Players 2026","War Thunder in 2026: is it too late to start? Guide for new players.","misc"),
    ("war-thunder-ranked","War Thunder Ranked {y}","War Thunder ranked modes and competitive play guide {y}.","misc"),
    ("war-thunder-decals","War Thunder Decals {y}","War Thunder decals and camouflage guide {y}. Free and premium camos.","misc"),
    ("war-thunder-aces","War Thunder Aces of Thunder {y}","War Thunder VR mode Aces of Thunder {y}: what it is and how to play.","misc"),
    ("war-thunder-gaijin-pass","Gaijin Pass War Thunder {y}","What is Gaijin Pass in War Thunder {y}? Account security guide.","misc"),
    ("war-thunder-market","War Thunder Market {y}","War Thunder Marketplace {y}: how to buy, sell, and trade items.","misc"),
    ("war-thunder-warbonds","War Thunder Warbonds {y}","War Thunder Warbonds guide {y}. What are they and how to earn them fast.","misc"),
    ("war-thunder-spare-parts","War Thunder Spare Parts and FPE {y}","War Thunder spare parts and fire extinguishers guide {y}.","misc"),
    ("war-thunder-modifications","War Thunder Modifications Guide {y}","War Thunder vehicle modifications guide {y}. Which to unlock first.","misc"),
    ("war-thunder-ammo-types","War Thunder Ammo Types {y}","War Thunder ammo types explained {y}. AP, APHE, HEAT, APDS, APFSDS guide.","misc"),
    ("war-thunder-bushes","War Thunder Bushes {y}","War Thunder bushes and camouflage mechanic {y}. How they work.","misc"),
    ("war-thunder-rangefinder","War Thunder Rangefinder {y}","Using the War Thunder rangefinder {y}. How to range targets accurately.","misc"),
    ("war-thunder-spotting","War Thunder Spotting Mechanic {y}","War Thunder spotting explained {y}. How to spot and be spotted.","misc"),
    ("war-thunder-bombing","War Thunder Bombing Guide {y}","War Thunder bombing guide {y}. How to destroy bases and ground targets.","misc"),
    ("war-thunder-gunner","War Thunder Gunner Position {y}","Using the gunner position in War Thunder {y}. Tips and controls.","misc"),
    ("war-thunder-pilot-snipe","War Thunder Pilot Sniping {y}","War Thunder pilot sniping guide {y}. How it works and how to counter it.","misc"),
    ("war-thunder-spawn-points","War Thunder Spawn Points {y}","How War Thunder spawn points work {y}. How to earn more SP quickly.","misc"),
    ("war-thunder-battle-rating","War Thunder Battle Rating Explained {y}","War Thunder Battle Rating system explained {y}. BR spread and compression.","misc"),
    ("war-thunder-research-points","War Thunder Research Points {y}","War Thunder RP guide {y}. How to earn research points faster.","misc"),
    ("war-thunder-ace-crew","War Thunder Ace Crew {y}","War Thunder Ace Crew guide {y}. How to get ace crews and what they do.","misc"),
    ("war-thunder-artillery","War Thunder Artillery {y}","War Thunder artillery call-in guide {y}. How to use and counter it.","misc"),
    ("war-thunder-air-spawn","War Thunder Air Spawn {y}","War Thunder air spawn guide {y}. Which aircraft get air spawn and why.","misc"),
    ("war-thunder-flares","War Thunder Flares {y}","War Thunder flares guide {y}. How to use countermeasures against missiles.","misc"),
    ("war-thunder-missile-guide","War Thunder Missile Guide {y}","War Thunder missiles explained {y}. ATGM, SAM, and AAM types.","misc"),
    ("war-thunder-best-starter-vehicle","War Thunder Best Starter Vehicle {y}","Best starter vehicles in War Thunder {y} for each nation.","misc"),
    ("war-thunder-low-tier","War Thunder Low Tier Guide {y}","War Thunder low tier guide {y}. Best vehicles and tactics at BR 1.0–3.0.","misc"),
    ("war-thunder-mid-tier","War Thunder Mid Tier Guide {y}","War Thunder mid tier guide {y}. Best vehicles and tactics at BR 4.0–7.0.","misc"),
    ("war-thunder-high-tier","War Thunder High Tier Guide {y}","War Thunder high tier guide {y}. Best vehicles and tactics at BR 8.0–10.0.","misc"),
    ("war-thunder-air-sim","War Thunder Air Simulator Guide {y}","War Thunder Air Simulator (SB) guide {y}. Cockpit, navigation, and combat.","misc"),
    ("war-thunder-naval-arcade","War Thunder Naval Arcade {y}","War Thunder Naval Arcade guide {y}. Best ships and tips for new players.","misc"),
    ("war-thunder-combined-arms","War Thunder Combined Arms {y}","War Thunder combined arms battles {y}. How tanks, planes, and helis interact.","misc"),
    ("war-thunder-map-guide","War Thunder Maps Guide {y}","War Thunder maps guide {y}. Best positions on popular maps.","misc"),
    ("war-thunder-winter-maps","War Thunder Winter Maps {y}","War Thunder winter maps guide {y}. Best vehicles for snow and ice maps.","misc"),
    ("war-thunder-urban-maps","War Thunder Urban Maps {y}","War Thunder urban maps guide {y}. Best tactics and vehicle choices.","misc"),
    ("war-thunder-open-maps","War Thunder Open Maps {y}","War Thunder open field maps guide {y}. Long-range sniping tips.","misc"),
]

# Deduplicate KEYWORDS (nation slugs appear twice in the list above — keep first occurrence)
_seen = set()
_kw_deduped = []
for entry in KEYWORDS:
    if entry[0] not in _seen:
        _seen.add(entry[0])
        _kw_deduped.append(entry)
KEYWORDS = _kw_deduped


# ── BLOG POSTS (20) ───────────────────────────────────────────────────────────
BLOG_POSTS = [
    {"slug":"best-nation-beginners","title":f"Best Nation for Beginners in War Thunder {YEAR}","date":"2025-01-10","desc":f"Choosing your first nation in War Thunder can feel overwhelming. Here's the definitive {YEAR} guide.","body":f"""<p>When you first launch War Thunder, you'll be asked to choose a nation. Here's the full breakdown for {YEAR}.</p>
<h2>Top 3 Nations for Beginners</h2>
<div class="tbl-wrap"><table class="compare-table"><tr><th>Nation</th><th>Playstyle</th><th>Difficulty</th><th>Top-Tier MBT</th></tr>
<tr><td><strong>USA</strong></td><td>All-round</td><td class="winner">Easy</td><td>M1A2 SEP v2</td></tr>
<tr><td>USSR</td><td>Aggressive brawler</td><td>Medium</td><td>T-90M</td></tr>
<tr><td>Germany</td><td>Long-range sniper</td><td>Medium</td><td>Leopard 2A7V</td></tr></table></div>
<p><strong>USA</strong> — well-armoured Shermans at low tier, forgiving aircraft, smooth tech tree. Best for beginners.<br>
<strong>USSR</strong> — sloped T-34 armour bounces shells, high reward, steeper learning curve.<br>
<strong>Germany</strong> — best optics and penetration, requires more map knowledge.</p>
<p>All three nations are free. <a href="{AFF_URL}" rel="nofollow sponsored">Download War Thunder here</a> and try them all.</p>"""},
    {"slug":"war-thunder-vs-world-of-tanks","title":f"War Thunder vs World of Tanks {YEAR}: Definitive Comparison","date":"2025-02-14","desc":"Tank enthusiasts debate War Thunder vs World of Tanks. Here's the honest breakdown.","body":f"""<p>Both games have millions of active players but offer very different experiences in {YEAR}.</p>
<div class="tbl-wrap"><table class="compare-table"><tr><th>Category</th><th>War Thunder</th><th>World of Tanks</th></tr>
<tr><td>Price</td><td class="winner">Free</td><td class="winner">Free</td></tr>
<tr><td>Vehicle Types</td><td class="winner">Air + Ground + Naval</td><td class="loser">Tanks only</td></tr>
<tr><td>Physics</td><td class="winner">Real ballistics</td><td class="loser">HP system</td></tr>
<tr><td>Vehicle Count</td><td class="winner">2,000+</td><td>~600</td></tr>
<tr><td>Platforms + Crossplay</td><td class="winner">PC/PS/Xbox + Yes</td><td>PC/Console, No crossplay</td></tr>
<tr><td>Beginner Friendliness</td><td>Medium</td><td class="winner">High</td></tr></table></div>
<h2>Verdict</h2>
<p>For realism and content: <strong>War Thunder</strong>. For casual pure-tank arcade: <strong>WoT</strong>. Try War Thunder first — <a href="{AFF_URL}" rel="nofollow sponsored">download free here</a>.</p>"""},
    {"slug":"silver-lions-farming-guide","title":f"Best Ways to Farm Silver Lions in War Thunder {YEAR}","date":"2025-03-05","desc":f"Silver Lions are War Thunder's main currency. Here are the most efficient farming methods in {YEAR}.","body":f"""<p>Running out of Silver Lions (SL) is one of the most frustrating War Thunder experiences. Here's how to stay profitable in {YEAR}.</p>
<h2>Top 5 SL Farming Methods</h2>
<p><strong>1. Base Bombing in Air RB</strong> — Destroy bases with bombers (IL-4, B-17). Earns 10,000–30,000 SL per run even with average performance.<br>
<strong>2. Premium Account</strong> — Doubles SL earned every match. One month (~$10) pays for itself in saved repair costs within days.<br>
<strong>3. Low-Tier Sessions (BR 1.0–2.0)</strong> — Repair costs near zero, winning streaks earn pure positive SL.<br>
<strong>4. Daily Tasks</strong> — Always complete the daily mission before your session. It awards SL multipliers.<br>
<strong>5. Events and Battle Pass</strong> — Seasonal events regularly reward large SL bonuses for participation.</p>
<p><a href="{AFF_URL}" rel="nofollow sponsored">Download War Thunder free</a> and start farming today.</p>"""},
    {"slug":"war-thunder-beginners-guide","title":f"War Thunder Complete Beginner Guide {YEAR}","date":"2025-04-01","desc":f"Everything a new War Thunder player needs to know in {YEAR}. Modes, nations, tips, and more.","body":f"""<p>War Thunder is one of the deepest free games on the market. This guide gets you from zero to winning in {YEAR}.</p>
<h2>The Three Modes</h2>
<div class="tbl-wrap"><table class="compare-table"><tr><th>Mode</th><th>Difficulty</th><th>Best For</th></tr>
<tr><td>Arcade Battles</td><td class="winner">Easy</td><td>Learning controls and maps</td></tr>
<tr><td>Realistic Battles</td><td>Medium</td><td>Main competitive mode</td></tr>
<tr><td>Simulator Battles</td><td>Hard</td><td>Hardcore immersion</td></tr></table></div>
<h2>Your First 10 Hours</h2>
<p>Hours 1–2: Complete the tutorial. Hours 2–5: Arcade Battles at Rank I. Hours 5–10: Transition to Realistic Battles once you understand armour angles. Never rush the tech tree — each BR range has a unique and fun meta.</p>
<h2>Key Habits to Build Early</h2>
<p>Open the Armour Viewer before queuing in a new tank. Prioritise Agility and Vitality crew skills first. Always complete the daily task for SL multipliers.</p>
<p><a href="{AFF_URL}" rel="nofollow sponsored">Download War Thunder free</a> and apply these tips today.</p>"""},
    {"slug":"war-thunder-fps-guide","title":f"War Thunder FPS Boost Guide {YEAR}","date":"2025-05-10","desc":f"How to get more FPS in War Thunder {YEAR}. Settings, launch options, and hardware tips.","body":f"""<p>War Thunder's Dagor Engine is well-optimised but default settings favour visuals. Here's how to maximise FPS in {YEAR}.</p>
<div class="tbl-wrap"><table class="compare-table"><tr><th>Setting</th><th>Recommended</th><th>FPS Gain</th></tr>
<tr><td>Shadow Quality</td><td>Low or Medium</td><td class="winner">High</td></tr>
<tr><td>SSAO</td><td>Off</td><td>Medium</td></tr>
<tr><td>Grass Density</td><td>Low</td><td>Medium</td></tr>
<tr><td>DLSS/FSR</td><td>Quality mode</td><td class="winner">Very High</td></tr>
<tr><td>Motion Blur</td><td>Off</td><td>Small</td></tr></table></div>
<h2>Steam Launch Options</h2>
<p>Add <code>-dx12</code> for modern Nvidia/AMD GPUs, <code>-dx11</code> for older hardware, <code>-vulkan</code> on Linux.</p>
<p>War Thunder is <a href="{AFF_URL}" rel="nofollow sponsored">free to download</a> — optimise and dominate.</p>"""},
    {"slug":"war-thunder-best-premium-vehicles","title":f"Best Premium Vehicles in War Thunder {YEAR}","date":"2025-06-15","desc":f"Which premium vehicles are worth buying in War Thunder {YEAR}? Full ranked list.","body":f"""<p>Premium vehicles earn 200–300% more RP and SL than standard vehicles. Here are the best picks for {YEAR}.</p>
<div class="tbl-wrap"><table class="compare-table"><tr><th>Nation</th><th>Vehicle</th><th>BR</th><th>Why It's Worth It</th></tr>
<tr><td>USSR</td><td>T-54 1951</td><td>8.3</td><td>Outstanding armour + SL earner</td></tr>
<tr><td>USA</td><td>M1 KVT</td><td>10.0</td><td>Top-tier Abrams hull, devastates</td></tr>
<tr><td>Germany</td><td>Leopard A1A1 L/44</td><td>9.7</td><td>High-pen APFSDS, great mobility</td></tr>
<tr><td>UK</td><td>Centurion Mk.5 AVRE</td><td>7.3</td><td>Unique derp, high SL earner</td></tr>
<tr><td>USA (Air)</td><td>F-89B</td><td>7.3</td><td>Rocket-heavy jet, SL grinder</td></tr></table></div>
<p>Try the free game first. <a href="{AFF_URL}" rel="nofollow sponsored">Download here</a> before spending anything.</p>"""},
    {"slug":"war-thunder-crossplay-guide","title":f"War Thunder Crossplay Guide {YEAR}","date":"2025-07-20","desc":f"Full crossplay guide for War Thunder {YEAR}. PC, PS4/5, and Xbox cross-platform explained.","body":f"""<p>War Thunder supports full crossplay between all platforms in {YEAR}.</p>
<div class="tbl-wrap"><table class="compare-table"><tr><th>Feature</th><th>Status</th></tr>
<tr><td>PC ↔ PS4/PS5 matchmaking</td><td class="winner">✅ On by default</td></tr>
<tr><td>PC ↔ Xbox matchmaking</td><td class="winner">✅ On by default</td></tr>
<tr><td>Universal account (all platforms)</td><td class="winner">✅ Full sync</td></tr>
<tr><td>Progress carries across platforms</td><td class="winner">✅ Vehicles, SL, RP all sync</td></tr>
<tr><td>Squad with cross-platform friends</td><td class="winner">✅ Search by Gaijin username</td></tr></table></div>
<p>Play War Thunder free on any platform: <a href="{AFF_URL}" rel="nofollow sponsored">download here</a>.</p>"""},
    {"slug":"war-thunder-naval-guide","title":f"War Thunder Naval Forces Guide {YEAR}","date":"2025-08-18","desc":f"Complete War Thunder naval forces guide for {YEAR}. Ships, destroyers, battleships explained.","body":f"""<p>Naval is War Thunder's most underplayed branch — shorter queues and faster progress in {YEAR}.</p>
<div class="tbl-wrap"><table class="compare-table"><tr><th>Nation</th><th>Strength</th><th>Best Early Ship</th></tr>
<tr><td>USA</td><td>Fast PT boats, strong destroyers</td><td>PT-103</td></tr>
<tr><td>USSR</td><td>Heavy armour, powerful guns</td><td>BMO gunboat</td></tr>
<tr><td>Germany</td><td>Fast S-Boote torpedo boats</td><td>S-100</td></tr>
<tr><td>UK</td><td>Strong destroyers</td><td>MTB-1 1 Vosper</td></tr></table></div>
<h2>Key Tips</h2><ul><li>Aim for the waterline to flood opponents</li><li>Target ammo racks for instant kills</li><li>Never stay stationary — ships die fast under fire</li></ul>
<p><a href="{AFF_URL}" rel="nofollow sponsored">Download War Thunder free</a> and take to the seas.</p>"""},
    {"slug":"war-thunder-helicopter-guide","title":f"War Thunder Helicopter Guide {YEAR}","date":"2025-09-12","desc":f"Best helicopters in War Thunder {YEAR} and how to use them in Ground RB.","body":f"""<p>Helicopters are punishing to learn but can single-handedly swing matches in {YEAR}.</p>
<div class="tbl-wrap"><table class="compare-table"><tr><th>Nation</th><th>Helicopter</th><th>BR</th><th>Best For</th></tr>
<tr><td>USSR</td><td>Mi-4AV</td><td>7.7</td><td>Easy to fly, unguided rockets</td></tr>
<tr><td>USA</td><td>UH-1B (Huey)</td><td>8.3</td><td>Beginner-friendly, rockets + guns</td></tr>
<tr><td>Germany</td><td>BO 105 PAH-1</td><td>9.3</td><td>HOT ATGMs, small profile</td></tr></table></div>
<h2>Golden Rules</h2><ul><li>Never hover stationary — SPAA locks on in 3 seconds</li><li>Kill SPAA before engaging tanks</li><li>Use terrain masking — pop up, fire, drop back</li><li>Above BR 9.0: always carry flares</li></ul>
<p><a href="{AFF_URL}" rel="nofollow sponsored">Download War Thunder free</a>.</p>"""},
    {"slug":"war-thunder-realistic-battles-guide","title":f"War Thunder Realistic Battles Guide {YEAR}","date":"2025-10-08","desc":f"How to succeed in War Thunder Realistic Battles in {YEAR}. Tactics, positioning, aiming.","body":f"""<p>Realistic Battles (RB) is War Thunder's most popular mode. No lead indicators, real physics, one life per vehicle.</p>
<div class="tbl-wrap"><table class="compare-table"><tr><th>Feature</th><th>Arcade</th><th>Realistic</th></tr>
<tr><td>Lead indicator</td><td>Yes</td><td class="winner">No</td></tr>
<tr><td>Nametags on enemies</td><td>Yes</td><td class="winner">No</td></tr>
<tr><td>Physics</td><td>Partial</td><td class="winner">Full simulation</td></tr>
<tr><td>Spawns per vehicle</td><td>3</td><td>1</td></tr></table></div>
<h2>Core Principles</h2>
<p><strong>Patience wins.</strong> Rushing gets you killed in 90 seconds. <strong>Hull-down is king.</strong> Only expose your turret. <strong>First shot wins.</strong> In RB a penetrating hit usually kills — miss and take return fire before reloading.</p>
<p><a href="{AFF_URL}" rel="nofollow sponsored">Download War Thunder free</a>.</p>"""},
    {"slug":"war-thunder-golden-eagles-guide","title":f"How to Get Golden Eagles in War Thunder {YEAR}","date":"2025-11-01","desc":f"Legitimate ways to earn free Golden Eagles in War Thunder {YEAR}. No hacks, no scams.","body":f"""<p>Golden Eagles (GE) are War Thunder's premium currency. Legitimate free methods in {YEAR}:</p>
<p><strong>1. Twitch Drops</strong> — Watch official War Thunder streams during campaigns (check the official site). Awards GE and premium vehicles.<br>
<strong>2. Community Contests</strong> — Screenshot and art contests on the War Thunder forums award up to 5,000 GE.<br>
<strong>3. Battle Pass Free Track</strong> — Completing all tasks each season awards small amounts of GE.<br>
<strong>4. Content Creator Program</strong> — YouTube/Twitch creators can apply for the Gaijin partner program.</p>
<h2>Avoid Scams</h2>
<p>Any site claiming to generate free GE is a credential-stealing scam. Gaijin cannot add GE to accounts via third-party tools.</p>
<p><a href="{AFF_URL}" rel="nofollow sponsored">Download War Thunder free</a> — earn your eagles legitimately.</p>"""},
    {"slug":"war-thunder-update-history","title":f"War Thunder Major Updates {YEAR}","date":"2025-12-01","desc":f"War Thunder's biggest updates and what they added. Full update history through {YEAR}.","body":f"""<p>Gaijin releases 4–6 major named updates per year, each adding hundreds of vehicles and new mechanics.</p>
<p><strong>Seek &amp; Destroy (2024)</strong> — Customisable tank commanders, reworked crew mechanics, F-15E Strike Eagle, Su-30SM.<br>
<strong>Air Superiority (2023)</strong> — F-16C, MiG-29SMT, Eurofighter Typhoon (early access), Israeli aircraft expansion.<br>
<strong>Kings of Battle (2023)</strong> — Surface-to-surface missiles, Guided Bomb Units, major naval rework.<br>
<strong>La Royale (2023)</strong> — French and Italian naval tech trees added from scratch.</p>
<p>Follow the official Dev Blog for upcoming content 2–3 weeks before each patch. <a href="{AFF_URL}" rel="nofollow sponsored">Download War Thunder free</a>.</p>"""},
    {"slug":"war-thunder-economy-guide","title":f"War Thunder Economy Guide {YEAR} — SL, RP, GE Explained","date":"2026-01-15","desc":f"Full War Thunder economy guide for {YEAR}. How Silver Lions, Research Points, and Golden Eagles work.","body":f"""<p>War Thunder's economy is the #1 source of confusion for new players. Here's the complete breakdown for {YEAR}.</p>
<div class="tbl-wrap"><table class="compare-table"><tr><th>Currency</th><th>Earned By</th><th>Spent On</th></tr>
<tr><td>Silver Lions (SL)</td><td>Playing battles</td><td>Vehicles, repairs, ammo, mods</td></tr>
<tr><td>Research Points (RP)</td><td>Playing battles</td><td>New vehicle/mod research</td></tr>
<tr><td>Golden Eagles (GE)</td><td>Purchase / events</td><td>Premium vehicles, premium time</td></tr></table></div>
<h2>Key Rules</h2>
<p>At high BRs (9.0+) repair costs spike. If SL is tight, drop to Rank II/III to rebuild. Premium account (~$10/month) doubles both SL and RP — worth it if you play 5+ hours/week. One Talisman on your favourite vehicle permanently doubles RP and improves performance.</p>
<p><a href="{AFF_URL}" rel="nofollow sponsored">Start playing War Thunder free</a>.</p>"""},
    {"slug":"war-thunder-crew-skills-guide","title":f"War Thunder Crew Skills Guide {YEAR}","date":"2026-02-10","desc":f"Best crew skills to prioritize in War Thunder {YEAR}. Ground, air, and naval priority guide.","body":f"""<p>Crew skills are War Thunder's most impactful and most neglected progression system. Here's what to prioritise in {YEAR}.</p>
<div class="tbl-wrap"><table class="compare-table"><tr><th>Skill</th><th>Priority</th><th>Effect</th></tr>
<tr><td>Agility (Driver/Gunner)</td><td class="winner">1st</td><td>Faster turret + hull traverse</td></tr>
<tr><td>Vitality (All crew)</td><td class="winner">2nd</td><td>Crew survives more hits</td></tr>
<tr><td>Keen Vision (Commander)</td><td>3rd</td><td>Spot enemies at longer range</td></tr>
<tr><td>Reload Speed (Loader)</td><td>4th</td><td>Faster reload — huge DPS gain</td></tr>
<tr><td>G-Tolerance (Pilot)</td><td class="winner">1st (Air)</td><td>No blackout in hard turns</td></tr></table></div>
<p>After maxing skills, pay SL to "Expert qualify" crews for a +3 to all skills — essential on vehicles you play often.</p>
<p><a href="{AFF_URL}" rel="nofollow sponsored">Download War Thunder free</a>.</p>"""},
    {"slug":"war-thunder-top-tier-guide","title":f"War Thunder Top Tier Guide {YEAR} — BR 11.0+","date":"2026-03-05","desc":f"Complete guide to War Thunder top-tier gameplay {YEAR}. Best vehicles, maps, and tactics.","body":f"""<p>Top tier (BR 11.0–12.0+) is the pinnacle of War Thunder in {YEAR} — 4th-gen MBTs, composite armour, and active protection systems.</p>
<div class="tbl-wrap"><table class="compare-table"><tr><th>Nation</th><th>Top MBT</th><th>BR</th><th>Standout Trait</th></tr>
<tr><td>USA</td><td>M1A2 SEP V2</td><td>11.7</td><td>Fast reload, strong turret</td></tr>
<tr><td>USSR</td><td>T-90M</td><td>11.7</td><td>Relikt ERA, strong gun</td></tr>
<tr><td>Germany</td><td>Leopard 2A7V</td><td>11.7</td><td>Best all-round protection</td></tr>
<tr><td>UK</td><td>Challenger 3 TD</td><td>11.7</td><td>Excellent gun and optics</td></tr>
<tr><td>Israel</td><td>Merkava Mk.4M</td><td>11.7</td><td>Trophy APS system</td></tr></table></div>
<h2>Top-Tier Rules</h2><ul><li>Use thermals always — everyone has them, you lose without them</li><li>Speed of engagement wins — most shells penetrate most targets</li><li>Avoid open ground — helicopter ATGMs cover every exposed position</li></ul>
<p><a href="{AFF_URL}" rel="nofollow sponsored">Download War Thunder free</a> and start the grind.</p>"""},
    {"slug":"war-thunder-air-rb-guide","title":f"War Thunder Air Realistic Battles Guide {YEAR}","date":"2026-04-01","desc":f"Complete Air RB guide for War Thunder {YEAR}. Energy fighting, BnZ, jet tactics.","body":f"""<p>Air RB is where War Thunder aviation shines in {YEAR}. Real energy models, no lead indicators, multi-minute tactical fights.</p>
<h2>Three Fighting Concepts</h2>
<p><strong>Boom and Zoom (BnZ)</strong> — Dive from altitude, fire, climb back. Best for: Bf 109, P-47, early jets.<br>
<strong>Turn Fighting</strong> — Out-turn in sustained circles. Best for: Zero, Yak-3, Spitfire.<br>
<strong>Head-On</strong> — High-risk direct attack. Only valid with fast, heavy cannons.</p>
<h2>Altitude = Life</h2>
<p>Never waste altitude. A pilot at 5,000m diving has 800 km/h available. A pilot at 1,000m climbing bleeds speed until they stall. Always climb before engaging.</p>
<h2>Jet-Era Tips</h2><ul><li>Missiles can be dodged with tight turns and flares at range</li><li>Supersonic jets bleed speed turning — fight in the vertical</li><li>RWR notching: fly 90° perpendicular to incoming radar to break lock</li></ul>
<p><a href="{AFF_URL}" rel="nofollow sponsored">Download War Thunder free</a>.</p>"""},
    {"slug":"war-thunder-sound-and-graphic-mods","title":f"Best War Thunder Mods {YEAR} — Sounds, Sights, Skins","date":"2026-04-20","desc":f"Best War Thunder mods {YEAR}: sound mods, gun sight mods, and historical skins. Install guide.","body":f"""<p>Gaijin officially supports user skins and sight mods via the CDK. Here are the best mods to install in {YEAR}.</p>
<p><strong>Sound Mods</strong> — Community mods with higher-fidelity engine audio. Find them on live.warthunder.com. Install .blk and .ogg files into the UserSounds folder.<br>
<strong>Historical Sights</strong> — Period-accurate gun reticles (Soviet 1943, US M70D periscope). Download .blk files from live.warthunder.com.<br>
<strong>Historical Skins</strong> — Museum-quality .dds camouflage textures for every vehicle. Place in UserSkins within the vehicle's folder.</p>
<h2>Install Rules</h2><ul><li>Only download from live.warthunder.com — the official Gaijin mod marketplace</li><li>Never use third-party file patchers — anti-cheat bans result</li></ul>
<p><a href="{AFF_URL}" rel="nofollow sponsored">Download War Thunder free</a>.</p>"""},
    {"slug":"war-thunder-battle-pass-guide","title":f"War Thunder Battle Pass Guide {YEAR}","date":"2026-05-01","desc":f"War Thunder Battle Pass {YEAR}: what you get, cost, free vs paid, and is it worth it?","body":f"""<p>War Thunder's Battle Pass runs ~90 days per season with a premium vehicle as the top reward.</p>
<div class="tbl-wrap"><table class="compare-table"><tr><th>Track</th><th>Cost</th><th>Top Reward</th></tr>
<tr><td>Free Track</td><td class="winner">Free</td><td>Cosmetics, boosters, some GE</td></tr>
<tr><td>Premium (Basic)</td><td>~2,500 GE</td><td>Unique premium vehicle</td></tr>
<tr><td>Premium + Boost</td><td>~4,500 GE</td><td>Same + 25 levels instantly</td></tr></table></div>
<p>Daily tasks award 100 BP XP each — completing them takes 1–2 battles. Play 30 min/day and you can finish the full pass without the boost. The premium vehicle is typically worth 3,000–6,000 GE standalone, making the ~2,500 GE pass excellent value for active players.</p>
<p><a href="{AFF_URL}" rel="nofollow sponsored">Download War Thunder free</a>.</p>"""},
    {"slug":"war-thunder-squadron-guide","title":f"War Thunder Squadron Guide {YEAR}","date":"2026-05-15","desc":f"War Thunder squadron guide {YEAR}: how to find a clan, squadron vehicles, and squad play tips.","body":f"""<p>Joining a squadron in War Thunder unlocks exclusive vehicles and +20% RP for your whole squad in {YEAR}.</p>
<h2>What Squadrons Give You</h2><ul><li><strong>Squadron vehicles</strong> — unique premiums earnable only through Squadron Research Points (SRP)</li><li><strong>+20% RP bonus</strong> when 4 squadron members play together</li><li><strong>Community</strong> — help, events, and coordinated play</li></ul>
<h2>How to Find a Squadron</h2>
<p>Squadron tab in hangar → Browse Squadrons → filter by language, playstyle, activity. Look for 100+ members and activity within 7 days.</p>
<h2>Creating Your Own</h2>
<p>Costs 1,000 GE (~$4). Need 3+ active members to begin vehicle research. Minimum viable squad: 10 active players doing weekly tasks.</p>
<p><a href="{AFF_URL}" rel="nofollow sponsored">Download War Thunder free</a>.</p>"""},
    {"slug":"war-thunder-steam-deck-guide","title":f"War Thunder on Steam Deck {YEAR} — Performance Guide","date":"2026-05-25","desc":f"How to play War Thunder on Steam Deck {YEAR}. Settings, performance, controls, and tips.","body":f"""<p>War Thunder runs on Steam Deck via Proton in {YEAR}. Here's what to expect.</p>
<div class="tbl-wrap"><table class="compare-table"><tr><th>Settings Preset</th><th>FPS</th><th>Battery Life</th><th>Use Case</th></tr>
<tr><td>Low</td><td>60+ fps</td><td>~90 min</td><td>Arcade Battles</td></tr>
<tr><td>Medium</td><td>40–55 fps</td><td>~75 min</td><td class="winner">Best balance</td></tr>
<tr><td>High</td><td>25–35 fps</td><td>~55 min</td><td>Docked only</td></tr></table></div>
<h2>Recommended Settings</h2>
<p>Resolution: 1280×800 native. Shadows: Low. TDP Limit: 12W. Frame rate: 40fps (matches 40Hz mode). Enable gyro aiming for aircraft — set Gyro to Mouse at sensitivity 2–3 in Steam Deck settings. Use Steam version only — the Gaijin standalone launcher does not work on Deck.</p>
<p><a href="{AFF_URL}" rel="nofollow sponsored">Download War Thunder free on Steam</a>.</p>"""},
]


# ── CSS ───────────────────────────────────────────────────────────────────────
CSS = """*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}:root{--p:#4a7c59;--a:#d4a017;--dk:#1a1a1a;--tx:#222;--mu:#555;--bg:#f8f8f5;--wh:#fff;--r:8px;--sh:0 2px 12px rgba(0,0,0,.1)}@media(prefers-color-scheme:dark){:root{--bg:#111;--wh:#1c1c1c;--tx:#e8e8e8;--mu:#aaa;--sh:0 2px 12px rgba(0,0,0,.4)}}html{scroll-behavior:smooth}body{font-family:'Open Sans',sans-serif;background:var(--bg);color:var(--tx);line-height:1.7}a{color:var(--p);text-decoration:none}a:hover{text-decoration:underline}.skip{position:absolute;transform:translateY(-100%);background:var(--a);color:var(--dk);padding:8px 16px;border-radius:0 0 var(--r) var(--r);font-weight:700;transition:transform .2s;z-index:999}.skip:focus{transform:translateY(0)}.container{max-width:1100px;margin:0 auto;padding:0 20px}.nav{background:var(--dk);position:sticky;top:0;z-index:99;box-shadow:var(--sh)}.nav-i{display:flex;align-items:center;justify-content:space-between;height:60px}.logo{color:#fff;font-family:'Oswald',sans-serif;font-size:1.4rem;font-weight:700;display:flex;align-items:center;gap:8px}.logo span{color:var(--a)}.lm{background:var(--a);color:var(--dk);width:28px;height:28px;border-radius:4px;display:grid;place-items:center;font-size:.9rem}.nav-l{display:flex;align-items:center;gap:16px}.nav-l a{color:#ccc;font-size:.9rem;transition:color .2s}.nav-l a:hover{color:#fff;text-decoration:none}.ncta{background:var(--a)!important;color:var(--dk)!important;padding:6px 14px;border-radius:var(--r);font-weight:700;font-size:.85rem!important}.ncta:hover{opacity:.9;text-decoration:none!important}.hbg{display:none;flex-direction:column;gap:5px;cursor:pointer;padding:8px;background:none;border:none}.hbg span{display:block;width:22px;height:2px;background:#ccc}.mob-nav{display:none;position:absolute;top:60px;left:0;right:0;background:var(--dk);padding:16px 20px;flex-direction:column;gap:12px;z-index:98}.mob-nav.open{display:flex}.mob-nav a{color:#ccc;font-size:1rem}.hero{background:linear-gradient(135deg,#1a2a1a 0%,#2d4a2d 60%,#1a3a1a 100%);color:#fff;padding:80px 20px;text-align:center;position:relative;overflow:hidden}.hero::before{content:'';position:absolute;inset:0;background:url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none'%3E%3Cg fill='%23fff' fill-opacity='.03'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")}.htag{background:var(--a);color:var(--dk);font-size:.75rem;font-weight:700;padding:4px 12px;border-radius:20px;display:inline-block;margin-bottom:16px;letter-spacing:.05em;text-transform:uppercase}.hero h1{font-family:'Oswald',sans-serif;font-size:clamp(2rem,6vw,3.5rem);font-weight:700;line-height:1.1;margin-bottom:8px}.hero h1 span{color:var(--a)}.hsub{font-size:1.1rem;max-width:600px;margin:16px auto 32px;opacity:.9}.hbtns{display:flex;gap:12px;justify-content:center;flex-wrap:wrap}.btn{background:var(--a);color:var(--dk);padding:14px 32px;border-radius:var(--r);font-weight:700;font-size:1rem;transition:transform .2s,opacity .2s;display:inline-block}.btn:hover{transform:translateY(-2px);opacity:.9;text-decoration:none}.btn2{background:transparent;color:#fff;border:2px solid rgba(255,255,255,.4);padding:12px 28px;border-radius:var(--r);font-weight:600;transition:border-color .2s}.btn2:hover{border-color:#fff;text-decoration:none}.sbar{display:flex;gap:32px;justify-content:center;flex-wrap:wrap;margin-top:48px;padding-top:32px;border-top:1px solid rgba(255,255,255,.15)}.stat{text-align:center}.sn{font-family:'Oswald',sans-serif;font-size:2rem;font-weight:700;color:var(--a)}.sl{font-size:.8rem;opacity:.7;text-transform:uppercase;letter-spacing:.05em}.sec{padding:64px 0}.sec-alt{background:var(--wh)}.stit{font-family:'Oswald',sans-serif;font-size:clamp(1.5rem,4vw,2.2rem);font-weight:700;text-align:center;margin-bottom:8px}.ssub{text-align:center;color:var(--mu);margin-bottom:48px;max-width:560px;margin-left:auto;margin-right:auto}.wg{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:24px}.wc{background:var(--wh);border-radius:var(--r);padding:28px;box-shadow:var(--sh);border-left:4px solid var(--p)}.wc h3{font-family:'Oswald',sans-serif;font-size:1.1rem;margin-bottom:8px}.wc p{font-size:.9rem;color:var(--mu)}.compare-table{width:100%;border-collapse:collapse;font-size:.9rem}.compare-table th{background:var(--dk);color:#fff;padding:12px 16px;text-align:left;font-family:'Oswald',sans-serif;font-size:1rem}.compare-table th:first-child{background:var(--p)}.compare-table td{padding:11px 16px;border-bottom:1px solid #e8e8e8}.compare-table tr:nth-child(even) td{background:#f5f5f2}.winner{color:var(--p);font-weight:700}.loser{color:#999}.tbl-wrap{overflow-x:auto}.faq{max-width:760px;margin:0 auto}.fi{border-bottom:1px solid #e8e8e8}.fq{width:100%;background:none;border:none;text-align:left;padding:20px 40px 20px 0;font-weight:700;font-size:1rem;color:var(--tx);cursor:pointer;position:relative;font-family:'Open Sans',sans-serif}.fq::after{content:'＋';position:absolute;right:0;top:50%;transform:translateY(-50%);font-size:1.2rem;color:var(--p);transition:.2s}.fq.open::after{transform:translateY(-50%) rotate(45deg)}.fb{max-height:0;overflow:hidden;transition:max-height .3s ease}.fb.open{max-height:200px}.fb p{padding-bottom:16px;color:var(--mu);font-size:.95rem}.bg{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:24px}.bc{background:var(--wh);border-radius:var(--r);box-shadow:var(--sh);overflow:hidden;transition:transform .2s}.bc:hover{transform:translateY(-4px)}.bcb{padding:20px}.bcb h3{font-family:'Oswald',sans-serif;font-size:1.1rem;margin-bottom:8px}.bcb p{font-size:.85rem;color:var(--mu);margin-bottom:12px}.bcb a{font-weight:700;font-size:.85rem}.kh{background:linear-gradient(135deg,#1a2a1a,#2d4a2d);color:#fff;padding:56px 20px;text-align:center}.kh h1{font-family:'Oswald',sans-serif;font-size:clamp(1.6rem,5vw,2.8rem);font-weight:700;margin-bottom:12px}.kh p{opacity:.85;max-width:560px;margin:0 auto 24px}.rrow{display:flex;gap:24px;justify-content:center;flex-wrap:wrap;margin:32px 0}.rb{text-align:center;background:rgba(255,255,255,.08);padding:16px 20px;border-radius:var(--r)}.rb .sc{font-family:'Oswald',sans-serif;font-size:2rem;color:var(--a);font-weight:700}.rb .lb{font-size:.75rem;opacity:.7;text-transform:uppercase;letter-spacing:.05em}.kb{max-width:780px;margin:0 auto;padding:48px 20px}.kb h2{font-family:'Oswald',sans-serif;font-size:1.4rem;margin:32px 0 12px}.kb p{margin-bottom:16px;color:var(--mu)}.kb ul,.kb ol{padding-left:20px;margin-bottom:16px;color:var(--mu)}.kb li{margin-bottom:6px}.kb strong{color:var(--tx)}.kb code{background:#f0f0f0;padding:2px 6px;border-radius:4px;font-family:monospace}.kcta{background:linear-gradient(135deg,var(--p),#2d5a3d);color:#fff;text-align:center;padding:40px 24px;border-radius:12px;margin:40px 0}.kcta h3{font-family:'Oswald',sans-serif;font-size:1.5rem;margin-bottom:8px}.kcta p{opacity:.85;margin-bottom:20px}.rl{display:flex;flex-wrap:wrap;gap:10px;margin-top:12px}.rl a{background:var(--wh);border:1px solid #ddd;padding:6px 14px;border-radius:20px;font-size:.8rem;color:var(--p);transition:background .2s}.rl a:hover{background:var(--p);color:#fff;text-decoration:none}.bc2{font-size:.8rem;color:var(--mu);margin-bottom:8px}.bc2 a{color:var(--mu)}.bc2 a:hover{color:var(--p)}.ph{background:linear-gradient(135deg,#1a2a1a,#2d4a2d);color:#fff;padding:56px 20px;text-align:center}.ph h1{font-family:'Oswald',sans-serif;font-size:clamp(1.5rem,4vw,2.4rem);font-weight:700;max-width:760px;margin:0 auto 12px}.pb{max-width:780px;margin:48px auto;padding:0 20px}.pb h2{font-family:'Oswald',sans-serif;font-size:1.5rem;margin:32px 0 12px}.pb h3{font-size:1.1rem;font-weight:700;margin:24px 0 8px}.pb p{margin-bottom:16px;color:var(--mu)}.pb ul,.pb ol{padding-left:20px;margin-bottom:16px;color:var(--mu)}.pb li{margin-bottom:6px}.pb strong{color:var(--tx)}.pb code{background:#f0f0f0;padding:2px 6px;border-radius:4px;font-family:monospace}.rsc{display:flex;gap:24px;flex-wrap:wrap;justify-content:center;margin:32px 0}.rsc .sc2{text-align:center;background:var(--wh);border-radius:var(--r);padding:20px;box-shadow:var(--sh);min-width:120px}.rsc .sc2 .sco{font-family:'Oswald',sans-serif;font-size:2.2rem;color:var(--p);font-weight:700}.rsc .sc2 .slb{font-size:.75rem;color:var(--mu);text-transform:uppercase}.ft{background:var(--dk);color:#999;padding:40px 0}.fti{display:flex;flex-direction:column;gap:16px;align-items:center;text-align:center}.fdisc{font-size:.78rem;max-width:700px;line-height:1.6}.flinks{display:flex;flex-wrap:wrap;gap:12px;justify-content:center}.flinks a{color:#666;font-size:.82rem}.flinks a:hover{color:#ccc;text-decoration:none}.sticky{display:none;position:fixed;bottom:0;left:0;right:0;background:var(--dk);padding:12px 20px;z-index:90;box-shadow:0 -2px 12px rgba(0,0,0,.3)}.sticky-in{max-width:600px;margin:0 auto;display:flex;align-items:center;justify-content:space-between;gap:12px}.sticky-t{color:#ccc;font-size:.85rem;flex:1}.sticky-b{background:var(--a);color:var(--dk);padding:8px 20px;border-radius:var(--r);font-weight:700;font-size:.85rem;white-space:nowrap}.sticky-b:hover{opacity:.9;text-decoration:none}.hero::before{pointer-events:none}@media(max-width:768px){.sbar{gap:20px}.nav-l a:not(.ncta){display:none}.hbg{display:flex}.hbtns{flex-direction:column;align-items:center}.sticky{display:block}}"""

JS = """<script>
document.querySelectorAll('.fq').forEach(b=>{
  b.addEventListener('click',()=>{
    const bd=b.nextElementSibling,op=b.classList.contains('open');
    document.querySelectorAll('.fq').forEach(x=>{x.classList.remove('open');x.nextElementSibling.classList.remove('open');});
    if(!op){b.classList.add('open');bd.classList.add('open');}
  });
});
document.querySelector('.hbg')?.addEventListener('click',()=>{
  document.querySelector('.mob-nav')?.classList.toggle('open');
});
</script>"""

# ── HELPERS ───────────────────────────────────────────────────────────────────
def pu(lang, path=""):
    base = f"{SITE_URL}/{lang}" if lang != "en" else SITE_URL
    return f"{base}/{path}" if path else f"{base}/"

def hreflang(path=""):
    tags = [f'<link rel="alternate" hreflang="{lc}" href="{pu(lc,path)}"/>' for lc in LANGUAGES]
    tags.append(f'<link rel="alternate" hreflang="x-default" href="{pu("en",path)}"/>')
    return "\n".join(tags)

def nav_html(lang,t):
    return (f'<a href="{pu(lang)}">{t["nav_home"]}</a>'
            f'<a href="{pu(lang,"review/")}">{t["nav_review"]}</a>'
            f'<a href="{pu(lang,"compare/")}">{t["nav_compare"]}</a>'
            f'<a href="{pu(lang,"blog/")}">{t["nav_blog"]}</a>')

def sitenav_ld(lang,t):
    sc=[{"@type":"SiteNavigationElement","name":t["nav_home"],"url":pu(lang)},
        {"@type":"SiteNavigationElement","name":t["nav_review"],"url":pu(lang,"review/")},
        {"@type":"SiteNavigationElement","name":t["nav_compare"],"url":pu(lang,"compare/")},
        {"@type":"SiteNavigationElement","name":t["nav_blog"],"url":pu(lang,"blog/")}]
    return f'<script type="application/ld+json">{json.dumps({"@context":"https://schema.org","@graph":sc})}</script>'

def shell(lang,title,meta,canonical,body,schema=""):
    t=LANGUAGES[lang]
    nh=nav_html(lang,t)
    return f"""<!DOCTYPE html>
<html lang="{lang}" dir="{t['dir']}">
<head>
<meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>{title} — {SITE_NAME}</title>
<meta name="description" content="{meta}"/>
<link rel="canonical" href="{canonical}"/>
<meta property="og:title" content="{title}"/>
<meta property="og:description" content="{meta}"/>
<meta property="og:url" content="{canonical}"/>
<meta property="og:type" content="website"/>
<meta name="twitter:card" content="summary_large_image"/>
<meta name="robots" content="index,follow"/>
{hreflang()}
<link rel="dns-prefetch" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link href="https://fonts.googleapis.com/css2?family=Oswald:wght@600;700&family=Open+Sans:wght@400;600&display=swap" rel="stylesheet"/>
<style>{CSS}</style>
{schema}{sitenav_ld(lang,t)}
</head>
<body>
<a href="#main" class="skip">{t['skip']}</a>
<nav class="nav"><div class="container nav-i">
  <a href="{pu(lang)}" class="logo"><div class="lm">⚡</div>War<span>Thunder</span></a>
  <div class="nav-l">{nh}<a href="{AFF_URL}" class="ncta" target="_blank" rel="nofollow sponsored">{t['cta']}</a></div>
  <button class="hbg" aria-label="Menu"><span></span><span></span><span></span></button>
</div><div class="mob-nav">{nh}<a href="{AFF_URL}" class="ncta" target="_blank" rel="nofollow sponsored">{t['cta']}</a></div></nav>
<main id="main">{body}</main>
<footer class="ft"><div class="container fti">
  <p class="fdisc">{t['disc']}</p>
  <div class="flinks"><a href="{pu(lang)}">Home</a><a href="{pu(lang,'review/')}">Review</a><a href="{pu(lang,'compare/')}">Compare</a><a href="{pu(lang,'blog/')}">Blog</a><a href="{pu('en','privacy/')}">Privacy</a><a href="{pu('en','terms/')}">Terms</a></div>
  <p style="font-size:.72rem;color:#444">© {YEAR} {SITE_NAME}. Built {TODAY}.</p>
</div></footer>
<div class="sticky"><div class="sticky-in"><span class="sticky-t">{t['sticky_cta']}</span><a href="{AFF_URL}" class="sticky-b" target="_blank" rel="nofollow sponsored">{t['cta']} →</a></div></div>
{JS}
</body></html>"""

def faq_ld(qas):
    sc={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in qas]}
    return f'<script type="application/ld+json">{json.dumps(sc)}</script>'

def bc_ld(items):
    sc={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":i+1,"name":n,"item":u} for i,(n,u) in enumerate(items)]}
    return f'<script type="application/ld+json">{json.dumps(sc)}</script>'

def art_ld(title,desc,date,url):
    sc={"@context":"https://schema.org","@type":"Article","headline":title,"description":desc,"datePublished":date,"dateModified":TODAY,"url":url,"publisher":{"@type":"Organization","name":SITE_NAME}}
    return f'<script type="application/ld+json">{json.dumps(sc)}</script>'

def game_ld():
    sc={"@context":"https://schema.org","@type":"VideoGame","name":"War Thunder","description":"Free-to-play military MMO with 2,000+ aircraft, tanks, and ships.","genre":["Military","Simulation"],"gamePlatform":["PC","PlayStation 4","PlayStation 5","Xbox One","Xbox Series X"],"offers":{"@type":"Offer","price":"0","priceCurrency":"USD"},"url":AFF_URL}
    return f'<script type="application/ld+json">{json.dumps(sc)}</script>'

def write(path,content):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(content,encoding="utf-8")

# ── CATEGORY COPY ─────────────────────────────────────────────────────────────
def cat_copy(slug,title,cat,y):
    if cat=="free":
        return f"""<h2>Best Free War Games in {y}</h2>
<p>Not all free-to-play war games are genuine. The best ones offer full content without a paywall — all maps, all modes, all vehicles earnable without spending money. War Thunder meets every criterion.</p>
<div class="tbl-wrap"><table class="compare-table"><tr><th>Game</th><th>Price</th><th>Vehicles</th><th>Branches</th><th>Platforms</th></tr>
<tr><td><strong>War Thunder</strong></td><td class="winner">Free</td><td class="winner">2,000+</td><td class="winner">Air+Ground+Naval</td><td class="winner">PC/PS/Xbox</td></tr>
<tr><td>World of Tanks</td><td class="winner">Free</td><td>600+</td><td class="loser">Tanks only</td><td>PC/Console</td></tr>
<tr><td>Crossout</td><td class="winner">Free</td><td>Custom</td><td class="loser">Ground only</td><td>PC/PS/Xbox</td></tr>
</table></div>
<h2>How to Start Playing Free</h2>
<ol style="padding-left:20px;color:var(--mu);margin-bottom:16px">
<li style="margin-bottom:8px">Click the download button above</li>
<li style="margin-bottom:8px">Create a free Gaijin account (60 seconds)</li>
<li style="margin-bottom:8px">Choose USA as your first nation</li>
<li style="margin-bottom:8px">Complete the tutorial — about 10 minutes</li>
<li style="margin-bottom:8px">Queue for your first Arcade Battle</li>
</ol>"""
    elif cat=="best":
        return f"""<h2>Rankings: Best Free War Games in {y}</h2>
<div class="tbl-wrap"><table class="compare-table"><tr><th>Game</th><th>Price</th><th>Content</th><th>F2P Fair?</th><th>Score</th></tr>
<tr><td><strong>War Thunder</strong></td><td class="winner">Free</td><td class="winner">2,000+ vehicles</td><td class="winner">Yes</td><td class="winner">9.4/10</td></tr>
<tr><td>World of Tanks</td><td class="winner">Free</td><td>600+ tanks</td><td>Mostly</td><td>7.8/10</td></tr>
<tr><td>Enlisted</td><td class="winner">Free</td><td>Infantry+vehicles</td><td>Yes</td><td>7.5/10</td></tr>
<tr><td>Crossout</td><td class="winner">Free</td><td>Custom vehicles</td><td>Mostly</td><td>7.2/10</td></tr>
</table></div>
<h2>Why War Thunder Wins in {y}</h2>
<p>War Thunder is the only free game that covers air, ground, and naval combat historically across all platforms with real simulation physics. No other free game comes close to its content breadth or update cadence.</p>"""
    elif cat=="similar":
        return f"""<h2>War Thunder Alternatives in {y}</h2>
<div class="tbl-wrap"><table class="compare-table"><tr><th>Game</th><th>Free</th><th>Vehicle Focus</th><th>Realism</th></tr>
<tr><td>World of Tanks</td><td class="winner">Yes</td><td>Tanks only</td><td>Arcade HP</td></tr>
<tr><td>Crossout</td><td class="winner">Yes</td><td>Custom vehicles</td><td>Arcade</td></tr>
<tr><td>Enlisted</td><td class="winner">Yes</td><td>Vehicles + infantry</td><td>Semi-realistic</td></tr>
<tr><td>IL-2 Sturmovik</td><td class="loser">Paid</td><td>Aircraft only</td><td class="winner">Hardcore sim</td></tr>
</table></div>
<h2>Why Players Return to War Thunder</h2>
<p>Every alternative covers a subset of what War Thunder does. WoT is tanks-only. IL-2 is aircraft-only. Crossout is custom vehicles. War Thunder is the only free game that covers all three historically, on all platforms. Once you've tried alternatives, the breadth pulls you back.</p>"""
    elif cat=="wt":
        return f"""<h2>The Honest Answer for {y}</h2>
<p>War Thunder's free-to-play model is among the fairest in the genre. Every vehicle is obtainable without payment. The free experience includes all modes, all maps, and all tech trees.</p>
<div class="tbl-wrap"><table class="compare-table"><tr><th>Content</th><th>Free?</th></tr>
<tr><td>Full vehicle tech trees (all nations)</td><td class="winner">✅ Yes</td></tr>
<tr><td>All game modes (Arcade/Realistic/Simulator)</td><td class="winner">✅ Yes</td></tr>
<tr><td>All maps (100+)</td><td class="winner">✅ Yes</td></tr>
<tr><td>Events with earnable premium vehicles</td><td class="winner">✅ Yes</td></tr>
<tr><td>Premium account (×2 RP/SL)</td><td class="loser">❌ Paid</td></tr>
<tr><td>Premium vehicles (skip grind)</td><td class="loser">❌ Paid</td></tr>
</table></div>"""
    elif cat=="vs":
        return f"""<h2>Side-by-Side Comparison</h2>
<div class="tbl-wrap"><table class="compare-table"><tr><th>Feature</th><th>War Thunder</th><th>Competitor</th></tr>
<tr><td>Price</td><td class="winner">Free</td><td>Free / Paid</td></tr>
<tr><td>Vehicle Types</td><td class="winner">Air + Ground + Naval</td><td>Varies</td></tr>
<tr><td>Physics</td><td class="winner">Simulation ballistics</td><td>Arcade / HP system</td></tr>
<tr><td>Platforms + Crossplay</td><td class="winner">PC/PS/Xbox + Yes</td><td>Varies</td></tr>
<tr><td>Active Players</td><td class="winner">100M+ registered</td><td>Smaller</td></tr>
<tr><td>Update Cadence</td><td class="winner">4–6 major/year</td><td>Varies</td></tr>
</table></div>
<h2>Verdict for {y}</h2>
<p>For most content at zero cost across the most platforms: War Thunder wins. Both games are free — try War Thunder first and decide.</p>"""
    elif cat=="geo":
        geo = GEO_DETAILS.get(slug,{})
        if geo:
            stores = ", ".join(geo["stores"])
            return f"""<h2>War Thunder in {geo['country']} — {y}</h2>
<div class="tbl-wrap"><table class="compare-table"><tr><th>Detail</th><th>Info</th></tr>
<tr><td>Currency</td><td>{geo['currency']}</td></tr>
<tr><td>Nearest Server</td><td>{geo['cluster']}</td></tr>
<tr><td>Expected Ping</td><td class="winner">{geo['ping']}</td></tr>
<tr><td>Download Stores</td><td>{stores}</td></tr>
<tr><td>Subscription Required</td><td class="winner">None — 100% free</td></tr>
</table></div>
<p>{geo.get('extra','')}</p>
<h2>How to Download in {geo['country']}</h2>
<p><strong>PC:</strong> Steam or Gaijin.net — search "War Thunder" → Free download (~50GB).<br>
<strong>PlayStation:</strong> Open the PlayStation Store → Search "War Thunder" → Download (Free).<br>
<strong>Xbox:</strong> Open Microsoft Store → Search "War Thunder" → Get (Free).</p>"""
        return f"""<h2>Playing War Thunder in Your Region</h2>
<p>War Thunder is fully available and supported in your country in {y}. Download from Steam, PlayStation Store, or Microsoft Store — all free.</p>"""
    elif cat=="intent":
        return f"""<h2>How to Start Playing War Thunder in {y}</h2>
<ol style="padding-left:20px;color:var(--mu);margin-bottom:16px">
<li style="margin-bottom:8px">Click the download button above and choose your platform</li>
<li style="margin-bottom:8px">Create a free Gaijin account — email + password, under 60 seconds</li>
<li style="margin-bottom:8px">Download the game — 40–60 GB depending on platform</li>
<li style="margin-bottom:8px">Choose your nation — USA recommended for beginners</li>
<li style="margin-bottom:8px">Complete the 10-minute tutorial</li>
<li style="margin-bottom:8px">Queue for your first Arcade Battle</li>
</ol>
<h2>No Credit Card Required</h2>
<p>War Thunder never asks for payment to download or play. The free version is the full game — all modes, all maps, all nations.</p>"""
    elif cat=="steam":
        return f"""<h2>War Thunder on Steam in {y}</h2>
<p>War Thunder is a permanent free download on Steam with a "Very Positive" rating from 200,000+ reviews — one of the top-rated free games on the platform.</p>
<div class="tbl-wrap"><table class="compare-table"><tr><th>Spec</th><th>Minimum</th><th>Recommended</th></tr>
<tr><td>OS</td><td>Windows 7 64-bit</td><td>Windows 10/11</td></tr>
<tr><td>CPU</td><td>Intel i5</td><td>Intel i7</td></tr>
<tr><td>RAM</td><td>8 GB</td><td>16 GB</td></tr>
<tr><td>GPU</td><td>GTX 660</td><td>RTX 2070</td></tr>
<tr><td>Storage</td><td>40 GB HDD</td><td>40 GB SSD</td></tr>
</table></div>
<p>Search "War Thunder" in Steam → Click "Play Game" (free) → Download installs → Launch and create your Gaijin account.</p>"""
    elif cat=="console":
        return f"""<h2>War Thunder on Console — {y}</h2>
<p>War Thunder is 100% free on PS4, PS5, Xbox One, and Xbox Series X|S. No PS Plus. No Game Pass. Just download and play.</p>
<div class="tbl-wrap"><table class="compare-table"><tr><th>Platform</th><th>FPS</th><th>Resolution</th><th>Load Times</th></tr>
<tr><td>PS4 / Xbox One</td><td>30fps</td><td>1080p</td><td>Slow (HDD)</td></tr>
<tr><td>PS5 / Xbox Series X</td><td class="winner">60fps</td><td class="winner">4K upscale</td><td class="winner">Fast (SSD)</td></tr>
</table></div>
<p>Your Gaijin account syncs across all platforms — vehicles, SL, and RP carry over when you switch.</p>"""
    elif cat=="hist":
        return f"""<h2>War Thunder's Historical Coverage in {y}</h2>
<div class="tbl-wrap"><table class="compare-table"><tr><th>Era</th><th>Years</th><th>Iconic Vehicles</th></tr>
<tr><td>Interwar</td><td>1930–1939</td><td>Biplanes, early tanks</td></tr>
<tr><td>WW2</td><td>1939–1945</td><td>Tiger I, Spitfire, T-34, B-17</td></tr>
<tr><td>Early Cold War</td><td>1945–1960</td><td>F-86 Sabre, MiG-15, M48 Patton</td></tr>
<tr><td>Cold War</td><td>1960–1980</td><td>F-4 Phantom, MiG-21, Leopard 1</td></tr>
<tr><td>Modern</td><td>1980–present</td><td>F-16C, Leopard 2A7V, T-90M</td></tr>
</table></div>
<p>Gaijin builds vehicles from declassified blueprints. The community actively submits historical documents to correct vehicle stats — the most community-verified military game in existence.</p>"""
    elif cat=="cross":
        return f"""<h2>Gaijin's Free Game Ecosystem in {y}</h2>
<div class="tbl-wrap"><table class="compare-table"><tr><th>Game</th><th>Best For</th><th>Setting</th><th>Vehicles</th></tr>
<tr><td><strong>War Thunder</strong></td><td>Historical sim</td><td>WW2–Modern</td><td>Real historical</td></tr>
<tr><td>Crossout</td><td>Vehicle builder</td><td>Post-apocalyptic</td><td>Custom-built</td></tr>
<tr><td>Enlisted</td><td>Infantry + vehicles</td><td>WW2</td><td>Real + infantry</td></tr>
</table></div>
<p>One Gaijin account works across all three games. All are free — try them all.</p>"""
    elif cat=="value":
        return f"""<h2>The Real Cost of War Thunder in {y}</h2>
<div class="tbl-wrap"><table class="compare-table"><tr><th>Goal</th><th>Free (time)</th><th>With Premium</th></tr>
<tr><td>Rank I → III</td><td>10–20 hours</td><td>5–10 hours</td></tr>
<tr><td>Rank III → V</td><td>40–80 hours</td><td>20–40 hours</td></tr>
<tr><td>Rank V → VII</td><td>100–200 hours</td><td>50–100 hours</td></tr>
<tr><td>Top Tier</td><td>200–400 hours</td><td>100–200 hours</td></tr>
</table></div>
<p>Every gate in War Thunder is time, not money. Premium halves the time but is never required. Most players never spend money and still get 500+ hours of enjoyment.</p>"""
    elif cat=="tech":
        return f"""<h2>Technical Specifications — War Thunder {y}</h2>
<div class="tbl-wrap"><table class="compare-table"><tr><th>Spec</th><th>Minimum</th><th>Recommended</th><th>4K Ultra</th></tr>
<tr><td>CPU</td><td>i5-4460</td><td>i7-9700K</td><td>i9-12900K</td></tr>
<tr><td>RAM</td><td>8 GB</td><td>16 GB</td><td>32 GB</td></tr>
<tr><td>GPU</td><td>GTX 660</td><td>RTX 2070</td><td>RTX 3080+</td></tr>
<tr><td>Storage</td><td>40 GB HDD</td><td>40 GB SSD</td><td>40 GB NVMe</td></tr>
</table></div>
<h2>Top Performance Tips</h2>
<ul><li>Use DirectX 12 on modern GPUs — ~20% FPS gain</li><li>Set Shadows to Low first — biggest single improvement</li><li>Enable DLSS (Nvidia) or FSR (AMD)</li><li>Install on SSD — load times drop from 45s to under 10s</li></ul>"""
    elif cat=="nation":
        nd = NATION_TABLES.get(slug)
        if nd:
            rows = "".join(f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td></tr>" for r in nd["rows"])
            return f"""<h2>Vehicle Progression</h2>
<p>{nd['intro']}</p>
<div class="tbl-wrap"><table class="compare-table">
<tr><th>Vehicle</th><th>BR</th><th>Type</th><th>Why Play It</th></tr>
{rows}
</table></div>"""
        return f"""<h2>Nation Guide</h2><p>War Thunder has 12+ nations each with unique vehicle trees and playstyles. See our full nation guides for detailed tech tree breakdowns.</p>"""
    else:  # misc
        return f"""<h2>War Thunder Community & Meta in {y}</h2>
<div class="tbl-wrap"><table class="compare-table"><tr><th>Resource</th><th>Best For</th></tr>
<tr><td>r/Warthunder</td><td class="winner">Discussion, memes, tips</td></tr>
<tr><td>Official Forums</td><td>Bug reports, vehicle suggestions</td></tr>
<tr><td>War Thunder Wiki</td><td>Vehicle stats and weakspots</td></tr>
<tr><td>Dev Blog (official site)</td><td>Upcoming content previews</td></tr>
</table></div>
<p>The Dev Blog reveals upcoming vehicles 2–3 weeks before each major patch — follow it to stay ahead of the meta.</p>"""


# ── PAGE BUILDERS ─────────────────────────────────────────────────────────────
def build_homepage(lang):
    t=LANGUAGES[lang]; y=YEAR
    why_cards="".join(f'<div class="wc"><h3>{h}</h3><p>{d}</p></div>' for item in t["why"] for h,d in [item.split("|")])
    faq_items="".join(f'<div class="fi"><button class="fq">{q}</button><div class="fb"><p>{a}</p></div></div>' for q,a in t["faq_qs"])
    blog_cards="".join(f'<div class="bc"><div class="bcb"><h3>{p["title"]}</h3><p>{p["desc"][:100]}...</p><a href="{pu(lang,"blog/"+p["slug"]+"/")}">Read more →</a></div></div>' for p in BLOG_POSTS[:3])
    body=f"""
<div class="hero"><div class="container">
  <div class="htag">Free to Play — {y}</div>
  <h1>{t['hero1']}<br><span>{t['hero2']}</span></h1>
  <p class="hsub">{t['hero_sub']}</p>
  <div class="hbtns">
    <a href="{AFF_URL}" class="btn" target="_blank" rel="nofollow sponsored">{t['cta']}</a>
    <a href="{pu(lang,'review/')}" class="btn2">Read Review</a>
  </div>
  <div class="sbar">
    <div class="stat"><div class="sn">2,000+</div><div class="sl">Vehicles</div></div>
    <div class="stat"><div class="sn">100M+</div><div class="sl">Players</div></div>
    <div class="stat"><div class="sn">100+</div><div class="sl">Maps</div></div>
    <div class="stat"><div class="sn">12+</div><div class="sl">Nations</div></div>
    <div class="stat"><div class="sn">100%</div><div class="sl">Free</div></div>
  </div>
</div></div>
<section class="sec sec-alt"><div class="container">
  <h2 class="stit">{t['feat_title']}</h2>
  <p class="ssub">Why War Thunder has 100M+ registered players in {y}.</p>
  <div class="wg">{why_cards}</div>
</div></section>
<section class="sec"><div class="container">
  <h2 class="stit">War Thunder vs The Competition</h2>
  <p class="ssub">How it stacks up against World of Tanks, Crossout, and Enlisted in {y}.</p>
  <div class="tbl-wrap"><table class="compare-table">
  <tr><th>Feature</th><th>War Thunder</th><th>World of Tanks</th><th>Crossout</th><th>Enlisted</th></tr>
  <tr><td>Price</td><td class="winner">Free</td><td class="winner">Free</td><td class="winner">Free</td><td class="winner">Free</td></tr>
  <tr><td>Vehicles</td><td class="winner">2,000+</td><td>600+</td><td>Custom</td><td>Mixed</td></tr>
  <tr><td>Branches</td><td class="winner">Air+Ground+Naval</td><td class="loser">Tanks only</td><td class="loser">Ground</td><td>Ground+Infantry</td></tr>
  <tr><td>Realism</td><td class="winner">Simulation</td><td>Arcade HP</td><td>Arcade</td><td>Semi</td></tr>
  <tr><td>Crossplay</td><td class="winner">Yes</td><td class="loser">No</td><td class="winner">Yes</td><td class="winner">Yes</td></tr>
  </table></div>
</div></section>
<section class="sec sec-alt"><div class="container">
  <h2 class="stit">Frequently Asked Questions</h2>
  <div class="faq">{faq_items}</div>
</div></section>
<section class="sec"><div class="container">
  <h2 class="stit">{t['blog_title']}</h2>
  <p class="ssub">Guides, tips, and news to help you dominate in {y}.</p>
  <div class="bg">{blog_cards}</div>
  <div style="text-align:center;margin-top:32px"><a href="{pu(lang,'blog/')}" class="btn">{t['see_all']} →</a></div>
</div></section>
<div style="background:var(--p);padding:56px 20px;text-align:center;color:white">
  <div class="container">
    <h2 style="font-family:'Oswald',sans-serif;font-size:2.2rem;margin-bottom:8px">Ready to Play for Free?</h2>
    <p style="opacity:.85;margin-bottom:24px;max-width:500px;margin-left:auto;margin-right:auto">100M+ players. No subscription. No hidden fees. Download now.</p>
    <a href="{AFF_URL}" class="btn" style="background:var(--a);color:var(--dk)" target="_blank" rel="nofollow sponsored">{t['dl']} — {SITE_NAME}</a>
  </div>
</div>"""
    schema=game_ld()+faq_ld(t["faq_qs"])+hreflang()
    return shell(lang,f"Best Free Military Game {y}",t["meta_home"],pu(lang),body,schema)

def build_review(lang):
    t=LANGUAGES[lang]; y=YEAR
    body=f"""<div class="ph"><div class="container"><h1>{t['review_title']}</h1><p style="opacity:.8">Updated: {TODAY}</p></div></div>
<div class="pb">
<div class="rsc">
  <div class="sc2"><div class="sco">9.4</div><div class="slb">Overall</div></div>
  <div class="sc2"><div class="sco">10</div><div class="slb">Value</div></div>
  <div class="sc2"><div class="sco">9.5</div><div class="slb">Content</div></div>
  <div class="sc2"><div class="sco">9.2</div><div class="slb">Realism</div></div>
  <div class="sc2"><div class="sco">9.0</div><div class="slb">Community</div></div>
  <div class="sc2"><div class="sco">8.8</div><div class="slb">Economy</div></div>
</div>
<h2>Overview</h2>
<p>War Thunder is a free-to-play military MMO by Gaijin Entertainment. Since 2012 it has grown into the world's largest vehicle combat game — 2,000+ historically accurate vehicles, 100+ maps, 100M+ registered accounts.</p>
<h2>Gameplay</h2>
<p>Three modes: <strong>Arcade Battles</strong> (lead indicators, beginner-friendly), <strong>Realistic Battles</strong> (full simulation physics — the main competitive mode), and <strong>Simulator Battles</strong> (full cockpit, no HUD). All are free.</p>
<h2>Free-to-Play Fairness</h2>
<p>Every vehicle is earnable for free. The main criticism is the tech tree grind — 200–500 hours to top tier free, halved with premium. No vehicle is gated behind a hard paywall. Events regularly award free premium vehicles.</p>
<h2>Verdict: 9.4/10 — Exceptional</h2>
<p>For a free game, War Thunder rivals $60 paid alternatives. Essential if you have any interest in military vehicles.</p>
<div style="text-align:center;margin:32px 0"><a href="{AFF_URL}" class="btn" target="_blank" rel="nofollow sponsored">{t['dl']} Free</a></div>
</div>"""
    return shell(lang,t["review_title"],f"Full War Thunder review {y}. Gameplay, economy, verdict.",pu(lang,"review/"),body,art_ld(t["review_title"],f"Full War Thunder review {y}.",TODAY,pu(lang,"review/")))

def build_compare(lang):
    t=LANGUAGES[lang]; y=YEAR
    body=f"""<div class="ph"><div class="container"><h1>{t['compare_title']}</h1><p style="opacity:.8">Updated {TODAY}</p></div></div>
<div class="pb">
<div class="tbl-wrap"><table class="compare-table">
<tr><th>Feature</th><th>War Thunder</th><th>World of Tanks</th><th>Crossout</th></tr>
<tr><td>Price</td><td class="winner">Free</td><td class="winner">Free</td><td class="winner">Free</td></tr>
<tr><td>Vehicles</td><td class="winner">2,000+</td><td>600+</td><td>Custom</td></tr>
<tr><td>Branches</td><td class="winner">Air+Ground+Naval</td><td class="loser">Tanks only</td><td class="loser">Ground only</td></tr>
<tr><td>Physics</td><td class="winner">Simulation ballistics</td><td>HP system</td><td>Arcade</td></tr>
<tr><td>Platforms</td><td class="winner">PC/PS4/PS5/Xbox</td><td>PC/Console</td><td>PC/PS/Xbox</td></tr>
<tr><td>Crossplay</td><td class="winner">Yes</td><td class="loser">No</td><td class="winner">Yes</td></tr>
<tr><td>Naval</td><td class="winner">Yes</td><td class="loser">No</td><td class="loser">No</td></tr>
<tr><td>Air</td><td class="winner">Yes</td><td class="loser">No</td><td class="loser">No</td></tr>
<tr><td>Historical Accuracy</td><td class="winner">Extremely high</td><td>Moderate</td><td class="loser">Fictional</td></tr>
<tr><td>Active Players</td><td class="winner">100M+ registered</td><td>~90M registered</td><td>~10M registered</td></tr>
</table></div>
<h2>Verdict</h2>
<p>All three are worth trying. War Thunder wins on content depth, realism, and combined-arms breadth. WoT wins for casual tank-only play. Crossout wins for creative vehicle building.</p>
<div style="text-align:center;margin:32px 0"><a href="{AFF_URL}" class="btn" target="_blank" rel="nofollow sponsored">Try War Thunder Free</a></div>
</div>"""
    return shell(lang,t["compare_title"],f"War Thunder vs WoT vs Crossout {y}: which free game wins?",pu(lang,"compare/"),body)

def build_blog_index(lang):
    t=LANGUAGES[lang]
    cards="".join(f'<div class="bc"><div class="bcb"><h3><a href="{pu(lang,"blog/"+p["slug"]+"/")}"{" style="}color:inherit{""}">{p["title"]}</a></h3><p>{p["desc"]}</p><a href="{pu(lang,"blog/"+p["slug"]+"/")}">Read more →</a></div></div>' for p in BLOG_POSTS)
    body=f"""<div class="ph"><div class="container"><h1>{t['blog_title']}</h1><p style="opacity:.8">{len(BLOG_POSTS)} guides — updated {TODAY}</p></div></div>
<section class="sec"><div class="container"><div class="bg">{cards}</div></div></section>"""
    return shell(lang,t["blog_title"],f"War Thunder guides and news {YEAR}.",pu(lang,"blog/"),body)

def build_blog_post(lang,post):
    t=LANGUAGES[lang]; url=pu(lang,f"blog/{post['slug']}/")
    body=f"""<div class="ph"><div class="container">
  <p class="bc2" style="color:rgba(255,255,255,.6)"><a href="{pu(lang)}" style="color:rgba(255,255,255,.6)">Home</a> › <a href="{pu(lang,'blog/')}" style="color:rgba(255,255,255,.6)">Blog</a> › {post['title']}</p>
  <h1>{post['title']}</h1><p style="opacity:.7">{post['date']}</p>
</div></div>
<div class="pb">{post['body']}
<div style="text-align:center;margin:32px 0"><a href="{AFF_URL}" class="btn" target="_blank" rel="nofollow sponsored">{t['cta']}</a></div>
</div>"""
    return shell(lang,post["title"],post["desc"],url,body,art_ld(post["title"],post["desc"],post["date"],url)+bc_ld([("Home",pu(lang)),("Blog",pu(lang,"blog/")),(post["title"],url)]))

def build_kw(lang,slug,title_fmt,meta_fmt,cat):
    t=LANGUAGES[lang]; y=YEAR
    title=title_fmt.replace("{y}",y); meta=meta_fmt.replace("{y}",y); url=pu(lang,f"{slug}/")
    copy=cat_copy(slug,title,cat,y)
    related="".join(f'<a href="{pu(lang,s+"/")}">{tf.replace("{y}",y)}</a>' for s,tf,_,c in KEYWORDS if c==cat and s!=slug)[:10*50]
    related_links="".join(f'<a href="{pu(lang,s+"/")}">{tf.replace("{y}",y)}</a>' for s,tf,_,c in KEYWORDS if c==cat and s!=slug)
    faq_qs=[(f"Is {title} available in {y}?",f"Yes — War Thunder is a top option. 100% free on PC, PS4/5, and Xbox."),
            ("Do I need to pay anything?","No. War Thunder is completely free. Optional premium exists but is never required."),
            ("What platforms?","PC (Steam & Gaijin.net), PS4, PS5, Xbox One, Xbox Series X|S with crossplay."),
            ("Is there crossplay?","Yes — full cross-platform play between PC, PlayStation, and Xbox.")]
    body=f"""<div class="kh">
  <p class="bc2"><a href="{pu(lang)}" style="color:rgba(255,255,255,.6)">Home</a> › {title}</p>
  <h1>{title}</h1>
  <p>100% free on PC, PS4/5 & Xbox — no subscription, no paywall.</p>
  <a href="{AFF_URL}" class="btn" target="_blank" rel="nofollow sponsored">{t['cta']}</a>
  <div class="rrow">
    <div class="rb"><div class="sc">9.4</div><div class="lb">Overall</div></div>
    <div class="rb"><div class="sc">10</div><div class="lb">Free Access</div></div>
    <div class="rb"><div class="sc">9.5</div><div class="lb">Content</div></div>
    <div class="rb"><div class="sc">9.2</div><div class="lb">Realism</div></div>
    <div class="rb"><div class="sc">9.0</div><div class="lb">Community</div></div>
  </div>
</div>
<div class="kb">
{copy}
<div class="kcta"><h3>Ready to Play for Free?</h3><p>Join 100M+ players. No subscription needed.</p><a href="{AFF_URL}" class="btn" target="_blank" rel="nofollow sponsored">{t['cta']}</a></div>
<h2>{t['related']}</h2>
<div class="rl">{related_links}</div>
</div>"""
    return shell(lang,title,meta,url,body,bc_ld([("Home",pu(lang)),(title,url)])+faq_ld(faq_qs))

def build_privacy():
    t=LANGUAGES["en"]
    body=f"""<div class="ph"><div class="container"><h1>{t['privacy_title']}</h1><p style="opacity:.7">Updated: {TODAY}</p></div></div>
<div class="pb">
<h2>Information We Collect</h2><p>Standard web server logs only (IP, browser type, pages visited). No tracking cookies beyond site functionality.</p>
<h2>Affiliate Links</h2><p>Links marked rel="nofollow sponsored" are affiliate links to Gaijin Entertainment. We earn a commission when you register via these links at no cost to you.</p>
<h2>Analytics</h2><p>We may use privacy-preserving aggregate analytics. No personally identifiable information is stored.</p>
</div>"""
    return shell("en",t["privacy_title"],"Privacy policy.",pu("en","privacy/"),body)

def build_terms():
    t=LANGUAGES["en"]
    body=f"""<div class="ph"><div class="container"><h1>{t['terms_title']}</h1><p style="opacity:.7">Updated: {TODAY}</p></div></div>
<div class="pb">
<h2>Use of This Site</h2><p>This site provides information about War Thunder by Gaijin Entertainment for informational purposes. We are not affiliated with Gaijin Entertainment.</p>
<h2>Affiliate Disclosure</h2><p>We participate in the Gaijin affiliate program. We earn a commission when you register via our links at no additional cost to you. This is disclosed on every page.</p>
<h2>Limitation of Liability</h2><p>War Thunder® is a trademark of Gaijin Entertainment. We are not liable for decisions made based on this site's content.</p>
</div>"""
    return shell("en",t["terms_title"],"Terms of use.",pu("en","terms/"),body)

def build_404():
    body="""<div style="text-align:center;padding:100px 20px">
  <h1 style="font-family:'Oswald',sans-serif;font-size:5rem;color:var(--p)">404</h1>
  <p style="font-size:1.2rem;margin:16px 0 32px;color:var(--mu)">Page not found. Head back to the front line.</p>
  <a href="/" class="btn">Back to Home</a>
</div>"""
    return shell("en","Page Not Found","Page not found.",f"{SITE_URL}/404.html",body)

# ── SITEMAPS / ROBOTS / LLMS ──────────────────────────────────────────────────
def sitemap_index():
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap><loc>{SITE_URL}/sitemap-main.xml</loc><lastmod>{TODAY}</lastmod></sitemap>
  <sitemap><loc>{SITE_URL}/sitemap-kw.xml</loc><lastmod>{TODAY}</lastmod></sitemap>
  <sitemap><loc>{SITE_URL}/sitemap-blog.xml</loc><lastmod>{TODAY}</lastmod></sitemap>
  <sitemap><loc>{SITE_URL}/sitemap-geo.xml</loc><lastmod>{TODAY}</lastmod></sitemap>
</sitemapindex>"""

def sitemap(urls):
    rows="\n".join(f"  <url><loc>{u}</loc><lastmod>{TODAY}</lastmod><changefreq>weekly</changefreq><priority>{p}</priority></url>" for u,p in urls)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{rows}\n</urlset>'

def robots():
    return f"""User-agent: *\nAllow: /\nCrawl-delay: 0\nUser-agent: GPTBot\nAllow: /\nUser-agent: ClaudeBot\nAllow: /\nUser-agent: anthropic-ai\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n"""

def llms_txt(count):
    blog_lines="\n".join(f"- [{p['title']}]({pu('en','blog/'+p['slug']+'/')})" for p in BLOG_POSTS)
    kw_lines="\n".join(f"- [{s}]({pu('en',s+'/')})" for s,*_ in KEYWORDS[:40])
    langs_lines="\n".join(f"- {lc} ({d['name']}): {pu(lc)}" for lc,d in LANGUAGES.items())
    return f"""# {SITE_NAME}

> War Thunder affiliate guide site. Helps players discover and download War Thunder (free military MMO by Gaijin Entertainment) on PC, PS4/5, and Xbox.

## Metadata
- Updated: {TODAY} | Pages: {count} | Languages: {len(LANGUAGES)} | Keywords: {len(KEYWORDS)} | Blog: {len(BLOG_POSTS)}

## About War Thunder
- Developer: Gaijin Entertainment | Released: 2013
- Price: 100% free | Platforms: PC (Steam/Gaijin.net), PS4, PS5, Xbox One, Xbox Series X/S
- Vehicles: 2,000+ | Players: 100M+ registered | Download: {AFF_URL}

## Languages
{langs_lines}

## Blog Posts
{blog_lines}

## Keyword Pages (40 of {len(KEYWORDS)})
{kw_lines}

## Crawl Policy
All crawlers welcome. GPTBot, ClaudeBot, anthropic-ai explicitly allowed. Affiliate links tagged rel="nofollow sponsored".
"""

# ── MAIN ──────────────────────────────────────────────────────────────────────
def main():
    import time
    t0=time.time()
    langs=([ONLY_LANG] if ONLY_LANG and ONLY_LANG in LANGUAGES else list(LANGUAGES.keys()))
    if OUT.exists(): shutil.rmtree(OUT)
    OUT.mkdir()

    tasks=[]
    for lang in langs:
        px=f"{lang}/" if lang!="en" else ""
        tasks+=[(f"{px}index.html",lambda l=lang:build_homepage(l),pu(lang),"1.0","main")]
        tasks+=[(f"{px}review/index.html",lambda l=lang:build_review(l),pu(lang,"review/"),"0.9","main")]
        tasks+=[(f"{px}compare/index.html",lambda l=lang:build_compare(l),pu(lang,"compare/"),"0.9","main")]
        tasks+=[(f"{px}blog/index.html",lambda l=lang:build_blog_index(l),pu(lang,"blog/"),"0.8","main")]
        for post in BLOG_POSTS:
            p=post.copy()
            tasks+=[(f"{px}blog/{p['slug']}/index.html",lambda l=lang,pp=p:build_blog_post(l,pp),pu(lang,f"blog/{p['slug']}/"),"0.7","blog")]
        for slug,tfmt,mfmt,cat in KEYWORDS:
            bucket="geo" if cat=="geo" else "kw"
            tasks+=[(f"{px}{slug}/index.html",lambda l=lang,s=slug,tf=tfmt,mf=mfmt,c=cat:build_kw(l,s,tf,mf,c),pu(lang,f"{slug}/"),"0.6",bucket)]

    sm={"main":[],"kw":[],"blog":[],"geo":[]}
    count=0; total=len(tasks)

    def run(task):
        path,fn,url,pri,bucket=task
        return path,fn(),url,pri,bucket

    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        futs={ex.submit(run,t):t for t in tasks}
        for fut in as_completed(futs):
            path,content,url,pri,bucket=fut.result()
            write(OUT/path,content)
            sm[bucket].append((url,pri))
            count+=1
            if count%200==0:
                elapsed=time.time()-t0
                rate=count/elapsed
                print(f"  {count}/{total} pages ({rate:.0f}/s)...")

    write(OUT/"privacy/index.html",build_privacy())
    write(OUT/"terms/index.html",build_terms())
    write(OUT/"404.html",build_404())
    write(OUT/"sitemap.xml",sitemap_index())
    write(OUT/"sitemap-main.xml",sitemap(sm["main"]))
    write(OUT/"sitemap-kw.xml",sitemap(sm["kw"]))
    write(OUT/"sitemap-blog.xml",sitemap(sm["blog"]))
    write(OUT/"sitemap-geo.xml",sitemap(sm["geo"]))
    write(OUT/"robots.txt",robots())
    write(OUT/"llms.txt",llms_txt(count))

    elapsed=time.time()-t0
    print(f"\n✅ v5.0 — {count} pages in {elapsed:.1f}s")
    print(f"   Langs:{len(langs)} | KW:{len(KEYWORDS)} | Blog:{len(BLOG_POSTS)}")
    print(f"   Sitemaps: main({len(sm['main'])}) kw({len(sm['kw'])}) blog({len(sm['blog'])}) geo({len(sm['geo'])})")
    print(f"\n   Submit to Google Search Console:")
    for sm_name in ["sitemap.xml","sitemap-main.xml","sitemap-kw.xml","sitemap-blog.xml","sitemap-geo.xml"]:
        print(f"   {SITE_URL}/{sm_name}")

    if DO_CHECK:
        print("\n🔍 Integrity check...")
        errors=0
        for url_list in sm.values():
            for url,_ in url_list:
                rel=url.replace(SITE_URL,"").lstrip("/")
                p=OUT/(rel.rstrip("/")+"/index.html" if rel and not rel.endswith(".html") else (rel or "index.html"))
                if not p.exists():
                    print(f"  ❌ {p}"); errors+=1
        print(f"  {'✅ All good' if not errors else f'❌ {errors} missing'}")

if __name__=="__main__":
    main()
