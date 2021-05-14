from django.test import TestCase

from ...model_generator import get_alphabetic_user_profiles

from ddcz.tavern import LIST_ALL, create_tavern_table, get_tavern_table_list


class TavernListingTestCase(TestCase):
    def assertTableInListing(self, table, listing):
        self.assertIn(table.pk, [table.pk for table in listing])

    def assertTableNotInListing(self, table, listing):
        self.assertNotIn(table.pk, [table.pk for table in listing])


class TestPublicTableFullListing(TavernListingTestCase):
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

    def test_shown_to_random_user(self):
        self.assertTableInListing(
            self.public_table, get_tavern_table_list(self.unaffected, LIST_ALL)
        )

    def test_shown_to_owner(self):
        self.assertTableInListing(
            self.public_table, get_tavern_table_list(self.owner, LIST_ALL)
        )

    def test_hidden_from_banned(self):
        self.assertTableInListing(
            self.public_table, get_tavern_table_list(self.banned, LIST_ALL)
        )
