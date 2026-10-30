/**
 * api.js — shared helper for all API calls
 * Projects are fetched live from the Railway backend (em-personal-os).
 * Other calls (stats, pageview, contact) go to the Render portfolio backend.
 */

const API_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
  ? 'http://localhost:5000'
  : '';   // same origin on Render — no prefix needed

const RAILWAY_URL = 'https://em-personal-os.up.railway.app';

// ── FETCH HELPERS ─────────────────────────────────────────────────────────────

async function apiGet(path) {
  try {
    const res = await fetch(API_URL + path);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return await res.json();
  } catch (err) {
    console.warn('API GET failed:', path, err);
    return null;
  }
}

async function apiPost(path, body) {
  try {
    const res = await fetch(API_URL + path, {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify(body),
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return await res.json();
  } catch (err) {
    console.warn('API POST failed:', path, err);
    return null;
  }
}

/**
 * Map a Railway project object to the shape the portfolio expects.
 * Railway: { id, project_number, title, status("complete/active/planned"),
 *            tools, github_url, live_url, description, created_at, updated_at }
 * Portfolio expects: { number, title, status("done/active/planned"),
 *                      category, type, date, tags, insights, ... }
 */
function mapRailwayProject(p) {
  const statusMap = { complete: 'done', active: 'active', planned: 'planned' };
  const num = parseInt(p.project_number, 10) || p.id;
  const dateStr = p.created_at ? p.created_at.slice(0, 7) : null; // "YYYY-MM"

  // Build tags from tools string e.g. "Python, SQL, Power BI"
  const tags = p.tools ? p.tools.split(',').map(t => t.trim()) : [];

  return {
    id:          p.id,
    number:      num,
    project_number: p.project_number,
    title:       p.title,
    status:      statusMap[p.status] || 'planned',
    category:    p.category || 'coding',
    type:        'data',
    date:        dateStr,
    date_sub:    null,
    description: p.description || null,
    problem:     p.description || null,
    what_i_did:  null,
    tools:       p.tools || '',
    tags:        tags,
    insights:    [],
    chart_image: null,
    github_url:  p.github_url || null,
    kaggle_url:  null,
    live_url:    p.live_url || null,
    powerbi_url: null,
  };
}

// ── PUBLIC API ────────────────────────────────────────────────────────────────

const API = {

  /** Fetch all projects live from Railway, mapped to portfolio shape */
  async getProjects(filters = {}) {
    try {
      const res = await fetch(RAILWAY_URL + '/projects/public');
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      let projects = data.map(mapRailwayProject);

      // Apply optional filters (status, category)
      if (filters.status)   projects = projects.filter(p => p.status   === filters.status);
      if (filters.category) projects = projects.filter(p => p.category === filters.category);

      return projects;
    } catch (err) {
      console.warn('Railway projects fetch failed:', err);
      return null;
    }
  },

  /** Fetch live stats (views, visitors, project counts) */
  getStats() {
    return apiGet('/api/stats');
  },

  /** Log a page view — call once per page load */
  logPageView(page) {
    return apiPost('/api/pageview', { page });
  },

  /** Save a contact form submission */
  submitContact(name, email, message) {
    return apiPost('/api/contact', { name, email, message });
  },
};