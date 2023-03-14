
from flask import Blueprint, render_template, jsonify, redirect, url_for, session
from flask_mail import Message
from flask import request
import string
import random
from tools.forms import *
from model.models import User
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint("login", __name__)


@bp.route("/login/", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        data = dict(
            title="登录"
        )
        return render_template("login.html", data=data)
    else:
        res = dict(code=0)
        form = LoginForm(request.form)
        if form.validate():
            session['name'] = form.data['name']
            session['face'] = CRUD.user(form.data['name']).face
            res["code"] = 1
        else:
            res = form.errors
            res["code"] = 0
        return res
