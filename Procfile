web: gunicorn --config gunicorn.conf.py project_a_17.wsgi

# TODO: look into this line (it was in the Heroku tutorial)
# Uncomment this `release` process if you are using a database, so that Django's model
# migrations are run as part of app deployment, using Heroku's Release Phase feature:
# https://docs.djangoproject.com/en/6.0/topics/migrations/
# https://devcenter.heroku.com/articles/release-phase
#release: ./manage.py migrate --no-input