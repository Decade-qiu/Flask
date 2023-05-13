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

bp = Blueprint("upload", __name__)


@bp.route("/upload/", methods=['POST'])
def upload():
    files = request.files["img"]
    upload_path = os.path.join(
        os.path.dirname(
            os.path.dirname(__file__)
        ), "static/uploads"
    )
    # 如果目录不存在则创建
    if not os.path.exists(upload_path):
        os.mkdir(upload_path)
    # 指定修改名称
    imgname = files.filename
    imgname = datetime.now().strftime("%Y%m%d%H%M%S")+uuid.uuid4().hex+imgname
    files.save(os.path.join(upload_path, imgname))
    return dict(
        code=1, image=imgname
    )
