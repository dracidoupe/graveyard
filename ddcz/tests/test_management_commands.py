from django.test import TestCase
from django.core.management import call_command

from ddcz.models import (
    Author,
    CommonArticle,
    Phorum,
)
from ddcz.tests.model_generator import create_profiled_user


class AllocateReputationTestCase(TestCase):
    def setUp(self):
        self.user = create_profiled_user("testuser", "pw")
        self.profile = self.user.profile
        self.profile.reputation_available = 0
        self.profile.level = "0"
        self.profile.status = "4"
        self.profile.save()

    def test_allocates_base_reputation(self):
        call_command("allocatereputation")
        self.profile.refresh_from_db()
        self.assertGreater(self.profile.reputation_available, 0)

    def test_higher_level_gets_more(self):
        user2 = create_profiled_user("highlevel", "pw")
        profile2 = user2.profile
        profile2.level = "3"
        profile2.status = "4"
        profile2.reputation_available = 0
        profile2.save()

        call_command("allocatereputation")
        self.profile.refresh_from_db()
        profile2.refresh_from_db()
        self.assertGreater(
            profile2.reputation_available, self.profile.reputation_available
        )

    def test_skips_banned_users(self):
        self.profile.status = "1"
        self.profile.save()
        call_command("allocatereputation")
        self.profile.refresh_from_db()
        self.assertEqual(0, self.profile.reputation_available)

    def test_adds_to_existing_available(self):
        self.profile.reputation_available = 5
        self.profile.save()
        call_command("allocatereputation")
        self.profile.refresh_from_db()
        self.assertGreater(self.profile.reputation_available, 5)

    def test_caps_at_maximum(self):
        self.profile.reputation_available = 250
        self.profile.save()
        call_command("allocatereputation")
        self.profile.refresh_from_db()
        # Should not exceed 255 (tinyint unsigned max from legacy DB)
        self.assertLessEqual(self.profile.reputation_available, 255)


class RecalculateLevelsTestCase(TestCase):
    fixtures = ["pages"]

    def setUp(self):
        self.user = create_profiled_user("testuser", "pw")
        self.profile = self.user.profile
        self.profile.level = "0"
        self.profile.reputation = 0
        self.profile.status = "4"
        self.profile.save()

    def _create_phorum_posts(self, count):
        for i in range(count):
            Phorum.objects.create(
                nickname=self.profile.nick,
                text=f"Post {i}",
                reputation=0,
                registered_or_ip="1",
                user=self.profile,
            )

    def _create_creations(self, count):
        author = Author.objects.create(
            user=self.profile,
            author_type=Author.USER_TYPE,
            user_nick=self.profile.nick,
        )
        for i in range(count):
            CommonArticle.objects.create(
                name=f"Article {i}",
                text="Text",
                creative_page_slug="clanky",
                is_published="a",
                author=author,
                author_nick=self.profile.nick,
                rating=3,
                rater_no=5,
                rating_sum=15,
            )

    def test_stays_level_zero_with_no_activity(self):
        call_command("recalculatelevels")
        self.profile.refresh_from_db()
        self.assertEqual("0", self.profile.level)

    def test_level_up_from_discussion_activity(self):
        """User with significant phorum activity should reach level 1"""
        self._create_phorum_posts(30)
        self.profile.reputation = 20
        self.profile.save()

        call_command("recalculatelevels")
        self.profile.refresh_from_db()
        self.assertGreaterEqual(int(self.profile.level), 1)

    def test_level_up_from_creation_activity(self):
        """User with creations should reach level 3"""
        self._create_creations(10)
        self.profile.reputation = 50
        self.profile.save()

        call_command("recalculatelevels")
        self.profile.refresh_from_db()
        self.assertGreaterEqual(int(self.profile.level), 3)

    def test_skips_banned_users(self):
        self.profile.status = "1"
        self.profile.save()
        call_command("recalculatelevels")
        self.profile.refresh_from_db()
        self.assertEqual("0", self.profile.level)

    def test_does_not_downgrade_staff(self):
        self.profile.level = "8"
        self.profile.save()
        call_command("recalculatelevels")
        self.profile.refresh_from_db()
        self.assertEqual("8", self.profile.level)

    def test_tracks_max_level(self):
        """max_level should track the highest level achieved"""
        self._create_phorum_posts(30)
        self.profile.reputation = 20
        self.profile.save()

        call_command("recalculatelevels")
        self.profile.refresh_from_db()
        new_level = int(self.profile.level)
        self.assertEqual(new_level, self.profile.max_level)

    def test_does_not_lower_max_level(self):
        """max_level should never decrease"""
        self.profile.max_level = 4
        self.profile.level = "0"
        self.profile.save()

        call_command("recalculatelevels")
        self.profile.refresh_from_db()
        self.assertGreaterEqual(self.profile.max_level, 4)
