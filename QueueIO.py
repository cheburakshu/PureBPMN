import queue
import uuid
import threading
class QueueInit(queue.Queue):
    def __init__(self,*args,**kwargs):
        self._id =  uuid.uuid1().int
        self._modelId = kwargs.get('modelId')
        self._type = 'QUEUE'
        self._obj = queue.Queue()

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
            if ([self.getId()] == kwargs['id']):
                return self.getObj()
            else:
                return

class QueueIO(queue.Queue):
    def __init__(self,*args,**kwargs):
        self._id =  uuid.uuid1().int
        self._modelId = kwargs.get('modelId')

# Main Q dictionary object.
        self._q = {}

# Init queues.
        self._q ['In'] = {}
        self._q ['Out'] = {}
        self._q ['Err'] = {}
        self._q ['OnSuccess'] = {}
        self._q ['OnFailure'] = {}

        if (kwargs.get('type') == 'connection'):
            for i in kwargs.get('connectionObject').values():
                self._q.update(i)
        else:
            if(kwargs.get('ports')):
                portQ = {}
                for port in kwargs.get('ports'):
                    portQ [port] = list(QueueInit(*args,**kwargs) for _ in range(int(kwargs.get('queue_count'))))
                self._q['In'] = {kwargs.get('modelName'):portQ}
            #if (kwargs.get('type') != 'sink'):
            self._q['Out'].update(dict({kwargs.get('modelName'):dict({kwargs.get('modelName'):list(QueueInit(*args,**kwargs) for _ in range(int(kwargs.get('queue_count'))))})}))
        self._q['Err'].update(dict({kwargs.get('modelName'):dict({'Err':list(QueueInit(*args,**kwargs) for _ in range(int(kwargs.get('queue_count'))))})}))

# Init subRefs.
        self._subRefs = {}
        self._subRefs ['In'] = {}
        self._subRefs ['Out'] = {}
        self._subRefs ['Err'] = {}
        self._subRefs ['OnSuccess'] = {}
        self._subRefs ['OnFailure'] = {}

        self.setSubRefs()

    def getId(self):
        return self._id

    def getModelId(self):
        return self._modelId
   
    def filter(self,qObject,criteria):
        return {k:v for k,v in qObject.items() if k == criteria}

    def getQ(self,model=None,port=None):
        if port and model:
            return self.filter(self.filter(self._q,model),port)
        else:
            return self._q

    def getQIn(self,model=None,port=None):
        if port and model:
            return {model:self.filter(self._q['In'].get(model),port)}
        else:
            return self._q['In']

    def getQOut(self,model=None,port=None):
        if port and model:
            return {model:self.filter(self._q['Out'].get(model),port)}
        else:
            return self._q['Out']

    def getQErr(self,port=None):
        if port and model:
            return {model:self.filter(self._q['Err'].get(model),port)}
        else:
            return self._q['Err']

    def getQOnSuccess(self,port=None):
        if port and model:
            return {model:self.filter(self._q['OnSuccess'].get(model),port)}
        else:
            return self._q['OnSuccess']

    def getQOnFailure(self,port=None):
        if port and model:
            return {model:self.filter(self._q['OnFailure'].get(model),port)}
        else:
            return self._q['OnFailure']

    def setSubRefs(self):
        for qType,_modelPortQueues in self.getQ().items():
            modelPortQ = {}
            for _model,_portQueues in _modelPortQueues.items():
            #for qType,_portQueues in self.getQ().items():
                portQ = {}
                for _port,_queues in _portQueues.items():
                    portQ [_port] = list(map(lambda x:x.getId(),_queues))
                modelPortQ [_model] = portQ
            self._subRefs [qType] = modelPortQ

    def getSubRefs(self):
        return self._subRefs
