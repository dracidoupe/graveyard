import logging

from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration

# Parts of header and query parameter names that identify the visitor
VISITOR_IDENTITY_TERMS = ["forwarded", "-ip", "remote-", "via", "-user"]


def get_sentry_options():
    return {
        "integrations": [
            DjangoIntegration(),
            # Not enabled by default since sentry-sdk 3. Logged errors are reported
            # as issues, log lines themselves are not shipped
            LoggingIntegration(event_level=logging.ERROR, level=None),
        ],
        # Keeps logged errors free of stack frames and their local variables
        "attach_stacktrace": False,
        # sentry-sdk 3 collects everything unless told otherwise and no longer
        # scrubs request bodies, which here include passwords from the login form
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
