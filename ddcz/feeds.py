from django.conf import settings
from django.urls import reverse

from django.contrib.syndication.views import Feed

from ddcz.models import Phorum, News, CreativePage, Dating, CreationComment, Creation
from ddcz.creations import ApprovalChoices


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

    def item_pubdate(self, item):
        return item.date


class CompleteNewsFeed(Feed):
    title = "Novinky na Dračím Doupěti"
    link = "/novinky/"
    description = "Všechny veřejně dostupné novinky na Dračím Doupěti"

    INCLUDED_MODELS = [
        News,
        CreativePage,
        Dating,
        Phorum,
        # Getting URL of comment creation is expensive due to lack of generic relation,
        # it has (n+1) and hence is currently capped to lower number
        CreationComment,
    ]

    def items(self):
        # current cache is long lived; implement push cache in case it's a problem;
        # Also most queries are for the articles that change the least often,
        # so maybe a separate cache there

        items = []
        for model in self.INCLUDED_MODELS:
            if model in [Phorum, News]:
                items.extend(
                    model.objects.order_by("-date")[: settings.RSS_LATEST_ITEMS_COUNT]
                )
            elif model == Dating:
                items.extend(
                    model.objects.order_by("-published")[
                        : settings.RSS_LATEST_ITEMS_COUNT
                    ]
                )
            elif model == CreationComment:
                items.extend(
                    model.objects.order_by("-date")[: settings.RSS_COMMENT_ITEMS_COUNT]
                )
            elif model == CreativePage:
                pages = CreativePage.get_all_models()
                for page in pages:
                    model = page["model"]
                    query = (
                        model.objects.filter(
                            is_published=ApprovalChoices.APPROVED.value
                        )
                        # .select_related("creative_page")
                        .order_by("-published")
                    )
                    if model.__name__ == "CommonArticle":
                        query = query.filter(creative_page_slug=page["page"].slug)
                    query = query[0 : settings.RSS_LATEST_ITEMS_COUNT]
                    for creation in query:
                        creation.creative_page = page["page"]
                        items.append(creation)
            else:
                raise ValueError(f"Model {model} is not supported")
        return items

    def item_title(self, item):
        if isinstance(item, News):
            return f"Aktualita od {item.author}"
        elif isinstance(item, Dating):
            return f"{item.name} v sekci {item.group}"
        elif isinstance(item, Phorum):
            return f"{item.nickname} ve fóru"
        elif isinstance(item, CreationComment):
            # Retrieving the creation name is expensive, so only do upon request
            return f"Komentář k dílu od {item.nickname}"
        elif isinstance(item, Creation):
            return f"{item.name} v rubrice {item.creative_page.name}"
        else:
            return item.name

    def item_guid(self, item):
        return f"ddcz:{item.__class__.__name__.lower()}:{item.id}"

    def item_pubdate(self, item):
        if isinstance(item, (News, Phorum, CreationComment)):
            return item.date
        elif isinstance(item, (Dating, Creation)):
            return item.published
        else:
            return None

    def item_description(self, item):
        if isinstance(item, (News, Dating, Phorum, CreationComment)):
            return item.text
        elif isinstance(item, Creation):
            if hasattr(item, "text"):
                text = item.text
                if len(text) > 255:
                    text = text[:255] + "... (pro plný text navštivte stránku)"
                return text
            else:
                return str(item)
        else:
            return str(item)
