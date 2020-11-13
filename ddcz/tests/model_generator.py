from ddcz.models import Author, CommonArticle, UserProfile


def get_valid_article_chain():

    user = UserProfile(
        nick_uzivatele = 'Author',
        email_uzivatele = 'test@example.com'
    )

    author = Author(
        id = 1,
        user = user,
        author_type = Author.USER_TYPE
    )

    article = CommonArticle(
        author = author,
        jmeno = 'Test Article',
        autor = user.nick_uzivatele,
        autmail = user.email_uzivatele,
        schvaleno = CommonArticle.CREATION_APPROVED,
        rubrika = 'clanky'
    )

    return {
        'user': user,
        'author': author,
        'article': article,
    }