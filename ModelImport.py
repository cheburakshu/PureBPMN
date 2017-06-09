from functools import lru_cache
import importlib
@lru_cache(maxsize=2048)
class ModelImport(object):
    def __init__(self,*args,**kwargs):
        pass
    def importModule(self,_module):
        return importlib.import_module(_module)    
