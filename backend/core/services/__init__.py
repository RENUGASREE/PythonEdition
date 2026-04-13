"""Certificate awarding service for module completion"""
from django.utils import timezone
from core.models import User, Certificate, CertificateTemplate, UserMastery, Lesson
from gamification.models import Badge, UserBadge
from gamification.services import award_badge


def check_and_award_module_certificate(user: User, module_id: str, difficulty: str = None):
    """
    Check if user has completed a module and award appropriate certificate.
    
    Args:
        user: The user to check
        module_id: The module ID to check completion for
        difficulty: Optional difficulty level (Beginner, Intermediate, Pro)
    
    Returns:
        Certificate if awarded, None otherwise
    """
    # Get all lessons for this module
    lessons = Lesson.objects.filter(module_id=module_id)
    if difficulty:
        lessons = lessons.filter(difficulty=difficulty)
    
    total_lessons = lessons.count()
    if total_lessons == 0:
        return None
    
    # Check user progress for these lessons
    from core.models import UserProgress
    completed_lessons = UserProgress.objects.filter(
        user=user,
        lesson__in=lessons,
        completed=True
    ).count()
    
    # Award certificate if 80% or more completed
    if completed_lessons / total_lessons >= 0.8:
        # Determine certificate template code
        module_name = lessons.first().module_id.replace('mod-', '').replace('-', ' ').title()
        diff_suffix = difficulty.lower() if difficulty else 'completion'
        template_code = f"module-{module_id.split('-')[1] if '-' in module_id else 'completion'}-{diff_suffix}"
        
        # Fallback template codes
        template_codes_to_try = [
            f"module-{module_id.split('-')[1] if '-' in module_id else 'all'}-{diff_suffix}",
            "module-completion",
            "full-course"
        ]
        
        template = None
        for code in template_codes_to_try:
            try:
                template = CertificateTemplate.objects.get(code=code)
                break
            except CertificateTemplate.DoesNotExist:
                continue
        
        if not template:
            template = CertificateTemplate.objects.first()
        
        if template:
            # Check if certificate already exists
            existing = Certificate.objects.filter(
                user=user,
                module=module_id
            ).first()
            
            if not existing:
                certificate = Certificate.objects.create(
                    user=user,
                    module=module_id,
                    pdf_path=f"/certificates/{user.username}_{module_id}_{timezone.now().strftime('%Y%m%d')}.pdf",
                )
                return certificate
    
    return None


def check_and_award_lesson_badge(user: User, lesson_id: str):
    """
    Award badge for lesson completion.
    
    Args:
        user: The user to award badge to
        lesson_id: The lesson ID that was completed
    
    Returns:
        Badge if awarded, None otherwise
    """
    from core.models import UserProgress
    
    # Check if lesson is completed
    progress = UserProgress.objects.filter(
        user=user,
        lesson_id=lesson_id,
        completed=True
    ).first()
    
    if progress:
        lesson = progress.lesson
        module_num = lesson.module_id.split('-')[1] if '-' in lesson.module_id else '1'
        diff = lesson.difficulty.lower()
        
        # Try to find matching badge
        badge_code = f"lesson-complete-{module_num}-{diff}"
        try:
            badge = Badge.objects.get(code=badge_code)
            # Check if user already has this badge
            if not UserBadge.objects.filter(user=user, badge=badge).exists():
                award_badge(user, badge_code)
                return badge
        except Badge.DoesNotExist:
            pass
    
    return None


def check_and_award_module_badge(user: User, module_id: str):
    """
    Award badge for completing all lessons in a module.
    
    Args:
        user: The user to award badge to
        module_id: The module ID to check
    
    Returns:
        Badge if awarded, None otherwise
    """
    lessons = Lesson.objects.filter(module_id=module_id)
    total_lessons = lessons.count()
    
    if total_lessons == 0:
        return None
    
    from core.models import UserProgress
    completed_lessons = UserProgress.objects.filter(
        user=user,
        lesson__in=lessons,
        completed=True
    ).count()
    
    # Award module badge if all lessons completed
    if completed_lessons == total_lessons:
        module_num = module_id.split('-')[1] if '-' in module_id else '1'
        badge_code = f"module-complete-{module_num}"
        
        try:
            badge = Badge.objects.get(code=badge_code)
            if not UserBadge.objects.filter(user=user, badge=badge).exists():
                award_badge(user, badge_code)
                return badge
        except Badge.DoesNotExist:
            pass
    
    return None
