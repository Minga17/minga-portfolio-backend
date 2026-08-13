# minga-portfolio-backend

Flask + SQLite backend for the [minga-portfolio](https://minga-portfolio.onrender.com) website.

## Stack

- **Flask** 3.0.3 with flask-cors
- **SQLite** (file-based, via `DATABASE_PATH` env var)
- **Gunicorn** 22.0.0 (production WSGI server)
- Deployed on [Render](https://render.com)

## Project Structure

```
app.py          # Flask app with API routes
database.py     # SQLite connection & schema init
seed.py         # Seeds portfolio projects into the DB
tests/test_api.py  # Pytest test suite (9 tests)
static/         # Static assets (JS, CV PDF)
images/         # Chart images and profile photos
render.yaml     # Render deployment config
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/projects` | List all projects (optional `status`, `category` filters) |
| GET | `/api/projects/<id>` | Get a single project |
| POST | `/api/pageview` | Log a page view |
| POST | `/api/contact` | Submit contact form |
| GET | `/api/stats` | Site statistics |
| GET | `/api/admin/contacts` | Admin: list contacts (requires `ADMIN_KEY`) |

## Setup

```bash
pip install -r requirements.txt
python seed.py        # seed the database
python app.py         # run dev server on :5000
```

## Testing

```bash
pip install pytest
python -m pytest tests/ -v
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_PATH` | `portfolio.db` | SQLite database file path |
| `ADMIN_KEY` | (none) | Required for admin contacts endpoint |