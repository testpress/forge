#!/bin/sh
set -e

python manage.py migrate --noinput
python manage.py collectstatic --noinput
# No-ops itself outside DEBUG, so this is safe to leave in a production image.
python manage.py seed_demo_data

exec "$@"
