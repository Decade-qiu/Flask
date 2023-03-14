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

bp = Blueprint("myStream", __name__)


@bp.route("/myStream/", methods=['GET'])
def myStream():
    data = dict(
        title="直播列表",
        stream=''
    )
    data['stream'] = CRUD.show_stream(session.get('name', ''))
    return render_template("myStream.html", data=data)
