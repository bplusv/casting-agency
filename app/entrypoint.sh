#!/bin/bash
set -e
python manage.py db upgrade
if [ "$1" = 'development' ]; then
    export FLASK_APP=wsgi
    export FLASK_ENV=development
    flask run --host=0.0.0.0
else
    gunicorn --bind 0.0.0.0:$PORT wsgi
fi
