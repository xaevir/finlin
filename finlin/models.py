import logging
import re
log = logging.getLogger(__name__)



def Mongo(event):
    settings = event.request.registry.settings
    db = settings['db_conn'][settings['db_name']]   
    event.request.db = db

class Root(object):
    __name__ = None
    __parent__ = None
    def __init__(self, request):
        self.request = request 
    def __getitem__(self, key):
        log.debug('key is:' + key)
        doc = self.request.db.company.find_one({'__name__':key})
        if doc:
            company = Company(doc)
            company.__parent__ = self
            return company
        else: 
            raise KeyError(key) 
        
    
class Company(object):
    def __init__(self, data): 
        self.title = data['title'] 
        self.__name__ = self.slugify(data['title']) 
        self.slug = self.slugify(data['title']) 
        self.analysis = data['analysis']
    def slugify(self, name):
        filter = { 
            # replace non-alphanumeric characters with a hyphen 
            '[^a-zA-Z0-9]+' : '-',
            # replace multiple hyphens with a single hyphen
            '/-+/' : '-'
        }
        for k, v in filter.items():
            name = re.sub(k, v, name)
        name = name.strip('-') 
        return name	


def get_root(request):
    return Root(request)
