# Widgets Elementor requis — SCZI

Import prévu pour **Hello Elementor** + **Elementor** + **Elementor Pro**. Conteneurs Flexbox uniquement (pas de sections/colonnes legacy).

## Elementor (gratuit)

| Widget (`widgetType`) | Où |
|---|---|
| **Heading** (`heading`) | Titres, kickers, chip Qualibat |
| **Text Editor** (`text-editor`) | Textes client, listes HTML |
| **Image** (`image`) | Logo, photos chantiers, macarons Qualibat, paysage |
| **Button** (`button`) | CTA « Demander un devis », liens secondaires |
| **Icon List** (`icon-list`) | Coordonnées, menus footer, listes d’identité |
| **Icon Box** (`icon-box`) | Faits (20 ans, RGE, étapes, aides) |
| **Image Box** (`image-box`) | Cartes métiers (accueil, hub Services, sarking) |
| **Accordion** (`accordion`) | FAQ (toiture, sarking, combles, Velux) + schéma FAQ |
| **Google Maps** (`google_maps`) | Zone d’intervention / siège |
| **HTML** (`html`) | Tableau laine de roche (page combles) |
| **Divider** / **Spacer** | Non utilisés (marges via padding des conteneurs) |

Conteneur : **Container** Flexbox (`elType: container`, `container_type: flex`).

## Elementor Pro

| Widget / fonction | Où | Obligatoire |
|---|---|---|
| **Nav Menu** (`nav-menu`) | En-tête Theme Builder | Oui — menu WP « Menu principal » (sous-menu Services) |
| **Form** (`form`) | Page Devis / contact | Oui |
| **Gallery** (`gallery`) | Accueil (extrait), Toiture, Velux, Réalisations | Oui (sinon remplacer par Image Carousel gratuit, moins adapté) |
| **Theme Builder** | Conditions header / footer « Entire Site » | Oui |
| **Kit / styles globaux** | Couleurs et polices | Recommandé |

## Fonctions WordPress (hors widgets)

- **Apparence > Menus** : menu nommé exactement `Menu principal` (le widget Nav Menu le référence par `menu_name`).
- **Réglages > Lecture** : page Accueil en page d’accueil statique.
- **Permaliens** : structure « Nom de l’article ».
- **Redirections 301** : plugin Redirection ou Rank Math (déjà présent sur l’ancien site).

## Couleurs / polices à poser dans le Kit Elementor

- Primaire / accents : `#C8102E`
- Texte : `#1C1612`
- Fond : `#F7F2EA` et blanc `#FFFFFF`
- Titres : Fraunces (ou Georgia en secours)
- Corps : Source Sans 3 (ou system-ui)

Ne pas activer WooCommerce. Atomic / Elementor 4 n’est pas requis.
