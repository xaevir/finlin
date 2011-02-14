import logging
from pprint import pprint
import re
import datetime
import cryptacular.bcrypt

log = logging.getLogger(__name__)


def Mongo(event):
    settings = event.request.registry.settings
    db = settings['db_conn'][settings['db_name']]   
    event.request.db = db


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
        return Company(doc, self)             

    def items(self):
        result = {}
        for obj in self.db.company.find():
            obj['__parent__']= self
            result[obj['__name__']] = obj
        return result


def get_root(request):
    root = Root(request)
    return root 

class Company(dict):
    def __init__ (self, data, parent=None):
        self['_id'] = data.get('_id', None) 
        self['name'] = data['name']
        self['analysis'] = data['analysis'] 
        self.__name__ = self['__name__'] = self.slugify(self['name'])
        self['created'] = data.get('created', 
                                    datetime.datetime.now()) 
        self.__parent__ = parent 

    def slugify(self, name):
        filter = { 
            '&+' : 'and', # replace & with 'and'              
            '[^a-zA-Z0-9]+' : '_', # non-alphanumeric characters with a hyphen
            '-+' : '_' # replace multiple hyphens with a single hyphen
        }
        for k, v in filter.items():
            name = re.sub(k, v, name)
        name = name.strip('_') 
        return name	

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
