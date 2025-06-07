from datetime import datetime

from django.contrib.auth import logout
from django.contrib.auth.models import User

SESSION_KEYS_TO_PRESERVE = ["skin"]

ASSUMED_JOINED_DATE = datetime(2003, 1, 1)


def migrate_user(profile, password=""):
    """
    Create proper Django user for an existing UserProfile

    If the password is not given (because i.e. migration is happening on a password reset field),
    it's set to unusable password and password reset is required before logging in.
    """
    if not profile.last_login:
        profile.last_login = datetime.now()

    user = User.objects.create_user(
        id=profile.id,
        username=profile.nick,
        password=password,
        date_joined=profile.registration_approved_date or ASSUMED_JOINED_DATE,
        last_login=profile.last_login,
    )
    profile.user = user
    profile.save()

    if not password:
        user.set_unusable_password()
        user.save()

    # TODO: Presumably, we could fix more things during migration...like foreign keys.
    return user


def logout_user_without_losing_session(request):
    cache = {k: request.session.get(k) for k in SESSION_KEYS_TO_PRESERVE}
    logout(request)
    for key in cache:
        if cache[key]:
            request.session[key] = cache[key]
