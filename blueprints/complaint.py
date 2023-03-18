
from flask import Blueprint, render_template, jsonify, redirect, url_for, session
from flask_mail import Message
from flask import request
import string
import random
from tools.forms import *
from model.models import User
from werkzeug.security import generate_password_hash, check_password_hash

# /auth
bp = Blueprint("complaint", __name__)


@bp.route("/complaint/", methods=['GET'])
def main():
    data = dict(
            title="投诉",
            user=CRUD.user(session.get('name'))
        )
    return render_template("complaint.html", data=data)
