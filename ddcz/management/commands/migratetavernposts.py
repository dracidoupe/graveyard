import logging
import sys

from django.core.management.base import BaseCommand

from ddcz.models import TavernPost, UserProfile
from ddcz.text import misencode

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Fills in reference to User object into CreationComments"

    def add_arguments(self, parser):
        parser.add_argument(
            "--batch-size",
            action="store",
            dest="batch_size",
            help="Limit the amount of processed posts",
        )

    def handle(self, *args, **options):
        i = 0
        total_no = TavernPost.objects.filter(user__isnull=True).count()
        logger.info(f"Found {total_no} posts for migration")
        query = TavernPost.objects.filter(user__isnull=True)
        logger.info(f"Migrating Tavern Posts, batch size {options['batch_size']}")
        if "batch_size" in options and options["batch_size"]:
            query = query[0 : int(options["batch_size"])]
        for comment in query:
            i += 1
            if i % 10 == 0:
                sys.stdout.write(".")
                sys.stdout.flush()
            try:
                comment.user = UserProfile.objects.get(nick=misencode(comment.nickname))
                comment.save()

            except UserProfile.DoesNotExist:
                logger.info("Can't find author for nickname %s" % comment.nickname)
