import logging
import logging.config
import time

def logSetup():
    LOG_PATH = 'log/'
    fileName = LOG_PATH + 'runlog.' + str(int(time.time())) + '.out'
    logging.config.fileConfig('config/logging.conf',defaults={'logfilename': fileName})
