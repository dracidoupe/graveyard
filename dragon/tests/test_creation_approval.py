from django.test import TestCase
from django.urls import reverse

from ddcz.models import Author, CommonArticle, Monster
from ddcz.tests.model_generator import create_profiled_user


class CreationApprovalAccessTestCase(TestCase):
    fixtures = ["pages"]

    def setUp(self):
        self.staff = create_profiled_user("staff", "staffpw")
        self.staff.is_staff = True
        self.staff.save()

    def test_requires_login(self):
        response = self.client.get(reverse("dragon:creations"))
        self.assertEqual(302, response.status_code)

    def test_requires_staff(self):
        create_profiled_user("normal", "pw")
        self.client.login(username="normal", password="pw")
        response = self.client.get(reverse("dragon:creations"))
        self.assertEqual(403, response.status_code)

    def test_staff_can_access(self):
        self.client.login(username="staff", password="staffpw")
        response = self.client.get(reverse("dragon:creations"))
        self.assertEqual(200, response.status_code)


class CreationApprovalListTestCase(TestCase):
    fixtures = ["pages"]

    def setUp(self):
        self.staff = create_profiled_user("staff", "staffpw")
        self.staff.is_staff = True
        self.staff.save()
        self.client.login(username="staff", password="staffpw")

        self.author_user = create_profiled_user("author", "authorpw")
        self.author_profile = self.author_user.profile
        self.author = Author.objects.create(
            user=self.author_profile,
            author_type=Author.USER_TYPE,
            user_nick="author",
        )

    def test_shows_unapproved_creations(self):
        CommonArticle.objects.create(
            name="Cekajici clanek",
            text="Text",
            creative_page_slug="clanky",
            is_published="n",
            author=self.author,
            author_nick="author",
            rating=0,
            rater_no=0,
            rating_sum=0,
        )
        response = self.client.get(reverse("dragon:creations"))
        self.assertContains(response, "Cekajici clanek")

    def test_does_not_show_approved_creations(self):
        CommonArticle.objects.create(
            name="Schvaleny clanek",
            text="Text",
            creative_page_slug="clanky",
            is_published="a",
            author=self.author,
            author_nick="author",
            rating=0,
            rater_no=0,
            rating_sum=0,
        )
        response = self.client.get(reverse("dragon:creations"))
        self.assertNotContains(response, "Schvaleny clanek")

    def test_shows_multiple_creation_types(self):
        CommonArticle.objects.create(
            name="Cekajici clanek",
            text="Text",
            creative_page_slug="clanky",
            is_published="n",
            author=self.author,
            author_nick="author",
            rating=0,
            rater_no=0,
            rating_sum=0,
        )
        Monster.objects.create(
            name="Cekajici nestvura",
            hitpoint_class="A",
            attack="10",
            defense="4",
            fortitude="10",
            size="B",
            experience="100",
            description="Popis",
            group="Zvire",
            is_published="n",
            author=self.author,
            author_nick="author",
            rating=0,
            rater_no=0,
            rating_sum=0,
        )
        response = self.client.get(reverse("dragon:creations"))
        self.assertContains(response, "Cekajici clanek")
        self.assertContains(response, "Cekajici nestvura")


class CreationApproveTestCase(TestCase):
    fixtures = ["pages"]

    def setUp(self):
        self.staff = create_profiled_user("staff", "staffpw")
        self.staff.is_staff = True
        self.staff.save()
        self.client.login(username="staff", password="staffpw")

        self.author_user = create_profiled_user("author", "authorpw")
        self.author_profile = self.author_user.profile
        self.author_profile.email = "author@example.com"
        self.author_profile.save()
        self.author = Author.objects.create(
            user=self.author_profile,
            author_type=Author.USER_TYPE,
            user_nick="author",
        )

        self.article = CommonArticle.objects.create(
            name="Ke schvaleni",
            text="Text clanku",
            creative_page_slug="clanky",
            is_published="n",
            author=self.author,
            author_nick="author",
            author_mail="author@example.com",
            rating=0,
            rater_no=0,
            rating_sum=0,
        )

    def test_approve_creation(self):
        response = self.client.post(
            reverse("dragon:creation-approve"),
            {
                "creation_id": str(self.article.pk),
                "creative_page_slug": "clanky",
                "action": "approve",
            },
            follow=True,
        )
        self.assertEqual(200, response.status_code)
        self.article.refresh_from_db()
        self.assertEqual("a", self.article.is_published)

    def test_reject_creation(self):
        response = self.client.post(
            reverse("dragon:creation-approve"),
            {
                "creation_id": str(self.article.pk),
                "creative_page_slug": "clanky",
                "action": "reject",
            },
            follow=True,
        )
        self.assertEqual(200, response.status_code)
        self.assertFalse(CommonArticle.objects.filter(pk=self.article.pk).exists())

    def test_approve_requires_staff(self):
        self.client.logout()
        create_profiled_user("normal", "pw")
        self.client.login(username="normal", password="pw")
        response = self.client.post(
            reverse("dragon:creation-approve"),
            {
                "creation_id": str(self.article.pk),
                "creative_page_slug": "clanky",
                "action": "approve",
            },
        )
        self.assertEqual(403, response.status_code)
        self.article.refresh_from_db()
        self.assertEqual("n", self.article.is_published)

    def test_success_message_on_approve(self):
        response = self.client.post(
            reverse("dragon:creation-approve"),
            {
                "creation_id": str(self.article.pk),
                "creative_page_slug": "clanky",
                "action": "approve",
            },
            follow=True,
        )
        self.assertContains(response, "schváleno")

    def test_success_message_on_reject(self):
        response = self.client.post(
            reverse("dragon:creation-approve"),
            {
                "creation_id": str(self.article.pk),
                "creative_page_slug": "clanky",
                "action": "reject",
            },
            follow=True,
        )
        self.assertContains(response, "zamítnuto")
