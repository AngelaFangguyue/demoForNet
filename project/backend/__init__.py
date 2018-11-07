# -*- coding: utf-8 -*-

import os
import json
from flask import Flask
from backend import config
from flask_pymongo import PyMongo


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

def register_blueprint(app):
    from backend.account import account
    from backend.api import api
    app.register_blueprint(account)
    app.register_blueprint(api, url_prefix="/api")


def register_mongoDB(app):
    app.config.update(
        MONGO_HOST=config.MONGO_HOST,
        MONGO_PORT=config.MONGO_PORT,
        MONGO_DBNAME=config.MONGO_DBNAME
    )
    return PyMongo(app, config_prefix="MONGO")


app = Flask(__name__)
app.secret_key = config.SESSION_SECRET_KEY
app.config['SESSION_COOKIE_NAME'] = "session%d:"%config.WEB_SERVER_PORT

mongo = register_mongoDB(app)
register_context_processors(app)
register_blueprint(app)

from backend import views
import sys
reload(sys)
sys.setdefaultencoding('utf-8')



