import logging
import re
log = logging.getLogger(__name__)



def Mongo(event):
    settings = event.request.registry.settings
    db = settings['db_conn'][settings['db_name']]   
    event.request.db = db

def mongo_cursor_to_dict(cursor):
    children = {}
    for doc in cursor:
         children[doc['__name__']] = doc['_id'] 
    return children


class Root(object):
    __name__ = None
    __parent__ = None
    def __init__(self, request):
        self.request = request 
        self.names = {} 
        self.cursor = request.db.company.find({}, {'__name__':1})
        self.names = mongo_cursor_to_dict(self.cursor)
        log.debug(self.names)
    def __getitem__(self, key):
        if self.names[key]:
            doc = self.request.db.company.find_one({'__name__':key})
            company = Company(doc)
            company.__parent__ = self
            return company
        else: 
            return self.names
            #raise KeyError(key) 
            
    
class Company(object):
    def __init__(self, data): 
        self.title = data['title'] 
        self.__name__ = self.slugify(data['title']) 
        self.slug = self.slugify(data['title']) 
        self.analysis = data['analysis']
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
        name = name.strip('-') 
        return name	


def get_root(request):
    return Root(request)
