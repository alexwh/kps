#!/usr/bin/env bash
(pipenv run python manage.py qcluster &
pipenv run python manage.py runserver)
