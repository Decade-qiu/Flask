
from flask import Blueprint, render_template, jsonify, redirect, url_for, session
from exts import mail, db
from flask_mail import Message
from flask import request
import string
import random
from tools.forms import *
from model.models import User
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint("regist", __name__)


@bp.route("/regist/", methods=['GET', 'POST'])
def regist():
    if request.method == 'GET':
        data = dict(
            title="注册"
        )
        return render_template("regist.html", data=data)
    else:
        res = dict(code=0)
        form = RegistForm(request.form)
        if form.validate():
            if CRUD.save_regist_user(form):
                res["code"] = 1
        else:
            res = form.errors
            res["code"] = 0
        return res
