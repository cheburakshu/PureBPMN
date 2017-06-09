import Configparser
import copy
from functools import lru_cache

@lru_cache(maxsize=2048)
class ModelConfig(object):
    @lru_cache(maxsize=2048)
    def __init__(self,fileName): #*args,**kwargs):
        self._configs = Configparser.Configparser(fileName) #kwargs['filename'])
        self._models = self._configs.getConfigElement('model','keys').split(sep=',')
        self._key = {}
        self._val = {}
        self._inputPorts = {}
        self.loadSection().setInputPorts()

    @lru_cache(maxsize=2048)
    def loadSection(self):
        for kv in self._models:
            for i in (self._configs.getConfigSection('model_' + kv)):
                self._val [i[0]] = i[1]
            self._key [kv] = copy.deepcopy(self._val)
        return self

    @lru_cache(maxsize=2048)
    def getModels(self):
        return list(filter(lambda x:x != 'connection',self._models))

    @lru_cache(maxsize=2048)
    def getConnection(self):
        return list(filter(lambda x:x != 'connection',self._models))

    @lru_cache(maxsize=2048)
    def getModelAttributes(self,model):
        return self._key [model]

    @lru_cache(maxsize=2048)
    def getModelInputPorts(self,model):
        return self.getInputPorts().get(model)
    
    @lru_cache(maxsize=2048)
    def getInputPorts(self):
        return self._inputPorts
    
    @lru_cache(maxsize=2048)
    def setInputPorts(self):
        for model,property in self._key.items():
            for port in list(filter(lambda x:x != '',property['OnSuccess'].split(',') + property['OnFailure'].split(','))):
                if (not self._inputPorts.get(port)):
                    self._inputPorts [port] = [model]
                else:
                    self._inputPorts [port] = self._inputPorts.get(port) + [model]

#mc=ModelConfig('models.conf')
#mc.loadSection()
#print(mc.getConnection())
#mc.setInputPorts()
#print(mc.getModelInputPorts('print'))
#mc.loadSection.cache_info()
#print(mc.getSection('input'))
#print(mc.getSection.cache_info())
#mc.loadSection()
#print(mc.loadSection.cache_info())
#print(mc.getSection('input'))
#print(mc.getSection.cache_info())
#mc.loadSection()
#print(mc.loadSection.cache_info())
#print(mc.getSection('input'))
#print(mc.getSection.cache_info())
