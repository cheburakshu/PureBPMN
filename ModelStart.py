import time
import sys
from ModelBootstrap import ModelBootstrap
import ModelManager
import threading

def bootstrap(_filename):
#Model Bootstrap
    mb = ModelBootstrap(filename=_filename)


runForEver = threading.Event()

# Expects a .conf for the model. It should be availble in config folder
modelConf=sys.argv[1]

t = threading.Thread(target=bootstrap,args=(modelConf,))
t.setDaemon(False)
t.start()
# This will wait forever. 
# 
runForEver.wait()
