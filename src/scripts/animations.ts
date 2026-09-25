import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

gsap.registerPlugin(ScrollTrigger);

/* ---------------------------------------------------------------------- */
/* Scroll reveal — fade/rise on enter, staggered for .reveal-stagger groups */
/* ---------------------------------------------------------------------- */
function initReveal() {
  const groups = document.querySelectorAll<HTMLElement>(".reveal-stagger");
  groups.forEach((group) => {
    Array.from(group.children).forEach((child, i) => {
      child.classList.add("reveal");
      (child as HTMLElement).style.transitionDelay = `${Math.min(i * 90, 360)}ms`;
    });
  });

  const items = document.querySelectorAll<HTMLElement>(".reveal");
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
/* Process strip — pinned scroll sequence                                 */
/* ---------------------------------------------------------------------- */
function initProcessStrip() {
  const root = document.querySelector<HTMLElement>("[data-process]");
  if (!root) return;
  const pinTarget = root.querySelector<HTMLElement>("[data-process-pin]");
  const steps = Array.from(root.querySelectorAll<HTMLElement>("[data-process-step]"));
  const fill = root.querySelector<HTMLElement>("[data-process-fill]");
  const indexLabel = root.querySelector<HTMLElement>("[data-process-index]");
  if (!pinTarget || steps.length === 0) return;

  ScrollTrigger.create({
    trigger: root,
    start: "top top",
    end: "bottom bottom",
    pin: pinTarget,
    pinSpacing: false,
  });

  steps.forEach((step, i) => {
    ScrollTrigger.create({
      trigger: step,
      start: "top center",
      end: "bottom center",
      onToggle: (self) => {
        if (!self.isActive) return;
        steps.forEach((s) => s.classList.remove("is-active"));
        step.classList.add("is-active");
        if (fill) fill.style.width = `${((i + 1) / steps.length) * 100}%`;
        if (indexLabel) indexLabel.textContent = `${String(i + 1).padStart(2, "0")} / ${String(steps.length).padStart(2, "0")}`;
      },
    });
  });
}

/* ---------------------------------------------------------------------- */
/* Sticky nav background handled in Nav.astro; init everything else here  */
/*                                                                        */
/* "astro:page-load" fires on the initial page load AND after every      */
/* client-side view-transition navigation, so it alone covers both cases */
/* — registering a second listener for DOMContentLoaded would run init() */
/* twice on first load and create duplicate (conflicting) ScrollTriggers.*/
/* ---------------------------------------------------------------------- */
function init() {
  ScrollTrigger.getAll().forEach((t) => t.kill());
  document.documentElement.classList.remove("no-js");
  initReveal();
  initWordReveal();
  initMagnetic();
  initCounters();
  initProcessStrip();
  ScrollTrigger.refresh();
}

document.addEventListener("astro:page-load", init);
