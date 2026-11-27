import logging

from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration

VISITOR_IDENTITY_TERMS = ["forwarded", "-ip", "remote-", "via", "-user"]


def get_sentry_options():
    return {
        "integrations": [
            DjangoIntegration(),
            LoggingIntegration(event_level=logging.ERROR, level=None),
        ],
        "data_collection": {
            "user_info": False,
            "http_bodies": [],
            "cookies": {"mode": "off"},
            "database_query_data": False,
            "http_headers": {
                "request": {"mode": "denylist", "terms": VISITOR_IDENTITY_TERMS},
            },
            "url_query_params": {"mode": "denylist", "terms": VISITOR_IDENTITY_TERMS},
            "stack_frame_variables": {"mode": "denylist"},
        },
    }
