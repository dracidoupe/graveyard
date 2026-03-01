from django.test import Client, TestCase
from django.urls import reverse

from ddcz.models import Author, CommonArticle, Monster

from ..model_generator import create_profiled_user


class CreationSubmitAccessTestCase(TestCase):
    fixtures = ["pages"]

    def setUp(self):
        super().setUp()
        self.client = Client()
        self.password = "testpassword123"
        self.user = create_profiled_user("testauthor", self.password)

    def test_anonymous_user_redirected(self):
        response = self.client.get(
            reverse("ddcz:creation-submit", kwargs={"creative_page_slug": "clanky"})
        )
        self.assertEqual(302, response.status_code)

    def test_authenticated_user_can_access(self):
        self.client.login(username="testauthor", password=self.password)
        response = self.client.get(
            reverse("ddcz:creation-submit", kwargs={"creative_page_slug": "clanky"})
        )
        self.assertEqual(200, response.status_code)

    def test_nonexistent_creative_page_returns_404(self):
        self.client.login(username="testauthor", password=self.password)
        response = self.client.get(
            reverse("ddcz:creation-submit", kwargs={"creative_page_slug": "neexistuje"})
        )
        self.assertEqual(404, response.status_code)


class CommonArticleSubmitTestCase(TestCase):
    fixtures = ["pages"]

    def setUp(self):
        super().setUp()
        self.client = Client()
        self.password = "testpassword123"
        self.user = create_profiled_user("testauthor", self.password)
        self.profile = self.user.profile
        self.profile.email = "author@example.com"
        self.profile.save()
        self.client.login(username="testauthor", password=self.password)

    def test_submit_common_article(self):
        response = self.client.post(
            reverse("ddcz:creation-submit", kwargs={"creative_page_slug": "clanky"}),
            {
                "name": "Testovaci clanek",
                "text": "Obsah clanku",
                "abstract": "Kratky popis",
            },
            follow=True,
        )
        self.assertEqual(200, response.status_code)

        article = CommonArticle.objects.filter(name="Testovaci clanek").first()
        self.assertIsNotNone(article)
        self.assertEqual("Obsah clanku", article.text)
        self.assertEqual("Kratky popis", article.abstract)
        self.assertEqual("clanky", article.creative_page_slug)
        self.assertEqual(CommonArticle.CREATION_NOT_APPROVED_YET, article.is_published)
        self.assertEqual("testauthor", article.author_nick)
        self.assertIsNotNone(article.author)
        self.assertEqual(Author.USER_TYPE, article.author.author_type)

    def test_submit_creates_author_if_not_exists(self):
        self.assertFalse(Author.objects.filter(user=self.profile).exists())

        self.client.post(
            reverse("ddcz:creation-submit", kwargs={"creative_page_slug": "clanky"}),
            {
                "name": "Prvni clanek",
                "text": "Text",
            },
        )

        author = Author.objects.get(user=self.profile)
        self.assertEqual(Author.USER_TYPE, author.author_type)
        self.assertEqual("testauthor", author.user_nick)

    def test_submit_reuses_existing_author(self):
        author = Author.objects.create(
            user=self.profile,
            author_type=Author.USER_TYPE,
            user_nick="testauthor",
        )

        self.client.post(
            reverse("ddcz:creation-submit", kwargs={"creative_page_slug": "clanky"}),
            {
                "name": "Druhy clanek",
                "text": "Text",
            },
        )

        self.assertEqual(1, Author.objects.filter(user=self.profile).count())
        article = CommonArticle.objects.get(name="Druhy clanek")
        self.assertEqual(author.pk, article.author.pk)

    def test_submit_sets_creative_page_slug_from_url(self):
        """creative_page_slug is set from the URL, not user input."""
        self.client.post(
            reverse(
                "ddcz:creation-submit", kwargs={"creative_page_slug": "novapovolani"}
            ),
            {
                "name": "Nove povolani",
                "text": "Popis",
            },
        )

        article = CommonArticle.objects.get(name="Nove povolani")
        self.assertEqual("novapovolani", article.creative_page_slug)

    def test_submit_requires_name(self):
        response = self.client.post(
            reverse("ddcz:creation-submit", kwargs={"creative_page_slug": "clanky"}),
            {
                "name": "",
                "text": "Obsah",
            },
        )
        self.assertEqual(200, response.status_code)
        self.assertFalse(CommonArticle.objects.filter(text="Obsah").exists())

    def test_submit_requires_text(self):
        response = self.client.post(
            reverse("ddcz:creation-submit", kwargs={"creative_page_slug": "clanky"}),
            {
                "name": "Clanek bez textu",
                "text": "",
            },
        )
        self.assertEqual(200, response.status_code)
        self.assertFalse(CommonArticle.objects.filter(name="Clanek bez textu").exists())

    def test_submit_shows_success_message(self):
        response = self.client.post(
            reverse("ddcz:creation-submit", kwargs={"creative_page_slug": "clanky"}),
            {
                "name": "Clanek s uspechem",
                "text": "Text",
            },
            follow=True,
        )
        self.assertContains(response, "bylo odesláno ke schválení")

    def test_submit_initializes_rating_fields(self):
        self.client.post(
            reverse("ddcz:creation-submit", kwargs={"creative_page_slug": "clanky"}),
            {
                "name": "Clanek s ratingem",
                "text": "Text",
            },
        )

        article = CommonArticle.objects.get(name="Clanek s ratingem")
        self.assertEqual(0, article.rater_no)
        self.assertEqual(0, article.rating_sum)
        self.assertEqual(0, article.rating)


class MonsterSubmitTestCase(TestCase):
    fixtures = ["pages"]

    def setUp(self):
        super().setUp()
        self.client = Client()
        self.password = "testpassword123"
        self.user = create_profiled_user("testauthor", self.password)
        self.profile = self.user.profile
        self.profile.email = "author@example.com"
        self.profile.save()
        self.client.login(username="testauthor", password=self.password)

    def test_submit_monster(self):
        response = self.client.post(
            reverse("ddcz:creation-submit", kwargs={"creative_page_slug": "bestiar"}),
            {
                "name": "Testovaci nestvura",
                "hitpoint_class": "A",
                "attack": "10/5",
                "defense": "4",
                "fortitude": "10",
                "size": "B",
                "experience": "100",
                "description": "Popis nestvury",
                "group": "Zvire",
            },
            follow=True,
        )
        self.assertEqual(200, response.status_code)

        monster = Monster.objects.filter(name="Testovaci nestvura").first()
        self.assertIsNotNone(monster)
        self.assertEqual("A", monster.hitpoint_class)
        self.assertEqual("Popis nestvury", monster.description)
        self.assertEqual(Monster.CREATION_NOT_APPROVED_YET, monster.is_published)

    def test_monster_form_has_correct_fields(self):
        response = self.client.get(
            reverse("ddcz:creation-submit", kwargs={"creative_page_slug": "bestiar"})
        )
        content = response.content.decode("utf-8")
        self.assertIn("Životaschopnost", content)
        self.assertIn("Útočné číslo", content)
        self.assertIn("Obranné číslo", content)


class FileUploadCreationSubmitTestCase(TestCase):
    """File-upload creation types show an informational message instead of a form."""

    fixtures = ["pages"]

    def setUp(self):
        super().setUp()
        self.client = Client()
        self.password = "testpassword123"
        self.user = create_profiled_user("testauthor", self.password)
        self.client.login(username="testauthor", password=self.password)

    def test_gallery_shows_not_yet_available(self):
        response = self.client.get(
            reverse("ddcz:creation-submit", kwargs={"creative_page_slug": "galerie"})
        )
        self.assertEqual(200, response.status_code)
        self.assertContains(response, "zatím není k dispozici")

    def test_download_shows_not_yet_available(self):
        response = self.client.get(
            reverse("ddcz:creation-submit", kwargs={"creative_page_slug": "downloady"})
        )
        self.assertEqual(200, response.status_code)
        self.assertContains(response, "zatím není k dispozici")
