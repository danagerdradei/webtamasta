/* Shared navbar injector — call initSharedNavbar() on every page */

function getNavPaths(isSubPage) {
  const p = isSubPage ? '../' : '';
  const pp = isSubPage ? '' : 'pages/';
  return { root: p, pages: pp };
}

function buildNavbarHTML(isSubPage = false) {
  const { root, pages } = getNavPaths(isSubPage);
  return `
<nav class="navbar" id="navbar">
  <div class="container">
    <a href="${root}index.html" class="nav-logo-wrap">
      <img src="${root}img/LatinTunes.jpeg" alt="LatinTunes"
        style="width:38px;height:38px;border-radius:50%;display:block;flex-shrink:0;object-fit:cover;" />
      <span class="nav-logo-text">LATIN<span>TUNES</span></span>
    </a>
    <ul class="nav-links" id="nav-links">
      <li><a href="${root}index.html"          data-page="home"><i class="fas fa-home"></i> Inicio</a></li>
      <li><a href="${pages}services.html"       data-page="services"><i class="fas fa-music"></i> Servicios</a></li>
      <li><a href="${pages}booking.html"        data-page="booking"><i class="fas fa-calendar-check"></i> Reservar</a></li>
      <li><a href="${pages}beats.html"          data-page="beats"><i class="fas fa-drum"></i> Beats</a></li>
      <li><a href="${pages}equipment.html"      data-page="equipment"><i class="fas fa-microphone"></i> Equipos</a></li>
      <li><a href="${pages}packages.html"       data-page="packages"><i class="fas fa-tags"></i> Paquetes</a></li>
      <li><a href="${pages}about.html"          data-page="about"><i class="fas fa-building"></i> Nosotros</a></li>
      <li><a href="${pages}contact.html"        data-page="contact"><i class="fas fa-envelope"></i> Contacto</a></li>
      <li class="nav-mobile-auth" id="nav-mobile-auth"></li>
    </ul>
    <div class="nav-auth" id="nav-auth"></div>
    <button class="hamburger" id="hamburger" aria-label="Menú">
      <span></span><span></span><span></span>
    </button>
  </div>
</nav>`;
}

function initSharedNavbar(currentPage = '', isSubPage = false) {
  document.body.insertAdjacentHTML('afterbegin', buildNavbarHTML(isSubPage));
  if (currentPage) {
    const activeLink = document.querySelector(`[data-page="${currentPage}"]`);
    if (activeLink) activeLink.classList.add('active');
  }
  initNavbar();
  updateNavAuth();
}
