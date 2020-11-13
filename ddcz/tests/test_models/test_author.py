from django.test import SimpleTestCase, TestCase

from ..model_generator import get_valid_article_chain

from ddcz.models import Author, CommonArticle, UserProfile, Quest

class TestAuthorLinkRender(SimpleTestCase):
    def setUp(self):
        super().setUp()

        data = get_valid_article_chain()

        self.user = data['user']
        self.author_user = data['author']
        self.article = data['article']

    def test_name_inferred(self):
        self.assertEqual('Author', self.author_user.name)

    def test_profile_url_inferred(self):
        self.assertEqual('/autor/1-author/', self.author_user.profile_url)

class TestAuthorCretionsList(TestCase):
    fixtures = ['pages']

    def setUp(self):
        super().setUp()

        data = get_valid_article_chain()

        self.user = data['user']
        self.author_user = data['author']
        self.article = data['article']

        self.quest = Quest(
            jmeno = 'Example Quest',
            author = self.author_user,
            autor = self.user.nick_uzivatele,
            autmail = self.user.email_uzivatele,
            schvaleno = Quest.CREATION_APPROVED
        )

        self.user.save()
        self.author_user.save()
        self.article.save()
        self.quest.save()

    def test_author_relation_saved_properly(self):
        self.assertEqual(self.author_user, self.article.author)
        self.assertEqual(self.author_user, Quest.objects.all()[0].author)

    def test_author_creations_pages_returned(self):
        author_creations = self.author_user.get_all_creations()

        self.assertEqual(['clanky', 'dobrodruzstvi'], list(author_creations))

    def test_author_creations_returned(self):
        author_creations = self.author_user.get_all_creations()

        self.assertEqual('Example Quest', author_creations['dobrodruzstvi']['creations'][0].jmeno)
        self.assertEqual('Test Article', author_creations['clanky']['creations'][0].jmeno)

    def test_author_pages_returned(self):
        author_creations = self.author_user.get_all_creations()

        self.assertEqual('clanky', author_creations['clanky']['page'].slug)
