import logging
from pprint import pprint
import re
import datetime

import cryptacular.bcrypt

from zope.interface import implements
from zope.interface import Interface

log = logging.getLogger(__name__)



def Mongo(event):
    settings = event.request.registry.settings
    db = settings['db_conn'][settings['db_name']]   
    event.request.db = db

class Root(dict):
    __name__ = None
    __parent__ = None
    def __init__(self, request):
        self.request = request 
    def __getitem__(self, key):
        if key == 'user':
            return UserContainer('user', self)
        doc = self.request.db.company.find_one({'__name__':key})
        if doc is None:
            raise KeyError
        
        company = Company(doc)
        company.__parent__ = self
        company.__name__ = key
        return company

def to_dict(cursor):
    children = {}
    for doc in cursor:
         children[doc.get('__name__')] = doc.get('_id') 
    return children

def get_root(request):
    root = Root(request)
    root.children['user'] = True   
    return root 


class Company(object):
    def __init__(self, data): 
        self.name = data.get('name', None)
        self.analysis = data['analysis']
        try: 
            self.__name__ = data['__name__']
        except:
            self.__name__ = self.slugify(data['name'])
    def slugify(self, name):
        filter = { 
    		#// replace & with 'and' for readability
    		'&+' : 'and',
            # replace non-alphanumeric characters with a hyphen 
            '[^a-zA-Z0-9]+' : '_',
            # replace multiple hyphens with a single hyphen
            '-+' : '_'
        }
        for k, v in filter.items():
            name = re.sub(k, v, name)
        name = name.strip('_') 
        return name	


class UserFolder(object):
    __name__ = 'user'
    def __init__(self, parent): 
        self.__parent__ = parent
        self.request = parent.request
    def __getitem__(self, key):
        doc = self.request.db.user.find_one({'username':key})
        if doc is None:
            raise KeyError
        user = User()
        for k, v in doc.items():
            setattr(user, k, v)
        user.__parent__ = self
        user.__name__ = key
        return user

class User(object):
    def __init__(self, doc): 
        self.username= doc.get('username', None)        
        self.groups = doc.get('groups', ['commentors'])
        self.date_created = datetime.datetime.now
        if doc.get('password'):
            bcrypt = cryptacular.bcrypt.BCRYPTPasswordManager()
            self.password = bcrypt.encode(doc.get('password'))

