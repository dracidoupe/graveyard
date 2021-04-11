import logging
import sys

from django.apps import apps
from django.core.management.base import BaseCommand, CommandError

from ddcz.models import CreationComment, UserProfile
from ddcz.text import misencode

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Fills in reference to User object into CreationComments"

    def handle(self, *args, **options):
        i = 0
        for comment in CreationComment.objects.all():
            i += 1
            if i % 100 == 0:
                sys.stdout.write(".")
                sys.stdout.flush()
            try:
                comment.user = UserProfile.objects.get(
                    nick_uzivatele=misencode(comment.nickname)
                )
                comment.save()

            except UserProfile.DoesNotExist:
                logger.info("Can't find author for nickname %s" % comment.nickname)
