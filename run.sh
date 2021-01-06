#!/usr/bin/env bash
pipenv run python manage.py migrate
(pipenv run python manage.py qcluster &
pipenv run daphne -b 0.0.0.0 -p 8000 kps.asgi:application)
