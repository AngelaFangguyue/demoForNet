# -*- coding: utf-8 -*-

from flask import session
from flask import request
from flask import redirect
from backend.account import account
from backend.utils import openId
from backend import mongo
from backend.utils import logger
from backend import config


@account.route("/login")
def login():
    url = request.args.get("next")
    if url:
        session["redirect"] = url
    params = openId.LoginParams(
        netloc=config.NET_LOC,
        payloads=request.args,
        session=session,
        login_uri="/login",
        openid_redirect_to=session.get("redirect") or "/",
        on_success=on_success,
        success_args=(session, request.args),
        check_login_func=check_login,
        redirect=redirect,
    )
    return openId.login(params)


@account.route("/logout")
def logout():
    session.clear()
    return redirect("/index")


def on_success(session, payloads):
    try:
        ASSOC = session.pop("ASSOC")
    except KeyError:
        ASSOC = {}
    result = openId.MyCheck(payloads, ASSOC)
    if result[0]:
        session["email"] = payloads['openid.sreg.email']
        session["cname"] = payloads[u'openid.sreg.fullname']
        session["username"] = payloads['openid.sreg.nickname']
        return True
    else:
        return False


def login_required(func):
    from functools import wraps
    @wraps(func)
    def wrapper(*args, **kwargs):
        from flask import session
        if "email" in session:
            return func(*args, **kwargs)
        else:
            return "LOGIN REQUIRED", 404        # 这里要和前端main.js里面的axios的拦截器相对应

    return wrapper


def get_user_info(email):
    return mongo.db.account.find_one({"email": email})


def check_login(session):
    return "email" in session
