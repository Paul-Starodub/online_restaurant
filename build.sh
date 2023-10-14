#!/usr/bin/env bash
# exit on error
set -o errexit
chmod -R a+w /media/uploads/dishes
chmod -R a+w /media/uploads/users
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
celery -A online_restaurant worker -l INFO
