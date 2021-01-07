import logging

#global logger
logger = logging.getLogger(name='mylogger')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '[%(asctime)s:%(module)s:%(lineno)s:%(levelname)s] %(message)s'
)
filehandler = logging.FileHandler('harvester.log',mode='w')
filehandler.setLevel(logging.DEBUG)
filehandler.setFormatter(formatter)
logger.addHandler(filehandler)