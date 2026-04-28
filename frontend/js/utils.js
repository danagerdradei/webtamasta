/* Shared utilities */

function toast(message, type = 'info') {
  const container = document.getElementById('toast-container') || (() => {
    const c = document.createElement('div');
    c.id = 'toast-container';
    c.className = 'toast-container';
    document.body.appendChild(c);
    return c;
  })();

  const icons = { success: 'fa-check-circle', error: 'fa-times-circle', info: 'fa-info-circle' };
  const t = document.createElement('div');
  t.className = `toast ${type}`;
  t.innerHTML = `<i class="fas ${icons[type] || icons.info}"></i><span>${message}</span>`;
  container.appendChild(t);
  setTimeout(() => { t.style.opacity = '0'; t.style.transform = 'translateX(40px)'; t.style.transition = '0.3s'; setTimeout(() => t.remove(), 300); }, 3500);
}

function showLoader() {
  const el = document.getElementById('page-loader');
  if (el) { el.classList.remove('hidden'); }
}
function hideLoader() {
  const el = document.getElementById('page-loader');
  if (el) { el.classList.add('hidden'); }
}

function initScrollReveal() {
  const els = document.querySelectorAll('.reveal');
  if (!els.length) return;
  const obs = new IntersectionObserver((entries) => {
    entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('visible'); obs.unobserve(e.target); } });
  }, { threshold: 0.1 });
  els.forEach(el => obs.observe(el));
}

function initNavbar() {
  const nav = document.getElementById('navbar');
  if (!nav) return;
  const onScroll = () => nav.classList.toggle('scrolled', window.scrollY > 60);
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  const hamburger = document.getElementById('hamburger');
  const navLinks = document.getElementById('nav-links');
  if (hamburger && navLinks) {
    hamburger.addEventListener('click', () => {
      hamburger.classList.toggle('open');
      navLinks.classList.toggle('open');
    });
    navLinks.querySelectorAll('a').forEach(a => a.addEventListener('click', () => {
      hamburger.classList.remove('open');
      navLinks.classList.remove('open');
    }));
  }
}

function updateNavAuth() {
  const user = getUser();
  const authArea = document.getElementById('nav-auth');
  if (!authArea) return;

  if (user) {
    const initial = user.username ? user.username[0].toUpperCase() : 'U';
    authArea.innerHTML = `
      <div class="nav-user">
        <div class="avatar">${initial}</div>
        <span>${user.username}</span>
        ${user.role === 'admin' ? '<span class="badge badge-admin">Admin</span>' : user.role === 'premium' ? '<span class="badge badge-premium">Premium</span>' : ''}
      </div>
      ${user.role === 'admin' ? '<a href="admin.html" class="btn btn-secondary btn-sm">Panel</a>' : ''}
      <button class="btn btn-sm" style="background:var(--bg3);color:var(--text-muted);" onclick="handleLogout()">Salir</button>
    `;
  } else {
    authArea.innerHTML = `
      <a href="pages/login.html" class="btn btn-secondary btn-sm">Iniciar sesión</a>
      <a href="pages/register.html" class="btn btn-primary btn-sm">Registrarse</a>
    `;
  }
}

function handleLogout() {
  api.logout();
  toast('Sesión cerrada', 'info');
  setTimeout(() => { window.location.href = '/'; }, 800);
}

function requireAuth(redirectTo = 'login.html') {
  const token = getToken();
  if (!token) {
    window.location.href = redirectTo;
    return null;
  }
  return getUser();
}

function requireAdmin() {
  const user = requireAuth('login.html');
  if (user && user.role !== 'admin') {
    toast('Acceso denegado: solo administradores', 'error');
    setTimeout(() => { window.location.href = '../index.html'; }, 1200);
    return null;
  }
  return user;
}

function formatDuration(seconds) {
  const m = Math.floor(seconds / 60);
  const s = Math.floor(seconds % 60);
  return `${m}:${s.toString().padStart(2, '0')}`;
}

function formatDate(isoString) {
  if (!isoString) return '—';
  return new Date(isoString).toLocaleDateString('es-CO', { day: 'numeric', month: 'short', year: 'numeric' });
}

function initParticles(canvasId) {
  const canvas = document.getElementById(canvasId);
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  let particles = [];

  function resize() {
    canvas.width = canvas.offsetWidth;
    canvas.height = canvas.offsetHeight;
  }
  window.addEventListener('resize', resize);
  resize();

  for (let i = 0; i < 60; i++) {
    particles.push({
      x: Math.random() * canvas.width,
      y: Math.random() * canvas.height,
      r: Math.random() * 1.5 + 0.3,
      vx: (Math.random() - 0.5) * 0.3,
      vy: (Math.random() - 0.5) * 0.3,
      opacity: Math.random() * 0.5 + 0.1,
    });
  }

  function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    particles.forEach(p => {
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(212,160,23,${p.opacity})`;
      ctx.fill();
      p.x += p.vx; p.y += p.vy;
      if (p.x < 0 || p.x > canvas.width) p.vx *= -1;
      if (p.y < 0 || p.y > canvas.height) p.vy *= -1;
    });
    requestAnimationFrame(draw);
  }
  draw();
}
