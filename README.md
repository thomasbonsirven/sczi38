# SCZI — proposition de site statique

Site vitrine HTML/CSS/JS (sans étape de build) pour **Schubert Couverture Zinguerie Isolation** (SCZI), artisan couvreur à Brié-et-Angonnes (Isère, 38).

Proposition destinée à [GitHub Pages](https://docs.github.com/fr/pages), à partir du dépôt `thomasbonsirven/sczi38`. Elle remplace le WordPress actuel [sczi-renov38.fr](https://sczi-renov38.fr/), trop pauvre pour un métier de toiture : menus inachevés, e-mail factice, pages doublons Avada/Divi, mentions copiées-collées.

**URL prévue après activation de Pages :**  
https://thomasbonsirven.github.io/sczi38/

---

## Pages

| Fichier | Rôle |
| --- | --- |
| `index.html` | Accueil, métiers, labels, extraits de chantiers |
| `a-propos.html` | Entreprise, gérant, identité légale |
| `services/index.html` | Hub des métiers |
| `services/toiture.html` | Toiture neuve / réfection, lucarnes, tarif 2018 |
| `services/isolation-sarking.html` | Sarking / isolation par l’extérieur |
| `services/isolation-combles.html` | Combles perdus, tableau laine de roche |
| `services/velux.html` | Pose, remplacement, jumelage Velux |
| `services/zinguerie.html` | Cheminées, chéneaux, rives, joints debout |
| `realisations.html` | Galerie des chantiers |
| `zone-intervention.html` | De Noyarey à Crolles, via Brié-et-Angonnes et Grenoble |
| `contact.html` | Formulaire de devis |
| `mentions-legales.html` | Mentions légales |
| `credits.html` | Crédits photos et informations à fournir (lien discret en pied de page) |
| `404.html` | Page d’erreur GitHub Pages |
| `sitemap.xml` / `robots.txt` | SEO |

Les chemins sont **relatifs** : le site fonctionne à la racine d’un domaine ou sous `/sczi38/`.

---

## Ce qui vient du site actuel

Crawl de https://sczi-renov38.fr/ (WordPress Flatsome, sitemap Rank Math, API REST).

**Faits du site actuel, complétés par le gérant :**

- Enseigne : Schubert Couverture Zinguerie Isolation / SCZI / SCZI Toiture / SCZI Bâtiment
- Gérant : SCHUBERT Eric
- Implantation : Brié-et-Angonnes, Isère (38)
- Siège (mentions légales, JSON-LD, pied de page) : 4290 route Napoléon, 38320 Brié-et-Angonnes
- Zone d’intervention : de Noyarey à Crolles, en passant par Brié-et-Angonnes et Grenoble
- Téléphone : 04 38 70 03 94
- SIRET 75106621800023 · RCS Grenoble B 751 066 218
- Plus de 20 ans d’expérience en zinguerie, charpente, sarking et Velux
- Certification Qualibat depuis 2016, renouvelée jusqu’en 2026 (10 ans de performance et de qualité sur chantier) ; entreprise 100 % RGE
- Supports : tuiles, tuiles écailles, bac acier, ardoise, joints debout
- Normes DTU et CSTB
- Ouvrages : abergements / habillages de cheminée, chéneaux, planches de rive, bandeaux, Velux
- Isolation combles non aménageables par laine de roche soufflée ; combles aménagés par l’extérieur
- Revendication RGE + Qualibat, TVA 5,5 % et (à l’époque) crédit d’impôt 30 %
- Durées de vie toiture / étanchéité et prix neuf « à partir de 65 €/m² » (120 m², sans Velux ni cheminée)
- Exemples sarking R = 6,30 (laine de bois, double 120 mm, GR32 2×100 mm)
- Tableau de laine de roche soufflée, seuil R = 7
- Chantiers nommés : lucarne tuile écaille / joint debout cuivre ; Velux (cotes, duo, Eybens / Saint-Nazaire sur d’autres pages)
- Création graphique du site historique : Thomas BONSIRVEN
- Photos de la médiathèque WordPress, téléchargées dans `assets/img/chantiers/`, `assets/img/logo/`, `assets/img/badges/`

**Pages WordPress ignorées** (lorem ipsum thème Avada, doublons Divi/Fusion cassés, page `test`) : `toiture-renovation`, `toiture-2-2`, `isolation-*-2`, `installation-velux-2`, `sczi-isolation-toiture-sarking-zinguerie` (vide).

---

## Placeholders à compléter

Ces points ne figurent plus sur les pages publiques : ils sont listés ici et sur `credits.html` (lien « Crédits & informations » en pied de page). Rien de ce qui suit n’était publié de façon fiable sur sczi-renov38.fr :

1. **E-mail professionnel** (le thème pointe vers `mailto:your@email`)
2. **Formspree** : remplacer `https://formspree.io/f/xxxxxxxx` dans `contact.html`
3. **Horaires** d’accueil / d’appel
4. **Numéros de certificat Qualibat / RGE** (la certification Qualibat 2016–2026 et le 100 % RGE sont confirmés ; les n° ne sont pas encore publiés)
5. **Macarons Qualibat RGE 2018 à 2026** — seuls **2016** (`rge-2016.jpg`) et **2016–2017** (`rge.png`) ont été trouvés (médiathèque WordPress de sczi-renov38.fr, 16 pages, 91 médias, et `assets/img/badges/`). Ne pas fabriquer d’images.
6. **Barèmes chiffrés des aides** (MaPrimeRénov’, CEE, éco-PTZ, TVA 5,5 % sont cités sur l’accueil, sans montants)
7. **Tarifs actualisés** (le 65 €/m² date de la page Toiture ~2018)
8. **Légendes** des photos de chantier encore sans commune ni date
9. **Réseaux sociaux** (liens du thème : `http://url`)
10. **Forme juridique, capital, TVA intra, assurance décennale**
11. **Avis clients** : aucun sur le site actuel — volontairement absents ici
12. Nom d’hébergeur définitif si le domaine sczi-renov38.fr est recollé

Dans le JSON-LD `RoofingContractor`, les champs sourcés (nom, téléphone, adresse à Brié-et-Angonnes, gérant, métiers, zone Noyarey / Brié-et-Angonnes / Grenoble / Crolles / Isère) sont renseignés. Pas d’e-mail, pas de note Google, pas de geo inventée.

---

## Images de stock

Fichiers dans `assets/img/stock/`. Crédits légaux sur `credits.html` (par page) et dans `assets/img/stock/CREDITS.txt` (Unsplash et Pexels, licences libres, copies locales). Elles complètent les vrais chantiers (combles, atmosphère alpine) sans se faire passer pour des photos SCZI.

---

## Activer GitHub Pages

Deux options, au choix.

### A. Actions (recommandé, workflow déjà dans le dépôt)

1. GitHub → **Settings** → **Pages**
2. **Source** : *GitHub Actions*
3. Pousser `main` (ou lancer le workflow *Déploiement GitHub Pages* à la main)
4. Le site est servi à `https://thomasbonsirven.github.io/sczi38/`

Fichier : `.github/workflows/pages.yml`.  
`.nojekyll` empêche Jekyll de filtrer des dossiers.

### B. Branche, racine

1. **Settings** → **Pages**
2. Source : *Deploy from a branch*
3. Branche `main`, dossier `/ (root)`
4. Enregistrer

Pas de `npm` / `bundle` : ouvrir `index.html` ou servir le dossier.

Pour un domaine perso (ex. sczi-renov38.fr) : Settings → Pages → Custom domain, puis mettre à jour `SITE` dans `sitemap.xml`, `robots.txt` et les balises canonical / Open Graph. Les liens internes, relatifs, n’ont pas besoin d’être réécrits.

### Formulaire

1. Créer un formulaire sur [Formspree](https://formspree.io/)
2. Remplacer `xxxxxxxx` dans `contact.html`
3. Ou passer `action` en `mailto:` une fois l’e-mail réel connu

---

## Technique

- HTML + `assets/css/styles.css` + `assets/js/main.js`
- Mobile first, menu, galerie lightbox, `details/summary` pour les FAQ
- `scripts/generate-site.py` régénère le HTML si besoin ; **ce n’est pas requis pour Pages**
- Prévisualisation locale : `python3 -m http.server 8080` à la racine du dépôt
