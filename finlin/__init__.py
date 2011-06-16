from pyramid.config import Configurator
from pyramid.events import subscriber
from pyramid.events import NewRequest
from pyramid.session import UnencryptedCookieSessionFactoryConfig
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.renderers import get_renderer

from finlin.security import groupfinder
from finlin.models import get_root

import logging

from gridfs import GridFS
import pymongo

from pyramid.url import resource_url

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """

    authn_policy = AuthTktAuthenticationPolicy(secret='batman',
                                               callback=groupfinder)
    authz_policy = ACLAuthorizationPolicy()


    mongodb_uri = settings.get('mongodb_uri')
    if mongodb_uri is None:
        raise ValueError("No 'mongodb_uri' in application configuration.")

    my_session_factory = UnencryptedCookieSessionFactoryConfig('batman')
    conn = pymongo.Connection(mongodb_uri)
    config = Configurator(root_factory=get_root,
                          settings=settings,
                          session_factory = my_session_factory,
                          authentication_policy=authn_policy,
                          authorization_policy=authz_policy,
                          renderer_globals_factory=renderer_globals_factory

                          )

    config.registry.settings['db_conn'] = conn
    config.add_subscriber(add_mongo_db, NewRequest)

    config.add_static_view('static', 'finlin:static')
    config.scan('finlin')
    return config.make_wsgi_app()

def renderer_globals_factory(system):
    return {'main': get_renderer('finlin:templates/master.pt').implementation(),
            'resource_url' : resource_url  
    }

def add_mongo_db(event):
    settings = event.request.registry.settings
    db = settings['db_conn'][settings['db_name']]
    event.request.db = db
    event.request.fs = GridFS(db)   
