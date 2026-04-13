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
                    
                    # Hydrate detailed content for all modules
                    print("Hydrating detailed lesson content for all modules...")
                    hydrate_commands = [
                        'hydrate_module1', 'hydrate_module1_b', 'hydrate_module1_extra',
                        'hydrate_module2', 'hydrate_module2_b',
                        'hydrate_module3', 'hydrate_module3_b',
                        'hydrate_module4', 'hydrate_module4_b',
                        'hydrate_module5', 'hydrate_module5_b',
                        'hydrate_module6', 'hydrate_module6_b',
                        'hydrate_module7', 'hydrate_module7_b',
                        'hydrate_module8', 'hydrate_module8_b',
                        'hydrate_module9', 'hydrate_module9_b',
                        'hydrate_module10', 'hydrate_module10_b',
                    ]
                    for cmd in hydrate_commands:
                        try:
                            call_command(cmd, verbosity=0)
                            print(f"Hydrated {cmd} successfully")
                        except Exception as e:
                            print(f"Hydrate {cmd} error (may have already run): {e}")
                    print("Module hydration completed")
                    
                    # Seed additional required data
                    print("Seeding additional data (certificates, badges, challenges, diagnostic quiz)...")
                    try:
                        call_command('seed_certificate_templates', verbosity=0)
                        print("Certificate templates seeded successfully")
                    except Exception as e:
                        print(f"Certificate templates seeding error: {e}")
                    
                    try:
                        call_command('seed_sample_badges', verbosity=0)
                        print("Sample badges seeded successfully")
                    except Exception as e:
                        print(f"Sample badges seeding error: {e}")
                    
                    try:
                        call_command('seed_sample_challenges', verbosity=0)
                        print("Sample challenges seeded successfully")
                    except Exception as e:
                        print(f"Sample challenges seeding error: {e}")
                    
                    try:
                        call_command('seed_placement_quiz', verbosity=0)
                        print("Placement quiz seeded successfully")
                    except Exception as e:
                        print(f"Placement quiz seeding error: {e}")
                    
                    try:
                        call_command('seed_structured_diagnostic_quiz', verbosity=0)
                        print("Structured diagnostic quiz seeded successfully")
                    except Exception as e:
                        print(f"Structured diagnostic quiz seeding error: {e}")
                    
                    print("All data seeding completed")
                    
                except Exception as e:
                    print(f"10-module curriculum seeding error: {e}")
                    
            except Exception as e:
                print(f"Auto-startup error: {e}")
