from ModelIO import ModelIO
from ModelConfig import ModelConfig
class ModelCreate(object):
    def __init__(self,*args,**kwargs):
        self._ModelConfig = ModelConfig(kwargs.get('filename')) #*args,**kwargs)
        self._modelNames = self._ModelConfig.getModels()
        self._model = None

    def create(self,*args,**kwargs):
        self._model = ModelIO(*args,**kwargs)

    def getModel(self):
        return self._model

