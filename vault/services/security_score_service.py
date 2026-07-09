
from ..model.user_model import Profile, LoginLog


def calculate_security_score(user):

    profile = Profile.objects.get(user=user)

    score = 0

    # PROFILE COMPLETION
    if profile.profile_completed:
        score += 10

    # 2FA
    if profile.two_factor_enabled:
        score += 20

    # WEAK PASSWORDS
    if profile.weak_password_count == 0:
        score += 20
    else:
        score += max(0, 20 - (profile.weak_password_count * 2))

    # REUSED PASSWORDS
    if profile.reused_password_count == 0:
        score += 20
    else:
        score += max(0, 20 - (profile.reused_password_count * 2))

    # LOGIN ANALYSIS
    blocked_count = LoginLog.objects.filter(
        user=user,
        status='BLOCKED'
    ).count()

    if blocked_count == 0:
        score += 10
    else:
        score += max(0, 10 - blocked_count)

    # BASE SECURITY
    score += 20

    # LIMIT
    score = min(score, 100)

    profile.security_score = score
    profile.save()

    return score
