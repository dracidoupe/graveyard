# Raise, Undeads!

import json
import logging

import pymysql
import pymysql.cursors


import falcon
from falcon import HTTP_200
from falcon_cors import CORS


def getConnection():
    return pymysql.connect(host='localhost',
                             user='ddcz_test',
                             password='xxx',
                             db='dracidoupe_cz',
                             charset='latin2',
                             cursorclass=pymysql.cursors.DictCursor)

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
        items = []

        conn = getConnection()
        try:
            with conn.cursor() as cursor:
                # TODO: marker, limit
                sql = "SELECT id, datum, autor, autmail, text FROM aktuality ORDER BY datum DESC LIMIT 10"
                cursor.execute(sql)

                for row in cursor.fetchall():
                    items.append({
                        u"id": row["id"],
                        u"date": row["datum"].isoformat(),
                        u"text": row["text"],
                        u"author": {
                            u"nick": row["autor"],
                            u"_url": u"/uzivatele/%s" % row["autor"]
                        }
                    })

                return items
        finally:
            conn.close()

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
            items = self.db.get_news(marker, limit)
            resp.body = json.dumps({
                u"name": "Aktuality",
                u"_links": {u"self": { u"href": u"/aktuality/" }},
                u"items": items
            }
        )
        except Exception as ex:
            self.logger.error(ex)

            description = ('Aliens have attacked our base! We will '
                           'be back as soon as we fight them off. '
                           'We appreciate your patience.')

            raise falcon.HTTPServiceUnavailable(
                'Service Outage',
                description,
                30)

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
