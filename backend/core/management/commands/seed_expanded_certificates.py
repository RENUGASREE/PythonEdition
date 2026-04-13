from django.core.management.base import BaseCommand
from core.models import CertificateTemplate

class Command(BaseCommand):
    help = "Seed 30 certificate templates for all modules x 3 difficulty levels"

    def handle(self, *args, **options):
        modules = [
            "Python Basics", "Data Types", "Control Flow", "Functions",
            "Modules & Packages", "File Handling", "Error Handling",
            "OOP", "Advanced Python", "Real-world Projects"
        ]
        difficulties = ["Beginner", "Intermediate", "Pro"]
        
        templates = []
        
        # Module-specific certificates by difficulty
        for i, module in enumerate(modules, start=1):
            for diff in difficulties:
                code = f"module-{i}-{diff.lower()}"
                title = f"{module} - {diff} Certificate"
                desc = f"Awarded for completing {module} at {diff.lower()} level"
                templates.append((code, title, desc))
        
        # Overall achievement certificates
        templates.extend([
            ("beginner-track", "Beginner Track Completion", "Awarded for completing all beginner lessons"),
            ("intermediate-track", "Intermediate Track Completion", "Awarded for completing all intermediate lessons"),
            ("pro-track", "Pro Track Completion", "Awarded for completing all pro lessons"),
            ("full-course", "Full Course Mastery", "Awarded for completing all 300 lessons"),
            ("perfect-score", "Perfect Score Achievement", "Awarded for 100% completion rate"),
            ("fast-learner", "Fast Learner Badge", "Awarded for completing course in record time"),
        ])
        
        count = 0
        for code, title, desc in templates:
            obj, created = CertificateTemplate.objects.get_or_create(
                code=code,
                defaults={"title": title, "description": desc}
            )
            if created:
                count += 1
                self.stdout.write(f"  Created: {title}")
            else:
                obj.title = title
                obj.description = desc
                obj.save()
                self.stdout.write(f"  Updated: {title}")
        
        self.stdout.write(self.style.SUCCESS(f"\nSeeded {len(templates)} certificate templates ({count} new)"))
