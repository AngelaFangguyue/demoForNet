# -*- coding:utf-8 -*-

"""
配置文件
"""

import platform


WEB_SERVER_PORT = 9874      # 后端端口

if "Windows" in platform.system():
    NET_LOC = "http://localhost:%d" % WEB_SERVER_PORT
else:
    pass


