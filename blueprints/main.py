
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
        title="首页",
    )
    page = request.args.get('page', 1)
    res = CRUD.show_course('all_1mqnabzvxc', int(page))
    # 打乱res
    random.shuffle(res.items)
    data['course'] = res.items
    return render_template(
        "courses.html", data=data,
        pagination=res
    )
