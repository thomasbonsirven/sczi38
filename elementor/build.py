#!/usr/bin/env python3
"""Génère les JSON Elementor importables du site SCZI (format Templates > Export 0.4)."""
from __future__ import annotations

import hashlib
import json
import shutil
import zipfile
from pathlib import Path

ROOT = Path("/workspace")
OUT = ROOT / "elementor"
JSON_DIR = OUT / "json"
IMG_DIR = OUT / "images"

IMG = "https://thomasbonsirven.github.io/sczi38/assets/img"
RED = "#C8102E"
INK = "#1C1612"
PAPER = "#F7F2EA"
WHITE = "#FFFFFF"
MUTED = "#6B625A"
DARK = "#1C1612"

PHONE = "04 38 70 03 94"
PHONE_TEL = "tel:+33438700394"
ADDRESS = "4290 route Napoléon, 38320 Brié-et-Angonnes"
MAPS = "https://www.google.com/maps/search/?api=1&query=4290+route+Napol%C3%A9on%2C+38320+Bri%C3%A9-et-Angonnes"
MENU = "Menu principal"

_n = 0
_used: set[str] = set()


def nid() -> str:
    global _n
    while True:
        _n += 1
        hid = hashlib.sha1(f"sczi-el-{_n}".encode()).hexdigest()[:8]
        if hid not in _used:
            _used.add(hid)
            return hid


def sz(size, unit="px"):
    return {"size": size, "unit": unit, "sizes": []}


def pad(t, r=None, b=None, l=None, unit="px"):
    if r is None:
        r = b = l = t
    return {"top": str(t), "right": str(r), "bottom": str(b), "left": str(l), "unit": unit, "isLinked": t == r == b == l}


def gap(n):
    return {"unit": "px", "size": n, "column": str(n), "row": str(n), "isLinked": True}


def link(url, external=False):
    return {"url": url, "is_external": "on" if external else "", "nofollow": ""}


def media(path, alt=""):
    url = path if path.startswith("http") else f"{IMG}/{path.lstrip('/')}"
    obj = {"url": url, "id": "", "alt": alt, "source": "url"}
    return obj


def icon(name, lib="fa-solid"):
    return {"value": name, "library": lib}


def widget(wtype, settings):
    return {
        "id": nid(),
        "elType": "widget",
        "widgetType": wtype,
        "settings": settings,
        "elements": [],
    }


def container(settings, children, inner=False, html_tag=""):
    s = {"container_type": "flex", **settings}
    if html_tag:
        s["html_tag"] = html_tag
    return {
        "id": nid(),
        "elType": "container",
        "isInner": inner,
        "settings": s,
        "elements": children,
    }


def boxed(bg, children, extra=None, html_tag="section"):
    s = {
        "content_width": "boxed",
        "boxed_width": sz(1140),
        "flex_direction": "column",
        "flex_gap": gap(20),
        "padding": pad(48, 20, 48, 20),
        "background_background": "classic",
        "background_color": bg,
    }
    if extra:
        s.update(extra)
    return container(s, children, html_tag=html_tag)


def row(children, extra=None, inner=True):
    s = {
        "content_width": "full",
        "flex_direction": "row",
        "flex_wrap": "wrap",
        "flex_gap": gap(20),
        "flex_align_items": "stretch",
    }
    if extra:
        s.update(extra)
    return container(s, children, inner=inner)


def col(children, extra=None):
    s = {
        "content_width": "full",
        "flex_direction": "column",
        "flex_gap": gap(12),
        "width": sz(100, "%"),
    }
    if extra:
        s.update(extra)
    return container(s, children, inner=True)


def heading(text, tag="h2", color=INK, size=None, extra=None):
    s = {"title": text, "header_size": tag, "title_color": color, "align": "start"}
    if size:
        s["typography_typography"] = "custom"
        s["typography_font_size"] = sz(size)
        s["typography_font_weight"] = "700"
    if extra:
        s.update(extra)
    return widget("heading", s)


def kicker(text, color=RED):
    return heading(
        text,
        "p",
        color,
        13,
        extra={
            "typography_text_transform": "uppercase",
            "typography_letter_spacing": sz(1.6),
            "typography_font_weight": "700",
        },
    )


def text(html, color=INK):
    return widget("text-editor", {"editor": html, "text_color": color, "align": "start"})


def btn(label, url, primary=True):
    s = {
        "text": label,
        "link": link(url),
        "size": "md",
        "align": "left",
        "background_background": "classic",
        "border_radius": pad(6),
    }
    if primary:
        s["background_color"] = RED
        s["button_text_color"] = WHITE
        s["button_background_hover_color"] = "#9A0C23"
        s["hover_color"] = WHITE
    else:
        s["background_color"] = WHITE
        s["button_text_color"] = INK
        s["border_border"] = "solid"
        s["border_width"] = pad(1)
        s["border_color"] = "rgba(28,22,18,0.18)"
    return widget("button", s)


def image(path, alt="", extra=None):
    s = {
        "image": media(path, alt),
        "image_size": "full",
        "align": "start",
        "image_border_radius": pad(12),
    }
    if extra:
        s.update(extra)
    return widget("image", s)


def icon_list(items, view="traditional"):
    rows = []
    for text_, url, ic in items:
        row = {"_id": nid(), "text": text_, "selected_icon": icon(ic)}
        if url:
            row["link"] = link(url, url.startswith("http") or url.startswith("tel:"))
        rows.append(row)
    return widget("icon-list", {"icon_list": rows, "view": view})


def icon_box(title, desc, ic="fas fa-check"):
    return widget(
        "icon-box",
        {
            "selected_icon": icon(ic),
            "title_text": title,
            "description_text": desc,
            "title_size": "h3",
            "position": "block-start",
            "primary_color": RED,
            "title_color": INK,
            "description_color": MUTED,
        },
    )


def image_box(path, alt, title, desc, url=""):
    s = {
        "image": media(path, alt),
        "title_text": title,
        "description_text": desc,
        "title_size": "h3",
    }
    if url:
        s["link"] = link(url)
    return widget("image-box", s)


def accordion(pairs):
    tabs = [{"_id": nid(), "tab_title": t, "tab_content": c} for t, c in pairs]
    return widget("accordion", {"tabs": tabs, "title_html_tag": "h3", "faq_schema": "yes"})


def gallery(items):
    return widget(
        "gallery",
        {
            "gallery": [{"id": "", "url": f"{IMG}/chantiers/{fn}"} for fn, _cap in items],
            "gallery_layout": "grid",
            "columns": 3,
            "columns_tablet": 2,
            "columns_mobile": 2,
            "gap": sz(10),
            "link_to": "file",
            "aspect_ratio": "4:3",
            "open_lightbox": "yes",
            "lazyload": "yes",
        },
    )


def template(title, ttype, content, page_settings=None):
    return {
        "version": "0.4",
        "title": title,
        "type": ttype,
        "content": content,
        "page_settings": page_settings or {},
    }


PAGE_SETTINGS = {
    "hide_title": "yes",
    "background_background": "classic",
    "background_color": PAPER,
}


def save(name, data):
    path = JSON_DIR / name
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("wrote", path.relative_to(ROOT), "ids", len(_used))


# ---------- reusable bits ----------

def header_tpl():
    logo = image(
        "logo/logo.png",
        "SCZI Toiture",
        extra={"link_to": "custom", "link": link("/"), "width": sz(140)},
    )
    nav = widget(
        "nav-menu",
        {
            "menu_name": MENU,
            "layout": "horizontal",
            "align_items": "center",
            "pointer": "underline",
            "dropdown": "tablet",
            "toggle": "burger",
            "toggle_align": "right",
            "color_menu_item": INK,
            "color_menu_item_hover": RED,
            "color_menu_item_active": RED,
            "pointer_color_menu_item_hover": RED,
        },
    )
    cta = btn("Demander un devis", "/contact/")
    bar = container(
        {
            "content_width": "boxed",
            "boxed_width": sz(1140),
            "flex_direction": "row",
            "flex_align_items": "center",
            "flex_justify_content": "space-between",
            "flex_wrap": "nowrap",
            "flex_gap": gap(16),
            "padding": pad(10, 20, 10, 20),
            "background_background": "classic",
            "background_color": WHITE,
            "border_border": "solid",
            "border_color": "rgba(28,22,18,0.10)",
            "border_width": pad(0, 0, 1, 0),
            "min_height": sz(72),
        },
        [logo, nav, cta],
        html_tag="header",
    )
    return template("SCZI — En-tête", "header", [bar], {"hide_title": "yes"})


def footer_tpl():
    brand = col(
        [
            image("logo/logo.png", "SCZI Toiture", extra={"width": sz(120), "image_border_radius": pad(8)}),
            text(
                "<p>Schubert Couverture Zinguerie Isolation — réfection de toiture, isolation et zinguerie à Brié-et-Angonnes (Isère).</p>"
                "<p>Gérant : SCHUBERT Eric</p>"
            ),
        ]
    )
    services = col(
        [
            heading("Services", "h3", size=18),
            icon_list(
                [
                    ("Toiture", "/toiture/", "fas fa-angle-right"),
                    ("Isolation sarking", "/isolation-sarking/", "fas fa-angle-right"),
                    ("Combles perdus", "/isolation-combles-perdus/", "fas fa-angle-right"),
                    ("Velux", "/installation-velux/", "fas fa-angle-right"),
                    ("Zinguerie", "/zinguerie/", "fas fa-angle-right"),
                ]
            ),
        ]
    )
    entreprise = col(
        [
            heading("Entreprise", "h3", size=18),
            icon_list(
                [
                    ("L’entreprise", "/entreprise/", "fas fa-angle-right"),
                    ("Réalisations", "/realisations/", "fas fa-angle-right"),
                    ("Zone d’intervention", "/zone-intervention/", "fas fa-angle-right"),
                    ("Contact / devis", "/contact/", "fas fa-angle-right"),
                    ("Mentions légales", "/mentions-legales/", "fas fa-angle-right"),
                ]
            ),
        ]
    )
    coords = col(
        [
            heading("Coordonnées", "h3", size=18),
            icon_list(
                [
                    (ADDRESS, MAPS, "fas fa-map-marker-alt"),
                    (PHONE, PHONE_TEL, "fas fa-phone"),
                    ("SIRET 75106621800023", "", "fas fa-id-card"),
                    ("RCS Grenoble B 751 066 218", "", "fas fa-building"),
                ]
            ),
        ]
    )
    legal = row(
        [
            text("<p>© SCZI — Schubert Couverture Zinguerie Isolation</p>", MUTED),
            widget(
                "button",
                {
                    "text": "Crédits & informations",
                    "link": link("/credits/"),
                    "size": "xs",
                    "align": "right",
                    "background_background": "classic",
                    "background_color": "rgba(0,0,0,0)",
                    "button_text_color": MUTED,
                },
            ),
        ],
        extra={"flex_justify_content": "space-between", "flex_align_items": "center"},
    )
    body = boxed(
        DARK,
        [row([brand, services, entreprise, coords]), legal],
        extra={"flex_gap": gap(28)},
        html_tag="footer",
    )
    # dark text on dark bg: override children text colors via heading/text already set
    # Recolor heading/text in footer: set on boxed overlay? Keep simple: light text
    for node in [brand, services, entreprise, coords]:
        pass
    # Patch text colors: recreate legal/text with white
    brand["elements"][1]["settings"]["text_color"] = "#EFE7DB"
    for c in (services, entreprise, coords):
        c["elements"][0]["settings"]["title_color"] = WHITE
    legal["elements"][0]["settings"]["text_color"] = "#C9C0B6"
    return template("SCZI — Pied de page", "footer", [body], {"hide_title": "yes"})


def qualibat_block():
    chip = heading(
        "Qualibat RGE depuis 2016",
        "p",
        RED,
        13,
        extra={"typography_text_transform": "uppercase", "typography_letter_spacing": sz(0.8)},
    )
    stats = row(
        [
            icon_box("2016 – 2026", "Dix ans de certification Qualibat", "fas fa-certificate"),
            icon_box("100 % RGE", "Toute l’activité est reconnue RGE", "fas fa-leaf"),
            icon_box("Contrôle", "Qualification suivie, travaux dans les règles de l’art", "fas fa-check"),
        ]
    )
    badges = row(
        [
            col(
                [
                    image("badges/rge-2016.jpg", "Macaron Qualibat RGE, année 2016", extra={"width": sz(180)}),
                    heading("2016", "h4", size=16),
                ],
                extra={"flex_align_items": "center", "width": sz(200, "px")},
            ),
            col(
                [
                    image("badges/rge.png", "Macaron Qualibat RGE, années 2016 et 2017", extra={"width": sz(180)}),
                    heading("2016–2017", "h4", size=16),
                ],
                extra={"flex_align_items": "center", "width": sz(200, "px")},
            ),
        ]
    )
    aids = row(
        [
            icon_box("MaPrimeRénov’", "Aide de l’État pour des travaux d’amélioration énergétique, sous conditions de ressources et de projet.", "fas fa-home"),
            icon_box("Primes CEE", "Certificats d’économies d’énergie : une prime versée par les fournisseurs d’énergie, selon les gestes réalisés.", "fas fa-bolt"),
            icon_box("Éco-prêt à taux zéro", "Emprunt sans intérêts pour financer des travaux de rénovation énergétique éligibles.", "fas fa-university"),
            icon_box("TVA 5,5 %", "Taux réduit sur les travaux de rénovation énergétique, lorsque les conditions fiscales sont réunies.", "fas fa-percent"),
            icon_box("Travail qualifié et contrôlé", "Le signe RGE atteste d’une entreprise formée, suivie, et d’un chantier déclaré selon le référentiel.", "fas fa-user-check"),
            icon_box("Conformité aux normes", "Les ouvrages restent réalisés dans le respect des DTU et des avis CSTB applicables au support.", "fas fa-ruler-combined"),
        ]
    )
    inner = [
        kicker("Qualibat · RGE"),
        chip,
        heading("10 ans de certification Qualibat, entreprise 100 % RGE."),
        text(
            "<p>SCZI est certifiée Qualibat depuis 2016, renouvelée jusqu’en 2026 : <strong>10 ans de performance et de qualité</strong> sur les chantiers. L’entreprise est <strong>100 % RGE</strong> (Reconnu Garant de l’Environnement).</p>"
        ),
        stats,
        heading("Macarons Qualibat RGE", "h3", size=20),
        badges,
        heading("Ce que le RGE change pour vous", "h3", size=20),
        text(
            "<p>Un artisan RGE, c’est la condition pour demander les aides publiques à la rénovation énergétique. Les montants, plafonds et pièces à fournir <strong>dépendent du foyer et des règles en vigueur</strong> au moment du chantier : nous n’affichons pas de chiffres qui pourraient dater.</p>"
        ),
        aids,
    ]
    return boxed("#F3EBE0", inner)


def cta_block():
    return boxed(
        DARK,
        [
            row(
                [
                    col(
                        [
                            kicker("Devis", "#FFB4BC"),
                            heading("Expliquez le toit, on revient vers vous.", "h2", WHITE),
                            text(
                                "<p>Décrivez le bâtiment, le lieu des travaux et vos besoins : nous revenons vers vous.</p>",
                                "#EFE7DB",
                            ),
                            btn("Ouvrir le formulaire", "/contact/"),
                        ]
                    ),
                    col(
                        [
                            heading(PHONE, "p", WHITE, 28),
                            text(f"<p>{ADDRESS}</p>", "#EFE7DB"),
                            widget("button", {"text": "Appeler", "link": link(PHONE_TEL), "size": "md", "background_background": "classic", "background_color": WHITE, "button_text_color": INK}),
                        ]
                    ),
                ]
            )
        ],
    )


def zone_block():
    return boxed(
        WHITE,
        [
            kicker("Territoire"),
            heading("De Noyarey à Crolles, en passant par Grenoble."),
            text(
                "<p>SCZI intervient de Noyarey à Crolles, en passant par Brié-et-Angonnes et Grenoble. Le siège est à Brié-et-Angonnes, en Isère.</p>"
            ),
            row(
                [
                    col(
                        [
                            heading("Le corridor d’intervention", "h2"),
                            icon_list(
                                [
                                    (f"Siège : {ADDRESS}", MAPS, "fas fa-map-marker-alt"),
                                    ("De Noyarey à Crolles", "", "fas fa-route"),
                                    ("En passant par Brié-et-Angonnes et Grenoble", "", "fas fa-city"),
                                    ("Département : Isère (38)", "", "fas fa-map"),
                                    ("Chantiers documentés : toiture à Eybens, isolation et toiture à Saint-Nazaire", "", "fas fa-hammer"),
                                ]
                            ),
                        ]
                    ),
                    col(
                        [
                            widget(
                                "google_maps",
                                {
                                    "address": ADDRESS,
                                    "zoom": sz(12),
                                    "height": sz(320),
                                },
                            ),
                            text(f'<p><a href="{MAPS}">Ouvrir dans Google Maps</a></p>'),
                        ]
                    ),
                ]
            ),
        ],
    )


def page_hero(kicker_t, h1, lede=""):
    kids = [kicker(kicker_t), heading(h1, "h1", size=36)]
    if lede:
        kids.append(text(f"<p>{lede}</p>"))
    return boxed(PAPER, kids, extra={"padding": pad(40, 20, 24, 20)})


GALLERY_NAMED = [
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
]
GALLERY_PLAIN = [
    "img-0091.jpg", "img-0427.jpg", "img-0422.jpg", "img-0153.jpg", "img-0135.jpg",
    "img-0110.jpg", "img-0108.jpg", "img-0064.jpg", "img-0058.jpg", "img-0054.jpg",
    "img-0042.jpg", "img-0039.jpg", "img-0032.jpg", "img-0651.jpg", "img-0638.jpg",
    "img-0593.jpg", "img-0590.jpg", "img-0561.jpg", "img-0530.jpg", "img-0515.jpg",
    "img-0284.jpg", "img-0246.jpg", "img-0241.jpg", "img-0086.jpg", "img-0059.jpg",
    "img-0056.jpg", "img-0052.jpg", "img-0050.jpg", "img-0021.jpg", "img-0009.jpg",
    "img-0003.jpg", "dsc-0037.jpg", "fullsizer.jpg", "sans-titre-5.jpg", "sans-titre-2.jpg",
]
ALL_GALLERY = GALLERY_NAMED + [(fn, "") for fn in GALLERY_PLAIN]


def page_accueil():
    hero = container(
        {
            "content_width": "boxed",
            "boxed_width": sz(1140),
            "flex_direction": "column",
            "flex_gap": gap(16),
            "flex_justify_content": "flex-end",
            "min_height": sz(560),
            "padding": pad(80, 20, 48, 20),
            "background_background": "classic",
            "background_image": media("chantiers/lucarne-pendant.jpg", "Pose de zinc et de tuiles écailles en toiture"),
            "background_size": "cover",
            "background_position": "center center",
            "background_overlay_background": "classic",
            "background_overlay_color": "#1C1612",
            "background_overlay_opacity": sz(0.55),
            "html_tag": "section",
        },
        [
            kicker("Schubert Couverture Zinguerie Isolation", "#FFB4BC"),
            heading("Qualibat RGE depuis 2016", "p", WHITE, 14, extra={"typography_text_transform": "uppercase"}),
            heading("La toiture, l’isolation et le zinc, travaillés pour le climat de l’Isère.", "h1", WHITE, 42),
            text(
                "<p>Notre entreprise spécialisée dans la réfection de toiture, l’isolation de toiture et de comble non aménageable est implantée à Brié-et-Angonnes, dans l’Isère.</p>",
                "#F1E8DE",
            ),
            row(
                [btn("Demander un devis", "/contact/"), btn("Voir les chantiers", "/realisations/", primary=False)],
                extra={"flex_align_items": "center"},
            ),
            row(
                [
                    icon_box("20 ans+", "d’expérience en zinguerie, charpente, sarking et Velux"),
                    icon_box("Brié-et-Angonnes", "siège en Isère (38), de Noyarey à Crolles"),
                    icon_box("DTU / CSTB", "réponses adaptées aux tuiles, ardoise, bac acier, joints debout"),
                    icon_box("Eric Schubert", "gérant, sur le chantier comme au devis"),
                ]
            ),
        ],
    )
    metiers = boxed(
        PAPER,
        [
            kicker("Métiers"),
            heading("Quatre savoir-faire de toiture, un seul interlocuteur."),
            text("<p>Couverture, isolation par l’extérieur, combles perdus, Velux et zinguerie : un seul interlocuteur pour le toit.</p>"),
            row(
                [
                    image_box("chantiers/lucarne-apres.jpg", "Lucarne en tuiles écailles et zinc", "Toiture neuve et réfection", "Tuiles, tuiles écailles, bac acier, ardoise ou joints debout. Habillage de lucarnes, charpente associée.", "/toiture/"),
                    image_box("chantiers/sarking-1054.jpg", "Isolation de toiture par l’extérieur", "Sarking et isolation par l’extérieur", "Isoler lors d’une réfection sans démonter les plafonds en rampant, ni perdre de hauteur sous toiture.", "/isolation-sarking/"),
                    image_box("stock/isolation-laine.jpg", "Isolant en laine", "Combles perdus soufflés", "Isolation par projection de laine de roche, pour les volumes trop bas pour être aménagés.", "/isolation-combles-perdus/"),
                    image_box("chantiers/velux-apres.jpg", "Fenêtre de toit Velux", "Pose et remplacement de Velux", "Du simple remplacement au jumelage, jusqu’à la transformation d’un débarras en chambre.", "/installation-velux/"),
                ]
            ),
            text('<p><a href="/zinguerie/">Zinguerie : chéneaux, abergements, rives et joints debout →</a></p>'),
        ],
    )
    pourquoi = boxed(
        WHITE,
        [
            row(
                [
                    col(
                        [
                            kicker("Pourquoi SCZI"),
                            heading("Un artisan local, des toitures pensées pour le massif."),
                            text(
                                "<p>Que votre toiture soit en tuiles, en tuiles écailles, en bac acier, en ardoise ou en joints debout, nous vous répondons de manière adaptée et personnalisée, en respectant les normes DTU et CSTB.</p>"
                                "<p>Nous effectuons des habillages et abergements de cheminée, la pose de chéneaux, des habillages de planches de rive et de bandeaux. Nous assurons également la pose et le remplacement de vos fenêtres de toit Velux.</p>"
                                "<p><strong>Faites des économies de chauffage</strong> en pensant à l’isolation des combles non aménageables par laine de roche soufflée, ou à l’isolation des combles aménagés par l’extérieur.</p>"
                            ),
                            icon_box("Un gérant identifiable", "SCHUBERT Eric, gérant. Le visage du chantier, pas un standard anonyme.", "fas fa-user"),
                            icon_box("Des toits en Isère", "Lucarnes, sarking, Velux : des chantiers à Eybens, Saint-Nazaire et dans l’agglomération grenobloise.", "fas fa-map-marker-alt"),
                        ]
                    ),
                    col([image("chantiers/lucarne-pendant.jpg", "Pose de zinc et de tuiles écailles sur une lucarne")]),
                ]
            )
        ],
    )
    chantiers = boxed(
        WHITE,
        [
            kicker("Chantiers"),
            heading("Quelques toits déjà documentés."),
            gallery(
                [
                    ("lucarne-avant.jpg", ""),
                    ("lucarne-apres.jpg", ""),
                    ("velux-avant.jpg", ""),
                    ("velux-apres.jpg", ""),
                    ("sarking-0685.jpg", ""),
                    ("eybens-avant.jpg", ""),
                ]
            ),
            btn("Galerie complète", "/realisations/", primary=False),
        ],
    )
    return template("SCZI — Accueil", "page", [hero, metiers, pourquoi, qualibat_block(), chantiers, cta_block()], PAGE_SETTINGS)


def page_entreprise():
    return template(
        "SCZI — L’entreprise",
        "page",
        [
            page_hero("L’entreprise", "Schubert Couverture Zinguerie Isolation.", "SCZI — aussi présentée comme SCZI Bâtiment et SCZI Toiture — est une entreprise de couverture basée à Brié-et-Angonnes, dans l’Isère."),
            boxed(
                WHITE,
                [
                    row(
                        [
                            col(
                                [
                                    heading("Un gérant, un métier de toiture."),
                                    text(
                                        "<p><strong>SCHUBERT Eric</strong> dirige l’entreprise, spécialisée dans la réfection de toiture, l’isolation de toiture et de comble non aménageable.</p>"
                                        "<p>Plus de 20 ans d’expérience en <strong>zinguerie, charpente, sarking et Velux</strong>. Les supports de couverture : tuiles, tuiles écailles, bac acier, ardoise et joints debout.</p>"
                                        "<p>Les travaux sont réalisés dans le respect des normes <strong>DTU</strong> et <strong>CSTB</strong>.</p>"
                                    ),
                                ]
                            ),
                            col([image("chantiers/lucarne-pendant.jpg", "Pose de zinc sur une lucarne")]),
                        ]
                    )
                ],
            ),
            boxed(
                PAPER,
                [
                    row(
                        [
                            col(
                                [
                                    heading("Identité légale"),
                                    icon_list(
                                        [
                                            ("Dénomination : SCHUBERT COUVERTURE ZINGUERIE", "", "fas fa-briefcase"),
                                            ("Enseigne : Schubert Couverture Zinguerie Isolation (SCZI)", "", "fas fa-signature"),
                                            (f"Siège : {ADDRESS}", MAPS, "fas fa-map-marker-alt"),
                                            ("SIRET : 75106621800023", "", "fas fa-id-card"),
                                            ("RCS : Grenoble B 751 066 218", "", "fas fa-building"),
                                            (f"Téléphone : {PHONE}", PHONE_TEL, "fas fa-phone"),
                                        ]
                                    ),
                                ]
                            ),
                            col(
                                [
                                    heading("Un métier, une enseigne"),
                                    text("<p>SCZI — aussi SCZI Bâtiment et SCZI Toiture — intervient de Noyarey à Crolles, en passant par Brié-et-Angonnes et Grenoble.</p>"),
                                    image("logo/logo-visuel.jpg", "Logo SCZI Toiture"),
                                ]
                            ),
                        ]
                    )
                ],
            ),
            cta_block(),
        ],
        PAGE_SETTINGS,
    )


def page_services():
    cards = [
        ("chantiers/lucarne-apres.jpg", "Réfection de lucarne", "Toiture", "Neuf, réfection, tuiles, écailles, ardoise, bac acier, joints debout.", "/toiture/"),
        ("chantiers/sarking-1054.jpg", "Isolation de toiture par l’extérieur", "Isolation sarking", "Isoler par l’extérieur lors d’une réfection, R = 6,30.", "/isolation-sarking/"),
        ("stock/isolation-laine.jpg", "Isolant en laine", "Combles perdus", "Laine de roche soufflée, résistances thermiques selon l’épaisseur.", "/isolation-combles-perdus/"),
        ("chantiers/velux-apres.jpg", "Velux", "Velux", "Pose, remplacement, jumelage, chevrette de panne.", "/installation-velux/"),
        ("chantiers/lucarne-pendant.jpg", "Zinguerie", "Zinguerie", "Cheminées, chéneaux, rives, bandeaux, joints debout.", "/zinguerie/"),
    ]
    return template(
        "SCZI — Services",
        "page",
        [
            page_hero("Services", "Le toit, l’isolant, le zinc, la lumière.", "Couverture, isolation, Velux et zinguerie : les métiers de SCZI à Brié-et-Angonnes, en Isère."),
            boxed(WHITE, [row([image_box(*c) for c in cards])]),
        ],
        PAGE_SETTINGS,
    )


def page_toiture():
    return template(
        "SCZI — Toiture",
        "page",
        [
            page_hero("Toiture", "Toits neufs, réfections, lucarnes : le travail se voit de la rue."),
            boxed(
                WHITE,
                [
                    row(
                        [
                            col(
                                [
                                    text("<p>Toiture neuve ou réfection : tuiles, tuiles écailles, bac acier, ardoise ou joints debout. Lucarne en joint debout cuivre, charpente associée.</p><p>La charpente fait partie de l’expérience de l’entreprise (plus de 20 ans).</p>"),
                                ]
                            ),
                            col([image("chantiers/lucarne-apres.jpg", "Lucarne en tuiles écailles")]),
                        ]
                    )
                ],
            ),
            boxed(
                PAPER,
                [
                    row(
                        [
                            col(
                                [
                                    heading("Toiture traditionnelle"),
                                    text(
                                        "<p>Une toiture traditionnelle en terre cuite a une durée de vie minimum de <strong>80 ans</strong>. D’autres matériaux allongent encore cette perspective :</p>"
                                        "<ul><li>tuile en terre cuite écaille plate : <strong>90 ans</strong> au minimum ;</li>"
                                        "<li>tuiles en ardoise : plus de <strong>120 ans</strong> de vie minimum.</li></ul>"
                                        "<p><strong>Indication pour un bâtiment neuf</strong> — Surface de 120 m², toit sans Velux, sans cheminée, tuiles en terre cuite : <strong>à partir de 65 €/m²</strong>.</p>"
                                    ),
                                ]
                            ),
                            col(
                                [
                                    heading("Toiture plate"),
                                    text(
                                        "<p>Une toiture plate ne contient pas de tuiles : on parle d’étanchéité bitume ou végétalisée.</p>"
                                        "<h3>Étanchéité bitume</h3>"
                                        "<p>Primaire d’accroche, puis déroulage et chauffage des rouleaux au chalumeau pour superposer les lés.</p>"
                                        "<ul><li>dalle béton : maximum 40 ans avec un entretien très régulier ;</li>"
                                        "<li>ossature bois : maximum 20 ans, avec possible reprise d’étanchéité.</li></ul>"
                                        "<h3>Étanchéité végétalisée</h3>"
                                        "<p>Surface végétale au-dessus du toit plat, membrane contre la corrosion liée aux racines. Entretien au minimum tous les 6 mois. Durée de vie : <strong>15 ans en moyenne</strong>.</p>"
                                    ),
                                ]
                            ),
                        ]
                    )
                ],
            ),
            boxed(
                WHITE,
                [
                    heading("Réfection de lucarne — avant / après"),
                    text("<p>Réfection de toiture tuile écaille et lucarne en joint debout cuivre.</p>"),
                    gallery([("lucarne-avant.jpg", "Avant"), ("lucarne-pendant.jpg", "Pendant"), ("lucarne-apres.jpg", "Après")]),
                ],
            ),
            boxed(
                PAPER,
                [
                    heading("Comment se déroule une réfection"),
                    row(
                        [
                            icon_box("Échange et visite", "Vous décrivez le bâtiment, les désordres (fuites, tuiles, zinc) et le lieu des travaux. Une visite permet d’adapter la réponse au support réel."),
                            icon_box("Choix du matériau", "Tuile, écaille, ardoise, bac acier ou joint debout : le choix suit le bâti, le budget et les règles de l’art DTU / CSTB."),
                            icon_box("Chantier", "Protection, dépose, reprise éventuelle de charpente, couverture, zinguerie de rive et d’ouvrage, contrôles d’étanchéité."),
                            icon_box("Remise", "Relecture du chantier avec vous. La lucarne en tuile écaille et zinc montre le niveau de finition visé."),
                        ]
                    ),
                    heading("Questions fréquentes"),
                    accordion(
                        [
                            ("Intervenez-vous seulement en neuf ?", "Non. Nous réalisons aussi des réfections, comme la lucarne en tuile écaille ou la toiture à Eybens. Le neuf permet surtout de comparer durées de vie et un prix d’ordre de grandeur."),
                            ("Travaillez-vous l’ardoise et le zinc ?", "Oui : ardoise et joints debout sont listés parmi les réponses possibles, au même titre que tuiles et bac acier."),
                            ("Peut-on isoler en même temps ?", "C’est même le moment le plus logique : voir la page sarking. Isoler par l’extérieur évite de démonter les plafonds en rampant."),
                        ]
                    ),
                    btn("Demander un devis toiture", "/contact/"),
                ],
            ),
        ],
        PAGE_SETTINGS,
    )


def page_sarking():
    return template(
        "SCZI — Isolation sarking",
        "page",
        [
            page_hero("Isolation", "Isoler par-dessus la charpente, sans sacrifier la hauteur sous plafond."),
            boxed(
                WHITE,
                [
                    row(
                        [
                            col(
                                [
                                    text(
                                        "<p>Le procédé permet, en cas de réfection de toiture, d’isoler dans les normes sans avoir à démonter les plafonds en rampant et/ou perdre de la hauteur due à l’épaisseur d’isolant.</p>"
                                        "<p>Il vise une baisse de consommation d’énergie, en isolant au moment où la couverture est ouverte.</p>"
                                    )
                                ]
                            ),
                            col([image("chantiers/sarking-1054.jpg", "Chantier d’isolation de toiture par l’extérieur")]),
                        ]
                    )
                ],
            ),
            boxed(
                PAPER,
                [
                    heading("Trois montages"),
                    text("<p>Différentes solutions existent suivant la configuration de la charpente et le budget. Les exemples visent une résistance thermique <strong>R = 6,30</strong>.</p>"),
                    row(
                        [
                            image_box("chantiers/sarking-1014.jpg", "Laine de bois et panneau sarking", "Laine de bois + sarking", "Laine de bois semi-rigide de 200 mm entre chevrons, panneau sarking de 60 mm. Objectif : supprimer les ponts thermiques des chevrons et les entrées d’air. R = 6,30."),
                            image_box("chantiers/sarking-0685.jpg", "Double couche de laine de bois 120 mm", "Deux fois 120 mm", "Laine de bois semi-rigide en deux épaisseurs de 120 mm entre chevrons, couches croisées. R = 6,30. Isolation et toiture à Saint-Nazaire."),
                            image_box("chantiers/sarking-double-chevron.jpg", "Double chevronnage et laine de verre", "Double chevronnage", "Isolation par l’extérieur avec double chevronnage, laine de verre 2 × 100 mm en GR32. R = 6,30. Isolation toiture à Eybens."),
                        ]
                    ),
                ],
            ),
            boxed(
                WHITE,
                [
                    heading("Déroulement type"),
                    row(
                        [
                            icon_box("Réfection programmée", "Le sarking a surtout du sens quand la couverture est ouverte. On isole alors « dans la foulée » du toit."),
                            icon_box("Lecture de la charpente", "Entre chevrons, hors chevrons, double chevronnage : le choix suit la structure et le budget."),
                            icon_box("Continuité de l’enveloppe", "Les panneaux hors chevrons visent à casser le pont thermique du bois et les fuites d’air."),
                            icon_box("Couverture et zinc", "La toiture se referme : tuiles, écailles, zinguerie. L’isolant n’est plus exposé."),
                        ]
                    ),
                    heading("FAQ"),
                    accordion(
                        [
                            ("Faut-il vider les combles ?", "Le sarking vise justement à éviter de démonter les plafonds en rampant."),
                            ("Pourquoi R = 6,30 ?", "C’est la résistance thermique visée sur les trois montages présentés."),
                        ]
                    ),
                    btn("Demander un devis isolation", "/contact/"),
                ],
            ),
        ],
        PAGE_SETTINGS,
    )


COMBLES_TABLE = """
<table>
<thead><tr><th>Ép. (mm)</th><th>Ép. après tassement (mm)</th><th>R (m².K/W)</th><th>Pouvoir couvrant (kg/m²)</th><th>Sacs / 100 m²</th><th>Up (W/m².K)</th></tr></thead>
<tbody>
<tr><td>95</td><td>90</td><td>2</td><td>2</td><td>9,6</td><td></td></tr>
<tr><td>230</td><td>225</td><td>5</td><td>4,9</td><td>24,1</td><td>0,2</td></tr>
<tr><td>275</td><td>270</td><td>6</td><td>5,8</td><td>28,9</td><td>0,16</td></tr>
<tr><td>320</td><td>315</td><td>7</td><td>6,8</td><td>33,2</td><td>0,14</td></tr>
<tr><td>365</td><td>360</td><td>8</td><td>7,8</td><td>38,5</td><td>0,12</td></tr>
<tr><td>410</td><td>405</td><td>9</td><td>8,7</td><td>43,4</td><td></td></tr>
<tr><td>455</td><td>450</td><td>10</td><td>9,7</td><td>48,2</td><td></td></tr>
<tr><td>500</td><td>495</td><td>11</td><td>10,6</td><td>53</td><td></td></tr>
<tr><td>545</td><td>540</td><td>12</td><td>11,6</td><td>57,8</td><td></td></tr>
<tr><td>595</td><td>585</td><td>13</td><td>12,6</td><td>62,6</td><td></td></tr>
<tr><td>640</td><td>630</td><td>14</td><td>13,5</td><td>67,5</td><td></td></tr>
<tr><td>685</td><td>675</td><td>15</td><td>14,5</td><td>72,3</td><td></td></tr>
</tbody>
</table>
"""


def page_combles():
    return template(
        "SCZI — Combles perdus",
        "page",
        [
            page_hero("Combles perdus", "Quand le comble est trop bas pour vivre, on l’isole par le sol."),
            boxed(
                WHITE,
                [
                    row(
                        [
                            col(
                                [
                                    text(
                                        "<p>Le terme comble perdu désigne un espace insuffisant entre la dernière hauteur de plafond horizontale et la toiture du bâtiment.</p>"
                                        "<p>Dans ce cas, l’isolation par projection reste la plus performante pour la rupture de pont thermique (pénétration dans les recoins, lame d’air entre couches) et d’un point de vue financier (gain de temps face aux rouleaux ou panneaux).</p>"
                                        "<p>Isolation des combles non aménageables <strong>par laine de roche soufflée</strong>.</p>"
                                    )
                                ]
                            ),
                            col([image("stock/isolation-laine.jpg", "Isolant en laine")]),
                        ]
                    )
                ],
            ),
            boxed(
                PAPER,
                [
                    heading("Fiche technique — laine de roche soufflée"),
                    text("<p>À partir d’une résistance thermique de <strong>7</strong> (ligne mise en avant), l’épaisseur après tassement est de 315 mm.</p>"),
                    widget("html", {"html": COMBLES_TABLE}),
                ],
            ),
            boxed(
                WHITE,
                [
                    heading("Processus"),
                    row(
                        [
                            icon_box("Accès au comble", "Trappe, passage, état du plancher : on vérifie que le soufflage peut se faire sans tasser un plafond fragile."),
                            icon_box("Épaisseur cible", "Le tableau relie millimètres, tassement, résistance thermique R et nombre de sacs. La ligne R = 7 est mise en avant."),
                            icon_box("Projection", "La laine de roche est soufflée pour garnir recoins et lames d’air, plus rapidement que des panneaux."),
                        ]
                    ),
                    heading("FAQ"),
                    accordion(
                        [
                            ("Différence avec le sarking ?", "Combles perdus = volume non habitable, isolation au sol du comble. Sarking = isolation par l’extérieur, souvent pour combles aménagés ou à préserver en hauteur."),
                            ("Puis-je aménager plus tard ?", "Si l’espace redevient habitable, la logique change : isolation des combles aménagés par l’extérieur (sarking)."),
                        ]
                    ),
                    btn("Demander un devis combles", "/contact/"),
                ],
            ),
        ],
        PAGE_SETTINGS,
    )


def page_velux():
    return template(
        "SCZI — Velux",
        "page",
        [
            page_hero("Velux", "Plus de lumière sous les combles, sans construire un chien assis."),
            boxed(
                WHITE,
                [
                    row(
                        [
                            col(
                                [
                                    text(
                                        "<p>Les châssis de toit Velux apportent de la lumière et permettent d’aménager un comble, pour un coût moindre qu’un chien assis.</p>"
                                        "<p>Un Velux vise un coefficient Uw de 1,1 (plus le Uw se rapproche de 1, meilleure est l’isolation thermique).</p>"
                                    )
                                ]
                            ),
                            col([image("chantiers/velux-apres.jpg", "Fenêtre de toit Velux")]),
                        ]
                    )
                ],
            ),
            boxed(
                PAPER,
                [
                    row(
                        [
                            col(
                                [
                                    heading("Integra Solar"),
                                    text(
                                        "<p>Le modèle Integra Solar dispose de capteurs qui actionnent la ventilation en cas de trop forte humidité ou de fort taux de CO₂, et se referment à la détection de pluie. Une tablette Velux permet de programmer ouvertures, fermetures, volet extérieur, et d’autres appareils télécommandés Somfy, dans une limite de 60 appareils.</p>"
                                        "<p>Un ancien châssis qui laisse passer trop de chaleur se remplace pour se rapprocher de ces performances.</p>"
                                    ),
                                ]
                            ),
                            col(
                                [
                                    heading("Exemples de chantiers"),
                                    text(
                                        "<ul><li>Transformation d’un débarras en chambre et réalisation de chevrette de panne pour pose d’un Velux.</li>"
                                        "<li>Aile droite : agrandissement d’un Velux 114 × 118 cm en jumelage après réfection totale de toiture ; aile gauche : changement de Velux. Isolation par l’extérieur en laine de bois 2 × 120 mm croisées, R = 6,30.</li>"
                                        "<li>Création de Velux en duo 134 × 140 cm ainsi que 134 × 98 cm.</li></ul>"
                                    ),
                                ]
                            ),
                        ]
                    )
                ],
            ),
            boxed(
                WHITE,
                [
                    gallery(
                        [
                            ("velux-avant.jpg", "Avant"),
                            ("velux-apres.jpg", "Après"),
                            ("velux-transformation.jpg", "Chevrette"),
                            ("velux-pose.jpg", "Pose"),
                            ("velux-aile-droite.jpg", "Aile droite"),
                            ("velux-aile-gauche.jpg", "Aile gauche"),
                            ("velux-duo.jpg", "Duo"),
                        ]
                    )
                ],
            ),
            boxed(
                PAPER,
                [
                    heading("Étapes"),
                    row(
                        [
                            icon_box("Cote et usage", "Chambre, bureau, simple éclairement : la cote (ex. 114/118) et le jumelage se décident avec la charpente."),
                            icon_box("Chevrette si besoin", "Une chevrette de panne se pose lorsque la structure ne permet pas une pose directe."),
                            icon_box("Étanchéité", "Raccord de toiture, abergement, isolation périphérique : le châssis n’est pas une simple menuiserie posée dans un trou."),
                        ]
                    ),
                    heading("FAQ"),
                    accordion(
                        [
                            ("Peut-on poser un Velux sans refaire tout le toit ?", "Oui : des remplacements isolés sont possibles. Un jumelage peut aussi accompagner une réfection totale."),
                            ("Pourquoi pas un chien assis ?", "Le Velux est moins onéreux, tout en apportant lumière et confort d’aménagement."),
                        ]
                    ),
                    btn("Demander un devis Velux", "/contact/"),
                ],
            ),
        ],
        PAGE_SETTINGS,
    )


def page_zinguerie():
    return template(
        "SCZI — Zinguerie",
        "page",
        [
            page_hero("Zinguerie", "Le zinc tient l’eau là où les tuiles s’arrêtent."),
            boxed(
                WHITE,
                [
                    row(
                        [
                            col(
                                [
                                    text(
                                        "<p>Habillages et abergements de cheminée, pose de chéneaux, habillages de planches de rive et de bandeaux, toitures en joints debout : plus de 20 ans en zinguerie.</p>"
                                        "<p>La réfection de lucarne en joint debout cuivre montre le niveau d’ouvrage : le métal n’est pas un accessoire, c’est la ligne d’eau du toit.</p>"
                                    )
                                ]
                            ),
                            col([image("chantiers/lucarne-pendant.jpg", "Pose de zinc sur une lucarne")]),
                        ]
                    )
                ],
            ),
            boxed(
                PAPER,
                [
                    row(
                        [
                            icon_box("Cheminées", "Habillages et abergements : le point singulier le plus fréquent des infiltrations, traité dans le respect des DTU."),
                            icon_box("Chéneaux", "Pose de chéneaux pour collecter et évacuer les eaux pluviales, en cohérence avec la couverture."),
                            icon_box("Rives et bandeaux", "Habillages de planches de rive et de bandeaux : la finition du rampant, au vent et à la pluie de l’Isère."),
                            icon_box("Joints debout", "Couverture métallique (cuivre documenté sur une lucarne) lorsque le projet sort de la tuile classique."),
                        ]
                    )
                ],
            ),
            boxed(
                WHITE,
                [
                    heading("Pourquoi le zinc compte en montagne grenobloise"),
                    text("<p>Neige, gel, fortes pluies : les points singuliers (lucarne, cheminée, rive) fatiguent avant le plein rampant. Un abergement juste, un chéneau dimensionné, une rive bien habillée prolongent la couverture — tuile ou ardoise.</p>"),
                    row(
                        [
                            icon_box("Relevé des ouvrages", "Cheminées, noues, rives, lucarnes : on liste les points d’eau avant de parler couleur de tuile."),
                            icon_box("Façonnage", "Le zinc et le cuivre se façonnent sur le chantier, pas seulement comme accessoires du commerce."),
                            icon_box("Raccord couverture", "Le métal se coud avec la tuile ou l’ardoise pour que l’eau n’ait qu’un chemin."),
                        ]
                    ),
                    btn("Demander un devis zinguerie", "/contact/"),
                ],
            ),
        ],
        PAGE_SETTINGS,
    )


def page_realisations():
    return template(
        "SCZI — Réalisations",
        "page",
        [
            page_hero("Réalisations", "Les toits déjà photographiés.", "Lucarnes, Velux, sarking, toitures à Eybens et Saint-Nazaire : une sélection de chantiers."),
            boxed(WHITE, [gallery(ALL_GALLERY)]),
        ],
        PAGE_SETTINGS,
    )


def page_zone():
    return template(
        "SCZI — Zone d’intervention",
        "page",
        [
            page_hero("Territoire", "De Noyarey à Crolles, en passant par Grenoble.", "SCZI intervient de Noyarey à Crolles, en passant par Brié-et-Angonnes et Grenoble. Le siège est à Brié-et-Angonnes, en Isère."),
            zone_block(),
            boxed(
                PAPER,
                [
                    heading("Pourquoi le climat local compte"),
                    text("<p>Tuiles écailles, zinc, sarking et laine soufflée répondent à des toits exposés au froid, à la neige et aux écarts thermiques de l’agglomération grenobloise. L’isolation par l’extérieur et les combles perdus y sont des leviers d’économie de chauffage.</p>"),
                    image("stock/paysage-alpes.jpg", "Paysage de montagne en Isère"),
                    btn("Indiquer le lieu des travaux", "/contact/"),
                ],
            ),
        ],
        PAGE_SETTINGS,
    )


def form_field(fid, ftype, label, width="100", required=False, placeholder=""):
    return {
        "_id": nid(),
        "custom_id": fid,
        "field_type": ftype,
        "field_label": label,
        "placeholder": placeholder,
        "required": "true" if required else "",
        "width": width,
        "allow_multiple_upload": "false",
        "field_options": "",
    }


def page_contact():
    form = widget(
        "form",
        {
            "form_name": "Devis SCZI",
            "form_fields": [
                form_field("nom", "text", "Nom", "50", True),
                form_field("telephone", "tel", "Téléphone", "50"),
                form_field("email", "email", "E-mail", "100", True),
                form_field("lieu", "text", "Lieu des futurs travaux", "50"),
                form_field("budget", "text", "Budget estimé", "50"),
                form_field("besoin", "textarea", "Vos besoins", "100", True),
                form_field("mentions", "acceptance", "En envoyant ce formulaire, vous acceptez d’être recontacté au sujet de votre projet.", "100", True),
            ],
            "button_text": "Envoyer",
            "button_size": "md",
            "button_align": "start",
            "submit_actions": ["email"],
            "email_to": "admin@example.com",
            "email_subject": "Demande de devis SCZI",
            "success_message": "Merci. Pour confirmer votre demande, appelez-nous au 04 38 70 03 94.",
            "button_background_color": RED,
            "button_text_color": WHITE,
            "mark_required": "yes",
            "show_labels": "true",
            "input_size": "md",
        },
    )
    aside = col(
        [
            heading("Coordonnées"),
            icon_list(
                [
                    (PHONE, PHONE_TEL, "fas fa-phone"),
                    (ADDRESS, MAPS, "fas fa-map-marker-alt"),
                    ("Gérant : SCHUBERT Eric", "", "fas fa-user"),
                ]
            ),
            text('<p>Voir les <a href="/mentions-legales/">mentions légales</a>.</p>'),
        ]
    )
    return template(
        "SCZI — Devis / contact",
        "page",
        [
            page_hero("Contact", "Un devis, à partir du toit que vous décrivez.", "Nom, téléphone, e-mail, lieu des travaux, budget estimé et besoins : nous revenons vers vous."),
            boxed(WHITE, [row([col([form]), aside])]),
        ],
        PAGE_SETTINGS,
    )


def page_mentions():
    html = f"""
<p>La société SCHUBERT COUVERTURE ZINGUERIE<br>
SIRET 75106621800023<br>
RCS Ville tribunal : Grenoble B 751 066 218<br>
Siège social : 4290 route Napoléon — 38320 Brié-et-Angonnes<br>
Téléphone : {PHONE}<br>
Directeur de la publication : la société SCHUBERT COUVERTURE ZINGUERIE</p>
"""
    return template(
        "SCZI — Mentions légales",
        "page",
        [
            page_hero("Informations légales", "Mentions légales", "Éditeur, hébergement et protection des données personnelles."),
            boxed(
                WHITE,
                [
                    heading("Éditeur"),
                    text(html),
                    heading("Hébergement"),
                    text("<p>Ce site est hébergé par GitHub Pages — GitHub, Inc., 88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, États-Unis.</p>"),
                    heading("Données personnelles"),
                    text(
                        "<p>La société SCHUBERT COUVERTURE ZINGUERIE n’enregistre pas d’informations personnelles permettant l’identification, à l’exception des formulaires que l’utilisateur est libre de remplir. Ces informations ne seront pas utilisées sans votre accord ; elles servent à vous adresser des courriers, des brochures, des devis ou à vous contacter.</p>"
                        "<p>Les informations recueillies bénéficient de la protection de la loi « Informatique et Libertés » n° 78-17 du 6 janvier 1978. Droit d’accès, de rectification, d’opposition et de suppression sur simple demande à SCHUBERT COUVERTURE ZINGUERIE, 4290 route Napoléon — 38320 Brié-et-Angonnes.</p>"
                        "<p>La société peut procéder à des analyses statistiques non nominatives et en informer des tiers (organismes d’évaluation de fréquentation) sous forme résumée et non nominative.</p>"
                        "<p>Ce site n’installe pas de cookies de mesure d’audience.</p>"
                    ),
                    heading("Création graphique"),
                    text("<p>Création graphique : Thomas BONSIRVEN.</p>"),
                    heading("Liens hypertexte"),
                    text("<p>La société SCHUBERT COUVERTURE ZINGUERIE ne contrôle pas les sites en connexion avec le sien, et ne saurait donc être responsable de leur contenu.</p>"),
                    heading("Photographies"),
                    text('<p>Les crédits photographiques et les mentions d’origine sont regroupés sur la page <a href="/credits/">Crédits & informations</a>.</p>'),
                ],
            ),
        ],
        PAGE_SETTINGS,
    )


def page_credits():
    return template(
        "SCZI — Crédits & informations",
        "page",
        [
            page_hero("Documentation interne", "Crédits & informations", "Page hors parcours client : crédits des photos de stock (obligation légale) et liste de ce qui reste à fournir. Les pages publiques n’affichent que le texte destiné aux visiteurs."),
            boxed(
                WHITE,
                [
                    heading("Crédits photographiques, par page"),
                    text(
                        "<p>Les photos de chantiers (lucarnes, Velux, sarking, Eybens, Saint-Nazaire, etc.) proviennent des archives SCZI. Les visuels de stock ci-dessous sont des copies locales, licences Unsplash / Pexels.</p>"
                    ),
                    heading("Accueil, hub Services, Isolation combles", "h3"),
                    text('<p><code>isolation-laine.jpg</code> — Pexels, Karolina Grabowska — <a href="https://images.pexels.com/photos/5691622/pexels-photo-5691622.jpeg">source</a></p>'),
                    heading("Zone d’intervention", "h3"),
                    text('<p><code>paysage-alpes.jpg</code> — Pexels, James Wheeler — <a href="https://images.pexels.com/photos/417074/pexels-photo-417074.jpeg">source</a> (photo et fond de la carte)</p>'),
                    heading("Autres photos de stock du dépôt (non affichées sur les pages publiques)", "h3"),
                    text(
                        "<ul><li>Unsplash : Quin Stevenson, Annika Gordon, Daniel McCullough, Dan Gold, R ARCHITECTURE, Daniel Hjalmarsson</li>"
                        "<li>Pexels : Pixabay, Bin Zhang, Kiwihug, Vecislavas Popa, Blue Bird, Binyamin Mellish</li></ul>"
                    ),
                ],
            ),
            boxed(
                PAPER,
                [
                    heading("Informations encore à fournir"),
                    text(
                        "<ol>"
                        "<li>E-mail professionnel</li>"
                        "<li>Identifiant Formspree (remplacer xxxxxxxx dans contact.html) ou adresse mailto définitive — sur WordPress : destinataire du widget Formulaire Elementor Pro</li>"
                        "<li>Horaires d’accueil / d’appel</li>"
                        "<li>Numéros de certificat Qualibat et RGE</li>"
                        "<li>Macarons / certificats Qualibat RGE des années <strong>2018 à 2026</strong> (inventaire : seuls <strong>2016</strong> et <strong>2016–2017</strong> existent). Ne pas inventer d’images.</li>"
                        "<li>Barèmes chiffrés des aides (MaPrimeRénov’, CEE, éco-PTZ, TVA 5,5 % sont cités sur l’accueil, sans montants)</li>"
                        "<li>Tarifs actualisés (le 65 €/m² date d’environ 2018)</li>"
                        "<li>Légendes des photos de chantier encore sans commune ni date</li>"
                        "<li>Réseaux sociaux (les anciens liens du thème étaient factices)</li>"
                        "<li>Forme juridique, capital, TVA intra, assurance décennale</li>"
                        "<li>Avis clients (aucun n’est inventé ici)</li>"
                        "<li>Hébergeur à confirmer si le domaine sczi-renov38.fr est recollé</li>"
                        "<li>Métaux de zinguerie au catalogue, garanties de patine</li>"
                        "<li>Marque d’isolant et avis technique pour le soufflage</li>"
                        "</ol>"
                    ),
                ],
            ),
        ],
        PAGE_SETTINGS,
    )


def collect_images():
    used = {
        "logo/logo.png",
        "logo/logo-visuel.jpg",
        "badges/rge-2016.jpg",
        "badges/rge.png",
        "stock/isolation-laine.jpg",
        "stock/paysage-alpes.jpg",
        "chantiers/lucarne-avant.jpg",
        "chantiers/lucarne-pendant.jpg",
        "chantiers/lucarne-apres.jpg",
        "chantiers/velux-avant.jpg",
        "chantiers/velux-apres.jpg",
        "chantiers/velux-installation.jpg",
        "chantiers/velux-transformation.jpg",
        "chantiers/velux-pose.jpg",
        "chantiers/velux-aile-droite.jpg",
        "chantiers/velux-aile-gauche.jpg",
        "chantiers/velux-duo.jpg",
        "chantiers/sarking-1054.jpg",
        "chantiers/sarking-1016.jpg",
        "chantiers/sarking-1014.jpg",
        "chantiers/sarking-0685.jpg",
        "chantiers/sarking-0684.jpg",
        "chantiers/sarking-double-chevron.jpg",
        "chantiers/sarking-0083.jpg",
        "chantiers/sarking-0109.jpg",
        "chantiers/toiture-0664.jpg",
        "chantiers/toiture-0662.jpg",
        "chantiers/eybens-avant.jpg",
        "chantiers/mur-pignon-1.jpg",
        "chantiers/mur-pignon-2.jpg",
    }
    for fn, _ in ALL_GALLERY:
        used.add(f"chantiers/{fn}")
    return sorted(used)


def copy_images():
    if IMG_DIR.exists():
        shutil.rmtree(IMG_DIR)
    copied = []
    for rel in collect_images():
        src = ROOT / "assets" / "img" / rel
        dst = IMG_DIR / rel
        if not src.exists():
            print("MISSING IMAGE", src)
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        copied.append(rel)
    return copied


def walk_ids(node, bag):
    if isinstance(node, dict):
        if "id" in node and "elType" in node:
            bag.append(node["id"])
        if "_id" in node:
            bag.append(node["_id"])
        for v in node.values():
            walk_ids(v, bag)
    elif isinstance(node, list):
        for v in node:
            walk_ids(v, bag)


def validate(files):
    errors = []
    all_ids = []
    for path in files:
        raw = path.read_text(encoding="utf-8")
        try:
            data = json.loads(raw)
        except json.JSONDecodeError as e:
            errors.append(f"{path.name}: JSON invalide ({e})")
            continue
        for key in ("version", "title", "type", "content", "page_settings"):
            if key not in data:
                errors.append(f"{path.name}: clé manquante {key}")
        if data.get("version") != "0.4":
            errors.append(f"{path.name}: version {data.get('version')}")
        if data.get("type") not in ("header", "footer", "section", "page", "container"):
            errors.append(f"{path.name}: type {data.get('type')}")
        if not isinstance(data.get("content"), list):
            errors.append(f"{path.name}: content n'est pas une liste")
        ids = []
        walk_ids(data, ids)
        for i in ids:
            if not isinstance(i, str) or len(i) != 8 or any(c not in "0123456789abcdef" for c in i):
                errors.append(f"{path.name}: id non hex8 {i!r}")
        dups = [i for i in ids if ids.count(i) > 1]
        if dups:
            errors.append(f"{path.name}: ids dupliqués {sorted(set(dups))[:5]}")
        all_ids.extend(ids)

        def check_el(el, loc):
            if not isinstance(el, dict):
                errors.append(f"{path.name}: {loc} n'est pas un objet")
                return
            if el.get("elType") not in ("container", "widget"):
                errors.append(f"{path.name}: {loc} elType {el.get('elType')}")
            if "settings" not in el or "elements" not in el:
                errors.append(f"{path.name}: {loc} settings/elements manquants")
            if el.get("elType") == "widget" and not el.get("widgetType"):
                errors.append(f"{path.name}: {loc} widget sans widgetType")
            for i, child in enumerate(el.get("elements") or []):
                check_el(child, f"{loc}/{el.get('elType')}-{i}")

        for i, el in enumerate(data.get("content") or []):
            check_el(el, f"content[{i}]")
    return errors, len(all_ids)


def make_zips(copied):
    media_zip = OUT / "images-media.zip"
    with zipfile.ZipFile(media_zip, "w", zipfile.ZIP_DEFLATED) as zf:
        for rel in copied:
            zf.write(IMG_DIR / rel, f"images/{rel}")
    full = OUT / "sczi-elementor-import.zip"
    with zipfile.ZipFile(full, "w", zipfile.ZIP_DEFLATED) as zf:
        for p in OUT.rglob("*"):
            if p.is_file() and p.name not in ("sczi-elementor-import.zip", "images-media.zip") and p.suffix != ".pyc":
                if p.name == "build.py":
                    zf.write(p, "elementor/build.py")
                    continue
                zf.write(p, f"elementor/{p.relative_to(OUT)}")
        zf.write(media_zip, "elementor/images-media.zip")
    return media_zip, full


def main():
    if JSON_DIR.exists():
        shutil.rmtree(JSON_DIR)
    JSON_DIR.mkdir(parents=True)

    save("header.json", header_tpl())
    save("footer.json", footer_tpl())
    save("section-qualibat-rge.json", template("SCZI — Bloc Qualibat RGE", "container", [qualibat_block()]))
    save("section-cta-devis.json", template("SCZI — Bandeau devis", "container", [cta_block()]))
    save("section-zone.json", template("SCZI — Bloc zone d’intervention", "container", [zone_block()]))
    save("page-accueil.json", page_accueil())
    save("page-entreprise.json", page_entreprise())
    save("page-services.json", page_services())
    save("page-toiture.json", page_toiture())
    save("page-sarking.json", page_sarking())
    save("page-combles.json", page_combles())
    save("page-velux.json", page_velux())
    save("page-zinguerie.json", page_zinguerie())
    save("page-realisations.json", page_realisations())
    save("page-zone.json", page_zone())
    save("page-contact.json", page_contact())
    save("page-mentions-legales.json", page_mentions())
    save("page-credits.json", page_credits())

    files = sorted(JSON_DIR.glob("*.json"))
    errors, nids = validate(files)
    copied = copy_images()
    media_zip, full = make_zips(copied)
    print("json_files", len(files), "unique_ids", nids, "images", len(copied))
    print("zips", media_zip.name, full.name, full.stat().st_size)
    if errors:
        print("VALIDATION ERRORS")
        for e in errors:
            print(" -", e)
        raise SystemExit(1)
    print("validation OK")


if __name__ == "__main__":
    main()
