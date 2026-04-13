import os
import django
from django.core.management.base import BaseCommand
from core.models import Lesson

class Command(BaseCommand):
    help = "CRITICAL TEST: Clear all lesson content to identify the active server."

    def handle(self, *args, **kwargs):
        self.stdout.write("💀 CRITICAL BLACKOUT TEST STARTING...")
        lessons = Lesson.objects.all()
        for lesson in lessons:
            lesson.content = "!!! BLACKOUT TEST ACTIVE - IF YOU SEE THIS, WE HAVE THE RIGHT SERVER !!!"
            lesson.title = f"[TEST] {lesson.title}"
            lesson.save()
        self.stdout.write(f"💀 BLACKOUT COMPLETE on {len(lessons)} lessons.")
