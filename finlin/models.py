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


class TraversableEntity(object):
     def __init__(self, parent=None, name=None, db=None):
         self._db = db
         self.__parent__ = parent
         self.__name__ = name

     def __getitem__(self, key):
        log.debug('key: %s' % key )
        log.debu('key')
        doc = self._collection.find_one({'__name__':key})
        if doc is None:
            raise KeyError
        if isinstance(self, UserContainer):
            obj = User(exists=True)             
        for k, v in doc.items():
            setattr(obj, k, v)
        obj.__parent__ = self
        obj.__name__ = key
        return obj

     def items(self):
         result = []
         for obj in self._collection.find():
             obj.__parent__= self
             obj.__name__ = obj.__name__
             result.append((obj.__name__, obj))
         return result

     @property
     def _collection(self):
         db = self._db
         collection = db[self.__name__]
         return collection

class Root(object):
    __name__ = None
    __parent__ = None
    def __init__(self, request):
        self.db = request.db 
    def __getitem__(self, key):
        if key == 'user':
            return UserContainer(parent=self, name='user', db=self.db )
        doc = self.db.company.find_one({'__name__':key})
        if doc is None:
            raise KeyError
        company = Company(exists=True)             
        for k, v in doc.items():
            setattr(company, k, v)
        company.__parent__ = self
        return company

    def items(self):
        result = {}
        for obj in self.db.company.find():
            obj['__parent__']= self
            result[obj['__name__']] = obj
        return result



def get_root(request):
    root = Root(request)
    return root 



class UserContainer(TraversableEntity):
    pass

class Company(object):
    def __init__(self, data=None, exists=False): 
        if exists: return
        self.name = data['name'] 
        self.analysis = data['analysis']
        self.__name__ = property(slugify(data['__name__']))
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



class User(object):
    def __init__(self, data=None, exists=False):
        if exists: return
        self.username= data['username']        
        self.groups = ['commentors']
        self.created = datetime.datetime.now()
        self.password = property(data['password'])
    def password(self, unencoded):
        bcrypt = cryptacular.bcrypt.BCRYPTPasswordManager()
        return bcrypt.encode(unencoded)

