from datetime import datetime
import pytz

from django.test import TestCase

from ddcz.models import News, UserProfile


class AnimalTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.problematic_diacritic_string = "ěščřžýáíéďťň"

    def test_set_save_doesnt_destroy_model(self):
        p = UserProfile(nick_uzivatele=self.problematic_diacritic_string)
        p.save()

        self.assertEquals(self.problematic_diacritic_string, p.nick_uzivatele)

    def test_set_save_doesnt_destroy_database(self):
        p = UserProfile.objects.create(nick_uzivatele=self.problematic_diacritic_string)

        d = UserProfile.objects.get(id=p.id).nick_uzivatele

        self.assertEquals(self.problematic_diacritic_string, d)


class NewsTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.problematic_diacritic_string = "ěščřžýáíéďťň"

    def test_save_and_read(self):
        p = News(
            date=datetime.now(pytz.timezone("Europe/Prague")),
            author="xoxo",
            author_mail="xoxo@example.com",
            text=self.problematic_diacritic_string,
        )
        p.save()

        self.assertEquals(self.problematic_diacritic_string, p.text)
