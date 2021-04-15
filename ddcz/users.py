from django.contrib.auth import logout
from django.contrib.auth.models import User

SESSION_KEYS_TO_PRESERVE = ["skin"]


def migrate_user(profile, password):
    """ Create proper Django user for an existing (presumably authenticated) UserProfile """
    user = User.objects.create_user(
        id=profile.id,
        username=profile.nick_uzivatele,
        password=password,
        date_joined=profile.reg_schval_datum,
        last_login=profile.pospristup,
    )
    profile.user = user
    profile.save()

    # TODO: Presumably, we could fix more things during migration...like foreign keys.

    return user


def logout_user_without_losing_session(request):
    cache = {k: request.session.get(k) for k in SESSION_KEYS_TO_PRESERVE}
    logout(request)
    for key in cache:
        if cache[key]:
            request.session[key] = cache[key]
