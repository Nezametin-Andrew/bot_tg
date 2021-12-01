#! /bin/bash

python manage.py makemigrations app --no-input

python manage.py migrate --no-input

python manage.py collectstatic --no-input

cp templates_admin/*.html /usr/local/lib/python3.8/site-packages/django/contrib/admin/templates/admin/

exec gunicorn dj_bot.wsgi:application -b 0.0.0.0:8000 --reload
