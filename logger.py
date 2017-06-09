import logging
import logging.config
import time
from functools import lru_cache

class logger(object):
    def __init__(self,*args,**kwargs):
        self._logger = None

    def logSetup(self):
        LOG_PATH = 'log/'
        fileName = LOG_PATH + 'runlog.' + str(int(time.time())) + '.out'
        logging.config.fileConfig('config/logging.conf',defaults={'logfilename': fileName})
        #self.setLogger()

    def setLogger(self,_name):
        self._logger = logging.getLogger(_name)

    def getLogger(self):
        return self._logger
       
    def debug(self,message):
        #LEVEL 10
        self.getLogger().debug(message)
    
    def info(self,message):
        #LEVEL 20
        self._logger.info(message)

    def warn(self,message):
        #LEVEL 30
        self._logger.warning(message)

    def error(self,message):
        #LEVEL 40
        self._logger.error(message)

    def critical(self,message):
        #LEVEL 50
        self._logger.critical(message)

#log=logger()
#log.logSetup()
#log.info('test')
#log.debug('testing')
#USAGE
#logSetup()
#getLogger()
#info('testing')
#debug('testing')
#warn('testing')
#error('testing')
#critical('testing')
