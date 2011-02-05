from pyramid.config import Configurator
from pyramid.events import subscriber
from pyramid.events import NewRequest
from finlin.models import get_root

from gridfs import GridFS
import pymongo


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    mongodb_uri = settings.get('mongodb_uri')
    if mongodb_uri is None:
        raise ValueError("No 'mongodb_uri' in application configuration.")

    conn = pymongo.Connection(mongodb_uri)
    config = Configurator(root_factory=get_root,settings=settings)

    config.registry.settings['db_conn'] = conn
    config.add_subscriber(add_mongo_db, NewRequest)

    config.add_static_view('static', 'finlin:static')
    config.scan('finlin')
    return config.make_wsgi_app()


def add_mongo_db(event):
    settings = event.request.registry.settings
    db = settings['db_conn'][settings['db_name']]
    event.request.db = db
    event.request.fs = GridFS(db)   
