# Procrastination Analyzer

A Django web app to help students track study behavior, identify procrastination patterns, and improve productivity with actionable suggestions.

## Features

- User registration, login, and logout
- Study session tracking with focus scores (1-10)
- Distraction logging with type, duration, and context
- Habit tracking with streaks and stability score
- Task management with priority and completion status
- AI-style suggestion engine based on user data
- Alert system for milestones and risk signals
- Analytics dashboard with productivity trends
- Seed command for realistic demo data

## Tech Stack

- Python 3.10+
- Django 5.x
- SQLite (default, development)
- HTML/CSS + Django Templates

## Project Structure

```text
ANtiGravity_WPL/
  manage.py
  requirements.txt
  db.sqlite3
  procrastination_analyzer/
    settings.py
    urls.py
  analyzer/
    models.py
    views.py
    forms.py
    urls.py
    suggestion_engine.py
    templates/analyzer/
    static/analyzer/
    management/commands/seed_demo_data.py
```

## Getting Started (Local Setup)

### 1. Clone and enter project

```bash
git clone <your-repo-url>
cd ANtiGravity_WPL
```

### 2. Create virtual environment

Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply migrations

```bash
python manage.py migrate
```

### 5. (Optional) Seed demo data

```bash
python manage.py seed_demo_data
```

Demo login created by seed command:

- Username: `demo`
- Password: `demo1234`

### 6. Run server

```bash
python manage.py runserver
```

Open in browser:

- App: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

## Main Routes

- `/` -> Login
- `/register/` -> Registration
- `/dashboard/` -> Dashboard summary
- `/sessions/` -> Study sessions
- `/distractions/` -> Distraction logs
- `/habits/` -> Habit tracking
- `/tasks/` -> Task management
- `/suggestions/` -> Suggestions + feedback
- `/alerts/` -> Alert center
- `/analytics/` -> 30-day analytics

## Useful Commands

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_demo_data
python manage.py test
```

## Notes

- Current configuration is development-oriented (`DEBUG=True`).
- Default DB is SQLite for simplicity.
- Move secrets to environment variables before production deployment.

## Future Improvements

- Deploy on Render/Railway/Azure
- Add PostgreSQL support for production
- Add automated tests for core workflows
- Add API endpoints for mobile integration

## License

This project is currently for academic/personal use. Add a license file (for example, MIT) before open-source distribution.
