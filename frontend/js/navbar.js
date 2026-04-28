/* Shared navbar injector — call initSharedNavbar() on every page */

/* Logo SVG inline — profile warrior (simplified for small sizes) */
const ATAMASTA_LOGO_SVG = `<svg width="38" height="38" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <g id="gkn">
      <rect x="182" y="95" width="14" height="2.2" fill="#d4a017"/>
      <rect x="193.8" y="97.2" width="2.2" height="5" fill="#d4a017"/>
      <rect x="182" y="99.8" width="11.8" height="2.2" fill="#d4a017"/>
      <rect x="182" y="95" width="2.2" height="7" fill="#d4a017"/>
    </g>
  </defs>
  <circle cx="100" cy="100" r="99" fill="#090909"/>
  <use href="#gkn" transform="rotate(0 100 100)"/><use href="#gkn" transform="rotate(20 100 100)"/>
  <use href="#gkn" transform="rotate(40 100 100)"/><use href="#gkn" transform="rotate(60 100 100)"/>
  <use href="#gkn" transform="rotate(80 100 100)"/><use href="#gkn" transform="rotate(100 100 100)"/>
  <use href="#gkn" transform="rotate(120 100 100)"/><use href="#gkn" transform="rotate(140 100 100)"/>
  <use href="#gkn" transform="rotate(160 100 100)"/><use href="#gkn" transform="rotate(180 100 100)"/>
  <use href="#gkn" transform="rotate(200 100 100)"/><use href="#gkn" transform="rotate(220 100 100)"/>
  <use href="#gkn" transform="rotate(240 100 100)"/><use href="#gkn" transform="rotate(260 100 100)"/>
  <use href="#gkn" transform="rotate(280 100 100)"/><use href="#gkn" transform="rotate(300 100 100)"/>
  <use href="#gkn" transform="rotate(320 100 100)"/><use href="#gkn" transform="rotate(340 100 100)"/>
  <circle cx="100" cy="100" r="98" fill="none" stroke="#d4a017" stroke-width="1.5"/>
  <circle cx="100" cy="100" r="82" fill="none" stroke="#d4a017" stroke-width="1"/>
  <circle cx="100" cy="100" r="81.5" fill="#090909"/>
  <path fill="#d4a017" d="M115,39 L118,45 L122,55 L124,65 L124,75 L123,85 L122,95 L120,105 L118,115 L114,125 L108,133 L100,137 L90,133 L84,125 L83,118 L81,110 L79,106 L75,102 L76,99 L78,97 L74,94 L71,90 L75,86 L79,82 L83,78 L86,73 L87,67 L88,61 L88,51 L88,41 L91,37 L95,39 L100,36 L104,39 L109,40 L112,38 Z"/>
  <rect x="87" y="70" width="38" height="8" rx="2" fill="#d4a017"/>
  <rect x="87" y="72" width="38" height="3" rx="1" fill="#a07010"/>
  <circle cx="92" cy="91" r="5.5" fill="#d4a017"/>
  <circle cx="92" cy="91" r="3" fill="#090909"/>
</svg>`;

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
      ${ATAMASTA_LOGO_SVG}
      <span class="nav-logo-text">ATA<span>MASTA</span></span>
    </a>
    <ul class="nav-links" id="nav-links">
      <li><a href="${root}index.html" data-page="home"><i class="fas fa-home"></i> Inicio</a></li>
      <li><a href="${pages}about.html" data-page="about"><i class="fas fa-user"></i> Artista</a></li>
      <li><a href="${pages}discography.html" data-page="discography"><i class="fas fa-compact-disc"></i> Discografía</a></li>
      <li><a href="${pages}music.html" data-page="music"><i class="fas fa-headphones"></i> Música</a></li>
      <li><a href="${pages}videos.html" data-page="videos"><i class="fas fa-film"></i> Videos</a></li>
      <li><a href="${pages}contact.html" data-page="contact"><i class="fas fa-envelope"></i> Contacto</a></li>
    </ul>
    <div class="nav-auth" id="nav-auth"></div>
    <button class="hamburger" id="hamburger" aria-label="Menú">
      <span></span><span></span><span></span>
    </button>
  </div>
</nav>`;
}

function initSharedNavbar(currentPage = '', isSubPage = false) {
  // Inject navbar at top of body
  document.body.insertAdjacentHTML('afterbegin', buildNavbarHTML(isSubPage));

  // Highlight active page
  if (currentPage) {
    const activeLink = document.querySelector(`[data-page="${currentPage}"]`);
    if (activeLink) activeLink.classList.add('active');
  }

  initNavbar();
  updateNavAuth();
}
