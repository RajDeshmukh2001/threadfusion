#!/bin/sh

# Collect static files
python manage.py collectstatic --noinput

# Start Gunicorn web server
exec gunicorn --bind 0.0.0.0:${PORT:-8000} capstone.wsgi:application