from django.urls import reverse

from django.contrib.syndication.views import Feed

from ddcz.models import Phorum


class PhorumFeed(Feed):
    title = "Fórum Dračího Doupěte"
    link = "/forum/"
    description = "Veřejná diskuze ve Fóru."

    def items(self):
        return Phorum.objects.order_by("-date")[:50]

    def item_title(self, item):
        return f"{item.nickname} v {item.date}"

    def item_description(self, item):
        return item.text

    def item_link(self, item):
        return reverse("ddcz:phorum-item", args=[item.id])
