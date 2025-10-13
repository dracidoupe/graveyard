from ddcz.models import UserProfile
from ddcz.tests.model_generator import create_profiled_user

from .cases import DragonSeleniumTestCase


class TestUsersManagement(DragonSeleniumTestCase):
    def setUp(self):
        self.staff = create_profiled_user("staffuser", "staffpass")
        self.staff.is_staff = True
        self.staff.save()

        self.normal_user = create_profiled_user("normaluser", "normalpass")
        self.normal_profile = UserProfile.objects.get(user=self.normal_user)
        self.normal_profile.status = "4"
        self.normal_profile.save()

    def test_staff_can_access_users_page(self):
        self.dragon_login_as_staff(
            UserProfile.objects.get(user=self.staff), "staffpass"
        )

        self.el(self.dragon_page.NAV_USERS).click()

        self.assertIn("Správa uživatelů", self.selenium.page_source)
        self.assertIsNotNone(self.el(self.dragon_page.USER_SEARCH_INPUT))

    def test_staff_can_search_for_user(self):
        self.dragon_login_as_staff(
            UserProfile.objects.get(user=self.staff), "staffpass"
        )

        self.selenium.get(f"{self.live_server_url}/sprava/uzivatele/")

        search_input = self.el(self.dragon_page.USER_SEARCH_INPUT)
        search_input.send_keys("normaluser")
        self.el(self.dragon_page.USER_SEARCH_SUBMIT).click()

        self.assertIn("Nalezený uživatel", self.selenium.page_source)
        self.assertIn("normaluser", self.selenium.page_source)
        self.assertIsNotNone(self.el(self.dragon_page.USER_INFO_TABLE))

    def test_staff_can_ban_user(self):
        self.dragon_login_as_staff(
            UserProfile.objects.get(user=self.staff), "staffpass"
        )

        self.selenium.get(f"{self.live_server_url}/sprava/uzivatele/?nick=normaluser")

        self.assertIsNotNone(self.el(self.dragon_page.BAN_BUTTON))

        # Handle the confirmation dialog
        self.selenium.execute_script("window.confirm = function(){return true;}")
        self.el(self.dragon_page.BAN_BUTTON).click()

        # Check success message
        success_msg = self.el(self.dragon_page.MESSAGE_SUCCESS)
        self.assertIn("zablokován", success_msg.text)

        # Verify user is banned in database
        self.normal_profile.refresh_from_db()
        self.assertEqual(self.normal_profile.status, "1")

    def test_staff_can_unban_user(self):
        # First ban the user
        self.normal_profile.status = "1"
        self.normal_profile.save()

        self.dragon_login_as_staff(
            UserProfile.objects.get(user=self.staff), "staffpass"
        )

        self.selenium.get(f"{self.live_server_url}/sprava/uzivatele/?nick=normaluser")

        self.assertIsNotNone(self.el(self.dragon_page.UNBAN_BUTTON))
        self.el(self.dragon_page.UNBAN_BUTTON).click()

        # Check success message
        success_msg = self.el(self.dragon_page.MESSAGE_SUCCESS)
        self.assertIn("odblokován", success_msg.text)

        # Verify user is unbanned in database
        self.normal_profile.refresh_from_db()
        self.assertEqual(self.normal_profile.status, "4")

    def test_search_for_nonexistent_user_shows_error(self):
        self.dragon_login_as_staff(
            UserProfile.objects.get(user=self.staff), "staffpass"
        )

        self.selenium.get(f"{self.live_server_url}/sprava/uzivatele/")

        search_input = self.el(self.dragon_page.USER_SEARCH_INPUT)
        search_input.send_keys("nonexistentuser")
        self.el(self.dragon_page.USER_SEARCH_SUBMIT).click()

        error_msg = self.el(self.dragon_page.MESSAGE_ERROR)
        self.assertIn("nenalezen", error_msg.text)
