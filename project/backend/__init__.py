# -*- coding: utf-8 -*-

from flask import Flask
from backend import config
import os
import json

def register_context_processors(app):
    @app.context_processor
    def manifest():
        """
        读取到打包好的静态文件和原始文件的对应关系，将对应关系添加到上下文中
        :return:
        """
        manifest = {}
        APP_DIR = os.path.dirname(__file__)
        try:
            with open(APP_DIR + '/static/dist/manifest.json', 'r') as f:
                manifest = json.load(f)
        except Exception:
            print(
                'no manifest file found at ' + APP_DIR + '/static/dist/manifest.json'
            )
        return dict(manifest=manifest)


app = Flask(__name__)
register_context_processors(app)

from backend import views
import sys
reload(sys)
sys.setdefaultencoding('utf-8')



