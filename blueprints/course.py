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
        title="直播列表",
        stream=''
    )
    page = request.args.get('page', 1)
    res = CRUD.show_stream('all_1mqnabzvxc', int(page))
    data['stream'] = res.items
    return render_template(
        "course.html", data=data,
        pagination=res
    )

@bp.route("/courses/", methods=['GET'])
def courses():
    data = dict(
        title="课程列表",
    )
    page = request.args.get('page', 1)
    res = CRUD.show_course('all_1mqnabzvxc', int(page))
    data['course'] = res.items
    return render_template(
        "courses.html", data=data,
        pagination=res
    )

@bp.route("/kc/", methods=['GET'])
def kc():
    data = dict(
        title="课程",
    )
    res = CRUD.find_course(request.args.get('id'))
    data['course'] = res
    return render_template(
        "kc.html", data=data,
    )
