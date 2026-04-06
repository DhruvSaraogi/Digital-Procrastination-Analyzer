# 📘 ABOUT — Digital Procrastination Analyzer (ProcrastiTrack)

> **Source of Truth** for the AntiGravity_WPL project.
> Last updated: April 2026

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Tech Stack](#2-tech-stack)
3. [Project Structure](#3-project-structure)
4. [Architecture & Data Flow](#4-architecture--data-flow)
5. [Database Schema (Models)](#5-database-schema-models)
6. [Suggestion Engine — Rule-Based AI](#6-suggestion-engine--rule-based-ai)
7. [Views & Business Logic](#7-views--business-logic)
8. [Forms & Validation](#8-forms--validation)
9. [URL Routing](#9-url-routing)
10. [Templates & Frontend](#10-templates--frontend)
11. [Custom Template Tags](#11-custom-template-tags)
12. [Admin Panel](#12-admin-panel)
13. [Seed Demo Data Command](#13-seed-demo-data-command)
14. [Features — Detailed Breakdown](#14-features--detailed-breakdown)
15. [Functional Requirements](#15-functional-requirements)
16. [Non-Functional Requirements](#16-non-functional-requirements)
17. [Security Features](#17-security-features)
18. [Configuration & Settings](#18-configuration--settings)
19. [How to Run (Local Setup)](#19-how-to-run-local-setup)
20. [Deployment (Production)](#20-deployment-production)
21. [API Endpoints](#21-api-endpoints)
22. [User Journey / Workflow](#22-user-journey--workflow)
23. [Key Algorithms](#23-key-algorithms)
24. [Dependencies](#24-dependencies)
25. [Documents & References](#25-documents--references)
26. [Future Improvements](#26-future-improvements)
27. [License](#27-license)

---

## 1. Project Overview

| Field | Detail |
|-------|--------|
| **Project Name** | Digital Procrastination Analyzer |
| **Brand Name** | ProcrastiTrack |
| **Repository** | `AntiGravity_WPL` (DhruvSaraogi/Digital-Procrastination-Analyzer) |
| **Type** | Full-Stack Django Web Application |
| **Purpose** | Track study behavior, detect procrastination patterns, and boost productivity with rule-based AI suggestions |
| **Target Users** | Students who want to monitor and improve their study habits |
| **Domain** | EdTech / Productivity / Self-Improvement |
| **Django Project** | `procrastination_analyzer` |
| **Django App** | `analyzer` |

### What It Does

ProcrastiTrack is a web-based system that allows students to:

- **Log study sessions** with subject, duration, and self-rated focus scores (1–10)
- **Record distractions** by type, duration, and context
- **Build habits** with streak tracking and stability scoring
- **Manage tasks** with priorities and deadlines
- **Receive AI-style personalized suggestions** based on 15 behavioral rules
- **View analytics dashboards** with interactive Chart.js visualizations
- **Get alerts** for milestones, overdue tasks, and focus warnings
- **Detect behavioral patterns** like peak focus times and distraction triggers

---

## 2. Tech Stack

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| **Language** | Python | 3.10+ | Core backend language |
| **Framework** | Django | 5.0+ (generated on 5.2.3) | Web framework (MTV pattern) |
| **Database (Dev)** | SQLite3 | Built-in | File-based development DB |
| **Database (Prod)** | PostgreSQL | via `psycopg2-binary` ≥ 2.9 | Production-grade RDBMS |
| **Frontend Framework** | Bootstrap | 5.3.3 | Responsive UI components |
| **Icons** | Bootstrap Icons | 1.11.3 | Icon library |
| **Typography** | Google Fonts (Inter) | Weights 300–800 | Modern sans-serif typeface |
| **Charts** | Chart.js | 4.4.6 | Interactive data visualizations |
| **AJAX** | jQuery | 3.7.1 | Asynchronous UI interactions |
| **CSS** | Custom vanilla CSS | — | Premium dark glassmorphism theme |
| **WSGI Server** | Gunicorn | ≥ 22.0 | Production HTTP server |
| **Static Files** | WhiteNoise | ≥ 6.7 | Static file serving in production |
| **DB URL Parsing** | dj-database-url | ≥ 2.2 | Parse `DATABASE_URL` env var |

---

## 3. Project Structure

```
AntiGravity_WPL/
├── manage.py                                   # Django CLI entry point
├── db.sqlite3                                  # SQLite database file
├── requirements.txt                            # Python dependencies
├── Procfile                                    # Heroku/Render/Railway deploy config
├── README.md                                   # Quick-start readme
├── PROJECT_EXPLANATION.md                      # Line-by-line code explanation (~2000 lines)
├── ABOUT.md                                    # THIS FILE — source of truth
├── Project_Development_Log.docx                # Academic development log
├── WPL_MINI PROJECT SYNOPSIS TEMPLATE.docx     # Academic synopsis document
│
├── procrastination_analyzer/                   # Django project configuration
│   ├── __init__.py
│   ├── settings.py                             # All Django settings
│   ├── urls.py                                 # Root URL router
│   ├── wsgi.py                                 # WSGI application entry
│   └── asgi.py                                 # ASGI application entry
│
├── analyzer/                                   # Main Django app
│   ├── __init__.py
│   ├── apps.py                                 # App config (name: 'analyzer')
│   ├── models.py                               # 8 database models (268 lines)
│   ├── views.py                                # 17 view functions (421 lines)
│   ├── forms.py                                # 5 form classes (139 lines)
│   ├── urls.py                                 # 17 URL patterns (44 lines)
│   ├── admin.py                                # 8 admin registrations (55 lines)
│   ├── suggestion_engine.py                    # AI engine: 4 functions (406 lines)
│   ├── tests.py                                # Test placeholder
│   │
│   ├── management/
│   │   └── commands/
│   │       └── seed_demo_data.py               # Demo data seeder (190 lines)
│   │
│   ├── templatetags/
│   │   └── analyzer_extras.py                  # 6 custom template filters (86 lines)
│   │
│   ├── templates/analyzer/                     # 11 HTML templates
│   │   ├── base.html                           # Master layout (sidebar + nav)
│   │   ├── login.html                          # Login page
│   │   ├── register.html                       # Registration page
│   │   ├── dashboard.html                      # Main dashboard with charts
│   │   ├── study_session.html                  # Study session CRUD
│   │   ├── distraction_log.html                # Distraction logging
│   │   ├── habits.html                         # Habit tracker with AJAX
│   │   ├── tasks.html                          # Task manager with AJAX
│   │   ├── suggestions.html                    # AI suggestions + history
│   │   ├── alerts.html                         # Alert center with dismiss
│   │   └── analytics.html                      # 30-day deep analytics
│   │
│   ├── static/analyzer/css/
│   │   └── style.css                           # Custom dark theme (884 lines)
│   │
│   └── migrations/
│       └── 0001_initial.py                     # Initial schema migration
│
└── static/                                     # Project-level static dir (empty)
```

### File Size Summary

| File | Lines | Size |
|------|-------|------|
| `models.py` | 268 | 10 KB |
| `views.py` | 421 | 16 KB |
| `suggestion_engine.py` | 406 | 19 KB |
| `forms.py` | 139 | 5 KB |
| `style.css` | 884 | 20 KB |
| `seed_demo_data.py` | 190 | 8 KB |
| `dashboard.html` | 252 | 11 KB |
| `analytics.html` | 232 | 9 KB |
| `base.html` | 178 | 8 KB |
| **Total app code** | **~3,200+** | **~120 KB** |

---

## 4. Architecture & Data Flow

### Pattern: MTV (Model–Template–View)

```
┌──────────────┐     HTTP Request     ┌──────────────────┐
│   Browser    │ ──────────────────→  │   URLs (urls.py)  │
│   (Client)   │                      │   Route dispatch   │
└──────────────┘                      └────────┬─────────┘
       ↑                                       │
       │  HTML Response                        ↓
       │                              ┌──────────────────┐
       │                              │   Views (views.py)│
       │                              │   Business logic   │
       │                              └───┬──────────┬───┘
       │                                  │          │
       │                                  ↓          ↓
       │                          ┌────────────┐ ┌──────────────────────┐
       │                          │  Models     │ │ suggestion_engine.py │
       │                          │ (Database)  │ │ • analyze_and_suggest│
       │                          │  8 tables   │ │ • compute_metrics    │
       │                          └────────────┘ │ • detect_patterns    │
       │                                         │ • generate_alerts    │
       │                                         └──────────────────────┘
       │                                  │
       │                                  ↓
       │                          ┌──────────────────┐
       └───────────────────────── │  Templates (.html)│
                                  │  + Chart.js       │
                                  │  + Bootstrap 5    │
                                  │  + jQuery AJAX    │
                                  └──────────────────┘
```

### Database Relations

```
User (Django Auth)
 ├──→ (1:N) StudySession
 │              └──→ (1:N) DistractionLog
 ├──→ (1:N) DistractionLog  (standalone distractions also allowed)
 ├──→ (1:N) Habit
 ├──→ (1:N) Task
 ├──→ (1:N) ProductivityMetrics  (one per user per day, unique_together)
 ├──→ (1:N) SuggestionHistory
 ├──→ (1:N) BehaviorPattern
 └──→ (1:N) Alert
```

---

## 5. Database Schema (Models)

All 8 models are defined in `analyzer/models.py`. Every model has a `ForeignKey` to Django's built-in `User`.

### 5.1 StudySession

| Field | Type | Description |
|-------|------|-------------|
| `user` | ForeignKey(User) | Owner |
| `subject` | CharField(200) | Study subject name |
| `start_time` | DateTimeField | Session start |
| `end_time` | DateTimeField | Session end |
| `focus_score` | IntegerField (1–10) | Self-rated focus |
| `notes` | TextField (optional) | Free-form notes |
| `created_at` | DateTimeField (auto) | Record creation |

**Computed properties:** `duration_minutes`, `duration_hours`
**Ordering:** Newest first (`-start_time`)

### 5.2 DistractionLog

| Field | Type | Description |
|-------|------|-------------|
| `user` | ForeignKey(User) | Owner |
| `session` | ForeignKey(StudySession, optional) | Linked session |
| `distraction_type` | CharField (10 choices) | Category of distraction |
| `duration_minutes` | PositiveIntegerField | Time lost in minutes |
| `context` | TextField (optional) | What triggered it |
| `timestamp` | DateTimeField | When it occurred |

**Distraction types:** Social Media, Phone Notifications, People/Conversations, Food/Snacks, Daydreaming, Entertainment, Internet Browsing, Noise/Environment, Fatigue/Sleepiness, Other

### 5.3 Habit

| Field | Type | Description |
|-------|------|-------------|
| `user` | ForeignKey(User) | Owner |
| `name` | CharField(200) | Habit name |
| `description` | TextField (optional) | Details |
| `target_frequency` | CharField (daily/weekly/custom) | Expected frequency |
| `current_streak` | PositiveIntegerField | Active consecutive days |
| `longest_streak` | PositiveIntegerField | Best-ever streak |
| `total_completions` | PositiveIntegerField | Lifetime count |
| `last_completed` | DateField (optional) | Last completion date |
| `is_active` | BooleanField | Soft-delete flag |

**Computed property:** `stability_score` (0–100) — based on consistency ratio + streak bonus (max 30% for 30-day streak)

### 5.4 Task

| Field | Type | Description |
|-------|------|-------------|
| `user` | ForeignKey(User) | Owner |
| `title` | CharField(300) | Task title |
| `description` | TextField (optional) | Details |
| `priority` | CharField (low/medium/high/urgent) | Priority level |
| `status` | CharField (pending/in_progress/completed/overdue) | Current status |
| `deadline` | DateTimeField (optional) | Due date |
| `completed_at` | DateTimeField (optional) | Completion timestamp |

**Computed property:** `is_overdue` — `True` if deadline passed and not completed

### 5.5 ProductivityMetrics

Derived daily summary. **One record per user per day** (`unique_together = ['user', 'date']`).

| Field | Type | Description |
|-------|------|-------------|
| `date` | DateField | The day |
| `total_study_minutes` | FloatField | Sum of session durations |
| `avg_focus_score` | FloatField | Mean focus score |
| `total_distraction_minutes` | FloatField | Sum of distraction durations |
| `distraction_ratio` | FloatField | distraction / study ratio |
| `sessions_count` | PositiveIntegerField | Number of sessions |
| `tasks_completed` | PositiveIntegerField | Tasks done that day |
| `habits_completed` | PositiveIntegerField | Habits done that day |
| `productivity_score` | FloatField (0–100) | Weighted composite score |

### 5.6 SuggestionHistory

| Field | Type | Description |
|-------|------|-------------|
| `suggestion_text` | TextField | The suggestion content |
| `category` | CharField (6 choices) | focus/distraction/habit/task/schedule/wellness |
| `is_helpful` | BooleanField (nullable) | User feedback (👍/👎) |
| `is_read` | BooleanField | Read status |
| `generated_at` | DateTimeField (auto) | Creation time |

### 5.7 BehaviorPattern

| Field | Type | Description |
|-------|------|-------------|
| `pattern_type` | CharField (6 choices) | peak_focus/low_focus/distraction_trigger/productive_habit/procrastination/improvement |
| `description` | TextField | Human-readable description |
| `confidence` | FloatField (0.0–1.0) | Detection confidence |
| `data_points` | PositiveIntegerField | Supporting data count |
| `is_active` | BooleanField | Active flag |

### 5.8 Alert

| Field | Type | Description |
|-------|------|-------------|
| `alert_type` | CharField (8 choices) | streak_broken/streak_milestone/low_focus/high_distraction/task_overdue/goal_achieved/improvement/reminder |
| `severity` | CharField (info/warning/success/danger) | Visual severity |
| `title` | CharField(200) | Alert headline |
| `message` | TextField | Full message |
| `is_read` | BooleanField | Read flag |
| `is_dismissed` | BooleanField | Dismiss flag |

---

## 6. Suggestion Engine — Rule-Based AI

Located in `analyzer/suggestion_engine.py` (406 lines). Contains 4 core functions:

### 6.1 `analyze_and_suggest(user)` — 15 Rules

Returns `[{'text': str, 'category': str}, ...]`

| Rule # | Condition | Category | Summary |
|--------|-----------|----------|---------|
| 1 | No study sessions this week | focus | Encourages starting with Pomodoro |
| 2 | Avg focus < 4 or < 6 or ≥ 8 | focus | Tiered focus feedback |
| 3 | > 15 distractions this week | distraction | Distraction notepad technique |
| 4 | Top distraction type by total minutes | distraction | Type-specific tips (9 unique tips) |
| 5 | Distraction ratio > 30% | distraction | Pomodoro recommendation |
| 6 | Broken habit streaks | habit | "What-the-hell effect" warning |
| 7 | Low stability habits (< 30%) | habit | Habit stacking suggestion |
| 8 | No active habits | habit | Start with one small habit |
| 9 | Overdue tasks exist | task | Break into smaller steps |
| 10 | > 10 pending tasks | task | Eisenhower Matrix recommendation |
| 11 | No tasks at all | task | Planning reduces procrastination |
| 12 | Avg session < 20 min | schedule | Short session warning |
| 13 | Peak study time analysis (morning/afternoon/evening) | schedule | Schedule optimization |
| 14 | > 35 study hours/week | wellness | Burnout prevention |
| 15 | 15%+ productivity improvement week-over-week | focus | Positive reinforcement |

### 6.2 `compute_daily_metrics(user, date)`

**Productivity Score Formula (0–100):**

```
focus_component       = (avg_focus / 10) × 40         → max 40 points
study_component       = min(study_min / 240, 1) × 30  → max 30 points (4h = 100%)
distraction_penalty   = min(ratio, 1.0) × 20          → max −20 points
task_bonus            = min(tasks_done / 3, 1) × 10   → max 10 points

score = max(0, focus + study − distraction + tasks)
```

Uses `update_or_create` to maintain one record per user per day.

### 6.3 `detect_patterns(user)`

Analyzes 30-day data to find:
- **Peak focus times** — Morning/Afternoon/Evening blocks with avg focus ≥ 7
- **Low focus times** — Blocks with avg focus ≤ 4
- **Top distraction trigger** — Most time-consuming distraction type

Requires ≥ 5 sessions to activate. Stores results in `BehaviorPattern` with confidence scores.

### 6.4 `generate_alerts(user)`

Auto-generates alerts for:
- **Streak broken** — Daily habit not completed for 2+ days (severity: warning)
- **Streak milestones** — 7, 14, 21, 30, 60, 100 days (severity: success)
- **Task overdue** — Past deadline and not completed (severity: danger)
- **Low focus warning** — Today's avg focus < 4 with 2+ sessions (severity: warning)

Deduplicates by checking for existing alerts on the same day.

---

## 7. Views & Business Logic

`analyzer/views.py` — 17 view functions across 421 lines.

| View Function | Method | Auth | URL | Purpose |
|--------------|--------|------|-----|---------|
| `register_view` | GET/POST | No | `/register/` | User registration |
| `login_view` | GET/POST | No | `/` | User login |
| `logout_view` | GET | Yes | `/logout/` | User logout |
| `dashboard_view` | GET | Yes | `/dashboard/` | Main dashboard with stats & charts |
| `study_sessions_view` | GET/POST | Yes | `/sessions/` | Log & view sessions |
| `delete_session` | GET | Yes | `/sessions/delete/<pk>/` | Delete a session |
| `distractions_view` | GET/POST | Yes | `/distractions/` | Log & view distractions |
| `habits_view` | GET/POST | Yes | `/habits/` | Create & view habits |
| `complete_habit` | GET (AJAX) | Yes | `/habits/complete/<pk>/` | Mark habit done today |
| `delete_habit` | GET | Yes | `/habits/delete/<pk>/` | Soft-delete (archive) habit |
| `tasks_view` | GET/POST | Yes | `/tasks/` | Create & view tasks |
| `complete_task` | GET (AJAX) | Yes | `/tasks/complete/<pk>/` | Mark task completed |
| `delete_task` | GET | Yes | `/tasks/delete/<pk>/` | Hard-delete task |
| `suggestions_view` | GET | Yes | `/suggestions/` | Generate & view suggestions |
| `rate_suggestion` | GET (AJAX) | Yes | `/suggestions/rate/<pk>/` | Rate suggestion helpful/not |
| `alerts_view` | GET | Yes | `/alerts/` | View all alerts |
| `dismiss_alert` | GET (AJAX) | Yes | `/alerts/dismiss/<pk>/` | Dismiss an alert |
| `analytics_view` | GET | Yes | `/analytics/` | 30-day deep analytics |
| `api_unread_count` | GET (AJAX) | Yes | `/api/unread-count/` | Unread alert count for badge |

### Dashboard View — Data Prepared

The dashboard computes:
- 7-day study hours, avg focus, distraction count, task completion stats
- 7-day chart data arrays (dates, study hours, focus scores, distraction minutes)
- Distraction type distribution (grouped by type, summed minutes)
- Today's productivity score
- Top 5 active habit streaks
- 5 most recent unread alerts

### Analytics View — 30-Day Computation

Iterates over last 30 days calling `compute_daily_metrics()` for each, then prepares arrays for 5 charts: productivity score trend, study hours bar, focus score trend, distraction ratio trend, and habit stability horizontal bar.

---

## 8. Forms & Validation

`analyzer/forms.py` — 5 form classes.

| Form Class | Model | Fields | Special Features |
|------------|-------|--------|------------------|
| `RegisterForm` | User (UserCreationForm) | username, email, password1, password2 | Auto-applies Bootstrap dark theme classes |
| `StudySessionForm` | StudySession | subject, start_time, end_time, focus_score, notes | HTML5 `datetime-local` pickers; validates end > start |
| `DistractionForm` | DistractionLog | session, distraction_type, duration_minutes, context | Session dropdown filtered to current user; session optional |
| `HabitForm` | Habit | name, description, target_frequency | Frequency dropdown |
| `TaskForm` | Task | title, description, priority, deadline | Optional deadline with datetime picker |

All form widgets styled with Bootstrap dark theme classes: `bg-dark text-light border-secondary`.

---

## 9. URL Routing

### Root URLs (`procrastination_analyzer/urls.py`)
```
/admin/    → Django admin panel
/          → analyzer app URLs (all other routes)
```

### App URLs (`analyzer/urls.py`) — 17 Patterns

| URL Pattern | Name | View |
|-------------|------|------|
| `/` | `login` | `login_view` |
| `/register/` | `register` | `register_view` |
| `/logout/` | `logout` | `logout_view` |
| `/dashboard/` | `dashboard` | `dashboard_view` |
| `/sessions/` | `study_sessions` | `study_sessions_view` |
| `/sessions/delete/<int:pk>/` | `delete_session` | `delete_session` |
| `/distractions/` | `distractions` | `distractions_view` |
| `/habits/` | `habits` | `habits_view` |
| `/habits/complete/<int:pk>/` | `complete_habit` | `complete_habit` |
| `/habits/delete/<int:pk>/` | `delete_habit` | `delete_habit` |
| `/tasks/` | `tasks` | `tasks_view` |
| `/tasks/complete/<int:pk>/` | `complete_task` | `complete_task` |
| `/tasks/delete/<int:pk>/` | `delete_task` | `delete_task` |
| `/suggestions/` | `suggestions` | `suggestions_view` |
| `/suggestions/rate/<int:pk>/` | `rate_suggestion` | `rate_suggestion` |
| `/alerts/` | `alerts` | `alerts_view` |
| `/alerts/dismiss/<int:pk>/` | `dismiss_alert` | `dismiss_alert` |
| `/analytics/` | `analytics` | `analytics_view` |
| `/api/unread-count/` | `api_unread_count` | `api_unread_count` |

---

## 10. Templates & Frontend

### 10.1 Template Hierarchy

```
base.html (master layout)
 ├── login.html        (extends → auth_content block)
 ├── register.html     (extends → auth_content block)
 ├── dashboard.html    (extends → content block)
 ├── study_session.html
 ├── distraction_log.html
 ├── habits.html
 ├── tasks.html
 ├── suggestions.html
 ├── alerts.html
 └── analytics.html
```

### 10.2 Base Template Features

- **Dark theme** via `data-bs-theme="dark"`
- **Sidebar navigation** with active-state highlighting
- **Mobile hamburger menu** (responsive ≤ 991px)
- **Toast notifications** for Django messages (auto-dismiss after 4s)
- **Alert badge** — polls `/api/unread-count/` every 30 seconds via AJAX
- **User avatar** — first letter of username in gradient circle

### 10.3 CDN Dependencies

| Library | CDN URL |
|---------|---------|
| Bootstrap 5.3.3 CSS | `cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css` |
| Bootstrap Icons 1.11.3 | `cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css` |
| Google Fonts (Inter) | `fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800` |
| jQuery 3.7.1 | `code.jquery.com/jquery-3.7.1.min.js` |
| Bootstrap 5.3.3 JS | `cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js` |
| Chart.js 4.4.6 | `cdn.jsdelivr.net/npm/chart.js@4.4.6/dist/chart.umd.min.js` |

### 10.4 CSS Design System (`style.css` — 884 lines)

**Theme:** Premium dark glassmorphism

**CSS Custom Properties:**

| Variable | Value | Usage |
|----------|-------|-------|
| `--bg-primary` | `#0a0a1a` | Page background |
| `--bg-secondary` | `#12122a` | Sidebar background |
| `--bg-card` | `rgba(20, 20, 50, 0.7)` | Card backgrounds |
| `--accent-primary` | `#6c5ce7` | Purple accent |
| `--accent-success` | `#00cec9` | Teal/green accent |
| `--accent-danger` | `#ff6b6b` | Red accent |
| `--accent-warning` | `#fdcb6e` | Yellow accent |
| `--sidebar-width` | `260px` | Sidebar width |

**UI Components styled:** Sidebar, stat cards (with color-coded left borders), glass cards, tables, habit cards, suggestion cards, alert items, productivity ring (SVG), task items, auth pages, pattern cards, empty states, scrollbar, mobile header.

**Animations:** `fadeUp`, `slideUp`, `slideIn`, `pulse-badge`, staggered animation delays (`.stagger-1` to `.stagger-5`), hover transforms.

### 10.5 Charts (Chart.js)

| Page | Chart | Type | Data |
|------|-------|------|------|
| Dashboard | Study Hours & Focus Trend | Dual-axis Line | 7-day study hours + focus scores |
| Dashboard | Distraction Breakdown | Doughnut | Distraction type distribution |
| Dashboard | Productivity Score Ring | SVG Circle | Today's score (0–100) |
| Analytics | Productivity Score Trend | Line | 30-day productivity scores |
| Analytics | Study Hours | Bar | 30-day study hours |
| Analytics | Focus Score Trend | Line | 30-day focus scores |
| Analytics | Distraction Ratio | Line | 30-day distraction ratios |
| Analytics | Habit Stability | Horizontal Bar | Per-habit stability scores |

---

## 11. Custom Template Tags

`analyzer/templatetags/analyzer_extras.py` — 6 filters:

| Filter | Usage | Purpose |
|--------|-------|---------|
| `get_severity_class` | `{{ alert.severity\|get_severity_class }}` | Maps severity → Bootstrap alert class |
| `get_severity_icon` | `{{ severity\|get_severity_icon }}` | Maps severity → Bootstrap icon class |
| `get_priority_class` | `{{ task.priority\|get_priority_class }}` | Maps priority → Bootstrap badge class |
| `get_category_icon` | `{{ category\|get_category_icon }}` | Maps suggestion category → icon |
| `get_category_color` | `{{ category\|get_category_color }}` | Maps category → hex color |
| `multiply` | `{{ value\|multiply:100 }}` | Multiplies two numbers |
| `percentage_of` | `{{ value\|percentage_of:total }}` | Calculates percentage |

---

## 12. Admin Panel

All 8 models registered with `@admin.register` in `analyzer/admin.py`.

| Model | list_display | list_filter | search_fields |
|-------|-------------|-------------|---------------|
| StudySession | user, subject, start/end time, focus, duration | user, focus_score | subject, notes |
| DistractionLog | user, type, duration, timestamp | type, user | — |
| Habit | user, name, frequency, current/longest streak, stability | frequency, is_active | — |
| Task | user, title, priority, status, deadline | priority, status | — |
| ProductivityMetrics | user, date, avg_focus, study_min, score | user | — |
| SuggestionHistory | user, category, is_helpful, generated_at | category, is_helpful | — |
| BehaviorPattern | user, pattern_type, confidence, data_points, is_active | pattern_type | — |
| Alert | user, type, severity, title, is_read, created_at | type, severity, is_read | — |

Access via: `http://127.0.0.1:8000/admin/`

---

## 13. Seed Demo Data Command

**Command:** `python manage.py seed_demo_data`

**Creates:**
- 1 demo user (username: `demo`, password: `demo1234`)
- ~60 study sessions over 30 days (0–3 per day, various subjects)
- ~60+ distraction logs linked to random sessions
- 5 habits with realistic streaks (Read 30 min, Morning revision, Solve 5 problems, Weekly review, Exercise)
- 8 tasks (mix of pending, in-progress, completed)
- 31 days of computed productivity metrics
- Detected behavior patterns
- Generated alerts (streak milestones, overdue warnings)
- Generated suggestion history

**Focus score trend:** Designed to trend upward slightly over time (simulating improvement).

**Subjects used:** Mathematics, Physics, Computer Science, Data Structures, Operating Systems, Database Management, Web Programming, Statistics, English, Digital Electronics.

---

## 14. Features — Detailed Breakdown

### 14.1 User Authentication
- Registration with username, email, password (with Django's built-in validators)
- Login/logout with session management
- Auto-redirect authenticated users away from login/register pages
- `@login_required` decorator on all protected views
- User-isolated data (can only see own records)

### 14.2 Study Session Tracking
- Log sessions with subject, start/end time, focus score (1–10), optional notes
- Auto-calculated duration (minutes and hours)
- View last 20 sessions in a table
- Delete sessions with confirmation
- Triggers daily metric recomputation on save

### 14.3 Distraction Logging
- 10 predefined distraction categories
- Optional link to a specific study session
- Duration tracking in minutes
- Context field for recording triggers
- Session dropdown filtered to user's own sessions

### 14.4 Habit Tracking
- Create habits with name, description, target frequency (daily/weekly/custom)
- **AJAX completion** — mark done without page reload
- **Streak logic:** Consecutive-day tracking with auto-reset
- Longest streak tracking
- **Stability score** (0–100) computed from consistency + streak bonus
- Soft-delete (archive) instead of hard-delete

### 14.5 Task Management
- Create tasks with title, description, priority (4 levels), optional deadline
- **AJAX completion** with slide-out animation
- Auto-overdue detection
- Separate pending/completed views
- Delete with confirmation

### 14.6 AI Suggestion Engine
- 15 rule-based analysis rules
- Analyzes 7-day and 30-day behavioral data
- Type-specific distraction tips (9 unique strategies)
- Duplicate prevention (same suggestion won't repeat same day)
- User feedback system (👍/👎 rating via AJAX)
- Suggestion history with scroll view

### 14.7 Behavioral Pattern Detection
- Identifies peak focus time of day
- Detects low focus periods
- Finds primary distraction triggers
- Confidence scoring (0.0–1.0) based on data volume
- Data points counter

### 14.8 Alert System
- 4 alert sources: streak broken, streak milestones (7/14/21/30/60/100 days), task overdue, low focus
- 4 severity levels: info, warning, success, danger
- Dismissible via AJAX
- Read/unread tracking
- Navbar badge with real-time count (polls every 30s)
- Daily deduplication

### 14.9 Analytics Dashboard
- 30-day data window
- 5 interactive charts (productivity trend, study hours, focus scores, distraction ratio, habit stability)
- Summary statistics (total sessions, total hours, total distractions, avg productivity)
- Detected behavior patterns display with confidence bars

### 14.10 Dashboard
- Weekly summary cards (study hours, avg focus, distractions, tasks)
- Dual-axis line chart (study hours + focus trend)
- Doughnut chart (distraction distribution)
- SVG productivity score ring with gradient animation
- Top 5 habit streaks with stability bars
- Recent unread alerts preview

---

## 15. Functional Requirements

| ID | Requirement | Status |
|----|------------|--------|
| FR-01 | User registration with username, email, password | ✅ |
| FR-02 | User login and logout | ✅ |
| FR-03 | Log study sessions with subject, time, and focus score | ✅ |
| FR-04 | View and delete study sessions | ✅ |
| FR-05 | Log distractions with type, duration, and context | ✅ |
| FR-06 | Link distraction to specific study session (optional) | ✅ |
| FR-07 | Create daily/weekly/custom habits | ✅ |
| FR-08 | Mark habits complete with streak tracking | ✅ |
| FR-09 | Calculate habit stability score | ✅ |
| FR-10 | Archive (soft-delete) habits | ✅ |
| FR-11 | Create tasks with priority and deadline | ✅ |
| FR-12 | Mark tasks complete via AJAX | ✅ |
| FR-13 | Auto-detect overdue tasks | ✅ |
| FR-14 | Generate personalized suggestions (15 rules) | ✅ |
| FR-15 | Rate suggestions as helpful/unhelpful | ✅ |
| FR-16 | Compute daily productivity metrics | ✅ |
| FR-17 | Detect behavioral patterns (peak focus, distractions) | ✅ |
| FR-18 | Generate alerts for milestones, risks, overdue | ✅ |
| FR-19 | Dismiss alerts via AJAX | ✅ |
| FR-20 | Display 7-day dashboard with charts | ✅ |
| FR-21 | Display 30-day analytics with trend charts | ✅ |
| FR-22 | Real-time unread alert badge | ✅ |
| FR-23 | Seed demo data for presentations | ✅ |
| FR-24 | Django admin panel for all models | ✅ |

---

## 16. Non-Functional Requirements

| Requirement | Implementation |
|------------|---------------|
| **Responsive design** | Bootstrap 5 grid + mobile sidebar toggle (< 992px) |
| **Dark mode** | Full dark theme via CSS custom properties |
| **Performance** | WhiteNoise for static files; `update_or_create` for metrics |
| **UX** | AJAX for habit/task completion, alerts; toast notifications; slide animations |
| **Accessibility** | Semantic HTML, Bootstrap ARIA attributes, labeled forms |
| **Time zone** | `Asia/Kolkata` (IST) configured; `USE_TZ = True` |
| **Scalability** | PostgreSQL support via `DATABASE_URL`; Gunicorn WSGI |

---

## 17. Security Features

| Feature | Implementation |
|---------|---------------|
| **Authentication** | Django's built-in auth system with session-based login |
| **Authorization** | `@login_required` on all protected views |
| **Data isolation** | `user=request.user` filter on all queries; `get_object_or_404` with user check |
| **CSRF protection** | `{% csrf_token %}` in all forms; `CsrfViewMiddleware` enabled |
| **Password hashing** | Django's PBKDF2 password hasher (default) |
| **SQL injection prevention** | Django ORM query builder — no raw SQL |
| **XSS prevention** | Django template auto-escaping |
| **Clickjacking** | `XFrameOptionsMiddleware` enabled |
| **Secret key** | Environment variable (`SECRET_KEY`) for production |
| **Debug mode** | `DEBUG` controlled via environment variable |
| **Allowed hosts** | `ALLOWED_HOSTS` configurable via environment |

---

## 18. Configuration & Settings

`procrastination_analyzer/settings.py` key settings:

| Setting | Dev Value | Prod Behavior |
|---------|-----------|---------------|
| `SECRET_KEY` | Hardcoded insecure key | Reads from `SECRET_KEY` env var |
| `DEBUG` | `True` | Reads from `DEBUG` env var |
| `ALLOWED_HOSTS` | `127.0.0.1, localhost` | Reads from `ALLOWED_HOSTS` env var |
| `DATABASES` | SQLite (`db.sqlite3`) | PostgreSQL via `DATABASE_URL` env var |
| `STATIC_URL` | `/static/` | Same |
| `STATICFILES_DIRS` | `[BASE_DIR / 'static']` | Same |
| `STATIC_ROOT` | `BASE_DIR / 'staticfiles'` | Used by `collectstatic` |
| `STATICFILES_STORAGE` | Default | `CompressedManifestStaticFilesStorage` (WhiteNoise) |
| `TIME_ZONE` | `Asia/Kolkata` | Same |
| `LOGIN_URL` | `login` | Same |
| `LOGIN_REDIRECT_URL` | `dashboard` | Same |
| `DEFAULT_AUTO_FIELD` | `BigAutoField` | Same |

WhiteNoise middleware is conditionally inserted if the package is available.

---

## 19. How to Run (Local Setup)

### Prerequisites
- Python 3.10+
- pip

### Steps

```bash
# 1. Clone the repository
git clone <repo-url>
cd ANtiGravity_WPL

# 2. Create virtual environment
python -m venv .venv

# Windows (PowerShell):
.\.venv\Scripts\Activate.ps1

# macOS/Linux:
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Apply database migrations
python manage.py migrate

# 5. (Optional) Seed demo data
python manage.py seed_demo_data

# 6. (Optional) Create admin superuser
python manage.py createsuperuser

# 7. Run development server
python manage.py runserver
```

### Access Points

| URL | Purpose |
|-----|---------|
| `http://127.0.0.1:8000/` | Login page |
| `http://127.0.0.1:8000/dashboard/` | Main dashboard |
| `http://127.0.0.1:8000/admin/` | Django admin panel |

### Demo Credentials (after seeding)
- **Username:** `demo`
- **Password:** `demo1234`

---

## 20. Deployment (Production)

### Procfile (Heroku/Render/Railway)

```
web: gunicorn procrastination_analyzer.wsgi:application --bind 0.0.0.0:$PORT
release: python manage.py migrate
```

### Environment Variables Required

| Variable | Example |
|----------|---------|
| `SECRET_KEY` | A long random string |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `your-app.onrender.com` |
| `DATABASE_URL` | `postgres://user:pass@host:5432/dbname` |

### Static Files

Run `python manage.py collectstatic` — WhiteNoise serves files from `staticfiles/` with compression and caching.

---

## 21. API Endpoints

| Endpoint | Method | Auth | Response | Purpose |
|----------|--------|------|----------|---------|
| `/api/unread-count/` | GET | Yes | `{"count": N}` | Alert badge count |
| `/habits/complete/<pk>/` | GET | Yes | `{"status": "success", "streak": N, "total": N, "stability": N}` | Complete habit |
| `/tasks/complete/<pk>/` | GET | Yes | `{"status": "success", "message": "..."}` | Complete task |
| `/suggestions/rate/<pk>/?helpful=true/false` | GET | Yes | `{"status": "success"}` | Rate suggestion |
| `/alerts/dismiss/<pk>/` | GET | Yes | `{"status": "success"}` | Dismiss alert |

All AJAX endpoints return JSON responses.

---

## 22. User Journey / Workflow

```
1. Register / Login
        ↓
2. Dashboard (weekly overview, charts, alerts)
        ↓
3. Log Study Sessions → auto-updates metrics
        ↓
4. Log Distractions → tracks time lost & triggers
        ↓
5. Track Habits → build streaks → stability scoring
        ↓
6. Manage Tasks → priorities, deadlines, overdue alerts
        ↓
7. View Suggestions → 15 rule-based insights → rate feedback
        ↓
8. Monitor Alerts → streak milestones, focus warnings, overdue
        ↓
9. Deep Analytics → 30-day trends, pattern detection, habit stability
```

---

## 23. Key Algorithms

### Streak Logic (Habit Completion)
```
if last_completed == today:
    → already done, no change
elif last_completed == yesterday:
    → streak += 1 (consecutive)
else:
    → streak = 1 (restart)

longest_streak = max(longest_streak, current_streak)
```

### Stability Score (Habit)
```
days_active = max((today - created_at).days, 1)
expected = days_active (daily) | days_active/7 (weekly) | days_active/3 (custom)
consistency = min(total_completions / expected, 1.0)
streak_bonus = min(current_streak / 30, 0.3)
stability = min((consistency + streak_bonus) × 100, 100)
```

### Productivity Score (Daily)
```
focus     = (avg_focus / 10) × 40     [max 40]
study     = min(minutes / 240, 1) × 30 [max 30]
penalty   = min(dist_ratio, 1) × 20   [max −20]
tasks     = min(done / 3, 1) × 10     [max 10]
score     = max(0, focus + study − penalty + tasks)
```

---

## 24. Dependencies

### `requirements.txt`
```
Django>=5.0
gunicorn>=22.0
whitenoise>=6.7
dj-database-url>=2.2
psycopg2-binary>=2.9
```

### Frontend CDN Dependencies
- Bootstrap 5.3.3 (CSS + JS)
- Bootstrap Icons 1.11.3
- jQuery 3.7.1
- Chart.js 4.4.6
- Google Fonts (Inter)

---

## 25. Documents & References

| File | Description |
|------|-------------|
| `README.md` | Quick-start guide with setup instructions |
| `PROJECT_EXPLANATION.md` | ~2000-line detailed code explanation (line-by-line) |
| `Project_Development_Log.docx` | Academic project development log |
| `WPL_MINI PROJECT SYNOPSIS TEMPLATE.docx` | Academic mini project synopsis |
| `ABOUT.md` | **This file** — comprehensive source of truth |

---

## 26. Future Improvements

- Deploy on Render / Railway / Azure
- Add PostgreSQL support for production *(partially done — `DATABASE_URL` support exists)*
- Add automated tests for core workflows
- Add API endpoints for mobile integration
- Add export functionality (PDF/CSV reports)
- Implement real ML-based suggestion engine
- Add collaborative study features
- Implement notification emails
- Add Pomodoro timer widget

---

## 27. License

This project is currently for **academic/personal use**. Add a license file (e.g., MIT) before open-source distribution.

---

> **Generated:** April 2026
> **Project:** AntiGravity_WPL — Digital Procrastination Analyzer
> **Author:** Dhruv Saraogi
