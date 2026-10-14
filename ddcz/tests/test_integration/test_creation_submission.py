from django.contrib.auth.models import User
from django.core import mail
from django.test import TestCase
from django.urls import reverse

from ddcz.creations import ApprovalChoices
from ddcz.models import Author, CommonArticle, UserProfile
from ddcz.submissions import submit_common_article
from ddcz.tests.model_generator import create_profiled_user


class CreationSubmissionTestCase(TestCase):
    fixtures = ["pages"]

    def setUp(self):
        self.user = create_profiled_user("submitter", "secret")
        self.profile = UserProfile.objects.get(user=self.user)
        self.submit_url = reverse(
            "ddcz:creation-submit", kwargs={"creative_page_slug": "clanky"}
        )
        self.valid_data = {
            "name": "Nový <příběh>",
            "abstract": "Krátce",
            "section": "Povídky",
            "text": "<b>Ahoj</b>",
        }

    def test_anonymous_redirected(self):
        res = self.client.get(self.submit_url)
        self.assertEqual(302, res.status_code)

    def test_unknown_page_404(self):
        self.client.login(username="submitter", password="secret")
        res = self.client.get(
            reverse("ddcz:creation-submit", kwargs={"creative_page_slug": "bestiar"})
        )
        self.assertEqual(404, res.status_code)

    def test_form_displayed(self):
        self.client.login(username="submitter", password="secret")
        res = self.client.get(self.submit_url)
        self.assertEqual(200, res.status_code)

    def test_valid_submission(self):
        self.client.login(username="submitter", password="secret")
        res = self.client.post(self.submit_url, self.valid_data, follow=True)
        self.assertContains(res, "úspěšně odeslán")

        article = CommonArticle.objects.get()
        self.assertEqual(ApprovalChoices.WAITING.value, article.is_published)
        self.assertEqual("clanky", article.creative_page_slug)
        self.assertEqual("submitter", article.author_nick)
        self.assertEqual("Povídky", article.section)
        self.assertEqual("&lt;b&gt;Ahoj&lt;/b&gt;", article.text)
        self.assertEqual(0, int(article.rating))
        self.assertEqual(self.profile, article.author.user)
        self.assertEqual(Author.USER_TYPE, article.author.author_type)

    def test_author_reused(self):
        self.client.login(username="submitter", password="secret")
        self.client.post(self.submit_url, self.valid_data)
        self.client.post(self.submit_url, self.valid_data)
        self.assertEqual(1, Author.objects.count())
        self.assertEqual(2, CommonArticle.objects.count())

    def test_invalid_section_rejected(self):
        self.client.login(username="submitter", password="secret")
        self.valid_data["section"] = "Neexistuje"
        res = self.client.post(self.submit_url, self.valid_data)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, CommonArticle.objects.count())

    def test_pending_not_public(self):
        article = submit_common_article(
            self.profile, "clanky", "Tajne", "", "Povídky", "text"
        )
        res = self.client.get("/rubriky/clanky/")
        self.assertNotContains(res, "Tajne")
        res = self.client.get(f"/rubriky/clanky/{article.pk}-tajne/")
        self.assertEqual(404, res.status_code)


class SubmissionNotificationTestCase(TestCase):
    fixtures = ["pages"]

    def setUp(self):
        self.user = create_profiled_user("submitter", "secret")
        self.profile = UserProfile.objects.get(user=self.user)
        for nick, is_staff, is_active in [
            ("staff1", True, True),
            ("staff2", True, True),
            ("inactive", True, False),
            ("regular", False, True),
        ]:
            user = create_profiled_user(nick, "secret")
            user.is_staff = is_staff
            user.is_active = is_active
            user.save()

    def test_all_active_staff_notified(self):
        article = submit_common_article(
            self.profile, "clanky", "Nový &lt;příběh&gt;", "", "Povídky", "text"
        )

        self.assertEqual(
            {("staff1@example.com",), ("staff2@example.com",)},
            {tuple(m.to) for m in mail.outbox},
        )
        self.assertEqual(2, len(mail.outbox))
        body = mail.outbox[0].body
        self.assertIn(f"/sprava/prispevky/{article.pk}/", body)
        self.assertIn("Nový <příběh>", body)

    def test_no_staff_does_not_fail(self):
        User.objects.filter(is_staff=True).update(is_staff=False)
        submit_common_article(self.profile, "clanky", "Dílo", "", "Povídky", "text")
        self.assertEqual(0, len(mail.outbox))


class GraveyardSubmissionTestCase(TestCase):
    fixtures = ["pages"]

    def test_hrbitov_submission(self):
        create_profiled_user("submitter", "secret")
        self.client.login(username="submitter", password="secret")
        url = reverse("ddcz:creation-submit", kwargs={"creative_page_slug": "hrbitov"})
        self.assertEqual(200, self.client.get(url).status_code)

        self.client.post(
            url,
            {"name": "Hrdina", "abstract": "", "section": "Postava", "text": "Text"},
        )
        article = CommonArticle.objects.get()
        self.assertEqual("hrbitov", article.creative_page_slug)
        self.assertEqual("Postava", article.section)


class SectionColumnTestCase(TestCase):
    fixtures = ["pages"]

    def test_section_shown_in_list(self):
        CommonArticle.objects.create(
            name="Dílo",
            creative_page_slug="clanky",
            section="Povídky",
            is_published=ApprovalChoices.APPROVED.value,
            rating=0,
        )
        res = self.client.get("/rubriky/clanky/")
        self.assertContains(res, "<td>Povídky</td>", html=True)


class MySubmissionsTestCase(TestCase):
    fixtures = ["pages"]

    def setUp(self):
        self.user = create_profiled_user("submitter", "secret")
        self.profile = UserProfile.objects.get(user=self.user)
        self.other = create_profiled_user("other", "secret")
        self.other_profile = UserProfile.objects.get(user=self.other)
        self.mine = submit_common_article(
            self.profile, "clanky", "Moje", "", "Povídky", "text"
        )
        self.theirs = submit_common_article(
            self.other_profile, "clanky", "Cizi", "", "Povídky", "text"
        )
        self.client.login(username="submitter", password="secret")

    def test_lists_only_own(self):
        res = self.client.get(reverse("ddcz:my-submissions"))
        self.assertContains(res, "Moje")
        self.assertNotContains(res, "Cizi")

    def test_withdraw(self):
        res = self.client.post(
            reverse("ddcz:my-submission-withdraw", args=[self.mine.pk]), follow=True
        )
        self.assertContains(res, "stažen")
        self.mine.refresh_from_db()
        self.assertEqual(ApprovalChoices.WITHDRAWN.value, self.mine.is_published)

    def test_cannot_withdraw_foreign(self):
        self.client.post(reverse("ddcz:my-submission-withdraw", args=[self.theirs.pk]))
        self.theirs.refresh_from_db()
        self.assertEqual(ApprovalChoices.WAITING.value, self.theirs.is_published)

    def test_withdraw_requires_post(self):
        res = self.client.get(
            reverse("ddcz:my-submission-withdraw", args=[self.mine.pk])
        )
        self.assertEqual(405, res.status_code)
