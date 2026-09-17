(function(){
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- SCROLL PROGRESS BAR + STICKY HEADER ---------- */
  var progressBar = document.getElementById('progress-bar');
  var siteNav = document.getElementById('site-nav');
  function updateProgressBar(){
    var scrollTop = window.scrollY;
    var docHeight = document.documentElement.scrollHeight - window.innerHeight;
    var pct = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
    if(progressBar) progressBar.style.width = pct + '%';
    if(siteNav) siteNav.classList.toggle('scrolled', scrollTop > 40);
  }
  window.addEventListener('scroll', updateProgressBar);
  updateProgressBar();

  /* ---------- MOBILE NAV TOGGLE ---------- */
  var toggle = document.getElementById('nav-toggle');
  var navLinksWrap = document.querySelector('.nav-links');
  var mobileNavOpenTimer = null;
  function closeMobileNav(focusToggle){
    if(!navLinksWrap) return;
    navLinksWrap.classList.remove('mobile-open-visible');
    toggle.setAttribute('aria-expanded', 'false');
    clearTimeout(mobileNavOpenTimer);
    mobileNavOpenTimer = setTimeout(function(){ navLinksWrap.classList.remove('mobile-open'); }, reduced ? 0 : 220);
    if(focusToggle) toggle.focus();
  }
  function openMobileNav(){
    clearTimeout(mobileNavOpenTimer);
    navLinksWrap.classList.add('mobile-open');
    toggle.setAttribute('aria-expanded', 'true');
    requestAnimationFrame(function(){
      requestAnimationFrame(function(){ navLinksWrap.classList.add('mobile-open-visible'); });
    });
    var firstLink = navLinksWrap.querySelector('a, button');
    if(firstLink) firstLink.focus();
  }
  if(toggle && navLinksWrap){
    toggle.addEventListener('click', function(){
      var open = navLinksWrap.classList.contains('mobile-open');
      if(open) closeMobileNav(false); else openMobileNav();
    });
    document.addEventListener('keydown', function(e){
      if(e.key === 'Escape' && navLinksWrap.classList.contains('mobile-open')){
        closeMobileNav(true);
      }
    });
  }

  /* ---------- LEISTUNGEN DROPDOWN / MOBILE SUBMENU ---------- */
  var ddWrap = document.getElementById('nav-leistungen-dropdown');
  if(ddWrap){
    var ddTrigger = ddWrap.querySelector('.nav-dd-trigger');
    var ddMenu = ddWrap.querySelector('.nav-dropdown');
    var subTrigger = ddWrap.querySelector('.mobile-submenu-trigger');
    var subMenu = ddWrap.querySelector('.mobile-submenu');

    function closeDesktopDD(){
      ddWrap.classList.remove('open');
      if(ddTrigger) ddTrigger.setAttribute('aria-expanded', 'false');
    }
    if(ddTrigger){
      ddTrigger.addEventListener('click', function(){
        var open = ddWrap.classList.toggle('open');
        ddTrigger.setAttribute('aria-expanded', open ? 'true' : 'false');
      });
    }
    document.addEventListener('click', function(e){
      if(!ddWrap.contains(e.target)) closeDesktopDD();
    });
    document.addEventListener('keydown', function(e){
      if(e.key === 'Escape') closeDesktopDD();
    });

    if(subTrigger && subMenu){
      subTrigger.addEventListener('click', function(){
        var open = subMenu.classList.toggle('open');
        subTrigger.setAttribute('aria-expanded', open ? 'true' : 'false');
      });
    }
  }

  /* ---------- HERO HEADLINE STAGGER ---------- */
  var headline = document.getElementById('hero-headline');
  if(headline){
    var words = headline.textContent.trim().split(' ');
    headline.innerHTML = words.map(function(w){ return '<span class="word">'+w+'</span>'; }).join(' ');
    var wordEls = headline.querySelectorAll('.word');
    wordEls.forEach(function(el,i){ setTimeout(function(){ el.classList.add('in'); }, 120 + i*70); });
    setTimeout(function(){
      var lead = document.querySelector('.hero p.lead');
      var actions = document.querySelector('.hero-actions');
      if(lead) lead.classList.add('in');
      if(actions) actions.classList.add('in');
    }, 200);
    /* safety net: guarantee visibility even if the above ever fails to run */
    setTimeout(function(){
      document.querySelectorAll('.hero h1 .word, .hero p.lead, .hero-actions').forEach(function(el){ el.classList.add('in'); });
    }, 900);
  }

  /* ---------- HERO MOUSE PARALLAX ---------- */
  if(!reduced){
    var heroEl = document.querySelector('.hero');
    if(heroEl){
      var grid = document.getElementById('hero-grid');
      var emblem = document.getElementById('hero-emblem');
      heroEl.addEventListener('mousemove', function(e){
        var r = heroEl.getBoundingClientRect();
        var x = (e.clientX - r.left)/r.width - 0.5;
        var y = (e.clientY - r.top)/r.height - 0.5;
        if(grid) grid.style.transform = 'translate('+(x*14)+'px,'+(y*14)+'px)';
        if(emblem) emblem.style.transform = 'translateY(calc(-50% + '+(y*-18)+'px)) translateX('+(x*-18)+'px)';
      });
    }
  }

  /* ---------- REVEAL OBSERVER ---------- */
  var revealObserver = new IntersectionObserver(function(entries){
    entries.forEach(function(entry){
      if(entry.isIntersecting){ entry.target.classList.add('in'); revealObserver.unobserve(entry.target); }
    });
  }, { threshold:0.15 });

  function initRevealsFor(root){
    root.querySelectorAll('.reveal, .reveal-stagger').forEach(function(el){
      if(!el.classList.contains('in')) revealObserver.observe(el);
    });
  }
  initRevealsFor(document);

  /* ---------- COUNTERS ---------- */
  /* The static HTML already contains the real, final value (for crawlers,
     screen readers and no-JS users). When a counter scrolls into view we
     reset it to 0 and animate up to that same value purely as a visual
     enhancement. */
  var counterObserver = new IntersectionObserver(function(entries){
    entries.forEach(function(entry){
      if(entry.isIntersecting){
        animateCounter(entry.target);
        counterObserver.unobserve(entry.target);
      }
    });
  }, { threshold:0.4 });
  document.querySelectorAll('[data-count]').forEach(function(el){ counterObserver.observe(el); });

  function animateCounter(el){
    var target = parseFloat(el.dataset.count);
    var decimals = parseInt(el.dataset.decimal || '0');
    var prefix = el.dataset.prefix || '';
    var suffix = el.dataset.suffix || '';
    var dur = 1400, start = null;
    function step(ts){
      if(!start) start = ts;
      var p = Math.min((ts-start)/dur, 1);
      var eased = 1 - Math.pow(1-p, 3);
      var val = (target*eased).toFixed(decimals);
      el.textContent = prefix + val.replace('.', ',') + suffix;
      if(p < 1) requestAnimationFrame(step); else el.textContent = prefix + target.toFixed(decimals).replace('.', ',') + suffix;
    }
    requestAnimationFrame(step);
  }

  /* ---------- 3D TILT CARDS ---------- */
  if(!reduced){
    document.querySelectorAll('[data-tilt]').forEach(function(card){
      card.addEventListener('mousemove', function(e){
        var r = card.getBoundingClientRect();
        var x = (e.clientX - r.left)/r.width - 0.5;
        var y = (e.clientY - r.top)/r.height - 0.5;
        card.style.transform = 'perspective(700px) rotateX('+(y*-6)+'deg) rotateY('+(x*6)+'deg) translateY(-2px)';
      });
      card.addEventListener('mouseleave', function(){ card.style.transform = 'perspective(700px) rotateX(0) rotateY(0)'; });
    });
  }

  /* ---------- MAGNETIC BUTTONS ---------- */
  if(!reduced){
    document.querySelectorAll('[data-magnetic]').forEach(function(wrap){
      var btn = wrap.querySelector('a,button');
      wrap.addEventListener('mousemove', function(e){
        var r = wrap.getBoundingClientRect();
        var x = e.clientX - (r.left + r.width/2);
        var y = e.clientY - (r.top + r.height/2);
        btn.style.transform = 'translate('+(x*0.25)+'px,'+(y*0.35)+'px)';
      });
      wrap.addEventListener('mouseleave', function(){ btn.style.transform = 'translate(0,0)'; });
      btn.style.transition = 'transform .2s ease';
    });
  }

  /* ---------- MASK REVEAL CTA ---------- */
  var maskObserver = new IntersectionObserver(function(entries){
    entries.forEach(function(entry){
      if(entry.isIntersecting){ entry.target.classList.add('revealed'); maskObserver.unobserve(entry.target); }
    });
  }, { threshold:0.25 });
  document.querySelectorAll('[data-mask]').forEach(function(el){ maskObserver.observe(el); });
  setTimeout(function(){
    document.querySelectorAll('[data-mask]').forEach(function(el){ el.classList.add('revealed'); });
  }, 1800);

  /* ---------- SCALE ON SCROLL PANELS ---------- */
  var scalePanels = document.querySelectorAll('[data-scale]');
  function updateScalePanels(){
    scalePanels.forEach(function(panel){
      var r = panel.getBoundingClientRect();
      if(r.top < window.innerHeight && r.bottom > 0){
        var center = r.top + r.height/2;
        var dist = Math.abs(window.innerHeight/2 - center) / (window.innerHeight/2);
        var scale = 1 - Math.min(dist, 1)*0.1;
        panel.style.transform = 'scale('+Math.max(scale,0.88)+')';
      }
    });
  }

  /* ---------- PROZESS STICKY SCROLL ---------- */
  var prozessScroll = document.getElementById('prozess-scroll');
  var steps = document.querySelectorAll('.prozess-step');
  var indexLabel = document.getElementById('prozess-index');
  var barFill = document.getElementById('prozess-bar-fill');
  function updateProzess(){
    if(!prozessScroll) return;
    var r = prozessScroll.getBoundingClientRect();
    var total = r.height - window.innerHeight;
    if(total <= 0) return;
    var progress = Math.min(Math.max(-r.top / total, 0), 1);
    var stepCount = steps.length;
    var idx = Math.min(Math.floor(progress * stepCount), stepCount - 1);
    steps.forEach(function(s,i){ s.classList.toggle('active', i === idx); });
    if(indexLabel) indexLabel.textContent = ('0'+(idx+1)).slice(-2) + ' / 0' + stepCount;
    if(barFill) barFill.style.width = (((idx+1)/stepCount)*100) + '%';
  }

  var ticking = false;
  window.addEventListener('scroll', function(){
    if(!ticking){
      requestAnimationFrame(function(){ updateProzess(); updateScalePanels(); ticking = false; });
      ticking = true;
    }
  });
  updateProzess(); updateScalePanels();

  /* ---------- PROTOTYPE VIEWPORT TOGGLE ---------- */
  var protoBtns = document.querySelectorAll('.proto-btn');
  var protoViewport = document.getElementById('proto-viewport');
  protoBtns.forEach(function(btn){
    btn.addEventListener('click', function(){
      protoBtns.forEach(function(b){ b.classList.remove('active'); b.setAttribute('aria-pressed', 'false'); });
      btn.classList.add('active');
      btn.setAttribute('aria-pressed', 'true');
      var view = btn.dataset.view;
      protoViewport.classList.remove('view-desktop','view-mobile');
      protoViewport.classList.add('view-' + view);
    });
  });

  /* ---------- FAQ ACCORDION ---------- */
  document.querySelectorAll('.faq-item').forEach(function(item){
    var btn = item.querySelector('.faq-q');
    if(!btn) return;
    btn.addEventListener('click', function(){
      var open = item.classList.toggle('open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  });

  /* ---------- CONTACT FORM -> MAILTO ---------- */
  var form = document.getElementById('contact-form');
  if(form){
    form.addEventListener('submit', function(e){
      e.preventDefault();
      var name = document.getElementById('c-name').value;
      var company = document.getElementById('c-company').value;
      var mail = document.getElementById('c-mail').value;
      var phone = document.getElementById('c-phone').value;
      var topic = document.getElementById('c-topic').value;
      var message = document.getElementById('c-message').value;
      var subject = 'Kostenlose Potenzialanalyse' + (topic ? ' – ' + topic : '');
      var body = 'Name: '+name+'\nUnternehmen: '+company+'\nE-Mail: '+mail+'\nTelefon: '+phone+'\nThema: '+topic+'\n\n'+message;
      window.location.href = 'mailto:info@steinhauermedia.de?subject='+encodeURIComponent(subject)+'&body='+encodeURIComponent(body);
    });
  }
})();
