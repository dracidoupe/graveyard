import logging

from django.core.management.base import BaseCommand

from ddcz.tavern import migrate_tavern_access

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Migrate Tavern Access structures from v0 to v1"

    def handle(self, *args, **options):
        migrate_tavern_access(print_progress=True)
