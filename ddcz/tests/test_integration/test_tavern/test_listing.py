from django.contrib.auth.models import User
from django.urls import reverse
from django.test import Client, TestCase

from ...model_generator import get_alphabetic_user_profiles, create_profiled_user

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


class TestListingDoesNotHaveRunawayQueries(TavernListingTestCase):
    # This can be incremented, but the point is not to let pointless runaway queries happen
    # as it did before, see <https://github.com/dracidoupe/graveyard/issues/302>
    EXPECTED_LIST_QUERIES = 4

    def setUp(self):
        super().setUp()

        self.owner, self.banned = get_alphabetic_user_profiles(
            number_of_users=2, saved=True
        )

        self.owner_user = create_profiled_user(
            username="owner", password="bobr-evropsky"
        )
        self.banned_user = create_profiled_user(
            username="banned", password="bobrice-evropska"
        )

        for i in range(0, 15):
            table = create_tavern_table(
                owner=self.owner,
                public=True,
                name=f"Public {i}",
                description="Public Table",
            )

            table.update_access_privileges(access_banned=[self.banned.pk])

        self.client = Client()

    def test_owner_not_runaway(self):
        self.client.force_login(user=self.owner_user)
        with self.assertNumQueries(self.EXPECTED_LIST_QUERIES):
            self.client.get(f"{reverse('ddcz:tavern-list')}?vypis=vsechny")

    def test_banned_not_runaway(self):
        self.client.force_login(user=self.banned_user)
        with self.assertNumQueries(self.EXPECTED_LIST_QUERIES):
            self.client.get(f"{reverse('ddcz:tavern-list')}?vypis=vsechny")


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
