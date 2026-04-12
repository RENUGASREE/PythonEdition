import os
import sys
import logging

from django.apps import AppConfig

logger = logging.getLogger(__name__)


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        # Disabled auto-startup logic for production deployment
        # Superuser creation and data seeding are handled in build command
        # This prevents deployment errors from database access during startup
        pass
