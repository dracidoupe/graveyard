from django.test import TestCase

from ...model_generator import get_alphabetic_user_profiles

from ddcz.tavern import (
    LIST_ALL,
    LIST_FAVORITE,
    create_tavern_table,
    get_tavern_table_list,
    bookmark_table,
)


class TavernListingTestCase(TestCase):
    def assertTableInListing(self, table, listing):
        self.assertIn(table.pk, [table.pk for table in listing])

    def assertTableNotInListing(self, table, listing):
        self.assertNotIn(table.pk, [table.pk for table in listing])


class TestPublicTableListings(TavernListingTestCase):
    def setUp(self):
        super().setUp()

        (
            self.owner,
            self.banned,
            self.unaffected,
        ) = self.profiles = get_alphabetic_user_profiles(number_of_users=3, saved=True)

        self.public_table = create_tavern_table(
            owner=self.owner,
            public=True,
            name="Public",
            description="Public Tavern Table",
        )

        self.public_table.update_access_privileges(access_banned=[self.banned.pk])

        self.bookmarked_public_table = create_tavern_table(
            owner=self.owner,
            public=True,
            name="Public Bookmarked",
            description="Bookmarked Public Tavern Table",
        )

        self.bookmarked_public_table.update_access_privileges(
            access_banned=[self.banned.pk]
        )

        for user in self.profiles:
            bookmark_table(user, self.bookmarked_public_table)

    def test_shown_to_random_user(self):
        self.assertTableInListing(
            self.public_table, get_tavern_table_list(self.unaffected, LIST_ALL)
        )

    def test_shown_to_owner(self):
        self.assertTableInListing(
            self.public_table, get_tavern_table_list(self.owner, LIST_ALL)
        )

    def test_shown_to_banned(self):
        self.assertTableInListing(
            self.public_table, get_tavern_table_list(self.banned, LIST_ALL)
        )

    def test_not_linked_to_banned(self):
        self.assertFalse(self.public_table.show_listing_link(self.banned))

    def test_both_tables_shown(self):
        self.assertEquals(2, len(get_tavern_table_list(self.unaffected, LIST_ALL)))

    def test_bookmark_shown_to_random_user(self):
        self.assertTableInListing(
            self.bookmarked_public_table,
            get_tavern_table_list(self.unaffected, LIST_FAVORITE),
        )

    def test_bookmark_shown_to_owner(self):
        self.assertTableInListing(
            self.bookmarked_public_table,
            get_tavern_table_list(self.owner, LIST_FAVORITE),
        )

    def test_bookmark_shown_to_banned(self):
        self.assertTableInListing(
            self.bookmarked_public_table,
            get_tavern_table_list(self.banned, LIST_FAVORITE),
        )

    def test_bookmark_not_linked_to_banned(self):
        self.assertFalse(self.bookmarked_public_table.show_listing_link(self.banned))

    def test_only_favorite_shown(self):
        self.assertEquals(1, len(get_tavern_table_list(self.unaffected, LIST_FAVORITE)))


class TestOwnerAssistOverrule(TavernListingTestCase):
    def setUp(self):
        super().setUp()

        self.owner, self.assist, self.banned = get_alphabetic_user_profiles(
            number_of_users=3, saved=True
        )

        self.public_table = create_tavern_table(
            owner=self.owner,
            public=True,
            name="Public",
            description="Public Tavern Table",
        )

        # Owner bans themselves
        self.public_table.update_access_privileges(
            access_banned=[self.owner.pk, self.assist.pk, self.banned.pk],
            assistant_admins=[self.assist.pk],
        )

    def test_shown_admin(self):
        self.assertTableInListing(
            self.public_table, get_tavern_table_list(self.owner, LIST_ALL)
        )

    def test_shown_assist(self):
        self.assertTableInListing(
            self.public_table, get_tavern_table_list(self.owner, LIST_ALL)
        )

    def test_shown_banned(self):
        self.assertTableInListing(
            self.public_table, get_tavern_table_list(self.banned, LIST_ALL)
        )


class TestPrivateTableListings(TavernListingTestCase):
    def setUp(self):
        super().setUp()

        (
            self.owner,
            self.banned,
            self.unaffected,
            self.allowed,
            self.assist,
        ) = self.profiles = get_alphabetic_user_profiles(number_of_users=5, saved=True)

        self.private_table = create_tavern_table(
            owner=self.owner,
            public=False,
            name="Private",
            description="Private Tavern Table",
        )

        self.private_table.update_access_privileges(
            access_banned=[self.banned.pk],
            access_allowed=[self.allowed.pk],
            assistant_admins=[self.assist.pk],
        )

        self.bookmarked_private_table = create_tavern_table(
            owner=self.owner,
            public=False,
            name="Private Bookmarked",
            description="Bookmarked Private Tavern Table",
        )

        self.bookmarked_private_table.update_access_privileges(
            access_banned=[self.banned.pk],
            access_allowed=[self.allowed.pk],
            assistant_admins=[self.assist.pk],
        )

        for user in self.profiles:
            bookmark_table(user, self.bookmarked_private_table)

    def test_shown_to_random_user(self):
        self.assertTableInListing(
            self.private_table, get_tavern_table_list(self.unaffected, LIST_ALL)
        )

    def test_shown_to_owner(self):
        self.assertTableInListing(
            self.private_table, get_tavern_table_list(self.owner, LIST_ALL)
        )

    def test_shown_to_assist(self):
        self.assertTableInListing(
            self.private_table, get_tavern_table_list(self.assist, LIST_ALL)
        )

    def test_show_to_banned(self):
        self.assertTableInListing(
            self.private_table, get_tavern_table_list(self.banned, LIST_ALL)
        )

    def test_private_tables_shown(self):
        self.assertEquals(2, len(get_tavern_table_list(self.unaffected, LIST_ALL)))

    def test_both_tables_shown_to_allowed(self):
        self.assertEquals(2, len(get_tavern_table_list(self.allowed, LIST_ALL)))

    def test_bookmark_shown_to_random_user(self):
        self.assertTableInListing(
            self.bookmarked_private_table,
            get_tavern_table_list(self.unaffected, LIST_FAVORITE),
        )

    def test_bookmark_shown_to_owner(self):
        self.assertTableInListing(
            self.bookmarked_private_table,
            get_tavern_table_list(self.owner, LIST_FAVORITE),
        )

    def test_bookmark_shown_to_banned(self):
        self.assertTableInListing(
            self.bookmarked_private_table,
            get_tavern_table_list(self.banned, LIST_FAVORITE),
        )
