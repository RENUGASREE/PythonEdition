import os
import sys
import logging

from django.apps import AppConfig

logger = logging.getLogger(__name__)


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        # Automatically seed curriculum content and/or create a superuser in production.
        # Only run in a server runtime (gunicorn/runserver), not during migrations or management commands.
        if any(arg in sys.argv for arg in ("makemigrations", "migrate", "collectstatic", "test", "shell")):
            return

        # Auto-create a superuser if requested via environment variables.
        if os.getenv("CREATE_SUPERUSER_ON_STARTUP", "").strip().lower() in ("1", "true", "yes"):
            try:
                from django.contrib.auth import get_user_model

                User = get_user_model()
                username = os.getenv("SUPERUSER_USERNAME")
                email = os.getenv("SUPERUSER_EMAIL")
                password = os.getenv("SUPERUSER_PASSWORD")

                if username and email and password and not User.objects.filter(username=username).exists():
                    User.objects.create_superuser(username=username, email=email, password=password)
                    logger.info("Created superuser %s", username)
            except Exception as e:
                logger.exception("Failed to create superuser on startup: %s", e)

        # Auto-seed curriculum data if requested and if it's missing.
        if os.getenv("SEED_CURRICULUM_ON_STARTUP", "").strip().lower() in ("1", "true", "yes"):
            try:
                from django.core.management import call_command
                from core.models import Lesson

                if not Lesson.objects.exists():
                    call_command("seed_curriculum_data")
                    logger.info("Seeded curriculum data on startup")
                    
                    # Hydrate detailed content for all modules using high-quality content
                    logger.info("Hydrating detailed lesson content...")
                    hydrate_commands = [
                        'hydrate_module1', 'hydrate_module1_b',
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
                            logger.info("Hydrated %s successfully", cmd)
                        except Exception as e:
                            logger.warning("Hydrate %s error: %s", cmd, e)
                    
                    # Seed additional data (certificates, badges, diagnostic quiz)
                    try:
                        call_command('seed_expanded_certificates', verbosity=0)
                        logger.info("Seeded expanded certificates")
                    except Exception as e:
                        logger.warning("Certificate seeding error: %s", e)
                    
                    try:
                        call_command('seed_expanded_badges', verbosity=0)
                        logger.info("Seeded expanded badges")
                    except Exception as e:
                        logger.warning("Badge seeding error: %s", e)
                    
                    # Expanded diagnostic quiz - THIS IS THE DIFFERENCE from Python project
                    try:
                        call_command('seed_expanded_diagnostic_quiz', verbosity=0)
                        logger.info("Seeded expanded diagnostic quiz")
                    except Exception as e:
                        logger.warning("Diagnostic quiz seeding error: %s", e)
                    
                    logger.info("All data seeding completed")
            except Exception as e:
                logger.exception("Failed to seed curriculum data on startup: %s", e)
