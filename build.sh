#!/usr/bin/env bash
# exit on error
set -o errexit

curl -L https://github.com/stripe/stripe-cli/releases/latest/download/stripe-cli-darwin-amd64.tar.gz | tar xz -C /usr/local/bin/
pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate
stripe listen --forward-to https://online-restauraut.onrender.com:8000/webhook/stripe/ &
celery -A online_restaurant worker -l INFO &
