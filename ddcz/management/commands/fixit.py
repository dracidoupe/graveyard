from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = """
    It's broken. Fix it!
    Runs all recommended migrations. 
    """

    def handle(self, *args, **options):
        call_command("migrate")
        call_command("migrateauthors")
        call_command("migratecomments")
        call_command("migratephorum")
        call_command("loaddata", "pages")
        call_command("loaddata", "editorarticles")
        # call_command("loaddata", "creationexamples")
