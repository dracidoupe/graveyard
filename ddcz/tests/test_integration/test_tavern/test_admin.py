from django.urls import reverse
from django.test import Client, TestCase

from ...model_generator import get_alphabetic_user_profiles

from ddcz.tavern import create_tavern_table, TavernAccessRights


class TestTableAdminAccess(TestCase):
    def setUp(self):
        super().setUp()

        self.profiles = get_alphabetic_user_profiles(
            number_of_users=3, saved=True, with_corresponding_user=True
        )
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

        self.admin_url = reverse("ddcz:tavern-table-admin", args=[self.public_table.pk])
        self.client = Client()

    def tearDown(self):
        super().tearDown()
        self.client.logout()

    def test_nonadmin_cannot_access(self):
        self.client.login(
            username=self.banned.user.username, password=self.banned.user.email
        )
        self.assertEqual(302, self.client.get(self.admin_url).status_code)

        self.client.login(
            username=self.unaffected.user.username, password=self.unaffected.user.email
        )
        self.assertEqual(403, self.client.get(self.admin_url).status_code)

    def test_only_admin_can_access_admin(self):
        self.client.login(
            username=self.owner.user.username, password=self.owner.user.email
        )
        self.assertEqual(200, self.client.get(self.admin_url).status_code)


class TestTableAdmin(TestCase):
    def setUp(self):
        super().setUp()

        self.profiles = get_alphabetic_user_profiles(
            number_of_users=2, saved=True, with_corresponding_user=True
        )
        self.owner = self.profiles[0]
        self.helper = self.profiles[1]

        self.public_table = create_tavern_table(
            owner=self.owner,
            public=True,
            name="Public",
            description="Public Tavern Table",
        )

        self.admin_url = reverse("ddcz:tavern-table-admin", args=[self.public_table.pk])
        self.client = Client()
        self.client.login(
            username=self.owner.user.username, password=self.owner.user.email
        )

    def tearDown(self):
        super().tearDown()
        self.client.logout()

    def test_update_privileges_can_be_done_with_nickname(self):
        response = self.client.post(
            self.admin_url,
            {
                "name": self.public_table.name,
                "description": self.public_table.description,
                "allow_rep": self.public_table.allow_rep,
                "assistant_admins": self.helper.nick,
                "write_allowed": "",
                "access_allowed": "",
                "access_banned": "",
            },
        )

        self.assertEqual(302, response.status_code)

        self.public_table.refresh_from_db()
        self.assertEqual(
            {self.helper.nick},
            self.public_table.get_current_privileges_map()[
                TavernAccessRights.ASSISTANT_ADMIN
            ],
        )

        # Check page renders well after (we had bugs with storing bad data well and then not rendering)
        self.assertEqual(200, self.client.get(self.admin_url).status_code)
