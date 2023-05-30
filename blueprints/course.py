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
from tools.decorators import is_login
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

@bp.route("/mykc/", methods=['GET'])
@is_login
def mycourses():
    data = dict(
        title="课程列表",
    )
    page = request.args.get('page', 1)
    res = CRUD.show_course(session.get('name', ''), int(page))
    data['course'] = res.items
    return render_template(
        "myCourse.html", data=data,
        pagination=res
    )

@bp.route('/upkc/', methods=['POST'])
def upload():
    upload_path = os.path.join(
        os.path.dirname(
            os.path.dirname(__file__)
        ), "static/uploads"
    )
    files = request.files.getlist("files")
    uid = request.form.get('uid')
    print(files)
    data = {'code': '上传成功！'}
    course = None
    connect = ORM.db()
    try:
        course = connect.query(Course).filter_by(id=uid).order_by(Course.createdAt.desc()).first()
        con = json.loads(course.content)
        fns = ""
        con['files'] = con.get('files', '')
        for file in files:
            fname = file.filename
            fname = datetime.now().strftime("%Y%m%d%H%M%S")+uuid.uuid4().hex+"&"+fname
            file.save(os.path.join(upload_path, fname))
            fns += fname + " "
        con['files'] += fns
        course.content = json.dumps(con)
    except Exception as e:
        connect.rollback()
        data['code'] = e
    else:
        connect.commit()  
    finally:
        connect.close()
    return data

@bp.route('/upvideo/', methods=['POST'])
def uploadvv():
    upload_path = os.path.join(
        os.path.dirname(
            os.path.dirname(__file__)
        ), "static/uploads"
    )
    files = request.files.getlist("files")
    uid = request.form.get('uid')
    print(files)
    data = {'code': '上传成功！'}
    course = None
    connect = ORM.db()
    try:
        course = connect.query(Course).filter_by(id=uid).order_by(Course.createdAt.desc()).first()
        con = json.loads(course.content)
        fns = ""
        con['videos'] = con.get('videos', '')
        for file in files:
            fname = file.filename
            dt = datetime.now().strftime("%Y%m%d%H%M%S")
            fname = dt+"@"+uuid.uuid4().hex+"@"+fname
            file.save(os.path.join(upload_path, fname))
            fns += fname + " "
        con['videos'] += fns
        course.content = json.dumps(con)
    except Exception as e:
        connect.rollback()
        data['code'] = e
    else:
        connect.commit()  
    finally:
        connect.close()
    return data

@bp.route("/course/update/", methods=['GET', 'POST'])
def updcourses():
    if request.method == 'GET':
        data = dict(
            title="课程",
        )
        res = CRUD.find_course(request.args.get('id'))
        data['course'] = res
        data['con'] = json.loads(res.content)['info']
        data['price'] = json.loads(res.content).get('price', '0')
        return render_template(
            "updCourse.html", data=data,
        )
    else:
        form = courseUpdForm(request.form)
        uid = form.data['courseid']
        course = None
        connect = ORM.db()
        data = dict()
        data['code'] = 1
        try:
            course = connect.query(Course).filter_by(id=uid).order_by(Course.createdAt.desc()).first()
            course.title = form.data['title']
            con = json.loads(course.content)
            con['info'] = form.data['content']
            con['price'] = form.data['price']
            course.content = json.dumps(con)
            course.face = form.data['face']
        except Exception as e:
            connect.rollback()
            print(e)
        else:
            connect.commit()
            data['code'] = 0    
        finally:
            connect.close()
        return data   

def ccc(s):
    datetime_obj = datetime.strptime(s, '%Y%m%d%H%M%S')
    return datetime_obj.strftime('%Y年%m月%d日%H点%M分')

@bp.route("/kc/", methods=['GET'])
def kc():
    data = dict(
        title="课程",
    )
    res = CRUD.find_course(request.args.get('id'))
    data['course'] = res
    content = json.loads(res.content)
    data['content'] = content['info']
    data['price'] = content.get('price', '0')
    data['names'] = content['name'].split()
    data['pnum'] = len(data['names'])
    data['streamid'] = res.streamid
    ffs = content.get('files', '').split()
    # print(ffs, content.get('videos', '').split())
    data['files'] = [[f.split("&")[1], f] for f in ffs if f != ''][::-1]
    data['videos'] = [[f.split("@")[2], ccc(f.split("@")[0]), f, f.split("@")[0]] for f in content.get('videos', '').split() if f != ''][::-1]
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
