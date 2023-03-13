
from flask import Blueprint, render_template, jsonify, redirect, url_for, session
from exts import mail, db
from flask_mail import Message
from flask import request
import string
import random
from tools.forms import *
from model.models import User
from werkzeug.security import generate_password_hash, check_password_hash

# /auth
bp = Blueprint("main", __name__)


@bp.route("/", methods=['GET'])
def main():
    data = dict(
        title="Decade"
    )
    return render_template("main.html", data=data)
    # else:
    #     form = LoginForm(request.form)
    #     if form.validate():
    #         email = form.email.data
    #         password = form.password.data
    #         user = UserModel.query.filter_by(email=email).first()
    #         if not user:
    #             print("邮箱在数据库中不存在！")
    #             return redirect(url_for("auth.login"))
    #         if check_password_hash(user.password, password):
    #             # cookie：
    #             # cookie中不适合存储太多的数据，只适合存储少量的数据
    #             # cookie一般用来存放登录授权的东西
    #             # flask中的session，是经过加密后存储在cookie中的
    #             session['user_id'] = user.id
    #             return redirect("/")
    #         else:
    #             print("密码错误！")
    #             return redirect(url_for("auth.login"))
    #     else:
    #         print(form.errors)
    #         return redirect(url_for("auth.login"))