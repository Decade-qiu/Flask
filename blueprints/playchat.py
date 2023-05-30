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
    courseid = request.args.get('courseId', None)
    videoid = request.args.get('videoId', None)
    url = request.args.get('url', None)
    videoname = request.args.get('videoname', None)
    data = dict(
        title="弹幕视频",
        name=videoname,
        videoid=videoid+courseid,
        url=url
    )
    print(data)
    return render_template("playchat.html", data=data)
