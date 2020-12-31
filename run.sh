#!/usr/bin/env bash
(pipenv run python manage.py runserver &
pipenv run python manage.py qcluster)
