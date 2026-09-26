from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from database import init_db, get_db
import datetime
import hashlib
import json
import os

app = Flask(__name__, static_folder='static', static_url_path='/static')
CORS(app)

init_db()

# ── SERVE STATIC HTML FILES ──────────────────────────────────────────────────

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/index.html')
def home_html():
    return send_from_directory('.', 'index.html')

@app.route('/project')
def project():
    return send_from_directory('.', 'project.html')

@app.route('/project.html')
def project_html():
    return send_from_directory('.', 'project.html')

@app.route('/projects.html')
def projects_html():
    return send_from_directory('.', 'project.html')

@app.route('/static/js/api.js')
def serve_api_js():
    return send_from_directory('static/js', 'api.js')

@app.route('/images/<path:filename>')
def images(filename):
    return send_from_directory('images', filename)

# ── API: PROJECTS ─────────────────────────────────────────────────────────────

@app.route('/api/projects', methods=['GET'])
def get_projects():
    status   = request.args.get('status')
    category = request.args.get('category')

    db = get_db()
    query  = 'SELECT * FROM projects'
    params = []
    filters = []

    if status:
        filters.append('status = ?')
        params.append(status)
    if category:
        filters.append('type = ?')
        params.append(category)
    if filters:
        query += ' WHERE ' + ' AND '.join(filters)

    query += ' ORDER BY number'
    rows = db.execute(query, params).fetchall()
    db.close()

    projects = []
    for row in rows:
        p = dict(row)
        p['insights'] = json.loads(p['insights'] or '[]')
        p['tags']     = json.loads(p['tags']     or '[]')
        projects.append(p)

    return jsonify(projects)


@app.route('/api/projects/<int:project_id>', methods=['GET'])
def get_project(project_id):
    db  = get_db()
    row = db.execute('SELECT * FROM projects WHERE id = ?', [project_id]).fetchone()
    db.close()
    if row is None:
        return jsonify({'error': 'Not found'}), 404
    p = dict(row)
    p['insights'] = json.loads(p['insights'] or '[]')
    p['tags']     = json.loads(p['tags']     or '[]')
    return jsonify(p)

# ── API: PAGE VIEWS ──────────────────────────────────────────────────────────

@app.route('/api/pageview', methods=['POST'])
def log_pageview():
    data    = request.get_json() or {}
    page    = data.get('page', 'unknown')
    ip      = request.remote_addr or 'unknown'
    ip_hash = hashlib.md5(ip.encode()).hexdigest()
    ts      = datetime.datetime.utcnow().isoformat()

    db = get_db()
    db.execute(
        'INSERT INTO pageviews (page, ip_hash, timestamp) VALUES (?, ?, ?)',
        [page, ip_hash, ts]
    )
    db.commit()
    db.close()
    return jsonify({'status': 'ok'})

# ── API: CONTACT ─────────────────────────────────────────────────────────────

@app.route('/api/contact', methods=['POST'])
def save_contact():
    data    = request.get_json() or {}
    name    = data.get('name', '').strip()
    email   = data.get('email', '').strip()
    message = data.get('message', '').strip()

    if not name or not email or not message:
        return jsonify({'error': 'All fields required'}), 400

    db = get_db()
    db.execute(
        'INSERT INTO contacts (name, email, message, timestamp) VALUES (?, ?, ?, ?)',
        [name, email, message, datetime.datetime.utcnow().isoformat()]
    )
    db.commit()
    db.close()
    return jsonify({'status': 'ok', 'message': 'Message saved!'})

# ── API: STATS ────────────────────────────────────────────────────────────────

@app.route('/api/stats', methods=['GET'])
def get_stats():
    db = get_db()

    total_views     = db.execute('SELECT COUNT(*) FROM pageviews').fetchone()[0]
    unique_visitors = db.execute('SELECT COUNT(DISTINCT ip_hash) FROM pageviews').fetchone()[0]
    project_count   = db.execute('SELECT COUNT(*) FROM projects').fetchone()[0]
    done_count      = db.execute("SELECT COUNT(*) FROM projects WHERE status='done'").fetchone()[0]
    active_count    = db.execute("SELECT COUNT(*) FROM projects WHERE status='active'").fetchone()[0]
    planned_count   = db.execute("SELECT COUNT(*) FROM projects WHERE status='planned'").fetchone()[0]

    db.close()

    return jsonify({
        'total_views':      total_views,
        'unique_visitors':  unique_visitors,
        'project_count':    project_count,
        'done_count':       done_count,
        'active_count':     active_count,
        'planned_count':    planned_count,
        'rows_analysed':    361302,
        'github_repos':     2,
        'kaggle_notebooks': 9,
    })

# ── ADMIN: CONTACTS ───────────────────────────────────────────────────────────

@app.route('/api/admin/contacts', methods=['GET'])
def get_contacts():
    secret = request.args.get('key', '')
    if secret != os.environ.get('ADMIN_KEY', 'changeme'):
        return jsonify({'error': 'Unauthorized'}), 401

    db   = get_db()
    rows = db.execute('SELECT * FROM contacts ORDER BY timestamp DESC').fetchall()
    db.close()
    return jsonify([dict(r) for r in rows])

# ─────────────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    app.run(debug=True, port=5000)