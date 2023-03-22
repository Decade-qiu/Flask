
from flask import Blueprint, render_template, jsonify, redirect, url_for, session
from flask_mail import Message
from flask import request
import string
import random
from tools.forms import *
from model.models import User
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint("screen", __name__)


@bp.route("/screenShare/", methods=['GET'])
def screen():
    if request.method == 'GET':
        data = dict(
            title="屏幕分享"
        )
        return render_template("screenShare.html", data=data)
