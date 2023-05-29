import json
import os
import uuid
from datetime import datetime

from flask import Blueprint, render_template, jsonify, redirect, url_for, session
from flask_mail import Message
from flask import request
import string
import random
from tools.forms import *
from model.models import CC, Comment, User
from werkzeug.security import generate_password_hash, check_password_hash

from tools.orm import ORM

bp = Blueprint("msg", __name__)


@bp.route("/msg/", methods=['POST'])
def msg():
    sid = request.form.get('streamid')
    data = CRUD.new_msg(sid)
    result = []
    for v in data:
        result.append(json.loads(v.content))  
    return dict(
            data=result
        )

@bp.route("/com/", methods=['POST'])
def comment():
    sid = request.form.get('courseid')
    print(sid)
    connect = ORM.db()
    data = None
    try:
        data = connect.query(Comment).filter_by(courseId=sid).order_by(Comment.createdAt.asc()).all()
    except Exception as e:
        connect.rollback()
        print(e)
    else:
        connect.commit()
    finally:
        connect.close()
    result = []
    for v in data:
        result.append(json.loads(v.content))  
    return dict(
            data=result
        )

@bp.route("/kcpj/", methods=['POST'])
def kcpj():
    sid = request.form.get('courseid')
    connect = ORM.db()
    data = None
    try:
        data = connect.query(CC).filter_by(courseId=sid).order_by(CC.createdAt.asc()).all()
    except Exception as e:
        connect.rollback()
        print(e)
    else:
        connect.commit()
    finally:
        connect.close()
    result = []
    for v in data:
        result.append(json.loads(v.content))  
    return dict(
            data=result
        )
