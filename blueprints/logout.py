
from flask import Blueprint, render_template, jsonify, redirect, url_for, session
from exts import mail, db
from flask_mail import Message
from flask import request
import string
import random
from tools.forms import *
from model.models import User
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint("logout", __name__)


@bp.route("/logout/", methods=['GET'])
def logout():
    session.clear()
    return redirect("/login/")

