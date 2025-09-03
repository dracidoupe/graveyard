from datetime import timedelta
from django.test import TestCase, Client
from django.utils import timezone
from django.core.cache import cache
from django.conf import settings

from ..models import CreativePage, CreationComment, CommonArticle
from ..creations import ApprovalChoices


class TestNewsfeed(TestCase):
    def setUp(self):
        self.client = Client()
        cache.clear()
        self.creative_page = CreativePage.objects.create(
            name="Test Page", slug="test-page", model_class="ddcz.CommonArticle"
        )

    def test_newsfeed_empty_response(self):
        """Test that newsfeed returns 200 even when there are no articles or comments"""
        response = self.client.get("/novinky/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "news/newsfeed.html")
        self.assertEqual(len(response.context["articles"]), 0)
        self.assertEqual(len(response.context["comments"]), 0)

    def test_newsfeed_caching(self):
        """Test that newsfeed results are cached"""
        # Create some test data
        CommonArticle.objects.create(
            name="Test Article",
            is_published=ApprovalChoices.APPROVED.value,
            published=timezone.now(),
            creative_page_slug=self.creative_page.slug,
            text="Test content",
        )

        # First request should hit the database
        response1 = self.client.get("/novinky/")
        cached_data = cache.get(settings.NEWSFEED_CACHE_KEY)
        self.assertIsNotNone(cached_data)
        self.assertIn("articles", cached_data)
        self.assertIn("comments", cached_data)

        # Verify the cached data matches what we expect
        self.assertEqual(len(cached_data["articles"]), 1)
        self.assertEqual(cached_data["articles"][0].name, "Test Article")
        self.assertEqual(len(cached_data["comments"]), 0)

        # Second request should use cache and make no database queries
        with self.assertNumQueries(0):
            response2 = self.client.get("/novinky/")

        self.assertEqual(
            [a.name for a in response1.context["articles"]],
            [a.name for a in response2.context["articles"]],
        )

    def test_newsfeed_old_articles_filtered(self):
        """Test that articles older than NEWSFEED_OLDEST_ARTICLE_INTERVAL_WEEKS are filtered out"""
        self.assertEqual(0, CommonArticle.objects.count())
        old_article = CommonArticle.objects.create(
            name="Old Article",
            is_published=ApprovalChoices.APPROVED.value,
            creative_page_slug=self.creative_page.slug,
            text="Old content",
        )
        old_article.published = timezone.now() - timedelta(
            weeks=settings.NEWSFEED_OLDEST_ARTICLE_INTERVAL_WEEKS + 1
        )
        old_article.save()

        CommonArticle.objects.create(
            name="Recent Article",
            is_published=ApprovalChoices.APPROVED.value,
            creative_page_slug=self.creative_page.slug,
            text="Recent content",
        )

        response = self.client.get("/novinky/")
        articles = response.context["articles"]

        # Only recent article should be present
        self.assertEqual(
            len(articles), 1, "Expected only one article (recent), but got more"
        )
        self.assertEqual(articles[0].name, "Recent Article")

    def test_newsfeed_max_items(self):
        """Test that newsfeed respects max items limits"""
        now = timezone.now()
        # Create test articles that exceed the limit
        articles = []
        for i in range(settings.NEWSFEED_MAX_CREATIONS + 5):
            article = CommonArticle.objects.create(
                name=f"Article {i}",
                is_published=ApprovalChoices.APPROVED.value,
                creative_page_slug=self.creative_page.slug,
                text=f"Content {i}",
            )
            article.published = now - timedelta(minutes=i)
            article.save()
            articles.append(article)

        # Create test comments that exceed the limit
        article = articles[0]
        for i in range(settings.NEWSFEED_MAX_COMMENTS + 5):
            CreationComment.objects.create(
                text=f"Comment {i}",
                date=now - timedelta(minutes=i),
                foreign_table=self.creative_page.slug,
                foreign_id=article.id,
            )

        # Clear any cached data to ensure we get fresh results
        cache.clear()

        response = self.client.get("/novinky/")

        # Check that the number of items is limited
        self.assertLessEqual(
            len(response.context["articles"]), settings.NEWSFEED_MAX_CREATIONS
        )
        self.assertLessEqual(
            len(response.context["comments"]), settings.NEWSFEED_MAX_COMMENTS
        )

    def test_unpublished_articles_filtered(self):
        """Test that unpublished articles are not shown"""
        # Create an unpublished article
        CommonArticle.objects.create(
            name="Unpublished Article",
            is_published=ApprovalChoices.WAITING.value,
            creative_page_slug=self.creative_page.slug,
            text="Unpublished content",
        )

        # Create a published article
        CommonArticle.objects.create(
            name="Published Article",
            is_published=ApprovalChoices.APPROVED.value,
            creative_page_slug=self.creative_page.slug,
            text="Published content",
        )

        # Clear any cached data to ensure we get fresh results
        cache.clear()

        response = self.client.get("/novinky/")
        articles = response.context["articles"]

        # Only published article should be present
        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0].name, "Published Article")

    def tearDown(self):
        # Clean up after each test
        cache.clear()
