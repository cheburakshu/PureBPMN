import configparser
import os
import sys
from functools import lru_cache
import codecs

class Configparser(object):
# PRIVATE METHODS...
    @lru_cache(maxsize=2048)
    def __init__(self,fileName):
        self._CONFIG_PATH = 'config/'
        self._cfgparser = configparser.SafeConfigParser()
        self._cfgparser.optionxform = str
        self.loadConfig(fileName)

    @lru_cache(maxsize=2048)
    def loadConfig(self,fileName):
        #self._cfgparser.readfp(open(self.getAbsPath(self._CONFIG_PATH + fileName)))
        self._cfgparser.readfp(codecs.open(self.getAbsPath(self._CONFIG_PATH + fileName),'r','utf-8'))

    @lru_cache(maxsize=2048)
    def getDirName(self):
        try:
            dirname = os.path.dirname(os.path.abspath(__file__))
        except NameError:
            dirname = os.path.dirname(os.path.abspath(sys.argv[0]))
        return dirname

    @lru_cache(maxsize=2048)
    def getAbsPath(self,fileName):
        return os.path.join(self.getDirName(),fileName)
    
    @lru_cache(maxsize=2048)
    def getConfig(self):
        return self._cfgparser
    
# PUBLIC METHODS FOLLOW...
    @lru_cache(maxsize=2048)
    def getConfigElement(self,section,key):
        return self.getConfig().get(section,key)

    @lru_cache(maxsize=2048)
    def getConfigSection(self,section):
        return self.getConfig().items(section)
#def main():
#c = Configparser('models.conf') 
#print(c.getConfigElement('model','keys'))
#print(c.getConfigSection('model_input'))
#print(c.getConfigSection.cache_info())
#print(c.getConfigSection('model_input'))
#print(c.getConfigSection.cache_info())
