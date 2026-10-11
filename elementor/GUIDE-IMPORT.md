# Guide d’import Elementor — site SCZI

Objectif : remplacer demain le thème **Flatsome** (UX Builder) de [sczi-renov38.fr](https://sczi-renov38.fr/) par **Hello Elementor** + **Elementor** + **Elementor Pro**, **uniquement** en important les templates et pages de ce dossier. Pas de sur-design.

Les JSON sont au format Elementor *Templates > Export* (`version: "0.4"`). Les images pointent vers les copies GitHub Pages (`https://thomasbonsirven.github.io/sczi38/assets/img/...`) pour le sideload à l’import. Un zip des fichiers est aussi fourni pour un upload manuel.

---

## 0. Contenu du dossier

```
elementor/
  GUIDE-IMPORT.md          ← ce fichier
  WIDGETS.md
  json/                    ← 18 fichiers .json à importer
  images/                  ← copies locales des visuels
  images-media.zip         ← mêmes images, pour Médias > Ajouter
  sczi-elementor-import.zip
  build.py                 ← régénération (facultatif)
```

JSON Theme Builder : `header.json`, `footer.json`.  
Sections réutilisables : `section-qualibat-rge.json`, `section-cta-devis.json`, `section-zone.json`.  
Pages : `page-accueil.json`, `page-entreprise.json`, `page-services.json`, `page-toiture.json`, `page-sarking.json`, `page-combles.json`, `page-velux.json`, `page-zinguerie.json`, `page-realisations.json`, `page-zone.json`, `page-contact.json`, `page-mentions-legales.json`, `page-credits.json`.

---

## 1. Sauvegarde (avant tout)

1. **Extensions > Ajouter** : installer **UpdraftPlus** (ou duplicator) et lancer une sauvegarde complète (fichiers + base).
2. Exporter aussi **Outils > Exporter** : Pages, Médias, Menus.
3. Dans Flatsome : noter les pages publiées (URLs ci-dessous, § 9).
4. Télécharger une copie zip du site (hébergeur) si possible.

Ne pas désactiver Flatsome **avant** d’avoir Hello + Elementor + Pro actifs et les templates importés.

---

## 2. Installer Hello Elementor + Elementor + Elementor Pro

1. **Extensions > Ajouter** : installer et activer **Elementor**.
2. Installer et activer **Elementor Pro** (licence existante : *Elementor > Licence*).
3. **Apparence > Thèmes > Ajouter** : installer **Hello Elementor**, **ne pas encore l’activer**.
4. Vérifier : PHP ≥ 8, mémoire WP ≥ 256 Mo.

---

## 3. Passer de Flatsome à Hello (fenêtre courte)

1. Activer **Hello Elementor**.
2. **Extensions** : désactiver **Flatsome** (thème enfant s’il y en a un) et tout plugin **UX Builder / Flatsome** (UX Blocks, etc.).
3. Ne pas supprimer tout de suite : on pourra revenir en arrière avec la sauvegarde.
4. *Réglages > Permalinks* : choisir **Nom de l’article**, enregistrer deux fois.

Le site peut être laid quelques minutes : en-tête/pied Flatsome disparaissent. Enchaîner l’import.

---

## 4. Couleurs et polices du Kit

*Elementor > Réglages du site* (icône hamburger de l’éditeur, ou *Kit*) :

| Jeton | Valeur |
|---|---|
| Primaire | `#C8102E` |
| Texte | `#1C1612` |
| Fond | `#F7F2EA` |
| Titres | Fraunces (Google Fonts) ou Georgia |
| Corps | Source Sans 3 ou « System » |

Largeur de contenu : **1140 px**.

---

## 5. Menu WordPress (sous-menu Services)

Le widget **Nav Menu** de l’en-tête attend un menu nommé exactement **`Menu principal`**.

*Apparence > Menus* :

1. Créer le menu **Menu principal**, l’assigner à l’emplacement Hello / Elementor si proposé.
2. Structure (pages à créer au § 7, ou liens perso en attendant) :

```
Accueil                  → /
L’entreprise             → /entreprise/
Services                 → /services/
  ├ Toiture              → /toiture/
  ├ Isolation sarking    → /isolation-sarking/
  ├ Combles perdus       → /isolation-combles-perdus/
  ├ Velux                → /installation-velux/
  └ Zinguerie            → /zinguerie/
Réalisations             → /realisations/
Zone d’intervention      → /zone-intervention/
Devis                    → /contact/
```

Le sous-menu Services est un **menu WP classique** (entrée parente + enfants). Elementor Pro affiche le dropdown tout seul.

---

## 6. Importer les templates

*Modèles > Modèles enregistrés > Importer des modèles* (ou *Templates > Saved Templates > Import*).

Importer **dans cet ordre** :

1. `header.json` (type header)
2. `footer.json` (type footer)
3. `section-qualibat-rge.json`, `section-cta-devis.json`, `section-zone.json`
4. Tous les `page-*.json`

Si une image ne se sideloade pas : importer `images-media.zip` via *Médias > Ajouter* (dézipper d’abord), puis remplacer l’image dans le widget.

À l’import, Elementor attribue de nouveaux IDs internes : c’est normal.

---

## 7. Theme Builder : header et footer sur tout le site

1. *Modèles > Theme Builder*.
2. **En-tête** : le template **SCZI — En-tête**. Condition : **Entire Site** / Site entier. Publier.
3. **Pied de page** : **SCZI — Pied de page**. Condition : Site entier. Publier.
4. Désactiver / ne pas publier d’anciens headers Flatsome s’ils réapparaissent.

---

## 8. Créer les pages WordPress et coller le contenu

Pour chaque ligne : *Pages > Ajouter*, titre + permaliens (slug), *Modifier avec Elementor*, *Ajouter un modèle* (icône dossier) > onglet *Mes modèles* > insérer le JSON de page correspondant. Publier.

| Titre WP | Slug | JSON |
|---|---|---|
| Accueil | (laisser vide ou `accueil`) | `page-accueil.json` |
| L’entreprise | `entreprise` | `page-entreprise.json` |
| Services | `services` | `page-services.json` |
| Toiture | `toiture` | `page-toiture.json` |
| Isolation sarking | `isolation-sarking` | `page-sarking.json` |
| Combles perdus | `isolation-combles-perdus` | `page-combles.json` |
| Installation Velux | `installation-velux` | `page-velux.json` |
| Zinguerie | `zinguerie` | `page-zinguerie.json` |
| Réalisations | `realisations` | `page-realisations.json` |
| Zone d’intervention | `zone-intervention` | `page-zone.json` |
| Contact | `contact` | `page-contact.json` |
| Mentions légales | `mentions-legales` | `page-mentions-legales.json` |
| Crédits & informations | `credits` | `page-credits.json` |

Si une page Flatsome existe déjà (ex. `/toiture/`, `/contact/`, `/mentions-legales/`) : l’ouvrir, *Modifier avec Elementor*, vider le canevas Flatsome, insérer le nouveau modèle, publier. Cela conserve l’URL.

**Formulaire** (*page-contact*) : *Elementor Pro > Formulaire* → Actions après envoi = E-mail. Mettre l’adresse réelle dès qu’elle est connue (aujourd’hui absente du site). Message de succès déjà rédigé (renvoi vers le 04 38 70 03 94).

**Carte** : le widget Google Maps a besoin d’une clé API (*Elementor > Réglages > Intégrations*).

---

## 9. Page d’accueil

*Réglages > Lecture* : « Une page statique » → **Accueil**. Les articles de blog : aucune (ou une page vide non liée).

---

## 10. Redirections 301 (URLs Flatsome → nouveaux slugs)

Ancien site crawlé (16 pages Rank Math / WP). Plugin **Redirection** ou **Rank Math > Redirections**.

| Ancienne URL | Nouvelle URL |
|---|---|
| `/` | `/` (page Accueil) |
| `/installation-velux/` | `/installation-velux/` |
| `/installation-velux-2/` | `/installation-velux/` |
| `/isolation-combles-perdu/` | `/isolation-combles-perdus/` |
| `/isolation-combles-perdu-2/` | `/isolation-combles-perdus/` |
| `/isolation-toiture-exterieur-sarking/` | `/isolation-sarking/` |
| `/isolation-toiture-exterieur-ou-sarking-2/` | `/isolation-sarking/` |
| `/toiture/` | `/toiture/` |
| `/toiture-2-2/` | `/toiture/` |
| `/toiture-renovation/` | `/toiture/` |
| `/contact/` | `/contact/` |
| `/contact2/` | `/contact/` |
| `/mentions-legales/` | `/mentions-legales/` |
| `/sczi-toiture-isolation/` | `/` |
| `/sczi-isolation-toiture-sarking-zinguerie/` | `/` |
| `/test/` | `/` |

Pages nouvelles (pas d’ancienne URL) : `/entreprise/`, `/services/`, `/zinguerie/`, `/realisations/`, `/zone-intervention/`, `/credits/`.

Ne pas rediriger `/wp-content/uploads/…` (médias).

---

## 11. Cache

1. Purger le cache de l’extension (WP Rocket, LiteSpeed, etc. si présente).
2. Purger le cache hébergeur / Cloudflare.
3. Tester en navigation privée.

---

## 12. Checklist de mise en ligne

- [ ] Sauvegarde UpdraftPlus OK
- [ ] Hello Elementor + Elementor + Elementor Pro actifs
- [ ] Flatsome et UX Builder désactivés
- [ ] Kit : rouge `#C8102E`, fond `#F7F2EA`
- [ ] Menu **Menu principal** avec sous-menu Services
- [ ] Header / footer Theme Builder = Site entier
- [ ] 13 pages importées, slugs ci-dessus
- [ ] Accueil définie dans Lecture
- [ ] Formulaire : destinataire e-mail réel (dès qu’il existe)
- [ ] Clé Google Maps
- [ ] 301 des 16 anciennes URLs
- [ ] Permaliens réenregistrés
- [ ] Cache vidé
- [ ] Parcours téléphone : accueil → Services (dropdown) → Toiture → Devis
- [ ] Mobile : burger + sous-menu Services
- [ ] Mentions légales : remplacer « GitHub Pages » par l’hébergeur WP réel (liste à fournir, page Crédits)
- [ ] Pied de page : adresse 4290 route Napoléon, 38320 Brié-et-Angonnes ; tél. 04 38 70 03 94 ; liens Mentions + Crédits
- [ ] Accueil : chip « Qualibat RGE depuis 2016 », frise macarons 2016 et 2016–2017 seulement (pas d’images inventées)

---

## 13. En cas de problème

- **Menu vide** : le nom du menu n’est pas exactement `Menu principal`, ou le menu n’est pas créé.
- **Header Flatsome qui revient** : un ancien template Theme Builder est encore publié — le désactiver.
- **Images cassées** : uploader `images-media.zip`, puis dans chaque widget Image cliquer *Upload*.
- **JSON refusé** : importer via *Modèles > Import*, pas via l’importateur WordPress WXR.
- **Retour arrière** : réactiver Flatsome + restauration UpdraftPlus.
