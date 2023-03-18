
from flask import Blueprint, render_template, jsonify, redirect, url_for, session
from flask_mail import Message
from flask import request
import string
import random
from tools.forms import *
from model.models import User
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint("help", __name__)


@bp.route("/help/", methods=['GET'])
def help():
    data = dict(
        title="帮助"
    )
    return render_template("help.html", data=data)