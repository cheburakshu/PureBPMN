import threading
import uuid
import ModelTarget
import logging
class ThreadInit(threading.Thread):
    def __init__(self,args=(),**kwargs):
#Setup log
        self.logger = logging.getLogger(__name__)

        threading.Thread.__init__(self)
        self._id =  uuid.uuid1().int
        self._modelId = kwargs.get('modelId')
        self._type = 'THREAD'
        self._args = args
        self._kwargs = kwargs
        #self._target = kwargs.get('target')
        self._target = ModelTarget.ModelTarget(*args,**kwargs).getTarget()
        self._semaphore = kwargs.get('semaphore')
        return
    
    def run(self):
        if (self._semaphore):
            with self._semaphore:
                self._target(*self._args, **self._kwargs)
        else:
            self._target(*self._args, **self._kwargs)
        return

    def getId(self):
        return self._id

    def getType(self):
        return self._type

    #def getObj(self):
    #    return self._obj

    def getModelId(self):
        return self._modelId

    #def getObjById(self,*args,**kwargs):
    #    lock = threading.RLock()
    #    with lock:
    #        if (self.getId() == kwargs['id']):
    #            return self.getObj() 
    #        else:
    #            return  

class ThreadIO(threading.Thread):
    def __init__(self,*args,**kwargs):
#Setup log
        self.logger = logging.getLogger(__name__)

        super(ThreadIO,self).__init__()
        self._id =  uuid.uuid1().int
        self._modelId = kwargs.get('modelId')
        self._thread_count = int(kwargs.get('thread_count'))
        self._threads = []
        self._threadInstance = None
        self._subRefs = {}
        self.addThread(*args,**kwargs)
        self.setSubRefs()

# Thread without lock
    def addThread(self,*args,**kwargs):
        if (self._thread_count):
            for i in range(self._thread_count):
                self._threadInstance = ThreadInit(*args,**kwargs)
                self._threadInstance.setDaemon(True)
                #self.getThreadInstance().start()
                #self.setSubRefs()
                self._threads.append(ThreadInit(*args,**kwargs))
        else:
            self._threadInstance = ThreadInit(*args,**kwargs)
            #self.setSubRefs()
            self._threads.append(ThreadInit(*args,**kwargs))

#Thread with lock impl.
#    def addThread(self,*args,**kwargs):
#        lock = threading.RLock()
#        with lock:
#           if (self._thread_count):
#               for i in range(self._thread_count):
#                   self._threadInstance = ThreadInit(*args,**kwargs)
#                   self._threadInstance.setDaemon(True)
#                   #self.getThreadInstance().start()
#                   #self.setSubRefs()
#                   self._threads.append(ThreadInit(*args,**kwargs)) 
#           else:
#               self._threadInstance = ThreadInit(*args,**kwargs)
#               #self.setSubRefs()
#               self._threads.append(ThreadInit(*args,**kwargs))

    def getId(self):
        return self._id

    def getThreads(self):
        return self._threads

    def getModelId(self):
        return self._modelId

    def getSubRefs(self):
        return self._subRefs

    def getThreadInstance(self):
        return self._threadInstance

    def setSubRefs(self):
        self._subRefs ['id'] = list(map(lambda x:x.getId(),self.getThreads())) 
