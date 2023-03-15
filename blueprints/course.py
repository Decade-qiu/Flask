import os
import uuid
from datetime import datetime
from flask import Blueprint, render_template, jsonify, redirect, url_for, session
from flask_mail import Message
from flask import request
import string
import random
from tools.forms import *

bp = Blueprint("course", __name__)


@bp.route("/course/", methods=['GET'])
def course():
    data = dict(
        title="课程列表",
        stream=''
    )
    page = request.args.get('page', 1)
    res = CRUD.show_stream('all_1mqnabzvxc', int(page))
    data['stream'] = res.items
    return render_template(
        "course.html", data=data,
        pagination=res
    )
