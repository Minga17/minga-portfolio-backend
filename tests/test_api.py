"""Tests for the portfolio backend API."""
import json
import os
import pytest

# Set up test environment before importing app
os.environ['ADMIN_KEY'] = 'test-key'

from app import app, init_db, get_db, safe_json_loads
import database


@pytest.fixture
def client(tmp_path):
    """Create a test client with isolated SQLite database."""
    app.config['TESTING'] = True
    test_db = str(tmp_path / 'test_portfolio.db')
    database.DATABASE = test_db
    init_db()
    with app.test_client() as client:
        yield client


def test_home_page(client):
    """GET / should return 200."""
    rv = client.get('/')
    assert rv.status_code == 200


def test_project_page(client):
    """GET /project should return 200."""
    rv = client.get('/project')
    assert rv.status_code == 200


def test_media_page(client):
    """GET /media should return 200."""
    rv = client.get('/media')
    assert rv.status_code == 200


def test_projects_api(client):
    """GET /api/projects should return JSON list."""
    rv = client.get('/api/projects')
    assert rv.status_code == 200
    data = rv.get_json()
    assert isinstance(data, list)


def test_projects_api_filtered(client):
    """GET /api/projects with filters should return JSON list."""
    rv = client.get('/api/projects?status=done&category=data')
    assert rv.status_code == 200
    data = rv.get_json()
    assert isinstance(data, list)


def test_project_detail_api(client):
    """GET /api/projects/1 should return a project or 404."""
    rv = client.get('/api/projects/1')
    assert rv.status_code in (200, 404)
    if rv.status_code == 200:
        data = rv.get_json()
        assert 'id' in data


def test_stats_api(client):
    """GET /api/stats should return stats dict."""
    rv = client.get('/api/stats')
    assert rv.status_code == 200
    data = rv.get_json()
    assert 'total_views' in data
    assert 'project_count' in data


def test_pageview_api(client):
    """POST /api/pageview should log a view."""
    rv = client.post('/api/pageview',
                     data=json.dumps({'page': 'home'}),
                     content_type='application/json')
    assert rv.status_code == 200
    data = rv.get_json()
    assert data['status'] == 'ok'


def test_contact_api(client):
    """POST /api/contact should save a message."""
    rv = client.post('/api/contact',
                     data=json.dumps({
                         'name': 'Test User',
                         'email': 'test@example.com',
                         'message': 'Hello from tests'
                     }),
                     content_type='application/json')
    assert rv.status_code == 200
    data = rv.get_json()
    assert data['status'] == 'ok'


def test_contact_missing_fields(client):
    """POST /api/contact with missing fields should return 400."""
    rv = client.post('/api/contact',
                     data=json.dumps({'name': 'Test'}),
                     content_type='application/json')
    assert rv.status_code == 400


def test_admin_contacts_authorized(client):
    """GET /api/admin/contacts with correct key should return 200 and list."""
    rv = client.get('/api/admin/contacts?key=test-key')
    assert rv.status_code == 200
    data = rv.get_json()
    assert isinstance(data, list)


def test_admin_contacts_unauthorized(client):
    """GET /api/admin/contacts with wrong key should return 401."""
    rv = client.get('/api/admin/contacts?key=wrong-key')
    assert rv.status_code == 401


def test_admin_contacts_no_key(client):
    """GET /api/admin/contacts without ADMIN_KEY should return 503."""
    os.environ.pop('ADMIN_KEY', None)
    rv = client.get('/api/admin/contacts')
    assert rv.status_code == 503
    os.environ['ADMIN_KEY'] = 'test-key'


def test_safe_json_loads():
    """Test safe_json_loads helper with valid, invalid, and empty data."""
    assert safe_json_loads('["tag1", "tag2"]') == ["tag1", "tag2"]
    assert safe_json_loads('{"a": 1}') == {"a": 1}
    assert safe_json_loads(None) == []
    assert safe_json_loads('') == []
    assert safe_json_loads('invalid-json') == []
    assert safe_json_loads('invalid-json', default={}) == {}
