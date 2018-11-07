# -*- coding: utf-8 -*_

import logging
import logging.handlers
from backend import config

handler = logging.handlers.RotatingFileHandler(config.LOG_FILE, maxBytes=10*1024*1024, backupCount=5)
fmt = '[%(asctime)s] [%(levelname)s]:  %(message)s'
formatter = logging.Formatter(fmt)
handler.setFormatter(formatter)
logger = logging.getLogger('real')
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

def trans(msg):
    try:
        msg = str(msg) if not type(msg) is str else msg
        return msg
    except:
        return msg

def info(msg):
    msg = trans(msg)
    if config.LOG_DO_PRINT:
        try:
            print u'[INFO]%s'% msg
        except:
            pass
    logger.info(msg)


def debug(msg):
    msg = trans(msg)
    if config.LOG_DO_PRINT:
        try:
            print u'[DEBUG]%s'% msg
        except:
            pass
    logger.debug(msg)


def error(msg):
    msg = trans(msg)
    if config.LOG_DO_PRINT:
        try:
            print u'[ERROR]%s'% msg
        except:
            pass
    logger.error(msg)
