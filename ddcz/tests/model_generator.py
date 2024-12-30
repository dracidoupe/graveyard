from random import randint

from django.contrib.auth.models import User
from ddcz.models import (
    Author,
    CommonArticle,
    UserProfile,
    Market,
    MARKET_SECTION_CHOICES,
)

from ddcz.tavern import (
    create_tavern_table,
    bookmark_table,
)


def get_valid_article_chain():
    user = UserProfile(nick="Author", email="test@example.com")

    author = Author(id=1, user=user, author_type=Author.USER_TYPE)

    article = CommonArticle(
        author=author,
        name="Test Article",
        author_nick=user.nick,
        author_mail=user.email,
        is_published=CommonArticle.CREATION_APPROVED,
        creative_page_slug="clanky",
    )

    return {
        "user": user,
        "author": author,
        "article": article,
    }


def get_alphabetic_user_profiles(
    number_of_users=1, saved=False, with_corresponding_user=False, nick_prefix=""
):
    if number_of_users > 26:
        raise NotImplementedError("Out of alphabet, reimplement this function")

    alphabet_letters = map(chr, range(97, 97 + number_of_users))
    profiles = []
    for letter in alphabet_letters:
        nick = letter
        if nick_prefix:
            nick = f"{nick_prefix}-{letter}"
        email = f"{nick}@example.com"

        profile = UserProfile(nick=nick, email=email)
        profiles.append(profile)
        if saved:
            profile.save()

        if with_corresponding_user:
            user = User(username=nick, email=email)
            user.set_password(email)
            profile.user = user

        if saved and with_corresponding_user:
            user.save()
            # This needs reassigning to properly mark the field dirty with the correct foreign ID
            profile.user = user
            profile.save()

    return profiles


def create_profiled_user(username, password, email=False):
    if not email:
        email = f"{username}@example.com"
    profile = UserProfile(nick=username, email=email)
    user = User.objects.create_user(username=username, password=password)
    profile.user = user
    profile.save()
    return user


def create_test_tavern_table(all_users, bookmark, public):
    owner, allowed_user, banned_user, visiting_user = all_users

    public_desc = "Public" if public else "Private"
    bookmark_desc = "Bookmarked" if bookmark else "Unbookmarked"

    table = create_tavern_table(
        owner=owner,
        public=public,
        name=f"{public_desc.lower()}_{bookmark_desc.lower()}_table",
        description=f"{public_desc} {bookmark_desc} Table",
    )

    if bookmark:
        for user in all_users:
            bookmark_table(user, table)

    table.update_access_privileges(
        access_banned=[banned_user.id], access_allowed=[allowed_user.id]
    )

    return table


def get_tavern_tables(owner, allowed_user, banned_user, visiting_user):
    """
    Return all configurations of tavern tables interesting for testing, in a dictionary:
    * Public tables, bookmarked and unbookmarked by all users
    * Private tables, bookmarked and unbookmarked by all users
    * All tables are owned by owner
    * All tables are accessible to allowed_user
    * All tables are inaccessible to banned_user
    * Public tables are accessible to visiting_user, private tables are inaccessible to visiting_user
    """
    all_users = [owner, allowed_user, banned_user, visiting_user]
    return {
        "bookmarked_public_table": create_test_tavern_table(
            all_users, bookmark=True, public=True
        ),
        "unbookmarked_public_table": create_test_tavern_table(
            all_users, bookmark=False, public=True
        ),
        "bookmarked_private_table": create_test_tavern_table(
            all_users, bookmark=True, public=False
        ),
        "unbookmarked_private_table": create_test_tavern_table(
            all_users, bookmark=False, public=False
        ),
    }


def create_market_entries(number=1):
    """Create random group of markete entries submitted by anonymous users"""

    entries = [
        Market.objects.create(
            name=f"Seller #{i+1}",
            mail=f"seller{i}@example.com",
            # Escaping happens on (old version) text input, not here; test once this changes
            # text=SCRIPT_ALERT_INPUT,
            text=f"Seller Text #{i}",
            group=MARKET_SECTION_CHOICES[randint(0, len(MARKET_SECTION_CHOICES) - 1)][
                0
            ],
        )
        for i in range(0, number)
    ]

    return entries
