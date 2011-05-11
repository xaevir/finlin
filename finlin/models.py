from pyramid.threadlocal import get_current_request 
from pyramid.url import resource_url

import logging
from pprint import pprint
import re
import datetime
import cryptacular.bcrypt
from pymongo.objectid import ObjectId
log = logging.getLogger(__name__)
from bson.code import Code

from zope.interface import implements
from zope.interface import Interface


def get_db():
    req =  get_current_request()
    return req.db 
 


class Root(object):
    __name__ = None
    __parent__ = None
    def __init__(self, request):
        self.db = request.db 
        self.request = request
    def __getitem__(self, key):
        log.debug('Key is %s'% key)
        if key == 'user':
            return UserContainer(parent=self, name='user', db=self.db )
        doc = self.db.company.find_one({'slug':key})
        if doc is None:
            raise KeyError
        return Company(doc, key, self)             

    def items(self):
        result = {}
        for obj in self.db.company.find():
            obj['__parent__']= self
            result[obj['slug']] = obj
        return result


def get_root(request):
    root = Root(request)
    return root 


class Company(object):
    links = [('about', 'About'), 
             ('time_to_market', 'Time to Market'), 
             ('product', 'Product'),
             ('growth_strategy', 'Growth Strategy'),
             ('management',  'Managment')]

    def __init__(self, data, name, parent):
        self.__name__    = name
        self.__parent__  = parent 
        self.data        = data
        self.request     = parent.request
        self.nav         = self.create_nav() 
        #for k, v in data.items():
        #    setattr(self, k, v)



    def __getitem__(self, key):
        log.debug('Key is %s'% key)
        try:
            [x[0] for x in self.links].index(key)
        except ValueError:
            raise KeyError
        return CompanyPage(self.__data, key, self)

    def create_nav(self):
        nav = []
        for x,y in self.links:
            x =  resource_url(self, self.request, x)
            nav.append((x,y))
        nav.insert(0, (resource_url(self, self.request), 'Overview'))
        return nav

      
class CompanyPage(object):
    def __init__ (self, data, name, parent):
        self.__name__    = name
        self.__parent__  = parent 
        self.name        = data['name']
        self.page        = data.get(name, 'This section is empty')
        self.nav         = parent.nav

class CompanyData(dict):
    def get_comments(self):
        return get_db().comment.find({'company_id': self['_id']})

    def pretty_date(self, date):
        return date.strftime('%B %d, %Y')  

class Comment(dict):
    def __init__ (self, data, parent_context):
        self.__parent__   = parent_context
        self['_id']       = data.get('_id', ObjectId()) 
        self['body']      = data['body']
        self['created']   = data.get('created', datetime.datetime.now()) 
        self['company_id']  = parent_context['_id']
        self['username']  = data['username']
        self['path']     =  data.get('path', "")
        try:
            self['parent_id'] = data['parent_id']
            parent            = get_db().comment.find_one(
                                        {'parent_id': self['parent_id']})
            self['depth']     = parent['depth'] + 1
            self['path']      = parent['path'] + ":" + parent['_id']
        except KeyError: pass
            
    def save(self):
        get_db().comment.save(self)




class UserContainer(object):
    pass

class User(object):
    @staticmethod
    def set_password(unencoded):
        bcrypt = cryptacular.bcrypt.BCRYPTPasswordManager()
        return bcrypt.encode(unencoded)
    @staticmethod
    def check_password(encoded, password):
        bcrypt = cryptacular.bcrypt.BCRYPTPasswordManager()
        return bcrypt.check(encoded, password)



