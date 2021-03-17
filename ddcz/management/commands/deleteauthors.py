from django.apps import apps
from django.core.management.base import BaseCommand, CommandError

from ddcz.models import Author


class Command(BaseCommand):
    help = """
    Delete all data from Author table and associated references.
    Will be forbiddn to run on production (at one point)
    """

    def handle(self, *args, **options):
        Author.objects.all().delete()
