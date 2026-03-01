from django.test import Client, TestCase
from django.urls import reverse

from ddcz.models import CreationEmailSubscription

from ..model_generator import create_profiled_user


class UserSettingsAccessTestCase(TestCase):
    fixtures = ["pages"]

    def setUp(self):
        super().setUp()
        self.client = Client()
        self.password = "testpassword123"
        self.user = create_profiled_user("testuser", self.password)

    def test_anonymous_user_redirected(self):
        response = self.client.get(reverse("ddcz:user-settings"))
        self.assertEqual(302, response.status_code)
        self.assertIn("next=/nastaveni/", response.url)

    def test_authenticated_user_can_access_settings(self):
        self.client.login(username="testuser", password=self.password)
        response = self.client.get(reverse("ddcz:user-settings"))
        self.assertEqual(200, response.status_code)
        self.assertContains(response, "Osobní údaje")


class UserSettingsFormTestCase(TestCase):
    fixtures = ["pages"]

    def setUp(self):
        super().setUp()
        self.client = Client()
        self.password = "testpassword123"
        self.user = create_profiled_user("testuser", self.password)
        self.profile = self.user.profile

        self.profile.name_given = "Jan"
        self.profile.name_family = "Novák"
        self.profile.email = "jan@example.com"
        self.profile.gender = "Muž"
        self.profile.shire = "Praha"
        self.profile.description_raw = "Příliš žluťoučký kůň úpěl ďábelské ódy."
        self.profile.pii_display_permissions = "1,1,0,0,1,0,1,0"
        self.profile.save()

        self.client.login(username="testuser", password=self.password)

    def test_form_displays_current_values(self):
        response = self.client.get(reverse("ddcz:user-settings"))

        self.assertContains(response, 'value="Jan"')
        self.assertContains(response, 'value="Novák"')
        self.assertContains(response, "jan@example.com")
        self.assertContains(response, "Příliš žluťoučký kůň úpěl ďábelské ódy.")

    def test_form_saves_changes(self):
        response = self.client.post(
            reverse("ddcz:user-settings"),
            {
                "name_given": "Petr",
                "name_family": "Svoboda",
                "gender": "M",
                "shire": "Brněnský kraj",
                "description": "Nový popis",
                "show_name_given": True,
                "show_name_family": False,
                "show_email": True,
                "show_gender": False,
                "show_age": True,
                "show_shire": False,
            },
        )

        self.assertEqual(200, response.status_code)
        self.assertContains(response, "Uloženo!")

        self.profile.refresh_from_db()
        self.assertEqual("Petr", self.profile.name_given)
        self.assertEqual("Svoboda", self.profile.name_family)
        self.assertEqual("jan@example.com", self.profile.email)
        self.assertEqual("Muž", self.profile.gender)
        self.assertEqual("Brněnský kraj", self.profile.shire)
        self.assertEqual("Nový popis", self.profile.description_raw)

        permissions = self.profile.public_listing_permissions
        self.assertTrue(permissions["name_given"])
        self.assertFalse(permissions["name_family"])
        self.assertTrue(permissions["email"])
        self.assertFalse(permissions["gender"])
        self.assertTrue(permissions["age"])
        self.assertFalse(permissions["shire"])

    def test_form_validates_required_fields(self):
        response = self.client.post(
            reverse("ddcz:user-settings"),
            {
                "name_given": "",
                "name_family": "",
                "gender": "M",
                "shire": "",
                "description": "",
            },
        )

        self.assertEqual(200, response.status_code)
        self.assertContains(response, "Jméno")
        self.assertContains(response, "Příjmení")

        self.profile.refresh_from_db()
        self.assertEqual("Jan", self.profile.name_given)


class MailingListSettingsAccessTestCase(TestCase):
    fixtures = ["pages"]

    def setUp(self):
        super().setUp()
        self.client = Client()
        self.password = "testpassword123"
        self.user = create_profiled_user("testuser", self.password)
        self.profile = self.user.profile
        self.profile.email = "test@example.com"
        self.profile.save()

    def test_anonymous_user_redirected(self):
        response = self.client.get(reverse("ddcz:user-settings-mail"))
        self.assertEqual(302, response.status_code)

    def test_authenticated_user_can_access(self):
        self.client.login(username="testuser", password=self.password)
        response = self.client.get(reverse("ddcz:user-settings-mail"))
        self.assertEqual(200, response.status_code)
        self.assertContains(response, "Maillist")

    def test_settings_nav_links_present(self):
        """Both settings pages have navigation links to each other."""
        self.client.login(username="testuser", password=self.password)

        response = self.client.get(reverse("ddcz:user-settings"))
        self.assertContains(response, reverse("ddcz:user-settings-mail"))

        response = self.client.get(reverse("ddcz:user-settings-mail"))
        self.assertContains(response, reverse("ddcz:user-settings"))


class MailingListSubscriptionTestCase(TestCase):
    fixtures = ["pages"]

    def setUp(self):
        super().setUp()
        self.client = Client()
        self.password = "testpassword123"
        self.user = create_profiled_user("testuser", self.password)
        self.profile = self.user.profile
        self.profile.email = "test@example.com"
        self.profile.save()
        self.client.login(username="testuser", password=self.password)

    def test_no_subscriptions_by_default(self):
        response = self.client.get(reverse("ddcz:user-settings-mail"))
        self.assertEqual(200, response.status_code)
        self.assertFalse(
            CreationEmailSubscription.objects.filter(
                user_profile_id=self.profile.id
            ).exists()
        )

    def test_subscribe_to_news(self):
        response = self.client.post(
            reverse("ddcz:user-settings-mail"),
            {"subscribe_aktuality": "on"},
            follow=True,
        )
        self.assertEqual(200, response.status_code)
        self.assertContains(response, "Uloženo!")
        self.assertTrue(
            CreationEmailSubscription.objects.filter(
                user_profile_id=self.profile.id,
                creative_page_slug="aktuality",
            ).exists()
        )

    def test_unsubscribe_from_news(self):
        CreationEmailSubscription.objects.create(
            user_profile_id=self.profile.id,
            creative_page_slug="aktuality",
            user_email=self.profile.email,
            mime="p",
        )
        response = self.client.post(
            reverse("ddcz:user-settings-mail"),
            {},
            follow=True,
        )
        self.assertEqual(200, response.status_code)
        self.assertContains(response, "Uloženo!")
        self.assertFalse(
            CreationEmailSubscription.objects.filter(
                user_profile_id=self.profile.id,
                creative_page_slug="aktuality",
            ).exists()
        )

    def test_existing_subscription_shown_as_checked(self):
        CreationEmailSubscription.objects.create(
            user_profile_id=self.profile.id,
            creative_page_slug="aktuality",
            user_email=self.profile.email,
            mime="p",
        )
        response = self.client.get(reverse("ddcz:user-settings-mail"))
        self.assertContains(response, "checked")
