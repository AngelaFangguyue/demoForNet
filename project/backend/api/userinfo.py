# -*- coding: utf-8 -*-

from flask import session
from flask import jsonify
from flask import request
from backend.api import api
from backend.account import user as User
from backend import mongo


@api.route("/user/base", methods=["POST"])
@User.login_required
def fetch_user_base_info():
    user = User.get_user_info(session.get("email"))
    if not user:
        return "No such user", 404
    return jsonify(user), 200


@api.route("/user/nickname/modify", methods=["POST"])
@User.login_required
def modify_user_nickname():
    """修改用户昵称"""
    nickname = request.form.get("nickname")
    if not nickname:
        return "Lack nickname", 404
    mongo.db.account.update({"email": session["email"]}, {"$set": {"nickname": nickname}})
    return "Success", 200