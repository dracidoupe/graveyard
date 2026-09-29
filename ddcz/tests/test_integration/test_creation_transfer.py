from django.test import TestCase

from ddcz.creations import transfer_creations
from ddcz.models import AlchemistTool, Author, CommonArticle, UserProfile


def _make_author(nick, email):
    profile = UserProfile.objects.create(nick=nick, email=email)
    author = Author.objects.create(user=profile, author_type=Author.USER_TYPE)
    return profile, author


def _make_article(author, profile, **kwargs):
    defaults = {
        "name": "Article",
        "author": author,
        "author_nick": profile.nick if profile else None,
        "author_mail": profile.email if profile else None,
        "is_published": CommonArticle.CREATION_APPROVED,
        "creative_page_slug": "clanky",
    }
    defaults.update(kwargs)
    return CommonArticle.objects.create(**defaults)


def _make_tool(author, profile, **kwargs):
    defaults = {
        "name": "Tool",
        "author": author,
        "author_nick": profile.nick if profile else None,
        "author_mail": profile.email if profile else None,
        "is_published": AlchemistTool.CREATION_APPROVED,
    }
    defaults.update(kwargs)
    return AlchemistTool.objects.create(**defaults)


class TestTransferCreations(TestCase):
    def setUp(self):
        super().setUp()
        self.source_profile, self.source_author = _make_author(
            "Source", "source@example.com"
        )
        self.target_profile, self.target_author = _make_author(
            "Target", "target@example.com"
        )

    def test_creations_move_with_both_representations(self):
        article = _make_article(self.source_author, self.source_profile)

        transfer_creations(self.source_profile.pk, self.target_profile.pk)

        article.refresh_from_db()
        self.assertEqual(self.target_author, article.author)
        self.assertEqual(self.target_profile.nick, article.author_nick)
        self.assertEqual(self.target_profile.email, article.author_mail)

    def test_creation_matched_only_by_nick_when_fk_is_null(self):
        orphaned = _make_article(None, self.source_profile)

        moved = transfer_creations(self.source_profile.pk, self.target_profile.pk)

        orphaned.refresh_from_db()
        self.assertEqual([orphaned.pk], moved["CommonArticle"])
        self.assertEqual(self.target_author, orphaned.author)
        self.assertEqual(self.target_profile.nick, orphaned.author_nick)

    def test_misencoded_nick_is_matched(self):
        source_profile, source_author = _make_author("Břečťan", "b@example.com")
        article = _make_article(source_author, source_profile)

        moved = transfer_creations(source_profile.pk, self.target_profile.pk)

        article.refresh_from_db()
        self.assertEqual([article.pk], moved["CommonArticle"])
        self.assertEqual(self.target_author, article.author)

    def test_source_author_deleted_when_empty(self):
        _make_article(self.source_author, self.source_profile)

        transfer_creations(self.source_profile.pk, self.target_profile.pk)

        self.assertFalse(Author.objects.filter(pk=self.source_author.pk).exists())

    def test_source_author_kept_when_delete_disabled(self):
        _make_article(self.source_author, self.source_profile)

        transfer_creations(
            self.source_profile.pk,
            self.target_profile.pk,
            delete_empty_source_author=False,
        )

        self.assertTrue(Author.objects.filter(pk=self.source_author.pk).exists())

    def test_target_creations_are_additive(self):
        existing = _make_article(self.target_author, self.target_profile)
        moved_article = _make_article(self.source_author, self.source_profile)

        transfer_creations(self.source_profile.pk, self.target_profile.pk)

        existing.refresh_from_db()
        moved_article.refresh_from_db()
        self.assertEqual(self.target_author, existing.author)
        self.assertEqual(self.target_author, moved_article.author)

    def test_unrelated_user_creations_not_touched(self):
        other_profile, other_author = _make_author("Other", "other@example.com")
        other_article = _make_article(other_author, other_profile)
        _make_article(self.source_author, self.source_profile)

        transfer_creations(self.source_profile.pk, self.target_profile.pk)

        other_article.refresh_from_db()
        self.assertEqual(other_author, other_article.author)
        self.assertEqual(other_profile.nick, other_article.author_nick)

    def test_creation_ids_restricts_move(self):
        moved_article = _make_article(self.source_author, self.source_profile)
        kept_article = _make_article(self.source_author, self.source_profile)

        moved = transfer_creations(
            self.source_profile.pk,
            self.target_profile.pk,
            creation_ids={"CommonArticle": [moved_article.pk]},
        )

        moved_article.refresh_from_db()
        kept_article.refresh_from_db()
        self.assertEqual([moved_article.pk], moved["CommonArticle"])
        self.assertEqual(self.target_author, moved_article.author)
        self.assertEqual(self.source_author, kept_article.author)

    def test_round_trip_restores_original_state(self):
        # delete_empty_source_author=False on both legs: recreating a
        # deleted Author row at its original pk is the migration's job
        # (see 0023's `backwards`), not transfer_creations's -- this
        # isolates the round trip to what the function itself owns, the
        # FK and the denormalized nick/mail.
        article = _make_article(self.source_author, self.source_profile)
        tool = _make_tool(self.source_author, self.source_profile)

        moved = transfer_creations(
            self.source_profile.pk,
            self.target_profile.pk,
            delete_empty_source_author=False,
        )
        transfer_creations(
            self.target_profile.pk,
            self.source_profile.pk,
            creation_ids=moved,
            delete_empty_source_author=False,
        )

        article.refresh_from_db()
        tool.refresh_from_db()
        self.assertEqual(self.source_author, article.author)
        self.assertEqual(self.source_profile.nick, article.author_nick)
        self.assertEqual(self.source_profile.email, article.author_mail)
        self.assertEqual(self.source_author, tool.author)
        self.assertEqual(self.source_profile.nick, tool.author_nick)
        self.assertEqual(self.source_profile.email, tool.author_mail)

    def test_raises_when_target_has_no_author(self):
        no_author_profile = UserProfile.objects.create(
            nick="NoAuthor", email="noauthor@example.com"
        )
        _make_article(self.source_author, self.source_profile)

        with self.assertRaises(ValueError):
            transfer_creations(self.source_profile.pk, no_author_profile.pk)
