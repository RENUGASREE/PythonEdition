#!/usr/bin/env bash
# exit on error
set -o errexit
set -e

# Build script for Render
echo "Building Python Edition Backend..."
python -m pip install --upgrade pip
pip install -r requirements.txt

echo "Collecting static files..."
python manage.py collectstatic --no-input

echo "Applying database migrations..."
python manage.py migrate

echo "Creating superuser..."
python manage.py ensure_superuser --noinput
python manage.py blackout_test
