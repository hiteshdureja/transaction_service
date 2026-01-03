#!/bin/bash
set -e

# Run migrations
echo "Running database migrations..."
python manage.py migrate --noinput

# Collect static files (if any)
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear || true

# Start Gunicorn
echo "Starting Gunicorn..."
exec "$@"

