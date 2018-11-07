# -*- coding: utf-8 -*-

from flask import session
from flask import jsonify
from flask import request
from backend.api import api
from backend.account import user as User


@api.route("/user/base", methods=["POST"])
@User.login_required
def fetch_user_base_info():
    user = User.get_user_info(session.get("email"))
    if not user:
        return "No such user", 404
    return jsonify(user), 200