import json
import os
import uuid
from datetime import datetime

from flask import Blueprint, render_template, jsonify, redirect, url_for, session
from flask_mail import Message
from flask import request
import string
import random
from tools.forms import *
from model.models import User
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint("msg", __name__)


@bp.route("/msg/", methods=['POST'])
def msg():
    sid = request.form.get('streamid')
    data = CRUD.new_msg(sid)
    result = []
    for v in data:
        result.append(json.loads(v.content))  # 转化为字典追加
    return dict(
            data=result
        )
