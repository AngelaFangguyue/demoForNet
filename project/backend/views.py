# -*- coding: utf-8 -*-

from flask import render_template
from backend import app
from backend import config
from flask import session
from flask import redirect
from flask import url_for

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def index(path):
    email = session.get("email", None)
    if not email:
        return redirect(url_for("account.login", next=path))
    return render_template("index.html")