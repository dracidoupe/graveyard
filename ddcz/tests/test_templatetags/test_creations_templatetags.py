from .case import TemplateTestCase
from ..model_generator import get_valid_article_chain

from ddcz.models import Author, CommonArticle, UserProfile


class TestAuthorLinkRender(TemplateTestCase):
    fixtures = ["pages"]

    def setUp(self):
        super().setUp()

        data = get_valid_article_chain()

        self.user = data["user"]
        self.author_user = data["author"]
        self.article = data["article"]

    def test_user_link(self):
        render = self.render_template(
            "{% load creations %}" "{% author_display article %}",
            context={"article": self.article},
        )

        self.assertHTMLEqual(
            """<a rel="author" class="author" href="/autor/1-author/">Author</a>""",
            render,
        )
