
from flask import Blueprint, render_template, jsonify, redirect, url_for, session
from flask_mail import Message
from flask import request
import string
import random
from tools.forms import *
from model.models import User
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint("renmark", __name__)


@bp.route("/renmark/", methods=['GET'])
def screen():
    if request.method == 'GET':
        data = dict(
            title="连麦"
        )
        return render_template("renmark.html", data=data)
