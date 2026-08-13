"""Tests for the portfolio backend API."""
import json
import os
import pytest

# Set up test environment before importing app
os.environ['DATABASE_PATH'] = ':memory:'
os.environ['ADMIN_KEY'] = 'test-key'

from app import app, init_db, get_db
import database

@pytest.fixture
def client():
    """Create a test client with in-memory SQLite."""
    app.config['TESTING'] = True
    database.DATABASE = ':memory:'
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


def test_projects_api(client):
    """GET /api/projects should return JSON list."""
    rv = client.get('/api/projects')
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


def test_admin_contacts_no_key(client):
    """GET /api/admin/contacts without ADMIN_KEY should return 503."""
    os.environ.pop('ADMIN_KEY', None)
    rv = client.get('/api/admin/contacts')
    assert rv.status_code == 503
    os.environ['ADMIN_KEY'] = 'test-key'