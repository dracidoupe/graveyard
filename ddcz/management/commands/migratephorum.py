import logging
import sys

from django.core.management.base import BaseCommand

from ddcz.models import Phorum, UserProfile
from ddcz.text import misencode

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Fills in reference to User object into Phorum"

    def handle(self, *args, **options):
        for i, comment in enumerate(Phorum.objects.filter(user__isnull=True), start=1):
            if i % 100 == 0:
                sys.stdout.write(".")
                sys.stdout.flush()
            if comment.by_registered_user:
                try:
                    comment.user = UserProfile.objects.get(
                        nick=misencode(comment.nickname)
                    )
                    comment.save()

                except UserProfile.DoesNotExist:
                    logger.info(f"Can't find author for nickname {comment.nickname}")
