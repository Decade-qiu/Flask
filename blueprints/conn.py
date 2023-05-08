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
    f = "签到成功！"
    connect = ORM.db()
    try:
        check = Check(
            key=key,
            name=name
        )
        connect.add(check)
    except Exception as e:
        connect.rollback()
        f = "签到失败！"
    else:
        connect.commit()
    finally:
        connect.close()
    return dict(
            code=f
        )

