import logging

from django.core.management.base import BaseCommand

from ddcz.creations import ApprovalChoices
from ddcz.models import CreativePage, Phorum, CreationComment, UserProfile

logger = logging.getLogger(__name__)

ACTIVE_STATUS = "4"
STAFF_LEVEL = "8"

# Level thresholds: (min_posts, min_creations, min_reputation)
# Level 0: No requirements (default)
# Level 1: Active in discussions
# Level 2: Reviews/votes on creations
# Level 3: Has published creations
# Level 4: Experienced creator with many works
# Level 5: Exceptional contributor
LEVEL_THRESHOLDS = {
    1: {"min_posts": 20, "min_creations": 0, "min_reputation": 10},
    2: {"min_posts": 50, "min_creations": 0, "min_reputation": 30},
    3: {"min_posts": 0, "min_creations": 3, "min_reputation": 20},
    4: {"min_posts": 20, "min_creations": 8, "min_reputation": 50},
    5: {"min_posts": 50, "min_creations": 15, "min_reputation": 100},
}


def count_user_creations(user_profile):
    """Count all approved creations by this user across all creative pages."""
    total = 0
    for page_info in CreativePage.get_all_models():
        model = page_info["model"]
        page = page_info["page"]
        filters = {
            "is_published": ApprovalChoices.APPROVED.value,
            "author_nick": user_profile.nick,
        }
        if getattr(model, "SHARED_BETWEEN_CREATIVE_PAGES", False):
            filters["creative_page_slug"] = page.slug
        total += model.objects.filter(**filters).count()
    return total


def count_user_posts(user_profile):
    """Count phorum posts and creation comments by this user."""
    phorum_count = Phorum.objects.filter(user=user_profile).count()
    comment_count = CreationComment.objects.filter(user=user_profile).count()
    return phorum_count + comment_count


def calculate_level(post_count, creation_count, reputation):
    """Determine user level based on activity metrics."""
    level = 0
    for candidate_level in sorted(LEVEL_THRESHOLDS.keys()):
        thresholds = LEVEL_THRESHOLDS[candidate_level]
        if (
            post_count >= thresholds["min_posts"]
            and creation_count >= thresholds["min_creations"]
            and reputation >= thresholds["min_reputation"]
        ):
            level = candidate_level
    return level


class Command(BaseCommand):
    help = "Recalculate user levels based on activity and reputation"

    def handle(self, *args, **options):
        active_users = UserProfile.objects.filter(status=ACTIVE_STATUS).exclude(
            level=STAFF_LEVEL
        )
        updated = 0

        for profile in active_users:
            post_count = count_user_posts(profile)
            creation_count = count_user_creations(profile)
            new_level = calculate_level(post_count, creation_count, profile.reputation)

            new_level_str = str(new_level)
            changed = False

            if profile.level != new_level_str:
                profile.level = new_level_str
                changed = True

            if profile.max_level is None or new_level > profile.max_level:
                profile.max_level = new_level
                changed = True

            if changed:
                profile.save(update_fields=["level", "max_level"])
                updated += 1

        self.stdout.write(
            self.style.SUCCESS(f"Recalculated levels for {updated} users")
        )
