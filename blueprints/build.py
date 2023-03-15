import os
import uuid
from datetime import datetime

from flask import Blueprint, render_template, jsonify, redirect, url_for, session
from flask_mail import Message
from flask import request
import string
import random
from tools.decorators import is_login
from tools.forms import *
from model.models import User
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint("build", __name__)


@bp.route("/build/", methods=['GET', 'POST'])
@is_login
def build():
    if request.method == 'GET':
        data = dict(
            title="直播创建",
            name=session.get('name', '')
        )
        return render_template("build.html", data=data)
    else:
        form = StreamBuildForm(request.form)
        res = dict(code=0)
        if form.validate():
            if CRUD.save_stream(form):
                res["code"] = 1
        else:
            res = form.errors
            res["code"] = 0
        return res
