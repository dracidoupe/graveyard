from urllib.parse import urlsplit

from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sitemaps.views import index as sitemap_index_view
from django.contrib.sitemaps.views import sitemap as sitemap_view
from django.core.cache import cache
from django.core.management.base import BaseCommand
from django.test import RequestFactory

from ...sitemaps import SITEMAPS, sitemap_index_cache_key, sitemap_section_cache_key


class Command(BaseCommand):
    help = (
        "Precompute sitemap.xml (index + all sections/pages) and store it in the cache "
    )

    def handle(self, *args, **options):
        base_uri = urlsplit(settings.EMAIL_LINKS_BASE_URI)
        secure = base_uri.scheme == "https"
        factory = RequestFactory()

        def render(view, path, query=None, **kwargs):
            request = factory.get(
                path, query or {}, secure=secure, HTTP_HOST=base_uri.netloc
            )
            # Include common variables
            request.session = SessionStore()
            request.user = AnonymousUser()
            request.ddcz_profile = None
            response = view(request, sitemaps=SITEMAPS, **kwargs)
            response.render()
            return response.content

        index_content = render(
            sitemap_index_view,
            "/sitemap.xml",
            sitemap_url_name="ddcz:sitemap-section",
        )
        cache.set(
            sitemap_index_cache_key(), index_content, settings.SITEMAP_CACHE_INTERVAL
        )

        for name, sitemap_cls in SITEMAPS.items():
            num_pages = sitemap_cls().paginator.num_pages
            for page in range(1, num_pages + 1):
                content = render(
                    sitemap_view,
                    f"/sitemap-{name}.xml",
                    query={"p": page},
                    section=name,
                )
                cache.set(
                    sitemap_section_cache_key(name, page),
                    content,
                    settings.SITEMAP_CACHE_INTERVAL,
                )

        self.stdout.write("Sitemap warmed.")
