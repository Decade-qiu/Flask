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

bp = Blueprint("playchat", __name__)


@bp.route("/playchat/", methods=['GET'])
def playchat():
    vid = request.args.get('id', None)
    if vid:
        data = dict(
            title="弹幕视频"
        )
        data['video'] = CRUD.video(vid)
        # print(data)
        return render_template("playchat.html", data=data)
