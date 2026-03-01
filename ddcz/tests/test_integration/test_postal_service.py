from django.test import Client, TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from ddcz.models import UserProfile, Letter


class PostalServiceTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.client = Client()

        self.sender_nick = "odesilatel"
        self.receiver_nick = "prijemce"

        self.sender_user = User.objects.create_user(
            username=self.sender_nick, password="heslo-odesilatel"
        )
        self.sender_profile = UserProfile.objects.create(
            nick=self.sender_nick,
            email="sender@example.com",
            user=self.sender_user,
        )

        self.receiver_user = User.objects.create_user(
            username=self.receiver_nick, password="heslo-prijemce"
        )
        self.receiver_profile = UserProfile.objects.create(
            nick=self.receiver_nick,
            email="receiver@example.com",
            user=self.receiver_user,
        )

        self.letter = Letter.objects.create(
            sender=self.sender_nick,
            receiver=self.receiver_nick,
            text="Ahoj, jak se mas?",
            date="2024-01-15 12:00:00",
            visibility="3",
        )

    def test_postal_service_requires_login(self):
        res = self.client.get(reverse("ddcz:postal-service"))
        self.assertEqual(302, res.status_code)

    def test_postal_service_page_loads(self):
        self.client.force_login(user=self.sender_user)
        res = self.client.get(reverse("ddcz:postal-service"))
        self.assertEqual(200, res.status_code)
        self.assertContains(res, "Dračí pošta")

    def test_letter_visible_to_sender(self):
        self.client.force_login(user=self.sender_user)
        res = self.client.get(reverse("ddcz:postal-service"))
        self.assertContains(res, "Ahoj, jak se mas?")

    def test_letter_visible_to_receiver(self):
        self.client.force_login(user=self.receiver_user)
        res = self.client.get(reverse("ddcz:postal-service"))
        self.assertContains(res, "Ahoj, jak se mas?")

    def test_send_letter(self):
        self.client.force_login(user=self.sender_user)
        res = self.client.post(
            reverse("ddcz:postal-service"),
            {"fid": "2", "whom": self.receiver_nick, "text": "Novy dopis"},
            follow=True,
        )
        self.assertEqual(200, res.status_code)
        self.assertTrue(
            Letter.objects.filter(sender=self.sender_nick, text="Novy dopis").exists()
        )

    def test_send_letter_to_nonexistent_user(self):
        self.client.force_login(user=self.sender_user)
        res = self.client.post(
            reverse("ddcz:postal-service"),
            {"fid": "2", "whom": "neexistujici", "text": "Dopis"},
            follow=True,
        )
        self.assertEqual(200, res.status_code)
        self.assertContains(res, "nepodařilo nalézt")

    def test_delete_letter_by_sender(self):
        self.client.force_login(user=self.sender_user)
        res = self.client.post(
            reverse("ddcz:postal-service"),
            {"fid": "1", "id": str(self.letter.pk)},
            follow=True,
        )
        self.assertEqual(200, res.status_code)
        self.letter.refresh_from_db()
        self.assertEqual("2", self.letter.visibility)

    def test_delete_letter_by_receiver(self):
        self.client.force_login(user=self.receiver_user)
        res = self.client.post(
            reverse("ddcz:postal-service"),
            {"fid": "1", "id": str(self.letter.pk)},
            follow=True,
        )
        self.assertEqual(200, res.status_code)
        self.letter.refresh_from_db()
        self.assertEqual("1", self.letter.visibility)

    def test_cannot_delete_others_letter(self):
        other_user = User.objects.create_user(
            username="cizinec", password="heslo-cizinec"
        )
        UserProfile.objects.create(
            nick="cizinec",
            email="cizinec@example.com",
            user=other_user,
        )
        self.client.force_login(user=other_user)
        res = self.client.post(
            reverse("ddcz:postal-service"),
            {"fid": "1", "id": str(self.letter.pk)},
        )
        self.assertEqual(400, res.status_code)
        self.letter.refresh_from_db()
        self.assertEqual("3", self.letter.visibility)


class PostalServiceReplyTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.client = Client()

        self.sender_nick = "pisatel"
        self.receiver_nick = "cteni"

        self.sender_user = User.objects.create_user(
            username=self.sender_nick, password="heslo-pisatel"
        )
        self.sender_profile = UserProfile.objects.create(
            nick=self.sender_nick,
            email="pisatel@example.com",
            user=self.sender_user,
        )

        self.receiver_user = User.objects.create_user(
            username=self.receiver_nick, password="heslo-cteni"
        )
        self.receiver_profile = UserProfile.objects.create(
            nick=self.receiver_nick,
            email="cteni@example.com",
            user=self.receiver_user,
        )

        self.letter = Letter.objects.create(
            sender=self.sender_nick,
            receiver=self.receiver_nick,
            text="Puvodni zprava",
            date="2024-01-15 12:00:00",
            visibility="3",
        )

    def test_reply_creates_new_letter(self):
        """Reply to a letter creates a new letter with sender/receiver swapped."""
        self.client.force_login(user=self.receiver_user)
        res = self.client.post(
            reverse("ddcz:postal-service"),
            {
                "fid": "4",
                "id": str(self.letter.pk),
                "text": "Odpoved na zpravu",
            },
            follow=True,
        )
        self.assertEqual(200, res.status_code)
        reply = Letter.objects.filter(text="Odpoved na zpravu").first()
        self.assertIsNotNone(reply)
        self.assertEqual(self.receiver_nick, reply.sender)
        self.assertEqual(self.sender_nick, reply.receiver)
        self.assertEqual("3", reply.visibility)

    def test_reply_requires_letter_id(self):
        """Reply without letter ID returns bad request."""
        self.client.force_login(user=self.receiver_user)
        res = self.client.post(
            reverse("ddcz:postal-service"),
            {"fid": "4", "text": "Odpoved"},
        )
        self.assertEqual(400, res.status_code)

    def test_reply_requires_text(self):
        """Reply without text returns bad request."""
        self.client.force_login(user=self.receiver_user)
        res = self.client.post(
            reverse("ddcz:postal-service"),
            {"fid": "4", "id": str(self.letter.pk)},
        )
        self.assertEqual(400, res.status_code)

    def test_reply_to_nonexistent_letter(self):
        """Reply to nonexistent letter shows error and redirects."""
        self.client.force_login(user=self.receiver_user)
        res = self.client.post(
            reverse("ddcz:postal-service"),
            {"fid": "4", "id": "99999", "text": "Odpoved"},
            follow=True,
        )
        self.assertEqual(200, res.status_code)

    def test_reply_only_by_participant(self):
        """Only sender or receiver of original letter can reply to it."""
        other_user = User.objects.create_user(username="nekdo", password="heslo-nekdo")
        UserProfile.objects.create(
            nick="nekdo",
            email="nekdo@example.com",
            user=other_user,
        )
        self.client.force_login(user=other_user)
        res = self.client.post(
            reverse("ddcz:postal-service"),
            {
                "fid": "4",
                "id": str(self.letter.pk),
                "text": "Zkousim odpovedet",
            },
        )
        self.assertEqual(400, res.status_code)
        self.assertFalse(Letter.objects.filter(text="Zkousim odpovedet").exists())

    def test_sender_can_reply_to_own_letter(self):
        """Original sender can also reply (follow-up to their own message)."""
        self.client.force_login(user=self.sender_user)
        res = self.client.post(
            reverse("ddcz:postal-service"),
            {
                "fid": "4",
                "id": str(self.letter.pk),
                "text": "Doplneni k me zprave",
            },
            follow=True,
        )
        self.assertEqual(200, res.status_code)
        reply = Letter.objects.filter(text="Doplneni k me zprave").first()
        self.assertIsNotNone(reply)
        self.assertEqual(self.sender_nick, reply.sender)
        self.assertEqual(self.receiver_nick, reply.receiver)

    def test_reply_button_shown_in_letter_list(self):
        """Reply button with data-recipient is present for each letter."""
        self.client.force_login(user=self.receiver_user)
        res = self.client.get(reverse("ddcz:postal-service"))
        content = res.content.decode("utf-8")
        self.assertIn("postal_reply_button", content)
        self.assertIn(f'data-recipient="{self.sender_nick}"', content)
