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
                
                # Seed platform data with complete 10-module curriculum
                try:
                    print("Seeding 10-module curriculum structure...")
                    call_command('seed_curriculum', verbosity=0)
                    print("10-module curriculum structure seeded successfully")
                except Exception as e:
                    print(f"10-module curriculum seeding error, trying fallback: {e}")
                    # Fallback to curriculum data if 10-module fails
                    try:
                        print("Seeding curriculum data (fallback)...")
                        call_command('seed_curriculum_data', verbosity=0)
                        print("Curriculum data seeded successfully")
                    except Exception as e2:
                        print(f"Curriculum data seeding error, trying platform data: {e2}")
                        # Fallback to platform data if curriculum data fails
                        try:
                            print("Seeding platform data (fallback)...")
                            call_command('seed_platform_data', verbosity=0)
                            print("Platform data seeded successfully")
                        except Exception as e3:
                            print(f"Platform data seeding may have already run: {e3}")
                    
            except Exception as e:
                print(f"Auto-startup error: {e}")
