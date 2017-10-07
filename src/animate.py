# Raise, Undeads!

import configparser
import json
import logging
import os

import pymysql
import pymysql.cursors


import falcon
from falcon import HTTP_200
from falcon_cors import CORS

# '../config/raise.cfg'
config_file = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'config', 'raise.cfg'))
config = configparser.ConfigParser()
USE_CONFIG = False

if os.path.exists(config_file):
    USE_CONFIG = True
    config.read(config_file)

def get_config_value(section, option, default_value):
    if USE_CONFIG and config.has_section(section) and config.has_option(section, option):
        return config.get(section, option)
    else:
        return default_value


def getConnection():
    return pymysql.connect(host=get_config_value('db', 'host', 'localhost'),
                             user=get_config_value('db', 'user', 'ddcz_test'),
                             password=get_config_value('db', 'password', 'xxx'),
                             db=get_config_value('db', 'database_name', 'dracidoupe_cz'),
                             charset=get_config_value('db', 'charset', 'latin2'),
                             cursorclass=pymysql.cursors.DictCursor
                          )

if os.environ.has_key('ENVIRONMENT') and os.environ['ENVIRONMENT'] == 'production':
    fext_source = ['https://nove.dracidoupe.cz', 'https://www.dracidoupe.cz']
else:
    fext_source = ['http://localhost:8000']

cors = CORS(allow_origins_list=fext_source)

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
