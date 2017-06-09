import sys
import threading
import asyncio
import random
import importlib
import copy
import uuid
import collections
import time
import queue
from queue import Empty
from functools import lru_cache
import logging
import ModelImport
class ModelTarget(object):
    def __init__(self,*args,**kwargs):
#Setup log
        self.logger = logging.getLogger(__name__)

        super(ModelTarget,self).__init__()
        self._id =  uuid.uuid1().int
        self._modelId = kwargs.get('modelId')
        self._type = 'MODELTARGET'
        self._moduleName = kwargs.get('module')
        self._className = kwargs.get('class')
        self._methodName = kwargs.get('method')
        self._modelType = kwargs.get('type')
        self._input_ports = kwargs.get('input_ports')
# Transparent delays
        self._delay = kwargs.get('delay')
        self._args = args
        self._kwargs = kwargs

        self._qIn = kwargs.get('q').getQIn() 
        self._qOut = kwargs.get('q').getQOut()
        self._qErr = kwargs.get('q').getQErr()
        self._qOnSuccess = kwargs.get('q').getQOnSuccess()
        self._qOnFailure = kwargs.get('q').getQOnFailure()

        #self._module = self.importModule() 
        #self._module = ModelImport.ModelImport().importModule(self._moduleName)
        self._module = kwargs.get('moduleObj') ###ModelImport.ModelImport().importModule(self._moduleName)
        self._modelInit = kwargs.get('model_init_event')

#Low load impl
        self._lowLoadSema = kwargs.get('lowLoadSema')
        self._threadCount = int(kwargs.get('thread_count'))
        self._lowLoad = False

#Without lock
        #self.lock = threading.RLock()
        #self._loop = asyncio.get_event_loop()
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)

    #@lru_cache(maxsize=2048)
    #def importModule(self):
    #    return importlib.import_module(self._moduleName)

    def getRandomQs(self,qIO,method,filterEmpty=True,getAll=False):
        _queue=[]
        for model,ports in qIO.items():
            _model = model
            if (_queue and method == 'any'): break
            for port,queueInit in ports.items():
                _queues = list(map(lambda x:x.getObj(),queueInit))
                if _queues:
                    if filterEmpty: #Filter empty queues for get
                        filtered_q = list(filter(lambda x:x.qsize() > 0, _queues))
                    else: # Leave empty queues for put
                        filtered_q = list(filter(lambda x:x.qsize() >= 0, _queues))
                    if filtered_q:
                        _queue.append({'model':model,'port':port,'q':filtered_q[random.randint(0,len(filtered_q)-1)]})
                    if (method == 'all'):
                        if not filtered_q and list(set(_queues) - set(filtered_q)):
                            _queue.append({'model':model,'port':port,'q':list(set(_queues) - set(filtered_q))[0]})
                    elif (_queue and method == 'any'): break
## If input port all, check the load.
        if (_queue):
            if (method == 'all'):
                if (sorted(map(lambda x:x.get('q').qsize(),_queue))[0] < self._threadCount):
                    with self._lowLoadSema:
                        self._lowLoad = True
                        self.logger.debug('Model - %-10s on low load',_model)
                else:
                        self._lowLoad = False
                        self.logger.debug('Model - %-10s now on full load',_model)
#            else:
#                pass 
        return _queue
    
    def getPut(self,qIO,method=None,**kwargs):
        result = {}
        if (method == 'put'):
            for _queue in self.getRandomQs(qIO,method,filterEmpty=False):
                if self._modelType != 'sink':
                    _queue.get('q').put({(_queue.get('model'),_queue.get('port')):kwargs['item']})
                self.logger.debug('PUT: Model - %-10s, Port - %-10s, Data - %s, Qsize - %-10s', _queue.get('model'), _queue.get('port'), kwargs['item'],_queue.get('q').qsize())
                #if self._modelType == 'sink':
                #    self.logger.debug('PUT: Model - %-10s, Port - %-10s, Data - %s', _queue.get('model'), _queue.get('port'), kwargs['item'])
                #else:
        else:
            for _queue in self.getRandomQs(qIO,method,filterEmpty=True):
                self.logger.debug('GET: Model - %-10s, Port - %-10s, Data - %s, Qsize - %-10s', _queue.get('model'), _queue.get('port'), result, _queue.get('q').qsize())
                # Increasing timeout. If input_ports = all, the queue needs to wait on multiple processes to complete.
                if (method == 'all'):
                    if self._lowLoad:
                        result.update(_queue.get('q').get(timeout=10).get((_queue.get('model'),_queue.get('port'))))
                    else:
                        result.update(_queue.get('q').get(timeout=0.50).get((_queue.get('model'),_queue.get('port'))))
                else:
                    result.update(_queue.get('q').get(timeout=0.50).get((_queue.get('model'),_queue.get('port'))))
                self.logger.debug('GET: Model - %-10s, Port - %-10s, Data - %s, Qsize - %-10s', _queue.get('model'), _queue.get('port'), result, _queue.get('q').qsize())
                if (method == 'any'):
                    break
            if not result: #This is done for input_ports = any, to wait on a queue
                for _queue in self.getRandomQs(qIO,method,filterEmpty=False):
                    # Increasing timeout. If input_ports = any, the queue needs to wait on multiple processes to complete.
                    result.update(_queue.get('q').get(timeout=0.50).get((_queue.get('model'),_queue.get('port'))))
                    self.logger.debug('GET: Model - %-10s, Port - %-10s, Data - %s, Qsize - %-10s', _queue.get('model'), _queue.get('port'), result, _queue.get('q').qsize())
                    if (method == 'any'):
                        break
            return result

    def getQIn(self):
        return self._qIn

    def getQOut(self):
        return self._qOut

    def getQErr(self):
        return self._qErr

    def getQOnSuccess(self):
        return self._qOnSuccess

    def getQOnFailure(self):
        return self._qOnFailure

    async def consumer(self,*args,**kwargs):
        e_complete = kwargs.get('process_complete')
        while True:
            try:
                _result = kwargs.get('resultQ').get(timeout=0.50)
                if (self._modelType == 'connection'):
                    self.logger.debug('CONSUMER:GET: Class - %-10s, Method - %-10s, Recv - %s', self._className, self._methodName, _result)
                else:
                    self.logger.debug('CONSUMER:GET: Class - %-10s, Method - %-10s, Recv - %s', self._className, self._methodName, _result)
                if _result:
                    if (self._modelType == 'connection'):
                        if _result.get('OnFailure'):
                            self.getPut(self.getQOnFailure(),method='put',item=_result)
                        else:
                            self.getPut(self.getQOnSuccess(),method='put',item=_result)
                    else:
                        self.getPut(self.getQOut(),method='put',item=_result)
            except Empty:
                if e_complete.wait(5):
                    e_complete.clear()
                    break
                else:
                    continue

    def producer_api(self,*args,**kwargs):
        if (self._modelType == 'connection'):
            self.logger.debug('PRODUCER_API: Class - %-10s, Method - %-10s, Send - %s', self._className, self._methodName, kwargs.get('taskKwargs'))
        else:
            self.logger.debug('PRODUCER_API: Class - %-10s, Method - %-10s, Send - %s', self._className, self._methodName, kwargs.get('taskKwargs'))
        try:
            _result = getattr(kwargs.get('taskObject'),self._methodName)(kwargs.get('resultQ'),*kwargs.get('taskArgs'),**kwargs.get('taskKwargs')) 
        except:
            raise 
        #self.logger.debug('PRODUCER_API: Class - %-10s, Method - %-10s, Recv - %s', self._className, self._methodName, kwargs.get('taskKwargs'))


    async def producer(self,*args,**kwargs):
        e_complete = kwargs.get('process_complete')
        e_complete.clear() 
        try:
            self.producer_api(self,*args,**kwargs)
            e_complete.set() 
        except:
            e_complete.set() 
            raise

#    def target(self,*args,**kwargs):
#       while True:
#           try:
#               _args   = ()
#               _kwargs = {}
#               _object = None
#               resultQ = queue.Queue()
#               process_complete = threading.Event()
#               with self.lock:
#                   #self.logger.debug(self.importModule.cache_info())
#                   _object = getattr(self._module,self._className)(*self._args,**self._kwargs)
#                   try:
#                       _kwargs = self.getPut(self.getQIn(),method=self._input_ports)
## Controller
#                       tasks = [asyncio.ensure_future(self.producer(process_complete=process_complete,resultQ=resultQ,taskObject=_object,taskArgs=_args,taskKwargs=_kwargs,*args,**kwargs),loop=self._loop),asyncio.ensure_future(self.consumer(process_complete=process_complete,resultQ=resultQ,taskObject=_object,taskArgs=_args,taskKwargs=_kwargs,*args,**kwargs),loop=self._loop)]
#                       result_producer, result_consumer=self._loop.run_until_complete(asyncio.gather(*tasks,return_exceptions=False))
#                   except Empty:
#                       continue
#               if (self._modelType == 'generator'):
#                   break
#           except:
#               self.logger.debug(sys.exc_info())
#               self.getPut(self.getQErr(),method='put',item=sys.exc_info())

    def target(self,*args,**kwargs):
        self.logger.debug('WAITING FOR INIT OK SIGNAL')
        self._modelInit.wait()
        self.logger.debug('INIT OK')
        while True:
            try:
                _args   = ()
                _kwargs = {}
                _object = None
                resultQ = queue.Queue()
                process_complete = threading.Event()
                #self.logger.debug(self.importModule.cache_info())
                _object = getattr(self._module,self._className)(*self._args,**self._kwargs)
                try:
                    _kwargs = self.getPut(self.getQIn(),method=self._input_ports)
# Controller
                    tasks = [asyncio.ensure_future(self.producer(process_complete=process_complete,resultQ=resultQ,taskObject=_object,taskArgs=_args,taskKwargs=_kwargs,*args,**kwargs),loop=self._loop),asyncio.ensure_future(self.consumer(process_complete=process_complete,resultQ=resultQ,taskObject=_object,taskArgs=_args,taskKwargs=_kwargs,*args,**kwargs),loop=self._loop)]
                    result_producer, result_consumer=self._loop.run_until_complete(asyncio.gather(*tasks,return_exceptions=False))
                except Empty:
                    continue
                if (self._modelType == 'generator'):
                    break
            except:
                self.logger.error(str(sys.exc_info()) + ' in ' + self._className + '.' + self._methodName)
                self.getPut(self.getQErr(),method='put',item=sys.exc_info())
# Transparent delays
            if (self._delay):
                time.sleep(int(self._delay))


    def getTarget(self,*args,**kwargs):
        return self.target
