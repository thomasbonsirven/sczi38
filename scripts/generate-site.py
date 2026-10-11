#!/usr/bin/env python3
"""Génère les pages HTML statiques du site SCZI. Aucune étape de build n'est requise à la publication."""
from pathlib import Path

ROOT = Path("/workspace")
SITE = "https://thomasbonsirven.github.io/sczi38"
ASSET_V = "20261010e"
PHONE = "04 38 70 03 94"
PHONE_TEL = "+33438700394"
STREET = "4290 route Napoléon"
LOCALITY = "Brié-et-Angonnes"
POSTAL = "38320"
ADDRESS = f"{STREET}, {POSTAL} {LOCALITY}"
MAPS_URL = "https://www.google.com/maps/search/?api=1&query=4290+route+Napol%C3%A9on%2C+38320+Bri%C3%A9-et-Angonnes"
SIRET = "75106621800023"
RCS = "Grenoble B 751 066 218"


def asset(prefix, path):
    url = f"{prefix}assets/{path}"
    if path.startswith("css/") or path.startswith("js/"):
        return f"{url}?v={ASSET_V}"
    return url


SERVICE_LINKS = [
    ("toiture", "Toiture", "services/toiture.html"),
    ("isolation-sarking", "Isolation sarking", "services/isolation-sarking.html"),
    ("velux", "Velux", "services/velux.html"),
    ("isolation-combles", "Combles perdus", "services/isolation-combles.html"),
    ("zinguerie", "Zinguerie", "services/zinguerie.html"),
]
SERVICE_KEYS = {"services"} | {key for key, _, _ in SERVICE_LINKS}


def nav(prefix, current):
    def item(key, label, href):
        cur = ' aria-current="page"' if current == key else ""
        return f'<li><a href="{href}"{cur}>{label}</a></li>'

    hub_cur = ' aria-current="page"' if current == "services" else ""
    parent_class = "has-submenu"
    if current in SERVICE_KEYS:
        parent_class += " is-current"
    children = []
    for key, label, path in SERVICE_LINKS:
        cur = ' aria-current="page"' if current == key else ""
        children.append(f'            <li><a href="{prefix}{path}"{cur}>{label}</a></li>')
    services = f"""<li class="{parent_class}">
          <div class="submenu-pair">
            <a href="{prefix}services/index.html"{hub_cur}>Services</a>
            <button type="button" class="submenu-toggle" aria-expanded="false" aria-controls="submenu-services" aria-haspopup="true" aria-label="Afficher le sous-menu Services">
              <svg class="nav-chevron" viewBox="0 0 12 8" width="12" height="8" aria-hidden="true" focusable="false"><path d="M1 1.5 6 6.5 11 1.5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>
            </button>
          </div>
          <ul class="submenu" id="submenu-services">
{chr(10).join(children)}
          </ul>
        </li>"""
    return "\n        ".join([
        item("index.html", "Accueil", f"{prefix}index.html"),
        item("a-propos.html", "L’entreprise", f"{prefix}a-propos.html"),
        services,
        item("realisations.html", "Réalisations", f"{prefix}realisations.html"),
        item("zone-intervention.html", "Zone d’intervention", f"{prefix}zone-intervention.html"),
        item("contact.html", "Devis", f"{prefix}contact.html"),
    ])


def head(title, description, canonical, image, prefix, extra=""):
    og_img = f"{SITE}/{image}"
    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <meta name="robots" content="index,follow">
  <link rel="canonical" href="{canonical}">
  <meta property="og:locale" content="fr_FR">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="SCZI — Schubert Couverture Zinguerie Isolation">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{og_img}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{description}">
  <meta name="theme-color" content="#c8102e">
  <link rel="icon" href="{prefix}favicon.png" type="image/png">
  <link rel="apple-touch-icon" href="{asset(prefix, 'img/logo/logo-icon.png')}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,650&family=Source+Sans+3:wght@400;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{asset(prefix, 'css/styles.css')}">
  {extra}
</head>"""


SCHEMA = f"""<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "RoofingContractor",
  "name": "Schubert Couverture Zinguerie Isolation",
  "alternateName": ["SCZI", "SCZI Toiture", "SCHUBERT COUVERTURE ZINGUERIE"],
  "url": "{SITE}/",
  "telephone": "{PHONE_TEL}",
  "founder": {{
    "@type": "Person",
    "name": "SCHUBERT Eric"
  }},
  "address": {{
    "@type": "PostalAddress",
    "streetAddress": "{STREET}",
    "addressLocality": "{LOCALITY}",
    "postalCode": "{POSTAL}",
    "addressRegion": "Isère",
    "addressCountry": "FR"
  }},
  "areaServed": [
    {{"@type": "City", "name": "Noyarey"}},
    {{"@type": "City", "name": "Brié-et-Angonnes"}},
    {{"@type": "City", "name": "Grenoble"}},
    {{"@type": "City", "name": "Crolles"}},
    {{"@type": "AdministrativeArea", "name": "Isère"}}
  ],
  "knowsAbout": ["réfection de toiture", "isolation de toiture", "sarking", "combles perdus", "zinguerie", "charpente", "fenêtres de toit Velux"],
  "hasOfferCatalog": {{
    "@type": "OfferCatalog",
    "name": "Travaux de toiture et d'isolation",
    "itemListElement": [
      {{"@type": "Offer", "itemOffered": {{"@type": "Service", "name": "Toiture"}}}},
      {{"@type": "Offer", "itemOffered": {{"@type": "Service", "name": "Isolation toiture extérieur / sarking"}}}},
      {{"@type": "Offer", "itemOffered": {{"@type": "Service", "name": "Isolation combles perdus"}}}},
      {{"@type": "Offer", "itemOffered": {{"@type": "Service", "name": "Installation Velux"}}}},
      {{"@type": "Offer", "itemOffered": {{"@type": "Service", "name": "Zinguerie"}}}}
    ]
  }}
}}
</script>"""


def header(prefix, current):
    return f"""<body>
  <a class="skip-link" href="#contenu">Aller au contenu</a>
  <header class="site-header">
    <div class="topbar">
      <div class="wrap">
        <span>Artisan couvreur à Brié-et-Angonnes — Isère (38)</span>
        <span>
          <a href="tel:{PHONE_TEL}">{PHONE}</a>
          · {ADDRESS}
        </span>
      </div>
    </div>
    <div class="wrap nav-row">
      <a class="brand" href="{prefix}index.html">
        <img src="{asset(prefix, 'img/logo/logo.png')}" width="827" height="472" alt="SCZI Toiture">
        <span class="brand-text">
          <strong>SCZI</strong>
          <span>Couverture · Zinguerie · Isolation</span>
        </span>
      </a>
      <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="menu-principal" aria-label="Ouvrir le menu">
        <span></span><span></span><span></span>
      </button>
      <nav class="site-nav" id="menu-principal" aria-label="Navigation principale">
        <ul>
        {nav(prefix, current)}
        </ul>
      </nav>
      <a class="btn btn-primary nav-cta" href="{prefix}contact.html">Demander un devis</a>
    </div>
  </header>
  <main id="contenu">"""


def footer(prefix):
    return f"""  </main>
  <footer class="site-footer">
    <div class="wrap footer-grid">
      <div>
        <img src="{asset(prefix, 'img/logo/logo.png')}" width="180" alt="SCZI Toiture" style="width:140px;background:#fff;border-radius:8px;padding:6px;">
        <p>Schubert Couverture Zinguerie Isolation — réfection de toiture, isolation et zinguerie à Brié-et-Angonnes (Isère).</p>
        <p>Gérant : SCHUBERT Eric</p>
      </div>
      <div>
        <h3>Services</h3>
        <ul>
          <li><a href="{prefix}services/toiture.html">Toiture</a></li>
          <li><a href="{prefix}services/isolation-sarking.html">Isolation sarking</a></li>
          <li><a href="{prefix}services/isolation-combles.html">Combles perdus</a></li>
          <li><a href="{prefix}services/velux.html">Velux</a></li>
          <li><a href="{prefix}services/zinguerie.html">Zinguerie</a></li>
        </ul>
      </div>
      <div>
        <h3>Entreprise</h3>
        <ul>
          <li><a href="{prefix}a-propos.html">L’entreprise</a></li>
          <li><a href="{prefix}realisations.html">Réalisations</a></li>
          <li><a href="{prefix}zone-intervention.html">Zone d’intervention</a></li>
          <li><a href="{prefix}contact.html">Contact / devis</a></li>
          <li><a href="{prefix}mentions-legales.html">Mentions légales</a></li>
        </ul>
      </div>
      <div>
        <h3>Coordonnées</h3>
        <p><a href="{MAPS_URL}" rel="noopener noreferrer">{ADDRESS}</a></p>
        <p><a href="tel:{PHONE_TEL}">{PHONE}</a></p>
        <p>SIRET {SIRET}<br>RCS {RCS}</p>
      </div>
    </div>
    <div class="wrap legal">
      <p>© SCZI — Schubert Couverture Zinguerie Isolation</p>
      <p class="footer-credits"><a href="{prefix}credits.html">Crédits & informations</a></p>
    </div>
  </footer>
  <div class="mobile-cta">
    <a class="btn btn-ghost" href="tel:{PHONE_TEL}">Appeler</a>
    <a class="btn btn-primary" href="{prefix}contact.html">Devis</a>
  </div>
  <div class="lightbox" data-lightbox aria-hidden="true" role="dialog" aria-label="Agrandissement photo">
    <button type="button" data-close-lightbox aria-label="Fermer">×</button>
    <img alt="">
  </div>
  <script src="{asset(prefix, 'js/main.js')}"></script>
</body>
</html>"""


def page(path, title, description, current, body, prefix="./", image="assets/img/chantiers/lucarne-pendant.jpg", extra=""):
    canonical = f"{SITE}/{'' if path == 'index.html' else path}"
    if not canonical.endswith(".html") and path != "index.html":
        canonical = canonical.rstrip("/") + "/"
    html = (
        head(title, description, canonical if path != "index.html" else f"{SITE}/", image, prefix, extra)
        + header(prefix, current)
        + body
        + footer(prefix)
    )
    out = ROOT / path
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print("wrote", path)


# ---------- PAGES ----------

page(
    "index.html",
    "SCZI Toiture — Couverture, isolation et zinguerie à Brié-et-Angonnes (38)",
    "Entreprise spécialisée dans la réfection de toiture, l’isolation de toiture et de combles, implantée à Brié-et-Angonnes dans l’Isère. Intervention de Noyarey à Crolles, via Grenoble.",
    "index.html",
    extra=SCHEMA,
    body=f"""
  <section class="hero">
    <img class="hero-bg" src="assets/img/chantiers/lucarne-pendant.jpg" width="900" height="1200" alt="Pose de zinc et de tuiles écailles en toiture">
    <div class="wrap hero-inner">
      <p class="kicker" style="color:#ffb4bc">Schubert Couverture Zinguerie Isolation</p>
      <p class="hero-trust"><strong>Qualibat RGE depuis 2016</strong> Entreprise 100&nbsp;% RGE</p>
      <h1>La toiture, l’isolation et le zinc, travaillés pour le climat de l’Isère.</h1>
      <p class="lede">Notre entreprise spécialisée dans la réfection de toiture, l’isolation de toiture et de comble non aménageable est implantée à Brié-et-Angonnes, dans l’Isère.</p>
      <div class="hero-actions">
        <a class="btn btn-primary" href="contact.html">Demander un devis</a>
        <a class="btn btn-light" href="realisations.html">Voir les chantiers</a>
      </div>
      <div class="hero-facts">
        <div><strong>20 ans+</strong><span>d’expérience en zinguerie, charpente, sarking et Velux</span></div>
        <div><strong>Brié-et-Angonnes</strong><span>siège en Isère (38), de Noyarey à Crolles</span></div>
        <div><strong>DTU / CSTB</strong><span>réponses adaptées aux tuiles, ardoise, bac acier, joints debout</span></div>
        <div><strong>Eric Schubert</strong><span>gérant, sur le chantier comme au devis</span></div>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <p class="kicker">Métiers</p>
      <h2>Quatre savoir-faire de toiture, un seul interlocuteur.</h2>
      <p class="lede">Couverture, isolation par l’extérieur, combles perdus, Velux et zinguerie : un seul interlocuteur pour le toit.</p>
      <div class="grid-2" style="margin-top:1.5rem">
        <article class="card"><a class="stretched" href="services/toiture.html">
          <img src="assets/img/chantiers/lucarne-apres.jpg" alt="Lucarne en tuiles écailles et zinc">
          <div class="card-body"><span class="tag">Couverture</span><h3>Toiture neuve et réfection</h3><p>Tuiles, tuiles écailles, bac acier, ardoise ou joints debout. Habillage de lucarnes, charpente associée.</p></div></a></article>
        <article class="card"><a class="stretched" href="services/isolation-sarking.html">
          <img src="assets/img/chantiers/sarking-1054.jpg" alt="Isolation de toiture par l’extérieur">
          <div class="card-body"><span class="tag">Isolation</span><h3>Sarking et isolation par l’extérieur</h3><p>Isoler lors d’une réfection sans démonter les plafonds en rampant, ni perdre de hauteur sous toiture.</p></div></a></article>
        <article class="card"><a class="stretched" href="services/isolation-combles.html">
          <img src="assets/img/stock/isolation-laine.jpg" alt="Isolant en laine">
          <div class="card-body"><span class="tag">Combles</span><h3>Combles perdus soufflés</h3><p>Isolation par projection de laine de roche, pour les volumes trop bas pour être aménagés.</p></div></a></article>
        <article class="card"><a class="stretched" href="services/velux.html">
          <img src="assets/img/chantiers/velux-apres.jpg" alt="Fenêtre de toit Velux">
          <div class="card-body"><span class="tag">Lumière</span><h3>Pose et remplacement de Velux</h3><p>Du simple remplacement au jumelage, jusqu’à la transformation d’un débarras en chambre.</p></div></a></article>
      </div>
      <p style="margin-top:1.2rem"><a href="services/zinguerie.html">Zinguerie : chéneaux, abergements, rives et joints debout →</a></p>
    </div>
  </section>

  <section class="section section-alt">
    <div class="wrap split">
      <div>
        <p class="kicker">Pourquoi SCZI</p>
        <h2>Un artisan local, des toitures pensées pour le massif.</h2>
        <p>Que votre toiture soit en tuiles, en tuiles écailles, en bac acier, en ardoise ou en joints debout, nous vous répondons de manière adaptée et personnalisée, en respectant les normes DTU et CSTB.</p>
        <p>Nous effectuons des habillages et abergements de cheminée, la pose de chéneaux, des habillages de planches de rive et de bandeaux. Nous assurons également la pose et le remplacement de vos fenêtres de toit Velux.</p>
        <p><strong>Faites des économies de chauffage</strong> en pensant à l’isolation des combles non aménageables par laine de roche soufflée, ou à l’isolation des combles aménagés par l’extérieur.</p>
        <div class="trust" style="margin-top:1rem">
          <div class="trust-item"><span class="num">01</span><div><h3>Un gérant identifiable</h3><p>SCHUBERT Eric, gérant. Le visage du chantier, pas un standard anonyme.</p></div></div>
          <div class="trust-item"><span class="num">02</span><div><h3>Des toits en Isère</h3><p>Lucarnes, sarking, Velux : des chantiers à Eybens, Saint-Nazaire et dans l’agglomération grenobloise.</p></div></div>
        </div>
      </div>
      <figure>
        <img src="assets/img/chantiers/lucarne-pendant.jpg" alt="Pose de zinc et de tuiles écailles sur une lucarne">
      </figure>
    </div>
  </section>

  <section class="section section-qualibat" id="qualibat-rge">
    <div class="wrap">
      <p class="kicker">Qualibat · RGE</p>
      <h2>10 ans de certification Qualibat, entreprise 100&nbsp;% RGE.</h2>
      <p class="lede">SCZI est certifiée Qualibat depuis 2016, renouvelée jusqu’en 2026 : <strong>10 ans de performance et de qualité</strong> sur les chantiers. L’entreprise est <strong>100&nbsp;% RGE</strong> (Reconnu Garant de l’Environnement).</p>
      <div class="qualibat-highlights">
        <p><strong>2016 – 2026</strong><span>Dix ans de certification Qualibat</span></p>
        <p><strong>100&nbsp;% RGE</strong><span>Toute l’activité est reconnue RGE</span></p>
        <p><strong>Contrôle</strong><span>Qualification suivie, travaux dans les règles de l’art</span></p>
      </div>
      <h3 class="qualibat-frieze-title">Macarons Qualibat RGE</h3>
      <div class="badge-frieze" role="list">
        <figure role="listitem">
          <img src="assets/img/badges/rge-2016.jpg" width="1489" height="2048" alt="Macaron Qualibat RGE, année 2016">
          <figcaption>2016</figcaption>
        </figure>
        <figure role="listitem">
          <img src="assets/img/badges/rge.png" width="340" height="494" alt="Macaron Qualibat RGE, années 2016 et 2017">
          <figcaption>2016–2017</figcaption>
        </figure>
      </div>
      <h3>Ce que le RGE change pour vous</h3>
      <p>Un artisan RGE, c’est la condition pour demander les aides publiques à la rénovation énergétique. Les montants, plafonds et pièces à fournir <strong>dépendent du foyer et des règles en vigueur</strong> au moment du chantier : nous n’affichons pas de chiffres qui pourraient dater.</p>
      <ul class="rge-aids">
        <li>
          <h4>MaPrimeRénov’</h4>
          <p>Aide de l’État pour des travaux d’amélioration énergétique, sous conditions de ressources et de projet.</p>
        </li>
        <li>
          <h4>Primes CEE</h4>
          <p>Certificats d’économies d’énergie : une prime versée par les fournisseurs d’énergie, selon les gestes réalisés.</p>
        </li>
        <li>
          <h4>Éco-prêt à taux zéro</h4>
          <p>Emprunt sans intérêts pour financer des travaux de rénovation énergétique éligibles.</p>
        </li>
        <li>
          <h4>TVA 5,5&nbsp;%</h4>
          <p>Taux réduit sur les travaux de rénovation énergétique, lorsque les conditions fiscales sont réunies.</p>
        </li>
        <li>
          <h4>Travail qualifié et contrôlé</h4>
          <p>Le signe RGE atteste d’une entreprise formée, suivie, et d’un chantier déclaré selon le référentiel.</p>
        </li>
        <li>
          <h4>Conformité aux normes</h4>
          <p>Les ouvrages restent réalisés dans le respect des DTU et des avis CSTB applicables au support.</p>
        </li>
      </ul>
    </div>
  </section>

  <section class="section section-alt">
    <div class="wrap">
      <p class="kicker">Chantiers</p>
      <h2>Quelques toits déjà documentés.</h2>
      <div class="gallery" data-gallery>
        <a href="assets/img/chantiers/lucarne-avant.jpg"><img src="assets/img/chantiers/lucarne-avant.jpg" alt="Réfection de toiture et lucarne — avant"></a>
        <a href="assets/img/chantiers/lucarne-apres.jpg"><img src="assets/img/chantiers/lucarne-apres.jpg" alt="Réfection de toiture et lucarne — après"></a>
        <a href="assets/img/chantiers/velux-avant.jpg"><img src="assets/img/chantiers/velux-avant.jpg" alt="Installation Velux — avant"></a>
        <a href="assets/img/chantiers/velux-apres.jpg"><img src="assets/img/chantiers/velux-apres.jpg" alt="Installation Velux — après"></a>
        <a href="assets/img/chantiers/sarking-0685.jpg"><img src="assets/img/chantiers/sarking-0685.jpg" alt="Isolation sarking, laine de bois entre chevrons"></a>
        <a href="assets/img/chantiers/eybens-avant.jpg"><img src="assets/img/chantiers/eybens-avant.jpg" alt="Toiture de maison à Eybens — avant travaux"></a>
      </div>
      <p style="margin-top:1rem"><a class="btn btn-ghost" href="realisations.html">Galerie complète</a></p>
    </div>
  </section>

  <section class="section section-dark">
    <div class="wrap split">
      <div>
        <p class="kicker">Devis</p>
        <h2>Expliquez le toit, on revient vers vous.</h2>
        <p>Décrivez le bâtiment, le lieu des travaux et vos besoins : nous revenons vers vous.</p>
        <a class="btn btn-primary" href="contact.html">Ouvrir le formulaire</a>
      </div>
      <div>
        <p><a href="tel:{PHONE_TEL}" style="color:#fff;font-size:1.6rem;font-family:var(--font-serif);text-decoration:none">{PHONE}</a></p>
        <p>{ADDRESS}</p>
      </div>
    </div>
  </section>
""",
)

page(
    "a-propos.html",
    "L’entreprise SCZI — Schubert Couverture Zinguerie Isolation",
    "SCZI, dirigée par SCHUBERT Eric, est implantée à Brié-et-Angonnes (38320). Plus de 20 ans d’expérience en toiture, isolation, zinguerie, charpente et Velux.",
    "a-propos.html",
    body=f"""
  <section class="page-hero wrap">
    <p class="kicker">L’entreprise</p>
    <h1>Schubert Couverture Zinguerie Isolation.</h1>
    <p class="lede">SCZI — aussi présentée comme SCZI Bâtiment et SCZI Toiture — est une entreprise de couverture basée à Brié-et-Angonnes, dans l’Isère.</p>
  </section>
  <section class="section section-alt">
    <div class="wrap split">
      <div>
        <h2>Un gérant, un métier de toiture.</h2>
        <p><strong>SCHUBERT Eric</strong> dirige l’entreprise, spécialisée dans la réfection de toiture, l’isolation de toiture et de comble non aménageable.</p>
        <p>Plus de 20 ans d’expérience en <strong>zinguerie, charpente, sarking et Velux</strong>. Les supports de couverture : tuiles, tuiles écailles, bac acier, ardoise et joints debout.</p>
        <p>Les travaux sont réalisés dans le respect des normes <strong>DTU</strong> et <strong>CSTB</strong>.</p>
      </div>
      <img src="assets/img/chantiers/lucarne-pendant.jpg" alt="Pose de zinc sur une lucarne">
    </div>
  </section>
  <section class="section">
    <div class="wrap grid-2">
      <div>
        <h2>Identité légale</h2>
        <ul>
          <li>Dénomination : SCHUBERT COUVERTURE ZINGUERIE</li>
          <li>Enseigne : Schubert Couverture Zinguerie Isolation (SCZI)</li>
          <li>Siège : {ADDRESS}</li>
          <li>SIRET : {SIRET}</li>
          <li>RCS : {RCS}</li>
          <li>Téléphone : {PHONE}</li>
        </ul>
      </div>
      <div>
        <h2>Un métier, une enseigne</h2>
        <p>SCZI — aussi SCZI Bâtiment et SCZI Toiture — intervient de Noyarey à Crolles, en passant par Brié-et-Angonnes et Grenoble.</p>
        <img src="assets/img/logo/logo-visuel.jpg" alt="Logo SCZI Toiture" style="border-radius:18px;margin-top:1rem">
      </div>
    </div>
  </section>
""",
)

SERVICES_INTRO = ""

def service_page(slug, title, description, kicker, h1, body_inner, image):
    prefix = "../"
    page(
        f"services/{slug}.html",
        title,
        description,
        slug,
        prefix=prefix,
        image=f"assets/img/{image}",
        body=f"""
  <section class="page-hero wrap">
    <p class="kicker">{kicker}</p>
    <h1>{h1}</h1>
  </section>
  {body_inner}
""",
    )


service_page(
    "toiture",
    "Toiture neuve et réfection — SCZI Brié-et-Angonnes",
    "Réfection et toiture neuve en tuiles, tuiles écailles, ardoise, bac acier ou joints debout. Lucarnes, charpente associée. Artisan à Brié-et-Angonnes (38).",
    "Toiture",
    "Toits neufs, réfections, lucarnes : le travail se voit de la rue.",
    image="chantiers/lucarne-apres.jpg",
    body_inner=f"""
  <section class="section section-alt">
    <div class="wrap split">
      <div>
        <p class="lede">Toiture neuve ou réfection : tuiles, tuiles écailles, bac acier, ardoise ou joints debout. Lucarne en joint debout cuivre, charpente associée.</p>
        <p>La charpente fait partie de l’expérience de l’entreprise (plus de 20 ans).</p>
      </div>
      <img src="../assets/img/chantiers/lucarne-apres.jpg" alt="Lucarne en tuiles écailles">
    </div>
  </section>
  <section class="section">
    <div class="wrap grid-2">
      <article>
        <h2>Toiture traditionnelle</h2>
        <p>Une toiture traditionnelle en terre cuite a une durée de vie minimum de <strong>80 ans</strong>. D’autres matériaux allongent encore cette perspective :</p>
        <ul>
          <li>tuile en terre cuite écaille plate : <strong>90 ans</strong> au minimum ;</li>
          <li>tuiles en ardoise : plus de <strong>120 ans</strong> de vie minimum.</li>
        </ul>
        <div class="price-note">
          <strong>Indication pour un bâtiment neuf</strong>
          <p>Surface de 120 m², toit sans Velux, sans cheminée, tuiles en terre cuite : <strong>à partir de 65 €/m²</strong>.</p>
        </div>
      </article>
      <article>
        <h2>Toiture plate</h2>
        <p>Une toiture plate ne contient pas de tuiles : on parle d’étanchéité bitume ou végétalisée.</p>
        <h3>Étanchéité bitume</h3>
        <p>Primaire d’accroche, puis déroulage et chauffage des rouleaux au chalumeau pour superposer les lés.</p>
        <ul>
          <li>dalle béton : maximum 40 ans avec un entretien très régulier ;</li>
          <li>ossature bois : maximum 20 ans, avec possible reprise d’étanchéité.</li>
        </ul>
        <h3>Étanchéité végétalisée</h3>
        <p>Surface végétale au-dessus du toit plat, membrane contre la corrosion liée aux racines. Entretien au minimum tous les 6 mois. Durée de vie : <strong>15 ans en moyenne</strong>.</p>
      </article>
    </div>
  </section>
  <section class="section section-alt">
    <div class="wrap">
      <h2>Réfection de lucarne — avant / après</h2>
      <p>Réfection de toiture tuile écaille et lucarne en joint debout cuivre.</p>
      <div class="gallery" data-gallery>
        <figure><a href="../assets/img/chantiers/lucarne-avant.jpg"><img src="../assets/img/chantiers/lucarne-avant.jpg" alt="Avant : lucarne et toiture à reprendre"></a><figcaption>Avant</figcaption></figure>
        <figure><a href="../assets/img/chantiers/lucarne-pendant.jpg"><img src="../assets/img/chantiers/lucarne-pendant.jpg" alt="Pendant : pose du zinc et des tuiles"></a><figcaption>Pendant</figcaption></figure>
        <figure><a href="../assets/img/chantiers/lucarne-apres.jpg"><img src="../assets/img/chantiers/lucarne-apres.jpg" alt="Après : lucarne terminée"></a><figcaption>Après</figcaption></figure>
      </div>
    </div>
  </section>
  <section class="section">
    <div class="wrap">
      <h2>Comment se déroule une réfection</h2>
      <div class="steps">
        <div class="step"><h3>Échange et visite</h3><p>Vous décrivez le bâtiment, les désordres (fuites, tuiles, zinc) et le lieu des travaux. Une visite permet d’adapter la réponse au support réel.</p></div>
        <div class="step"><h3>Choix du matériau</h3><p>Tuile, écaille, ardoise, bac acier ou joint debout : le choix suit le bâti, le budget et les règles de l’art DTU / CSTB.</p></div>
        <div class="step"><h3>Chantier</h3><p>Protection, dépose, reprise éventuelle de charpente, couverture, zinguerie de rive et d’ouvrage, contrôles d’étanchéité.</p></div>
        <div class="step"><h3>Remise</h3><p>Relecture du chantier avec vous. La lucarne en tuile écaille et zinc montre le niveau de finition visé.</p></div>
      </div>
    </div>
  </section>
  <section class="section section-alt">
    <div class="wrap">
      <h2>Questions fréquentes</h2>
      <details><summary>Intervenez-vous seulement en neuf ?</summary><p>Non. Nous réalisons aussi des réfections, comme la lucarne en tuile écaille ou la toiture à Eybens. Le neuf permet surtout de comparer durées de vie et un prix d’ordre de grandeur.</p></details>
      <details><summary>Travaillez-vous l’ardoise et le zinc ?</summary><p>Oui : ardoise et joints debout sont listés parmi les réponses possibles, au même titre que tuiles et bac acier.</p></details>
      <details><summary>Peut-on isoler en même temps ?</summary><p>C’est même le moment le plus logique : voir la page sarking. Isoler par l’extérieur évite de démonter les plafonds en rampant.</p></details>
      <p><a class="btn btn-primary" href="../contact.html">Demander un devis toiture</a></p>
    </div>
  </section>
""",
)

service_page(
    "isolation-sarking",
    "Isolation toiture par l’extérieur et sarking — SCZI 38",
    "Procédé de sarking et isolation par l’extérieur lors d’une réfection de toiture. Exemples de résistances thermiques R = 6,30. Brié-et-Angonnes, Isère.",
    "Isolation",
    "Isoler par-dessus la charpente, sans sacrifier la hauteur sous plafond.",
    image="chantiers/sarking-1054.jpg",
    body_inner="""
  <section class="section section-alt">
    <div class="wrap split">
      <div>
        <p class="lede">Le procédé permet, en cas de réfection de toiture, d’isoler dans les normes sans avoir à démonter les plafonds en rampant et/ou perdre de la hauteur due à l’épaisseur d’isolant.</p>
        <p>Il vise une baisse de consommation d’énergie, en isolant au moment où la couverture est ouverte.</p>
      </div>
      <img src="../assets/img/chantiers/sarking-1054.jpg" alt="Chantier d’isolation de toiture par l’extérieur">
    </div>
  </section>
  <section class="section">
    <div class="wrap">
      <h2>Trois montages</h2>
      <p>Différentes solutions existent suivant la configuration de la charpente et le budget. Les exemples visent une résistance thermique <strong>R = 6,30</strong>.</p>
      <div class="grid-3" style="margin-top:1rem">
        <article class="card"><img src="../assets/img/chantiers/sarking-1014.jpg" alt="Laine de bois et panneau sarking"><div class="card-body">
          <h3>Laine de bois + sarking</h3>
          <p>Laine de bois semi-rigide de 200 mm entre chevrons, panneau sarking de 60 mm. Objectif : supprimer les ponts thermiques des chevrons et les entrées d’air. R = 6,30.</p>
        </div></article>
        <article class="card"><img src="../assets/img/chantiers/sarking-0685.jpg" alt="Double couche de laine de bois 120 mm"><div class="card-body">
          <h3>Deux fois 120 mm</h3>
          <p>Laine de bois semi-rigide en deux épaisseurs de 120 mm entre chevrons, couches croisées. R = 6,30. Isolation et toiture à Saint-Nazaire.</p>
        </div></article>
        <article class="card"><img src="../assets/img/chantiers/sarking-double-chevron.jpg" alt="Double chevronnage et laine de verre"><div class="card-body">
          <h3>Double chevronnage</h3>
          <p>Isolation par l’extérieur avec double chevronnage, laine de verre 2 × 100 mm en GR32. R = 6,30. Isolation toiture à Eybens.</p>
        </div></article>
      </div>
    </div>
  </section>
  <section class="section section-alt">
    <div class="wrap">
      <h2>Déroulement type</h2>
      <div class="steps">
        <div class="step"><h3>Réfection programmée</h3><p>Le sarking a surtout du sens quand la couverture est ouverte. On isole alors « dans la foulée » du toit.</p></div>
        <div class="step"><h3>Lecture de la charpente</h3><p>Entre chevrons, hors chevrons, double chevronnage : le choix suit la structure et le budget.</p></div>
        <div class="step"><h3>Continuity de l’enveloppe</h3><p>Les panneaux hors chevrons visent à casser le pont thermique du bois et les fuites d’air.</p></div>
        <div class="step"><h3>Couverture et zinc</h3><p>La toiture se referme : tuiles, écailles, zinguerie. L’isolant n’est plus exposé.</p></div>
      </div>
      <h2 style="margin-top:2rem">FAQ</h2>
      <details><summary>Faut-il vider les combles ?</summary><p>Le sarking vise justement à éviter de démonter les plafonds en rampant.</p></details>
      <details><summary>Pourquoi R = 6,30 ?</summary><p>C’est la résistance thermique visée sur les trois montages présentés.</p></details>
      <p><a class="btn btn-primary" href="../contact.html">Demander un devis isolation</a></p>
    </div>
  </section>
""",
)

service_page(
    "isolation-combles",
    "Isolation des combles perdus par laine de roche soufflée — SCZI 38",
    "Isolation par projection des combles non aménageables. Tableau de résistances thermiques de la laine de roche soufflée. Brié-et-Angonnes.",
    "Combles perdus",
    "Quand le comble est trop bas pour vivre, on l’isole par le sol.",
    image="stock/isolation-laine.jpg",
    body_inner="""
  <section class="section section-alt">
    <div class="wrap split">
      <div>
        <p class="lede">Le terme comble perdu désigne un espace insuffisant entre la dernière hauteur de plafond horizontale et la toiture du bâtiment.</p>
        <p>Dans ce cas, l’isolation par projection reste la plus performante pour la rupture de pont thermique (pénétration dans les recoins, lame d’air entre couches) et d’un point de vue financier (gain de temps face aux rouleaux ou panneaux).</p>
        <p>Isolation des combles non aménageables <strong>par laine de roche soufflée</strong>.</p>
      </div>
      <img src="../assets/img/stock/isolation-laine.jpg" alt="Isolant en laine">
    </div>
  </section>
  <section class="section">
    <div class="wrap">
      <h2>Fiche technique — laine de roche soufflée</h2>
      <p>À partir d’une résistance thermique de <strong>7</strong> (ligne mise en avant), l’épaisseur après tassement est de 315 mm.</p>
      <div class="table-wrap"><table>
        <thead><tr><th>Ép. (mm)</th><th>Ép. après tassement (mm)</th><th>R (m².K/W)</th><th>Pouvoir couvrant (kg/m²)</th><th>Sacs / 100 m²</th><th>Up (W/m².K)</th></tr></thead>
        <tbody>
          <tr><td>95</td><td>90</td><td>2</td><td>2</td><td>9,6</td><td></td></tr>
          <tr><td>230</td><td>225</td><td>5</td><td>4,9</td><td>24,1</td><td>0,2</td></tr>
          <tr><td>275</td><td>270</td><td>6</td><td>5,8</td><td>28,9</td><td>0,16</td></tr>
          <tr class="highlight"><td>320</td><td>315</td><td>7</td><td>6,8</td><td>33,2</td><td>0,14</td></tr>
          <tr><td>365</td><td>360</td><td>8</td><td>7,8</td><td>38,5</td><td>0,12</td></tr>
          <tr><td>410</td><td>405</td><td>9</td><td>8,7</td><td>43,4</td><td></td></tr>
          <tr><td>455</td><td>450</td><td>10</td><td>9,7</td><td>48,2</td><td></td></tr>
          <tr><td>500</td><td>495</td><td>11</td><td>10,6</td><td>53</td><td></td></tr>
          <tr><td>545</td><td>540</td><td>12</td><td>11,6</td><td>57,8</td><td></td></tr>
          <tr><td>595</td><td>585</td><td>13</td><td>12,6</td><td>62,6</td><td></td></tr>
          <tr><td>640</td><td>630</td><td>14</td><td>13,5</td><td>67,5</td><td></td></tr>
          <tr><td>685</td><td>675</td><td>15</td><td>14,5</td><td>72,3</td><td></td></tr>
        </tbody>
      </table></div>
    </div>
  </section>
  <section class="section section-alt">
    <div class="wrap">
      <h2>Processus</h2>
      <div class="steps">
        <div class="step"><h3>Accès au comble</h3><p>Trappe, passage, état du plancher : on vérifie que le soufflage peut se faire sans tasser un plafond fragile.</p></div>
        <div class="step"><h3>Épaisseur cible</h3><p>Le tableau relie millimètres, tassement, résistance thermique R et nombre de sacs. La ligne R = 7 est mise en avant.</p></div>
        <div class="step"><h3>Projection</h3><p>La laine de roche est soufflée pour garnir recoins et lames d’air, plus rapidement que des panneaux.</p></div>
      </div>
      <h2>FAQ</h2>
      <details><summary>Différence avec le sarking ?</summary><p>Combles perdus = volume non habitable, isolation au sol du comble. Sarking = isolation par l’extérieur, souvent pour combles aménagés ou à préserver en hauteur.</p></details>
      <details><summary>Puis-je aménager plus tard ?</summary><p>Si l’espace redevient habitable, la logique change : isolation des combles aménagés par l’extérieur (sarking).</p></details>
      <p><a class="btn btn-primary" href="../contact.html">Demander un devis combles</a></p>
    </div>
  </section>
""",
)

service_page(
    "velux",
    "Installation et remplacement de Velux — SCZI Isère",
    "Pose, remplacement, jumelage et création de fenêtres de toit Velux. Exemples de chantiers : transformation de débarras, duo 134/140. Brié-et-Angonnes.",
    "Velux",
    "Plus de lumière sous les combles, sans construire un chien assis.",
    image="chantiers/velux-apres.jpg",
    body_inner="""
  <section class="section section-alt">
    <div class="wrap split">
      <div>
        <p class="lede">Les châssis de toit Velux apportent de la lumière et permettent d’aménager un comble, pour un coût moindre qu’un chien assis.</p>
        <p>Un Velux vise un coefficient Uw de 1,1 (plus le Uw se rapproche de 1, meilleure est l’isolation thermique).</p>
      </div>
      <img src="../assets/img/chantiers/velux-apres.jpg" alt="Fenêtre de toit Velux">
    </div>
  </section>
  <section class="section">
    <div class="wrap grid-2">
      <div>
        <h2>Integra Solar</h2>
        <p>Le modèle Integra Solar dispose de capteurs qui actionnent la ventilation en cas de trop forte humidité ou de fort taux de CO₂, et se referment à la détection de pluie. Une tablette Velux permet de programmer ouvertures, fermetures, volet extérieur, et d’autres appareils télécommandés Somfy, dans une limite de 60 appareils.</p>
        <p>Un ancien châssis qui laisse passer trop de chaleur se remplace pour se rapprocher de ces performances.</p>
      </div>
      <div>
        <h2>Exemples de chantiers</h2>
        <ul>
          <li>Transformation d’un débarras en chambre et réalisation de chevrette de panne pour pose d’un Velux.</li>
          <li>Aile droite : agrandissement d’un Velux 114 × 118 cm en jumelage après réfection totale de toiture ; aile gauche : changement de Velux. Isolation par l’extérieur en laine de bois 2 × 120 mm croisées, R = 6,30.</li>
          <li>Création de Velux en duo 134 × 140 cm ainsi que 134 × 98 cm.</li>
        </ul>
      </div>
    </div>
  </section>
  <section class="section section-alt">
    <div class="wrap">
      <div class="gallery" data-gallery>
        <figure><a href="../assets/img/chantiers/velux-avant.jpg"><img src="../assets/img/chantiers/velux-avant.jpg" alt="Avant installation Velux"></a><figcaption>Avant</figcaption></figure>
        <figure><a href="../assets/img/chantiers/velux-apres.jpg"><img src="../assets/img/chantiers/velux-apres.jpg" alt="Après installation Velux"></a><figcaption>Après</figcaption></figure>
        <figure><a href="../assets/img/chantiers/velux-transformation.jpg"><img src="../assets/img/chantiers/velux-transformation.jpg" alt="Transformation de débarras, chevrette de panne"></a><figcaption>Chevrette / transformation</figcaption></figure>
        <figure><a href="../assets/img/chantiers/velux-pose.jpg"><img src="../assets/img/chantiers/velux-pose.jpg" alt="Pose de Velux"></a><figcaption>Pose</figcaption></figure>
        <figure><a href="../assets/img/chantiers/velux-aile-droite.jpg"><img src="../assets/img/chantiers/velux-aile-droite.jpg" alt="Velux aile droite"></a><figcaption>Aile droite</figcaption></figure>
        <figure><a href="../assets/img/chantiers/velux-aile-gauche.jpg"><img src="../assets/img/chantiers/velux-aile-gauche.jpg" alt="Velux aile gauche"></a><figcaption>Aile gauche</figcaption></figure>
        <figure><a href="../assets/img/chantiers/velux-duo.jpg"><img src="../assets/img/chantiers/velux-duo.jpg" alt="Création Velux en duo"></a><figcaption>Duo</figcaption></figure>
      </div>
    </div>
  </section>
  <section class="section">
    <div class="wrap">
      <h2>Étapes</h2>
      <div class="steps">
        <div class="step"><h3>Cote et usage</h3><p>Chambre, bureau, simple éclairement : la cote (ex. 114/118) et le jumelage se décident avec la charpente.</p></div>
        <div class="step"><h3>Chevrette si besoin</h3><p>Une chevrette de panne se pose lorsque la structure ne permet pas une pose directe.</p></div>
        <div class="step"><h3>Étanchéité</h3><p>Raccord de toiture, abergement, isolation périphérique : le châssis n’est pas une simple menuiserie posée dans un trou.</p></div>
      </div>
      <h2>FAQ</h2>
      <details><summary>Peut-on poser un Velux sans refaire tout le toit ?</summary><p>Oui : des remplacements isolés sont possibles. Un jumelage peut aussi accompagner une réfection totale.</p></details>
      <details><summary>Pourquoi pas un chien assis ?</summary><p>Le Velux est moins onéreux, tout en apportant lumière et confort d’aménagement.</p></details>
      <p><a class="btn btn-primary" href="../contact.html">Demander un devis Velux</a></p>
    </div>
  </section>
""",
)

service_page(
    "zinguerie",
    "Zinguerie, chéneaux et abergements — SCZI Brié-et-Angonnes",
    "Habillages et abergements de cheminée, chéneaux, planches de rive, bandeaux et joints debout. Savoir-faire zinc de SCZI en Isère.",
    "Zinguerie",
    "Le zinc tient l’eau là où les tuiles s’arrêtent.",
    image="chantiers/lucarne-pendant.jpg",
    body_inner="""
  <section class="section section-alt">
    <div class="wrap split">
      <div>
        <p class="lede">Habillages et abergements de cheminée, pose de chéneaux, habillages de planches de rive et de bandeaux, toitures en joints debout : plus de 20 ans en zinguerie.</p>
        <p>La réfection de lucarne en joint debout cuivre montre le niveau d’ouvrage : le métal n’est pas un accessoire, c’est la ligne d’eau du toit.</p>
      </div>
      <img src="../assets/img/chantiers/lucarne-pendant.jpg" alt="Pose de zinc sur une lucarne">
    </div>
  </section>
  <section class="section">
    <div class="wrap grid-2">
      <article class="card"><div class="card-body"><h3>Cheminées</h3><p>Habillages et abergements : le point singulier le plus fréquent des infiltrations, traité dans le respect des DTU.</p></div></article>
      <article class="card"><div class="card-body"><h3>Chéneaux</h3><p>Pose de chéneaux pour collecter et évacuer les eaux pluviales, en cohérence avec la couverture.</p></div></article>
      <article class="card"><div class="card-body"><h3>Rives et bandeaux</h3><p>Habillages de planches de rive et de bandeaux : la finition du rampant, au vent et à la pluie de l’Isère.</p></div></article>
      <article class="card"><div class="card-body"><h3>Joints debout</h3><p>Couverture métallique (cuivre documenté sur une lucarne) lorsque le projet sort de la tuile classique.</p></div></article>
    </div>
  </section>
  <section class="section section-alt">
    <div class="wrap">
      <h2>Pourquoi le zinc compte en montagne grenobloise</h2>
      <p>Neige, gel, fortes pluies : les points singuliers (lucarne, cheminée, rive) fatiguent avant le plein rampant. Un abergement juste, un chéneau dimensionné, une rive bien habillée prolongent la couverture — tuile ou ardoise.</p>
      <div class="steps" style="margin-top:1.2rem">
        <div class="step"><h3>Relevé des ouvrages</h3><p>Cheminées, noues, rives, lucarnes : on liste les points d’eau avant de parler couleur de tuile.</p></div>
        <div class="step"><h3>Façonnage</h3><p>Le zinc et le cuivre se façonnent sur le chantier, pas seulement comme accessoires du commerce.</p></div>
        <div class="step"><h3>Raccord couverture</h3><p>Le métal se coud avec la tuile ou l’ardoise pour que l’eau n’ait qu’un chemin.</p></div>
      </div>
      <p><a class="btn btn-primary" href="../contact.html">Demander un devis zinguerie</a></p>
    </div>
  </section>
""",
)

page(
    "services/index.html",
    "Services toiture, isolation, Velux et zinguerie — SCZI",
    "Couverture, sarking, combles perdus, Velux et zinguerie : les métiers de SCZI à Brié-et-Angonnes, Isère.",
    "services",
    prefix="../",
    image="assets/img/chantiers/lucarne-pendant.jpg",
    body="""
  <section class="page-hero wrap">
    <p class="kicker">Services</p>
    <h1>Le toit, l’isolant, le zinc, la lumière.</h1>
    <p class="lede">Couverture, isolation, Velux et zinguerie : les métiers de SCZI à Brié-et-Angonnes, en Isère.</p>
  </section>
  <section class="section section-alt">
    <div class="wrap grid-2">
      <article class="card"><a class="stretched" href="toiture.html"><img src="../assets/img/chantiers/lucarne-apres.jpg" alt="Réfection de lucarne"><div class="card-body"><h3>Toiture</h3><p>Neuf, réfection, tuiles, écailles, ardoise, bac acier, joints debout.</p></div></a></article>
      <article class="card"><a class="stretched" href="isolation-sarking.html"><img src="../assets/img/chantiers/sarking-1054.jpg" alt="Isolation de toiture par l’extérieur"><div class="card-body"><h3>Isolation sarking</h3><p>Isoler par l’extérieur lors d’une réfection, R = 6,30.</p></div></a></article>
      <article class="card"><a class="stretched" href="isolation-combles.html"><img src="../assets/img/stock/isolation-laine.jpg" alt="Isolant en laine"><div class="card-body"><h3>Combles perdus</h3><p>Laine de roche soufflée, résistances thermiques selon l’épaisseur.</p></div></a></article>
      <article class="card"><a class="stretched" href="velux.html"><img src="../assets/img/chantiers/velux-apres.jpg" alt="Velux"><div class="card-body"><h3>Velux</h3><p>Pose, remplacement, jumelage, chevrette de panne.</p></div></a></article>
      <article class="card"><a class="stretched" href="zinguerie.html"><img src="../assets/img/chantiers/lucarne-pendant.jpg" alt="Zinguerie"><div class="card-body"><h3>Zinguerie</h3><p>Cheminées, chéneaux, rives, bandeaux, joints debout.</p></div></a></article>
    </div>
  </section>
""",
)

# Realisations gallery - use original chantiers with captions from site when known
GALLERY_ITEMS = [
    ("lucarne-avant.jpg", "Réfection de toiture et lucarne — avant"),
    ("lucarne-pendant.jpg", "Réfection de lucarne — pendant (tuile écaille, joint debout)"),
    ("lucarne-apres.jpg", "Réfection de toiture et lucarne — après"),
    ("velux-avant.jpg", "Installation Velux — avant"),
    ("velux-apres.jpg", "Installation Velux — après"),
    ("velux-installation.jpg", "Installation Velux"),
    ("velux-transformation.jpg", "Transformation d’un débarras / chevrette de panne"),
    ("velux-pose.jpg", "Pose de Velux"),
    ("velux-aile-droite.jpg", "Velux — aile droite (jumelage 114/118)"),
    ("velux-aile-gauche.jpg", "Velux — aile gauche"),
    ("velux-duo.jpg", "Création de Velux en duo"),
    ("sarking-1054.jpg", "Isolation toiture par l’extérieur"),
    ("sarking-1016.jpg", "Isolation / sarking"),
    ("sarking-1014.jpg", "Laine de bois et panneau sarking — Saint-Nazaire"),
    ("sarking-0685.jpg", "Laine de bois 2 × 120 mm"),
    ("sarking-0684.jpg", "Isolation entre chevrons"),
    ("sarking-double-chevron.jpg", "Double chevronnage, laine de verre GR32 — Eybens"),
    ("sarking-0083.jpg", "Isolation par l’extérieur — Eybens"),
    ("sarking-0109.jpg", "Isolation par l’extérieur"),
    ("toiture-0664.jpg", "Ouvrage de toiture"),
    ("toiture-0662.jpg", "Ouvrage de toiture"),
    ("eybens-avant.jpg", "Toiture de maison à Eybens — avant"),
    ("mur-pignon-1.jpg", "Mur pignon"),
    ("mur-pignon-2.jpg", "Mur pignon"),
    ("img-0091.jpg", ""),
    ("img-0427.jpg", ""),
    ("img-0422.jpg", ""),
    ("img-0153.jpg", ""),
    ("img-0135.jpg", ""),
    ("img-0110.jpg", ""),
    ("img-0108.jpg", ""),
    ("img-0064.jpg", ""),
    ("img-0058.jpg", ""),
    ("img-0054.jpg", ""),
    ("img-0042.jpg", ""),
    ("img-0039.jpg", ""),
    ("img-0032.jpg", ""),
    ("img-0651.jpg", ""),
    ("img-0638.jpg", ""),
    ("img-0593.jpg", ""),
    ("img-0590.jpg", ""),
    ("img-0561.jpg", ""),
    ("img-0530.jpg", ""),
    ("img-0515.jpg", ""),
    ("img-0284.jpg", ""),
    ("img-0246.jpg", ""),
    ("img-0241.jpg", ""),
    ("img-0086.jpg", ""),
    ("img-0059.jpg", ""),
    ("img-0056.jpg", ""),
    ("img-0052.jpg", ""),
    ("img-0050.jpg", ""),
    ("img-0021.jpg", ""),
    ("img-0009.jpg", ""),
    ("img-0003.jpg", ""),
    ("dsc-0037.jpg", ""),
    ("fullsizer.jpg", ""),
    ("sans-titre-5.jpg", ""),
    ("sans-titre-2.jpg", ""),
]


def gallery_figure(fn, cap):
    alt = cap if cap else "Toiture, chantier SCZI"
    html = f'<figure><a href="assets/img/chantiers/{fn}"><img src="assets/img/chantiers/{fn}" alt="{alt}"></a>'
    if cap:
        html += f"<figcaption>{cap}</figcaption>"
    return html + "</figure>"


figs = "\n".join(gallery_figure(fn, cap) for fn, cap in GALLERY_ITEMS)

page(
    "realisations.html",
    "Réalisations toiture et isolation — galerie SCZI",
    "Galerie de chantiers SCZI : lucarnes, Velux, sarking, Eybens, Saint-Nazaire.",
    "realisations.html",
    body=f"""
  <section class="page-hero wrap">
    <p class="kicker">Réalisations</p>
    <h1>Les toits déjà photographiés.</h1>
    <p class="lede">Lucarnes, Velux, sarking, toitures à Eybens et Saint-Nazaire : une sélection de chantiers.</p>
  </section>
  <section class="section section-alt">
    <div class="wrap">
      <div class="gallery" data-gallery>
        {figs}
      </div>
    </div>
  </section>
""",
)

page(
    "zone-intervention.html",
    "Zone d’intervention SCZI — de Noyarey à Crolles",
    "SCZI intervient de Noyarey à Crolles, en passant par Brié-et-Angonnes et Grenoble. Siège : 4290 route Napoléon, 38320 Brié-et-Angonnes.",
    "zone-intervention.html",
    body=f"""
  <section class="page-hero wrap">
    <p class="kicker">Territoire</p>
    <h1>De Noyarey à Crolles, en passant par Grenoble.</h1>
    <p class="lede">SCZI intervient de Noyarey à Crolles, en passant par Brié-et-Angonnes et Grenoble. Le siège est à Brié-et-Angonnes, en Isère.</p>
  </section>
  <section class="section section-alt">
    <div class="wrap split">
      <div>
        <h2>Le corridor d’intervention</h2>
        <ul>
          <li>Siège : <a href="{MAPS_URL}" rel="noopener noreferrer">{ADDRESS}</a></li>
          <li>De <strong>Noyarey</strong> à <strong>Crolles</strong></li>
          <li>En passant par <strong>Brié-et-Angonnes</strong> et <strong>Grenoble</strong></li>
          <li>Département : Isère (38)</li>
          <li>Chantiers documentés : toiture à <strong>Eybens</strong>, isolation et toiture à <strong>Saint-Nazaire</strong></li>
        </ul>
      </div>
      <div class="map-placeholder">
        <div>
          <strong>Brié-et-Angonnes</strong>
          <p style="margin:0">{STREET} · {POSTAL}</p>
          <p style="margin:0.6rem 0 0"><a href="{MAPS_URL}" rel="noopener noreferrer">Ouvrir dans Google Maps</a></p>
        </div>
      </div>
    </div>
  </section>
  <section class="section">
    <div class="wrap">
      <h2>Pourquoi le climat local compte</h2>
      <p>Tuiles écailles, zinc, sarking et laine soufflée répondent à des toits exposés au froid, à la neige et aux écarts thermiques de l’agglomération grenobloise. L’isolation par l’extérieur et les combles perdus y sont des leviers d’économie de chauffage.</p>
      <img src="assets/img/stock/paysage-alpes.jpg" alt="Paysage de montagne en Isère" style="border-radius:18px;margin:1rem 0;max-height:22rem;width:100%;object-fit:cover">
      <p><a class="btn btn-primary" href="contact.html">Indiquer le lieu des travaux</a></p>
    </div>
  </section>
""",
)

page(
    "contact.html",
    "Devis toiture et isolation — contact SCZI Brié-et-Angonnes",
    "Demandez un devis SCZI : nom, téléphone, e-mail, lieu des travaux, budget estimé, besoins. Téléphone 04 38 70 03 94. Brié-et-Angonnes (38).",
    "contact.html",
    body=f"""
  <section class="page-hero wrap">
    <p class="kicker">Contact</p>
    <h1>Un devis, à partir du toit que vous décrivez.</h1>
    <p class="lede">Nom, téléphone, e-mail, lieu des travaux, budget estimé et besoins : nous revenons vers vous.</p>
  </section>
  <section class="section section-alt">
    <div class="wrap contact-layout">
      <form class="form" id="devis-form" action="https://formspree.io/f/xxxxxxxx" method="POST">
        <p class="form-notice" id="form-fallback" hidden></p>
        <div class="form-row">
          <label>Nom *<input name="nom" type="text" required autocomplete="name"></label>
          <label>Téléphone<input name="telephone" type="tel" autocomplete="tel"></label>
        </div>
        <label>E-mail *<input name="email" type="email" required autocomplete="email"></label>
        <div class="form-row">
          <label>Lieu des futurs travaux<input name="lieu" type="text"></label>
          <label>Budget estimé<input name="budget" type="text"></label>
        </div>
        <label>Vos besoins *<textarea name="besoin" required></textarea></label>
        <label class="hp">Site web<input name="company_website" tabindex="-1" autocomplete="off"></label>
        <p>En envoyant ce formulaire, vous acceptez d’être recontacté au sujet de votre projet. Voir les <a href="mentions-legales.html">mentions légales</a>.</p>
        <button class="btn btn-primary" type="submit">Envoyer</button>
      </form>
      <aside class="contact-card">
        <h2>Coordonnées</h2>
        <dl>
          <dt>Téléphone</dt>
          <dd><a href="tel:{PHONE_TEL}">{PHONE}</a></dd>
          <dt>Siège</dt>
          <dd><a href="{MAPS_URL}" rel="noopener noreferrer">{ADDRESS}</a></dd>
          <dt>Gérant</dt>
          <dd>SCHUBERT Eric</dd>
        </dl>
      </aside>
    </div>
  </section>
""",
)

page(
    "mentions-legales.html",
    "Mentions légales — Schubert Couverture Zinguerie Isolation",
    "Mentions légales SCZI : SIRET 75106621800023, RCS Grenoble B 751 066 218, siège 4290 route Napoléon, 38320 Brié-et-Angonnes, tél. 04 38 70 03 94.",
    "mentions",
    body=f"""
  <section class="page-hero wrap">
    <p class="kicker">Informations légales</p>
    <h1>Mentions légales</h1>
    <p class="lede">Éditeur, hébergement et protection des données personnelles.</p>
  </section>
  <section class="section section-alt">
    <div class="wrap" style="max-width:48rem">
      <h2>Éditeur</h2>
      <p>La société SCHUBERT COUVERTURE ZINGUERIE<br>
      SIRET {SIRET}<br>
      RCS Ville tribunal : {RCS}<br>
      Siège social : 4290 route Napoléon — 38320 Brié-et-Angonnes<br>
      Téléphone : {PHONE}<br>
      Directeur de la publication : la société SCHUBERT COUVERTURE ZINGUERIE</p>

      <h2>Hébergement</h2>
      <p>Ce site est hébergé par GitHub Pages — GitHub, Inc., 88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, États-Unis.</p>

      <h2>Données personnelles</h2>
      <p>La société SCHUBERT COUVERTURE ZINGUERIE n’enregistre pas d’informations personnelles permettant l’identification, à l’exception des formulaires que l’utilisateur est libre de remplir. Ces informations ne seront pas utilisées sans votre accord ; elles servent à vous adresser des courriers, des brochures, des devis ou à vous contacter.</p>
      <p>Les informations recueillies bénéficient de la protection de la loi « Informatique et Libertés » n° 78-17 du 6 janvier 1978. Droit d’accès, de rectification, d’opposition et de suppression sur simple demande à SCHUBERT COUVERTURE ZINGUERIE, 4290 route Napoléon — 38320 Brié-et-Angonnes.</p>
      <p>La société peut procéder à des analyses statistiques non nominatives et en informer des tiers (organismes d’évaluation de fréquentation) sous forme résumée et non nominative.</p>
      <p>Ce site n’installe pas de cookies de mesure d’audience.</p>

      <h2>Création graphique</h2>
      <p>Création graphique : Thomas BONSIRVEN.</p>

      <h2>Liens hypertexte</h2>
      <p>La société SCHUBERT COUVERTURE ZINGUERIE ne contrôle pas les sites en connexion avec le sien, et ne saurait donc être responsable de leur contenu.</p>

      <h2>Photographies</h2>
      <p>Les crédits photographiques et les mentions d’origine sont regroupés sur la page <a href="credits.html">Crédits & informations</a>.</p>
    </div>
  </section>
""",
)

page(
    "credits.html",
    "Crédits & informations — SCZI",
    "Crédits photographiques et informations encore à fournir pour le site SCZI.",
    "credits",
    body="""
  <section class="page-hero wrap">
    <p class="kicker">Documentation interne</p>
    <h1>Crédits & informations</h1>
    <p class="lede">Page hors parcours client : crédits des photos de stock (obligation légale) et liste de ce qui reste à fournir. Les pages publiques n’affichent que le texte destiné aux visiteurs.</p>
  </section>
  <section class="section section-alt">
    <div class="wrap" style="max-width:48rem">
      <h2>Crédits photographiques, par page</h2>
      <p>Les photos de chantiers (lucarnes, Velux, sarking, Eybens, Saint-Nazaire, etc.) proviennent des archives SCZI. Les visuels de stock ci-dessous sont des copies locales, licences Unsplash / Pexels.</p>
      <h3>Accueil, hub Services, Isolation combles</h3>
      <ul>
        <li><code>isolation-laine.jpg</code> — Pexels, Karolina Grabowska — <a href="https://images.pexels.com/photos/5691622/pexels-photo-5691622.jpeg">source</a></li>
      </ul>
      <h3>Zone d’intervention</h3>
      <ul>
        <li><code>paysage-alpes.jpg</code> — Pexels, James Wheeler — <a href="https://images.pexels.com/photos/417074/pexels-photo-417074.jpeg">source</a> (photo et fond de la carte)</li>
      </ul>
      <h3>Autres photos de stock du dépôt (non affichées sur les pages publiques)</h3>
      <ul>
        <li>Unsplash : Quin Stevenson, Annika Gordon, Daniel McCullough, Dan Gold, R ARCHITECTURE, Daniel Hjalmarsson</li>
        <li>Pexels : Pixabay, Bin Zhang, Kiwihug, Vecislavas Popa, Blue Bird, Binyamin Mellish</li>
      </ul>
      <p>Liste détaillée : <a href="assets/img/stock/CREDITS.txt">assets/img/stock/CREDITS.txt</a>.</p>
    </div>
  </section>
  <section class="section">
    <div class="wrap" style="max-width:48rem">
      <h2>Informations encore à fournir</h2>
      <ol>
        <li>E-mail professionnel</li>
        <li>Identifiant Formspree (remplacer <code>xxxxxxxx</code> dans <code>contact.html</code>) ou adresse mailto définitive</li>
        <li>Horaires d’accueil / d’appel</li>
        <li>Numéros de certificat Qualibat et RGE</li>
        <li>Macarons / certificats Qualibat RGE des années <strong>2018 à 2026</strong> (inventaire complet du site sczi-renov38.fr — 16 pages, 91 médias — et de <code>assets/img/badges/</code> : seuls <strong>2016</strong> et <strong>2016–2017</strong> existent). Ne pas inventer d’images.</li>
        <li>Barèmes chiffrés des aides (MaPrimeRénov’, CEE, éco-PTZ, TVA 5,5&nbsp;% sont cités sur l’accueil, sans montants)</li>
        <li>Tarifs actualisés (le 65 €/m² date d’environ 2018)</li>
        <li>Légendes des photos de chantier encore sans commune ni date</li>
        <li>Réseaux sociaux (les anciens liens du thème étaient factices)</li>
        <li>Forme juridique, capital, TVA intra, assurance décennale</li>
        <li>Avis clients (aucun n’est inventé ici)</li>
        <li>Hébergeur à confirmer si le domaine sczi-renov38.fr est recollé</li>
        <li>Métaux de zinguerie au catalogue, garanties de patine</li>
        <li>Marque d’isolant et avis technique pour le soufflage</li>
      </ol>
    </div>
  </section>
""",
)

page(
    "404.html",
    "Page introuvable — SCZI",
    "La page demandée n’existe pas sur le site SCZI.",
    "404",
    body="""
  <section class="page-hero wrap">
    <p class="kicker">Erreur 404</p>
    <h1>Cette page n’est pas sur le toit.</h1>
    <p class="lede">Le lien est cassé ou la page a été déplacée.</p>
    <a class="btn btn-primary" href="index.html">Retour à l’accueil</a>
  </section>
""",
)

# robots + sitemap
pages_urls = [
    "",
    "a-propos.html",
    "realisations.html",
    "zone-intervention.html",
    "contact.html",
    "mentions-legales.html",
    "credits.html",
    "services/index.html",
    "services/toiture.html",
    "services/isolation-sarking.html",
    "services/isolation-combles.html",
    "services/velux.html",
    "services/zinguerie.html",
]
sitemap = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for p in pages_urls:
    loc = f"{SITE}/{p}"
    sitemap.append(f"  <url><loc>{loc}</loc><changefreq>monthly</changefreq></url>")
sitemap.append("</urlset>")
(ROOT / "sitemap.xml").write_text("\n".join(sitemap) + "\n", encoding="utf-8")
(ROOT / "robots.txt").write_text(
    f"""User-agent: *
Allow: /

Sitemap: {SITE}/sitemap.xml
""",
    encoding="utf-8",
)
print("robots + sitemap ok")
