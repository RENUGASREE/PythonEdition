import os
import sys
import logging

from django.apps import AppConfig
from django.core.management import call_command
from django.db import connection

logger = logging.getLogger(__name__)


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        # Auto-run migrations, superuser creation, and data seeding on startup
        # This ensures database is properly initialized on deployment
        if os.environ.get('RUN_AUTO_STARTUP', 'true').lower() in ('1', 'true', 'yes'):
            try:
                # Run migrations to create database tables
                print("Running database migrations...")
                call_command('migrate', '--run-syncdb', verbosity=0)
                print("Migrations completed successfully")
                
                # Create superuser if environment variables are set
                if all([
                    os.environ.get('DJANGO_SUPERUSER_USERNAME'),
                    os.environ.get('DJANGO_SUPERUSER_EMAIL'),
                    os.environ.get('DJANGO_SUPERUSER_PASSWORD')
                ]):
                    try:
                        print("Creating superuser...")
                        call_command('create_superuser_env', verbosity=0)
                        print("Superuser created successfully")
                    except Exception as e:
                        print(f"Superuser may already exist: {e}")
                
                # Seed platform data
                try:
                    print("Seeding platform data...")
                    call_command('seed_platform_data', verbosity=0)
                    print("Platform data seeded successfully")
                except Exception as e:
                    print(f"Data seeding may have already run: {e}")
                    
            except Exception as e:
                print(f"Auto-startup error: {e}")
