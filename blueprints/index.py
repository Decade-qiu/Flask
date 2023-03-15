from flask import Blueprint, render_template, request
from tools.forms import *
from model.models import User
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint("index", __name__)


@bp.route("/index/", methods=['GET'])
def main():
    data = dict(
        title="视频列表"
    )
    q = request.args.get("q", "")
    data['video'] = CRUD.show_video(q)
    data['q'] = q
    return render_template("index.html", data=data)
