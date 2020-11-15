from django.apps import apps
from django.core.management.base import BaseCommand, CommandError

from ddcz.models import (
    Author, CreativePage, UserProfile
)
from ddcz.text import misencode

class Command(BaseCommand):
    help = 'Denormalizes authors from legacy tables to Author table'

    def get_author(self, creation):
        if creation.autor:
            author_type = Author.USER_TYPE
            author_name = creation.autor.lower()
        else:
            author_type = Author.WEBSITE_TYPE
            author_name = creation.zdroj.lower()

        if (author_type, author_name) in self.authors:
            return self.authors[(author_type, author_name)]

        else:
            if author_type is Author.WEBSITE_TYPE:
                author = Author.objects.create(
                    website = creation.zdroj,
                    website_email = creation.zdrojmail,
                    author_type = author_type
                )
            else:
                # Shouldn't be needed in theory (tm)
                try:
                    profile = UserProfile.objects.get(nick_uzivatele=misencode(author_name))

                    try:
                        author = Author.objects.get(user=profile, author_type=author_type)
                    except Author.DoesNotExist:
                        author = Author.objects.create(
                            user = profile,
                            author_type = author_type
                        )

                except UserProfile.DoesNotExist as err:
                    author_type = Author.ANONYMOUS_USER_TYPE

                    author = Author.objects.create(
                        author_type = author_type,
                        anonymous_user_nick = creation.autor
                    )
                    

            self.authors[(author_type, author_name)] = author
            return author

    def handle(self, *args, **options):
        self.authors = {}

        for author in Author.objects.all():
            self.authors[(author.author_type, author.name.lower())] = author

        creation_models = []

        for page in CreativePage.objects.all():
            app, model_class_name = page.model_class.split('.')
            model_class = apps.get_model(app, model_class_name)
            creation_models.append(model_class)

        for creation_model in creation_models:
            for creation in creation_model.objects.all():
                if not creation.author:
                    creation.author = self.get_author(creation)
                    creation.save()
