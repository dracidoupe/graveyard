from ddcz.models import Author, CommonArticle, UserProfile


def get_valid_article_chain():

    user = UserProfile(nick_uzivatele="Author", email_uzivatele="test@example.com")

    author = Author(id=1, user=user, author_type=Author.USER_TYPE)

    article = CommonArticle(
        author=author,
        jmeno="Test Article",
        autor=user.nick_uzivatele,
        autmail=user.email_uzivatele,
        schvaleno=CommonArticle.CREATION_APPROVED,
        rubrika="clanky",
    )

    return {
        "user": user,
        "author": author,
        "article": article,
    }


def get_alphabetic_user_profiles(number_of_users=1, saved=False):
    if number_of_users > 26:
        raise NotImplementedError("Out of alphabet, reimplement this function")

    alphabet_letters = map(chr, range(97, 97 + number_of_users))
    profiles = []
    for letter in alphabet_letters:
        profile = UserProfile(
            nick_uzivatele=letter, email_uzivatele=f"{letter}@example.com"
        )
        profiles.append(profile)
        if saved:
            profile.save()

    return profiles
