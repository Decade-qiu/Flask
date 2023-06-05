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

bp = Blueprint("stream", __name__)


@bp.route("/stream/", methods=['GET', 'POST'])
def stream():
    if request.method == 'GET':
        data = dict(
            title="Stream"
        )
        name = request.args.get('name', '')
        streamid = request.args.get('id', '')
        data['name'] = name
        data['streamid'] = streamid
        return render_template("stream.html", data=data)
    else:
        rtmp_url = request.form.get('url', "") + "/a/a/a/a"
        rtmp, myapp, name = rtmp_url[7:].split('/')[0:3]
        print(rtmp_url, rtmp, myapp, name)
        res = dict(
            name=name
        )
        return res

@bp.route("/ss/", methods=['GET'])
def ss():
    data = dict(
        title="Stream"
    )
    streamid = request.args.get('id', '')
    data['streamid'] = streamid
    return render_template("temp.html", data=data)

