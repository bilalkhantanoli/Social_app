#!/bin/bash
python manage.py fix_db_sequences
python manage.py collectstatic --noinput
python manage.py migrate
python manage.py fix_db_sequences
gunicorn --bind=0.0.0.0 --timeout 600 socialapp.wsgi
