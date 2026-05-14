# CIO Central

A full-stack organization management platform built for UVA student organizations (CIOs), designed so that a fresh instance can be independently deployed for any group. Built by a team of six across a six-sprint agile workflow as a semester-long software engineering course project.

**Stack:** Python 3 · Django 6 · PostgreSQL · Amazon S3 · Heroku · GitHub Actions CI · Bootstrap (custom SCSS theme)

---

## Features

### For Members
- **Google OAuth authentication** — sign in with a Google account; new accounts enter a pending approval queue before gaining access
- **Channel-based messaging** — persistent message board organized into channels (e.g. general, announcements). Members can post and delete their own messages. Poll and event announcements render as rich cards with inline links rather than plain text
- **Events** — browse upcoming and past org events with date, location, and description
- **Polls** — vote on executive-created polls and view live results with percentages
- **Member profiles** — profile pages with S3-backed profile picture uploads and a bio
- **Document library** — access shared org files stored on Amazon S3

### For Executives
- **Roster management** — three-tab view across active members, pending applications, and banned/rejected users. Executives can approve, reject, or ban members; owners can promote members to executive
- **Attendance tracking** — per-event attendance management with Present, Absent, Excused, and Unset statuses. Attendance records are lazily created for all approved members when an executive opens an event, then saved as statuses are updated
- **Analytics dashboard** — executive-only view with summary cards (total members, total events, average attendance), a bar chart of recent event turnout, and a per-user or per-event table with attendance rates. Drills down to a per-member attendance history page
- **Poll creation** — create polls with multiple options; publishing a poll automatically posts an announcement to the announcements channel as an atomic transaction
- **Channel management** — create, edit, and delete custom channels; mark channels as exec-only to restrict posting
- **Event management** — full CRUD for events with exec-only create/edit/delete controls
- **Organization settings** — edit the org name, description, and logo (S3-backed); owner-only access

### Administration
- **User Administrator role** — a sandboxed role creatable only via Django Admin, with its own isolated login at `/user-admin/login/`. User Admins can set any non-USERADMIN member's role (Member, Executive, Owner) and status (Approved, Pending, Rejected, Banned), but have no access to any other part of the application. Middleware enforces this isolation on every request
- **Account deletion** — owners can delete any account, executives can delete non-executives, and members can delete their own. Deletion uses a soft-delete sentinel pattern: rather than cascade-deleting related records, messages, attendance entries, and events are reassigned to a placeholder account so historical data is preserved

---

## Architecture

The project is organized as a collection of Django apps, each owning a specific domain:

| App | Responsibility |
|---|---|
| `core` | Custom user model, Google OAuth, role decorators, auth middleware |
| `profiles` | Profile pages, profile editing, account deletion |
| `events` | Event creation and management |
| `attendance` | Per-event attendance records and status tracking |
| `organization` | Channels, messaging, poll/event announcement enrichment |
| `documents` | S3-backed file uploads and document library |
| `polls` | Poll creation, voting, and result aggregation |
| `roster` | Member roster with application and ban management |
| `analytics` | Attendance analytics aggregated by user and event |
| `exec_panel` | Executive panel shell that namespaces exec-only routes |
| `organization_edit` | Org name, description, and logo settings |
| `user_admin` | Sandboxed User Administrator panel with its own auth flow |

---

## My Contributions

I served as **Requirements Lead**, responsible for stakeholder interviews, requirements elicitation, and backlog management in GitHub Issues. You can see the results of the requirements elicitation process [here](https://docs.google.com/document/d/1HgAqRqKNzDxtxvj-1WTxY3jIGjC8BJbroECBOESJKpk/edit?usp=sharing) as well as a [Change Impact Report](https://docs.google.com/document/d/1mIpiJqFtgGFH2_hsbgJMJP7pBYkuGl-zF2NvH5xFvfA/edit?usp=sharing) that was compiled in response to a major requirements change (a new "site administrator" role was added) during development.

Beyond that role, I was one of the primary backend and frontend contributors:

- **Attendance system** — built end-to-end: models, migrations, and views including lazy bulk creation of attendance records on event open, status updates (Present/Absent/Excused/Unset), and executive-only access guards
- **Roster** — built the three-tab roster view (active members, pending applications, banned/rejected) and all associated actions: approve, reject, ban, role promotion, and application restore
- **Account deletion** — designed and implemented the full deletion feature including role-aware permission logic (owner, executive, self), a confirmation modal, and the soft-delete sentinel pattern that reassigns historical records rather than destroying them
- **Organization page layout** — contributed to the structure and layout of the main messaging/home page
- **Code reviews** — reviewed teammate PRs throughout the project, catching bugs and providing feedback on architecture and implementation

---

## Running Locally

### Prerequisites
- Python 3.14+
- Node LTS (via nvm)
- A Google OAuth client ID and secret ([Google Cloud Console](https://console.cloud.google.com/))

### Setup

```bash
git clone https://github.com/todbukh/cio-central.git
cd cio-central

python -m venv .env
source .env/bin/activate  # Windows: .env\Scripts\activate

pip install -r requirements.txt
npm install
```

Create a `.env` file in the project root:

```
ENVIRONMENT=development
DJANGO_SECRET_KEY=any-random-string
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
```

Add this redirect URI in the Google Cloud Console:
```
http://localhost:8000/accounts/google/login/callback/
```

Then run:

```bash
python manage.py migrate

# Terminal 1 — SCSS watcher
npm run dev

# Terminal 2 — Dev server
heroku local --port 8000          # Mac/Linux
heroku local --port 8000 -f Procfile.windows  # Windows
```

App runs at [http://localhost:8000](http://localhost:8000).
