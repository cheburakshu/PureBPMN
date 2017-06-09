import threading
import uuid
class SubscribeInit(object):
    def __init__(self,*args,**kwargs):
        self._id =  uuid.uuid1().int
        self._modelId = kwargs.get('modelId')
        self._type = 'SUBSCRIBE'
        self._obj = {}

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


class SubscribeIO(object):
    def __init__(self,*args,**kwargs):
        self._id =  uuid.uuid1().int
        self._modelId = kwargs.get('modelId')
        self._subscribe = SubscribeInit(*args,**kwargs)
        self._subRefs = {}
        self.setSubRefs()

    def getId(self):
        return self._id

    def getSubscribe(self):
        return self._subscribe

    def setSubscribe(self,event):
        rlock = threading.RLock()
        with rlock:
            self._subscribe = event

    def getModelId(self):
        return self._modelId

    def getSubRefs(self):
        return self._subRefs

    def setSubRefs(self):
        self._subRefs ['id'] = self.getSubscribe().getId()

