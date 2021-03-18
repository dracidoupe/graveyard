from django.contrib.auth.models import User


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

    # TODO: Presumably, we could fix more things during migration...like FKs.

    return user
