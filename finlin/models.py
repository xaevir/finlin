from pyramid.threadlocal import get_current_request 
import logging
from pprint import pprint
import re
import datetime
import cryptacular.bcrypt
from pymongo.objectid import ObjectId
log = logging.getLogger(__name__)
from bson.code import Code


def get_db():
    req =  get_current_request()
    return req.db 
 
def slugify(name):
    filter = { 
        '&+' : 'and', # replace & with 'and'              
        '[^a-zA-Z0-9]+' : '_', # non-alphanumeric characters with a hyphen
        '-+' : '_' # replace multiple hyphens with a single hyphen
    }
    for k, v in filter.items():
        name = re.sub(k, v, name)
    name = name.strip('_') 
    return name	



class Root(object):
    __name__ = None
    __parent__ = None
    def __init__(self, request):
        self.db = request.db 
    def __getitem__(self, key):
        if key == 'user':
            return UserContainer(parent=self, name='user', db=self.db )
        doc = self.db.company.find_one({'slug':key})
        if doc is None:
            raise KeyError
        return Company(doc, self)             

    def items(self):
        result = {}
        for obj in self.db.company.find():
            obj['__parent__']= self
            result[obj['slug']] = obj
        return result


def get_root(request):
    root = Root(request)
    return root 

class Company(dict):
    def __init__ (self, data, parent=None):
        self['_id']      = data.get('_id', ObjectId()) 
        self['name']     = data['name']
        self['slug']     = slugify(self['name'])
        self['analysis'] = data['analysis'] 
        self['created']  = data.get('created', datetime.datetime.now()) 

        self.__name__    = self['slug']
        self.__parent__  = parent 

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



