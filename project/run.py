# -*- coding: utf-8 -*-

from backend import app
from backend import config

if __name__ == "__main__":
    app.run(port=config.WEB_SERVER_PORT, host="0.0.0.0", debug=True, threaded=True)