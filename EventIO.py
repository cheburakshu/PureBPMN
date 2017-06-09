import threading
import uuid
class EventInit(threading.Event):
    def __init__(self,*args,**kwargs):
        self._id =  uuid.uuid1().int
        self._modelId = kwargs.get('modelId')
        self._type = 'EVENT'
        self._obj = threading.Event()

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
            if (self.getId() == kwargs['id']):
                return self.getObj()
            else:
                return

class EventIO(threading.Event):
    def __init__(self,*args,**kwargs):
        self._id =  uuid.uuid1().int
        self._modelId = kwargs.get('modelId')
        self._event = EventInit(*args,**kwargs)
        self._subRefs = {}
        self.setSubRefs()

    def getId(self):
        return self._id

    def getEvent(self):
        return self._event

    def getModelId(self):
        return self._modelId

    def getSubRefs(self):
        return self._subRefs

    def setSubRefs(self):
        self._subRefs ['id'] = self.getEvent().getId()

