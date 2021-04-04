import sys

from django.apps import apps
from django.core.management.base import BaseCommand, CommandError

from ddcz.models import CreativePage
from ddcz.html import check_creation_html, HtmlTagMismatchException


class Command(BaseCommand):
    help = """
    Go through all creations and print out URLs of those failing HTML check.
    """

    def handle(self, *args, **options):
        errors_no = 0
        models_no = 0
        creations_no = 0

        for model in CreativePage.get_all_models():
            model = model["model"]
            models_no += 1
            for creation in model.objects.all():
                if hasattr(model, "legacy_html_attributes"):
                    creations_no += 1
                    for attr in model.legacy_html_attributes:
                        try:
                            check_creation_html(getattr(creation, attr))
                        except HtmlTagMismatchException as err:
                            errors_no += 1
                            # TODO: Get canonical URL
                            message = f"HTML errors for creation model {str(model)} ID {creation.pk}: {str(err)} \n"
                            sys.stderr.write(message)

        if errors_no == 0:
            sys.stdout.write(
                f"All checks OK! {models_no} models with {creations_no} creations checked. \n"
            )
            sys.stdout.flush()
        else:
            sys.stderr.flush()
            raise CommandError(f"HTML is not fixed everywhere yet: {errors_no} remaining. Check stderr output.")
