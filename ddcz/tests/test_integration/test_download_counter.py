from unittest.mock import patch, PropertyMock

from django.db.models.fields.files import FieldFile
from django.test import Client, TestCase
from django.urls import reverse

from ddcz.creations import ApprovalChoices
from ddcz.models import DownloadItem


class DownloadCounterTestCase(TestCase):
    fixtures = ["pages"]

    def setUp(self):
        super().setUp()
        self.client = Client()

        self.download_item = DownloadItem(
            pk=1,
            name="Test Download",
            is_published=ApprovalChoices.APPROVED.value,
            format="pdf",
            description="Test description",
            size=1024,
            group="test",
            download_counter=0,
            rating=0,
        )
        self.download_item.save()

    @patch.object(FieldFile, "url", new_callable=PropertyMock, return_value="/fake/url")
    def test_download_counter_increments(self, mock_url):
        initial_count = self.download_item.download_counter
        self.assertEqual(0, initial_count)

        url = reverse(
            "ddcz:download-file", kwargs={"download_id": self.download_item.pk}
        )
        response = self.client.get(url)

        self.assertEqual(302, response.status_code)

        self.download_item.refresh_from_db()
        self.assertEqual(1, self.download_item.download_counter)

    @patch.object(FieldFile, "url", new_callable=PropertyMock, return_value="/fake/url")
    def test_download_counter_increments_multiple_times(self, mock_url):
        url = reverse(
            "ddcz:download-file", kwargs={"download_id": self.download_item.pk}
        )

        for i in range(3):
            self.client.get(url)

        self.download_item.refresh_from_db()
        self.assertEqual(3, self.download_item.download_counter)

    @patch.object(FieldFile, "url", new_callable=PropertyMock, return_value="/fake/url")
    def test_download_returns_redirect_to_file(self, mock_url):
        url = reverse(
            "ddcz:download-file", kwargs={"download_id": self.download_item.pk}
        )
        response = self.client.get(url)

        self.assertEqual(302, response.status_code)
        self.assertEqual("/fake/url", response.url)

    def test_download_nonexistent_returns_404(self):
        url = reverse("ddcz:download-file", kwargs={"download_id": 99999})
        response = self.client.get(url)

        self.assertEqual(404, response.status_code)

    @patch.object(FieldFile, "url", new_callable=PropertyMock, return_value="/fake/url")
    def test_head_request_increments_counter(self, mock_url):
        url = reverse(
            "ddcz:download-file", kwargs={"download_id": self.download_item.pk}
        )
        response = self.client.head(url)

        self.assertEqual(302, response.status_code)

        self.download_item.refresh_from_db()
        self.assertEqual(1, self.download_item.download_counter)
