from django.core import mail
from django.test import TestCase
from django.urls import reverse

from ddcz.creations import ApprovalChoices
from ddcz.models import (
    CommonArticle,
    CreationComment,
    CreationEmailSubscription,
    CreationVote,
    ScheduledEmail,
    ScheduledNotification,
    UserProfile,
)
from ddcz.notifications import notify_scheduled
from ddcz.submissions import submit_common_article
from ddcz.tests.model_generator import create_profiled_user


class TestDragonCreationReview(TestCase):
    fixtures = ["pages"]

    def setUp(self):
        self.staff = create_profiled_user("staff", "staffpw")
        self.staff.is_staff = True
        self.staff.save()
        self.staff_profile = UserProfile.objects.get(user=self.staff)

        self.author_user = create_profiled_user("author", "secret")
        self.author_profile = UserProfile.objects.get(user=self.author_user)
        self.article = submit_common_article(
            self.author_profile, "clanky", "Dílo", "Anotace", "Povídky", "Text"
        )
        mail.outbox.clear()
        self.review_url = reverse("dragon:creation-review", args=[self.article.pk])
        self.pending_url = reverse("dragon:creations-pending")
        self.approve_data = {
            "form_type": "approve",
            "name": "Dílo",
            "abstract": "Anotace",
            "section": "Povídky",
            "text": "Upravený text",
            "rating": "4",
            "comment": "Pěkné",
        }

    def login_staff(self):
        self.client.login(username="staff", password="staffpw")

    def test_requires_login(self):
        self.assertEqual(302, self.client.get(self.pending_url).status_code)
        self.assertEqual(302, self.client.get(self.review_url).status_code)

    def test_requires_staff(self):
        self.client.login(username="author", password="secret")
        self.assertEqual(403, self.client.get(self.pending_url).status_code)
        self.assertEqual(403, self.client.get(self.review_url).status_code)
        self.assertEqual(
            403, self.client.post(self.review_url, self.approve_data).status_code
        )

    def test_queue_lists_only_pending(self):
        done = submit_common_article(
            self.author_profile, "clanky", "Hotovo", "", "Povídky", "t"
        )
        done.is_published = ApprovalChoices.REJECTED.value
        done.save()
        self.login_staff()
        res = self.client.get(self.pending_url)
        self.assertContains(res, "Dílo")
        self.assertNotContains(res, "Hotovo")

    def test_review_page(self):
        self.login_staff()
        res = self.client.get(self.review_url)
        self.assertContains(res, "Dílo")

    def test_approve(self):
        self.login_staff()
        res = self.client.post(self.review_url, self.approve_data, follow=True)
        self.assertContains(res, "byl schválen")

        self.article.refresh_from_db()
        self.assertEqual(ApprovalChoices.APPROVED.value, self.article.is_published)
        self.assertEqual("Upravený text", self.article.text)
        self.assertEqual(4, int(self.article.rating))
        self.assertEqual(3, self.article.rater_no)
        self.assertEqual(12, self.article.rating_sum)

        vote = CreationVote.objects.get()
        self.assertEqual(self.staff_profile, vote.user_profile)
        self.assertEqual(4, vote.rating)

        comment = CreationComment.objects.get()
        self.assertEqual("Pěkné", comment.text)
        self.assertEqual("clanky", comment.foreign_table)

        self.assertEqual(1, len(mail.outbox))
        self.assertEqual(["author@example.com"], mail.outbox[0].to)

        self.assertEqual(200, self.client.get("/rubriky/clanky/").status_code)
        self.assertContains(self.client.get("/rubriky/clanky/"), "Dílo")

    def test_approve_abstaining(self):
        self.login_staff()
        self.approve_data["rating"] = "8"
        self.approve_data["comment"] = ""
        self.client.post(self.review_url, self.approve_data)

        self.article.refresh_from_db()
        self.assertEqual(0, int(self.article.rating))
        self.assertEqual(0, self.article.rater_no)
        self.assertEqual(0, self.article.rating_sum)
        self.assertEqual(0, CreationComment.objects.count())

    def test_approve_invalid_keeps_pending(self):
        self.login_staff()
        self.approve_data["section"] = "Neexistuje"
        res = self.client.post(self.review_url, self.approve_data)
        self.assertEqual(200, res.status_code)
        self.article.refresh_from_db()
        self.assertEqual(ApprovalChoices.WAITING.value, self.article.is_published)

    def test_approve_queues_subscriber_emails(self):
        CreationEmailSubscription.objects.create(
            user_profile_id=self.staff_profile.pk,
            creative_page_slug="clanky",
            user_email="staff@example.com",
            mime=0,
        )
        self.login_staff()
        self.client.post(self.review_url, self.approve_data)

        self.assertEqual(1, ScheduledNotification.objects.count())
        notify_scheduled()

        self.assertEqual(0, ScheduledNotification.objects.count())
        scheduled = ScheduledEmail.objects.get()
        self.assertEqual("staff@example.com", scheduled.recipient_email)
        self.assertIn("Dílo", scheduled.email_subject)
        self.assertIn(f"/rubriky/clanky/{self.article.pk}-dilo/", scheduled.email_text)

    def test_reject(self):
        self.login_staff()
        res = self.client.post(
            self.review_url,
            {"form_type": "reject", "reason": "Nevhodné"},
            follow=True,
        )
        self.assertContains(res, "byl zamítnut")

        self.article.refresh_from_db()
        self.assertEqual(ApprovalChoices.REJECTED.value, self.article.is_published)
        self.assertEqual(1, len(mail.outbox))
        self.assertIn("Nevhodné", mail.outbox[0].body)

    def test_reject_requires_reason(self):
        self.login_staff()
        self.client.post(self.review_url, {"form_type": "reject", "reason": ""})
        self.article.refresh_from_db()
        self.assertEqual(ApprovalChoices.WAITING.value, self.article.is_published)

    def test_decided_article_not_reviewable(self):
        self.login_staff()
        self.client.post(self.review_url, self.approve_data)
        self.assertEqual(404, self.client.get(self.review_url).status_code)
        self.assertEqual(
            404, self.client.post(self.review_url, self.approve_data).status_code
        )
        self.assertEqual(1, CommonArticle.objects.count())
