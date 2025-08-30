from .models import Badge, UserBadge, Activity
from django.utils import timezone

def award_points(user, points, description):
    """Award points to a user and log the activity"""
    user.points += points
    user.save()
    
    # Log the activity
    Activity.objects.create(
        user=user,
        activity_type='points_awarded',
        points_earned=points,
        description=description
    )

def check_badges(user):
    """Check if user has earned any new badges"""
    badges = Badge.objects.all()
    
    for badge in badges:
        # Check if user already has this badge
        if UserBadge.objects.filter(user=user, badge=badge).exists():
            continue
            
        # Check badge conditions
        earned = False
        
        if badge.points_required > 0 and user.points >= badge.points_required:
            earned = True
        elif badge.reports_required > 0 and user.reports.count() >= badge.reports_required:
            earned = True
        elif badge.special_condition == 'first_report' and user.reports.count() >= 1:
            earned = True
        elif badge.special_condition == 'validator' and user.validated_reports.count() >= 5:
            earned = True
            
        if earned:
            UserBadge.objects.create(user=user, badge=badge)
            # Award bonus points for earning a badge
            award_points(user, badge.points_required // 10, f"Earned badge: {badge.name}")

def gamification_context(request):
    """Context processor to add gamification data to all templates"""
    if request.user.is_authenticated:
        return {
            'user_points': request.user.points,
            'user_level': request.user.level,
            'user_badges': UserBadge.objects.filter(user=request.user).select_related('badge')[:5],
        }
    return {}