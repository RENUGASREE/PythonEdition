import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, UserProgress, Lesson
from gamification.services import add_xp, update_streak, award_badge

logger = logging.getLogger(__name__)

@receiver(post_save, sender=UserProgress)
def handle_user_progress_update(sender, instance, created, **kwargs):
    """
    Automate XP and badge awarding when a lesson is marked completed.
    """
    if instance.completed:
        # Find the actual User object
        # user_id in UserProgress might be original_uuid or str(id)
        user = User.objects.filter(original_uuid=instance.user_id).first()
        if not user:
            # Fallback to standard ID if user_id is a string representation of an int
            try:
                user = User.objects.filter(id=int(instance.user_id)).first()
            except (ValueError, TypeError):
                pass
        
        if user:
            # Check if XP for this lesson was already awarded to avoid duplicates
            from gamification.models import XpEvent
            reason = f"Lesson completed: {instance.lesson_id}"
            if not XpEvent.objects.filter(user=user, reason=reason).exists():
                add_xp(user, 10, reason)
                update_streak(user)
                logger.info(f"Automated XP awarded to {user.username} for lesson {instance.lesson_id}")
            
            # Badge checks for lesson counts
            completed_count = UserProgress.objects.filter(user_id=instance.user_id, completed=True).count()
            if completed_count >= 1:
                award_badge(user, "python-pioneer") # Example badge
            if completed_count >= 10:
                award_badge(user, "consistent-learner")
            if completed_count >= 25:
                award_badge(user, "topic-wizard")
        else:
            logger.warning(f"Could not find User for user_id {instance.user_id} in signals")
