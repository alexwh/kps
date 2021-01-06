#!/usr/bin/env bash
pipenv run python manage.py migrate
(pipenv run python manage.py qcluster &
pipenv run python manage.py runserver 0.0.0.0:8000)
