## Getting Started

### Prerequisites

- **Python 3.14.0rc2** (see `.python-version`) — install via `pyenv install 3.14.0rc2`
- **Heroku CLI** — [Install guide](https://devcenter.heroku.com/articles/heroku-cli)
- **Git**
- **Node** - install nvm via `curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.4/install.sh | bash`
  - Then, run `nvm install --lts` and `nvm use --lts` (node version 24.14.0)

### 1. Clone the repo

```bash
git clone https://github.com/uva-cs3240-s26/project-a-17.git
cd project-a-17
```

### 2. Create a virtual environment

```bash
python -m venv .env
source .env/bin/activate        # Mac/Linux
# .env\Scripts\activate         # Windows
```

### 3. Install dependencies

Python Deps:

```bash
pip install -r requirements.txt
```

JS Deps:

```bash
npm install
```

### 4. Set up your `.env` file

Create a `.env` file in the project root (it is gitignored). This file is loaded automatically by `heroku local`:

```
ENVIRONMENT=development
DJANGO_SECRET_KEY=any-random-string-for-local-dev
```

`ENVIRONMENT=development` enables Django's debug mode and gunicorn auto-reload. `DJANGO_SECRET_KEY` is required by Django — use any random value locally.

### 5. Run database migrations

The local dev setup uses SQLite, so no Postgres install is needed:

```bash
python manage.py migrate
```

### 6. Run npm to compile bootstrap theme override
```bash
npm run dev
```

### 7. Run the development server

Keeping the npm development sass watcher running, open a new terminal tab and run the dev server:

Runs at [http://localhost:8000/](http://localhost:8000/):

**Mac/Linux:**
```bash
heroku local --port 8000
```

**Windows:**
```bash
heroku local --port 8000 -f Procfile.windows
```

### Adding dependencies

```bash
pip install <package>
pip freeze > requirements.txt   # Update the lockfile before committing
```

---

## Deployment

Deployment happens automatically when you push to main, so ensure that PRs to main are fully functional

**You cannot commit directly to main. It is disallowed by GitHub. Make sure to commit to a non-protected branch and PR + get at least one other team member's approval to modify main.**

## Team Expectations:
* **Communicate in advance** when you will be unable to make meetings, engagements, or deadlines for assigned tasks.
  * Things happen, but if this becomes a habit, it will be important to have a conversation.
* **Create and/or resolve GitHub issues** related to tasks you are tackling.
* **Make use of the project board.**
* **Respectfully communicate** with other team members, especially when in disagreement. Everyone’s ideas deserve to be respectfully heard.
* **Communicate in advance** if you are going to go in a different direction than initially discussed. Even a quick message is fine, but generally try to keep the team in the loop.
* **Be direct.** If there are issues, it is better to discuss them in a direct but friendly way in order to resolve them.
* **Don’t be afraid to ask for help.** It is better to get help than to fail silently, and we are a team that all want to help each other out.

[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/F1hjDb63)
