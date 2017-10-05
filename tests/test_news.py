from falcon import testing
import pytest

import json

import animate


# Depending on your testing strategy and how your application
# manages state, you may be able to broaden the fixture scope
# beyond the default 'function' scope used in this example.
@pytest.fixture()
def client():
    # Assume the hypothetical `myapp` package has a function called
    # `create()` to initialize and return a `falcon.API` instance.
    return testing.TestClient(animate.create())


def test_get_message(client):
    doc = {
        "name": "Aktuality",
        "_links": {"self": { "href": "/aktuality/" }},
        "items": [
            {
                "date": "2017-01-02 02:02:02",
                "title": "Example News",
                "text": "Text of news (tm)",
                "author": {
                    "nick": "Unknown/N",
                    "_url": "/uzivatele/123/"
                }
            },
            {
                "date": "2017-01-01 01:01:01",
                "title": "Example News 2",
                "text": "Text of news (tm), but longer",
                "author": {
                    "nick": "Unknown/N",
                    "_url": "/uzivatele/123/"
                }
            }
        ]
    }
    result = client.simulate_get('/aktuality/')
    assert result.json == doc
