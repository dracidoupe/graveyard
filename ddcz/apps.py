from django.apps import AppConfig


class DdczConfig(AppConfig):
    name = "ddcz"

    def ready(self):
        from django.db.models import fields

        # Hotfix for missing blank field
        fields.BLANK_CHOICE_LABEL = "- Vyberte možnost -"
