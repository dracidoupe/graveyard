from django.contrib.auth.models import User
from ddcz.models import Author, CommonArticle, UserProfile

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
    number_of_users=1, saved=False, with_corresponding_user=False
):
    if number_of_users > 26:
        raise NotImplementedError("Out of alphabet, reimplement this function")

    alphabet_letters = map(chr, range(97, 97 + number_of_users))
    profiles = []
    for letter in alphabet_letters:
        email = f"{letter}@example.com"
        if with_corresponding_user:
            user = User(username=letter, email=email)
            user.set_password(email)

        profile = UserProfile(nick=letter, email=email)
        profiles.append(profile)

        if saved:
            if with_corresponding_user:
                user.save()
                profile.user = user
            profile.save()

    return profiles


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
