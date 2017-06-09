import uuid

class ModelConnections(object):
    def __init__(self,*args,**kwargs):
        pass

    def connection(self,resultQ,*args,**kwargs):
#    def connection(self,*args,**kwargs):
        resultQ.put(kwargs)
        return kwargs
