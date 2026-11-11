import json
from html import unescape
from urllib.parse import urljoin

from django.conf import settings
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe
from django.utils.text import Truncator

from .models import GalleryPicture, Monster, Photo

SITE_NAME = "DraciDoupe.cz"
DESCRIPTION_MAX_LENGTH = 160

JSON_LD_ESCAPES = {
    ord(">"): "\\u003E",
    ord("<"): "\\u003C",
    ord("&"): "\\u0026",
}


def plain_text(entity_string):
    if not entity_string:
        return ""
    text = strip_tags(unescape(entity_string))
    return " ".join(unescape(text).split())


def meta_description(text):
    return Truncator(plain_text(text)).chars(DESCRIPTION_MAX_LENGTH)


def absolute_url(path):
    return urljoin(settings.EMAIL_LINKS_BASE_URI, path)


def monster_stats(monster):
    stats = [
        plain_text(monster.group),
        f"velikost {plain_text(monster.size)}" if monster.size else "",
        f"ŽT {plain_text(monster.hitpoint_class)}" if monster.hitpoint_class else "",
        f"ÚČ {plain_text(monster.attack)}" if monster.attack else "",
    ]
    return ", ".join(stat for stat in stats if stat)


def author_name(creation):
    if creation.author_id:
        return creation.author.name
    return creation.author_nick or "Neznámý"


def creation_description(creation, creative_page):
    if isinstance(creation, (GalleryPicture, Photo)):
        return meta_description(
            f"Obrázek {creation.name} od {author_name(creation)} v rubrice {creative_page.name}"
        )

    body = ""
    for attr in ("abstract", "description", "text"):
        body = plain_text(getattr(creation, attr, None))
        if body:
            break

    if isinstance(creation, Monster):
        stats = monster_stats(creation)
        if stats:
            body = f"{stats}. {body}" if body else stats

    if not body:
        body = f"{creation.name} – {creative_page.name} na {SITE_NAME}"

    return meta_description(body)


def creation_json_ld(creation, creative_page, url, description, image_url=None):
    data = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": plain_text(creation.name),
        "articleSection": creative_page.name,
        "author": {"@type": "Person", "name": author_name(creation)},
        "datePublished": creation.published.isoformat(),
        "url": url,
        "mainEntityOfPage": url,
        "description": description,
        "publisher": {"@type": "Organization", "name": SITE_NAME},
    }
    if image_url:
        data["image"] = image_url

    return mark_safe(json.dumps(data, ensure_ascii=False).translate(JSON_LD_ESCAPES))
