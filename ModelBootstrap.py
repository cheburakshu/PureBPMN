import copy
from ModelIO import ModelIO
from ModelConfig import ModelConfig
from pprint import pprint
from ModelManager import ModelManager
import ModelCreate
import logSetup
import logging
import asyncio
import threading

class ModelBootstrap(object):
    def __init__(self,*args,**kwargs):
# Setup log configurations
        logSetup.logSetup()
        self.logger = logging.getLogger(__name__)

        self._ModelConfig = ModelConfig(kwargs.get('filename'))
        self._modelNames = self._ModelConfig.getModels()
        self._ModelCreate = ModelCreate.ModelCreate(*args,**kwargs)
        self._modelInit = threading.Event()
        self.createModels(*args,**kwargs)
        self._ModelManager = ModelManager()
        self.createConnections(*args,**kwargs)
        self.startThreads()

    def createModels(self,*args,**kwargs):
        for modelName in self._modelNames:
            self._ModelCreate.create(modelName=modelName,model_init_event=self._modelInit,*args,**kwargs)
 
    def createConnections(self,*args,**kwargs):
        for _connection in self._ModelManager.getModelConnections():
            self._ModelCreate.create(modelName='connection',connectionObject=_connection,model_init_event=self._modelInit,*args,**kwargs)

    async def startParallelThreads(self,_thread,modelName):
        _thread.setDaemon(True)
        _thread.start()
        if _thread.isDaemon():
            self.logger.debug('Model - %s, Started daemon thread - %s', modelName, _thread.getName())
        else:
            self.logger.debug('Model - %s, Started non-daemon thread - %s', modelName, _thread.getName())

 
    def startThreads(self,*args,**kwargs):
        self.logger.info('Starting Threads')
        tasks = []
        for modelName, _threads in self._ModelManager.getModelThreads():
            for _thread in _threads:
                loop = asyncio.get_event_loop()
                tasks.append(asyncio.ensure_future(self.startParallelThreads(_thread,modelName),loop=loop))
        loop.run_until_complete(asyncio.gather(*tasks,return_exceptions=False))
        #print('init ok')
        self._modelInit.set()
        self.logger.info('Started all Threads.')
