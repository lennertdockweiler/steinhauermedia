#!/usr/bin/env python3
"""
Static site generator for Steinhauer Media.

Reads site.config.json (single source of truth for domain, company info,
contact data, social links and the OG placeholder image) and writes out
every page of the site as plain, framework-free static HTML.

Run after editing site.config.json to propagate the change into every
canonical tag, Open Graph tag, JSON-LD block, sitemap.xml and robots.txt:

    python3 scripts/generate_site.py

The generated files are plain HTML/CSS/JS with no runtime dependency on
this script or on Python -- it only has to be re-run when content or the
central config changes.
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG = json.load(open(os.path.join(ROOT, "site.config.json"), encoding="utf-8"))

CO = CONFIG["company"]
ADDR = CO["address"]
ADDRESS_LINE = f'{ADDR["street"]}, {ADDR["postalCode"]} {ADDR["city"]}'
EMAIL = CO["email"]
PHONES = CO["phones"]
INSTAGRAM = CO["social"].get("instagram")


def site_url(slug=""):
    base = CONFIG["siteUrl"].rstrip("/")
    if not slug:
        return base + "/"
    return base + "/" + slug.strip("/") + "/"


def asset_url(path):
    base = CONFIG["siteUrl"].rstrip("/")
    return base + "/" + path.lstrip("/")


# ---------------------------------------------------------------------------
# Route table
# ---------------------------------------------------------------------------
# depth 0 = root (index.html), depth 1 = /<slug>/index.html
ROUTES = [
    {"slug": "", "depth": 0, "nav": "home",
     "title": "Steinhauer Media | Social Media & Performance Marketing Konstanz",
     "description": "Steinhauer Media aus Konstanz: Social-Media-Content, SEO/GEO und Google & Meta Ads aus einer Hand. Kostenlose Potenzialanalyse für planbar mehr Kunden am Bodensee.",
     "crumbs": []},
    {"slug": "leistungen", "depth": 1, "nav": "leistungen",
     "title": "Online Marketing Leistungen | Steinhauer Media Konstanz",
     "description": "Social Media, SEO & GEO, Google & Meta Ads, Social Recruiting und Webdesign: Steinhauer Media aus Konstanz bündelt Ihr Online-Marketing in einem System.",
     "crumbs": [("Leistungen", None)]},
    {"slug": "social-media-agentur-konstanz", "depth": 1, "nav": "leistungen",
     "title": "Social Media Agentur Konstanz | Steinhauer Media",
     "description": "Steinhauer Media produziert organische Short-Form-Videos und Social-Media-Content für Unternehmen in Konstanz und am Bodensee – von Skript bis Schnitt.",
     "crumbs": [("Leistungen", "leistungen"), ("Social Media", None)]},
    {"slug": "google-ads-agentur-konstanz", "depth": 1, "nav": "leistungen",
     "title": "Google Ads Agentur Konstanz | Steinhauer Media",
     "description": "Google & Meta Ads Management von Steinhauer Media: zielgerichtete Kampagnen für kaufbereite Neukunden – für Unternehmen in Konstanz und am Bodensee.",
     "crumbs": [("Leistungen", "leistungen"), ("Google Ads", None)]},
    {"slug": "seo-agentur-konstanz", "depth": 1, "nav": "leistungen",
     "title": "SEO Agentur Konstanz | Steinhauer Media",
     "description": "SEO & GEO für lokale Sichtbarkeit: Steinhauer Media optimiert Website, Content und Google-Unternehmensprofil für Unternehmen in Konstanz und am Bodensee.",
     "crumbs": [("Leistungen", "leistungen"), ("SEO & GEO", None)]},
    {"slug": "webdesign-konstanz", "depth": 1, "nav": "leistungen",
     "title": "Webdesign Konstanz | Steinhauer Media",
     "description": "Steinhauer Media entwickelt schnelle, mobiloptimierte Websites mit interaktiver Live-Vorschau vor Beauftragung – für Unternehmen in Konstanz und am Bodensee.",
     "crumbs": [("Leistungen", "leistungen"), ("Webdesign", None)]},
    {"slug": "social-recruiting", "depth": 1, "nav": "leistungen",
     "title": "Social Recruiting | Steinhauer Media",
     "description": "Authentische Recruiting-Reels gegen den Fachkräftemangel: Steinhauer Media zeigt Team und Arbeitsalltag Ihres Unternehmens für mehr Bewerbungen.",
     "crumbs": [("Leistungen", "leistungen"), ("Social Recruiting", None)]},
    {"slug": "referenzen", "depth": 1, "nav": "referenzen",
     "title": "Referenzen & Ergebnisse | Steinhauer Media",
     "description": "Ausgewählte Projekte von Steinhauer Media – darunter eine Kampagne mit 142 Anfragen bei 17,60 € pro Lead für einen Kunden im Bereich dauerhafte Haarentfernung.",
     "crumbs": [("Referenzen", None)]},
    {"slug": "pakete", "depth": 1, "nav": "pakete",
     "title": "Marketing Pakete | Steinhauer Media",
     "description": "Basis, Komplett-Service oder Vollgas: Die Marketing-Pakete von Steinhauer Media im Vergleich – transparent, flexibel und individuell abstimmbar.",
     "crumbs": [("Pakete", None)]},
    {"slug": "ueber-uns", "depth": 1, "nav": "ueber-uns",
     "title": "Über uns | Steinhauer Media Konstanz",
     "description": "Shawn und Lennert sind Steinhauer Media: zwei Spezialisten für Social-Media-Content und Performance-Marketing mit Sitz am Bodensee.",
     "crumbs": [("Über uns", None)]},
    {"slug": "kontakt", "depth": 1, "nav": "kontakt",
     "title": "Kontakt & Potenzialanalyse | Steinhauer Media",
     "description": "Kontaktieren Sie Steinhauer Media in Konstanz für eine kostenlose Potenzialanalyse – per Telefon, WhatsApp, E-Mail oder Kontaktformular.",
     "crumbs": [("Kontakt", None)]},
    {"slug": "impressum", "depth": 1, "nav": None,
     "title": "Impressum | Steinhauer Media",
     "description": "Impressum von Steinhauer Media.",
     "crumbs": [("Impressum", None)]},
    {"slug": "datenschutz", "depth": 1, "nav": None,
     "title": "Datenschutz | Steinhauer Media",
     "description": "Datenschutzerklärung von Steinhauer Media.",
     "crumbs": [("Datenschutz", None)]},
]
ROUTES_BY_SLUG = {r["slug"]: r for r in ROUTES}

SITEMAP_SLUGS = ["", "leistungen", "social-media-agentur-konstanz",
                  "google-ads-agentur-konstanz", "seo-agentur-konstanz",
                  "webdesign-konstanz", "social-recruiting", "referenzen",
                  "pakete", "ueber-uns", "kontakt", "impressum", "datenschutz"]

NAV_LABELS = {
    "leistungen": "Leistungen", "referenzen": "Referenzen", "pakete": "Pakete",
    "ueber-uns": "Über uns", "kontakt": "Kontakt", "home": "Home",
}

LEISTUNGEN_DROPDOWN = [
    ("social-media-agentur-konstanz", "Social Media"),
    ("social-recruiting", "Social Recruiting"),
    ("webdesign-konstanz", "Webdesign"),
    ("seo-agentur-konstanz", "SEO & GEO"),
    ("google-ads-agentur-konstanz", "Google & Meta Ads"),
    ("leistungen", "Leistungsübersicht"),
]

FOOTER_LEISTUNGEN = LEISTUNGEN_DROPDOWN[:5]
FOOTER_AGENTUR = [("referenzen", "Referenzen"), ("pakete", "Pakete"),
                   ("ueber-uns", "Über uns"), ("kontakt", "Kontakt")]
FOOTER_RECHTLICH = [("impressum", "Impressum"), ("datenschutz", "Datenschutz")]


def href_to(target_slug, depth):
    """Relative href from a page at the given depth to target_slug."""
    prefix = "../" if depth == 1 else ""
    if not target_slug:
        return prefix if depth == 1 else "./"
    return prefix + target_slug + "/"


def asset(path, depth):
    prefix = "../" if depth == 1 else ""
    return prefix + path


# ---------------------------------------------------------------------------
# Head (title, meta, canonical, OG, Twitter, JSON-LD)
# ---------------------------------------------------------------------------
def render_jsonld(route):
    org_id = site_url() + "#organization"
    org = {
        "@context": "https://schema.org",
        "@type": ["ProfessionalService", "Organization"],
        "@id": org_id,
        "name": CONFIG["siteName"],
        "url": site_url(),
        "logo": asset_url("assets/img/logo.png"),
        "image": asset_url("assets/img/logo.png"),
        "email": EMAIL,
        "telephone": PHONES[0]["value"],
        "address": {
            "@type": "PostalAddress",
            "streetAddress": ADDR["street"],
            "postalCode": ADDR["postalCode"],
            "addressLocality": ADDR["city"],
            "addressCountry": ADDR["country"],
        },
        "areaServed": ["Konstanz", "Bodensee"],
    }
    if CO.get("legalName"):
        org["legalName"] = CO["legalName"]
    if INSTAGRAM:
        org["sameAs"] = [INSTAGRAM]

    website = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": CONFIG["siteName"],
        "url": site_url(),
        "inLanguage": CONFIG["language"],
        "publisher": {"@id": org_id},
    }

    blocks = [org, website]

    if route["crumbs"]:
        items = [{"@type": "ListItem", "position": 1, "name": "Startseite", "item": site_url()}]
        pos = 2
        for label, slug in route["crumbs"]:
            item = {"@type": "ListItem", "position": pos, "name": label}
            if slug is not None:
                item["item"] = site_url(slug)
            else:
                item["item"] = site_url(route["slug"])
            items.append(item)
            pos += 1
        blocks.append({
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": items,
        })

    return "\n".join(
        f'<script type="application/ld+json">{json.dumps(b, ensure_ascii=False)}</script>'
        for b in blocks
    )


def render_head(route, extra_head=""):
    slug = route["slug"]
    depth = route["depth"]
    canonical = site_url(slug)
    css = asset("assets/css/style.css", depth)
    og_image = asset_url(CONFIG["ogImage"])
    d = route["description"]
    return f'''<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{route["title"]}</title>
<meta name="description" content="{d}">
<link rel="canonical" href="{canonical}">
<meta name="theme-color" content="#15130E">
<link rel="icon" href="{asset("assets/img/logo.png", depth)}">
<meta property="og:title" content="{route["title"]}">
<meta property="og:description" content="{d}">
<meta property="og:url" content="{canonical}">
<meta property="og:type" content="website">
<meta property="og:image" content="{og_image}">
<meta property="og:site_name" content="{CONFIG["siteName"]}">
<meta property="og:locale" content="{CONFIG["locale"]}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{route["title"]}">
<meta name="twitter:description" content="{d}">
<meta name="twitter:image" content="{og_image}">
<link rel="stylesheet" href="{css}">
{extra_head}
{render_jsonld(route)}'''


# ---------------------------------------------------------------------------
# Nav / breadcrumb / footer
# ---------------------------------------------------------------------------
def render_nav(route):
    depth = route["depth"]
    active_nav = route["nav"]
    home_href = href_to("", depth)
    logo = asset("assets/img/logo.png", depth)

    dd_items = "\n".join(
        f'          <a href="{href_to(s, depth)}" role="menuitem">{label}</a>' +
        ("\n          <div class=\"divider\" role=\"separator\"></div>" if s == "google-ads-agentur-konstanz" else "")
        for s, label in LEISTUNGEN_DROPDOWN
    )

    def link(slug, label, extra=""):
        cls = "active" if active_nav == slug else ""
        return f'<a href="{href_to(slug, depth)}" data-route="{slug}" class="{cls}" {extra}>{label}</a>'

    mobile_dd_items = "\n".join(
        f'      <a href="{href_to(s, depth)}">{label}</a>'
        for s, label in LEISTUNGEN_DROPDOWN
    )
    leistungen_active = "active" if active_nav == "leistungen" else ""

    return f'''<a href="#main" class="skip-link">Zum Inhalt springen</a>
<div id="progress-bar"></div>
<nav id="site-nav">
  <a href="{home_href}" class="nav-emblem">
    <img src="{logo}" alt="Steinhauer Media Logo" width="24" height="24">
    <span>STEINHAUER MEDIA</span>
  </a>
  <div class="nav-links" id="nav-links-mobile">
    <a href="{href_to('kontakt', depth)}" class="mobile-cta-link" style="display:none;">Potenzialanalyse sichern</a>
    <div class="nav-item-dropdown" id="nav-leistungen-dropdown">
      <button type="button" class="nav-dd-trigger {leistungen_active}" aria-haspopup="true" aria-expanded="false" aria-controls="nav-leistungen-menu">
        Leistungen <span class="nav-dd-caret" aria-hidden="true">▾</span>
      </button>
      <div class="nav-dropdown" id="nav-leistungen-menu" role="menu">
{dd_items}
      </div>
      <button type="button" class="mobile-submenu-trigger" aria-expanded="false" aria-controls="mobile-leistungen-submenu">
        <span>Leistungen</span><span class="plus" aria-hidden="true">+</span>
      </button>
      <div class="mobile-submenu" id="mobile-leistungen-submenu">
{mobile_dd_items}
      </div>
    </div>
    {link('referenzen', 'Referenzen')}
    {link('pakete', 'Pakete')}
    {link('ueber-uns', 'Über uns')}
  </div>
  <div class="nav-cta">
    <a href="{href_to('kontakt', depth)}" class="btn primary" style="padding:11px 20px;">Kostenlose Potenzialanalyse</a>
    <button id="nav-toggle" aria-label="Menü öffnen" aria-expanded="false" aria-controls="nav-links-mobile"><span></span><span></span><span></span></button>
  </div>
</nav>'''


def render_breadcrumb(route):
    if not route["crumbs"]:
        return ""
    depth = route["depth"]
    items = [f'<li><a href="{href_to("", depth)}">Startseite</a></li>']
    for label, slug in route["crumbs"]:
        if slug is None:
            items.append(f'<li aria-current="page">{label}</li>')
        else:
            items.append(f'<li><a href="{href_to(slug, depth)}">{label}</a></li>')
    lis = "\n      ".join(items)
    return f'''<nav class="breadcrumb container" aria-label="Breadcrumb">
    <ol>
      {lis}
    </ol>
  </nav>'''


def render_footer(depth):
    leist = "\n          ".join(f'<li><a href="{href_to(s, depth)}">{l}</a></li>' for s, l in FOOTER_LEISTUNGEN)
    agentur = "\n          ".join(f'<li><a href="{href_to(s, depth)}">{l}</a></li>' for s, l in FOOTER_AGENTUR)
    rechtlich = "\n          ".join(f'<li><a href="{href_to(s, depth)}">{l}</a></li>' for s, l in FOOTER_RECHTLICH)
    logo = asset("assets/img/logo.png", depth)
    instagram_html = f'<p style="margin-top:14px;"><a href="{INSTAGRAM}" target="_blank" rel="noopener">Instagram</a></p>' if INSTAGRAM else ""
    return f'''<footer>
  <div class="container">
    <div class="footer-grid">
      <div>
        <div class="lockup" style="margin-bottom:16px;">
          <img src="{logo}" alt="Steinhauer Media Logo" style="height:26px; width:auto;">
          <span class="word" style="color:var(--ivory);">STEINHAUER MEDIA</span>
        </div>
        <p style="max-width:280px; font-size:0.88rem;">Social Media · Performance Marketing · Webdesign<br>Konstanz / Bodensee</p>
        {instagram_html}
      </div>
      <div>
        <h5>Leistungen</h5>
        <ul>
          {leist}
        </ul>
      </div>
      <div>
        <h5>Agentur</h5>
        <ul>
          {agentur}
        </ul>
      </div>
      <div>
        <h5>Rechtlich</h5>
        <ul>
          {rechtlich}
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© 2026 Steinhauer Media. Alle Rechte vorbehalten.</span>
      <span>Entwurf · Version 01</span>
    </div>
  </div>
</footer>'''


def cta_block(heading, btn_text, target_slug, depth):
    return f'''<section class="block tight deep">
    <div class="container" style="text-align:center;">
      <h2>{heading}</h2>
      <div style="margin-top:26px;"><span class="magnetic-wrap" data-magnetic><a href="{href_to(target_slug, depth)}" class="btn primary">{btn_text}</a></span></div>
    </div>
  </section>'''


def upcoming_case_callout(from_slug, anchor, name, category, blurb):
    """A professionally styled 'case study coming soon' teaser -- no invented
    numbers, just a dashed-border placeholder linking to the full write-up
    on the Referenzen page once real, verified figures are available."""
    d = ROUTES_BY_SLUG[from_slug]["depth"]
    return f'''<div class="reveal case-upcoming" style="margin-top:46px;">
      <span class="badge-soft">Case Study folgt</span>
      <h3>{name}</h3>
      <p class="muted" style="margin-top:6px; font-size:0.82rem; letter-spacing:0.06em; text-transform:uppercase;">{category}</p>
      <p class="muted" style="margin-top:14px; max-width:560px;">{blurb}</p>
      <div style="margin-top:20px;"><a href="{href_to('referenzen', d)}#{anchor}" class="link-underline">Zu den Referenzen</a></div>
    </div>'''


def related_links(depth, intro, links):
    a = ", ".join(f'<a href="{href_to(s, depth)}" class="link-underline">{label}</a>' for s, label in links)
    return f'<p class="muted related-links">{intro} {a}.</p>'


LEGACY_HASH_REDIRECT = '''<script>
(function(){
  if(!location.hash) return;
  var h = location.hash.replace('#/','').replace('#','');
  var map = {home:'./', leistungen:'leistungen/', pakete:'pakete/', referenzen:'referenzen/', 'ueber-uns':'ueber-uns/', kontakt:'kontakt/'};
  if(Object.prototype.hasOwnProperty.call(map, h)){
    location.replace(map[h]);
  } else if(h){
    location.replace('./');
  }
})();
</script>'''


def page_shell(route, main_html):
    depth = route["depth"]
    extra_head = LEGACY_HASH_REDIRECT if route["slug"] == "" else ""
    js = asset("assets/js/site.js", depth)
    head = render_head(route, extra_head)
    nav = render_nav(route)
    footer = render_footer(depth)
    return f'''<!DOCTYPE html>
<html lang="de">
<head>
{head}
</head>
<body>
<div class="grain-overlay"></div>
{nav}
<main id="main">
{main_html}
</main>
{footer}
<script src="{js}" defer></script>
</body>
</html>
'''


def write_page(route, main_html):
    path = os.path.join(ROOT, route["slug"], "index.html") if route["slug"] else os.path.join(ROOT, "index.html")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(page_shell(route, main_html))
    print("wrote", os.path.relpath(path, ROOT))


# ---------------------------------------------------------------------------
# Shared icons (verbatim from the original design)
# ---------------------------------------------------------------------------
ICON_SHORTFORM = '<svg class="icon" viewBox="0 0 40 40" fill="none"><path d="M14 12L28 20L14 28V12Z" stroke="#1E1B15" stroke-width="1.3"/></svg>'
ICON_SEO = '<svg class="icon" viewBox="0 0 40 40" fill="none"><circle cx="17" cy="17" r="10" stroke="#1E1B15" stroke-width="1.3"/><path d="M25 25L33 33" stroke="#1E1B15" stroke-width="1.3"/></svg>'
ICON_ADS = '<svg class="icon" viewBox="0 0 40 40" fill="none"><circle cx="20" cy="20" r="12" stroke="#1E1B15" stroke-width="1.3"/><circle cx="20" cy="20" r="5" stroke="#1E1B15" stroke-width="1.3"/><circle cx="20" cy="20" r="1.4" fill="#1E1B15"/></svg>'
ICON_RECRUITING = '<svg class="icon" viewBox="0 0 40 40" fill="none"><path d="M10 30V22C10 18 14 15 20 15C26 15 30 18 30 22V30" stroke="#1E1B15" stroke-width="1.3"/><circle cx="20" cy="10" r="4" stroke="#1E1B15" stroke-width="1.3"/></svg>'
ICON_WEBDESIGN = '<svg class="icon" viewBox="0 0 40 40" fill="none"><rect x="8" y="9" width="24" height="18" stroke="#1E1B15" stroke-width="1.3"/><path d="M8 15H32" stroke="#1E1B15" stroke-width="1.3"/><path d="M14 31H26" stroke="#1E1B15" stroke-width="1.3"/></svg>'

ICON_SHORTFORM_LG = ICON_SHORTFORM.replace('class="icon"', 'class="icon-lg"')
ICON_SEO_LG = ICON_SEO.replace('class="icon"', 'class="icon-lg"')
ICON_ADS_LG = ICON_ADS.replace('class="icon"', 'class="icon-lg"')
ICON_RECRUITING_LG = ICON_RECRUITING.replace('class="icon"', 'class="icon-lg"')
ICON_WEBDESIGN_LG = ICON_WEBDESIGN.replace('class="icon"', 'class="icon-lg"')

CLIENT_LOGOS = [
    ("client-club-aktiv.jpg", "Club Aktiv"),
    ("client-o2.jpg", "o2"),
    ("client-polywerft.jpg", "Polywerft"),
    ("client-staib.jpg", "Staib"),
    ("client-prima-vera-dresses.jpg", "Prima Vera Dresses"),
    ("client-bck-adventure.jpg", "BCK Adventure"),
    ("client-a-gradmann.jpg", "A. Gradmann"),
    ("client-langenbach.jpg", "Langenbach"),
    ("client-freshlineart.jpg", "FreshLineArt"),
]


def render_client_logos(depth):
    rows = "\n          ".join(
        f'<div class="logo-chip"><img src="{asset("assets/img/" + f, depth)}" alt="{alt}" loading="lazy" width="130" height="32"></div>'
        for f, alt in CLIENT_LOGOS
    )
    return f'''<div class="logo-row">
          {rows}
        </div>'''



# ---------------------------------------------------------------------------
# Counter helper -- real value must be present in the static HTML.
# ---------------------------------------------------------------------------
FAQ_ZEITAUFWAND_A = (
    "In der Regel benötigen wir etwa 30–60 Minuten pro Woche für den gemeinsamen "
    "Drehtermin. Planung, Skripte, Schnitt, Veröffentlichung und Auswertung übernehmen "
    "wir. Monatlich erhalten Sie einen kompakten Performance-Bericht; alle drei Monate "
    "analysieren wir die Entwicklung ausführlich und leiten die nächsten Maßnahmen ab."
)


def counter_text(count, decimals=0, prefix="", suffix=""):
    val = f"{count:.{decimals}f}".replace(".", ",")
    return f"{prefix}{val}{suffix}"


def counter_span(count, decimals=0, prefix="", suffix="", extra_class=""):
    text = counter_text(count, decimals, prefix, suffix)
    dataset = f'data-count="{count}"'
    if decimals:
        dataset += f' data-decimal="{decimals}"'
    if prefix:
        dataset += f' data-prefix="{prefix}"'
    if suffix:
        dataset += f' data-suffix="{suffix}"'
    return f'<div class="num {extra_class}" {dataset}>{text}</div>'


# ---------------------------------------------------------------------------
# HOME
# ---------------------------------------------------------------------------
def page_home():
    route = ROUTES_BY_SLUG[""]
    d = route["depth"]
    logos = render_client_logos(d)
    main = f'''<section class="hero">
    <div class="hero-scene">
      <div class="hero-grid" id="hero-grid"></div>
      <div class="hero-glow"></div>
      <svg class="hero-emblem" id="hero-emblem" viewBox="0 0 400 400" fill="none">
        <path d="M200 40L360 140H40L200 40Z" stroke="#1E1B15" stroke-width="1"/>
        <path d="M70 150V340M130 150V340M270 150V340M330 150V340" stroke="#1E1B15" stroke-width="0.8"/>
        <path d="M50 345H350" stroke="#1E1B15" stroke-width="1"/>
        <circle cx="200" cy="90" r="10" stroke="#1E1B15" stroke-width="1"/>
      </svg>
      <!-- TODO: sobald das Hero-Video vorliegt (Shawn & Lennert bei echten Kundendrehs: Kamera,
           Skript, Kundendreh, Smartphone/Reel, Schnitt, Analytics, Kundengespräch), diesen
           Platzhalter durch <video autoplay muted loop playsinline> ersetzen. Kein Stockvideo verwenden. -->
      <div class="hero-placeholder"><span>PLATZHALTER<br>Foto / Video<br>folgt</span></div>
    </div>
    <div class="container hero-inner">
      <div class="hero-kicker">
        <svg class="em" viewBox="0 0 40 40" fill="none" aria-hidden="true"><path d="M20 6L35 17H5L20 6Z" stroke="#1E1B15" stroke-width="1.4"/></svg>
        <span>Social Media &amp; Performance Marketing · Konstanz</span>
      </div>
      <h1 id="hero-headline">Mehr Sichtbarkeit. Mehr Anfragen. Messbar.</h1>
      <p class="lead">Wir helfen Unternehmen am Bodensee mit Social Media, Google und Performance Marketing dabei, aus Aufmerksamkeit echte Kunden zu machen.</p>
      <div class="hero-actions">
        <span class="magnetic-wrap" data-magnetic><a href="{href_to('kontakt', d)}" class="btn primary">Kostenlose Potenzialanalyse</a></span>
        <a href="#ergebnisse" class="link-underline" style="color:var(--ink-soft);">Unsere Ergebnisse ansehen</a>
      </div>
    </div>
    <div class="hero-scroll"><div class="line"></div><span>Scrollen</span></div>
  </section>

  <section class="block tight">
    <div class="container">
      <div class="reveal" style="text-align:center;">
        <p class="muted" style="font-size:0.82rem; letter-spacing:0.1em; text-transform:uppercase;">Vertraut von Unternehmen aus der Region</p>
      </div>
      <!-- TODO: sobald weitere freigegebene Kundenlogos vorliegen, hier ergänzen -->
      {logos}
      <div class="stats-grid stats-grid-5 reveal-stagger" style="margin-top:56px;">
        <div class="stat-item">{counter_span(100, suffix="%")}<div class="lbl">Fokus auf Kundenzufriedenheit</div></div>
        <div class="stat-item">{counter_span(3, suffix="+")}<div class="lbl">Jahre Erfahrung</div></div>
        <div class="stat-item">{counter_span(5, suffix=" Mio.+")}<div class="lbl">Views generiert</div></div>
        <div class="stat-item">{counter_span(120, suffix="k+")}<div class="lbl">Likes gesammelt</div></div>
        <div class="stat-item">{counter_span(30, suffix="+")}<div class="lbl">Glückliche Kunden</div></div>
      </div>
    </div>
  </section>

  <section class="block deep">
    <div class="container">
      <div class="reveal">
        <h2>DAS PROBLEM</h2>
        <p class="prose muted" style="margin-top:18px;">Die meisten Unternehmen scheitern nicht an fehlendem Aufwand, sondern an fehlender Strategie zwischen Content, Werbung und Website.</p>
      </div>
      <div class="split-cols">
        <div class="reveal problem-list">
          <div class="principle">
            <div class="n" aria-hidden="true">01</div>
            <h3>Content ohne klare Strategie</h3>
            <p>Es wird regelmäßig gepostet, aber Reichweite und Anfragen bleiben aus.</p>
          </div>
          <div class="principle">
            <div class="n" aria-hidden="true">02</div>
            <h3>Werbebudget ohne nachvollziehbare Ergebnisse</h3>
            <p>Kampagnen laufen, aber niemand weiß genau, welche Anfragen tatsächlich daraus entstehen.</p>
          </div>
          <div class="principle">
            <div class="n" aria-hidden="true">03</div>
            <h3>Bei Google kaum sichtbar</h3>
            <p>Potenzielle Kunden suchen nach der Leistung – finden aber Wettbewerber zuerst.</p>
          </div>
        </div>
        <div class="reveal">
          <h3>UNSER ANSATZ</h3>
          <ul>
            <li><span class="mark" aria-hidden="true">+</span>Content, der Reichweite und Vertrauen aufbaut</li>
            <li><span class="mark" aria-hidden="true">+</span>Google &amp; Meta Ads für qualifizierte Anfragen</li>
            <li><span class="mark" aria-hidden="true">+</span>Websites und SEO, die Besucher zu Kunden führen</li>
          </ul>
        </div>
      </div>
    </div>
  </section>

  <section class="block">
    <div class="container">
      <div class="reveal">
        <h2>Drei Leistungen, ein System.</h2>
        <p class="prose muted" style="margin-top:16px;">Content, Werbung und digitale Infrastruktur greifen bei uns ineinander, um Unternehmen sichtbar zu machen und Kundenanfragen zu erzeugen.</p>
      </div>
      <div class="service-grid reveal-stagger">
        <a href="{href_to('social-media-agentur-konstanz', d)}" class="service-card" data-tilt>
          {ICON_SHORTFORM}
          <span class="tag">01 — Content</span>
          <h3>Social Media &amp; Video</h3>
          <p>Strategie, Ideen, Skripte, Drehs und Short-Form Content für Unternehmen.</p>
          <span class="link-underline" style="margin-top:18px; display:inline-block;">Social Media ansehen</span>
        </a>
        <a href="{href_to('webdesign-konstanz', d)}" class="service-card" data-tilt>
          {ICON_WEBDESIGN}
          <span class="tag">03 — Web &amp; Search</span>
          <h3>Website, SEO &amp; GEO</h3>
          <p>Schnelle Websites und Suchmaschinenoptimierung, damit Unternehmen gefunden werden und Besucher zu Anfragen werden.</p>
          <span class="link-underline" style="margin-top:18px; display:inline-block;">Website &amp; SEO ansehen</span>
        </a>
        <a href="{href_to('google-ads-agentur-konstanz', d)}" class="service-card" data-tilt>
          {ICON_ADS}
          <span class="tag">05 — Performance</span>
          <h3>Google &amp; Meta Ads</h3>
          <p>Werbekampagnen, Tracking und Landingpages für qualifizierte Kundenanfragen.</p>
          <span class="link-underline" style="margin-top:18px; display:inline-block;">Performance Marketing ansehen</span>
        </a>
      </div>
      <p class="muted" style="margin-top:28px; font-size:0.92rem;">Zusätzlich: <a href="{href_to('social-recruiting', d)}" class="link-underline">Social Recruiting</a> — Mitarbeiter dort erreichen, wo sie jeden Tag unterwegs sind.</p>
    </div>
  </section>

  <section class="block deep">
    <div class="container">
      <div class="reveal">
        <h2>Ausgewählte Projekte</h2>
        <p class="prose muted" style="margin-top:16px;">Eine Auswahl an Unternehmen, mit denen wir bereits zusammengearbeitet haben.</p>
      </div>
      <!-- TODO: Branche, durchgeführte Leistungen und belegbare Kennzahlen pro Projekt ergänzen, sobald freigegeben -->
      <div class="projects-grid reveal-stagger" style="margin-top:44px;">
        <div class="project-card"><img src="{asset('assets/img/client-club-aktiv.jpg', d)}" alt="Club Aktiv" loading="lazy" width="130" height="32"><span class="v">Club Aktiv</span></div>
        <div class="project-card"><img src="{asset('assets/img/client-polywerft.jpg', d)}" alt="Polywerft" loading="lazy" width="130" height="32"><span class="v">Polywerft</span></div>
        <div class="project-card"><img src="{asset('assets/img/client-bck-adventure.jpg', d)}" alt="BCK Adventure" loading="lazy" width="130" height="32"><span class="v">BCK Adventure</span></div>
        <div class="project-card"><img src="{asset('assets/img/client-staib.jpg', d)}" alt="Staib" loading="lazy" width="130" height="32"><span class="v">Staib</span></div>
      </div>
      <div style="margin-top:34px;"><a href="{href_to('referenzen', d)}" class="link-underline">Alle Referenzen ansehen</a></div>
    </div>
  </section>

  <section class="prozess-block">
    <div class="prozess-scroll" id="prozess-scroll" style="height:180vh;">
      <div class="prozess-sticky">
        <div class="container">
          <div class="prozess-grid">
            <div class="prozess-pin">
              <div class="prozess-index" id="prozess-index" aria-hidden="true">01 / 05</div>
              <h2>Social Media, das planbar Kunden bringt.</h2>
              <p>Von der ersten Idee bis zum Umsatz — ein durchdachter Prozess statt Zufallstreffer.</p>
              <div class="prozess-bar"><i id="prozess-bar-fill"></i></div>
            </div>
            <div class="prozess-steps">
              <div class="prozess-step active" data-step="1"><span class="num">STRATEGIE</span><h3>Zielgruppen &amp; Botschaft</h3><p>Zielgruppen, Kernbotschaft und Kanäle werden präzise auf Ihr Angebot abgestimmt.</p></div>
              <div class="prozess-step" data-step="2"><span class="num">PRODUKTION</span><h3>Skript, Dreh, Schnitt</h3><p>Wir übernehmen Skript, Dreh vor Ort und professionellen Schnitt — ganz ohne Aufwand für Sie.</p></div>
              <div class="prozess-step" data-step="3"><span class="num">ADS</span><h3>Google &amp; Meta</h3><p>Gezielte Kampagnen bringen den Content genau zu den Menschen, die kaufbereit sind.</p></div>
              <div class="prozess-step" data-step="4"><span class="num">LEADS</span><h3>Planbare Anfragen</h3><p>Qualifizierte Anfragen laufen regelmäßig und nachvollziehbar bei Ihnen ein.</p></div>
              <div class="prozess-step" data-step="5"><span class="num">UMSATZ</span><h3>Messbares Wachstum</h3><p>Aus Sichtbarkeit wird Wachstum — Monat für Monat transparent nachvollziehbar.</p></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section class="block" id="ergebnisse">
    <div class="container">
      <div class="reveal" style="max-width:720px;">
        <p class="muted" style="font-size:0.82rem; letter-spacing:0.1em; text-transform:uppercase;">Case Study</p>
        <h2 style="margin-top:14px;">142 qualifizierte Anfragen für eine lokale Dienstleisterin.</h2>
        <p class="muted" style="margin-top:12px;">Google Search Ads + Meta Retargeting</p>
      </div>
      <div class="case-grid case-grid-3 reveal-stagger" style="margin-top:44px;">
        <div class="case-card">{counter_span(142)}<div class="lbl">Anfragen</div></div>
        <div class="case-card">{counter_span(17.6, decimals=1, prefix="€")}<div class="lbl">Cost per Lead</div></div>
        <div class="case-card">{counter_span(8.4, decimals=1, suffix="%")}<div class="lbl">Conversion Rate</div></div>
      </div>
      <div class="case-study-grid reveal-stagger" style="margin-top:56px;">
        <div>
          <h4>Ausgangslage</h4>
          <p class="muted">Eine Kundin im Bereich dauerhafte Haarentfernung in Regensburg wollte planbar mehr qualifizierte Anfragen gewinnen, statt sich auf Zufallslaufkundschaft zu verlassen.</p>
        </div>
        <div>
          <h4>Strategie</h4>
          <p class="muted">Kombination aus Google Search Ads für aktive Suchanfragen und Meta-Retargeting, um Interessenten erneut gezielt anzusprechen.</p>
        </div>
        <div>
          <h4>Umsetzung</h4>
          <p class="muted">Kampagnenstruktur, Zielgruppen, Landingpage und Tracking wurden aufgesetzt und laufend anhand der Ergebnisse optimiert.</p>
        </div>
        <div>
          <h4>Ergebnis</h4>
          <p class="muted">142 qualifizierte Neukundenanfragen bei 17,60&nbsp;€ Cost per Lead und einer Conversion-Rate von 8,4&nbsp;%.</p>
        </div>
      </div>
      <div style="margin-top:34px;"><a href="{href_to('referenzen', d)}" class="link-underline">Case Study ansehen</a></div>
    </div>
  </section>

  <section class="block deep">
    <div class="container">
      <div class="service-detail reveal" style="border-top:none; padding-top:0;">
        <div>
          {ICON_WEBDESIGN_LG}
        </div>
        <div>
          <h2>Sehen Sie Ihre neue Website, bevor Sie uns beauftragen.</h2>
          <p class="muted" style="margin-top:16px;">Keine abstrakten PDF-Konzepte. Für ausgewählte Projekte erstellen wir einen interaktiven Prototyp, den Sie direkt auf Smartphone und Desktop testen können.</p>
          <div style="margin-top:26px; display:flex; gap:20px; flex-wrap:wrap;">
            <a href="{href_to('webdesign-konstanz', d)}" class="btn primary">Webdesign ansehen</a>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section class="block">
    <div class="container">
      <div class="reveal" style="max-width:640px;">
        <h2>Zwei Spezialisten. Ein Ansprechpartner für Ihre digitale Sichtbarkeit.</h2>
      </div>
      <div class="team-grid" style="margin-top:44px;">
        <div class="team-card reveal">
          <img class="team-photo" src="{asset('assets/img/team-shawn.jpg', d)}" alt="Shawn, Social Media Spezialist bei Steinhauer Media" width="84" height="84">
          <h3 style="font-size:1.1rem;">Shawn</h3>
          <p class="gold" style="font-size:0.82rem; letter-spacing:0.06em; margin-top:4px;">Social Media &amp; organisches Wachstum</p>
          <p>Verantwortlich für Social-Media-Strategie, Content, Drehs, Reels und organisches Wachstum.</p>
        </div>
        <div class="team-card reveal">
          <img class="team-photo" src="{asset('assets/img/team-lennert.jpg', d)}" alt="Lennert, Spezialist für Websites und Performance Marketing bei Steinhauer Media" width="84" height="84">
          <h3 style="font-size:1.1rem;">Lennert</h3>
          <p class="gold" style="font-size:0.82rem; letter-spacing:0.06em; margin-top:4px;">Websites &amp; Performance Marketing</p>
          <p>Verantwortlich für Webdesign, SEO, Google Ads, Meta Ads und Tracking.</p>
        </div>
      </div>
      <div style="margin-top:30px;"><a href="{href_to('ueber-uns', d)}" class="link-underline">Mehr über uns</a></div>
    </div>
  </section>

  <section class="block deep">
    <div class="container">
      <div class="reveal">
        <h2>Pakete für planbare Ergebnisse.</h2>
        <p class="prose muted" style="margin-top:16px;">Drei Modelle als Ausgangspunkt — das passende Paket stimmen wir individuell mit Ihnen ab.</p>
      </div>
      <div class="pricing-grid" style="margin-top:44px;">
        <div class="pricing-card reveal">
          <h3>Basis</h3>
          <p class="muted" style="margin-top:8px; font-size:0.9rem;">Für den soliden Einstieg</p>
          <ul>
            <li>4 Reels pro Monat</li>
            <li>Instagram &amp; Facebook</li>
            <li>Dreh vor Ort &amp; Schnitt</li>
          </ul>
          <p class="muted" style="font-size:0.85rem; margin-top:auto; padding-top:16px;">Für wen geeignet? Unternehmen, die professionell mit Social Media starten möchten.</p>
        </div>
        <div class="pricing-card featured reveal">
          <span class="badge">Meistgewählt</span>
          <h3>Komplett-Service</h3>
          <p class="muted" style="margin-top:8px; font-size:0.9rem;">Content plus Sichtbarkeit</p>
          <ul>
            <li>8 Short-Form Videos / Monat</li>
            <li>SEO- &amp; GEO-Optimierung</li>
            <li>Community Management</li>
          </ul>
          <p class="muted" style="font-size:0.85rem; margin-top:auto; padding-top:16px;">Für wen geeignet? Unternehmen, die Content und digitale Sichtbarkeit aus einer Hand möchten.</p>
        </div>
        <div class="pricing-card reveal">
          <h3>Vollgas</h3>
          <p class="muted" style="margin-top:8px; font-size:0.9rem;">Maßgeschneidert, alle Kanäle</p>
          <ul>
            <li>Bis zu 15 Videos / Monat</li>
            <li>Instagram, Facebook &amp; TikTok</li>
            <li>SEO, GEO &amp; Website</li>
          </ul>
          <p class="muted" style="font-size:0.85rem; margin-top:auto; padding-top:16px;">Für wen geeignet? Unternehmen, die Content, Ads und Website kombinieren möchten.</p>
        </div>
      </div>
      <div style="margin-top:34px;"><a href="{href_to('pakete', d)}" class="link-underline">Pakete ansehen</a></div>
    </div>
  </section>

  <section class="block">
    <div class="container">
      <div class="reveal" style="max-width:640px;">
        <h2>Häufig gestellte Fragen.</h2>
      </div>
      <div style="max-width:760px; margin-top:30px;">
        <div class="faq-item reveal">
          <button type="button" class="faq-q" aria-expanded="false"><span>Wie viel Zeitaufwand entsteht für mein Team und mich?</span><span class="plus" aria-hidden="true">+</span></button>
          <div class="faq-a"><p>{FAQ_ZEITAUFWAND_A}</p></div>
        </div>
        <div class="faq-item reveal">
          <button type="button" class="faq-q" aria-expanded="false"><span>Gibt es lange Vertragslaufzeiten?</span><span class="plus" aria-hidden="true">+</span></button>
          <div class="faq-a"><p>Nein. Wir setzen auf partnerschaftliche Zusammenarbeit auf Augenhöhe mit flexiblen Monatsmodellen.</p></div>
        </div>
      </div>
      <div style="margin-top:26px;"><a href="{href_to('pakete', d)}" class="link-underline">Weitere Fragen ansehen</a></div>
    </div>
  </section>

  <section class="block tight">
    <div class="container">
      <div class="cta-mask reveal" data-mask>
        <p style="color:var(--gold-bright); font-size:0.8rem; letter-spacing:0.14em; text-transform:uppercase; position:relative; z-index:1;">Kostenlose Potenzialanalyse</p>
        <h2 style="margin-top:16px;">Finden wir heraus, wo Ihr größtes digitales Potenzial liegt.</h2>
        <p>In einem unverbindlichen Gespräch schauen wir uns an:</p>
        <ul class="check-list" style="text-align:left; max-width:460px; margin:22px auto 0; position:relative; z-index:1;">
          <li>wie sichtbar Ihr Unternehmen aktuell ist</li>
          <li>wo potenzielle Kunden verloren gehen</li>
          <li>welche Kanäle für Ihr Unternehmen sinnvoll sind</li>
          <li>welche nächsten Schritte sinnvoll wären</li>
        </ul>
        <div class="btn-zone">
          <span class="magnetic-wrap" data-magnetic><a href="{href_to('kontakt', d)}" class="btn on-dark primary" style="background:var(--gold-bright); color:var(--dark); border-color:var(--gold-bright);">Kostenlose Potenzialanalyse anfragen</a></span>
        </div>
        <p class="muted" style="margin-top:16px; font-size:0.82rem; position:relative; z-index:1;">Unverbindlich · keine Vorbereitung notwendig</p>
        <div class="contact-quick">
          <div class="item"><div class="k" style="color:rgba(246,241,228,0.5);">Adresse</div><div class="v" style="color:var(--ivory);">{ADDRESS_LINE}</div></div>
          <div class="item"><div class="k" style="color:rgba(246,241,228,0.5);">E-Mail</div><div class="v" style="color:var(--ivory);">{EMAIL}</div></div>
          <div class="item"><div class="k" style="color:rgba(246,241,228,0.5);">Telefon</div><div class="v" style="color:var(--ivory);">{PHONES[0]["value"]}</div></div>
        </div>
      </div>
    </div>
  </section>'''
    write_page(route, main)

# ---------------------------------------------------------------------------
# LEISTUNGEN (overview)
# ---------------------------------------------------------------------------
def page_leistungen():
    route = ROUTES_BY_SLUG["leistungen"]
    d = route["depth"]
    crumb = render_breadcrumb(route)
    cards = [
        ("social-media-agentur-konstanz", ICON_SHORTFORM, "01", "Social Media &amp; Video", "Strategie, Ideen, Skripte, Drehs und Short-Form Content für Unternehmen."),
        ("social-recruiting", ICON_RECRUITING, "02", "Social Recruiting", "Mitarbeiter dort erreichen, wo sie jeden Tag unterwegs sind."),
        ("webdesign-konstanz", ICON_WEBDESIGN, "03", "Webdesign", "Schnelle, moderne Websites — vorab live und interaktiv zum Testen, bevor Sie uns beauftragen."),
        ("seo-agentur-konstanz", ICON_SEO, "04", "SEO &amp; GEO", "Local SEO, technische SEO und GEO für nachhaltige Sichtbarkeit bei Google."),
        ("google-ads-agentur-konstanz", ICON_ADS, "05", "Google &amp; Meta Ads", "Werbekampagnen, Tracking und Landingpages für qualifizierte Kundenanfragen."),
    ]
    card_html = "\n    ".join(f'''<a class="service-detail reveal" href="{href_to(slug, d)}" style="text-decoration:none; color:inherit;">
      <div>
        {icon}
        <span class="tag gold" style="font-size:0.72rem; letter-spacing:0.1em; text-transform:uppercase;">{num}</span>
        <h2 style="margin-top:8px;">{name}</h2>
      </div>
      <div>
        <p class="muted">{desc}</p>
        <span class="link-underline">Mehr erfahren</span>
      </div>
    </a>''' for slug, icon, num, name, desc in cards)

    main = f'''{crumb}
  <section class="page-hero">
    <div class="container">
      <div class="kicker">Leistungen</div>
      <h1 style="font-size:clamp(1.9rem,4vw,3rem);">Alles aus einer Hand — von der Idee bis zum Umsatz.</h1>
      <p class="prose muted" style="margin-top:18px;">Fünf Bausteine, die einzeln funktionieren und gemeinsam ihre volle Wirkung entfalten.</p>
    </div>
  </section>

  <section class="container">
    {card_html}
  </section>

  {cta_block("Bereit für den ersten Schritt?", "Kostenlose Potenzialanalyse", "kontakt", d)}'''
    write_page(route, main)


# ---------------------------------------------------------------------------
# Shared shell for the 5 dedicated service pages
# ---------------------------------------------------------------------------
def service_page(slug, kicker_num, icon_lg, heading, lead, bullets, related_intro, related_targets,
                  cta_text="Kostenlose Potenzialanalyse", workflow=None, callout="", note=""):
    route = ROUTES_BY_SLUG[slug]
    d = route["depth"]
    crumb = render_breadcrumb(route)
    lis = "\n          ".join(f'<li>{b}</li>' for b in bullets)
    related = related_links(d, related_intro, related_targets)
    workflow_html = ""
    if workflow:
        steps = "\n        ".join(
            f'<div class="workflow-step"><span class="n">{i+1:02d}</span><span>{step}</span></div>' +
            ("<span class=\"workflow-arrow\" aria-hidden=\"true\">→</span>" if i < len(workflow) - 1 else "")
            for i, step in enumerate(workflow)
        )
        workflow_html = f'''<div class="reveal workflow-row" style="margin-top:46px;">
        {steps}
      </div>'''
    note_html = f'<p class="muted" style="margin-top:22px; font-size:0.85rem;">{note}</p>' if note else ""
    main = f'''{crumb}
  <section class="page-hero">
    <div class="container">
      <div class="kicker">Leistungen · {kicker_num}</div>
      <h1 style="font-size:clamp(1.9rem,4vw,3rem);">{heading}</h1>
      <p class="prose muted" style="margin-top:18px;">{lead}</p>
    </div>
  </section>

  <section class="container" style="padding-bottom:20px;">
    <div class="service-detail reveal">
      <div>
        {icon_lg}
      </div>
      <div>
        <ul>
          {lis}
        </ul>
        {note_html}
        {related}
      </div>
    </div>
    {workflow_html}
    {callout}
  </section>

  {cta_block("Bereit für den ersten Schritt?", cta_text, "kontakt", d)}'''
    write_page(route, main)


def page_social_media():
    service_page(
        "social-media-agentur-konstanz", "01", ICON_SHORTFORM_LG,
        "Social Media für Unternehmen in Konstanz &amp; am Bodensee.",
        "Strategie, Ideen, Skripte, Drehs und Short-Form Content für Unternehmen — von der ersten Idee bis zum veröffentlichten Reel.",
        [
            "Strategie &amp; Content-Planung",
            "Ideen &amp; Skripte",
            "Drehs vor Ort",
            "Schnitt",
            "Reels &amp; Instagram-Betreuung",
            "TikTok",
            "Posting",
            "Reporting",
        ],
        "Passt gut dazu:",
        [("google-ads-agentur-konstanz", "Google & Meta Ads"), ("referenzen", "Referenzen"), ("kontakt", "Kontakt")],
        cta_text="Social-Media-Potenzial besprechen",
        workflow=["Strategie", "Skript", "Dreh", "Schnitt", "Veröffentlichung", "Analyse"],
        callout=upcoming_case_callout(
            "social-media-agentur-konstanz", "case-club-aktiv", "Club Aktiv",
            "Social Media · organisches Instagram-Wachstum",
            "Ein lokales Fitnessstudio, für das wir organische Social-Media-Präsenz und Community-Aufbau umsetzen. Die vollständige Case Study folgt, sobald die Ergebnisse final ausgewertet sind.",
        ),
    )


def page_google_ads():
    case_callout = f'''<div class="reveal case-callout" style="margin-top:46px;">
      <p class="muted" style="font-size:0.82rem; letter-spacing:0.1em; text-transform:uppercase;">Ergebnis aus der Praxis</p>
      <div class="case-grid case-grid-3" style="margin-top:20px;">
        <div class="case-card">{counter_span(142)}<div class="lbl">Anfragen</div></div>
        <div class="case-card">{counter_span(17.6, decimals=1, prefix="€")}<div class="lbl">Cost per Lead</div></div>
        <div class="case-card">{counter_span(8.4, decimals=1, suffix="%")}<div class="lbl">Conversion Rate</div></div>
      </div>
      <p class="muted" style="margin-top:16px; font-size:0.9rem;">Google Search Ads + Meta Retargeting für eine lokale Dienstleisterin. <a href="../referenzen/" class="link-underline">Case Study ansehen</a></p>
    </div>'''
    service_page(
        "google-ads-agentur-konstanz", "05", ICON_ADS_LG,
        "Google Ads für Unternehmen in Konstanz und am Bodensee.",
        "Werbekampagnen, Tracking und Landingpages für qualifizierte Kundenanfragen — Meta Ads ergänzen die Strategie dort, wo es sinnvoll ist.",
        [
            "Search Ads",
            "Keyword-Recherche",
            "Tracking",
            "Landingpages",
            "Kampagnenoptimierung",
            "Retargeting",
            "Reporting",
        ],
        "Passt gut dazu:",
        [("referenzen", "Case Study ansehen"), ("kontakt", "Kontakt")],
        cta_text="Ads-Potenzial besprechen",
        callout=case_callout,
    )


def page_seo():
    service_page(
        "seo-agentur-konstanz", "04", ICON_SEO_LG,
        "Bei Google gefunden werden, wenn Kunden nach Ihrer Leistung suchen.",
        "Local SEO, technische SEO und GEO, damit Unternehmen dort gefunden werden, wo potenzielle Kunden tatsächlich suchen.",
        [
            "Local SEO",
            "Technische SEO",
            "On-Page SEO",
            "Content",
            "Google Unternehmensprofil",
            "Lokale Suchanfragen",
            "Strukturierte Daten",
            "GEO / KI-Sichtbarkeit",
        ],
        "Passt gut dazu:",
        [("webdesign-konstanz", "Webdesign"), ("kontakt", "Kontakt")],
        cta_text="SEO-Potenzial prüfen",
        note="Wir versprechen keine bestimmten Rankings, sondern arbeiten kontinuierlich und nachvollziehbar an nachhaltiger Sichtbarkeit.",
    )


def page_webdesign():
    d = ROUTES_BY_SLUG["webdesign-konstanz"]["depth"]
    demo_section = f'''<div class="reveal" style="margin-top:70px; max-width:680px;">
      <p class="muted" style="font-size:0.82rem; letter-spacing:0.1em; text-transform:uppercase;">Interaktive Website-Demo</p>
      <h2 style="margin-top:14px;">Nicht nur ansehen. Direkt ausprobieren.</h2>
      <p class="muted" style="margin-top:14px;">Für ausgewählte Projekte erstellen wir bereits vor der finalen Entscheidung einen klickbaren Prototyp. So sehen Sie nicht nur ein Konzept – Sie erleben bereits, wie Ihre zukünftige Website funktionieren könnte.</p>
    </div>
    <div class="reveal proto-frame lg" style="margin-top:36px;">
      <div class="proto-toggle">
        <button type="button" class="proto-btn active" data-view="desktop" aria-pressed="true">🖥 Desktop</button>
        <button type="button" class="proto-btn" data-view="mobile" aria-pressed="false">📱 Smartphone</button>
        <a href="https://zahnarzt.steinhauermedia.de" target="_blank" rel="noopener" class="link-underline proto-openlink">Demo in neuem Tab öffnen</a>
      </div>
      <div class="proto-viewport view-desktop" id="proto-viewport">
        <iframe src="https://zahnarzt.steinhauermedia.de" title="Interaktive Website-Demo Zahnarztpraxis" loading="lazy"></iframe>
      </div>
    </div>'''
    service_page(
        "webdesign-konstanz", "03", ICON_WEBDESIGN_LG,
        "Websites, die gut aussehen und aus Besuchern Anfragen machen.",
        "Schnelle, moderne Websites — vorab live und interaktiv zum Testen, bevor Sie uns beauftragen.",
        [
            "Konzeption",
            "UI/UX",
            "Responsive Umsetzung",
            "Mobile",
            "Performance",
            "SEO",
            "Conversion",
            "Analytics",
            "Deployment",
        ],
        "Passt gut dazu:",
        [("seo-agentur-konstanz", "SEO & GEO"), ("referenzen", "Referenzen"), ("kontakt", "Kontakt")],
        cta_text="Website-Prototyp anfragen",
        callout=demo_section,
    )


def page_social_recruiting():
    service_page(
        "social-recruiting", "02", ICON_RECRUITING_LG,
        "Mitarbeiter dort erreichen, wo sie jeden Tag unterwegs sind.",
        "Authentische Recruiting-Reels und gezielte Meta-Kampagnen für Unternehmen, die neue Mitarbeitende suchen.",
        [
            "Recruiting Reels",
            "Arbeitgeberpositionierung",
            "Mitarbeiterinterviews",
            "Arbeitsalltag",
            "Meta-Kampagnen",
            "Bewerbungsfunnels",
        ],
        "Passt gut dazu:",
        [("social-media-agentur-konstanz", "Social Media"), ("kontakt", "Kontakt")],
        cta_text="Recruiting-Potenzial besprechen",
        note="Wir garantieren keine bestimmte Bewerberzahl, sondern qualifizierte Sichtbarkeit bei potenziellen Mitarbeitenden.",
        callout=upcoming_case_callout(
            "social-recruiting", "case-polywerft", "Polywerft Konstanz",
            "Social Recruiting",
            "Eine Recruiting-Kampagne, mit der wir Mitarbeiter für Polywerft Konstanz gewinnen. Die vollständige Case Study folgt, sobald die Ergebnisse final ausgewertet sind.",
        ),
    )

# ---------------------------------------------------------------------------
# PAKETE
# ---------------------------------------------------------------------------
def page_pakete():
    route = ROUTES_BY_SLUG["pakete"]
    d = route["depth"]
    crumb = render_breadcrumb(route)
    main = f'''{crumb}
  <section class="page-hero">
    <div class="container">
      <div class="kicker">Pakete</div>
      <h1 style="font-size:clamp(1.9rem,4vw,3rem);">Transparente Zusammenarbeit, planbare Ergebnisse.</h1>
      <p class="prose muted" style="margin-top:18px;">Drei Modelle als Ausgangspunkt — das passende Paket stimmen wir immer individuell mit Ihnen ab.</p>
    </div>
  </section>

  <section class="container" style="padding-bottom:100px;">
    <div class="pricing-grid">
      <div class="pricing-card reveal">
        <h2 style="font-size:1.3rem;">Basis Paket</h2>
        <p class="muted" style="margin-top:8px; font-size:0.9rem;">Der solide Einstieg in Social Media</p>
        <ul>
          <li>Community Management &amp; Reporting</li>
          <li>4 Reels pro Monat</li>
          <li>Instagram- &amp; Facebook-Betreuung</li>
          <li>Ideengenerierung &amp; Skript</li>
          <li>Video-Dreh vor Ort &amp; Schnitt</li>
          <li>Caption, Cover &amp; Posting</li>
        </ul>
        <p class="muted" style="font-size:0.85rem; margin-bottom:20px;">Für wen geeignet? Unternehmen, die professionell mit Social Media starten möchten.</p>
        <a href="mailto:{EMAIL}" class="btn" style="text-align:center; justify-content:center;">Kostenloses Angebot</a>
      </div>
      <div class="pricing-card featured reveal">
        <span class="badge">Meistgewählt</span>
        <h2 style="font-size:1.3rem;">Komplett-Service</h2>
        <p class="muted" style="margin-top:8px; font-size:0.9rem;">Content plus Sichtbarkeit aus einer Hand</p>
        <ul>
          <li>Alle Leistungen aus dem Basis Paket</li>
          <li>8 Short-Form Videos pro Monat</li>
          <li>SEO &amp; GEO Website-Optimierung</li>
          <li>Regelmäßiges Performance-Reporting</li>
        </ul>
        <p class="muted" style="font-size:0.85rem; margin-bottom:20px;">Für wen geeignet? Unternehmen, die Content und digitale Sichtbarkeit aus einer Hand möchten.</p>
        <a href="mailto:{EMAIL}" class="btn on-dark" style="text-align:center; justify-content:center;">Kostenloses Angebot</a>
      </div>
      <div class="pricing-card reveal">
        <h2 style="font-size:1.3rem;">Vollgas Paket</h2>
        <p class="muted" style="margin-top:8px; font-size:0.9rem;">Maßgeschneidert für maximales Tempo</p>
        <ul>
          <li>Alle Leistungen aus dem Komplett-Service</li>
          <li>Bis zu 15 Short-Form Videos pro Monat</li>
          <li>Zusätzlich TikTok-Betreuung</li>
          <li>Google &amp; Meta Ads inklusive</li>
        </ul>
        <p class="muted" style="font-size:0.85rem; margin-bottom:20px;">Für wen geeignet? Unternehmen, die Content, Ads und Website kombinieren möchten.</p>
        <a href="mailto:{EMAIL}" class="btn" style="text-align:center; justify-content:center;">Kostenloses Angebot</a>
      </div>
    </div>

    <div style="max-width:760px; margin-top:100px;">
      <h2>Häufig gestellte Fragen.</h2>
      <div style="margin-top:30px;">
        <div class="faq-item reveal">
          <button type="button" class="faq-q" aria-expanded="false"><span>Wie viel Zeitaufwand entsteht für mein Team und mich?</span><span class="plus" aria-hidden="true">+</span></button>
          <div class="faq-a"><p>{FAQ_ZEITAUFWAND_A}</p></div>
        </div>
        <div class="faq-item reveal">
          <button type="button" class="faq-q" aria-expanded="false"><span>Auf welchen Plattformen laufen Content und Ads?</span><span class="plus" aria-hidden="true">+</span></button>
          <div class="faq-a"><p>Primär Instagram Reels, TikTok und YouTube Shorts sowie Meta Ads und Google Ads. Die Strategie stimmen wir exakt auf Ihre Zielgruppe ab.</p></div>
        </div>
        <div class="faq-item reveal">
          <button type="button" class="faq-q" aria-expanded="false"><span>Wie schnell sind erste Ergebnisse sichtbar?</span><span class="plus" aria-hidden="true">+</span></button>
          <div class="faq-a"><p>Erste organische Reichweiten- und Engagement-Zuwächse zeigen sich meist innerhalb von 2–4 Wochen. Bezahlte Kampagnen liefern oft schon nach 7–14 Tagen qualifizierte Anfragen.</p></div>
        </div>
        <div class="faq-item reveal">
          <button type="button" class="faq-q" aria-expanded="false"><span>Gibt es lange Vertragslaufzeiten?</span><span class="plus" aria-hidden="true">+</span></button>
          <div class="faq-a"><p>Nein. Wir setzen auf partnerschaftliche Zusammenarbeit auf Augenhöhe mit flexiblen Monatsmodellen, die sich Ihrer Unternehmensphase anpassen.</p></div>
        </div>
        <div class="faq-item reveal">
          <button type="button" class="faq-q" aria-expanded="false"><span>Wie läuft die Zusammenarbeit konkret ab?</span><span class="plus" aria-hidden="true">+</span></button>
          <div class="faq-a"><p>Nach der kostenlosen Potenzialanalyse erstellen wir eine Content- und Ad-Strategie, drehen und schneiden vor Ort und übernehmen Posting sowie Reporting — Sie erhalten monatlich einen kurzen Überblick über alle Ergebnisse.</p></div>
        </div>
      </div>
    </div>
  </section>'''
    write_page(route, main)


# ---------------------------------------------------------------------------
# REFERENZEN
# ---------------------------------------------------------------------------
def page_referenzen():
    route = ROUTES_BY_SLUG["referenzen"]
    d = route["depth"]
    crumb = render_breadcrumb(route)
    logos = render_client_logos(d)
    main = f'''{crumb}
  <section class="page-hero">
    <div class="container">
      <div class="kicker">Referenzen</div>
      <h1 style="font-size:clamp(1.9rem,4vw,3rem);">Ergebnisse statt Eitelkeits-Metriken.</h1>
      <p class="prose muted" style="margin-top:18px;">Ausgewählte Projekte und Kampagnen, die zeigen, wie wir arbeiten.</p>
    </div>
  </section>

  <section class="container" style="padding-bottom:40px;">
    <div class="reveal">
      <p class="muted">Vertraut von</p>
      {logos}
    </div>
  </section>

  <section class="container" id="case-google-ads" style="padding-bottom:80px;">
    <div class="reveal" style="max-width:640px;">
      <h2>142 qualifizierte Anfragen für eine lokale Dienstleisterin.</h2>
      <p class="muted" style="margin-top:14px;">Google Search Ads + Meta Retargeting · Beispiel-Kampagne, Regensburg</p>
    </div>
    <div class="case-grid" style="margin-top:44px;">
      <div class="case-card reveal">{counter_span(142)}<div class="lbl">Anfragen</div></div>
      <div class="case-card reveal">{counter_span(1.48, decimals=1, prefix="€")}<div class="lbl">Kosten pro Klick</div></div>
      <div class="case-card reveal">{counter_span(8.4, decimals=1, suffix="%")}<div class="lbl">Conversion Rate</div></div>
      <div class="case-card reveal">{counter_span(17.6, decimals=1, prefix="€")}<div class="lbl">Cost per Lead</div></div>
    </div>
    <div class="case-study-grid reveal-stagger" style="margin-top:56px;">
      <div>
        <h4>Ausgangslage</h4>
        <p class="muted">Eine Kundin im Bereich dauerhafte Haarentfernung in Regensburg wollte planbar mehr qualifizierte Anfragen gewinnen, statt sich auf Zufallslaufkundschaft zu verlassen.</p>
      </div>
      <div>
        <h4>Strategie</h4>
        <p class="muted">Kombination aus Google Search Ads für aktive Suchanfragen und Meta-Retargeting, um Interessenten erneut gezielt anzusprechen.</p>
      </div>
      <div>
        <h4>Umsetzung</h4>
        <!-- TODO: weitere Umsetzungsdetails (Creatives, Zeitraum, Budget) ergänzen, sobald final freigegeben -->
        <p class="muted">Kampagnenstruktur, Zielgruppen, Landingpage und Tracking wurden aufgesetzt und laufend anhand der Ergebnisse optimiert.</p>
      </div>
      <div>
        <h4>Ergebnis</h4>
        <p class="muted">142 qualifizierte Neukundenanfragen bei 17,60&nbsp;€ Cost per Lead und einer Conversion-Rate von 8,4&nbsp;%.</p>
      </div>
    </div>
    {related_links(d, "Passende Leistung:", [("google-ads-agentur-konstanz", "Google & Meta Ads")])}
  </section>

  <section class="container" style="padding-bottom:80px;">
    <div class="reveal" style="max-width:640px; margin-bottom:8px;">
      <p class="muted" style="font-size:0.82rem; letter-spacing:0.1em; text-transform:uppercase;">Weitere Projekte</p>
      <h2 style="margin-top:14px;">Case Studies in Vorbereitung.</h2>
      <p class="muted" style="margin-top:14px;">Diese Projekte laufen bereits — die vollständigen Ergebnisse veröffentlichen wir hier, sobald sie final ausgewertet und freigegeben sind.</p>
    </div>
    <div class="upcoming-grid" style="margin-top:44px;">
      <div class="reveal case-upcoming" id="case-club-aktiv">
        <span class="badge-soft">Case Study folgt</span>
        <h3>Club Aktiv</h3>
        <p class="muted" style="margin-top:6px; font-size:0.82rem; letter-spacing:0.06em; text-transform:uppercase;">Social Media · organisches Instagram-Wachstum</p>
        <p class="muted" style="margin-top:14px;">Ein Fitnessstudio, für das wir organische Social-Media-Präsenz und Community-Aufbau umsetzen — von Content-Strategie bis Reels.</p>
        <div class="fields">
          Zeitraum · Ausgangslage · Content-Strategie · veröffentlichte Reels · Views · Reichweite · Followerentwicklung · Engagement · Top-Reels · Ergebnis
        </div>
        {related_links(d, "Passende Leistung:", [("social-media-agentur-konstanz", "Social Media")])}
      </div>
      <div class="reveal case-upcoming" id="case-polywerft">
        <span class="badge-soft">Case Study folgt</span>
        <h3>Polywerft Konstanz</h3>
        <p class="muted" style="margin-top:6px; font-size:0.82rem; letter-spacing:0.06em; text-transform:uppercase;">Social Recruiting</p>
        <p class="muted" style="margin-top:14px;">Eine Recruiting-Kampagne, mit der wir Mitarbeiter für Polywerft Konstanz gewinnen — mit authentischen Recruiting-Reels und gezielter Ansprache.</p>
        <div class="fields">
          Ausgangslage · gesuchte Position(en) · Recruiting-Strategie · Content / Recruiting-Reels · Kampagne · Bewerbungen · qualifizierte Bewerbungen · Einstellungen · Zeitraum · Ergebnis
        </div>
        {related_links(d, "Passende Leistung:", [("social-recruiting", "Social Recruiting")])}
      </div>
    </div>
    <!-- TODO: replace placeholder structure above with verified figures for Club Aktiv and
         Polywerft Konstanz once available; keep the "Case Study folgt" framing until then. -->
  </section>

  <section class="container" style="padding-bottom:100px;">
    <div class="reveal" style="max-width:640px; margin-bottom:36px;">
      <h2>Interaktive Webseiten-Vorschau</h2>
      <p class="muted" style="margin-top:16px;">Statt PDF-Konzepten liefern wir einen echten, klickbaren Live-Prototyp — direkt am Smartphone oder Desktop testbar, bevor überhaupt eine Entscheidung fällt.</p>
    </div>
    <div class="reveal proto-frame">
      <div class="proto-toggle">
        <button type="button" class="proto-btn active" data-view="desktop" aria-pressed="true">🖥 Desktop</button>
        <button type="button" class="proto-btn" data-view="mobile" aria-pressed="false">📱 Smartphone</button>
        <a href="https://zahnarzt.steinhauermedia.de" target="_blank" rel="noopener" class="link-underline proto-openlink">In neuem Tab öffnen</a>
      </div>
      <div class="proto-viewport view-desktop" id="proto-viewport">
        <iframe src="https://zahnarzt.steinhauermedia.de" title="Live-Prototyp Zahnarztpraxis" loading="lazy"></iframe>
      </div>
    </div>
  </section>

  {cta_block("Ihr Projekt könnte das nächste sein.", "Kostenlose Potenzialanalyse", "kontakt", d)}'''
    write_page(route, main)


# ---------------------------------------------------------------------------
# UEBER UNS
# ---------------------------------------------------------------------------
def page_ueber_uns():
    route = ROUTES_BY_SLUG["ueber-uns"]
    d = route["depth"]
    crumb = render_breadcrumb(route)
    related = related_links(d, "Sehen Sie sich außerdem an:", [("referenzen", "Referenzen"), ("kontakt", "Kontakt")])
    main = f'''{crumb}
  <section class="page-hero">
    <div class="container">
      <div class="kicker">Über uns</div>
      <h1 style="font-size:clamp(1.9rem,4vw,3rem);">Zwei Spezialisten. Ein Ansprechpartner für Ihre digitale Sichtbarkeit.</h1>
      <p class="prose muted" style="margin-top:18px;">Zwei Spezialisten, ein System: Content, der gesehen wird, und Performance, die sich rechnet.</p>
    </div>
  </section>

  <section class="container" style="padding-bottom:90px;">
    <div class="team-grid">
      <div class="team-card reveal">
        <img class="team-photo" src="{asset('assets/img/team-shawn.jpg', d)}" alt="Shawn, Social Media Spezialist bei Steinhauer Media" width="84" height="84">
        <h2 style="font-size:1.18rem;">Shawn</h2>
        <p class="gold" style="font-size:0.82rem; letter-spacing:0.06em; margin-top:4px;">Social Media &amp; organisches Wachstum</p>
        <p>Verantwortlich für:</p>
        <ul style="margin-top:10px;">
          <li>Social-Media-Strategie</li>
          <li>Content</li>
          <li>Drehs</li>
          <li>Reels</li>
          <li>organisches Wachstum</li>
        </ul>
      </div>
      <div class="team-card reveal">
        <img class="team-photo" src="{asset('assets/img/team-lennert.jpg', d)}" alt="Lennert, Spezialist für Websites und Performance Marketing bei Steinhauer Media" width="84" height="84">
        <h2 style="font-size:1.18rem;">Lennert</h2>
        <p class="gold" style="font-size:0.82rem; letter-spacing:0.06em; margin-top:4px;">Websites &amp; Performance Marketing</p>
        <p>Verantwortlich für:</p>
        <ul style="margin-top:10px;">
          <li>Webdesign</li>
          <li>SEO</li>
          <li>Google Ads</li>
          <li>Meta Ads</li>
          <li>Tracking</li>
        </ul>
      </div>
    </div>
  </section>

  <section class="container" style="padding-bottom:90px;">
    <div class="reveal img-reveal team-group-frame">
      <img src="{asset('assets/img/team-group.jpg', d)}" alt="Shawn und Lennert, die Gründer von Steinhauer Media" width="900" height="600" loading="lazy">
    </div>
  </section>

  <section class="block deep">
    <div class="container">
      <div class="reveal" style="max-width:640px;">
        <h2>Warum wir schneller liefern als klassische Agenturen.</h2>
      </div>
      <div class="principles-grid">
        <div class="principle reveal">
          <div class="n" aria-hidden="true">01</div>
          <h3>Digital Natives statt Meeting-Schleifen</h3>
          <p>Wir reden nicht monatelang über Trends — wir setzen sie direkt um und verstehen Plattform-Algorithmen nativ.</p>
        </div>
        <div class="principle reveal">
          <div class="n" aria-hidden="true">02</div>
          <h3>End-to-End Produktion</h3>
          <p>Vom ersten Skript über den Dreh vor Ort bis zum fertigen Schnitt — für Sie entsteht kein eigener Aufwand.</p>
        </div>
        <div class="principle reveal">
          <div class="n" aria-hidden="true">03</div>
          <h3>Fokus auf messbaren Ertrag</h3>
          <p>Keine Vanity-Metriken. Bei uns zählen qualifizierte Leads und nachvollziehbare Sichtbarkeit bei Google.</p>
        </div>
      </div>
      {related}
    </div>
  </section>

  {cta_block("Lernen Sie uns persönlich kennen.", "Kostenlose Potenzialanalyse", "kontakt", d)}'''
    write_page(route, main)

# ---------------------------------------------------------------------------
# KONTAKT
# ---------------------------------------------------------------------------
def page_kontakt():
    route = ROUTES_BY_SLUG["kontakt"]
    d = route["depth"]
    crumb = render_breadcrumb(route)
    phone_cards = "\n        ".join(
        f'<div class="card"><div class="k">{p["label"]}</div><div class="v"><a href="tel:{p["href"]}" class="link-underline">{p["value"]}</a> · <a href="https://wa.me/{p["href"].lstrip("+")}" target="_blank" rel="noopener" class="link-underline">WhatsApp</a></div></div>'
        for p in PHONES
    )
    main = f'''{crumb}
  <section class="page-hero">
    <div class="container">
      <div class="kicker">Kontakt</div>
      <h1 style="font-size:clamp(1.9rem,4vw,3rem);">Lassen Sie uns über Ihr Wachstum sprechen.</h1>
      <p class="prose muted" style="margin-top:18px;">Schreiben Sie uns unkompliziert eine Nachricht oder greifen Sie direkt zum Hörer.</p>
    </div>
  </section>

  <section class="container" style="padding-bottom:110px;">
    <div class="contact-grid">
      <form id="contact-form" class="reveal" aria-label="Kontaktformular">
        <div class="form-row"><label for="c-name">Name*</label><input id="c-name" name="name" type="text" required autocomplete="name"></div>
        <div class="form-row"><label for="c-company">Unternehmen</label><input id="c-company" name="company" type="text" autocomplete="organization"></div>
        <div class="form-row"><label for="c-mail">E-Mail*</label><input id="c-mail" name="email" type="email" required autocomplete="email"></div>
        <div class="form-row"><label for="c-phone">Telefon</label><input id="c-phone" name="phone" type="tel" autocomplete="tel"></div>
        <div class="form-row">
          <label for="c-topic">Wobei können wir helfen?*</label>
          <select id="c-topic" name="topic" required>
            <option value="">Bitte auswählen</option>
            <option value="Social Media">Social Media</option>
            <option value="Google / Meta Ads">Google / Meta Ads</option>
            <option value="SEO">SEO</option>
            <option value="Website">Website</option>
            <option value="Recruiting">Recruiting</option>
            <option value="Noch unsicher">Noch unsicher</option>
          </select>
        </div>
        <div class="form-row"><label for="c-message">Erzählen Sie uns kurz, worum es geht.*</label><textarea id="c-message" name="message" rows="5" required></textarea></div>
        <span class="magnetic-wrap" data-magnetic><button type="submit" class="btn primary">Kostenlose Potenzialanalyse anfragen</button></span>
      </form>
      <div class="contact-side reveal">
        <div class="card"><div class="k">E-Mail</div><div class="v"><a href="mailto:{EMAIL}" class="link-underline">{EMAIL}</a></div></div>
        {phone_cards}
        <div class="card"><div class="k">Adresse</div><div class="v">{ADDRESS_LINE}</div></div>
      </div>
    </div>
  </section>'''
    write_page(route, main)


# ---------------------------------------------------------------------------
# IMPRESSUM
# ---------------------------------------------------------------------------
def page_impressum():
    route = ROUTES_BY_SLUG["impressum"]
    d = route["depth"]
    crumb = render_breadcrumb(route)
    legal_name = CO.get("legalName") or "[Vertretungsberechtigte Person / Rechtsform – bitte ergänzen]"
    main = f'''{crumb}
  <section class="page-hero">
    <div class="container">
      <div class="kicker">Rechtliches</div>
      <h1 style="font-size:clamp(1.9rem,4vw,3rem);">Impressum</h1>
    </div>
  </section>

  <section class="container" style="padding-bottom:100px;">
    <div class="reveal prose">
      <h2 style="font-size:1.18rem;">Angaben gemäß § 5 TMG</h2>
      <p class="muted" style="margin-top:14px;">
        {legal_name}<br>
        {ADDRESS_LINE}<br>
        Deutschland
      </p>

      <h2 style="font-size:1.18rem; margin-top:40px;">Kontakt</h2>
      <p class="muted" style="margin-top:14px;">
        E-Mail: <a href="mailto:{EMAIL}" class="link-underline">{EMAIL}</a><br>
        Telefon: {PHONES[0]["value"]}
      </p>

      <h2 style="font-size:1.18rem; margin-top:40px;">Umsatzsteuer-ID</h2>
      <p class="muted" style="margin-top:14px;">[Umsatzsteuer-Identifikationsnummer gemäß § 27a UStG – bitte ergänzen, falls vorhanden]</p>

      <h2 style="font-size:1.18rem; margin-top:40px;">Verantwortlich für den Inhalt nach § 18 Abs. 2 MStV</h2>
      <p class="muted" style="margin-top:14px;">{legal_name}<br>{ADDRESS_LINE}</p>

      <h2 style="font-size:1.18rem; margin-top:40px;">Streitschlichtung</h2>
      <p class="muted" style="margin-top:14px;">Die Europäische Kommission stellt eine Plattform zur Online-Streitbeilegung (OS) bereit: <a href="https://ec.europa.eu/consumers/odr/" target="_blank" rel="noopener" class="link-underline">https://ec.europa.eu/consumers/odr/</a>. Wir sind nicht verpflichtet und nicht bereit, an Streitbeilegungsverfahren vor einer Verbraucherschlichtungsstelle teilzunehmen.</p>
    </div>
  </section>'''
    write_page(route, main)


# ---------------------------------------------------------------------------
# DATENSCHUTZ
# ---------------------------------------------------------------------------
def page_datenschutz():
    route = ROUTES_BY_SLUG["datenschutz"]
    d = route["depth"]
    crumb = render_breadcrumb(route)
    legal_name = CO.get("legalName") or "[Vertretungsberechtigte Person / Rechtsform – bitte ergänzen]"
    main = f'''{crumb}
  <section class="page-hero">
    <div class="container">
      <div class="kicker">Rechtliches</div>
      <h1 style="font-size:clamp(1.9rem,4vw,3rem);">Datenschutzerklärung</h1>
    </div>
  </section>

  <section class="container" style="padding-bottom:100px;">
    <div class="reveal prose">
      <h2 style="font-size:1.18rem;">Verantwortlicher</h2>
      <p class="muted" style="margin-top:14px;">
        {legal_name}<br>
        {ADDRESS_LINE}<br>
        E-Mail: <a href="mailto:{EMAIL}" class="link-underline">{EMAIL}</a>
      </p>

      <h2 style="font-size:1.18rem; margin-top:40px;">Kontaktformular</h2>
      <p class="muted" style="margin-top:14px;">Das Kontaktformular auf dieser Website öffnet beim Absenden Ihr lokales E-Mail-Programm mit einer vorausgefüllten Nachricht an {EMAIL} (mailto-Link). Ihre Eingaben werden dabei nicht an einen Server dieser Website übertragen oder dort gespeichert; die Übermittlung erfolgt ausschließlich über Ihr E-Mail-Programm, sobald Sie die E-Mail selbst versenden.</p>

      <h2 style="font-size:1.18rem; margin-top:40px;">Eingebundene Inhalte Dritter</h2>
      <p class="muted" style="margin-top:14px;">Auf der Seite „Referenzen" binden wir einen interaktiven Live-Prototyp per iframe von einer eigenen Subdomain (steinhauermedia.de) ein. Beim Laden dieser Seite kann eine Verbindung zu diesem Server aufgebaut werden. Zudem verlinken wir auf unser Instagram-Profil; beim Anklicken dieses externen Links gelten die Datenschutzbestimmungen von Meta/Instagram.</p>

      <h2 style="font-size:1.18rem; margin-top:40px;">Cookies &amp; Analyse-Tools</h2>
      <p class="muted" style="margin-top:14px;">Diese Website setzt aktuell keine Cookies und verwendet keine Analyse- oder Tracking-Tools.</p>

      <h2 style="font-size:1.18rem; margin-top:40px;">Ihre Rechte</h2>
      <p class="muted" style="margin-top:14px;">Sie haben jederzeit das Recht auf Auskunft, Berichtigung, Löschung oder Einschränkung der Verarbeitung Ihrer bei uns gespeicherten personenbezogenen Daten sowie ein Beschwerderecht bei einer Datenschutz-Aufsichtsbehörde. Wenden Sie sich hierzu an {EMAIL}.</p>
    </div>
  </section>'''
    write_page(route, main)


# ---------------------------------------------------------------------------
# 404
# ---------------------------------------------------------------------------
def page_404():
    route = {"slug": "404", "depth": 0, "nav": None,
             "title": "Seite nicht gefunden | Steinhauer Media",
             "description": "Diese Seite konnte nicht gefunden werden.",
             "crumbs": []}
    d = route["depth"]
    main = f'''<section class="page-hero" style="text-align:center;">
    <div class="container">
      <div class="kicker">404</div>
      <h1 style="font-size:clamp(1.9rem,4vw,3rem);">Diese Seite gibt es leider nicht.</h1>
      <p class="prose muted" style="margin:18px auto 0;">Der aufgerufene Link ist veraltet oder fehlerhaft. Nutzen Sie einen der folgenden Wege weiter.</p>
      <div class="error-actions" style="justify-content:center;">
        <a href="{href_to('', d)}" class="btn primary">Zur Startseite</a>
        <a href="{href_to('kontakt', d)}" class="btn">Kontakt</a>
      </div>
    </div>
  </section>'''
    extra_head = '<meta name="robots" content="noindex,follow">'
    js = asset("assets/js/site.js", d)
    head = render_head(route, extra_head)
    nav = render_nav(route)
    footer = render_footer(d)
    html = f'''<!DOCTYPE html>
<html lang="de">
<head>
{head}
</head>
<body>
<div class="grain-overlay"></div>
{nav}
<main id="main">
{main}
</main>
{footer}
<script src="{js}" defer></script>
</body>
</html>
'''
    with open(os.path.join(ROOT, "404.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote 404.html")

# ---------------------------------------------------------------------------
# sitemap.xml / robots.txt
# ---------------------------------------------------------------------------
def write_sitemap():
    urls = "\n".join(
        f'  <url><loc>{site_url(slug)}</loc></url>' for slug in SITEMAP_SLUGS
    )
    xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{urls}
</urlset>
'''
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(xml)
    print("wrote sitemap.xml")


def write_robots():
    txt = f'''User-agent: *
Allow: /

Sitemap: {site_url()}sitemap.xml
'''
    with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(txt)
    print("wrote robots.txt")


def write_nojekyll():
    open(os.path.join(ROOT, ".nojekyll"), "w").close()
    print("wrote .nojekyll")


def main():
    page_home()
    page_leistungen()
    page_social_media()
    page_google_ads()
    page_seo()
    page_webdesign()
    page_social_recruiting()
    page_pakete()
    page_referenzen()
    page_ueber_uns()
    page_kontakt()
    page_impressum()
    page_datenschutz()
    page_404()
    write_sitemap()
    write_robots()
    write_nojekyll()


if __name__ == "__main__":
    main()
