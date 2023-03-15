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

bp = Blueprint("myStream", __name__)


@bp.route("/myStream/", methods=['GET'])
@is_login
def myStream():
    data = dict(
        title="直播列表",
        stream=''
    )
    page = request.args.get('page', 1)
    res = CRUD.show_stream(session.get('name', ''), int(page))
    data['stream'] = res.items
    return render_template(
        "myStream.html", data=data,
        pagination=res
    )
