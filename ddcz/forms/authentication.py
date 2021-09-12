import logging

from django import forms
from django.contrib.auth import forms as authforms

from ..models import UserProfile
from ..users import migrate_user

logger = logging.getLogger(__name__)


class LoginForm(forms.Form):
    nick = forms.CharField(label="Nick", max_length=25)
    password = forms.CharField(
        label="Heslo", max_length=100, widget=forms.PasswordInput
    )


class PasswordResetForm(authforms.PasswordResetForm):
    def get_users(self, email):
        """Given an email, return matching user(s) who should receive a reset.
        This is overrides from original form to use UserProfile instead of standard
        user model since that is normative for email storage.
        """

        user_profiles = UserProfile.objects.filter(email__iexact=email)

        # Allow resetting password of users that were not migrated yet
        # This is the only moment beside login that supports migration
        for up in user_profiles:
            if not up.user:
                migrate_user(profile=up)

        users = tuple(
            list(
                up.user
                for up in user_profiles
                # Note that we are allowing password reset for users with unusable password; we expect not to
                # be using SSO etc.
                # Banned users should have is_active = False
                if up.user and up.user.is_active
            )
        )

        logger.info(
            "Selected users for password reset: %s"
            % ", ".join([str(u.pk) for u in users])
        )

        return users
