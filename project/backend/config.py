# -*- coding:utf-8 -*-

"""
配置文件
"""

import platform


WEB_SERVER_PORT = 12345      # 端口
SESSION_SECRET_KEY = '\x1b\x0c\xd9b\xab\xb0\x82\xf0\x9f)\xae\x8b\xa2r~\xf2nlYV\x87\x1a\x12\xa0'   # 用的时候自己换一个

if "Windows" in platform.system():
    NET_LOC = "http://localhost:%d" % WEB_SERVER_PORT
else:
    # NET_LOC = "http://qa.pangu.netease.com:%d" % WEB_SERVER_PORT
    pass

LOG_FILE = "real.log"   # logger记录文件
LOG_DO_PRINT = True     # 记录log的同时也print

# MongoDB Configs
MONGO_HOST = "localhost"
MONGO_PORT = 27017
MONGO_DBNAME = "my_website"

