#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate
curl -O https://github.com/stripe/stripe-cli/releases/download/v1.7.0/stripe_1.7.0_darwin_amd64.tar.gz
tar xvf stripe_1.7.0_darwin_amd64.tar.gz
sudo mv stripe /usr/local/bin/
stripe listen --forward-to https://online-restauraut.onrender.com:8000/webhook/stripe/ &
celery -A online_restaurant worker -l INFO &
