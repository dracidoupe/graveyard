# Raise, Undeads!

import json

import falcon
from falcon import HTTP_200
from falcon_cors import CORS

cors = CORS(allow_origins_list=['http://localhost:8080'])

class RequireJSON(object):

    def process_request(self, req, resp):
        if not req.client_accepts_json:
            raise falcon.HTTPNotAcceptable(
                'This API only supports responses encoded as JSON.',
                href='http://docs.examples.com/api/json')

        if req.method in ('POST', 'PUT'):
            if 'application/json' not in req.content_type:
                raise falcon.HTTPUnsupportedMediaType(
                    'This API only supports requests encoded as JSON.',
                    href='http://docs.examples.com/api/json')



class NewsResource(object):
    def on_get(self, req, resp):
        """ Return last page of News """
        resp.body = json.dumps(json.loads("""
        {
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
        """))

app = falcon.API(middleware=[
    cors.middleware,
    RequireJSON()
])
news = NewsResource()

app.add_route('/aktuality/', news)
