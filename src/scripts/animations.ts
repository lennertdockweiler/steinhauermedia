import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

gsap.registerPlugin(ScrollTrigger);

/* ---------------------------------------------------------------------- */
/* Scroll reveal — fade/rise (or clip-path wipe) on enter, staggered for  */
/* .reveal-stagger groups                                                 */
/* ---------------------------------------------------------------------- */
function initReveal() {
  const groups = document.querySelectorAll<HTMLElement>(".reveal-stagger");
  groups.forEach((group) => {
    Array.from(group.children).forEach((child, i) => {
      child.classList.add("reveal");
      (child as HTMLElement).style.transitionDelay = `${Math.min(i * 90, 360)}ms`;
    });
  });

  const items = document.querySelectorAll<HTMLElement>(".reveal, .wipe-observe");
  const io = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          io.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.14, rootMargin: "0px 0px -8% 0px" }
  );
  items.forEach((el) => io.observe(el));
}

/* ---------------------------------------------------------------------- */
/* Word-stagger reveal for hero-grade headlines                           */
/* ---------------------------------------------------------------------- */
function initWordReveal() {
  document.querySelectorAll<HTMLElement>("[data-word-reveal]").forEach((el) => {
    const words = el.querySelectorAll<HTMLElement>(".word");
    gsap.set(words, { yPercent: 110, opacity: 0 });
    ScrollTrigger.create({
      trigger: el,
      start: "top 88%",
      once: true,
      onEnter: () =>
        gsap.to(words, {
          yPercent: 0,
          opacity: 1,
          duration: 0.9,
          ease: "expo.out",
          stagger: 0.045,
        }),
    });
  });
}

/* ---------------------------------------------------------------------- */
/* Magnetic buttons                                                       */
/* ---------------------------------------------------------------------- */
function initMagnetic() {
  const els = document.querySelectorAll<HTMLElement>("[data-magnetic]");
  els.forEach((el) => {
    const strength = 0.35;
    const moveX = gsap.quickTo(el, "x", { duration: 0.5, ease: "power3.out" });
    const moveY = gsap.quickTo(el, "y", { duration: 0.5, ease: "power3.out" });
    el.addEventListener("mousemove", (e) => {
      const r = el.getBoundingClientRect();
      const relX = e.clientX - (r.left + r.width / 2);
      const relY = e.clientY - (r.top + r.height / 2);
      moveX(relX * strength);
      moveY(relY * strength);
    });
    el.addEventListener("mouseleave", () => {
      moveX(0);
      moveY(0);
    });
  });
}

/* ---------------------------------------------------------------------- */
/* Count-up stat numbers                                                  */
/* ---------------------------------------------------------------------- */
function initCounters() {
  const els = document.querySelectorAll<HTMLElement>("[data-count]");
  els.forEach((el) => {
    const target = parseFloat(el.dataset.count || "0");
    const decimals = parseInt(el.dataset.decimals || "0", 10);
    const prefix = el.dataset.prefix || "";
    const suffix = el.dataset.suffix || "";
    const obj = { val: 0 };
    ScrollTrigger.create({
      trigger: el,
      start: "top 90%",
      once: true,
      onEnter: () =>
        gsap.to(obj, {
          val: target,
          duration: 1.6,
          ease: "power2.out",
          onUpdate: () => {
            el.textContent = `${prefix}${obj.val.toFixed(decimals).replace(".", ",")}${suffix}`;
          },
        }),
    });
  });
}

/* ---------------------------------------------------------------------- */
/* Fixed top scroll-progress bar — fills with how far down the current    */
/* page you've scrolled. Combined with the nav-scrolled toggle into one   */
/* listener, attached once at module scope: document is never replaced by */
/* a view transition, and both handlers just re-query the live elements.  */
/* ---------------------------------------------------------------------- */
function onScroll() {
  const header = document.getElementById("site-nav");
  if (header) {
    if (window.scrollY > 12) header.classList.add("nav-scrolled");
    else header.classList.remove("nav-scrolled");
  }
  const fill = document.getElementById("scroll-progress-fill");
  if (fill) {
    const docHeight = document.documentElement.scrollHeight - window.innerHeight;
    const progress = docHeight > 0 ? Math.min(1, Math.max(0, window.scrollY / docHeight)) : 0;
    fill.style.transform = `scaleX(${progress})`;
  }
}

/* ---------------------------------------------------------------------- */
/* Process section progress line — fills as the section scrolls past,     */
/* no pin: the page never stops scrolling for it.                         */
/* ---------------------------------------------------------------------- */
function initProcessProgress() {
  const section = document.querySelector<HTMLElement>("[data-process]");
  const fill = section?.querySelector<HTMLElement>("[data-process-fill]");
  if (!section || !fill) return;
  ScrollTrigger.create({
    trigger: section,
    start: "top 75%",
    end: "bottom 55%",
    scrub: true,
    onUpdate: (self) => {
      fill.style.transform = `scaleX(${self.progress})`;
    },
  });
}

/* ---------------------------------------------------------------------- */
/* Hero cursor-glow — a soft radial highlight that follows the pointer    */
/* ---------------------------------------------------------------------- */
function initCursorGlow() {
  const glow = document.querySelector<HTMLElement>("[data-cursor-glow]");
  const zone = glow?.closest<HTMLElement>("[data-cursor-glow-zone]");
  if (!glow || !zone) return;
  gsap.set(glow, { xPercent: -50, yPercent: -50, opacity: 0 });
  const moveX = gsap.quickTo(glow, "x", { duration: 0.6, ease: "power3.out" });
  const moveY = gsap.quickTo(glow, "y", { duration: 0.6, ease: "power3.out" });
  zone.addEventListener("mousemove", (e) => {
    const r = zone.getBoundingClientRect();
    moveX(e.clientX - r.left);
    moveY(e.clientY - r.top);
    gsap.to(glow, { opacity: 1, duration: 0.4 });
  });
  zone.addEventListener("mouseleave", () => gsap.to(glow, { opacity: 0, duration: 0.4 }));
}

/* ---------------------------------------------------------------------- */
/* Icon draw-in — strokes/outlines trace themselves on scroll-enter       */
/* ---------------------------------------------------------------------- */
function initIconDraw() {
  const svgs = document.querySelectorAll<SVGSVGElement>("svg[data-draw]");
  svgs.forEach((svg) => {
    const shapes = svg.querySelectorAll<SVGGeometryElement>("path, circle, rect");
    shapes.forEach((shape) => {
      const length = shape.getTotalLength();
      shape.style.strokeDasharray = `${length}`;
      shape.style.strokeDashoffset = `${length}`;
    });
  });

  const io = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        const shapes = entry.target.querySelectorAll("path, circle, rect");
        gsap.to(shapes, { strokeDashoffset: 0, duration: 1, ease: "power2.out", stagger: 0.08 });
        io.unobserve(entry.target);
      });
    },
    { threshold: 0.4 }
  );
  svgs.forEach((svg) => io.observe(svg));
}

/* ---------------------------------------------------------------------- */
/* Card tilt — subtle 3D perspective tilt following the pointer            */
/* ---------------------------------------------------------------------- */
function initTilt() {
  const cards = document.querySelectorAll<HTMLElement>("[data-tilt]");
  cards.forEach((card) => {
    gsap.set(card, { transformPerspective: 700 });
    const rotateX = gsap.quickTo(card, "rotationX", { duration: 0.4, ease: "power2.out" });
    const rotateY = gsap.quickTo(card, "rotationY", { duration: 0.4, ease: "power2.out" });
    card.addEventListener("mousemove", (e) => {
      const r = card.getBoundingClientRect();
      const px = (e.clientX - r.left) / r.width - 0.5;
      const py = (e.clientY - r.top) / r.height - 0.5;
      rotateY(px * 8);
      rotateX(-py * 8);
    });
    card.addEventListener("mouseleave", () => {
      rotateX(0);
      rotateY(0);
    });
  });
}

/* ---------------------------------------------------------------------- */
/* "astro:page-load" fires on the initial page load AND after every      */
/* client-side view-transition navigation, so it alone covers both cases */
/* — registering a second listener for DOMContentLoaded would run init() */
/* twice on first load and create duplicate (conflicting) ScrollTriggers.*/
/* ---------------------------------------------------------------------- */
function init() {
  ScrollTrigger.getAll().forEach((t) => t.kill());
  document.documentElement.classList.remove("no-js");
  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  initReveal();
  initCounters();
  onScroll();
  if (!reducedMotion) {
    initWordReveal();
    initMagnetic();
    initProcessProgress();
    initCursorGlow();
    initIconDraw();
    initTilt();
  }
  ScrollTrigger.refresh();
}

document.addEventListener("astro:page-load", init);
document.addEventListener("scroll", onScroll, { passive: true });
