import logging


logger = logging.getLogger(__name__)


def log_wrong_legacy_route(url):
    logger.warning(
        f"There has been submitted URL address from the old website: index.php >> No redirect could be found for a legacy URL {url}"
    )
