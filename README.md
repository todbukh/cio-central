## Dev & Deployment

### 1. Requirements/Deps
```bash
pip install -r requirements.txt # Install
pip freeze > requirements.txt   # Update
```

### 2. Local Development
Runs at [http://localhost:5006/](http://localhost:5006/) Use following commands for dev/prod parity:

* **Mac/Linux:** `heroku local --port 5006`
* **Windows:** `heroku local --port 5006 -f Procfile.windows`

### 3. Deployment
```bash
git push heroku main
```

**You cannot commit directly to main. It is disallowed by the GitHub. Make sure to commit to a non-protected branch and PR + get at least one other team member's approval to modify main.**

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
