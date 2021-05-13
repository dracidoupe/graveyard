from django.test import TestCase

from ..model_generator import get_alphabetic_user_profiles

from ddcz.tavern import create_tavern_table


class TestPublicTableAccess(TestCase):
    def setUp(self):
        super().setUp()

        self.profiles = get_alphabetic_user_profiles(number_of_users=3, saved=True)
        self.owner = self.profiles[0]
        self.banned = self.profiles[1]
        self.unaffected = self.profiles[2]

        self.public_table = create_tavern_table(
            owner=self.owner,
            public=True,
            name="Public",
            description="Public Tavern Table",
        )

        self.public_table.update_access_privileges(access_banned=[self.banned.pk])

    def test_random_user_can_access(self):
        self.assertTrue(
            self.public_table.is_user_access_allowed(user_profile=self.unaffected)
        )

    def test_owner_can_access(self):
        self.assertTrue(
            self.public_table.is_user_access_allowed(user_profile=self.owner)
        )

    def test_banned_is_declined(self):
        self.assertFalse(
            self.public_table.is_user_access_allowed(user_profile=self.banned)
        )
