from urllib.request import urlopen
from django.conf import settings

from ddcz.models import Phorum

from ..model_generator import get_valid_article_chain
from .cases import SeleniumTestCase


class TestPhorum(SeleniumTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        data = get_valid_article_chain()

        cls.user = data["user"]
        cls.user.save()

        cls.comment = Phorum.objects.create(
            nickname="Author",
            email="test@example.com",
            text="Text of the comment",
            registered_or_ip="1",
            reputation=0,
            user=cls.user,
        )

        cls.selenium.get("%s%s" % (cls.live_server_url, "/forum/"))

    def test_page_heading_present(self):
        text = self.selenium.find_element_by_xpath('//h1[@class="page-heading"]').text
        self.assertEquals("Fórum", text)

    def test_author_rendered(self):
        text = self.selenium.find_element_by_xpath(
            '//div[@id="page-phorum"]//span[@class="nick"]'
        ).text.strip()
        self.assertEquals("Author", text)

    def test_comment_text_rendered(self):
        text = self.selenium.find_element_by_xpath(
            '//div[@id="page-phorum"]//p[@class="comment_text"]'
        ).text
        self.assertEquals(self.comment.text, text)

    def test_author_link_rendered(self):
        url = self.selenium.find_element_by_xpath(
            '//div[@id="page-phorum"]//span[@class="nick"]/a'
        ).get_attribute("href")
        self.assertIn(self.user.slug, url)
        self.assertIn(str(self.user.pk), url)
