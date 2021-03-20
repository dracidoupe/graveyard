import logging

from django import forms
from django.contrib.auth import forms as authforms

from ..models import UserProfile

logger = logging.getLogger(__name__)


class LoginForm(forms.Form):
    nick = forms.CharField(label="Nick", max_length=20)
    password = forms.CharField(label="Heslo", max_length=50, widget=forms.PasswordInput)


class PasswordResetForm(authforms.PasswordResetForm):
    def get_users(self, email):
        """Given an email, return matching user(s) who should receive a reset.
        This is overridem from original form to use UserProfile instead of standard
        user model since that is normative for email storage.
        """

        user_profiles = UserProfile.objects.filter(email_uzivatele__iexact=email)

        users = tuple(
            list(
                up.user
                for up in user_profiles
                if up.user.has_usable_password() and up.user.is_active
            )
        )

        logger.info(
            "Selected users for password reset: %s"
            % ", ".join([str(u.pk) for u in users])
        )

        return users
