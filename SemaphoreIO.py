import threading
import uuid
import logging

class SemaphoreInit(threading.Semaphore):
    def __init__(self,*args,**kwargs):
#Setup log
        self.logger = logging.getLogger(__name__)

        self._id =  uuid.uuid1().int
        self._modelId = kwargs.get('modelId')
        self._type = 'SEMAPHORE'
        self._limit = int(kwargs.get('thread_pool_max'))
        self._lowLoadSema = kwargs.get('lowLoadSema')
        if (self._lowLoadSema):
            self._obj = threading.Semaphore(1)
        elif (self._limit):
            self._obj = threading.Semaphore(self._limit)
        else:
            self._obj = threading.Semaphore(999)
        return

    def getId(self):
        return self._id

    def getType(self):
        return self._type

    def getObj(self):
        return self._obj

    def getModelId(self):
        return self._modelId

    def getObjById(self,*args,**kwargs):
        lock = threading.RLock()
        with lock:
            if (self.getId() == kwargs[id]):
                return self.getObj()
            else:
                return

class SemaphoreIO(threading.Semaphore):
    def __init__(self,*args,**kwargs):
#Setup log
        self.logger = logging.getLogger(__name__)

        self._id =  uuid.uuid1().int
        self._modelId = kwargs.get('modelId')
        self._semaphore = SemaphoreInit(*args,**kwargs)
        self._subRefs = {}
        self.setSubRefs()

    def getId(self):
        return self._id

    def getSemaphore(self):
        return self._semaphore

    def getModelId(self):
        return self._modelId

    def getSubRefs(self):
        return self._subRefs

    def setSubRefs(self):
        self._subRefs ['id'] = self.getSemaphore().getId()


#s=SemaphoreIO(2)
#print(s)
