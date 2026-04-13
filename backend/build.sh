#!/usr/bin/env bash
# exit on error
set -o errexit

# Build script for Render
python -m pip install --upgrade pip
pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate
python manage.py ensure_superuser --noinput
python manage.py seed_platform_data
python manage.py seed_curriculum_data
python manage.py seed_structured_diagnostic_quiz
python manage.py hydrate_all_lessons
python manage.py update_lesson_challenges
