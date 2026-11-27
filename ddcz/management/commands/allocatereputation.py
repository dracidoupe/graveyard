from django.core.management.base import BaseCommand

from ddcz.models import UserProfile

# Reputation allocation per level, per run
# Higher levels get more votes to distribute
ALLOCATION_PER_LEVEL = {
    "0": 1,
    "1": 2,
    "2": 3,
    "3": 4,
    "4": 5,
    "5": 6,
    "8": 6,
}

# Legacy DB uses tinyint unsigned for reputation_available
MAX_REPUTATION_AVAILABLE = 255

# Status "1" is banned, "4" is normal
ACTIVE_STATUS = "4"


class Command(BaseCommand):
    help = "Allocate reputation votes to active users based on their level"

    def handle(self, *args, **options):
        active_users = UserProfile.objects.filter(status=ACTIVE_STATUS)
        updated = 0

        for profile in active_users:
            allocation = ALLOCATION_PER_LEVEL.get(profile.level, 1)
            new_available = min(
                profile.reputation_available + allocation,
                MAX_REPUTATION_AVAILABLE,
            )
            if new_available != profile.reputation_available:
                profile.reputation_available = new_available
                profile.save(update_fields=["reputation_available"])
                updated += 1

        self.stdout.write(
            self.style.SUCCESS(f"Allocated reputation to {updated} users")
        )
