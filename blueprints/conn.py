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
from model.models import *
from werkzeug.security import generate_password_hash, check_password_hash

from tools.orm import ORM

bp = Blueprint("conn", __name__)

@bp.route("/conn/", methods=['POST'])
def conn():
    key = request.form.get('streamid')
    name = request.form.get('name')
    pwd = request.form.get('pwd')
    f = "签到成功！"
    ff = 1
    connect = ORM.db()
    try:
        stream = connect.query(Stream).filter(Stream.id==key).first()
        time = stream.cktAt
        passd = stream.pwd
        if int(passd)!= int(pwd):
            f = "签到码错误！"
            ff = 0
        cur_time = datetime.now()
        if  cur_time > time:
            f = "已经超时！"
            ff = 0
        if ff == 1:
            check = Check(
                key=key,
                name=name,
                ckt=cur_time.strftime("%Y-%m-%d %H:%M:%S")
            )
            connect.add(check)
    except Exception as e:
        connect.rollback()
        f = "签到失败！"
        print(e)
    else:
        connect.commit()
    finally:
        connect.close()
    return dict(
            code=f
        )

@bp.route("/mute/", methods=['POST'])
def is_mute():
    key = request.form.get('streamid')
    f = 0
    connect = ORM.db()
    try:
        stream = connect.query(Stream).filter(Stream.id==key).first()
        f = stream.mute
    except Exception as e:
        connect.rollback()
    else:
        connect.commit()
    finally:
        connect.close()
    return dict(
            code=f
        )