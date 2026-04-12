from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
import os

User = get_user_model()

class Command(BaseCommand):
    help = 'Create superuser using environment variables'

    def handle(self, *args, **options):
        # Get environment variables
        username = os.getenv('DJANGO_SUPERUSER_USERNAME')
        email = os.getenv('DJANGO_SUPERUSER_EMAIL')
        password = os.getenv('DJANGO_SUPERUSER_PASSWORD')

        # Check if all required variables are set
        if not all([username, email, password]):
            self.stdout.write(
                self.style.ERROR('Please set DJANGO_SUPERUSER_USERNAME, DJANGO_SUPERUSER_EMAIL, and DJANGO_SUPERUSER_PASSWORD environment variables')
            )
            return

        try:
            # Check if user already exists
            if User.objects.filter(username=username).exists():
                self.stdout.write(
                    self.style.WARNING(f'User "{username}" already exists')
                )
                return

            # Create superuser
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created superuser: {username}')
            )
            
        except ValidationError as e:
            self.stdout.write(
                self.style.ERROR(f'Validation error: {e}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating superuser: {e}')
            )
