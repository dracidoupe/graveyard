from django.core.management.base import BaseCommand

from ddcz.email import send_email_batch
from ddcz.notifications import notify_scheduled


class Command(BaseCommand):
    help = "Send all scheduled notifications"

    def handle(self, *args, **options):
        notify_scheduled()
        send_email_batch()
