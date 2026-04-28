/* Centralised API client */
const API_BASE = 'http://localhost:8000';

function getToken() { return localStorage.getItem('atamasta_token'); }
function setToken(t) { localStorage.setItem('atamasta_token', t); }
function removeToken() { localStorage.removeItem('atamasta_token'); }
function getUser() { try { return JSON.parse(localStorage.getItem('atamasta_user') || 'null'); } catch { return null; } }
function setUser(u) { localStorage.setItem('atamasta_user', JSON.stringify(u)); }
function removeUser() { localStorage.removeItem('atamasta_user'); }

async function apiFetch(path, options = {}) {
  const token = getToken();
  const headers = { 'Content-Type': 'application/json', ...options.headers };
  if (token) headers['Authorization'] = `Bearer ${token}`;

  const res = await fetch(`${API_BASE}${path}`, { ...options, headers });
  if (res.status === 204) return null;
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.detail || 'Request failed');
  return data;
}

const api = {
  // Auth
  register: (body) => apiFetch('/api/auth/register', { method: 'POST', body: JSON.stringify(body) }),
  login: (body) => apiFetch('/api/auth/login', { method: 'POST', body: JSON.stringify(body) }),
  me: () => apiFetch('/api/auth/me'),
  logout() { removeToken(); removeUser(); },

  // Albums
  getAlbums: () => apiFetch('/api/albums'),
  getAlbum: (id) => apiFetch(`/api/albums/${id}`),
  createAlbum: (body) => apiFetch('/api/albums', { method: 'POST', body: JSON.stringify(body) }),
  updateAlbum: (id, body) => apiFetch(`/api/albums/${id}`, { method: 'PUT', body: JSON.stringify(body) }),
  deleteAlbum: (id) => apiFetch(`/api/albums/${id}`, { method: 'DELETE' }),
  createSong: (body) => apiFetch('/api/albums/songs', { method: 'POST', body: JSON.stringify(body) }),
  playSong: (id) => apiFetch(`/api/albums/songs/${id}/play`, { method: 'POST' }),

  // Admin
  adminGetUsers: (params = '') => apiFetch(`/api/admin/users${params ? '?' + params : ''}`),
  adminUpdateUser: (id, body) => apiFetch(`/api/admin/users/${id}`, { method: 'PATCH', body: JSON.stringify(body) }),
  adminDeleteUser: (id) => apiFetch(`/api/admin/users/${id}`, { method: 'DELETE' }),
  adminGetStats: () => apiFetch('/api/admin/stats'),
  adminGetMessages: () => apiFetch('/api/admin/messages'),
  adminMarkRead: (id) => apiFetch(`/api/admin/messages/${id}/read`, { method: 'PATCH' }),

  // Contact
  sendContact: (body) => apiFetch('/api/contact', { method: 'POST', body: JSON.stringify(body) }),
};
