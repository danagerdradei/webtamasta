/* Centralised API client */
const API_BASE = 'http://localhost:8000';

function getToken() { return localStorage.getItem('latintunes_token'); }
function setToken(t) { localStorage.setItem('latintunes_token', t); }
function removeToken() { localStorage.removeItem('latintunes_token'); }
function getUser() { try { return JSON.parse(localStorage.getItem('latintunes_user') || 'null'); } catch { return null; } }
function setUser(u) { localStorage.setItem('latintunes_user', JSON.stringify(u)); }
function removeUser() { localStorage.removeItem('latintunes_user'); }

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

  // Beats
  getBeats: (params = '') => apiFetch(`/api/beats${params ? '?' + params : ''}`),
  getBeat: (id) => apiFetch(`/api/beats/${id}`),
  getCategories: () => apiFetch('/api/beats/categories'),
  createBeat: (body) => apiFetch('/api/beats', { method: 'POST', body: JSON.stringify(body) }),
  updateBeat: (id, body) => apiFetch(`/api/beats/${id}`, { method: 'PUT', body: JSON.stringify(body) }),
  deleteBeat: (id) => apiFetch(`/api/beats/${id}`, { method: 'DELETE' }),
  playBeat: (id) => apiFetch(`/api/beats/${id}/play`, { method: 'POST' }),

  // Services
  getServices: (activeOnly = true) => apiFetch(`/api/services?active_only=${activeOnly}`),
  getService: (id) => apiFetch(`/api/services/${id}`),
  getServiceCategories: () => apiFetch('/api/services/categories'),
  createService: (body) => apiFetch('/api/services', { method: 'POST', body: JSON.stringify(body) }),
  updateService: (id, body) => apiFetch(`/api/services/${id}`, { method: 'PUT', body: JSON.stringify(body) }),
  deleteService: (id) => apiFetch(`/api/services/${id}`, { method: 'DELETE' }),

  // Packages
  getPackages: (activeOnly = true) => apiFetch(`/api/services/packages/all?active_only=${activeOnly}`),
  createPackage: (body) => apiFetch('/api/services/packages', { method: 'POST', body: JSON.stringify(body) }),
  updatePackage: (id, body) => apiFetch(`/api/services/packages/${id}`, { method: 'PUT', body: JSON.stringify(body) }),
  deletePackage: (id) => apiFetch(`/api/services/packages/${id}`, { method: 'DELETE' }),

  // Equipment
  getEquipment: (availableOnly = false) => apiFetch(`/api/equipment?available_only=${availableOnly}`),
  getEquipmentItem: (id) => apiFetch(`/api/equipment/${id}`),
  getEquipmentCategories: () => apiFetch('/api/equipment/categories'),
  createEquipment: (body) => apiFetch('/api/equipment', { method: 'POST', body: JSON.stringify(body) }),
  updateEquipment: (id, body) => apiFetch(`/api/equipment/${id}`, { method: 'PUT', body: JSON.stringify(body) }),
  deleteEquipment: (id) => apiFetch(`/api/equipment/${id}`, { method: 'DELETE' }),

  // Bookings
  createBooking: (body) => apiFetch('/api/bookings', { method: 'POST', body: JSON.stringify(body) }),
  adminGetBookings: (status = '') => apiFetch(`/api/bookings${status ? '?status=' + status : ''}`),
  adminUpdateBooking: (id, body) => apiFetch(`/api/bookings/${id}`, { method: 'PATCH', body: JSON.stringify(body) }),
  adminDeleteBooking: (id) => apiFetch(`/api/bookings/${id}`, { method: 'DELETE' }),

  // Licenses
  adminGetLicenses: (status = '') => apiFetch(`/api/licenses${status ? '?status=' + status : ''}`),
  getLicense: (id) => apiFetch(`/api/licenses/${id}`),
  verifyLicense: (number) => apiFetch(`/api/licenses/verify/${number}`),
  createLicense: (body) => apiFetch('/api/licenses', { method: 'POST', body: JSON.stringify(body) }),
  updateLicense: (id, body) => apiFetch(`/api/licenses/${id}`, { method: 'PATCH', body: JSON.stringify(body) }),
  deleteLicense: (id) => apiFetch(`/api/licenses/${id}`, { method: 'DELETE' }),
};
