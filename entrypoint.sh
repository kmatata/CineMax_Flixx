#! /bin/bash

python manage.py migrate
celery -A cineMania worker -l info
python manage.py runserver 0.0.0.0:8000
