// Central content source for the whole site. Mirrors the real business
// facts previously held in site.config.json / scripts/generate_site.py —
// no numbers here are invented, only re-organized for the new layout.

export const company = {
  name: "Steinhauer Media",
  legalName: null as string | null,
  founders: ["Shawn", "Lennert"],
  address: {
    street: "Von-Emmich-Str. 6b",
    postalCode: "78467",
    city: "Konstanz",
    country: "DE",
  },
  addressLine: "Von-Emmich-Str. 6b, 78467 Konstanz",
  email: "info@steinhauermedia.de",
  phones: [
    { label: "Lennert", value: "+49 152 23657154", href: "+4915223657154" },
    { label: "Shawn", value: "+49 151 56002155", href: "+4915156002155" },
  ],
  instagram: "https://www.instagram.com/steinhauer.media",
  locale: "de_DE",
  language: "de",
};

export type ServiceSlug =
  | "social-media-agentur-konstanz"
  | "social-recruiting"
  | "webdesign-konstanz"
  | "seo-agentur-konstanz"
  | "google-ads-agentur-konstanz";

export interface Service {
  slug: ServiceSlug;
  num: string;
  icon: "shortform" | "recruiting" | "webdesign" | "seo" | "ads";
  name: string;
  shortDesc: string;
  heading: string;
  lead: string;
  bullets: string[];
  workflow?: string[];
  note?: string;
  ctaText: string;
  related: { slug: string; label: string }[];
}

export const services: Service[] = [
  {
    slug: "social-media-agentur-konstanz",
    num: "01",
    icon: "shortform",
    name: "Social Media & Video",
    shortDesc: "Strategie, Skripte, Drehs und Short-Form Content für Unternehmen.",
    heading: "Social Media für Unternehmen in Konstanz & am Bodensee.",
    lead: "Strategie, Ideen, Skripte, Drehs und Short-Form Content — von der ersten Idee bis zum veröffentlichten Reel.",
    bullets: [
      "Strategie & Content-Planung",
      "Ideen & Skripte",
      "Drehs vor Ort",
      "Schnitt",
      "Reels & Instagram-Betreuung",
      "TikTok",
      "Posting",
      "Reporting",
    ],
    workflow: ["Strategie", "Skript", "Dreh", "Schnitt", "Veröffentlichung", "Analyse"],
    ctaText: "Social-Media-Potenzial besprechen",
    related: [
      { slug: "google-ads-agentur-konstanz", label: "Google & Meta Ads" },
      { slug: "referenzen", label: "Referenzen" },
      { slug: "kontakt", label: "Kontakt" },
    ],
  },
  {
    slug: "social-recruiting",
    num: "02",
    icon: "recruiting",
    name: "Social Recruiting",
    shortDesc: "Mitarbeiter dort erreichen, wo sie jeden Tag unterwegs sind.",
    heading: "Mitarbeiter dort erreichen, wo sie jeden Tag unterwegs sind.",
    lead: "Authentische Recruiting-Reels und gezielte Meta-Kampagnen für Unternehmen, die neue Mitarbeitende suchen.",
    bullets: [
      "Recruiting Reels",
      "Arbeitgeberpositionierung",
      "Mitarbeiterinterviews",
      "Arbeitsalltag",
      "Meta-Kampagnen",
      "Bewerbungsfunnels",
    ],
    note: "Wir garantieren keine bestimmte Bewerberzahl, sondern qualifizierte Sichtbarkeit bei potenziellen Mitarbeitenden.",
    ctaText: "Recruiting-Potenzial besprechen",
    related: [
      { slug: "social-media-agentur-konstanz", label: "Social Media" },
      { slug: "kontakt", label: "Kontakt" },
    ],
  },
  {
    slug: "webdesign-konstanz",
    num: "03",
    icon: "webdesign",
    name: "Webdesign",
    shortDesc: "Schnelle, moderne Websites — vorab live und interaktiv zum Testen.",
    heading: "Websites, die gut aussehen und aus Besuchern Anfragen machen.",
    lead: "Schnelle, moderne Websites — vorab live und interaktiv zum Testen, bevor Sie uns beauftragen.",
    bullets: [
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
    ctaText: "Website-Prototyp anfragen",
    related: [
      { slug: "seo-agentur-konstanz", label: "SEO & GEO" },
      { slug: "referenzen", label: "Referenzen" },
      { slug: "kontakt", label: "Kontakt" },
    ],
  },
  {
    slug: "seo-agentur-konstanz",
    num: "04",
    icon: "seo",
    name: "SEO & GEO",
    shortDesc: "Local SEO, technische SEO und GEO für nachhaltige Sichtbarkeit.",
    heading: "Bei Google gefunden werden, wenn Kunden nach Ihrer Leistung suchen.",
    lead: "Local SEO, technische SEO und GEO, damit Unternehmen dort gefunden werden, wo potenzielle Kunden tatsächlich suchen.",
    bullets: [
      "Local SEO",
      "Technische SEO",
      "On-Page SEO",
      "Content",
      "Google Unternehmensprofil",
      "Lokale Suchanfragen",
      "Strukturierte Daten",
      "GEO / KI-Sichtbarkeit",
    ],
    note: "Wir versprechen keine bestimmten Rankings, sondern arbeiten kontinuierlich und nachvollziehbar an nachhaltiger Sichtbarkeit.",
    ctaText: "SEO-Potenzial prüfen",
    related: [
      { slug: "webdesign-konstanz", label: "Webdesign" },
      { slug: "kontakt", label: "Kontakt" },
    ],
  },
  {
    slug: "google-ads-agentur-konstanz",
    num: "05",
    icon: "ads",
    name: "Google & Meta Ads",
    shortDesc: "Werbekampagnen, Tracking und Landingpages für qualifizierte Anfragen.",
    heading: "Google Ads für Unternehmen in Konstanz und am Bodensee.",
    lead: "Werbekampagnen, Tracking und Landingpages für qualifizierte Kundenanfragen — Meta Ads ergänzen die Strategie dort, wo es sinnvoll ist.",
    bullets: [
      "Search Ads",
      "Keyword-Recherche",
      "Tracking",
      "Landingpages",
      "Kampagnenoptimierung",
      "Retargeting",
      "Reporting",
    ],
    ctaText: "Ads-Potenzial besprechen",
    related: [
      { slug: "referenzen", label: "Case Study ansehen" },
      { slug: "kontakt", label: "Kontakt" },
    ],
  },
];

export const stats = [
  { value: 100, suffix: "%", label: "Fokus auf Kundenzufriedenheit" },
  { value: 3, suffix: "+", label: "Jahre Erfahrung" },
  { value: 5, suffix: " Mio.+", label: "Views generiert" },
  { value: 120, suffix: "k+", label: "Likes gesammelt" },
  { value: 30, suffix: "+", label: "Glückliche Kunden" },
];

export const flagshipCase = {
  title: "142 qualifizierte Anfragen für eine lokale Dienstleisterin.",
  subtitle: "Google Search Ads + Meta Retargeting · Beispiel-Kampagne, Regensburg",
  stats: [
    { value: 142, decimals: 0, prefix: "", suffix: "", label: "Anfragen" },
    { value: 1.48, decimals: 1, prefix: "€", suffix: "", label: "Kosten pro Klick" },
    { value: 8.4, decimals: 1, prefix: "", suffix: "%", label: "Conversion Rate" },
    { value: 17.6, decimals: 1, prefix: "€", suffix: "", label: "Cost per Lead" },
  ],
  breakdown: [
    {
      heading: "Ausgangslage",
      text: "Eine Kundin im Bereich dauerhafte Haarentfernung in Regensburg wollte planbar mehr qualifizierte Anfragen gewinnen, statt sich auf Zufallslaufkundschaft zu verlassen.",
    },
    {
      heading: "Strategie",
      text: "Kombination aus Google Search Ads für aktive Suchanfragen und Meta-Retargeting, um Interessenten erneut gezielt anzusprechen.",
    },
    {
      heading: "Umsetzung",
      text: "Kampagnenstruktur, Zielgruppen, Landingpage und Tracking wurden aufgesetzt und laufend anhand der Ergebnisse optimiert.",
    },
    {
      heading: "Ergebnis",
      text: "142 qualifizierte Neukundenanfragen bei 17,60 € Cost per Lead und einer Conversion-Rate von 8,4 %.",
    },
  ],
};

export const upcomingCases = [
  {
    id: "case-club-aktiv",
    name: "Club Aktiv",
    category: "Social Media · organisches Instagram-Wachstum",
    blurb:
      "Ein Fitnessstudio, für das wir organische Social-Media-Präsenz und Community-Aufbau umsetzen — von Content-Strategie bis Reels.",
    fields:
      "Zeitraum · Ausgangslage · Content-Strategie · veröffentlichte Reels · Views · Reichweite · Followerentwicklung · Engagement · Top-Reels · Ergebnis",
    related: { slug: "social-media-agentur-konstanz", label: "Social Media" },
  },
  {
    id: "case-polywerft",
    name: "Polywerft Konstanz",
    category: "Social Recruiting",
    blurb:
      "Eine Recruiting-Kampagne, mit der wir Mitarbeiter für Polywerft Konstanz gewinnen — mit authentischen Recruiting-Reels und gezielter Ansprache.",
    fields:
      "Ausgangslage · gesuchte Position(en) · Recruiting-Strategie · Content / Recruiting-Reels · Kampagne · Bewerbungen · qualifizierte Bewerbungen · Einstellungen · Zeitraum · Ergebnis",
    related: { slug: "social-recruiting", label: "Social Recruiting" },
  },
];

export const clientLogos = [
  { file: "client-club-aktiv.jpg", alt: "Club Aktiv" },
  { file: "client-o2.jpg", alt: "o2" },
  { file: "client-polywerft.jpg", alt: "Polywerft" },
  { file: "client-staib.jpg", alt: "Staib" },
  { file: "client-prima-vera-dresses.jpg", alt: "Prima Vera Dresses" },
  { file: "client-bck-adventure.jpg", alt: "BCK Adventure" },
  { file: "client-a-gradmann.jpg", alt: "A. Gradmann" },
  { file: "client-langenbach.jpg", alt: "Langenbach" },
  { file: "client-freshlineart.jpg", alt: "FreshLineArt" },
];

export const team = [
  {
    name: "Shawn",
    role: "Social Media & organisches Wachstum",
    photo: "team-shawn.jpg",
    responsibilities: ["Social-Media-Strategie", "Content", "Drehs", "Reels", "organisches Wachstum"],
  },
  {
    name: "Lennert",
    role: "Websites & Performance Marketing",
    photo: "team-lennert.jpg",
    responsibilities: ["Webdesign", "SEO", "Google Ads", "Meta Ads", "Tracking"],
  },
];

export const principles = [
  {
    n: "01",
    heading: "Digital Natives statt Meeting-Schleifen",
    text: "Wir reden nicht monatelang über Trends — wir setzen sie direkt um und verstehen Plattform-Algorithmen nativ.",
  },
  {
    n: "02",
    heading: "End-to-End Produktion",
    text: "Vom ersten Skript über den Dreh vor Ort bis zum fertigen Schnitt — für Sie entsteht kein eigener Aufwand.",
  },
  {
    n: "03",
    heading: "Fokus auf messbaren Ertrag",
    text: "Keine Vanity-Metriken. Bei uns zählen qualifizierte Leads und nachvollziehbare Sichtbarkeit bei Google.",
  },
];

export const processSteps = [
  { num: "STRATEGIE", heading: "Zielgruppen & Botschaft", text: "Zielgruppen, Kernbotschaft und Kanäle werden präzise auf Ihr Angebot abgestimmt." },
  { num: "PRODUKTION", heading: "Skript, Dreh, Schnitt", text: "Wir übernehmen Skript, Dreh vor Ort und professionellen Schnitt — ganz ohne Aufwand für Sie." },
  { num: "ADS", heading: "Google & Meta", text: "Gezielte Kampagnen bringen den Content genau zu den Menschen, die kaufbereit sind." },
  { num: "WACHSTUM", heading: "Planbare Anfragen", text: "Qualifizierte Anfragen laufen regelmäßig und nachvollziehbar bei Ihnen ein." },
];

const zeitaufwandAnswer =
  "In der Regel benötigen wir etwa 30–60 Minuten pro Woche für den gemeinsamen Drehtermin. Planung, Skripte, Schnitt, Veröffentlichung und Auswertung übernehmen wir. Monatlich erhalten Sie einen kompakten Performance-Bericht; alle drei Monate analysieren wir die Entwicklung ausführlich und leiten die nächsten Maßnahmen ab.";

export const faq = [
  { q: "Wie viel Zeitaufwand entsteht für mein Team und mich?", a: zeitaufwandAnswer },
  { q: "Auf welchen Plattformen laufen Content und Ads?", a: "Primär Instagram Reels, TikTok und YouTube Shorts sowie Meta Ads und Google Ads. Die Strategie stimmen wir exakt auf Ihre Zielgruppe ab." },
  { q: "Wie schnell sind erste Ergebnisse sichtbar?", a: "Erste organische Reichweiten- und Engagement-Zuwächse zeigen sich meist innerhalb von 2–4 Wochen. Bezahlte Kampagnen liefern oft schon nach 7–14 Tagen qualifizierte Anfragen." },
  { q: "Gibt es lange Vertragslaufzeiten?", a: "Nein. Wir setzen auf partnerschaftliche Zusammenarbeit auf Augenhöhe mit flexiblen Monatsmodellen, die sich Ihrer Unternehmensphase anpassen." },
  { q: "Wie läuft die Zusammenarbeit konkret ab?", a: "Nach der kostenlosen Potenzialanalyse erstellen wir eine Content- und Ad-Strategie, drehen und schneiden vor Ort und übernehmen Posting sowie Reporting — Sie erhalten monatlich einen kurzen Überblick über alle Ergebnisse." },
];

export interface PricingTier {
  name: string;
  tagline: string;
  features: string[];
  fit: string;
  featured?: boolean;
}

export const pricing: PricingTier[] = [
  {
    name: "Basis",
    tagline: "Der solide Einstieg in Social Media",
    features: [
      "Community Management & Reporting",
      "4 Reels pro Monat",
      "Instagram- & Facebook-Betreuung",
      "Ideengenerierung & Skript",
      "Video-Dreh vor Ort & Schnitt",
      "Caption, Cover & Posting",
    ],
    fit: "Unternehmen, die professionell mit Social Media starten möchten.",
  },
  {
    name: "Komplett-Service",
    tagline: "Content plus Sichtbarkeit aus einer Hand",
    features: [
      "Alle Leistungen aus dem Basis Paket",
      "8 Short-Form Videos pro Monat",
      "SEO & GEO Website-Optimierung",
      "Regelmäßiges Performance-Reporting",
    ],
    fit: "Unternehmen, die Content und digitale Sichtbarkeit aus einer Hand möchten.",
    featured: true,
  },
  {
    name: "Vollgas",
    tagline: "Maßgeschneidert für maximales Tempo",
    features: [
      "Alle Leistungen aus dem Komplett-Service",
      "Bis zu 15 Short-Form Videos pro Monat",
      "Zusätzlich TikTok-Betreuung",
      "Google & Meta Ads inklusive",
    ],
    fit: "Unternehmen, die Content, Ads und Website kombinieren möchten.",
  },
];

export const demoUrl = "https://zahnarzt.steinhauermedia.de";

export const navLinks = [
  { slug: "referenzen", label: "Referenzen" },
  { slug: "pakete", label: "Pakete" },
  { slug: "ueber-uns", label: "Über uns" },
];

export const footerLeistungen = services.map((s) => ({ slug: s.slug, label: s.name }));
export const footerAgentur = [
  { slug: "referenzen", label: "Referenzen" },
  { slug: "pakete", label: "Pakete" },
  { slug: "ueber-uns", label: "Über uns" },
  { slug: "kontakt", label: "Kontakt" },
];
export const footerRechtlich = [
  { slug: "impressum", label: "Impressum" },
  { slug: "datenschutz", label: "Datenschutz" },
];
