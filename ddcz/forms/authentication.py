import logging

from django import forms
from django.contrib.auth import forms as authforms

from ..models import UserProfile
from ..users import migrate_user

logger = logging.getLogger(__name__)


class LoginForm(forms.Form):
    nick = forms.CharField(label="Nick", max_length=25)
    password = forms.CharField(
        label="Heslo",
        max_length=100,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )


class PasswordResetForm(authforms.PasswordResetForm):
    def get_users(self, email):
        """Given an email, return matching user(s) who should receive a reset.
        This is overrides from original form to use UserProfile instead of standard
        user model since that is normative for email storage.
        """

        user_profiles = UserProfile.objects.filter(email__iexact=email)
        users = []

        # Allow resetting password of users that were not migrated yet
        # This is the only moment beside login that supports migration
        for up in user_profiles:
            if not up.user:
                logger.info(f"Migrating user profile {up.nick} to Django user")
                migrate_user(profile=up)
            if up.user and up.user.is_active:
                user = up.user
                # This is a bit hacky as we rely on Django not to save the changed email field (as we do not want to store email on Django field for time being),
                # however it's good enough hack to make emails to be sent for now.
                # Reconsider email handling once we're fully migrated and on lates Django
                user.email = up.email
                users.append(user)
            else:
                logger.warn(
                    f"NOT selecting user {up.nick} as a password reset candidate since user is not active or migration failed"
                )

        logger.info(
            "Selected users for password reset: %s"
            % ", ".join([str(u.pk) for u in users])
        )

        return tuple(users)
