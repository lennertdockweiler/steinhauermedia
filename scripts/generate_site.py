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
    ("google-ads-agentur-konstanz", "Google Ads"),
    ("seo-agentur-konstanz", "SEO & GEO"),
    ("webdesign-konstanz", "Webdesign"),
    ("social-recruiting", "Social Recruiting"),
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
        ("\n          <div class=\"divider\" role=\"separator\"></div>" if s == "social-recruiting" else "")
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
      <div class="hero-placeholder"><span>PLATZHALTER<br>Foto / Video<br>folgt</span></div>
    </div>
    <div class="container hero-inner">
      <div class="hero-kicker">
        <svg class="em" viewBox="0 0 40 40" fill="none" aria-hidden="true"><path d="M20 6L35 17H5L20 6Z" stroke="#1E1B15" stroke-width="1.4"/></svg>
        <span>Social Media &amp; Performance Marketing · Konstanz</span>
      </div>
      <h1 id="hero-headline">Digitale Sichtbarkeit, die planbar Neukunden bringt.</h1>
      <p class="lead">Ein Partner für Social-Media-Performance-Content, SEO/GEO und Werbeanzeigen — aus einer Hand, mit Sitz am Bodensee.</p>
      <div class="hero-actions">
        <span class="magnetic-wrap" data-magnetic><a href="{href_to('kontakt', d)}" class="btn primary">Kostenlose Potenzialanalyse</a></span>
        <a href="{href_to('leistungen', d)}" class="link-underline" style="color:var(--ink-soft);">Leistungen ansehen</a>
      </div>
    </div>
    <div class="hero-scroll"><div class="line"></div><span>Scrollen</span></div>
  </section>

  <section class="block tight">
    <div class="container">
      <div class="stats-grid stats-grid-5 reveal-stagger">
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
        <h2>Warum die meisten Unternehmen online unsichtbar bleiben.</h2>
        <p class="prose muted" style="margin-top:18px;">Viele posten regelmäßig, verbrennen Budget für planlose Werbeanzeigen und erzielen trotzdem keine neuen Kundenanfragen. Wir schließen die Lücke zwischen kreativem Content und handfesten Verkaufszahlen.</p>
      </div>
      <div class="split-cols">
        <div class="reveal">
          <h3>Das Problem</h3>
          <ul>
            <li><span class="mark" aria-hidden="true">–</span>Zeitraubendes Posten ohne klare Strategie</li>
            <li><span class="mark" aria-hidden="true">–</span>Teure Ads ohne messbaren ROI</li>
            <li><span class="mark" aria-hidden="true">–</span>Unsichtbarkeit bei regionalen Google-Suchen</li>
          </ul>
        </div>
        <div class="reveal">
          <h3>Unsere Lösung</h3>
          <ul>
            <li><span class="mark" aria-hidden="true">+</span>Virale Kurzvideos mit Verkaufspsychologie</li>
            <li><span class="mark" aria-hidden="true">+</span>Präzise Google- &amp; Social-Ads für echte Leads</li>
            <li><span class="mark" aria-hidden="true">+</span>Lokale Dominanz durch SEO- &amp; GEO-Optimierung</li>
          </ul>
        </div>
      </div>
    </div>
  </section>

  <section class="block">
    <div class="container">
      <div class="reveal">
        <h2>Drei Leistungen, ein System.</h2>
        <p class="prose muted" style="margin-top:16px;">Content, Sichtbarkeit und Werbung greifen bei uns ineinander — statt als lose Einzelmaßnahmen nebeneinander zu laufen.</p>
      </div>
      <div class="service-grid">
        <a href="{href_to('social-media-agentur-konstanz', d)}" class="service-card" data-tilt>
          {ICON_SHORTFORM}
          <span class="tag">01 — Content</span>
          <h3>Short-Form Video</h3>
          <p>Organische Reels &amp; TikToks mit Verkaufspsychologie, die im Algorithmus wirklich funktionieren.</p>
        </a>
        <a href="{href_to('seo-agentur-konstanz', d)}" class="service-card" data-tilt>
          {ICON_SEO}
          <span class="tag">02 — Sichtbarkeit</span>
          <h3>SEO &amp; GEO</h3>
          <p>Regionale Google-Dominanz, damit man Sie findet, bevor der Wettbewerb überhaupt in Sicht ist.</p>
        </a>
        <a href="{href_to('google-ads-agentur-konstanz', d)}" class="service-card" data-tilt>
          {ICON_ADS}
          <span class="tag">03 — Wachstum</span>
          <h3>Google &amp; Meta Ads</h3>
          <p>Zielgerichtete Kampagnen, die kaufbereite Leads und Bewerber zuverlässig liefern.</p>
        </a>
      </div>
      <div style="margin-top:34px;"><a href="{href_to('leistungen', d)}" class="link-underline">Alle Leistungen im Detail</a></div>
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

  <section class="block">
    <div class="container">
      <div class="reveal">
        <p class="muted" style="margin-bottom:8px;">Vertraut von wachsenden Unternehmen</p>
        {logos}
      </div>
      <div class="project-row">
        <div class="reveal">
          <div class="scale-panel" data-scale><span>Beispiel-Kampagne · Regensburg</span></div>
        </div>
        <div class="reveal">
          <h2>142 Anfragen bei 17,60&nbsp;€ pro Lead.</h2>
          <p class="muted" style="margin-top:16px;">Für eine Kundin im Bereich dauerhafte Haarentfernung erzielten wir über Google Search Ads und Meta-Retargeting 142 qualifizierte Neukundenanfragen bei einer Conversion-Rate von 8,4&nbsp;%.</p>
          <div style="margin-top:26px;"><a href="{href_to('referenzen', d)}" class="link-underline">Alle Projekte ansehen</a></div>
        </div>
      </div>
    </div>
  </section>

  <section class="block deep">
    <div class="container">
      <div class="reveal">
        <h2>Individuelle Pakete für planbare Ergebnisse.</h2>
        <p class="prose muted" style="margin-top:16px;">Drei Modelle, ein gemeinsames Ziel: mehr Sichtbarkeit, die sich in echten Anfragen niederschlägt.</p>
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
        </div>
        <div class="pricing-card reveal">
          <h3>Vollgas</h3>
          <p class="muted" style="margin-top:8px; font-size:0.9rem;">Maßgeschneidert, alle Kanäle</p>
          <ul>
            <li>Bis zu 15 Videos / Monat</li>
            <li>Instagram, Facebook &amp; TikTok</li>
            <li>SEO, GEO &amp; Website</li>
          </ul>
        </div>
      </div>
      <div style="margin-top:34px;"><a href="{href_to('pakete', d)}" class="link-underline">Alle Pakete im Vergleich</a></div>
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
          <div class="faq-a"><p>Minimal. Wir übernehmen Konzeption, Skripte, Vor-Ort-Dreh und den kompletten Schnitt. Für Sie fallen in der Regel nur 1–2 Stunden pro Monat für Freigaben an.</p></div>
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
        <h2>Lassen Sie uns über Ihr Wachstum sprechen.</h2>
        <p>Sichern Sie sich eine unverbindliche Potenzialanalyse — wir zeigen konkret, wie Sie mit Short-Form Video und Performance Ads planbar neue Kunden gewinnen.</p>
        <div class="btn-zone">
          <span class="magnetic-wrap" data-magnetic><a href="{href_to('kontakt', d)}" class="btn on-dark primary" style="background:var(--gold-bright); color:var(--dark); border-color:var(--gold-bright);">Potenzialanalyse anfragen</a></span>
        </div>
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
        ("social-media-agentur-konstanz", ICON_SHORTFORM, "01", "Short-Form Video", "Organische Reels &amp; TikToks in drei aufeinander abgestimmten Formaten für maximale Reichweite, Vertrauen und Kundenbindung."),
        ("seo-agentur-konstanz", ICON_SEO, "02", "SEO &amp; GEO", "Regionale Google-Dominanz statt Unsichtbarkeit bei lokalen Suchanfragen."),
        ("google-ads-agentur-konstanz", ICON_ADS, "03", "Google &amp; Meta Ads", "Ganzheitliches Kampagnen-Management für kaufbereite Neukunden und qualifizierte Fachkräfte."),
        ("social-recruiting", ICON_RECRUITING, "04", "Social Recruiting", "Authentische Recruiting-Reels gegen den Fachkräftemangel."),
        ("webdesign-konstanz", ICON_WEBDESIGN, "05", "Webdesign &amp; Prototyping", "Schnelle, moderne Websites — vorab live und interaktiv zum Testen."),
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
def service_page(slug, kicker_num, icon_lg, heading, lead, bullets, related_intro, related_targets):
    route = ROUTES_BY_SLUG[slug]
    d = route["depth"]
    crumb = render_breadcrumb(route)
    lis = "\n          ".join(f'<li>{b}</li>' for b in bullets)
    related = related_links(d, related_intro, related_targets)
    main = f'''{crumb}
  <section class="page-hero">
    <div class="container">
      <div class="kicker">Leistungen · {kicker_num}</div>
      <h1 style="font-size:clamp(1.9rem,4vw,3rem);">{heading}</h1>
      <p class="prose muted" style="margin-top:18px;">{lead}</p>
    </div>
  </section>

  <section class="container" style="padding-bottom:70px;">
    <div class="service-detail reveal">
      <div>
        {icon_lg}
      </div>
      <div>
        <ul>
          {lis}
        </ul>
        {related}
      </div>
    </div>
  </section>

  {cta_block("Bereit für den ersten Schritt?", "Kostenlose Potenzialanalyse", "kontakt", d)}'''
    write_page(route, main)


def page_social_media():
    d = ROUTES_BY_SLUG["social-media-agentur-konstanz"]["depth"]
    service_page(
        "social-media-agentur-konstanz", "01", ICON_SHORTFORM_LG,
        "Short-Form Video Content",
        "Organische Reels &amp; TikToks in drei aufeinander abgestimmten Formaten für maximale Reichweite, Vertrauen und Kundenbindung.",
        [
            "Humorvolle Alltags-Hooks für virale Reichweite",
            "Experten-Talking-Heads für Vertrauensaufbau",
            "Informative Karussell-Posts zum Merken &amp; Teilen",
            "Skript, Dreh vor Ort, Schnitt, Posting &amp; Community Management",
        ],
        "Passt gut dazu:",
        [("google-ads-agentur-konstanz", "Google & Meta Ads"), ("referenzen", "Referenzen"), ("kontakt", "Kontakt")],
    )


def page_google_ads():
    service_page(
        "google-ads-agentur-konstanz", "03", ICON_ADS_LG,
        "Google &amp; Meta Ads",
        "Ganzheitliches Kampagnen-Management für kaufbereite Neukunden und qualifizierte Fachkräfte.",
        [
            "High-Intent Search Ads für aktive Suchanfragen",
            "Meta-Retargeting mit Video-Creatives",
            "Laufende Optimierung von Keywords &amp; Geboten",
        ],
        "Passt gut dazu:",
        [("referenzen", "Case Study ansehen"), ("kontakt", "Kontakt")],
    )


def page_seo():
    service_page(
        "seo-agentur-konstanz", "02", ICON_SEO_LG,
        "SEO &amp; GEO",
        "Regionale Google-Dominanz statt Unsichtbarkeit bei lokalen Suchanfragen.",
        [
            "Website- &amp; Content-SEO für nachhaltiges Ranking",
            "Generative Engine Optimization für KI-Suchergebnisse",
            "Google-Unternehmensprofil auf Bestleistung optimiert",
        ],
        "Passt gut dazu:",
        [("webdesign-konstanz", "Webdesign"), ("kontakt", "Kontakt")],
    )


def page_webdesign():
    service_page(
        "webdesign-konstanz", "05", ICON_WEBDESIGN_LG,
        "Webdesign &amp; Prototyping",
        "Schnelle, moderne Websites — vorab live und interaktiv zum Testen.",
        [
            "Blitzschnelle, mobiloptimierte Umsetzung",
            "Interaktive Live-Vorschau vor Beauftragung",
            "Direkt verzahnt mit SEO &amp; GEO",
        ],
        "Passt gut dazu:",
        [("seo-agentur-konstanz", "SEO & GEO"), ("referenzen", "Referenzen"), ("kontakt", "Kontakt")],
    )


def page_social_recruiting():
    service_page(
        "social-recruiting", "04", ICON_RECRUITING_LG,
        "Social Recruiting",
        "Authentische Recruiting-Reels gegen den Fachkräftemangel.",
        [
            "„Ein Tag als …“ — Einblicke in Team &amp; Arbeitsalltag",
            "Klare Ansprache von Benefits &amp; Gehalt",
            "60-Sekunden Express-Bewerbung ohne Lebenslauf",
        ],
        "Passt gut dazu:",
        [("social-media-agentur-konstanz", "Short-Form Video"), ("kontakt", "Kontakt")],
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
        <a href="mailto:{EMAIL}" class="btn" style="text-align:center; justify-content:center;">Kostenloses Angebot</a>
      </div>
    </div>

    <div style="max-width:760px; margin-top:100px;">
      <h2>Häufig gestellte Fragen.</h2>
      <div style="margin-top:30px;">
        <div class="faq-item reveal">
          <button type="button" class="faq-q" aria-expanded="false"><span>Wie viel Zeitaufwand entsteht für mein Team und mich?</span><span class="plus" aria-hidden="true">+</span></button>
          <div class="faq-a"><p>Minimal. Wir übernehmen Konzeption, Skripte, Vor-Ort-Dreh und den kompletten Schnitt. Für Sie fallen in der Regel nur 1–2 Stunden pro Monat für Freigaben und kurze Abstimmungen an.</p></div>
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

  <section class="container" style="padding-bottom:80px;">
    <div class="reveal" style="max-width:640px;">
      <h2>Beispiel-Kampagne: Regensburg</h2>
      <p class="muted" style="margin-top:14px;">Für eine Kundin im Bereich dauerhafte Haarentfernung kombinierten wir Google Search Ads mit Meta-Retargeting.</p>
    </div>
    <div class="case-grid" style="margin-top:44px;">
      <div class="case-card reveal">{counter_span(142)}<div class="lbl">Generierte Anfragen</div></div>
      <div class="case-card reveal">{counter_span(1.48, decimals=1, prefix="€")}<div class="lbl">Kosten pro Klick</div></div>
      <div class="case-card reveal">{counter_span(8.4, decimals=1, suffix="%")}<div class="lbl">Conversion-Rate</div></div>
      <div class="case-card reveal">{counter_span(17.6, decimals=1, prefix="€")}<div class="lbl">Kosten pro Lead</div></div>
    </div>
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

  {cta_block("Ihr Projekt könnte das nächste sein.", "Jetzt Kontakt aufnehmen", "kontakt", d)}'''
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
      <h1 style="font-size:clamp(1.9rem,4vw,3rem);">Gemeinsam sind wir Steinhauer Media.</h1>
      <p class="prose muted" style="margin-top:18px;">Zwei Spezialisten, ein System: Content, der gesehen wird, und Performance, die sich rechnet.</p>
    </div>
  </section>

  <section class="container" style="padding-bottom:90px;">
    <div class="team-grid">
      <div class="team-card reveal">
        <img class="team-photo" src="{asset('assets/img/team-shawn.jpg', d)}" alt="Shawn, Instagram-Experte bei Steinhauer Media" width="84" height="84">
        <h2 style="font-size:1.18rem;">Shawn</h2>
        <p class="gold" style="font-size:0.82rem; letter-spacing:0.06em; margin-top:4px;">Instagram &amp; organisches Wachstum</p>
        <p>Shawn ist unser Instagram-Experte mit jahrelanger Erfahrung im organischen Wachstum durch Reels. Er entwickelt Reel-Strategien, die messbar Reichweite, Sichtbarkeit und Ergebnisse bringen.</p>
      </div>
      <div class="team-card reveal">
        <img class="team-photo" src="{asset('assets/img/team-lennert.jpg', d)}" alt="Lennert, Experte für Websites, SEO und bezahlte Werbung bei Steinhauer Media" width="84" height="84">
        <h2 style="font-size:1.18rem;">Lennert</h2>
        <p class="gold" style="font-size:0.82rem; letter-spacing:0.06em; margin-top:4px;">Websites, SEO &amp; bezahlte Werbung</p>
        <p>Lennert ist unser Profi für Websites, SEO und bezahlte Werbung. Mit fundiertem Know-how in Suchmaschinenoptimierung und Performance-Marketing macht er aus jeder Website eine Wachstumsmaschine.</p>
      </div>
    </div>
  </section>

  <section class="container" style="padding-bottom:90px;">
    <div class="reveal" style="max-width:760px; border:1px solid var(--line); padding:8px; border-radius:var(--radius);">
      <img src="{asset('assets/img/team-group.jpg', d)}" alt="Shawn und Lennert, die Gründer von Steinhauer Media" style="width:100%; border-radius:2px;" width="900" height="600">
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
          <p>Keine Vanity-Metriken. Bei uns zählen qualifizierte Leads und eine dominierende regionale Google-Präsenz.</p>
        </div>
      </div>
      {related}
    </div>
  </section>

  {cta_block("Lernen Sie uns persönlich kennen.", "Termin vereinbaren", "kontakt", d)}'''
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
        <div class="form-row"><label for="c-name">Name</label><input id="c-name" name="name" type="text" required autocomplete="name"></div>
        <div class="form-row"><label for="c-mail">E-Mail</label><input id="c-mail" name="email" type="email" required autocomplete="email"></div>
        <div class="form-row"><label for="c-subject">Betreff</label><input id="c-subject" name="subject" type="text"></div>
        <div class="form-row"><label for="c-message">Ihre Nachricht</label><textarea id="c-message" name="message" rows="5" required></textarea></div>
        <span class="magnetic-wrap" data-magnetic><button type="submit" class="btn primary">Nachricht senden</button></span>
      </form>
      <div class="contact-side reveal">
        <div class="card"><div class="k">Adresse</div><div class="v">{ADDRESS_LINE}</div></div>
        <div class="card"><div class="k">E-Mail</div><div class="v"><a href="mailto:{EMAIL}" class="link-underline">{EMAIL}</a></div></div>
        {phone_cards}
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
