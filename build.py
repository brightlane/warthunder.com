#!/usr/bin/env python3
"""
build.py — War Thunder Affiliate Site  v4.0
Site   : https://brightlane.github.io/warthunder/
Aff    : https://convert.ctypy.com/aff_c?offer_id=29176&aff_id=21885
Markets: AU, CA, FR, DE, KR, NZ, UK, US
langs  : EN, FR, DE, KO
Pages  : ~700+ (core + 150 keyword pages × 4 langs + blog + utility)
"""

import json, shutil, datetime
from pathlib import Path

# ── CONFIG ────────────────────────────────────────────────────────────────────
SITE_URL  = "https://brightlane.github.io/warthunder"
AFF_URL   = "https://convert.ctypy.com/aff_c?offer_id=29176&aff_id=21885"
SITE_NAME = "WarThunder Guide"
TODAY     = datetime.date.today().isoformat()
YEAR      = str(datetime.date.today().year)
OUT       = Path("dist")

# ── LANGUAGES ─────────────────────────────────────────────────────────────────
LANGUAGES = {
    "en": {
        "name":"English","dir":"ltr","locale":"en_US","lang":"en",
        "cta":"Play Free Now","dl":"Download Free",
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
            ("Is War Thunder pay-to-win?",f"No. Premium vehicles and time can speed progression, but skill is the primary factor. Top players regularly compete in free vehicles in {YEAR}."),
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
    },
    "fr": {
        "name":"Français","dir":"ltr","locale":"fr_FR","lang":"fr",
        "cta":"Jouer Gratuitement","dl":"Télécharger Gratuitement",
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
    },
    "de": {
        "name":"Deutsch","dir":"ltr","locale":"de_DE","lang":"de",
        "cta":"Kostenlos Spielen","dl":"Kostenlos Herunterladen",
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
    },
    "ko": {
        "name":"한국어","dir":"ltr","locale":"ko_KR","lang":"ko",
        "cta":"무료로 플레이","dl":"무료 다운로드",
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
    },
}

# ── KEYWORDS (150 slugs) ──────────────────────────────────────────────────────
# Each entry: (slug, title_en, meta_en, category)
KEYWORDS = [
    # — Free war/military games
    ("free-war-games","Free War Games {y}","Best free war games {y} — play War Thunder free on PC, PS4/5, Xbox.","free"),
    ("free-war-games-pc","Free War Games PC {y}","Best free war games for PC in {y}. Download War Thunder free on Steam.","free"),
    ("free-war-games-ps4","Free War Games PS4 {y}","Best free war games for PS4 in {y}. War Thunder is 100% free on PS4.","free"),
    ("free-war-games-ps5","Free War Games PS5 {y}","Best free war games for PS5 in {y}. Download War Thunder free on PS5.","free"),
    ("free-war-games-xbox","Free War Games Xbox {y}","Best free war games for Xbox {y}. Play War Thunder free on Xbox.","free"),
    ("free-war-games-no-download","Free War Games No Download","Play free war games online. No download required alternatives.","free"),
    ("free-war-games-online","Free War Games Online {y}","Play free war games online {y}. Best browser & download options.","free"),
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
    ("free-warship-games","Free Warship Games {y}","Best free warship games {y}. War Thunder's naval forces feature destroyers to battleships.","free"),
    ("free-naval-combat-games","Free Naval Combat Games {y}","Best free naval combat games {y}. War Thunder naval battles are uniquely realistic.","free"),
    ("free-battleship-games","Free Battleship Games {y}","Best free battleship games {y}. Command real WWII battleships in War Thunder.","free"),
    ("free-submarine-games","Free Submarine Games {y}","Best free submarine games {y}. Explore War Thunder's growing naval roster.","free"),
    ("free-pvp-war-games","Free PvP War Games {y}","Best free PvP war games {y}. War Thunder has millions of active PvP players.","free"),
    ("free-multiplayer-war-games","Free Multiplayer War Games {y}","Best free multiplayer war games {y}. War Thunder supports squads & clans.","free"),
    ("free-team-war-games","Free Team War Games {y}","Best free team war games {y}. Play War Thunder with friends in squad battles.","free"),
    ("free-co-op-war-games","Free Co-op War Games {y}","Best free co-op war games {y}. War Thunder's PvE mode is perfect for squads.","free"),
    ("free-open-world-war-games","Free Open World War Games {y}","Best free open-world military games {y}. War Thunder's maps span kilometers.","free"),
    # — "Best" intent
    ("best-free-war-game","Best Free War Game {y}","What is the best free war game in {y}? War Thunder wins on vehicles, realism & content.","best"),
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
    # — "Games like" searches
    ("games-like-war-thunder","Games Like War Thunder {y}","Looking for games like War Thunder? Compare alternatives and find out why WT is still #1.","similar"),
    ("games-like-war-thunder-free","Free Games Like War Thunder {y}","Best free games like War Thunder {y}. Alternatives reviewed and compared.","similar"),
    ("games-like-world-of-tanks","Games Like World of Tanks {y}","Games like World of Tanks {y}. War Thunder is the top free alternative.","similar"),
    ("games-like-world-of-tanks-free","Free Games Like World of Tanks {y}","Free alternatives to World of Tanks {y}. War Thunder wins on realism.","similar"),
    ("games-like-battlefield-free","Free Games Like Battlefield {y}","Free games like Battlefield {y}. War Thunder offers similar large-scale battles.","similar"),
    ("games-like-call-of-duty-free","Free Games Like Call of Duty {y}","Free alternatives to CoD {y}. War Thunder is free on all the same platforms.","similar"),
    ("war-thunder-alternative","War Thunder Alternative {y}","Looking for a War Thunder alternative? See how it compares to WoT and Crossout.","similar"),
    # — War Thunder specific
    ("is-war-thunder-free","Is War Thunder Free?","Yes — War Thunder is 100% free to download and play. Full details here.","wt"),
    ("is-war-thunder-pay-to-win","Is War Thunder Pay to Win?","Honest answer: is War Thunder pay-to-win in {y}? We break down the economy.","wt"),
    ("is-war-thunder-good","Is War Thunder Good {y}?","Is War Thunder worth playing in {y}? Full honest review.","wt"),
    ("war-thunder-download","War Thunder Download","How to download War Thunder free on PC, PS4/5 and Xbox. Step-by-step guide.","wt"),
    ("war-thunder-download-pc","War Thunder PC Download","Download War Thunder free on PC via Steam or Gaijin.net. Guide & tips.","wt"),
    ("war-thunder-download-ps4","War Thunder PS4 Download","Download War Thunder free on PS4. Step-by-step from the PlayStation Store.","wt"),
    ("war-thunder-download-ps5","War Thunder PS5 Download","Download War Thunder free on PS5. Guide and performance details.","wt"),
    ("war-thunder-download-xbox","War Thunder Xbox Download","Download War Thunder free on Xbox. Guide from the Microsoft Store.","wt"),
    ("war-thunder-review","War Thunder Review {y}","Full War Thunder review {y}. Gameplay, graphics, economy, verdict.","wt"),
    ("war-thunder-beginner-guide","War Thunder Beginner Guide {y}","New to War Thunder? Complete beginner guide for {y} — nations, modes, tips.","wt"),
    ("war-thunder-tips","War Thunder Tips {y}","Top War Thunder tips and tricks {y} to rank up faster.","wt"),
    ("war-thunder-best-nation","Best Nation War Thunder {y}","What is the best nation to start in War Thunder {y}? Full breakdown.","wt"),
    ("war-thunder-usa-tanks","War Thunder USA Tanks {y}","Best US tanks in War Thunder {y}. Full American ground forces guide.","wt"),
    ("war-thunder-germany-tanks","War Thunder Germany Tanks {y}","Best German tanks in War Thunder {y}. Germany ground forces guide.","wt"),
    ("war-thunder-russia-tanks","War Thunder Russia Tanks {y}","Best Soviet/Russian tanks in War Thunder {y}. USSR ground forces guide.","wt"),
    ("war-thunder-britain-tanks","War Thunder Britain Tanks {y}","Best British tanks in War Thunder {y}. UK ground forces guide.","wt"),
    ("war-thunder-japan-tanks","War Thunder Japan Tanks {y}","Best Japanese tanks in War Thunder {y}. Japan ground forces guide.","wt"),
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
    # — Versus / comparison
    ("war-thunder-vs-world-of-tanks","War Thunder vs World of Tanks {y}","War Thunder vs World of Tanks {y}: which free tank game wins?","vs"),
    ("war-thunder-vs-crossout","War Thunder vs Crossout {y}","War Thunder vs Crossout {y}: which free vehicle combat game is better?","vs"),
    ("war-thunder-vs-battlefield","War Thunder vs Battlefield {y}","War Thunder vs Battlefield {y}: free vs paid military game comparison.","vs"),
    ("war-thunder-vs-call-of-duty","War Thunder vs Call of Duty {y}","War Thunder vs Call of Duty {y}: which military game should you play?","vs"),
    ("war-thunder-vs-enlisted","War Thunder vs Enlisted {y}","War Thunder vs Enlisted {y}: both free Gaijin games compared.","vs"),
    ("world-of-tanks-vs-war-thunder","World of Tanks vs War Thunder {y}","WoT vs War Thunder {y}: full comparison. Which is better for you?","vs"),
    # — Geo pages
    ("war-thunder-australia","War Thunder Australia {y}","Play War Thunder free in Australia {y}. Download guide + server info.","geo"),
    ("war-thunder-canada","War Thunder Canada {y}","Play War Thunder free in Canada {y}. Download guide + server tips.","geo"),
    ("war-thunder-uk","War Thunder UK {y}","Play War Thunder free in the UK {y}. Download guide + best British vehicles.","geo"),
    ("war-thunder-new-zealand","War Thunder New Zealand {y}","Play War Thunder free in New Zealand {y}. NZ server guide + tips.","geo"),
    ("war-thunder-south-korea","War Thunder South Korea {y}","Play War Thunder free in South Korea {y}. 워 선더 한국 가이드.","geo"),
    ("war-thunder-germany","War Thunder Germany {y}","Play War Thunder free in Germany {y}. Download guide + German tech tree.","geo"),
    ("war-thunder-france","War Thunder France {y}","Jouez à War Thunder gratuitement en France {y}. Guide de téléchargement.","geo"),
    ("war-thunder-usa","War Thunder USA {y}","Play War Thunder free in the USA {y}. Download guide + American tech tree.","geo"),
    # — Download / play intent
    ("download-war-thunder-free","Download War Thunder Free","How to download War Thunder 100% free on PC, PS4/5, Xbox.","intent"),
    ("play-war-thunder-free","Play War Thunder Free {y}","Play War Thunder free {y}. Full guide on platforms, download, and getting started.","intent"),
    ("play-war-thunder-online","Play War Thunder Online {y}","How to play War Thunder online {y}. Modes, servers, and tips.","intent"),
    ("war-thunder-sign-up","War Thunder Sign Up {y}","How to sign up for War Thunder {y}. Free account creation guide.","intent"),
    ("war-thunder-create-account","Create War Thunder Account","How to create a free War Thunder account. Step-by-step guide.","intent"),
    ("war-thunder-free-to-play","War Thunder Free to Play {y}","War Thunder free to play {y}: what's included for free players?","intent"),
    ("how-to-play-war-thunder","How to Play War Thunder {y}","How to play War Thunder {y}: beginner guide, modes, and first steps.","intent"),
    # — Steam-specific
    ("war-thunder-steam","War Thunder Steam {y}","War Thunder on Steam {y}: how to download, system requirements, and tips.","steam"),
    ("war-thunder-steam-free","War Thunder Steam Free","Is War Thunder free on Steam? Yes — 100% free, rated Very Positive.","steam"),
    ("best-free-war-games-steam","Best Free War Games Steam {y}","Best free war games on Steam {y}. War Thunder leads the rankings.","steam"),
    ("free-games-steam-war","Free War Games on Steam {y}","Top free war games on Steam {y}. Download War Thunder — no cost.","steam"),
    # — PS4/PS5 specific
    ("war-thunder-ps4-free","War Thunder PS4 Free","Is War Thunder free on PS4? Yes — no PS Plus required. Guide here.","console"),
    ("war-thunder-ps5-free","War Thunder PS5 Free","Is War Thunder free on PS5? Yes — no PS Plus required. Full guide.","console"),
    ("war-thunder-ps5-upgrade","War Thunder PS5 Upgrade","Does War Thunder support PS5 upgrade? 60fps and improvements explained.","console"),
    ("free-ps4-games-no-subscription","Free PS4 Games No Subscription {y}","Best free PS4 games with no PlayStation Plus {y}. War Thunder is #1.","console"),
    ("free-ps5-games-no-ps-plus","Free PS5 Games No PS Plus {y}","Best free PS5 games with no PS Plus {y}. War Thunder requires no sub.","console"),
    # — Xbox specific
    ("war-thunder-xbox-free","War Thunder Xbox Free","Is War Thunder free on Xbox? Yes — no Xbox Game Pass required.","console"),
    ("war-thunder-xbox-series-x","War Thunder Xbox Series X","War Thunder on Xbox Series X: performance, fps, and download guide.","console"),
    ("free-xbox-games-no-gold","Free Xbox Games No Gold {y}","Best free Xbox games without Xbox Live Gold {y}. War Thunder is free.","console"),
    # — Historical / niche
    ("ww2-tank-game-free","Free WW2 Tank Game {y}","Best free WW2 tank games {y}. War Thunder has the largest WW2 tank roster.","hist"),
    ("free-cold-war-games","Free Cold War Games {y}","Best free Cold War era military games {y}. War Thunder spans 1950s–1980s jets.","hist"),
    ("free-modern-military-games","Free Modern Military Games {y}","Best free modern military games {y}. War Thunder includes contemporary vehicles.","hist"),
    ("free-wwii-flight-simulator","Free WWII Flight Simulator {y}","Best free WWII flight simulators {y}. War Thunder's Simulator mode is unmatched.","hist"),
    ("free-vietnam-war-games","Free Vietnam War Games {y}","Free games with Vietnam-era vehicles {y}. War Thunder covers the full Cold War period.","hist"),
    ("free-korean-war-games","Free Korean War Games {y}","Free games with Korean War-era vehicles. War Thunder's early jet era covers this.","hist"),
    # — Crossout crossover keywords
    ("crossout-vs-war-thunder","Crossout vs War Thunder {y}","Crossout vs War Thunder {y}: which free vehicle game should you play?","cross"),
    ("war-thunder-crossout","War Thunder and Crossout {y}","War Thunder and Crossout compared: which Gaijin free game wins?","cross"),
    # — Economic/value
    ("is-war-thunder-worth-it","Is War Thunder Worth It {y}?","Is War Thunder worth playing in {y}? Honest pros and cons review.","value"),
    ("war-thunder-free-content","War Thunder Free Content {y}","How much content is free in War Thunder {y}? Full breakdown for free players.","value"),
    ("war-thunder-no-money","Play War Thunder Without Spending Money","Can you enjoy War Thunder without spending money? Yes — here's how.","value"),
    # — Technical
    ("war-thunder-system-requirements","War Thunder System Requirements {y}","War Thunder PC system requirements {y}: minimum and recommended specs.","tech"),
    ("war-thunder-low-end-pc","War Thunder Low End PC {y}","Can War Thunder run on a low-end PC? Settings guide for weak hardware.","tech"),
    ("war-thunder-fps-boost","War Thunder FPS Boost Guide {y}","How to boost FPS in War Thunder {y}. Best graphics settings.","tech"),
    ("war-thunder-lag-fix","War Thunder Lag Fix {y}","How to fix lag in War Thunder {y}. Ping reduction and connection tips.","tech"),
    ("war-thunder-not-launching","War Thunder Not Launching Fix","War Thunder won't launch? Full fix guide for PC.","tech"),
    ("war-thunder-file-size","War Thunder File Size {y}","How big is War Thunder {y}? Download size on all platforms.","tech"),
    ("war-thunder-controller","War Thunder Controller Support","Does War Thunder support controllers? Full guide for PC, PS, Xbox.","tech"),
    ("war-thunder-crossplay","War Thunder Crossplay {y}","Does War Thunder have crossplay {y}? PC, PS4/5, Xbox cross-platform guide.","tech"),
]

# ── BLOG POSTS ────────────────────────────────────────────────────────────────
BLOG_POSTS = [
    {
        "slug":"best-nation-beginners",
        "title":f"Best Nation for Beginners in War Thunder {YEAR}",
        "date":"2025-01-10",
        "desc":f"Choosing your first nation in War Thunder can feel overwhelming. Here's the definitive {YEAR} guide.",
        "body":f"""<p>When you first launch War Thunder in {YEAR}, you'll be asked to choose a nation. This choice affects the vehicles you'll grind, the playstyle you'll develop, and how hard your first 50 hours will be.</p>
<h2>The Top 3 Nations for Beginners</h2>
<h3>1. United States</h3>
<p>The USA is widely considered the easiest starting nation. American tanks are well-armoured at low tiers and their aircraft have forgiving flight characteristics. The M4 Sherman series carries you comfortably through BR 3.0–4.0 while you learn the mechanics.</p>
<h3>2. Soviet Union (USSR)</h3>
<p>Soviet tanks punch above their weight at early BRs. The T-34 is iconic for a reason — sloped armour that bounces shells from opponents at the same tier. The downside: interiors are cramped and crew losses happen fast.</p>
<h3>3. Germany</h3>
<p>Germany has fantastic optics and penetration at every tier, but requires more map knowledge. Great for players who want to snipe from range rather than brawl up close.</p>
<h2>Which Should YOU Pick?</h2>
<p>If you want the smoothest experience: <strong>USA</strong>. If you want high skill ceiling: <strong>Germany</strong>. If you want fast-paced brawling: <strong>USSR</strong>.</p>
<p>Whichever you pick, War Thunder is 100% free — <a href="{AFF_URL}" rel="nofollow sponsored">download it here</a> and try them all.</p>"""
    },
    {
        "slug":"war-thunder-vs-world-of-tanks",
        "title":f"War Thunder vs World of Tanks {YEAR}: The Definitive Comparison",
        "date":"2025-02-14",
        "desc":"Tank enthusiasts often debate War Thunder vs World of Tanks. Here's the honest breakdown.",
        "body":f"""<p>Both games have been around for over a decade, but they offer very different experiences. Here's how they compare in {YEAR}.</p>
<h2>Realism</h2>
<p>War Thunder uses real-world ballistics and armour penetration. Shells ricochet, spall, and destroy specific modules. World of Tanks uses an abstracted HP system — hits deal a percentage of hitpoints. For simulation enthusiasts, War Thunder wins clearly.</p>
<h2>Vehicle Variety</h2>
<p>War Thunder: 2,000+ vehicles across ground, air, and naval. World of Tanks: tanks only (~600 vehicles). If you want planes and ships alongside tanks, War Thunder is the only choice.</p>
<h2>Business Model</h2>
<p>Both are free to play. War Thunder's economy is complex but rewarding for patient players. WoT is often criticised for more aggressive monetisation at higher tiers.</p>
<h2>Verdict</h2>
<p>For realistic combined-arms combat: <strong>War Thunder</strong>. For a more arcade tank-only experience: World of Tanks. War Thunder is <a href="{AFF_URL}" rel="nofollow sponsored">free to download here</a>.</p>"""
    },
    {
        "slug":"silver-lions-farming-guide",
        "title":f"Best Ways to Farm Silver Lions in War Thunder {YEAR}",
        "date":"2025-03-05",
        "desc":f"Silver Lions are War Thunder's main currency. Here are the most efficient farming methods in {YEAR}.",
        "body":f"""<p>Silver Lions (SL) are used to buy vehicles, repair them, and buy ammunition. Running out is one of the most frustrating experiences in War Thunder — here's how to keep your wallet full.</p>
<h2>Top SL Farming Methods {YEAR}</h2>
<h3>1. Play Premium Time Missions</h3>
<p>Premium account (or a single premium vehicle) gives a 100% SL bonus. Even a few days of premium around a sale massively accelerates earning.</p>
<h3>2. Use Talismanned Vehicles</h3>
<p>A Talisman on your favourite vehicle gives permanent bonus RP <em>and</em> helps you perform better — better performance = more SL per match.</p>
<h3>3. Fly Bombers</h3>
<p>Destroying bases in Air Realistic Battles yields high SL rewards even with average performance. IL-4 and B-17 are popular SL grinders.</p>
<h3>4. Play Low Tiers Occasionally</h3>
<p>Repair costs are minimal at BR 1.0–2.0. A winning streak at low tier can net positive SL even without premium.</p>
<h3>5. Complete Daily Missions</h3>
<p>Daily tasks award bonus SL multipliers. Always complete them before long sessions.</p>
<p>Ready to try? War Thunder is <a href="{AFF_URL}" rel="nofollow sponsored">100% free to download</a>.</p>"""
    },
    {
        "slug":"war-thunder-beginners-guide",
        "title":f"War Thunder Complete Beginner Guide {YEAR}",
        "date":"2025-04-01",
        "desc":f"Everything a new War Thunder player needs to know in {YEAR}. Modes, nations, tips, and more.",
        "body":f"""<p>War Thunder can feel overwhelming when you first start. This guide covers everything you need to know for {YEAR}.</p>
<h2>Step 1: Choose Your Nation</h2>
<p>USA is easiest for beginners. USSR for aggressive play. Germany for sniping. Full nation guide: <a href="{SITE_URL}/en/best-nation-beginners/">Best Nation Guide</a>.</p>
<h2>Step 2: Understand the Three Modes</h2>
<ul>
<li><strong>Arcade Battles (AB)</strong> — Simplified physics, lead indicators, faster matches. Best for learning.</li>
<li><strong>Realistic Battles (RB)</strong> — No lead indicators, real ballistics, one life per vehicle. Most popular mode.</li>
<li><strong>Simulator Battles (SB)</strong> — Full cockpit view, no HUD. For hardcore fans.</li>
</ul>
<h2>Step 3: Play Arcade First</h2>
<p>Spend your first 20–30 games in Arcade to learn maps and vehicle strengths. Move to RB once you're comfortable.</p>
<h2>Step 4: Don't Rush the Tech Tree</h2>
<p>Many new players rush to high tiers and then struggle with repair costs. Enjoy the journey — each BR range has a unique meta.</p>
<p><a href="{AFF_URL}" rel="nofollow sponsored">Download War Thunder free here</a> and get started today.</p>"""
    },
    {
        "slug":"war-thunder-fps-guide",
        "title":f"War Thunder FPS Boost Guide {YEAR} — Get More Performance",
        "date":"2025-05-10",
        "desc":f"How to get more FPS in War Thunder {YEAR}. Graphics settings, launch options, and hardware tips.",
        "body":f"""<p>War Thunder runs on a custom version of the Dagor Engine. With the right settings, even mid-range PCs can hit 60+ FPS consistently in {YEAR}.</p>
<h2>Critical Settings to Change</h2>
<ul>
<li><strong>Texture Quality:</strong> Set to Medium unless you have 8GB+ VRAM</li>
<li><strong>Shadows:</strong> Drop to Medium or Low — major FPS impact</li>
<li><strong>SSAO:</strong> Disable — barely visible, costs FPS</li>
<li><strong>Grass Density:</strong> Low — zero competitive disadvantage</li>
<li><strong>DLSS/FSR:</strong> Enable if your GPU supports it</li>
</ul>
<h2>Launch Options (Steam)</h2>
<p>In Steam properties, add: <code>-dx11</code> if you have an older GPU, or <code>-dx12</code> for newer Nvidia/AMD cards.</p>
<h2>Minimum Specs vs Recommended</h2>
<p><strong>Minimum:</strong> Intel i5-4460, 8GB RAM, GTX 660/RX 560, 40GB storage<br>
<strong>Recommended:</strong> Intel i7-9700K, 16GB RAM, RTX 2070/RX 5700 XT</p>
<p>War Thunder is <a href="{AFF_URL}" rel="nofollow sponsored">free to download</a> — optimise and enjoy.</p>"""
    },
    {
        "slug":"war-thunder-best-premium-vehicles",
        "title":f"Best Premium Vehicles in War Thunder {YEAR}",
        "date":"2025-06-15",
        "desc":f"Which premium vehicles are worth buying in War Thunder {YEAR}? Full ranked list.",
        "body":f"""<p>Premium vehicles cost Golden Eagles or real money, but the right ones pay for themselves in RP and SL bonuses. Here are the best in {YEAR}.</p>
<h2>Best Ground Premiums</h2>
<p><strong>T-54 1951 (USSR, BR 8.3)</strong> — Outstanding armour, reliable cannon, great SL earner.<br>
<strong>M1 KVT (USA, BR 10.0)</strong> — M1 Abrams hull with an upgraded gun. Devastating in top-tier.<br>
<strong>Leopard A1A1 L/44 (Germany, BR 9.7)</strong> — High penetration APFSDS, great mobility.</p>
<h2>Best Air Premiums</h2>
<p><strong>F-89B (USA, BR 7.3)</strong> — Rocket-heavy American jet, efficient SL farmer.<br>
<strong>IL-2 1942 (USSR, BR 2.3)</strong> — Budget premium, easy ground attack SL grinding.</p>
<h2>Should You Buy Premium?</h2>
<p>Only if you enjoy the game first. War Thunder is fully playable free. Try it <a href="{AFF_URL}" rel="nofollow sponsored">here for free</a> before spending anything.</p>"""
    },
    {
        "slug":"war-thunder-crossplay-guide",
        "title":f"War Thunder Crossplay Guide {YEAR} — PC, PS4/5, Xbox",
        "date":"2025-07-20",
        "desc":f"Does War Thunder have crossplay in {YEAR}? Full guide for all platforms.",
        "body":f"""<p>War Thunder fully supports crossplay between PC, PlayStation 4, PlayStation 5, Xbox One, and Xbox Series X|S in {YEAR}.</p>
<h2>How Crossplay Works</h2>
<p>All platforms share the same matchmaking pool. PC players and console players compete in the same battles. There are no region-locked servers — Australian, UK, and Korean players can all play together.</p>
<h2>Does PC Have an Advantage?</h2>
<p>PC players with mice have a slight aiming advantage in Arcade mode. In Realistic and Simulator modes, the playing field is more level since all players use manual aiming.</p>
<h2>Can I Play with Console Friends on PC?</h2>
<p>Yes — War Thunder uses a universal account system. Your account and progression work across all platforms. You can switch platforms and your vehicles, crew, and Silver Lions carry over.</p>
<h2>How to Add Cross-Platform Friends</h2>
<p>Search by username in the in-game friends list. Platform doesn't matter — the system is unified.</p>
<p>Play War Thunder free on any platform: <a href="{AFF_URL}" rel="nofollow sponsored">download here</a>.</p>"""
    },
    {
        "slug":"war-thunder-naval-guide",
        "title":f"War Thunder Naval Forces Guide {YEAR} — Getting Started",
        "date":"2025-08-18",
        "desc":f"Complete War Thunder naval forces guide for {YEAR}. Ships, destroyers, battleships explained.",
        "body":f"""<p>War Thunder's naval forces are the newest and most underplayed branch — which means faster matchmaking and easier progress in {YEAR}.</p>
<h2>Naval Basics</h2>
<p>Naval battles feature coastal vessels (torpedo boats, gun boats) at low BRs and bluewater fleets (destroyers, cruisers, battleships) at higher BRs.</p>
<h2>Best Starting Nation for Navy</h2>
<p><strong>USA</strong> — PT boats at low tier are fast and punchy. The Destroyer line is reliable.<br>
<strong>USSR</strong> — Beefy gun boats at low BR. Easy to learn.<br>
<strong>Germany</strong> — E-boats (S-Boote) are fast torpedo platforms perfect for flanking.</p>
<h2>Key Naval Tips</h2>
<ul>
<li>Aim for the waterline to flood opponents</li>
<li>Use smoke to disengage — naval battles punish stationary targets hard</li>
<li>Prioritise crew compartments over engine rooms in early engagements</li>
</ul>
<p>War Thunder naval is <a href="{AFF_URL}" rel="nofollow sponsored">free to play</a> — no additional purchase needed.</p>"""
    },
    {
        "slug":"war-thunder-update-history",
        "title":f"War Thunder Major Updates History {YEAR}",
        "date":"2025-09-05",
        "desc":f"War Thunder's biggest updates and what they added. Full {YEAR} update history.",
        "body":f"""<p>Gaijin Entertainment updates War Thunder multiple times per year. Here's what the major updates have brought.</p>
<h2>Recent Major Updates</h2>
<p><strong>Seek & Destroy (2024)</strong> — Introduced player-customisable tank commanders, reworked crew mechanics, new top-tier aircraft including the F-15E Strike Eagle and Su-30SM.</p>
<p><strong>Air Superiority (2023)</strong> — Added F-16C, MiG-29SMT, Eurofighter Typhoon (early access), and the Israeli tech tree aircraft expansion.</p>
<p><strong>Kings of Battle (2023)</strong> — Surface-to-surface missiles, Guided Bomb Units (GBUs), and a major naval rework for destroyer-class vessels.</p>
<h2>What to Expect in Future Updates</h2>
<p>Gaijin typically announces upcoming content on their official Dev Blog. New top-tier jets, naval expansions, and new national tech trees are always on the roadmap.</p>
<p>Stay up to date and <a href="{AFF_URL}" rel="nofollow sponsored">download War Thunder free</a>.</p>"""
    },
    {
        "slug":"war-thunder-helicopter-guide",
        "title":f"War Thunder Helicopter Guide {YEAR} — Best Helicopters & Tips",
        "date":"2025-10-12",
        "desc":f"Best helicopters in War Thunder {YEAR} and how to use them effectively.",
        "body":f"""<p>Helicopters in War Thunder are powerful but challenging to master. This guide covers the best options and core tactics for {YEAR}.</p>
<h2>Helicopter Basics</h2>
<p>Helicopters unlock at Rank VI in the ground tree of most nations. They spawn from the airfield and can engage ground targets with ATGMs (anti-tank guided missiles) from stand-off distance.</p>
<h2>Best Starter Helicopters</h2>
<p><strong>Mi-4AV (USSR)</strong> — Easy to fly, armed with unguided rockets. Great for learning the mode.<br>
<strong>UH-1B (USA)</strong> — The iconic Huey. Rockets and miniguns, beginner-friendly handling.<br>
<strong>Alouette III SA 316B (France/Germany)</strong> — Small, nimble, early ATGM carrier.</p>
<h2>Advanced Tips</h2>
<ul>
<li>Never hover stationary — SPAA (anti-aircraft) will destroy you instantly</li>
<li>Use terrain masking — fly behind hills and pop up to fire ATGMs</li>
<li>Prioritise SPAA first before engaging tanks</li>
<li>Flares are essential above BR 9.0</li>
</ul>
<p>Download War Thunder free: <a href="{AFF_URL}" rel="nofollow sponsored">click here</a>.</p>"""
    },
    {
        "slug":"war-thunder-realistic-battles-guide",
        "title":f"War Thunder Realistic Battles Guide {YEAR}",
        "date":"2025-11-08",
        "desc":f"How to succeed in War Thunder Realistic Battles (RB) in {YEAR}. Complete tactics guide.",
        "body":f"""<p>Realistic Battles (RB) is War Thunder's most popular game mode in {YEAR}. No lead indicators, real ballistics, and one life per vehicle make it more demanding — and more rewarding.</p>
<h2>Key Differences from Arcade</h2>
<ul>
<li>No lead indicator — you must judge shell travel time yourself</li>
<li>No crew replenishment between deaths in same vehicle</li>
<li>No nametags — spotting enemies requires actual visibility</li>
<li>One spawn per vehicle per match (aircraft have airfield respawns)</li>
</ul>
<h2>Core RB Principles</h2>
<p><strong>Patience wins.</strong> Rushing is how you die in the first 90 seconds. Move slowly, use cover, and let enemies expose themselves first.</p>
<p><strong>Know your weak spots.</strong> Every tank has armour weak spots. Learn them in the armour viewer before you queue.</p>
<p><strong>First shot matters.</strong> In RB, a penetrating first shot usually kills. Miss and you'll likely take a return shot before you reload.</p>
<h2>Map Awareness</h2>
<p>Study spawn points and choke points. In RB, the minimap is your most important tool — tanks that appear on it have been spotted by allies.</p>
<p>Ready to try RB? <a href="{AFF_URL}" rel="nofollow sponsored">Download War Thunder free here</a>.</p>"""
    },
    {
        "slug":"war-thunder-golden-eagles-guide",
        "title":f"How to Get Golden Eagles in War Thunder {YEAR}",
        "date":"2025-12-01",
        "desc":f"Legitimate ways to earn free Golden Eagles in War Thunder {YEAR}. No hacks, no scams.",
        "body":f"""<p>Golden Eagles (GE) are War Thunder's premium currency. While they're primarily purchased, there are a few legitimate ways to earn them free.</p>
<h2>Legitimate Free GE Methods {YEAR}</h2>
<p><strong>1. Twitch Drops</strong> — Gaijin regularly runs Twitch Drop campaigns where watching official or partnered streams awards premium items and occasionally Golden Eagles. Check the official War Thunder website for active campaigns.</p>
<p><strong>2. Competitions & Tournaments</strong> — Gaijin runs community screenshot contests, art contests, and player tournaments with GE prizes. Check the forums regularly.</p>
<p><strong>3. Content Creator Program</strong> — If you make War Thunder YouTube or Twitch content, you may qualify for the Gaijin creator program which provides a custom referral link earning GE per new signup.</p>
<p><strong>4. Battle Pass</strong> — Completing the free tier of each Battle Pass season can award some GE.</p>
<h2>Avoid Golden Eagle Scams</h2>
<p>Any website claiming to give you free GE by entering your login is a scam. Gaijin will never ask for your password outside the official client.</p>
<p><a href="{AFF_URL}" rel="nofollow sponsored">Download War Thunder free</a> and earn your way up legitimately.</p>"""
    },
]

# ── CSS ────────────────────────────────────────────────────────────────────────
CSS = """
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{--c-primary:#4a7c59;--c-accent:#d4a017;--c-dark:#1a1a1a;--c-text:#222;--c-muted:#555;--c-bg:#f8f8f5;--c-white:#fff;--radius:8px;--shadow:0 2px 12px rgba(0,0,0,.1)}
html{scroll-behavior:smooth}
body{font-family:'Open Sans',sans-serif;background:var(--c-bg);color:var(--c-text);line-height:1.7}
a{color:var(--c-primary);text-decoration:none}
a:hover{text-decoration:underline}
.container{max-width:1100px;margin:0 auto;padding:0 20px}

/* NAV */
.nav{background:var(--c-dark);position:sticky;top:0;z-index:99;box-shadow:var(--shadow)}
.nav-i{display:flex;align-items:center;justify-content:space-between;height:60px}
.logo{color:var(--c-white);font-family:'Oswald',sans-serif;font-size:1.4rem;font-weight:700;display:flex;align-items:center;gap:8px}
.logo span{color:var(--c-accent)}
.logo-mark{background:var(--c-accent);color:var(--c-dark);width:28px;height:28px;border-radius:4px;display:grid;place-items:center;font-size:.9rem}
.nav-links{display:flex;align-items:center;gap:16px}
.nav-links a{color:#ccc;font-size:.9rem;transition:color .2s}
.nav-links a:hover{color:var(--c-white);text-decoration:none}
.nav-cta{background:var(--c-accent)!important;color:var(--c-dark)!important;padding:6px 14px;border-radius:var(--radius);font-weight:700;font-size:.85rem!important}
.nav-cta:hover{opacity:.9;text-decoration:none!important}

/* HERO */
.hero{background:linear-gradient(135deg,#1a2a1a 0%,#2d4a2d 60%,#1a3a1a 100%);color:var(--c-white);padding:80px 20px;text-align:center;position:relative;overflow:hidden}
.hero::before{content:'';position:absolute;inset:0;background:url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.03'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")}
.hero-tag{background:var(--c-accent);color:var(--c-dark);font-size:.75rem;font-weight:700;padding:4px 12px;border-radius:20px;display:inline-block;margin-bottom:16px;letter-spacing:.05em;text-transform:uppercase}
.hero h1{font-family:'Oswald',sans-serif;font-size:clamp(2rem,6vw,3.5rem);font-weight:700;line-height:1.1;margin-bottom:8px}
.hero h1 span{color:var(--c-accent)}
.hero-sub{font-size:1.1rem;max-width:600px;margin:16px auto 32px;opacity:.9}
.hero-btns{display:flex;gap:12px;justify-content:center;flex-wrap:wrap}
.btn-primary{background:var(--c-accent);color:var(--c-dark);padding:14px 32px;border-radius:var(--radius);font-weight:700;font-size:1rem;transition:transform .2s,opacity .2s}
.btn-primary:hover{transform:translateY(-2px);opacity:.9;text-decoration:none}
.btn-secondary{background:transparent;color:var(--c-white);border:2px solid rgba(255,255,255,.4);padding:12px 28px;border-radius:var(--radius);font-weight:600;transition:border-color .2s}
.btn-secondary:hover{border-color:var(--c-white);text-decoration:none}
.stats-bar{display:flex;gap:32px;justify-content:center;flex-wrap:wrap;margin-top:48px;padding-top:32px;border-top:1px solid rgba(255,255,255,.15)}
.stat{text-align:center}
.stat-n{font-family:'Oswald',sans-serif;font-size:2rem;font-weight:700;color:var(--c-accent)}
.stat-l{font-size:.8rem;opacity:.7;text-transform:uppercase;letter-spacing:.05em}

/* SECTIONS */
.section{padding:64px 0}
.section-alt{background:var(--c-white)}
.section-title{font-family:'Oswald',sans-serif;font-size:clamp(1.5rem,4vw,2.2rem);font-weight:700;text-align:center;margin-bottom:8px}
.section-sub{text-align:center;color:var(--c-muted);margin-bottom:48px;max-width:560px;margin-left:auto;margin-right:auto}

/* WHY GRID */
.why-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:24px}
.why-card{background:var(--c-white);border-radius:var(--radius);padding:28px;box-shadow:var(--shadow);border-left:4px solid var(--c-primary)}
.why-card h3{font-family:'Oswald',sans-serif;font-size:1.1rem;margin-bottom:8px;color:var(--c-dark)}
.why-card p{font-size:.9rem;color:var(--c-muted)}

/* COMPARE TABLE */
.compare-table{width:100%;border-collapse:collapse;font-size:.9rem}
.compare-table th{background:var(--c-dark);color:var(--c-white);padding:12px 16px;text-align:left;font-family:'Oswald',sans-serif;font-size:1rem}
.compare-table th:first-child{background:var(--c-primary)}
.compare-table td{padding:11px 16px;border-bottom:1px solid #e8e8e8}
.compare-table tr:nth-child(even) td{background:#f5f5f2}
.compare-table .winner{color:var(--c-primary);font-weight:700}
.compare-table .loser{color:#999}
.tbl-wrap{overflow-x:auto}

/* FAQ */
.faq{max-width:760px;margin:0 auto}
.faq-item{border-bottom:1px solid #e8e8e8;padding:20px 0}
.faq-q{font-weight:700;font-size:1rem;margin-bottom:8px;color:var(--c-dark)}
.faq-a{color:var(--c-muted);font-size:.95rem}

/* BLOG GRID */
.blog-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:24px}
.blog-card{background:var(--c-white);border-radius:var(--radius);box-shadow:var(--shadow);overflow:hidden;transition:transform .2s}
.blog-card:hover{transform:translateY(-4px)}
.blog-card-body{padding:20px}
.blog-card-body h3{font-family:'Oswald',sans-serif;font-size:1.1rem;margin-bottom:8px}
.blog-card-body p{font-size:.85rem;color:var(--c-muted);margin-bottom:12px}
.blog-card-body a{font-weight:700;font-size:.85rem}

/* KW PAGE */
.kw-hero{background:linear-gradient(135deg,#1a2a1a,#2d4a2d);color:var(--c-white);padding:56px 20px;text-align:center}
.kw-hero h1{font-family:'Oswald',sans-serif;font-size:clamp(1.6rem,5vw,2.8rem);font-weight:700;margin-bottom:12px}
.kw-hero p{opacity:.85;max-width:560px;margin:0 auto 24px}
.rating-row{display:flex;gap:24px;justify-content:center;flex-wrap:wrap;margin:32px 0}
.rating-box{text-align:center;background:rgba(255,255,255,.08);padding:16px 20px;border-radius:var(--radius)}
.rating-box .score{font-family:'Oswald',sans-serif;font-size:2rem;color:var(--c-accent);font-weight:700}
.rating-box .label{font-size:.75rem;opacity:.7;text-transform:uppercase;letter-spacing:.05em}
.kw-body{max-width:780px;margin:0 auto;padding:48px 20px}
.kw-body h2{font-family:'Oswald',sans-serif;font-size:1.4rem;margin:32px 0 12px;color:var(--c-dark)}
.kw-body p{margin-bottom:16px;color:var(--c-muted)}
.kw-body ul{padding-left:20px;margin-bottom:16px;color:var(--c-muted)}
.kw-body ul li{margin-bottom:6px}
.kw-cta-box{background:linear-gradient(135deg,var(--c-primary),#2d5a3d);color:var(--c-white);text-align:center;padding:40px 24px;border-radius:12px;margin:40px 0}
.kw-cta-box h3{font-family:'Oswald',sans-serif;font-size:1.5rem;margin-bottom:8px}
.kw-cta-box p{opacity:.85;margin-bottom:20px}
.related-links{display:flex;flex-wrap:wrap;gap:10px;margin-top:12px}
.related-links a{background:var(--c-white);border:1px solid #ddd;padding:6px 14px;border-radius:20px;font-size:.8rem;color:var(--c-primary);transition:background .2s}
.related-links a:hover{background:var(--c-primary);color:var(--c-white);text-decoration:none}
.breadcrumb{font-size:.8rem;color:var(--c-muted);margin-bottom:8px}
.breadcrumb a{color:var(--c-muted)}
.breadcrumb a:hover{color:var(--c-primary)}

/* BLOG POST */
.post-hero{background:linear-gradient(135deg,#1a2a1a,#2d4a2d);color:var(--c-white);padding:56px 20px;text-align:center}
.post-hero h1{font-family:'Oswald',sans-serif;font-size:clamp(1.5rem,4vw,2.4rem);font-weight:700;max-width:760px;margin:0 auto 12px}
.post-body{max-width:780px;margin:48px auto;padding:0 20px}
.post-body h2{font-family:'Oswald',sans-serif;font-size:1.5rem;margin:32px 0 12px;color:var(--c-dark)}
.post-body h3{font-size:1.1rem;font-weight:700;margin:24px 0 8px;color:var(--c-dark)}
.post-body p{margin-bottom:16px;color:var(--c-muted)}
.post-body ul{padding-left:20px;margin-bottom:16px;color:var(--c-muted)}
.post-body ul li{margin-bottom:6px}
.post-body strong{color:var(--c-dark)}

/* REVIEW */
.review-score{display:flex;gap:24px;flex-wrap:wrap;justify-content:center;margin:32px 0}
.score-card{text-align:center;background:var(--c-white);border-radius:var(--radius);padding:20px;box-shadow:var(--shadow);min-width:120px}
.score-card .score{font-family:'Oswald',sans-serif;font-size:2.2rem;color:var(--c-primary);font-weight:700}
.score-card .label{font-size:.75rem;color:var(--c-muted);text-transform:uppercase}

/* FOOTER */
.footer{background:var(--c-dark);color:#999;padding:40px 0}
.footer-i{display:flex;flex-direction:column;gap:16px;align-items:center;text-align:center}
.footer-disc{font-size:.78rem;max-width:700px;line-height:1.6}
.footer-links{display:flex;flex-wrap:wrap;gap:12px;justify-content:center}
.footer-links a{color:#666;font-size:.82rem}
.footer-links a:hover{color:#ccc;text-decoration:none}

@media(max-width:640px){
  .stats-bar{gap:20px}
  .nav-links a:not(.nav-cta){display:none}
  .hero-btns{flex-direction:column;align-items:center}
}
"""

# ── HELPERS ───────────────────────────────────────────────────────────────────
def pu(lang, path=""):
    """Page URL helper"""
    base = f"{SITE_URL}/{lang}" if lang != "en" else SITE_URL
    return f"{base}/{path}" if path else f"{base}/"

def hreflang_tags(path="", langs=None):
    tags = []
    for lc in (langs or LANGUAGES.keys()):
        url = pu(lc, path)
        tags.append(f'<link rel="alternate" hreflang="{lc}" href="{url}"/>')
    tags.append(f'<link rel="alternate" hreflang="x-default" href="{pu("en", path)}"/>')
    return "\n".join(tags)

def nav_links_html(lang, t):
    return (f'<a href="{pu(lang)}">{t["nav_home"]}</a>'
            f'<a href="{pu(lang,"review/")}">{t["nav_review"]}</a>'
            f'<a href="{pu(lang,"compare/")}">{t["nav_compare"]}</a>'
            f'<a href="{pu(lang,"blog/")}">{t["nav_blog"]}</a>')

def page_shell(lang, title, meta_desc, canonical, body, extra_head="", schema=""):
    t = LANGUAGES[lang]
    nav_html = nav_links_html(lang, t)
    return f"""<!DOCTYPE html>
<html lang="{lang}" dir="{t['dir']}">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>{title} — {SITE_NAME}</title>
<meta name="description" content="{meta_desc}"/>
<link rel="canonical" href="{canonical}"/>
<meta property="og:title" content="{title}"/>
<meta property="og:description" content="{meta_desc}"/>
<meta property="og:url" content="{canonical}"/>
<meta property="og:type" content="website"/>
<meta property="og:site_name" content="{SITE_NAME}"/>
<meta name="twitter:card" content="summary_large_image"/>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link href="https://fonts.googleapis.com/css2?family=Oswald:wght@600;700&family=Open+Sans:wght@400;600&display=swap" rel="stylesheet"/>
<style>{CSS}</style>
{extra_head}
{schema}
</head>
<body>
<nav class="nav"><div class="container nav-i">
  <a href="{pu(lang)}" class="logo"><div class="logo-mark">⚡</div>War<span>Thunder</span></a>
  <div class="nav-links">{nav_html}<a href="{AFF_URL}" class="nav-cta" target="_blank" rel="nofollow sponsored">{t['cta']}</a></div>
</div></nav>
{body}
<footer class="footer"><div class="container footer-i">
  <p class="footer-disc">{t['disc']}</p>
  <div class="footer-links">
    <a href="{pu(lang)}">Home</a>
    <a href="{pu(lang,'review/')}">Review</a>
    <a href="{pu(lang,'compare/')}">Compare</a>
    <a href="{pu(lang,'blog/')}">Blog</a>
    <a href="{pu('en','privacy/')}">Privacy</a>
    <a href="{pu('en','terms/')}">Terms</a>
  </div>
</div></footer>
</body></html>"""

def faq_schema(qas):
    items = [{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in qas]
    sc = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":items}
    return f'<script type="application/ld+json">{json.dumps(sc)}</script>'

def breadcrumb_schema(items):
    els = [{"@type":"ListItem","position":i+1,"name":n,"item":u} for i,(n,u) in enumerate(items)]
    sc = {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":els}
    return f'<script type="application/ld+json">{json.dumps(sc)}</script>'

def article_schema(title, desc, date, url):
    sc = {"@context":"https://schema.org","@type":"Article",
          "headline":title,"description":desc,"datePublished":date,
          "dateModified":TODAY,"url":url,
          "publisher":{"@type":"Organization","name":SITE_NAME}}
    return f'<script type="application/ld+json">{json.dumps(sc)}</script>'

def videogame_schema():
    sc = {"@context":"https://schema.org","@type":"VideoGame",
          "name":"War Thunder","description":"Free-to-play military MMO with aircraft, tanks, and naval vessels.",
          "genre":["Military","Simulation","Action"],"gamePlatform":["PC","PlayStation 4","PlayStation 5","Xbox One","Xbox Series X"],
          "operatingSystem":"Windows, macOS, Linux, PlayStation, Xbox",
          "applicationCategory":"Game","offers":{"@type":"Offer","price":"0","priceCurrency":"USD"},
          "url":AFF_URL}
    return f'<script type="application/ld+json">{json.dumps(sc)}</script>'

def write(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")

# ── KW PAGE COPY GENERATOR ────────────────────────────────────────────────────
CATEGORY_COPY = {
    "free": lambda slug, title, y: f"""
        <h2>What Makes a Great Free War Game in {y}?</h2>
        <p>Not all free war games are equal. The best ones offer genuine depth — a large vehicle or unit roster, regular updates, a fair free-to-play economy, and a healthy player base that keeps matchmaking fast.</p>
        <p>War Thunder ticks every box: 2,000+ historically accurate vehicles, real physics, cross-platform play, and a community of 100 million registered players.</p>
        <h2>Why War Thunder Leads in {y}</h2>
        <ul>
          <li><strong>Truly free:</strong> Download and play indefinitely at no cost</li>
          <li><strong>Air, ground & naval:</strong> Most free military games cover one branch — War Thunder covers all three</li>
          <li><strong>Realistic physics:</strong> Shells ricochet, armour angles matter, damage is modelled per-component</li>
          <li><strong>All platforms:</strong> PC (Steam & Gaijin), PS4, PS5, Xbox — with crossplay</li>
          <li><strong>Constant updates:</strong> Multiple major content drops per year</li>
        </ul>
        <h2>Getting Started</h2>
        <p>Sign up via the button above, choose your nation (USA is easiest for beginners), and you'll be in your first battle within minutes. The tutorial covers basic controls and aiming — it's shorter than most games and gets you into matches fast.</p>
    """,
    "best": lambda slug, title, y: f"""
        <h2>How We Rank Free War Games in {y}</h2>
        <p>Our ranking looks at four factors: vehicle & content depth, free-to-play fairness, active player base, and platform availability. War Thunder scores top marks across all four in {y}.</p>
        <h2>The Comparison</h2>
        <div class="tbl-wrap"><table class="compare-table">
        <tr><th>Game</th><th>Price</th><th>Vehicles</th><th>Platforms</th><th>Realism</th></tr>
        <tr><td><strong>War Thunder</strong></td><td class="winner">Free</td><td class="winner">2,000+</td><td class="winner">PC/PS/Xbox</td><td class="winner">★★★★★</td></tr>
        <tr><td>World of Tanks</td><td class="winner">Free</td><td>600+</td><td>PC/Console</td><td class="loser">★★★☆☆</td></tr>
        <tr><td>Crossout</td><td class="winner">Free</td><td>Custom</td><td>PC/PS/Xbox</td><td class="loser">★★★☆☆</td></tr>
        <tr><td>Enlisted</td><td class="winner">Free</td><td>Infantry+</td><td>PC/PS/Xbox</td><td>★★★★☆</td></tr>
        </table></div>
        <h2>Bottom Line</h2>
        <p>For sheer content, realism, and platform coverage, War Thunder is the answer to "what is the best free war game in {y}?" — and it's not close.</p>
    """,
    "similar": lambda slug, title, y: f"""
        <h2>What to Look for in War Thunder Alternatives</h2>
        <p>If you're looking for something similar, the key features to match are: vehicle-based combat, free-to-play access, and realistic or semi-realistic physics. Few games hit all three.</p>
        <h2>How Alternatives Compare</h2>
        <p><strong>World of Tanks</strong> — Tank-only, arcade physics, no air or naval. Good for casual play.</p>
        <p><strong>Crossout</strong> — Post-apocalyptic vehicle builder. More arcade, customizable machines. Also free.</p>
        <p><strong>Enlisted</strong> — Squad-based WWII infantry + vehicles. Also made by Gaijin. Free to play.</p>
        <p><strong>IL-2 Sturmovik</strong> — Deep flight sim but paid. Better cockpit simulation, tiny player base.</p>
        <h2>Why People Return to War Thunder</h2>
        <p>No alternative matches War Thunder's combination of content breadth (air + ground + naval), historical accuracy, and free access. It remains the category leader in {y}.</p>
    """,
    "wt": lambda slug, title, y: f"""
        <h2>The Honest Answer</h2>
        <p>War Thunder's free-to-play model in {y} is genuinely one of the fairer ones in the genre. All vehicles are earnable without spending money — premium content speeds up the grind but never gates core gameplay.</p>
        <h2>What's Free</h2>
        <ul>
          <li>Entire base vehicle tech tree (all nations, all branches)</li>
          <li>All game modes (Arcade, Realistic, Simulator)</li>
          <li>All maps (100+)</li>
          <li>Regular battle pass free tier</li>
          <li>Events with earnable premium vehicles</li>
        </ul>
        <h2>What Costs Money</h2>
        <ul>
          <li>Premium account (doubles RP/SL earn rate)</li>
          <li>Premium vehicles (skip part of the grind)</li>
          <li>Cosmetics (skins, decals, emblems)</li>
        </ul>
        <p>None of the paid content is required to reach top tier or compete effectively. Skill matters more than spending in War Thunder.</p>
    """,
    "vs": lambda slug, title, y: f"""
        <h2>Side-by-Side Comparison</h2>
        <div class="tbl-wrap"><table class="compare-table">
        <tr><th>Feature</th><th>War Thunder</th><th>Competitor</th></tr>
        <tr><td>Price</td><td class="winner">Free</td><td>Free / Paid</td></tr>
        <tr><td>Vehicle Types</td><td class="winner">Air + Ground + Naval</td><td>Varies</td></tr>
        <tr><td>Realism</td><td class="winner">Simulation-grade</td><td>Arcade–Semi</td></tr>
        <tr><td>Platforms</td><td class="winner">PC, PS4/5, Xbox</td><td>Varies</td></tr>
        <tr><td>Player Base</td><td class="winner">100M+ registered</td><td>Smaller</td></tr>
        <tr><td>Update Cadence</td><td class="winner">Major updates quarterly</td><td>Varies</td></tr>
        </table></div>
        <h2>Which Should You Play?</h2>
        <p>If you want the most realistic combined-arms military game for free in {y}, War Thunder wins. If you prefer a more arcade experience with simpler mechanics, the alternative may suit you better.</p>
        <p>Both are free — try War Thunder first and decide for yourself.</p>
    """,
    "geo": lambda slug, title, y: f"""
        <h2>Playing War Thunder in Your Region</h2>
        <p>War Thunder is fully available in your country in {y}. Download from the official Gaijin website, Steam, PlayStation Store, or Microsoft Store. Your account works across all platforms and carries your progress.</p>
        <h2>Server & Ping</h2>
        <p>War Thunder has dedicated servers in Europe, North America, Asia, and Australia. The game automatically selects the best server for your location. Players in AU, NZ, and Korea typically connect to the Asia-Pacific cluster.</p>
        <h2>Payment & Currency</h2>
        <p>The base game is 100% free — no payment needed to download or play. If you choose to buy Golden Eagles, they're priced in your local currency via your platform's store.</p>
        <h2>Download Steps</h2>
        <ul>
          <li><strong>PC:</strong> Go to Gaijin.net or Steam → search War Thunder → Install (free)</li>
          <li><strong>PS4/PS5:</strong> PlayStation Store → search War Thunder → Download (free)</li>
          <li><strong>Xbox:</strong> Microsoft Store → search War Thunder → Get (free)</li>
        </ul>
    """,
    "intent": lambda slug, title, y: f"""
        <h2>How to Get Started in {y}</h2>
        <p>War Thunder has one of the smoothest onboarding experiences in free-to-play gaming in {y}. Here's exactly what to do:</p>
        <ol style="padding-left:20px;color:var(--c-muted);margin-bottom:16px">
          <li style="margin-bottom:8px">Click the download button above and choose your platform</li>
          <li style="margin-bottom:8px">Create a free Gaijin account (takes 60 seconds)</li>
          <li style="margin-bottom:8px">Choose your starting nation (USA recommended for beginners)</li>
          <li style="margin-bottom:8px">Complete the tutorial to earn starter vehicles and Silver Lions</li>
          <li style="margin-bottom:8px">Jump into your first Arcade Battle</li>
        </ol>
        <h2>What You Get for Free</h2>
        <p>Every nation's full vehicle tech tree is available to free players. You progress by earning Research Points (RP) in battles. There is no paywall on any vehicle — premium only speeds up the grind.</p>
        <h2>Minimum Requirements</h2>
        <p>PC: Intel i5, 8GB RAM, GTX 660, 40GB storage. Console: PS4/PS5 or any Xbox One or newer. Mobile: See War Thunder Mobile on the App Store / Google Play.</p>
    """,
    "steam": lambda slug, title, y: f"""
        <h2>War Thunder on Steam in {y}</h2>
        <p>War Thunder is available on Steam as a free download. It's one of the highest-rated free-to-play games on the platform, with tens of thousands of reviews and a "Very Positive" overall rating.</p>
        <h2>Steam vs Gaijin.net Launcher</h2>
        <p>You can play War Thunder through Steam or through the standalone Gaijin.net launcher. Both access the same servers, same account, and same content. The Gaijin launcher is slightly faster to update; Steam offers the convenience of your existing library.</p>
        <h2>Steam System Requirements</h2>
        <p><strong>Minimum:</strong> Windows 7 64-bit, Intel Core i5, 8GB RAM, NVIDIA GeForce GTX 660, 40GB storage.<br>
        <strong>Recommended:</strong> Windows 10/11, Intel i7, 16GB RAM, NVIDIA GeForce GTX 1060, SSD preferred.</p>
        <h2>How to Install via Steam</h2>
        <p>Search "War Thunder" in the Steam store → click "Play Game" (it's free) → wait for download → launch and create your Gaijin account.</p>
    """,
    "console": lambda slug, title, y: f"""
        <h2>War Thunder on Console in {y}</h2>
        <p>War Thunder is fully free on PlayStation 4, PlayStation 5, Xbox One, and Xbox Series X|S. No PS Plus or Xbox Game Pass subscription is required — it's genuinely free, no strings attached.</p>
        <h2>Console-Specific Features</h2>
        <ul>
          <li>Controller support with full button remapping</li>
          <li>PS5 / Xbox Series X run at up to 60fps with faster load times</li>
          <li>Cross-play with PC players enabled by default</li>
          <li>Same account as PC — switch platforms and keep all progress</li>
        </ul>
        <h2>How to Download on Console</h2>
        <p><strong>PlayStation:</strong> Open the PlayStation Store → search "War Thunder" → select Download (price shown as Free).<br>
        <strong>Xbox:</strong> Open the Microsoft Store → search "War Thunder" → select Get (it's free).</p>
        <p>Your first battle is about 10 minutes away from clicking the button above.</p>
    """,
    "hist": lambda slug, title, y: f"""
        <h2>War Thunder's Historical Coverage</h2>
        <p>War Thunder spans from the 1930s biplanes of the interwar period all the way to modern 4th-generation jet fighters and main battle tanks. This makes it uniquely suited for players interested in specific historical eras.</p>
        <h2>Era Coverage</h2>
        <ul>
          <li><strong>1930s–1939:</strong> Biplanes, early tanks, pre-war designs</li>
          <li><strong>WW2 (1939–1945):</strong> The deepest era — thousands of aircraft and tanks from all major nations</li>
          <li><strong>Early Cold War (1945–1960):</strong> Early jets, Korean War era tanks</li>
          <li><strong>Cold War (1960–1980):</strong> Supersonic jets, early guided missiles, MBTs</li>
          <li><strong>Modern (1980–present):</strong> 3rd and 4th gen fighters, reactive armour, top-tier MBTs</li>
        </ul>
        <h2>Historical Accuracy</h2>
        <p>Gaijin builds vehicles from declassified blueprints and historical documents. The community is known for submitting official sources to correct vehicle statistics. No other free game comes close to this level of historical detail.</p>
    """,
    "cross": lambda slug, title, y: f"""
        <h2>Both Games Are Made by Gaijin Entertainment</h2>
        <p>War Thunder and Crossout are both developed and published by Gaijin Entertainment, the Russian-Cypriot studio founded in 2002. Your Gaijin account works in both games.</p>
        <h2>War Thunder vs Crossout at a Glance</h2>
        <div class="tbl-wrap"><table class="compare-table">
        <tr><th>Feature</th><th>War Thunder</th><th>Crossout</th></tr>
        <tr><td>Style</td><td>Historical simulation</td><td>Post-apocalyptic arcade</td></tr>
        <tr><td>Vehicles</td><td>Real historical vehicles</td><td>Fully custom-built</td></tr>
        <tr><td>Modes</td><td>Air + Ground + Naval</td><td>Ground PvP/PvE</td></tr>
        <tr><td>Realism</td><td class="winner">Simulation-grade</td><td>Arcade</td></tr>
        <tr><td>Building</td><td>None</td><td class="winner">Deep crafting system</td></tr>
        </table></div>
        <h2>Which Should You Play?</h2>
        <p>Want historical realism and combined-arms warfare? <strong>War Thunder</strong>. Want to design your own crazy vehicle and blow things up in a post-apocalyptic setting? <strong>Crossout</strong>. Both are free — play both.</p>
    """,
    "value": lambda slug, title, y: f"""
        <h2>The Real Cost of Playing War Thunder in {y}</h2>
        <p>You can download, play, and reach top tier in War Thunder without spending a single cent. The free experience is complete — you get all nations, all branches (air/ground/naval), all game modes, and all maps.</p>
        <h2>Where the Grind Is</h2>
        <p>Reaching top-tier vehicles (Rank VII–VIII) takes 200–500 hours of free play. Premium account or vehicles halve this. Whether that's worth it to you depends on how quickly you want to progress.</p>
        <h2>Value vs Paid Games</h2>
        <p>A paid game like Battlefield 2042 launches at $60–70 and may have smaller, less regularly-updated content than War Thunder. For the price of zero, War Thunder offers more vehicles, more maps, and more active development than most paid titles.</p>
        <h2>Our Verdict</h2>
        <p>War Thunder is worth playing in {y}. Start free, decide after 20 hours whether premium makes sense for you. Most players never spend money and still have hundreds of hours of fun.</p>
    """,
    "tech": lambda slug, title, y: f"""
        <h2>Technical Overview {y}</h2>
        <p>War Thunder uses the custom Dagor Engine, developed in-house by Gaijin. It supports DirectX 11 and 12 on PC, with Vulkan available on Linux. The game is well-optimised for a wide range of hardware.</p>
        <h2>PC System Requirements</h2>
        <div class="tbl-wrap"><table class="compare-table">
        <tr><th>Spec</th><th>Minimum</th><th>Recommended</th></tr>
        <tr><td>OS</td><td>Windows 7 64-bit</td><td>Windows 10/11 64-bit</td></tr>
        <tr><td>CPU</td><td>Intel Core i5-4460</td><td>Intel Core i7-9700K</td></tr>
        <tr><td>RAM</td><td>8 GB</td><td>16 GB</td></tr>
        <tr><td>GPU</td><td>GTX 660 / RX 560</td><td>RTX 2070 / RX 5700 XT</td></tr>
        <tr><td>Storage</td><td>40 GB HDD</td><td>SSD preferred</td></tr>
        </table></div>
        <h2>Performance Tips</h2>
        <ul>
          <li>Lower shadow quality first — biggest single FPS gain</li>
          <li>Disable SSAO and motion blur — minimal visual impact</li>
          <li>Use FSR or DLSS if your GPU supports upscaling</li>
          <li>Set grass to Low — no gameplay disadvantage</li>
        </ul>
    """,
}

def kw_body_html(slug, title_fmt, cat, lang):
    t = LANGUAGES[lang]
    y = YEAR
    title = title_fmt.replace("{y}", y)
    copy_fn = CATEGORY_COPY.get(cat, CATEGORY_COPY["free"])
    body_copy = copy_fn(slug, title, y)
    # Find 8 related keywords in same category
    related = [(s, tf.replace("{y}", y)) for s, tf, _, c in KEYWORDS if c == cat and s != slug][:8]
    related_html = "".join(f'<a href="{pu(lang, s + "/")}">{tl}</a>' for s, tl in related)
    return f"""
<div class="kw-hero">
  <p class="breadcrumb"><a href="{pu(lang)}">Home</a> › {title}</p>
  <h1>{title}</h1>
  <p>100% free on PC, PS4/5 & Xbox — no subscription required.</p>
  <a href="{AFF_URL}" class="btn-primary" target="_blank" rel="nofollow sponsored">{t['cta']}</a>
  <div class="rating-row">
    <div class="rating-box"><div class="score">9.4</div><div class="label">Overall</div></div>
    <div class="rating-box"><div class="score">10</div><div class="label">Free Access</div></div>
    <div class="rating-box"><div class="score">9.5</div><div class="label">Content</div></div>
    <div class="rating-box"><div class="score">9.2</div><div class="label">Realism</div></div>
    <div class="rating-box"><div class="score">9.0</div><div class="label">Community</div></div>
  </div>
</div>
<div class="kw-body">
{body_copy}
<div class="kw-cta-box">
  <h3>Ready to Play?</h3>
  <p>Join 100M+ players. 100% free on all platforms.</p>
  <a href="{AFF_URL}" class="btn-primary" target="_blank" rel="nofollow sponsored">{t['cta']}</a>
</div>
<h2>Related Guides</h2>
<div class="related-links">{related_html}</div>
</div>"""

# ── PAGE BUILDERS ─────────────────────────────────────────────────────────────
def build_homepage(lang):
    t = LANGUAGES[lang]
    y = YEAR

    # Why cards
    why_cards = ""
    for item in t["why"]:
        h, d = item.split("|")
        why_cards += f'<div class="why-card"><h3>{h}</h3><p>{d}</p></div>'

    # FAQ items
    faq_items = ""
    for q, a in t["faq_qs"]:
        faq_items += f'<div class="faq-item"><div class="faq-q">{q}</div><div class="faq-a">{a}</div></div>'

    # Blog preview (first 3)
    blog_cards = ""
    for post in BLOG_POSTS[:3]:
        url = pu(lang, f"blog/{post['slug']}/")
        blog_cards += f"""<div class="blog-card">
          <div class="blog-card-body">
            <h3>{post['title']}</h3>
            <p>{post['desc'][:100]}...</p>
            <a href="{url}">Read more →</a>
          </div></div>"""

    body = f"""
<div class="hero">
  <div class="container">
    <div class="hero-tag">Free to Play — {y}</div>
    <h1>{t['hero1']}<br><span>{t['hero2']}</span></h1>
    <p class="hero-sub">{t['hero_sub']}</p>
    <div class="hero-btns">
      <a href="{AFF_URL}" class="btn-primary" target="_blank" rel="nofollow sponsored">{t['cta']}</a>
      <a href="{pu(lang,'review/')}" class="btn-secondary">Read Review</a>
    </div>
    <div class="stats-bar">
      <div class="stat"><div class="stat-n">2,000+</div><div class="stat-l">Vehicles</div></div>
      <div class="stat"><div class="stat-n">100M+</div><div class="stat-l">Players</div></div>
      <div class="stat"><div class="stat-n">100+</div><div class="stat-l">Maps</div></div>
      <div class="stat"><div class="stat-n">100%</div><div class="stat-l">Free</div></div>
    </div>
  </div>
</div>

<section class="section section-alt">
  <div class="container">
    <h2 class="section-title">{t['feat_title']}</h2>
    <p class="section-sub">Here's why War Thunder has 100M+ registered players in {y}.</p>
    <div class="why-grid">{why_cards}</div>
  </div>
</section>

<section class="section">
  <div class="container">
    <h2 class="section-title">War Thunder vs The Competition</h2>
    <p class="section-sub">How does it stack up against World of Tanks and Crossout?</p>
    <div class="tbl-wrap"><table class="compare-table">
    <tr><th>Feature</th><th>War Thunder</th><th>World of Tanks</th><th>Crossout</th></tr>
    <tr><td>Price</td><td class="winner">Free</td><td class="winner">Free</td><td class="winner">Free</td></tr>
    <tr><td>Vehicles</td><td class="winner">2,000+</td><td>600+</td><td>Custom</td></tr>
    <tr><td>Branches</td><td class="winner">Air+Ground+Naval</td><td class="loser">Tanks only</td><td class="loser">Ground only</td></tr>
    <tr><td>Realism</td><td class="winner">Simulation</td><td>Arcade</td><td>Arcade</td></tr>
    <tr><td>Platforms</td><td class="winner">PC/PS/Xbox</td><td>PC/Console</td><td>PC/PS/Xbox</td></tr>
    <tr><td>Crossplay</td><td class="winner">Yes</td><td>No</td><td>Yes</td></tr>
    </table></div>
  </div>
</section>

<section class="section section-alt">
  <div class="container">
    <h2 class="section-title">Frequently Asked Questions</h2>
    <div class="faq">{faq_items}</div>
  </div>
</section>

<section class="section">
  <div class="container">
    <h2 class="section-title">{t['blog_title']}</h2>
    <p class="section-sub">Guides, tips, and news to help you dominate.</p>
    <div class="blog-grid">{blog_cards}</div>
    <div style="text-align:center;margin-top:32px"><a href="{pu(lang,'blog/')}" class="btn-primary">All Guides →</a></div>
  </div>
</section>

<div style="background:var(--c-primary);padding:48px 20px;text-align:center;color:white">
  <div class="container">
    <h2 style="font-family:'Oswald',sans-serif;font-size:2rem;margin-bottom:8px">Ready to Play for Free?</h2>
    <p style="opacity:.85;margin-bottom:24px;max-width:500px;margin-left:auto;margin-right:auto">Join 100M+ players. No subscription. No hidden fees. Just download and play.</p>
    <a href="{AFF_URL}" class="btn-primary" style="background:var(--c-accent);color:var(--c-dark)" target="_blank" rel="nofollow sponsored">{t['dl']} — {SITE_NAME}</a>
  </div>
</div>"""

    schema = videogame_schema() + faq_schema(t["faq_qs"]) + hreflang_tags("", list(LANGUAGES.keys()))
    return page_shell(lang, f"Best Free Military Game {y}", t["meta_home"], pu(lang), body, schema=schema)

def build_review(lang):
    t = LANGUAGES[lang]
    y = YEAR
    body = f"""
<div class="post-hero">
  <div class="container">
    <h1>{t['review_title']}</h1>
    <p style="opacity:.8">Last updated: {TODAY}</p>
  </div>
</div>
<div class="post-body">
<div class="review-score">
  <div class="score-card"><div class="score">9.4</div><div class="label">Overall</div></div>
  <div class="score-card"><div class="score">10</div><div class="label">Value</div></div>
  <div class="score-card"><div class="score">9.5</div><div class="label">Content</div></div>
  <div class="score-card"><div class="score">9.2</div><div class="label">Realism</div></div>
  <div class="score-card"><div class="score">9.0</div><div class="label">Community</div></div>
  <div class="score-card"><div class="score">8.8</div><div class="label">Economy</div></div>
</div>
<h2>Overview</h2>
<p>War Thunder is a free-to-play military MMO developed by Gaijin Entertainment. Since its 2012 release it has grown into the world's largest vehicle combat game, with over 2,000 historically accurate aircraft, tanks, helicopters, and naval vessels spanning multiple nations and eras.</p>
<h2>Gameplay</h2>
<p>Three game modes cater to every skill level: Arcade Battles (simplified, beginner-friendly), Realistic Battles (full ballistics, most popular), and Simulator Battles (full cockpit immersion). Ground Forces, Aviation, and Naval Forces can all be played independently or together in combined-arms battles.</p>
<h2>Free-to-Play Fairness</h2>
<p>War Thunder's economy is the most common criticism. The tech tree grind to top tier is long without premium. However, skill carries players far in the free experience, and Gaijin regularly runs events that award premium vehicles for free.</p>
<h2>Graphics & Performance</h2>
<p>Running on the proprietary Dagor Engine, War Thunder looks excellent on high settings in {y}. PS5 and Xbox Series X run at 60fps. Low-end PCs can play at reduced settings with surprisingly decent performance.</p>
<h2>Verdict</h2>
<p>For a free game, War Thunder offers content that rivals and often surpasses paid alternatives. The breadth of vehicles and the quality of the physics simulation are unmatched at any price. If you enjoy military vehicles and want a free, deep, regularly updated game — download it.</p>
<div style="text-align:center;margin:32px 0">
  <a href="{AFF_URL}" class="btn-primary" target="_blank" rel="nofollow sponsored">{t['dl']} Free</a>
</div>
</div>"""
    schema = article_schema(t["review_title"], f"Full War Thunder review {y}.", TODAY, pu(lang, "review/"))
    return page_shell(lang, t["review_title"], f"Full War Thunder review {y}. Gameplay, economy, verdict.", pu(lang, "review/"), body, schema=schema)

def build_compare(lang):
    t = LANGUAGES[lang]
    y = YEAR
    body = f"""
<div class="post-hero">
  <div class="container">
    <h1>{t['compare_title']}</h1>
    <p style="opacity:.8">Full comparison — {y}</p>
  </div>
</div>
<div class="post-body">
<div class="tbl-wrap"><table class="compare-table">
<tr><th>Feature</th><th>War Thunder</th><th>World of Tanks</th><th>Crossout</th></tr>
<tr><td>Price</td><td class="winner">Free</td><td class="winner">Free</td><td class="winner">Free</td></tr>
<tr><td>Vehicles</td><td class="winner">2,000+</td><td>600+</td><td>Custom builds</td></tr>
<tr><td>Branches</td><td class="winner">Air + Ground + Naval</td><td class="loser">Tanks only</td><td class="loser">Ground only</td></tr>
<tr><td>Realism</td><td class="winner">Simulation ballistics</td><td>HP system</td><td>Arcade</td></tr>
<tr><td>Platforms</td><td class="winner">PC/PS4/PS5/Xbox</td><td>PC/Console</td><td>PC/PS/Xbox</td></tr>
<tr><td>Crossplay</td><td class="winner">Yes</td><td class="loser">No</td><td class="winner">Yes</td></tr>
<tr><td>Naval Combat</td><td class="winner">Yes</td><td class="loser">No</td><td class="loser">No</td></tr>
<tr><td>Air Combat</td><td class="winner">Yes</td><td class="loser">No</td><td class="loser">No</td></tr>
<tr><td>Historical Accuracy</td><td class="winner">Extremely high</td><td>Moderate</td><td class="loser">None (fictional)</td></tr>
<tr><td>Player Count</td><td class="winner">100M+ registered</td><td>~90M registered</td><td>~10M registered</td></tr>
</table></div>
<h2>Verdict</h2>
<p>All three games are free and worth trying. War Thunder wins for combined-arms realism and content depth. World of Tanks wins for a simpler, purely tank-focused arcade experience. Crossout wins for vehicle creativity and post-apocalyptic atmosphere. Start with War Thunder — if you want tanks-only or a builder game, the others are waiting.</p>
<div style="text-align:center;margin:32px 0">
  <a href="{AFF_URL}" class="btn-primary" target="_blank" rel="nofollow sponsored">Try War Thunder Free</a>
</div>
</div>"""
    return page_shell(lang, t["compare_title"], f"War Thunder vs World of Tanks vs Crossout {y}: which free game wins?", pu(lang, "compare/"), body)

def build_blog_index(lang):
    t = LANGUAGES[lang]
    cards = ""
    for post in BLOG_POSTS:
        url = pu(lang, f"blog/{post['slug']}/")
        cards += f"""<div class="blog-card">
          <div class="blog-card-body">
            <h3><a href="{url}" style="color:inherit">{post['title']}</a></h3>
            <p>{post['desc']}</p>
            <a href="{url}">Read more →</a>
          </div></div>"""
    body = f"""
<div class="post-hero"><div class="container">
  <h1>{t['blog_title']}</h1>
  <p style="opacity:.8">{len(BLOG_POSTS)} guides and reviews</p>
</div></div>
<div class="section"><div class="container">
  <div class="blog-grid">{cards}</div>
</div></div>"""
    return page_shell(lang, t["blog_title"], f"War Thunder guides, tips and news {YEAR}.", pu(lang, "blog/"), body)

def build_blog_post(lang, post):
    t = LANGUAGES[lang]
    url = pu(lang, f"blog/{post['slug']}/")
    body = f"""
<div class="post-hero"><div class="container">
  <p class="breadcrumb" style="color:rgba(255,255,255,.6)"><a href="{pu(lang)}" style="color:rgba(255,255,255,.6)">Home</a> › <a href="{pu(lang,'blog/')}" style="color:rgba(255,255,255,.6)">Blog</a> › {post['title']}</p>
  <h1>{post['title']}</h1>
  <p style="opacity:.7">{post['date']}</p>
</div></div>
<div class="post-body">{post['body']}
<div style="text-align:center;margin:32px 0">
  <a href="{AFF_URL}" class="btn-primary" target="_blank" rel="nofollow sponsored">{t['cta']}</a>
</div>
</div>"""
    schema = article_schema(post["title"], post["desc"], post["date"], url)
    return page_shell(lang, post["title"], post["desc"], url, body, schema=schema)

def build_keyword_page(lang, slug, title_fmt, meta_fmt, cat):
    t = LANGUAGES[lang]
    y = YEAR
    title = title_fmt.replace("{y}", y)
    meta = meta_fmt.replace("{y}", y)
    url = pu(lang, f"{slug}/")
    bc_schema = breadcrumb_schema([("Home", pu(lang)), (title, url)])
    faq_qs = [
        (f"Is {title} available in {y}?", f"Yes — War Thunder is a top option for {title.lower()}. It's 100% free on PC, PS4/5, and Xbox."),
        ("Do I need to pay anything?", "No. War Thunder is completely free to download and play. Optional premium content exists but is never required."),
        ("What platforms can I play on?", "PC (Steam & Gaijin.net), PlayStation 4, PlayStation 5, Xbox One, and Xbox Series X|S."),
    ]
    schema = bc_schema + faq_schema(faq_qs)
    body = kw_body_html(slug, title_fmt, cat, lang)
    return page_shell(lang, title, meta, url, body, schema=schema)

def build_privacy(lang="en"):
    t = LANGUAGES[lang]
    body = f"""
<div class="post-hero"><div class="container"><h1>{t['privacy_title']}</h1></div></div>
<div class="post-body">
<p>Last updated: {TODAY}</p>
<h2>Information We Collect</h2>
<p>This website does not collect personal information beyond standard web server logs (IP address, browser type, pages visited). We do not use cookies beyond those strictly necessary for site functionality.</p>
<h2>Third-Party Links</h2>
<p>This site contains affiliate links to Gaijin Entertainment via the Gaijin Affiliate Program. When you click these links and sign up for War Thunder, we may earn a commission at no extra cost to you. We are not responsible for the privacy practices of linked sites.</p>
<h2>Analytics</h2>
<p>We may use privacy-preserving analytics to understand aggregate traffic patterns. No personally identifiable information is stored.</p>
<h2>Contact</h2>
<p>For privacy questions, contact us via the GitHub repository linked in the footer.</p>
</div>"""
    return page_shell(lang, t["privacy_title"], "Privacy policy for WarThunder Guide.", pu(lang, "privacy/"), body)

def build_terms(lang="en"):
    t = LANGUAGES[lang]
    body = f"""
<div class="post-hero"><div class="container"><h1>{t['terms_title']}</h1></div></div>
<div class="post-body">
<p>Last updated: {TODAY}</p>
<h2>Use of This Site</h2>
<p>This website provides information and reviews about War Thunder, a free-to-play game by Gaijin Entertainment. Content is provided for informational purposes only.</p>
<h2>Affiliate Disclosure</h2>
<p>We participate in the Gaijin Entertainment affiliate program. Links marked with "rel=nofollow sponsored" are affiliate links. We earn a commission when you sign up via these links at no additional cost to you.</p>
<h2>Accuracy</h2>
<p>We strive to keep information accurate and up to date. Game details, pricing, and features may change. Always verify current information on the official War Thunder website.</p>
<h2>Limitation of Liability</h2>
<p>This site is not affiliated with Gaijin Entertainment. War Thunder® is a trademark of Gaijin Entertainment. We are not liable for any decisions made based on information on this site.</p>
</div>"""
    return page_shell(lang, t["terms_title"], "Terms of use for WarThunder Guide.", pu(lang, "terms/"), body)

def build_404():
    body = """
<div style="text-align:center;padding:100px 20px">
  <h1 style="font-family:'Oswald',sans-serif;font-size:4rem;color:var(--c-primary)">404</h1>
  <p style="font-size:1.2rem;margin:16px 0 32px">Page not found. Head back to the front line.</p>
  <a href="/" class="btn-primary">Back to Home</a>
</div>"""
    return page_shell("en", "Page Not Found", "Page not found.", f"{SITE_URL}/404.html", body)

# ── SITEMAP & ROBOTS ──────────────────────────────────────────────────────────
def build_sitemap(urls):
    items = "\n".join(
        f"  <url><loc>{u}</loc><lastmod>{TODAY}</lastmod><changefreq>weekly</changefreq><priority>{p}</priority></url>"
        for u, p in urls
    )
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{items}
</urlset>"""

def build_robots():
    return f"""User-agent: *
Allow: /
Crawl-delay: 0

User-agent: Googlebot
Crawl-delay: 0

Sitemap: {SITE_URL}/sitemap.xml
"""

def build_llms_txt(page_count):
    lang_lines = "\n".join(f"- {lc} ({d['name']}): {pu(lc)}" for lc, d in LANGUAGES.items())
    blog_lines = "\n".join(f"- [{p['title']}]({pu('en', 'blog/' + p['slug'] + '/')})" for p in BLOG_POSTS)
    kw_lines = "\n".join(f"- [{s}]({pu('en', s + '/')})" for s, *_ in KEYWORDS[:30])
    return f"""# {SITE_NAME}

> {SITE_NAME} is a War Thunder affiliate guide site. We help players discover, download, and get started with War Thunder (free-to-play military MMO by Gaijin Entertainment) across PC, PS4/5, and Xbox.

Updated: {TODAY} | Pages: {page_count} | Languages: {len(LANGUAGES)} | Keywords: {len(KEYWORDS)}

## Site
- URL: {SITE_URL}/
- Affiliate: {AFF_URL}
- Niche: Free-to-play military games → War Thunder
- Target markets: Australia, Canada, France, Germany, South Korea, New Zealand, UK, USA

## About War Thunder
War Thunder is a free-to-play military MMO by Gaijin Entertainment (est. 2012).
- Platforms: PC (Steam & Gaijin.net), PS4, PS5, Xbox One, Xbox Series X/S
- Price: 100% free (optional premium, not pay-to-win)
- Vehicles: 2,000+ aircraft, tanks, helicopters, naval vessels
- Players: 100M+ registered worldwide
- Download: {AFF_URL}

## Languages
{lang_lines}

## Core Pages
- [Home]({pu('en')}): Hero, stats, features, comparison table, FAQ, blog
- [Review]({pu('en','review/')}): Full {YEAR} review
- [Compare]({pu('en','compare/')}): War Thunder vs WoT vs Crossout
- [Blog]({pu('en','blog/')}): {len(BLOG_POSTS)} guides and reviews
- [Privacy]({pu('en','privacy/')}): Privacy policy
- [Terms]({pu('en','terms/')}): Terms of use

## Blog Posts ({len(BLOG_POSTS)})
{blog_lines}

## Keyword Pages (first 30 of {len(KEYWORDS)})
{kw_lines}

## Technical
- Built: {TODAY} | Generator: build.py v4.0
- Hosting: GitHub Pages
- Schema: VideoGame, FAQPage, BreadcrumbList, Article
- Hreflang: en, fr, de, ko + x-default
- Sitemaps: {SITE_URL}/sitemap.xml

## Crawl Policy
All crawlers welcome. Affiliate links tagged rel="nofollow sponsored".
"""

# ── MAIN BUILD ────────────────────────────────────────────────────────────────
def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()

    urls = []
    count = 0

    def w(path, content, priority="0.7"):
        nonlocal count
        write(OUT / path, content)
        urls.append((f"{SITE_URL}/{path}".rstrip("/index.html") + "/", priority))
        count += 1
        if count % 50 == 0:
            print(f"  {count} pages built...")

    # Core pages
    for lang in LANGUAGES:
        prefix = f"{lang}/" if lang != "en" else ""
        w(f"{prefix}index.html", build_homepage(lang), "1.0")
        w(f"{prefix}review/index.html", build_review(lang), "0.9")
        w(f"{prefix}compare/index.html", build_compare(lang), "0.9")
        w(f"{prefix}blog/index.html", build_blog_index(lang), "0.8")

        # Blog posts
        for post in BLOG_POSTS:
            w(f"{prefix}blog/{post['slug']}/index.html", build_blog_post(lang, post), "0.7")

        # Keyword pages
        for slug, title_fmt, meta_fmt, cat in KEYWORDS:
            w(f"{prefix}{slug}/index.html",
              build_keyword_page(lang, slug, title_fmt, meta_fmt, cat), "0.6")

    # Utility pages
    write(OUT / "privacy" / "index.html", build_privacy("en"))
    write(OUT / "terms" / "index.html", build_terms("en"))
    write(OUT / "404.html", build_404())

    # Sitemap, robots, llms.txt
    write(OUT / "sitemap.xml", build_sitemap(urls))
    write(OUT / "robots.txt", build_robots())
    write(OUT / "llms.txt", build_llms_txt(count))

    print(f"\n✅ Build complete: {count} pages → ./{OUT}/")
    print(f"   Langs: {len(LANGUAGES)} | Keywords: {len(KEYWORDS)} | Blog: {len(BLOG_POSTS)}")
    print(f"   Sitemap: {SITE_URL}/sitemap.xml")
    print(f"   llms.txt: {SITE_URL}/llms.txt")

if __name__ == "__main__":
    main()
