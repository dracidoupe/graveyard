from django.test import TestCase

from ..model_generator import get_valid_article_chain

from ddcz.models import Phorum


class TestAuthorLinkRender(TestCase):
    def setUp(self):
        super().setUp()

        data = get_valid_article_chain()

        self.user = data["user"]
        self.user.save()

        self.comment = Phorum.objects.create(
            nickname="Author",
            email="test@example.com",
            text="Text of the comment",
            reg="1",
            reputace=0,
            user=self.user,
        )

    def test_name_inferred(self):
        comment = Phorum.objects.all()[0]
        self.assertEqual(self.user.profile_url, comment.user_profile_url)
