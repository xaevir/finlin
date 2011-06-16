from pyramid.threadlocal import get_current_request 
from pyramid.url import resource_url

from pyramid.renderers import render

import logging
from pprint import pprint
import re
import datetime
import cryptacular.bcrypt
from pymongo.objectid import ObjectId
from pymongo.errors import InvalidId

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
        self.request = request

    def __getitem__(self, key):
        log.debug('Key is %s'% key)
        if key == 'user':
            return UserContainer(parent=self, name='user', db=self.db )
        if key == 'cms':
            return Cms(key, self, self.request)
        doc = self.request.db.company.find_one({'slug':key})
        if doc is None:
            raise KeyError
        return Company(doc, key, self, self.request)             

    def items(self):
        result = {}
        for obj in self.request.db.company.find():
            obj['__parent__']= self
            result[obj['slug']] = obj
        return result


def get_root(request):
    root = Root(request)
    return root 


class Cms(object):
    def __init__(self, name, parent, request):
        self.__name__    = name
        self.__parent__  = parent 
        self.request     = request
        self.url         = resource_url(self, self.request) 
        self.request.nav = render('finlin:templates/cms/nav.pt', {'context': self}, self.request)

    def __getitem__(self, key):
        log.debug('Key of Cms is %s'% key)
        if key == 'questions':
            doc = self.request.db.questions.find()
            if doc is None:
                raise KeyError
            return QuestionsIndex(doc, key, self, self.request)


class QuestionsIndex(object):
    def __init__ (self, data, name, parent, request):
        self.__name__    = name
        self.__parent__  = parent 
        self.request     = request
        self.data        = data
        self.url         = resource_url(self, self.request) 

    def __getitem__(self, key):
        log.debug('Key of QuestionsIndex is %s'% key)
        try:
            id =  ObjectId(key)
        except InvalidId: #needs to be at least a number I suppose
            raise KeyError
        doc = self.request.db.questions.find_one({'_id': id})
        if doc is None:
            raise KeyError
        return Question(doc, key, self, self.request)


class Question(object):
    def __init__ (self, data, name, parent, request):
        self.__name__    = name
        self.__parent__  = parent 
        self.request     = parent.request
        self.data        = data
        self.url         = resource_url(self, self.request) 


class Company(object):
    resources = {'growth_strategy': True, 
                 'competitive_advantage': True,
                 'overview': True,
                 'questions': True,
                 }             

    def __init__(self, data, name, parent, request):
        self.__name__    = name
        self.__parent__  = parent 
        self.data        = data
        self.request     = request
        
    def __getitem__(self, key):
        log.debug('Key is %s'% key)
        self.resources[key]
        return CompanyPage(self.data, key, self, self.request)

      
class CompanyPage(object):
    def __init__ (self, data, name, parent, request):
        self.__name__    = name
        self.__parent__  = parent 
        self.data        = data
        self.request     = request
        self.page        = data.get(name, 'This section is empty')

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



