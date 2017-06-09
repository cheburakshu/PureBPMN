from pprint import pprint
from ModelConfig import ModelConfig
from functools import lru_cache
import copy
import logging

@lru_cache(maxsize=2048)
class ModelManager(object):
    def __init__(self,*args,**kwargs):
#Setup log
        self.logger = logging.getLogger(__name__)

        self._modelRefs = {}
        self._models = {}
        self._q = {}
        self._qConnection = {}
        self._qConnections = []
        self._qOut = []
        self._qSuccessFailure = {}

    def getModelRefs(self,*args,**kwargs):
        return self._modelRefs

    def getModels(self,*args,**kwargs):
        return self._models
  
    def getModelNames(self,*args,**kwargs):
        return list(self.getModels().keys())

    def setModelRefs(self,*args,**kwargs):
        self._modelRefs [kwargs['modelName']] = kwargs['objRefs']

    def setModels(self,*args,**kwargs):
        self._models [kwargs['modelName']] = kwargs['model']

    def getModel(self,*args,**kwargs):
        return self.getModels(*args,**kwargs)[kwargs['modelName']]

    def getModelRef(self,*args,**kwargs):
        return self.getModelRefs(*args,**kwargs)[kwargs['modelName']]

    def getSubRefId(self,*args,**kwargs):
        return self.getModelRef(*args,**kwargs)[kwargs['objectType']]['subref'][kwargs['subId']]

    def setConnectionRefs(self,*args,**kwargs):
        self.getModelRef(modelName=list(kwargs['connectionObject'].keys())[0]).update(kwargs['modelRefs'])

    def setConnectionModels(self,*args,**kwargs):
        self.getModels().update({(list(kwargs['connectionObject'].keys())[0],'connection'):kwargs['model']})

    def getObject(self,*args,**kwargs):
        if (kwargs.get('objectType') == 'queue'):
            return self.getModel(*args,**kwargs).getQ()
        elif (kwargs.get('objectType') == 'thread'):
            return self.getModel(*args,**kwargs).getThread()
        elif (kwargs.get('objectType') == 'semaphore'):
            return self.getModel(*args,**kwargs).getSemaphore()
        elif (kwargs.get('objectType') == 'event'):
            return self.getModel(*args,**kwargs).getEvent()
        elif (kwargs.get('objectType') == 'subscribe'):
            return self.getModel(*args,**kwargs).getSubscribe()

    def getModelThreads(self):
        _threads = []
        for modelName in self.getModelNames():
            _threads.append((modelName,self.getObject(modelName=modelName,objectType='thread').getThreads()))
            #_threads.append(self.getModel(modelName=(modelName,'connection')).getThread().getThreads())
        return _threads

    def getConnectionQueues(self,*args,**kwargs):
        self._qOut = {}
        for model in self.getModelRef(*args,**kwargs)[kwargs['successFailure']]:
            if model:
                self._qOut.update(self.getObject(modelName=model,objectType='queue').getQIn(model,kwargs.get('modelName')))

    def getModelConnections(self,*args,**kwargs):
        for modelName in self.getModelNames():
            self._qSuccessFailure = {}
            self._qConnection = {}
            if (self.getModelRef(modelName=modelName)['model_type'] == 'sink'):
                continue
            self._q ['In'] = self.getObject(modelName=modelName,objectType='queue').getQOut() 
            for i in ['OnSuccess','OnFailure']:
                self.getConnectionQueues(modelName=modelName,successFailure=i) 
                self._q [i] = copy.copy(self._qOut)
            self._qConnection [modelName] = copy.copy(self._q)
            self._qConnections.append(copy.copy(self._qConnection))
        return self._qConnections
