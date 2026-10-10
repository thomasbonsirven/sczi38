#!/usr/bin/env python3
"""Génère les pages HTML statiques du site SCZI. Aucune étape de build n'est requise à la publication."""
from pathlib import Path

ROOT = Path("/workspace")
SITE = "https://thomasbonsirven.github.io/sczi38"
PHONE = "04 38 70 03 94"
PHONE_TEL = "+33438700394"
ADDRESS = "666 Route de Saint Nizier, 38170 Seyssinet-Pariset"
SIRET = "75106621800023"
RCS = "Grenoble B 751 066 218"


def asset(prefix, path):
    return f"{prefix}assets/{path}"


def nav(prefix, current):
    links = [
        ("index.html", "Accueil", f"{prefix}index.html"),
        ("a-propos.html", "L’entreprise", f"{prefix}a-propos.html"),
        ("services", "Services", f"{prefix}services/index.html"),
        ("realisations.html", "Réalisations", f"{prefix}realisations.html"),
        ("zone-intervention.html", "Zone d’intervention", f"{prefix}zone-intervention.html"),
        ("contact.html", "Devis", f"{prefix}contact.html"),
    ]
    items = []
    for key, label, href in links:
        cur = ' aria-current="page"' if current == key else ""
        items.append(f'<li><a href="{href}"{cur}>{label}</a></li>')
    return "\n        ".join(items)


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
    "streetAddress": "666 Route de Saint Nizier",
    "addressLocality": "Seyssinet-Pariset",
    "postalCode": "38170",
    "addressRegion": "Isère",
    "addressCountry": "FR"
  }},
  "areaServed": [
    {{"@type": "City", "name": "Seyssinet-Pariset"}},
    {{"@type": "City", "name": "Grenoble"}},
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
        <span>Artisan couvreur à Seyssinet-Pariset — 5 km de Grenoble</span>
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
        <p>Schubert Couverture Zinguerie Isolation — réfection de toiture, isolation et zinguerie à Seyssinet-Pariset (Isère).</p>
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
        <p>{ADDRESS}</p>
        <p><a href="tel:{PHONE_TEL}">{PHONE}</a></p>
        <p class="todo-fill" style="color:#5c3b16"><strong>E-mail à compléter</strong> Non publié sur le site actuel (lien thème : your@email).</p>
        <p>SIRET {SIRET}<br>RCS {RCS}</p>
      </div>
    </div>
    <div class="wrap legal">
      <p>© SCZI — Schubert Couverture Zinguerie Isolation. Site statique de proposition, destiné à GitHub Pages.</p>
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
    "SCZI Toiture — Couverture, isolation et zinguerie à Seyssinet-Pariset (38)",
    "Entreprise spécialisée dans la réfection de toiture, l’isolation de toiture et de combles, implantée à Seyssinet-Pariset dans l’Isère, à 5 km de Grenoble.",
    "index.html",
    extra=SCHEMA,
    body=f"""
  <section class="hero">
    <img class="hero-bg" src="assets/img/chantiers/lucarne-pendant.jpg" width="900" height="1200" alt="Artisan SCZI en toiture, pose de zinc et tuiles écailles avec les Alpes en arrière-plan">
    <div class="wrap hero-inner">
      <p class="kicker" style="color:#ffb4bc">Schubert Couverture Zinguerie Isolation</p>
      <h1>La toiture, l’isolation et le zinc, travaillés pour le climat de l’Isère.</h1>
      <p class="lede">Notre entreprise spécialisée dans la réfection de toiture, l’isolation de toiture et de comble non aménageable est implantée à Seyssinet-Pariset, à 5 km de Grenoble.</p>
      <div class="hero-actions">
        <a class="btn btn-primary" href="contact.html">Demander un devis</a>
        <a class="btn btn-light" href="realisations.html">Voir les chantiers</a>
      </div>
      <div class="hero-facts">
        <div><strong>10 ans+</strong><span>d’expérience en zinguerie, charpente, sarking et Velux</span></div>
        <div><strong>Seyssinet</strong><span>base à 5 km de Grenoble, Isère (38)</span></div>
        <div><strong>DTU / CSTB</strong><span>réponses adaptées aux tuiles, ardoise, bac acier, joints debout</span></div>
        <div><strong>Eric Schubert</strong><span>gérant, sur le chantier comme au devis</span></div>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <p class="kicker">Métiers</p>
      <h2>Quatre savoir-faire de toiture, un seul interlocuteur.</h2>
      <p class="lede">Le site historique présentait l’isolation, la toiture et les Velux. La zinguerie (chéneaux, abergements, rives, joints debout) y était déjà décrite : elle a désormais sa page dédiée.</p>
      <div class="grid-2" style="margin-top:1.5rem">
        <article class="card"><a class="stretched" href="services/toiture.html">
          <img src="assets/img/chantiers/lucarne-apres.jpg" alt="Lucarne après réfection, tuiles écailles et zinc">
          <div class="card-body"><span class="tag">Couverture</span><h3>Toiture neuve et réfection</h3><p>Tuiles, tuiles écailles, bac acier, ardoise ou joints debout. Habillage de lucarnes, charpente associée.</p></div></a></article>
        <article class="card"><a class="stretched" href="services/isolation-sarking.html">
          <img src="assets/img/chantiers/sarking-1054.jpg" alt="Isolation de toiture par l’extérieur, chantier SCZI">
          <div class="card-body"><span class="tag">Isolation</span><h3>Sarking et isolation par l’extérieur</h3><p>Isoler lors d’une réfection sans démonter les plafonds en rampant, ni perdre de hauteur sous toiture.</p></div></a></article>
        <article class="card"><a class="stretched" href="services/isolation-combles.html">
          <img src="assets/img/stock/isolation-laine.jpg" alt="Isolant en laine, illustration stock">
          <div class="card-body"><span class="tag">Combles</span><h3>Combles perdus soufflés</h3><p>Isolation par projection de laine de roche, pour les volumes trop bas pour être aménagés.</p></div></a></article>
        <article class="card"><a class="stretched" href="services/velux.html">
          <img src="assets/img/chantiers/velux-apres.jpg" alt="Fenêtre de toit Velux après installation">
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
          <div class="trust-item"><span class="num">02</span><div><h3>Des photos de vrais toits</h3><p>Lucarnes, sarking, Velux, Eybens, Saint-Nazaire : les images viennent du site existant.</p></div></div>
        </div>
      </div>
      <figure>
        <img src="assets/img/chantiers/lucarne-pendant.jpg" alt="SCHUBERT Eric ou un compagnon SCZI au travail sur une lucarne en zinc">
        <figcaption class="credit">Photo extraite du site sczi-renov38.fr — chantier de lucarne.</figcaption>
      </figure>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <p class="kicker">Qualifications</p>
      <h2>RGE et Qualibat, tels qu’annoncés sur le site actuel.</h2>
      <p>Le site indique : « Nous sommes désormais reconnue RGE et Qualibat, ce qui vous permet de bénéficier de crédit d’impôt et de la T.V.A à 5,5 %. » Les pages techniques mentionnaient aussi un crédit d’impôt de 30 % sur certains travaux d’isolation.</p>
      <div class="badge-row" style="margin:1.2rem 0">
        <img src="assets/img/badges/rge.png" alt="Badge Entreprise certifiée RGE Qualibat 2016-2017">
        <img src="assets/img/badges/rge-2016.jpg" alt="Attestation RGE 2016 issue du site actuel">
      </div>
      <div class="todo-fill">
        <strong>À compléter — validité actuelle des labels</strong>
        Le badge publié sur le site date de 2016–2017. Les numéros de certificat RGE / Qualibat, la date de fin de validité et le statut 2026 ne figurent pas en ligne. Les aides (MaPrimeRénov’, CEE, TVA réduite) ont aussi évolué depuis la mention des « 30 % ». Faites vérifier le dossier avant tout devis fiscal.
      </div>
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
        <p>Le formulaire reprend les champs du site actuel : nom, téléphone, e-mail, lieu des futurs travaux, budget estimé, besoins.</p>
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
    "SCZI, dirigée par SCHUBERT Eric, est implantée à Seyssinet-Pariset (38170). Plus de 10 ans d’expérience en toiture, isolation, zinguerie, charpente et Velux.",
    "a-propos.html",
    body=f"""
  <section class="page-hero wrap">
    <p class="kicker">L’entreprise</p>
    <h1>Schubert Couverture Zinguerie Isolation.</h1>
    <p class="lede">SCZI — aussi présentée comme SCZI Bâtiment et SCZI Toiture — est une entreprise de couverture basée à Seyssinet-Pariset, dans l’Isère.</p>
  </section>
  <section class="section section-alt">
    <div class="wrap split">
      <div>
        <h2>Un gérant, un métier de toiture.</h2>
        <p>Le site actuel identifie <strong>SCHUBERT Eric</strong> comme gérant. L’entreprise se présente comme spécialisée dans la réfection de toiture, l’isolation de toiture et de comble non aménageable.</p>
        <p>Elle met en avant plus de 10 ans d’expérience en <strong>zinguerie, charpente, sarking et Velux</strong>. Les supports de couverture cités sont les tuiles, les tuiles écailles, le bac acier, l’ardoise et les joints debout.</p>
        <p>Les travaux sont décrits comme réalisés dans le respect des normes <strong>DTU</strong> et <strong>CSTB</strong>.</p>
      </div>
      <img src="assets/img/chantiers/lucarne-pendant.jpg" alt="Compagnon SCZI au travail, t-shirt aux couleurs de l’entreprise">
    </div>
  </section>
  <section class="section">
    <div class="wrap grid-2">
      <div>
        <h2>Identité légale (site actuel)</h2>
        <ul>
          <li>Dénomination : SCHUBERT COUVERTURE ZINGUERIE</li>
          <li>Enseigne : Schubert Couverture Zinguerie Isolation (SCZI)</li>
          <li>Siège : {ADDRESS}</li>
          <li>SIRET : {SIRET}</li>
          <li>RCS : {RCS}</li>
          <li>Téléphone : {PHONE}</li>
          <li>Directeur de la publication : la société</li>
          <li>Création graphique du site historique : Thomas BONSIRVEN</li>
        </ul>
        <div class="todo-fill">
          <strong>À compléter</strong>
          Forme juridique détaillée, capital social, n° TVA intracommunautaire, e-mail professionnel, horaires d’accueil, effectif, assurance décennale (n° de police). Aucune de ces mentions n’apparaît clairement sur le site actuel, hors SIRET / RCS / adresse / téléphone.
        </div>
      </div>
      <div>
        <h2>Ce que nous ne faisons pas ici</h2>
        <p>Aucun avis client n’est publié sur sczi-renov38.fr. Ce site de proposition n’en invente pas. Les réseaux sociaux du thème actuel pointent vers <code>http://url</code> : ce sont des placeholders, ils ne sont pas repris.</p>
        <img src="assets/img/logo/logo-visuel.jpg" alt="Visuel de marque SCZI Toiture" style="border-radius:18px;margin-top:1rem">
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
        "services",
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
    "Toiture neuve et réfection — SCZI Seyssinet-Pariset",
    "Réfection et toiture neuve en tuiles, tuiles écailles, ardoise, bac acier ou joints debout. Lucarnes, charpente associée. Artisan à Seyssinet-Pariset (38).",
    "Toiture",
    "Toits neufs, réfections, lucarnes : le travail se voit de la rue.",
    image="chantiers/lucarne-apres.jpg",
    body_inner=f"""
  <section class="section section-alt">
    <div class="wrap split">
      <div>
        <p class="lede">Pour un bâtiment neuf, le site actuel compare toiture traditionnelle et toiture plate. Pour l’existant, il documente une réfection de toiture en tuile écaille avec lucarne en joint debout cuivre.</p>
        <p>Les couvertures traitées : tuiles, tuiles écailles, bac acier, ardoise, joints debout. La charpente fait partie de l’expérience affichée (plus de 10 ans).</p>
      </div>
      <img src="../assets/img/chantiers/lucarne-apres.jpg" alt="Lucarne après réfection, tuiles écailles">
    </div>
  </section>
  <section class="section">
    <div class="wrap grid-2">
      <article>
        <h2>Toiture traditionnelle</h2>
        <p>Une toiture traditionnelle en terre cuite a, d’après le texte du site, une durée de vie minimum de <strong>80 ans</strong>. D’autres matériaux allongent encore cette perspective :</p>
        <ul>
          <li>tuile en terre cuite écaille plate : <strong>90 ans</strong> au minimum ;</li>
          <li>tuiles en ardoise : plus de <strong>120 ans</strong> de vie minimum.</li>
        </ul>
        <div class="price-note">
          <strong>Indication tarifaire reprise du site (bâtiment neuf)</strong>
          <p>Surface de 120 m², toit sans Velux, sans cheminée, tuiles en terre cuite : <strong>à partir de 65 €/m²</strong>.</p>
          <p class="credit">Cette fourchette est celle publiée sur la page Toiture (dernière mise à jour indiquée : 2018). Elle n’a pas été actualisée ici.</p>
        </div>
        <div class="todo-fill" style="margin-top:1rem"><strong>À compléter</strong> Grille tarifaire actuelle, éventuels indices de révision, prestations incluses / exclues.</div>
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
        <p>Surface végétale au-dessus du toit plat, membrane contre la corrosion liée aux racines. Entretien au minimum tous les 6 mois. Durée de vie indiquée : <strong>15 ans en moyenne</strong>.</p>
        <p class="credit">La photo de toit végétalisé du site historique (EVA Lanxmeer) est un visuel d’illustration, pas nécessairement un chantier SCZI.</p>
      </article>
    </div>
  </section>
  <section class="section section-alt">
    <div class="wrap">
      <h2>Réfection de lucarne — avant / après</h2>
      <p>Chantier présenté comme « réfection de toiture tuile écaille et lucarne en joint de bout cuivre ».</p>
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
        <div class="step"><h3>Remise</h3><p>Relecture du chantier avec vous. Les photos de lucarne du site montrent le niveau de finition visé.</p></div>
      </div>
    </div>
  </section>
  <section class="section section-alt">
    <div class="wrap">
      <h2>Questions fréquentes</h2>
      <details><summary>Intervenez-vous seulement en neuf ?</summary><p>Non. Le site documente aussi la réfection (lucarne, Eybens). Le neuf sert surtout à comparer durées de vie et un prix d’ordre de grandeur.</p></details>
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
    "Procédé de sarking et isolation par l’extérieur lors d’une réfection de toiture. Exemples de résistances thermiques R = 6,30. Seyssinet-Pariset, Isère.",
    "Isolation",
    "Isoler par-dessus la charpente, sans sacrifier la hauteur sous plafond.",
    image="chantiers/sarking-1054.jpg",
    body_inner="""
  <section class="section section-alt">
    <div class="wrap split">
      <div>
        <p class="lede">Le procédé permet, en cas de réfection de toiture, d’isoler dans les normes sans avoir à démonter les plafonds en rampant et/ou perdre de la hauteur due à l’épaisseur d’isolant.</p>
        <p>Il vise une baisse de consommation d’énergie. Le site historique indiquait un crédit d’impôt de 30 % sur ces travaux : ce taux n’est plus le cadre légal actuel, d’où le bandeau ci-dessous.</p>
        <div class="todo-fill"><strong>Aides à actualiser</strong> Remplacer la mention « 30 % » par le dispositif en vigueur (MaPrimeRénov’, CEE, TVA). Confirmer que l’entreprise est toujours RGE au moment du devis.</div>
      </div>
      <img src="../assets/img/chantiers/sarking-1054.jpg" alt="Chantier d’isolation de toiture par l’extérieur">
    </div>
  </section>
  <section class="section">
    <div class="wrap">
      <h2>Trois montages décrits sur le site actuel</h2>
      <p>Différentes solutions existent suivant la configuration de la charpente et le budget. Les exemples publiés visent tous une résistance thermique <strong>R = 6,30</strong>.</p>
      <div class="grid-3" style="margin-top:1rem">
        <article class="card"><img src="../assets/img/chantiers/sarking-1014.jpg" alt="Laine de bois et panneau sarking"><div class="card-body">
          <h3>Laine de bois + sarking</h3>
          <p>Laine de bois semi-rigide de 200 mm entre chevrons, panneau sarking de 60 mm. Objectif : supprimer les ponts thermiques des chevrons et les entrées d’air. R = 6,30.</p>
        </div></article>
        <article class="card"><img src="../assets/img/chantiers/sarking-0685.jpg" alt="Double couche de laine de bois 120 mm"><div class="card-body">
          <h3>Deux fois 120 mm</h3>
          <p>Laine de bois semi-rigide en deux épaisseurs de 120 mm entre chevrons, couches croisées. R = 6,30. Chantier légendé « Isolation et toiture Saint-Nazaire ».</p>
        </div></article>
        <article class="card"><img src="../assets/img/chantiers/sarking-double-chevron.jpg" alt="Double chevronnage et laine de verre"><div class="card-body">
          <h3>Double chevronnage</h3>
          <p>Isolation par l’extérieur avec double chevronnage, laine de verre 2 × 100 mm en GR32. R = 6,30. Légende : « Isolation toiture extérieur Eybens » sur une version de la page.</p>
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
      <details><summary>Faut-il vider les combles ?</summary><p>Le propos du sarking, tel qu’écrit sur le site, est justement d’éviter de démonter les plafonds en rampant.</p></details>
      <details><summary>Pourquoi R = 6,30 ?</summary><p>C’est la valeur publiée sur les trois exemples, associée à l’époque à l’éligibilité d’un crédit d’impôt. La réglementation et les aides ont changé : à recaler au devis.</p></details>
      <p><a class="btn btn-primary" href="../contact.html">Demander un devis isolation</a></p>
    </div>
  </section>
""",
)

service_page(
    "isolation-combles",
    "Isolation des combles perdus par laine de roche soufflée — SCZI 38",
    "Isolation par projection des combles non aménageables. Tableau de résistances thermiques de la laine de roche soufflée. Seyssinet-Pariset.",
    "Combles perdus",
    "Quand le comble est trop bas pour vivre, on l’isole par le sol.",
    image="stock/isolation-laine.jpg",
    body_inner="""
  <section class="section section-alt">
    <div class="wrap split">
      <div>
        <p class="lede">Le terme comble perdu désigne un espace insuffisant entre la dernière hauteur de plafond horizontale et la toiture du bâtiment.</p>
        <p>Dans ce cas, l’isolation par projection reste, d’après le site, la plus performante pour la rupture de pont thermique (pénétration dans les recoins, lame d’air entre couches) et d’un point de vue financier (gain de temps face aux rouleaux ou panneaux).</p>
        <p>La page d’accueil précise : isolation des combles non aménageables <strong>par laine de roche soufflée</strong>.</p>
      </div>
      <img src="../assets/img/stock/isolation-laine.jpg" alt="Illustration stock : isolant en laine">
    </div>
    <div class="wrap"><p class="credit">Photo d’ambiance : Pexels — Karolina Grabowska. Aucune photo de soufflage n’était clairement légendée sur le site actuel.</p></div>
  </section>
  <section class="section">
    <div class="wrap">
      <h2>Fiche technique reprise du site</h2>
      <p>Le tableau ci-dessous est celui publié sous le titre « Fiche technique isolation laine de roche soufflé ». À partir d’une résistance thermique de <strong>7</strong> (ligne mise en avant), le crédit d’impôt était présenté comme éligible.</p>
      <div class="todo-fill" style="margin-bottom:1rem"><strong>À vérifier</strong> Marque de l’isolant, avis technique en vigueur, et aides 2026. Le tableau est historique.</div>
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
      <p class="credit">Extrait simplifié : le tableau original du site contient toutes les lignes intermédiaires (tous les 0,5 de R). Valeurs non réinventées.</p>
    </div>
  </section>
  <section class="section section-alt">
    <div class="wrap">
      <h2>Processus</h2>
      <div class="steps">
        <div class="step"><h3>Accès au comble</h3><p>Trappe, passage, état du plancher : on vérifie que le soufflage peut se faire sans tasser un plafond fragile.</p></div>
        <div class="step"><h3>Épaisseur cible</h3><p>Le tableau relie millimètres, tassement, R et nombre de sacs. Le site mettait en avant R ≥ 7 pour l’aide fiscale d’alors.</p></div>
        <div class="step"><h3>Projection</h3><p>La laine de roche est soufflée pour garnir recoins et lames d’air, plus rapidement que des panneaux.</p></div>
      </div>
      <h2>FAQ</h2>
      <details><summary>Différence avec le sarking ?</summary><p>Combles perdus = volume non habitable, isolation au sol du comble. Sarking = isolation par l’extérieur, souvent pour combles aménagés ou à préserver en hauteur.</p></details>
      <details><summary>Puis-je aménager plus tard ?</summary><p>Si l’espace redevient habitable, la logique change : le site parle alors d’isolation des combles aménagés par l’extérieur.</p></details>
      <p><a class="btn btn-primary" href="../contact.html">Demander un devis combles</a></p>
    </div>
  </section>
""",
)

service_page(
    "velux",
    "Installation et remplacement de Velux — SCZI Isère",
    "Pose, remplacement, jumelage et création de fenêtres de toit Velux. Exemples de chantiers : transformation de débarras, duo 134/140. Seyssinet-Pariset.",
    "Velux",
    "Plus de lumière sous les combles, sans construire un chien assis.",
    image="chantiers/velux-apres.jpg",
    body_inner="""
  <section class="section section-alt">
    <div class="wrap split">
      <div>
        <p class="lede">Les châssis de toit Velux sont présentés sur le site comme la solution la plus performante pour le gain de luminosité et l’aménagement de comble, et moins onéreuse que la création d’un chien assis.</p>
        <p>Le texte historique les décrit aussi comme la menuiserie de série la plus performante du marché en isolation thermique, avec une comparaison de coefficients : norme alors citée pour l’éligibilité au crédit d’impôt Uw = 1,4 et Sw = 0,23 ; Velux Uw = 1,1 et Sw = 0,23 (plus le Uw se rapproche de 1, meilleure est l’isolation, selon la page).</p>
        <div class="todo-fill"><strong>Performances à recaler</strong> Les Uw / Sw et les règles d’aides ont pu changer. Vérifier la gamme réellement posée (manuel, motorisé, Integra Solar) au moment du devis.</div>
      </div>
      <img src="../assets/img/chantiers/velux-apres.jpg" alt="Velux après pose, chantier SCZI">
    </div>
  </section>
  <section class="section">
    <div class="wrap grid-2">
      <div>
        <h2>Integra Solar, tel que décrit</h2>
        <p>Le modèle Integra Solar est présenté avec des capteurs qui actionnent la ventilation en cas de trop forte humidité ou de fort taux de CO₂, et se referment à la détection de pluie. Une tablette Velux permet de programmer ouvertures, fermetures, volet extérieur, et d’autres appareils télécommandés Somfy, dans une limite de 60 appareils.</p>
        <p>Le site invite aussi à remplacer un ancien châssis « qui double la chaleur du soleil » et s’éloigne des performances actuelles.</p>
      </div>
      <div>
        <h2>Chantiers publiés</h2>
        <ul>
          <li>Transformation d’un débarras en chambre et réalisation de chevrette de panne pour pose d’un Velux.</li>
          <li>Aile droite : agrandissement d’un Velux 114/118 en jumelage après réfection totale de toiture ; aile gauche : changement de Velux. Isolation par l’extérieur en laine de bois 2 × 120 mm croisées, R = 6,30.</li>
          <li>Création de Velux en duo 134/140 ainsi que 134/98.</li>
        </ul>
        <p class="credit">Légende Velux : largeur × hauteur en centimètres (exemple 114 × 118).</p>
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
        <div class="step"><h3>Chevrette si besoin</h3><p>Le site documente une chevrette de panne lorsque la structure ne permet pas une pose directe.</p></div>
        <div class="step"><h3>Étanchéité</h3><p>Raccord de toiture, abergement, isolation périphérique : le châssis n’est pas une simple menuiserie posée dans un trou.</p></div>
      </div>
      <h2>FAQ</h2>
      <details><summary>Peut-on poser un Velux sans refaire tout le toit ?</summary><p>Oui, des remplacements isolés sont décrits (aile gauche). Un jumelage a aussi été fait « suite à une réfection totale ».</p></details>
      <details><summary>Pourquoi pas un chien assis ?</summary><p>Le site présente le Velux comme moins onéreux, tout en apportant lumière et confort d’aménagement.</p></details>
      <p><a class="btn btn-primary" href="../contact.html">Demander un devis Velux</a></p>
    </div>
  </section>
""",
)

service_page(
    "zinguerie",
    "Zinguerie, chéneaux et abergements — SCZI Seyssinet-Pariset",
    "Habillages et abergements de cheminée, chéneaux, planches de rive, bandeaux et joints debout. Savoir-faire zinc de SCZI en Isère.",
    "Zinguerie",
    "Le zinc tient l’eau là où les tuiles s’arrêtent.",
    image="chantiers/lucarne-pendant.jpg",
    body_inner="""
  <section class="section section-alt">
    <div class="wrap split">
      <div>
        <p class="lede">Le site d’accueil ne consacre pas de menu à la zinguerie, mais il en décrit déjà les ouvrages : habillages et abergements de cheminée, pose de chéneaux, habillages de planches de rive et de bandeaux, toitures en joints debout. L’expérience « plus de 10 ans en zinguerie » est affichée en tête.</p>
        <p>La réfection de lucarne en joint debout cuivre montre le niveau d’ouvrage : le métal n’est pas un accessoire, c’est la ligne d’eau du toit.</p>
      </div>
      <img src="../assets/img/chantiers/lucarne-pendant.jpg" alt="Pose de zinc / cuivre en lucarne, chantier SCZI">
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
      <div class="todo-fill"><strong>À compléter</strong> Métaux proposés au catalogue (zinc naturel, quartz, cuivre, aluminium), garanties de patine, exemples de chéneaux récents avec date.</div>
      <div class="steps" style="margin-top:1.2rem">
        <div class="step"><h3>Relevé des ouvrages</h3><p>Cheminées, noues, rives, lucarnes : on liste les points d’eau avant de parler couleur de tuile.</p></div>
        <div class="step"><h3>Façonnage</h3><p>Les photos de lucarne montrent un travail de plateau, pas seulement des accessoires du commerce.</p></div>
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
    "Couverture, sarking, combles perdus, Velux et zinguerie : les métiers de SCZI à Seyssinet-Pariset, Isère.",
    "services",
    prefix="../",
    image="assets/img/chantiers/lucarne-pendant.jpg",
    body="""
  <section class="page-hero wrap">
    <p class="kicker">Services</p>
    <h1>Le toit, l’isolant, le zinc, la lumière.</h1>
    <p class="lede">Cinq pages de métier, construites à partir des textes et photos de sczi-renov38.fr — rédigées plus longuement, sans inventer de prix ni de labels.</p>
  </section>
  <section class="section section-alt">
    <div class="wrap grid-2">
      <article class="card"><a class="stretched" href="toiture.html"><img src="../assets/img/chantiers/lucarne-apres.jpg" alt="Réfection de lucarne"><div class="card-body"><h3>Toiture</h3><p>Neuf, réfection, tuiles, écailles, ardoise, bac acier, joints debout.</p></div></a></article>
      <article class="card"><a class="stretched" href="isolation-sarking.html"><img src="../assets/img/chantiers/sarking-1054.jpg" alt="Sarking"><div class="card-body"><h3>Isolation sarking</h3><p>Isoler par l’extérieur lors d’une réfection, R = 6,30 sur les exemples publiés.</p></div></a></article>
      <article class="card"><a class="stretched" href="isolation-combles.html"><img src="../assets/img/stock/isolation-laine.jpg" alt="Isolation"><div class="card-body"><h3>Combles perdus</h3><p>Laine de roche soufflée, tableau de résistances thermiques historique.</p></div></a></article>
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
    ("mur-pignon-1.jpg", "Mur pignon — chantier SCZI"),
    ("mur-pignon-2.jpg", "Mur pignon — chantier SCZI"),
    ("img-0091.jpg", "Chantier SCZI"),
    ("img-0427.jpg", "Chantier SCZI"),
    ("img-0422.jpg", "Chantier SCZI"),
    ("img-0153.jpg", "Chantier SCZI"),
    ("img-0135.jpg", "Chantier SCZI"),
    ("img-0110.jpg", "Chantier SCZI"),
    ("img-0108.jpg", "Chantier SCZI"),
    ("img-0064.jpg", "Chantier SCZI"),
    ("img-0058.jpg", "Chantier SCZI"),
    ("img-0054.jpg", "Chantier SCZI"),
    ("img-0042.jpg", "Chantier SCZI"),
    ("img-0039.jpg", "Chantier SCZI"),
    ("img-0032.jpg", "Chantier SCZI"),
    ("img-0651.jpg", "Chantier SCZI"),
    ("img-0638.jpg", "Chantier SCZI"),
    ("img-0593.jpg", "Chantier SCZI"),
    ("img-0590.jpg", "Chantier SCZI"),
    ("img-0561.jpg", "Chantier SCZI"),
    ("img-0530.jpg", "Chantier SCZI"),
    ("img-0515.jpg", "Chantier SCZI"),
    ("img-0284.jpg", "Chantier SCZI"),
    ("img-0246.jpg", "Chantier SCZI"),
    ("img-0241.jpg", "Chantier SCZI"),
    ("img-0086.jpg", "Chantier SCZI"),
    ("img-0059.jpg", "Chantier SCZI"),
    ("img-0056.jpg", "Chantier SCZI"),
    ("img-0052.jpg", "Chantier SCZI"),
    ("img-0050.jpg", "Chantier SCZI"),
    ("img-0021.jpg", "Chantier SCZI"),
    ("img-0009.jpg", "Chantier SCZI"),
    ("img-0003.jpg", "Chantier SCZI"),
    ("dsc-0037.jpg", "Chantier SCZI"),
    ("fullsizer.jpg", "Chantier SCZI"),
    ("sans-titre-5.jpg", "Chantier SCZI"),
    ("sans-titre-2.jpg", "Chantier SCZI"),
]

figs = "\n".join(
    f'<figure><a href="assets/img/chantiers/{fn}"><img src="assets/img/chantiers/{fn}" alt="{cap}"></a><figcaption>{cap}</figcaption></figure>'
    for fn, cap in GALLERY_ITEMS
)

page(
    "realisations.html",
    "Réalisations toiture et isolation — galerie SCZI",
    "Galerie des photos de chantiers publiées sur sczi-renov38.fr : lucarnes, Velux, sarking, Eybens, Saint-Nazaire.",
    "realisations.html",
    body=f"""
  <section class="page-hero wrap">
    <p class="kicker">Réalisations</p>
    <h1>Les toits déjà photographiés.</h1>
    <p class="lede">Toutes les photos ci-dessous viennent de la médiathèque du site actuel. Les légendes précises du thème (avant/après, Eybens, Saint-Nazaire, cotes Velux) sont reprises quand elles existaient. Les autres clichés sont simplement titrés « Chantier SCZI » — sans inventer de commune ni de date.</p>
  </section>
  <section class="section section-alt">
    <div class="wrap">
      <div class="todo-fill" style="margin-bottom:1.2rem"><strong>À compléter</strong> Année, commune, type d’ouvrage et matériel pour chaque photo encore titrée « Chantier SCZI ». Ajouter des avant/après récents si vous en avez.</div>
      <div class="gallery" data-gallery>
        {figs}
      </div>
      <p class="credit" style="margin-top:1rem">Le visuel de toit végétalisé (EVA Lanxmeer) du site historique est une photo d’illustration tierce ; il n’est pas affiché ici comme chantier SCZI.</p>
    </div>
  </section>
""",
)

page(
    "zone-intervention.html",
    "Zone d’intervention SCZI — Seyssinet-Pariset, Grenoble, Isère",
    "SCZI est implantée à Seyssinet-Pariset, à 5 km de Grenoble. Chantiers documentés à Eybens et Saint-Nazaire. Zone d’intervention en Isère à préciser.",
    "zone-intervention.html",
    body=f"""
  <section class="page-hero wrap">
    <p class="kicker">Territoire</p>
    <h1>Depuis Seyssinet-Pariset, vers les toits de l’agglomération.</h1>
    <p class="lede">L’entreprise est implantée à Seyssinet-Pariset dans l’Isère, à 5 km de Grenoble. C’est la seule zone d’implantation officiellement écrite.</p>
  </section>
  <section class="section section-alt">
    <div class="wrap split">
      <div>
        <h2>Ce qui est établi</h2>
        <ul>
          <li>Siège : {ADDRESS}</li>
          <li>Positionnement : 5 km de Grenoble</li>
          <li>Département : Isère (38)</li>
          <li>Chantier nommé : toiture de maison à <strong>Eybens</strong></li>
          <li>Chantier nommé : isolation et toiture à <strong>Saint-Nazaire</strong> (libellé du site, sans plus de précision administrative)</li>
        </ul>
        <div class="todo-fill">
          <strong>Rayon d’intervention à compléter</strong>
          Le site ne publie pas de liste de communes ni de rayon (20 km, 40 km, Chartreuse, Vercors, Grésivaudan…). N’indiquez ici que les secteurs où vous vous déplacez réellement.
        </div>
      </div>
      <div class="map-placeholder">
        <div>
          <strong>Seyssinet-Pariset</strong>
          <p style="margin:0">666 Route de Saint Nizier · 38170</p>
        </div>
      </div>
    </div>
  </section>
  <section class="section">
    <div class="wrap">
      <h2>Pourquoi le climat local compte</h2>
      <p>Sans prétendre à une étude climatique, le métier décrit (tuiles écailles, zinc, sarking, laine soufflée) répond à des toits exposés au froid, à la neige et aux écarts thermiques de l’agglomération grenobloise. L’isolation par l’extérieur et les combles perdus y sont présentés comme des leviers d’économie de chauffage.</p>
      <img src="assets/img/stock/paysage-alpes.jpg" alt="Paysage alpin, illustration de l’environnement isérois" style="border-radius:18px;margin:1rem 0;max-height:22rem;width:100%;object-fit:cover">
      <p class="credit">Photo stock : Pexels — James Wheeler. Ne représente pas le siège.</p>
      <p><a class="btn btn-primary" href="contact.html">Indiquer le lieu des travaux</a></p>
    </div>
  </section>
""",
)

page(
    "contact.html",
    "Devis toiture et isolation — contact SCZI Seyssinet-Pariset",
    "Demandez un devis SCZI : nom, téléphone, e-mail, lieu des travaux, budget estimé, besoins. Téléphone 04 38 70 03 94. Seyssinet-Pariset (38).",
    "contact.html",
    body=f"""
  <section class="page-hero wrap">
    <p class="kicker">Contact</p>
    <h1>Un devis, à partir du toit que vous décrivez.</h1>
    <p class="lede">Les champs sont ceux du formulaire Gravity Forms du site actuel. Aucun envoi n’est encore relié à une boîte mail réelle : voyez le bandeau ci-dessous.</p>
  </section>
  <section class="section section-alt">
    <div class="wrap contact-layout">
      <form class="form" id="devis-form" action="https://formspree.io/f/xxxxxxxx" method="POST">
        <div class="todo-fill" id="form-fallback">
          <strong>E-mail et Formspree à brancher</strong>
          Sur sczi-renov38.fr, le lien e-mail du thème est <code>mailto:your@email</code> — ce n’est pas une adresse réelle. Remplacez <code>xxxxxxxx</code> par un identifiant Formspree, ou basculez le <code>action</code> vers un mailto définitif. En l’état, la soumission ouvre un brouillon vers une adresse factice.
        </div>
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
        <p class="credit">En envoyant ce formulaire, vous acceptez d’être recontacté au sujet de votre projet. Voir les <a href="mentions-legales.html">mentions légales</a>.</p>
        <button class="btn btn-primary" type="submit">Envoyer</button>
      </form>
      <aside class="contact-card">
        <h2>Coordonnées publiées</h2>
        <dl>
          <dt>Téléphone</dt>
          <dd><a href="tel:{PHONE_TEL}">{PHONE}</a></dd>
          <dt>Siège</dt>
          <dd>{ADDRESS}</dd>
          <dt>Gérant</dt>
          <dd>SCHUBERT Eric</dd>
          <dt>E-mail</dt>
          <dd class="todo-fill" style="color:#5c3b16">Non publié sur le site actuel.</dd>
          <dt>Horaires</dt>
          <dd class="todo-fill" style="color:#5c3b16">Non indiqués sur le site actuel.</dd>
        </dl>
      </aside>
    </div>
  </section>
""",
)

page(
    "mentions-legales.html",
    "Mentions légales — Schubert Couverture Zinguerie Isolation",
    "Mentions légales SCZI : SIRET 75106621800023, RCS Grenoble B 751 066 218, siège 666 Route de Saint Nizier, 38170 Seyssinet-Pariset, tél. 04 38 70 03 94.",
    "mentions",
    body=f"""
  <section class="page-hero wrap">
    <p class="kicker">Informations légales</p>
    <h1>Mentions légales</h1>
    <p class="lede">Texte repris des mentions du site sczi-renov38.fr, nettoyé des shortcodes de thème et d’un bloc visiblement copié-collé (adresse « 20 Minutes France ») qui ne concerne pas SCZI.</p>
  </section>
  <section class="section section-alt">
    <div class="wrap" style="max-width:48rem">
      <h2>Éditeur</h2>
      <p>La société SCHUBERT COUVERTURE ZINGUERIE<br>
      SIRET {SIRET}<br>
      RCS Ville tribunal : {RCS}<br>
      Siège social : 666 Route de Saint Nizier — 38170 Seyssinet-Pariset<br>
      Téléphone : {PHONE}<br>
      Directeur de la publication : la société SCHUBERT COUVERTURE ZINGUERIE</p>
      <div class="todo-fill"><strong>À compléter</strong> E-mail de contact, forme juridique, capital social, n° TVA, hébergeur de ce dépôt GitHub Pages (GitHub, Inc. — à confirmer dans vos CGU), responsable du traitement RGPD nommément.</div>

      <h2>Hébergement de cette proposition</h2>
      <p>Ce site statique est conçu pour être servi par GitHub Pages à partir du dépôt du projet. L’hébergeur du site historique (WordPress / nginx sur sczi-renov38.fr) n’est pas nommé dans les mentions d’origine.</p>

      <h2>Données personnelles</h2>
      <p>La société SCHUBERT COUVERTURE ZINGUERIE n’enregistre pas d’informations personnelles permettant l’identification, à l’exception des formulaires que l’utilisateur est libre de remplir. Ces informations ne seront pas utilisées sans votre accord ; elles servent à vous adresser des courriers, des brochures, des devis ou à vous contacter.</p>
      <p>Les informations recueillies bénéficient de la protection de la loi « Informatique et Libertés » n° 78-17 du 6 janvier 1978. Droit d’accès, de rectification, d’opposition et de suppression sur simple demande à SCHUBERT COUVERTURE ZINGUERIE, 666 Route de Saint Nizier — 38170 Seyssinet-Pariset.</p>
      <p>La société peut procéder à des analyses statistiques non nominatives et en informer des tiers (organismes d’évaluation de fréquentation) sous forme résumée et non nominative.</p>
      <p>Cette proposition statique n’installe pas, par défaut, de cookies de mesure d’audience. Le bandeau cookies du site WordPress actuel n’est donc pas reproduit tant qu’aucun traceur n’est ajouté.</p>

      <h2>Création graphique</h2>
      <p>La création graphique du site historique a été réalisée par Thomas BONSIRVEN. La présente refonte est une proposition de site statique distincte.</p>

      <h2>Liens hypertexte</h2>
      <p>La société SCHUBERT COUVERTURE ZINGUERIE ne contrôle pas les sites en connexion avec le sien, et ne saurait donc être responsable de leur contenu.</p>

      <h2>Propriété des photographies</h2>
      <p>Les photos de chantiers proviennent de la médiathèque de sczi-renov38.fr. Les photos de stock (Unsplash, Pexels) sont créditées dans <a href="assets/img/stock/CREDITS.txt">assets/img/stock/CREDITS.txt</a>.</p>
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
