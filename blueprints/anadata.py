import json
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
from model.models import Course, User
from werkzeug.security import generate_password_hash, check_password_hash

from tools.orm import ORM

bp = Blueprint("data", __name__)


@bp.route("/data/", methods=['GET'])
@is_login
def data():
    cn = session.get('name', '')
    data = dict(
        title="课程创建",
        name=cn
    )
    connect = ORM.db()
    data['course'] = []
    for cc in connect.query(Course).all():
        con = json.loads(cc.content)
        if cn in con['name'].split():
            data['course'].append(cc.title)
    data['attend'] = [random.randint(0, 10) for i in range(len(data['course']))]
    # print(data['attend'], data['course'])
    return render_template("data.html", data=data)
