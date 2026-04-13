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
python manage.py seed_platform_data
python manage.py seed_curriculum_data
python manage.py seed_structured_diagnostic_quiz
python manage.py migrate_progress_ids
python manage.py hydrate_all_lessons
python manage.py update_lesson_challenges
