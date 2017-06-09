import Configparser
import copy
from functools import lru_cache

@lru_cache(maxsize=2048)
class AppConfig(object):
    @lru_cache(maxsize=2048)
    def __init__(self,fileName):
        self._configs = Configparser.Configparser(fileName)
        self._apps = self._configs.getConfigElement('app','keys').split(sep=',')
        self._key = {}
        self._val = {}
        self.loadSection()

    @lru_cache(maxsize=2048)
    def loadSection(self):
        for kv in self._apps:
            for i in (self._configs.getConfigSection('app_' + kv)):
                self._val [i[0]] = i[1]
            self._key [kv] = copy.deepcopy(self._val)
        return self

    @lru_cache(maxsize=2048)
    def getApps(self):
        return list(filter(lambda x:x != 'connection',self._apps))

    @lru_cache(maxsize=2048)
    def getAppAttributes(self,app):
        return self._key [app]

#ac=AppConfig('apps.conf')
#print(ac.getAppAttributes('Top100').get('user'))
#print(mc.getAppInputPorts('print'))
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
