from urllib.parse import urlparse

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.conf import settings

from ddcz.feeds import CompleteNewsFeed
from ddcz.models import (
    News,
    Phorum,
    Dating,
    CreationComment,
    CreativePage,
)
from ddcz.creations import ApprovalChoices
from ddcz.tests.model_generator import get_valid_article_chain

import feedparser


class FeedTestCase(TestCase):
    def assertItemInFeed(self, item, feed_items):
        """Helper method to check if an item is in feed items"""
        self.assertIn(item, feed_items)

    def assertItemNotInFeed(self, item, feed_items):
        """Helper method to check if an item is not in feed items"""
        self.assertNotIn(item, feed_items)


class TestCompleteNewsFeed(FeedTestCase):
    fixtures = ["pages"]

    def setUp(self):
        super().setUp()
        self.feed = CompleteNewsFeed()
        self.now = timezone.now()

        # Create test data
        self.news = News.objects.create(
            author="TestAuthor",
            text="Test news",
            date=self.now,
            author_mail="test@example.com",
        )

        self.phorum = Phorum.objects.create(
            nickname="TestUser",
            text="Test forum post",
            date=self.now,
            registered_or_ip="1",
            reputation=0,
            email="test@example.com",
        )

        self.dating = Dating.objects.create(
            name="Test Dating",
            group="hledam_hrace",
            published=self.now,
            text="Test dating post",
            area="Praha",
        )

        # Create article chain with author
        article_chain = get_valid_article_chain()
        self.user_profile = article_chain["user"]
        self.author = article_chain["author"]
        self.article = article_chain["article"]
        self.article.published = self.now
        self.article.text = "Test article text"
        self.article.abstract = "Test article abstract"

        # Save the models
        self.user_profile.save()
        self.author.save()
        self.article.save()

        self.comment = CreationComment.objects.create(
            nickname="TestCommenter",
            text="Test comment",
            date=self.now,
            foreign_table=self.article.creative_page_slug,
            foreign_id=self.article.id,
            email="test@example.com",
        )


class TestFeedBasics(TestCompleteNewsFeed):
    def test_feed_attributes(self):
        """Test basic feed attributes"""
        self.assertEqual(self.feed.title, "Novinky na Dračím Doupěti")
        self.assertEqual(self.feed.link, "/novinky/")
        self.assertEqual(
            self.feed.description, "Všechny veřejně dostupné novinky na Dračím Doupěti"
        )

    def test_feed_url_accessible(self):
        """Test that feed URL is accessible"""
        response = self.client.get(reverse("ddcz:creations-feed"))
        self.assertEqual(response.status_code, 200)

    def test_all_feed_items_have_urls(self):
        """Test that all items in the rendered feed have valid URLs"""
        response = self.client.get(reverse("ddcz:creations-feed"))
        self.assertEqual(response.status_code, 200)

        feed = feedparser.parse(response.content)

        # Verify each entry has a link
        for entry in feed.entries:
            self.assertTrue(
                hasattr(entry, "link"), f"Feed entry {entry.title} has no link"
            )
            self.assertTrue(entry.link, f"Feed entry {entry.title} has empty link")
            # Verify the link is accessible
            parsed = urlparse(entry.link)
            self.assertTrue(parsed.path, f"Link {entry.link} has no path component")

    def test_feed_guids_unique(self):
        """Test that all items in the feed have unique GUIDs"""
        response = self.client.get(reverse("ddcz:creations-feed"))
        self.assertEqual(response.status_code, 200)

        feed = feedparser.parse(response.content)

        # Collect all GUIDs
        guids = [entry.get("id") for entry in feed.entries if entry.get("id")]

        # Check that we have GUIDs
        self.assertTrue(len(guids) > 0, "No GUIDs found in feed entries")

        # Check for uniqueness
        unique_guids = set(guids)
        self.assertEqual(
            len(guids), len(unique_guids), "Duplicate GUIDs found in feed entries"
        )


class TestFeedContent(TestCompleteNewsFeed):
    def test_all_models_included(self):
        """Test that items() returns content from all included models"""
        items = list(self.feed.items())

        self.assertItemInFeed(self.news, items)
        self.assertItemInFeed(self.phorum, items)
        self.assertItemInFeed(self.dating, items)
        self.assertItemInFeed(self.article, items)
        self.assertItemInFeed(self.comment, items)

    def test_item_title_formatting(self):
        """Test that item_title formats titles correctly for each content type"""
        self.assertEqual(
            self.feed.item_title(self.news), f"Aktualita od {self.news.author}"
        )
        self.assertEqual(
            self.feed.item_title(self.dating),
            f"{self.dating.name} v sekci {self.dating.group}",
        )
        self.assertEqual(
            self.feed.item_title(self.phorum), f"{self.phorum.nickname} ve fóru"
        )
        self.assertEqual(
            self.feed.item_title(self.comment),
            f"Komentář k dílu od {self.comment.nickname}",
        )

        # this is normally set by get_item; fix when we have backlinks implemented
        self.article.creative_page = CreativePage.objects.get(slug="clanky")
        self.assertEqual(
            self.feed.item_title(self.article),
            f"{self.article.name} v rubrice {self.article.creative_page.name}",
        )


class TestFeedLimits(TestCompleteNewsFeed):
    def test_respects_rss_item_limits(self):
        """Test that the feed respects RSS item count limits from settings"""
        # Create more items than the limit
        for i in range(settings.RSS_LATEST_ITEMS_COUNT + 5):
            News.objects.create(author=f"Author{i}", text=f"News {i}", date=self.now)

        items = self.feed.items()
        news_items = [item for item in items if isinstance(item, News)]
        self.assertLessEqual(len(news_items), settings.RSS_LATEST_ITEMS_COUNT)

    def test_comment_count_limit(self):
        """Test that comment count is limited according to settings"""
        # Create more comments than the limit
        for i in range(settings.RSS_COMMENT_ITEMS_COUNT + 5):
            CreationComment.objects.create(
                nickname=f"Commenter{i}",
                text=f"Comment {i}",
                date=self.now,
                foreign_table="test-page",
                foreign_id=self.article.id,
            )

        items = self.feed.items()
        comment_items = [item for item in items if isinstance(item, CreationComment)]
        self.assertLessEqual(len(comment_items), settings.RSS_COMMENT_ITEMS_COUNT)


class TestCreativePageFiltering(TestCompleteNewsFeed):
    def test_approved_articles_included(self):
        """Test that approved articles are included in the feed"""
        items = list(self.feed.items())
        self.assertItemInFeed(self.article, items)

    def test_unapproved_articles_excluded(self):
        """Test that unapproved articles are not included in the feed"""
        article_chain = get_valid_article_chain()
        unapproved = article_chain["article"]
        unapproved.is_published = ApprovalChoices.WAITING.value
        unapproved.published = self.now
        unapproved.save()

        items = list(self.feed.items())
        self.assertItemNotInFeed(unapproved, items)
