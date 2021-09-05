import os
import os.path
from datetime import datetime

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = """
    Write release data from environment variables. To be used only during deploy.
    """

    def handle(self, *args, **options):
        version = os.environ.get("HEROKU_RELEASE_VERSION", "dev")
        # If we are on proper heroku versioning, get integer version to be used for cache control
        version_int = int(version[1:]) if version.startswith("v") else 1
        hash = os.environ.get("HEROKU_SLUG_COMMIT", None)
        release_date = os.environ.get("HEROKU_RELEASE_CREATED_AT", None)
        if release_date:
            try:
                release_date = datetime.fromisoformat(release_date).strftime(
                    "%-d. %-m. %Y"
                )
            except ValueError:
                release_date = None

        local_settings = os.path.join(
            os.path.dirname(__file__),
            os.pardir,
            os.pardir,
            os.pardir,
            "graveyard",
            "settings",
            "local.py",
        )

        with open(local_settings, "a") as f:
            f.write(f'DEPLOY_VERSION = "{version}"\n')
            f.write(f"VERSION = {version_int}\n")
            if hash:
                f.write(f'DEPLOY_HASH = "{hash[0:7]}"\n')
            if release_date:
                f.write(f'DEPLOY_DATE = "{release_date}"\n')
