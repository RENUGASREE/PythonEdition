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
        if os.environ.get('RUN_AUTO_STARTUP', 'false').lower() in ('1', 'true', 'yes'):
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
                    
                    # Hydrate detailed content for all modules (comprehensive)
                    print("Hydrating detailed lesson content for all 300 lessons...")
                    try:
                        call_command('hydrate_all_lessons', verbosity=0)
                        print("All lessons hydrated successfully")
                    except Exception as e:
                        print(f"Hydrate all lessons error: {e}")
                    print("Module hydration completed")
                    
                    # Seed additional required data
                    print("Seeding additional data (certificates, badges, challenges, diagnostic quiz)...")
                    try:
                        call_command('seed_expanded_certificates', verbosity=0)
                        print("Expanded certificate templates seeded successfully")
                    except Exception as e:
                        print(f"Expanded certificate templates seeding error: {e}")
                    
                    try:
                        call_command('seed_expanded_badges', verbosity=0)
                        print("Expanded badges seeded successfully")
                    except Exception as e:
                        print(f"Expanded badges seeding error: {e}")
                    
                    try:
                        call_command('seed_sample_challenges', verbosity=0)
                        print("Sample challenges seeded successfully")
                    except Exception as e:
                        print(f"Sample challenges seeding error: {e}")
                    
                    try:
                        call_command('seed_expanded_diagnostic_quiz', verbosity=0)
                        print("Expanded diagnostic quiz seeded successfully")
                    except Exception as e:
                        print(f"Expanded diagnostic quiz seeding error: {e}")
                    
                    print("All data seeding completed")
                    
                except Exception as e:
                    print(f"10-module curriculum seeding error: {e}")
                    
            except Exception as e:
                print(f"Auto-startup error: {e}")
