from html import unescape

from django.conf import settings
from django.core.cache import cache
from django.core.mail import send_mail
from django.db import transaction
from django.urls import reverse
from django.utils import timezone

from .commonarticles import COMMON_ARTICLES_CREATIVE_PAGES
from .creations import ApprovalChoices, PENDING_STATES
from .models import (
    Author,
    CommonArticle,
    CreationComment,
    CreationVote,
    NotificationEvent,
)
from .email import notify_staff_about_submission
from .notifications import schedule_notification
from .text import escape_user_input

RATING_ABSTAIN = 8
EDITOR_VOTE_WEIGHT = 3
# Editor votes above this are the "special" ones (competition winners) that can't be changed
EDITOR_VOTE_LOCKED_ABOVE = 5


def get_article_url(article):
    return settings.EMAIL_LINKS_BASE_URI + reverse(
        "ddcz:creation-detail",
        kwargs={
            "creative_page_slug": article.creative_page_slug,
            "creation_id": article.pk,
            "creation_slug": article.get_slug(),
        },
    )


def get_author_email(article):
    if article.author and article.author.user and article.author.user.email:
        return article.author.user.email
    return article.author_mail


def submit_common_article(
    user_profile, creative_page_slug, name, abstract, section, text
):
    if creative_page_slug not in COMMON_ARTICLES_CREATIVE_PAGES:
        raise ValueError(f"{creative_page_slug} is not a common article page")

    author, _ = Author.objects.get_or_create(
        user=user_profile,
        author_type=Author.USER_TYPE,
        defaults={"user_nick": user_profile.nick},
    )

    article = CommonArticle.objects.create(
        name=name,
        abstract=abstract,
        section=section,
        text=text,
        creative_page_slug=creative_page_slug,
        author=author,
        author_nick=user_profile.nick,
        author_mail=user_profile.email,
        is_published=ApprovalChoices.WAITING.value,
        rating=0,
        rater_no=0,
        rating_sum=0,
    )
    notify_staff_about_submission(article)
    return article


def withdraw_common_article(article, user_profile):
    if article.is_published not in PENDING_STATES:
        return False
    if not article.author or article.author.user_id != user_profile.pk:
        return False

    article.is_published = ApprovalChoices.WITHDRAWN.value
    article.save()
    return True


@transaction.atomic
def approve_common_article(article, editor_profile, rating, comment=""):
    if article.is_published not in PENDING_STATES:
        raise ValueError("Only pending articles can be approved")

    article.is_published = ApprovalChoices.APPROVED.value
    article.published = timezone.now()
    if rating == RATING_ABSTAIN:
        article.rating = 0
        article.rater_no = 0
        article.rating_sum = 0
    else:
        article.rating = rating
        article.rater_no = EDITOR_VOTE_WEIGHT
        article.rating_sum = EDITOR_VOTE_WEIGHT * rating
    article.save()

    CreationVote.objects.update_or_create(
        user_profile=editor_profile,
        creation_id=article.pk,
        creative_page_slug=article.creative_page_slug,
        defaults={
            "rating": rating,
            "time": int(timezone.now().timestamp()),
            "changed": "1" if rating > EDITOR_VOTE_LOCKED_ABOVE else "0",
        },
    )

    if comment:
        CreationComment.objects.create(
            nickname=editor_profile.nick,
            email=editor_profile.email,
            user=editor_profile,
            reputation=0,
            text=escape_user_input(comment),
            foreign_id=article.pk,
            foreign_table=article.creative_page_slug,
        )

    send_mail(
        "Schválení příspěvku na DraciDoupe.cz",
        f"""Zdravíme,

Váš příspěvek "{unescape(article.name)}" byl schválen a je zveřejněn na {get_article_url(article)} .

— Redakce DraciDoupe.cz
""",
        settings.DDCZ_TRANSACTION_EMAIL_FROM,
        [get_author_email(article)],
    )

    schedule_notification(
        event=NotificationEvent.CREATION_APPROVED,
        affected_object=article,
        extra_data={"creative_page_slug": article.creative_page_slug},
    )

    cache.delete_many(
        [
            f"creative-page:{article.creative_page_slug}:list",
            settings.NEWSFEED_CACHE_KEY,
        ]
    )


@transaction.atomic
def reject_common_article(article, editor_profile, reason):
    if article.is_published not in PENDING_STATES:
        raise ValueError("Only pending articles can be rejected")

    article.is_published = ApprovalChoices.REJECTED.value
    article.save()

    send_mail(
        "Zamítnutí příspěvku na DraciDoupe.cz",
        f"""Zdravíme,

redaktor {editor_profile.nick} zamítl Váš příspěvek "{unescape(article.name)}" s následujícím odůvodněním:

{reason}

— Redakce DraciDoupe.cz
""",
        settings.DDCZ_TRANSACTION_EMAIL_FROM,
        [get_author_email(article)],
    )
