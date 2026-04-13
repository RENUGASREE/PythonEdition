from django.core.management.base import BaseCommand
from gamification.models import Badge

class Command(BaseCommand):
    help = "Seed 100+ badges for 300 lessons (completion, streaks, achievements)"

    def handle(self, *args, **options):
        modules = [
            "Python Basics", "Data Types", "Control Flow", "Functions",
            "Modules & Packages", "File Handling", "Error Handling",
            "OOP", "Advanced Python", "Real-world Projects"
        ]
        difficulties = ["Beginner", "Intermediate", "Pro"]
        
        badges = []
        
        # Lesson completion badges (30 badges - 10 modules × 3 difficulties)
        for i, module in enumerate(modules, start=1):
            for diff in difficulties:
                code = f"lesson-complete-{i}-{diff.lower()}"
                title = f"{module} {diff} Master"
                desc = f"Complete all {diff.lower()} lessons in {module}"
                badges.append((code, title, desc))
        
        # Module completion badges (10 badges)
        for i, module in enumerate(modules, start=1):
            code = f"module-complete-{i}"
            title = f"{module} Master"
            desc = f"Complete all lessons in {module}"
            badges.append((code, title, desc))
        
        # Streak badges (10 badges)
        for days in [3, 7, 14, 30, 60, 90, 180, 365, 500, 730]:
            code = f"streak-{days}-days"
            title = f"{days} Day Streak"
            desc = f"Maintain a learning streak for {days} days"
            badges.append((code, title, desc))
        
        # XP achievement badges (10 badges)
        for xp in [100, 500, 1000, 2500, 5000, 10000, 25000, 50000, 100000, 250000]:
            code = f"xp-{xp}"
            title = f"{xp} XP Earned"
            desc = f"Earn {xp} total experience points"
            badges.append((code, title, desc))
        
        # Quiz perfection badges (5 badges)
        for count in [10, 25, 50, 100, 200]:
            code = f"quiz-perfect-{count}"
            title = f"{count} Perfect Quizzes"
            desc = f"Complete {count} quizzes with 100% score"
            badges.append((code, title, desc))
        
        # Challenge mastery badges (5 badges)
        for count in [10, 25, 50, 100, 200]:
            code = f"challenge-master-{count}"
            title = f"{count} Challenges Solved"
            desc = f"Successfully complete {count} coding challenges"
            badges.append((code, title, desc))
        
        # Speed badges (5 badges)
        for speed in ["fast", "faster", "fastest", "lightning", "godspeed"]:
            code = f"speed-{speed}"
            title = f"{speed.capitalize()} Learner"
            desc = f"Complete lessons at {speed} pace"
            badges.append((code, title, desc))
        
        # Special achievement badges (10 badges)
        special = [
            ("first-lesson", "First Steps", "Complete your very first lesson"),
            ("first-quiz", "Quiz Novice", "Complete your first quiz"),
            ("first-challenge", "Code Warrior", "Complete your first challenge"),
            ("perfect-module", "Module Perfectionist", "Complete a module with 100% on all quizzes"),
            ("night-owl", "Night Owl", "Study between 10PM - 2AM"),
            ("early-bird", "Early Bird", "Study between 6AM - 9AM"),
            ("weekend-warrior", "Weekend Warrior", "Study 10+ hours on weekend"),
            ("consistency-king", "Consistency King", "Study every day for a month"),
            ("helper", "Helper", "Help other learners (future feature)"),
            ("explorer", "Explorer", "Try all difficulty levels"),
        ]
        badges.extend(special)
        
        count = 0
        for code, title, desc in badges:
            obj, created = Badge.objects.get_or_create(
                code=code,
                defaults={"title": title, "description": desc}
            )
            if created:
                count += 1
                self.stdout.write(f"  ✅ Created: {title}")
            else:
                obj.title = title
                obj.description = desc
                obj.save()
                self.stdout.write(f"  🔄 Updated: {title}")
        
        self.stdout.write(self.style.SUCCESS(f"\n🎉 Seeded {len(badges)} badges ({count} new)"))
