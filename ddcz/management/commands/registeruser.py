from django.apps import apps
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError
from django.core.validators import validate_email

from ddcz.models import User, UserProfile


class Command(BaseCommand):
    help = """
    Register a user from console
    """

    def add_arguments(self, parser):
        parser.add_argument("nick", help="Unique nickname of the user")
        parser.add_argument("email", help="Unique email of the user")
        parser.add_argument("password", help="Password for log in")

    def handle(self, *args, **options):
        if User.objects.filter(username__iexact=options["nick"]).count() > 0:
            raise CommandError("User nickname already taken")

        if (
            UserProfile.objects.filter(nick_uzivatele__iexact=options["nick"]).count()
            > 0
        ):
            raise CommandError("User nickname already taken")

        if (
            UserProfile.objects.filter(email_uzivatele__iexact=options["email"]).count()
            > 0
        ):
            raise CommandError("User email already taken")

        validate_email(options["email"])

        # TODO/FIXME: Extract to method to be also used
        # for user registration
        self.valid_user = User.objects.create_user(
            username=options["nick"], password=options["password"]
        )

        self.valid_profile = UserProfile.objects.create(
            nick_uzivatele=options["nick"],
            email_uzivatele=options["email"],
            user=self.valid_user,
        )
