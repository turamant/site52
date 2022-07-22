#!/bin/bash
# pipenv shell

case $1 in
  dev)
    python manage.py runserver --settings=config.settings.dev
    ;;
  prod)
    python manage.py collectstatic --noinput
    python manage.py makemigrations
    python manage.py migrate
    gunicorn --bind 0.0.0.0:8001 config.wsgi
    ;;
esac