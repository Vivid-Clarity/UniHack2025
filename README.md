# Job Capsules

A career companion web app built for UniHack 2025. Job Capsules brings job searching, career events, and AI-powered career guidance together in one place, so students and early-career folks can manage their job hunt without juggling five different tabs.

Built with Flask, vanilla JS, and a handful of external APIs.

---

## Quick start

**Requirements:** Python 3.9+ (developed on 3.13)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the app
python main.py
```

Then open **http://127.0.0.1:5000/** in your browser.

The Flask dev server runs with `debug=True`, so it hot-reloads as you edit templates and Python files.

---

## Features

### Job Search — live

Search real job listings from across Australia, powered by the [Adzuna API](https://developer.adzuna.com/).

- Keyword search from the homepage or directly on the Job Tracker page
- Results render as cards with title, company, location, and description
- "Apply Now" links straight through to the original posting
- Search terms carry over from the homepage via the URL (`/jobTracker?search=ai`)

### Event Finder — live

Browse and filter career events: networking nights, workshops, hackathons, conferences, and meetups.

- Filter by title, organizer, tag, or location
- Event cards show date, location, host, description, and tags
- Currently serves a curated set of 20 events from a built-in dataset — the API layer is already in place, so swapping in a live events feed is a drop-in change

### AI Career Recommender — live

Get a personalized career pathway suggestion based on your background.

- Enter your skills, interests, education, and years of experience
- Sends the profile to DeepSeek (via OpenRouter) for a tailored recommendation
- Returns advice written in the voice of a career advisor

### Resume Builder — in progress

Fill in your details and get a formatted resume preview.

The form and preview layout are built and styled. Two pieces are still being wired up:

- **Extended fields** — the preview is scaffolded for work experience, education, skills, certifications, projects, languages, and interests. The matching form inputs are the next thing to add, which will light up the full preview.
- **PDF export** — the "Download as PDF" button is in place and wired to `html2pdf.js`; including the library gets the download working end-to-end.

### Accounts & LinkedIn login — in progress

- **LinkedIn OAuth** — the full backend flow is implemented and working: authorization redirect, state validation (CSRF-protected), token exchange, and profile fetch via LinkedIn's OpenID Connect `userinfo` endpoint. It currently returns the profile payload directly; connecting that response to a user session is the remaining step.
- **Email login & registration** — the login modal and registration form are designed and styled. Adding the `/login` and `/register` routes plus a user store will connect them to the backend.

---

## Project structure

```
├── main.py                 # Flask app, page routes, job search + career API routes
├── api_adsuna.py           # Adzuna job search integration
├── api_deepseek.py         # DeepSeek / OpenRouter career recommendation integration
├── api_linkedin.py         # LinkedIn OAuth 2.0 blueprint
├── events_api.py           # Events blueprint + event dataset
├── test_adsuna_api.py      # Standalone script for testing Adzuna calls
├── requirements.txt
├── templates/
│   ├── base.html           # Shared layout: header, nav, login modal, footer
│   ├── index.html          # Homepage
│   ├── job-tracker.html    # Job search + results
│   ├── event-finder.html   # Event listings + search
│   ├── career-recommender.html
│   ├── resume-builder.html
│   ├── register.html
│   ├── navbar.html         # Standalone nav partial
│   ├── job-card.html
│   └── event-card.html
└── static/
    ├── styles.css
    └── docs/               # Logo and icons
```

---

## Routes

### Pages

| Route                 | Description                    |
| --------------------- | ------------------------------ |
| `/`                   | Homepage with job search        |
| `/jobTracker`         | Job search and results          |
| `/eventFinder`        | Career events listing           |
| `/careerRecommender`  | AI career pathway form          |
| `/resumeBuilder`      | Resume builder and preview      |

### API

| Endpoint                                     | Method | Description                                |
| -------------------------------------------- | ------ | ------------------------------------------ |
| `/api/searchJobs?query=&location=`           | GET    | Job search via Adzuna                      |
| `/api/events`                                | GET    | All events                                 |
| `/api/events/search?query=&location=`        | GET    | Filtered events                            |
| `/api/recommendCareer`                       | POST   | AI career recommendation (JSON body)       |
| `/auth/linkedin`                             | GET    | Start LinkedIn OAuth flow                  |
| `/auth/linkedin/callback`                    | GET    | OAuth callback and profile fetch           |

---

## Configuration

The app talks to three external services:

| Service                 | Used for                     | Where it's configured |
| ----------------------- | ---------------------------- | --------------------- |
| Adzuna                  | Job listings                 | `api_adsuna.py`       |
| OpenRouter (DeepSeek)   | Career recommendations       | `api_deepseek.py`     |
| LinkedIn                | OAuth login                  | `api_linkedin.py`     |

Credentials currently live inline in those modules, which kept setup friction near zero during the hackathon. Moving them into environment variables (via `os.environ` and a `.env` file) is a worthwhile next step before this goes anywhere public — and it makes swapping in your own keys much easier.

The LinkedIn redirect URI is set to `http://127.0.0.1:5000/auth/linkedin/callback`, so run the app on port 5000 for the OAuth flow to complete.

---

## Roadmap

- [ ] Add the remaining resume form fields and include `html2pdf.js` for PDF export
- [ ] Add `/login` and `/register` routes with a user store
- [ ] Connect the LinkedIn OAuth result to a logged-in session
- [ ] Add saved-jobs tracking so the Job Tracker persists applications and their status
- [ ] Swap the built-in event dataset for a live events feed
- [ ] Move API credentials to environment variables
- [ ] Wire up the "Register Now" button on event cards

---

## Tech stack

Flask · Jinja2 templates · vanilla JavaScript · CSS · Adzuna API · OpenRouter (DeepSeek) · LinkedIn OAuth 2.0
