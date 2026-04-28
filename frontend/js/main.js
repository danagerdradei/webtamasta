/* ── Main page JS ─────────────────────────────────────────────────────────── */
document.addEventListener('DOMContentLoaded', async () => {
  initNavbar();
  updateNavAuth();
  initScrollReveal();
  initParticles('hero-particles');

  // Resize canvas to hero section
  const canvas = document.getElementById('hero-particles');
  if (canvas) {
    const hero = document.getElementById('hero');
    canvas.style.width = '100%';
    canvas.style.height = '100%';
  }

  // Smooth scroll for anchor links
  document.querySelectorAll('a[href^="#"]').forEach(a => {
    a.addEventListener('click', e => {
      const target = document.querySelector(a.getAttribute('href'));
      if (target) { e.preventDefault(); target.scrollIntoView({ behavior: 'smooth' }); }
    });
  });

  // Active nav link on scroll
  const sections = document.querySelectorAll('section[id]');
  const navLinks = document.querySelectorAll('.nav-links a');
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        navLinks.forEach(a => a.classList.remove('active'));
        const link = document.querySelector(`.nav-links a[href="#${entry.target.id}"]`);
        if (link) link.classList.add('active');
      }
    });
  }, { threshold: 0.4 });
  sections.forEach(s => observer.observe(s));

  await loadAlbums();
  initContactForm();

  setTimeout(() => hideLoader(), 600);
});

/* ── Albums & Player ──────────────────────────────────────────────────────── */
let albums = [];
let currentAlbumIndex = 0;
let currentTrackIndex = 0;
let isPlaying = false;
const audio = document.getElementById('audio-player');

async function loadAlbums() {
  try {
    albums = await api.getAlbums();
    renderAlbumGrid();
    renderAlbumTabs();
    renderVideoGrid();

    const totalSongs = albums.reduce((s, a) => s + (a.songs ? a.songs.length : 0), 0);
    document.getElementById('stat-albums').textContent = albums.length;
    document.getElementById('stat-songs').textContent = totalSongs + '+';
  } catch (err) {
    console.error('Failed to load albums:', err);
    document.getElementById('albums-grid').innerHTML = `
      <div style="color:var(--text-muted); text-align:center; grid-column:1/-1; padding:3rem;">
        <i class="fas fa-exclamation-triangle" style="color:var(--gold); font-size:2rem; margin-bottom:1rem; display:block;"></i>
        No se pudo conectar con el servidor. Verifica que el backend está corriendo.
      </div>`;
  }
}

function renderAlbumGrid() {
  const grid = document.getElementById('albums-grid');
  if (!albums.length) { grid.innerHTML = '<p style="color:var(--text-muted); grid-column:1/-1; text-align:center;">Sin álbumes disponibles</p>'; return; }

  grid.innerHTML = albums.map((album, i) => `
    <div class="album-card reveal" data-album-index="${i}" onclick="selectAlbum(${i})">
      ${album.is_premium ? '<div class="album-premium-badge"><i class="fas fa-crown"></i> Premium</div>' : ''}
      <div class="album-cover-wrap">
        <img src="${album.cover_url || 'assets/images/album-placeholder.jpg'}" alt="${album.title}" loading="lazy"
             onerror="this.src='https://via.placeholder.com/400x400/111111/d4a017?text=${encodeURIComponent(album.title)}'" />
        <div class="album-overlay">
          <button class="album-play-btn" onclick="event.stopPropagation(); selectAlbum(${i}); playTrack(0)">
            <i class="fas fa-play"></i>
          </button>
        </div>
      </div>
      <div class="album-info">
        <div class="album-title">${album.title}</div>
        <div class="album-year">${album.year}</div>
        <div class="album-track-count">${album.songs ? album.songs.length : 0} canciones</div>
      </div>
    </div>
  `).join('');

  initScrollReveal();
}

function renderAlbumTabs() {
  const tabs = document.getElementById('album-tabs');
  if (!albums.length) return;
  tabs.innerHTML = albums.map((a, i) => `
    <button class="btn ${i === 0 ? 'btn-primary' : 'btn-secondary'} btn-sm" onclick="selectAlbum(${i})" data-tab="${i}">
      ${a.is_premium ? '<i class="fas fa-crown"></i> ' : ''}${a.title}
    </button>
  `).join('');
  selectAlbum(0);
}

function selectAlbum(index) {
  currentAlbumIndex = index;
  const album = albums[index];
  if (!album) return;

  document.querySelectorAll('#album-tabs button').forEach((btn, i) => {
    btn.className = `btn ${i === index ? 'btn-primary' : 'btn-secondary'} btn-sm`;
  });

  const playerSection = document.getElementById('player-section');
  playerSection.style.display = 'block';

  const cover = album.cover_url || `https://via.placeholder.com/80x80/111111/d4a017?text=${encodeURIComponent(album.title)}`;
  document.getElementById('player-cover').src = cover;
  document.getElementById('player-album-name').textContent = album.title + ' (' + album.year + ')';
  document.getElementById('player-song-title').textContent = 'Selecciona una canción';

  const premiumNotice = document.getElementById('premium-notice');
  const user = getUser();
  const hasAccess = !album.is_premium || (user && (user.role === 'premium' || user.role === 'admin'));

  if (album.is_premium && !hasAccess) {
    premiumNotice.style.display = 'block';
    document.getElementById('track-list').innerHTML = `
      <li style="padding:2rem; text-align:center; color:var(--text-muted);">
        <i class="fas fa-lock" style="color:var(--gold); display:block; font-size:1.5rem; margin-bottom:0.5rem;"></i>
        Contenido premium — Inicia sesión para acceder
      </li>`;
    return;
  }

  premiumNotice.style.display = 'none';
  renderTrackList(album, hasAccess);
}

function renderTrackList(album, hasAccess) {
  const list = document.getElementById('track-list');
  if (!album.songs || !album.songs.length) {
    list.innerHTML = '<li style="padding:1.5rem; color:var(--text-muted); text-align:center;">Sin pistas disponibles</li>';
    return;
  }

  list.innerHTML = album.songs.map((song, i) => {
    const locked = song.is_premium && !hasAccess;
    return `
      <li class="track-item ${locked ? 'locked' : ''}" data-track="${i}" onclick="${locked ? 'showPremiumAlert()' : `playTrack(${i})`}">
        <span class="track-num">${song.track_number}</span>
        <span class="track-title">${song.title}</span>
        <span class="track-duration">${song.duration || '—'}</span>
        ${locked
          ? '<span class="track-premium-lock"><i class="fas fa-lock"></i></span>'
          : (song.youtube_embed_id ? `<button class="ctrl-btn btn-sm" onclick="event.stopPropagation(); openVideoModal('${song.youtube_embed_id}', '${song.title.replace(/'/g,"\\'")}')"><i class="fas fa-film"></i></button>` : '<span></span>')
        }
      </li>
    `;
  }).join('');
}

function playTrack(trackIndex) {
  const album = albums[currentAlbumIndex];
  if (!album || !album.songs) return;
  const song = album.songs[trackIndex];
  if (!song) return;

  const user = getUser();
  const hasAccess = !song.is_premium || (user && (user.role === 'premium' || user.role === 'admin'));
  if (!hasAccess) { showPremiumAlert(); return; }

  currentTrackIndex = trackIndex;
  document.querySelectorAll('.track-item').forEach((el, i) => el.classList.toggle('active', i === trackIndex));

  document.getElementById('player-song-title').textContent = song.title;

  if (song.audio_url) {
    audio.src = song.audio_url;
    audio.play().then(() => { isPlaying = true; updatePlayIcon(); }).catch(() => {});
  } else if (song.youtube_embed_id) {
    isPlaying = false;
    updatePlayIcon();
    openVideoModal(song.youtube_embed_id, song.title);
  } else {
    toast('Sin audio disponible para esta canción', 'info');
    return;
  }

  const videoBtn = document.getElementById('btn-video');
  videoBtn.style.display = song.youtube_embed_id ? 'flex' : 'none';
  videoBtn.onclick = () => openVideoModal(song.youtube_embed_id, song.title);

  api.playSong(song.id).catch(() => {});
}

function updatePlayIcon() {
  const icon = document.getElementById('play-icon');
  icon.className = isPlaying ? 'fas fa-pause' : 'fas fa-play';
}

function showPremiumAlert() {
  toast('Contenido exclusivo para miembros premium. ¡Regístrate gratis!', 'info');
}

// Player controls
document.getElementById('btn-play')?.addEventListener('click', () => {
  if (isPlaying) { audio.pause(); isPlaying = false; }
  else if (audio.src) { audio.play(); isPlaying = true; }
  else { const album = albums[currentAlbumIndex]; if (album?.songs?.length) playTrack(0); }
  updatePlayIcon();
});

document.getElementById('btn-prev')?.addEventListener('click', () => {
  const album = albums[currentAlbumIndex];
  if (!album?.songs?.length) return;
  playTrack((currentTrackIndex - 1 + album.songs.length) % album.songs.length);
});

document.getElementById('btn-next')?.addEventListener('click', () => {
  const album = albums[currentAlbumIndex];
  if (!album?.songs?.length) return;
  playTrack((currentTrackIndex + 1) % album.songs.length);
});

audio?.addEventListener('ended', () => {
  const album = albums[currentAlbumIndex];
  if (album?.songs && currentTrackIndex < album.songs.length - 1) playTrack(currentTrackIndex + 1);
  else { isPlaying = false; updatePlayIcon(); }
});

audio?.addEventListener('timeupdate', () => {
  if (!audio.duration) return;
  const pct = (audio.currentTime / audio.duration) * 100;
  document.getElementById('progress-fill').style.width = pct + '%';
  document.getElementById('time-current').textContent = formatDuration(audio.currentTime);
  document.getElementById('time-total').textContent = formatDuration(audio.duration);
});

document.getElementById('progress-bar')?.addEventListener('click', e => {
  if (!audio.duration) return;
  const rect = e.currentTarget.getBoundingClientRect();
  audio.currentTime = ((e.clientX - rect.left) / rect.width) * audio.duration;
});

/* ── Videos ──────────────────────────────────────────────────────────────── */
const YOUTUBE_VIDEOS = [
  { id: 'RapresentMNZ', title: 'Rapresent ft. MNZ (Video Oficial)', views: '6.9K', embedId: 'placeholder' },
  { id: 'NordafackazVid', title: 'Nordafackaz #1 (North Down Clica)', views: '1.9K', embedId: 'placeholder2' },
  { id: 'MolotovRocket', title: 'Molotov Rocket (Home Version)', views: '3.2K', embedId: 'placeholder3' },
  { id: 'Boombapkistan', title: 'Boombapkistan', views: '1.5K', embedId: 'placeholder4' },
  { id: 'PoloNorte', title: 'Polo Norte ft Ermitaño Mental', views: '1.7K', embedId: 'placeholder5' },
  { id: 'HomuraDamma', title: 'Homura Damma ft Da Flava', views: '1.5K', embedId: 'placeholder6' },
];

function renderVideoGrid() {
  const grid = document.getElementById('video-grid');
  const allSongs = albums.flatMap(a => a.songs || []).filter(s => s.youtube_embed_id);

  const videoData = allSongs.length ? allSongs : YOUTUBE_VIDEOS;

  grid.innerHTML = videoData.map(song => `
    <div class="video-card reveal">
      <div class="video-thumb-wrap" style="cursor:pointer;" onclick="openVideoModal('${song.youtube_embed_id || song.embedId}', '${(song.title || '').replace(/'/g,"\\'")}')">
        <img
          src="https://img.youtube.com/vi/${song.youtube_embed_id || song.embedId}/maxresdefault.jpg"
          alt="${song.title}"
          onerror="this.src='https://via.placeholder.com/480x270/111111/d4a017?text=VIDEO'"
          style="width:100%;height:100%;object-fit:cover;position:absolute;inset:0;"
        />
        <div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;background:rgba(0,0,0,0.3);transition:background 0.3s;" onmouseover="this.style.background='rgba(0,0,0,0.1)'" onmouseout="this.style.background='rgba(0,0,0,0.3)'">
          <div style="width:56px;height:56px;border-radius:50%;background:var(--gold);display:flex;align-items:center;justify-content:center;color:#000;font-size:1.4rem;">
            <i class="fas fa-play" style="margin-left:4px;"></i>
          </div>
        </div>
      </div>
      <div class="video-info">
        <div class="video-title">${song.title}</div>
        ${song.play_count !== undefined ? `<div class="video-views">${song.play_count} reproducciones</div>` : (song.views ? `<div class="video-views">${song.views} visualizaciones</div>` : '')}
      </div>
    </div>
  `).join('');
  initScrollReveal();
}

/* ── Video Modal ─────────────────────────────────────────────────────────── */
function openVideoModal(embedId, title) {
  const modal = document.getElementById('video-modal');
  const iframe = document.getElementById('video-modal-iframe');
  const titleEl = document.getElementById('video-modal-title');

  if (!embedId || embedId.startsWith('placeholder')) {
    toast('Video no disponible aún', 'info');
    return;
  }

  titleEl.textContent = title;
  iframe.src = `https://www.youtube.com/embed/${embedId}?autoplay=1`;
  modal.classList.add('open');
}

document.getElementById('video-modal-close')?.addEventListener('click', closeVideoModal);
document.getElementById('video-modal')?.addEventListener('click', e => { if (e.target === e.currentTarget) closeVideoModal(); });

function closeVideoModal() {
  const modal = document.getElementById('video-modal');
  const iframe = document.getElementById('video-modal-iframe');
  modal.classList.remove('open');
  iframe.src = '';
}

document.addEventListener('keydown', e => { if (e.key === 'Escape') closeVideoModal(); });

/* ── Contact Form ────────────────────────────────────────────────────────── */
function initContactForm() {
  const form = document.getElementById('contact-form');
  if (!form) return;

  form.addEventListener('submit', async e => {
    e.preventDefault();
    const btn = document.getElementById('contact-submit');
    const alertEl = document.getElementById('contact-alert');
    const data = Object.fromEntries(new FormData(form).entries());

    if (!data.name || !data.email || !data.subject || !data.message) {
      alertEl.innerHTML = '<div class="alert alert-error"><i class="fas fa-exclamation-circle"></i> Completa todos los campos</div>';
      return;
    }

    btn.disabled = true;
    btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Enviando...';
    alertEl.innerHTML = '';

    try {
      await api.sendContact(data);
      alertEl.innerHTML = '<div class="alert alert-success"><i class="fas fa-check-circle"></i> ¡Mensaje enviado! Te responderemos pronto.</div>';
      form.reset();
    } catch (err) {
      alertEl.innerHTML = `<div class="alert alert-error"><i class="fas fa-times-circle"></i> ${err.message}</div>`;
    } finally {
      btn.disabled = false;
      btn.innerHTML = '<i class="fas fa-paper-plane"></i> Enviar mensaje';
    }
  });
}
