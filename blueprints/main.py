
from flask import Blueprint, render_template, jsonify, redirect, url_for, session
from flask_mail import Message
from flask import request
import string
import random
from tools.forms import *
from model.models import User
from werkzeug.security import generate_password_hash, check_password_hash

# /auth
bp = Blueprint("main", __name__)


@bp.route("/", methods=['GET'])
def main():
    data = dict(
        title="Decade"
    )
    return render_template("main.html", data=data)
