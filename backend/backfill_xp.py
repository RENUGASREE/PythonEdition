from core.models import User, UserProgress
from gamification.models import XpEvent
from django.db.models import Sum
import logging

logger = logging.getLogger(__name__)

def backfill():
    users = User.objects.all()
    total_awarded = 0
    
    for user in users:
        # Get current XP
        current_xp = XpEvent.objects.filter(user=user).aggregate(Sum('points'))['points__sum'] or 0
        
        # Get completed lessons
        user_id = user.original_uuid or str(user.id)
        completed_progress = UserProgress.objects.filter(user_id=user_id, completed=True)
        completed_count = completed_progress.count()
        
        expected_xp = completed_count * 10
        
        if expected_xp > current_xp:
            gap = expected_xp - current_xp
            XpEvent.objects.create(
                user=user,
                points=gap,
                reason="Backfill: Lesson completions reward"
            )
            print(f"Awarded {gap} XP to {user.username} (Total lessons: {completed_count})")
            total_awarded += gap
        else:
            print(f"User {user.username} already has correct or more XP ({current_xp}) for {completed_count} lessons.")

    print(f"\nBackfill complete. Total XP awarded: {total_awarded}")

if __name__ == "__main__":
    backfill()
