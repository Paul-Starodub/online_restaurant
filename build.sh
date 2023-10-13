#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate
stripe listen --forward-to https://online-restauraut.onrender.com:8000/webhook/stripe/ &
celery -A online_restaurant worker -l INFO &
