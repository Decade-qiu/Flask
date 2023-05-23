import json
import os
import uuid
from datetime import datetime
from flask import Blueprint, render_template, jsonify, redirect, url_for, session
from flask_mail import Message
from flask import request
import string
import random
from model.models import Course
from tools.forms import *
from tools.orm import ORM

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
    content = json.loads(res.content)
    data['content'] = content['info']
    data['names'] = content['name'].split()
    data['pnum'] = len(data['names'])
    data['streamid'] = res.streamid
    print(res.streamid)
    if data['streamid'] != None:
        data['streamname'] = CRUD.find_stream(res.streamid).title
    return render_template(
        "kc.html", data=data,
    )

@bp.route("/kc/add", methods=['POST'])
def add():
    res = dict(code=0)
    # CRUD.add_course(request.form['title'], request.form('stu'))
    title = request.form['title']
    stu = request.form['stu']
    connect = ORM.db()
    try:
        print(title, stu)
        course = connect.query(Course).filter_by(title=title).order_by(Course.createdAt.desc()).first()
        content = json.loads(course.content)
        names = content['name']
        names += " "+stu
        content['name'] = names
        course.content = json.dumps(content)
    except Exception as e:
        print(e)
        connect.rollback()
    else:
        connect.commit()
    finally:
        connect.close()
        return res
