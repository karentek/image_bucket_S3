#!/bin/sh

echo "RUNNING MIGRATIONS"
python manage.py migrate

exec "$@"