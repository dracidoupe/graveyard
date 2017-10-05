# Raise, Undeads!

import json
import logging

import falcon
from falcon import HTTP_200
from falcon_cors import CORS

cors = CORS(allow_origins_list=['http://localhost:8080'])

def getLogger(name):
    logger = logging.getLogger(name)
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
            '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger

class StorageEngine(object):

    def get_news(self, marker, limit):
        return ""

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

    def __init__(self, db):
        self.db = db
        self.logger = getLogger('graveyard.' + __name__)

    def on_get(self, req, resp):
        """ Return last page of News """
        marker = req.get_param('marker') or ''
        limit = req.get_param_as_int('limit') or 50

        try:
            result = self.db.get_things(marker, limit)
        except Exception as ex:
            self.logger.error(ex)

            description = ('Aliens have attacked our base! We will '
                           'be back as soon as we fight them off. '
                           'We appreciate your patience.')

            raise falcon.HTTPServiceUnavailable(
                'Service Outage',
                description,
                30)
        else:
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

def create():
    app = falcon.API(middleware=[
        cors.middleware,
        RequireJSON()
    ])

    db = StorageEngine()

    news = NewsResource(db)

    app.add_route('/aktuality/', news)
    return app


app = create()
