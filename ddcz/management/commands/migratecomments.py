import logging
import sys

from django.core.management.base import BaseCommand

from ddcz.models import CreationComment, UserProfile
from ddcz.text import misencode

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Fills in reference to User object into CreationComments"

    def handle(self, *args, **options):
        i = 0
        for comment in CreationComment.objects.filter(user__isnull=True):
            i += 1
            if i % 100 == 0:
                sys.stdout.write(".")
                sys.stdout.flush()
            try:
                comment.user = UserProfile.objects.get(nick=misencode(comment.nickname))
                comment.save()

            except UserProfile.DoesNotExist:
                logger.info("Can't find author for nickname %s" % comment.nickname)
