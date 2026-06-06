// NovaSysTech — Main JavaScript (v2 - Amélioré)

document.addEventListener('DOMContentLoaded', function () {

  // ── NAVBAR SCROLL ────────────────────────────────────────
  const navbar = document.querySelector('.navbar');
  window.addEventListener('scroll', () => {
    navbar.classList.toggle('scrolled', window.scrollY > 50);
    const btt = document.querySelector('.back-to-top');
    if (btt) btt.classList.toggle('visible', window.scrollY > 400);
  });

  // ── BACK TO TOP ──────────────────────────────────────────
  const btt = document.querySelector('.back-to-top');
  if (btt) btt.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));

  // ── MOBILE MENU ──────────────────────────────────────────
  const toggle = document.querySelector('.nav-toggle');
  const menu = document.querySelector('.nav-menu');
  if (toggle && menu) {
    function closeMenu() {
      menu.classList.remove('open');
      toggle.classList.remove('active');
    }
    function toggleMenu() {
      menu.classList.toggle('open');
      toggle.classList.toggle('active');
    }
    toggle.addEventListener('click', (e) => {
      e.stopPropagation();
      toggleMenu();
    });
    // Close when a nav link is clicked, except when toggling the dropdown on mobile
    menu.querySelectorAll('.nav-link, .nav-dropdown-item').forEach(link => {
      link.addEventListener('click', (e) => {
        if (window.innerWidth <= 768 && link.parentElement.classList.contains('nav-dropdown')) {
          const dropdownMenu = link.nextElementSibling;
          if (dropdownMenu && dropdownMenu.classList.contains('nav-dropdown-menu')) {
            if (!dropdownMenu.classList.contains('open')) {
              e.preventDefault(); // Empêche la navigation au 1er clic
              dropdownMenu.classList.add('open'); // Ouvre le sous-menu
              return; // Ne ferme pas le menu principal
            }
          }
        }
        closeMenu();
      });
    });
    // Close on outside click
    document.addEventListener('click', e => {
      if (menu.classList.contains('open') && !toggle.contains(e.target) && !menu.contains(e.target)) {
        closeMenu();
      }
    });
  }

  // ── AOS (Animate on Scroll) ──────────────────────────────
  const aosEls = document.querySelectorAll('[data-aos]');
  if (aosEls.length) {
    const obs = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const delay = parseInt(entry.target.dataset.aosDelay || 0);
          setTimeout(() => entry.target.classList.add('aos-animate'), delay);
          obs.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });
    aosEls.forEach(el => obs.observe(el));
  }

  // ── COUNTER ANIMATION ────────────────────────────────────
  const counters = document.querySelectorAll('[data-counter]');
  if (counters.length) {
    const obs = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const el = entry.target;
          const target = parseInt(el.dataset.counter);
          const suffix = el.dataset.suffix || '';
          let startTime = null;
          const step = (ts) => {
            if (!startTime) startTime = ts;
            const progress = Math.min((ts - startTime) / 2000, 1);
            const ease = 1 - Math.pow(1 - progress, 3);
            el.textContent = Math.floor(ease * target) + suffix;
            if (progress < 1) requestAnimationFrame(step);
          };
          requestAnimationFrame(step);
          obs.unobserve(el);
        }
      });
    }, { threshold: 0.5 });
    counters.forEach(el => obs.observe(el));
  }

  // ── TOAST NOTIFICATIONS ──────────────────────────────────
  function showToast(success, message) {
    let container = document.querySelector('.toast-container');
    if (!container) {
      container = document.createElement('div');
      container.className = 'toast-container';
      document.body.appendChild(container);
    }
    const toast = document.createElement('div');
    toast.className = `toast ${success ? 'success' : 'error'}`;
    toast.innerHTML = `
      <div class="toast-icon">${success ? '✅' : '❌'}</div>
      <div class="toast-body">
        <strong>${success ? 'Succès !' : 'Erreur'}</strong>
        <span>${message}</span>
      </div>
    `;
    container.appendChild(toast);
    setTimeout(() => {
      toast.style.animation = 'fadeOut 0.4s ease forwards';
      setTimeout(() => toast.remove(), 400);
    }, 5000);
  }

  // ── AJAX FORM HANDLER ────────────────────────────────────
  function handleAjaxForm(formEl) {
    formEl.addEventListener('submit', async (e) => {
      e.preventDefault();
      const btn = formEl.querySelector('[type="submit"]');
      const origHTML = btn.innerHTML;
      btn.classList.add('btn-loading');
      btn.innerHTML = 'Envoi en cours...';

      try {
        const resp = await fetch(formEl.action || window.location.href, {
          method: 'POST',
          body: new FormData(formEl),
          headers: { 'X-Requested-With': 'XMLHttpRequest' }
        });
        const data = await resp.json();
        showToast(data.success, data.message || (data.success ? 'Envoyé !' : 'Erreur'));
        if (data.success) formEl.reset();
      } catch {
        showToast(false, 'Une erreur est survenue. Vérifiez votre connexion.');
      }
      btn.classList.remove('btn-loading');
      btn.innerHTML = origHTML;
      btn.disabled = false;
    });
  }

  const devisForm = document.getElementById('devis-form');
  if (devisForm) handleAjaxForm(devisForm);

  const contactForm = document.getElementById('contact-form');
  if (contactForm) handleAjaxForm(contactForm);

  // Newsletter forms
  document.querySelectorAll('.newsletter-form-js').forEach(form => {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const btn = form.querySelector('button');
      const origText = btn.textContent;
      btn.textContent = '...';
      try {
        const resp = await fetch('/newsletter/', {
          method: 'POST',
          body: new FormData(form),
          headers: { 'X-Requested-With': 'XMLHttpRequest' }
        });
        const data = await resp.json();
        showToast(data.success, data.message);
        if (data.success) { form.reset(); btn.textContent = '✓ Abonné !'; btn.style.background = 'var(--success)'; }
        else btn.textContent = origText;
      } catch { btn.textContent = origText; showToast(false, 'Erreur réseau.'); }
    });
  });

  // ── FAQ ACCORDION ────────────────────────────────────────
  document.querySelectorAll('.accordion-header').forEach(header => {
    header.addEventListener('click', () => {
      const item = header.closest('.accordion-item');
      const body = item.querySelector('.accordion-body');
      const isOpen = item.classList.contains('open');
      document.querySelectorAll('.accordion-item.open').forEach(i => {
        i.classList.remove('open');
        i.querySelector('.accordion-body').classList.remove('open');
      });
      if (!isOpen) { item.classList.add('open'); body.classList.add('open'); }
    });
  });

  // ── FAQ SIDEBAR NAV ──────────────────────────────────────
  document.querySelectorAll('.faq-nav-item').forEach(item => {
    item.addEventListener('click', () => {
      document.querySelectorAll('.faq-nav-item').forEach(i => i.classList.remove('active'));
      item.classList.add('active');
      const target = document.getElementById(item.dataset.target);
      if (target) target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
  });

  // ── PORTFOLIO FILTERS ────────────────────────────────────
  document.querySelectorAll('.filter-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const cat = btn.dataset.filter;
      document.querySelectorAll('.portfolio-item').forEach(item => {
        const show = cat === 'tous' || item.dataset.cat === cat;
        item.style.transition = 'opacity 0.3s, transform 0.3s';
        item.style.opacity = show ? '1' : '0';
        item.style.transform = show ? 'scale(1)' : 'scale(0.95)';
        item.style.pointerEvents = show ? 'auto' : 'none';
        setTimeout(() => item.style.display = show ? '' : 'none', show ? 0 : 300);
        if (show) item.style.display = '';
      });
    });
  });

  // ── SMOOTH SCROLL for anchor links ───────────────────────
  document.querySelectorAll('a[href^="#"]').forEach(a => {
    a.addEventListener('click', e => {
      const target = document.querySelector(a.getAttribute('href'));
      if (target) { e.preventDefault(); target.scrollIntoView({ behavior: 'smooth', block: 'start' }); }
    });
  });

  // ── AUTO DISMISS django messages ──────────────────────────
  document.querySelectorAll('.django-msg').forEach(msg => {
    setTimeout(() => { msg.style.opacity = '0'; setTimeout(() => msg.remove(), 400); }, 4000);
  });

});
