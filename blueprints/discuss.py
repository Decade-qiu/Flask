import json
import os
import uuid
from datetime import datetime

from flask import Blueprint, render_template, jsonify, redirect, render_template_string, url_for, session
from flask_mail import Message
from flask import request
import string
import random
from model.CRUD import dt
from tools.decorators import is_login
from tools.forms import *
from model.models import User
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint("discuss", __name__)


@bp.route("/discuss/", methods=['GET'])
def discuss():
    data = dict(
        title="Stream",
    )
    res = CRUD.get_posts()
    posts = []
    for i in res:
        d = json.loads(i.content)
        d['id'] = i.id
        posts.append(d)
    return render_template('discuss.html', data=data, posts=posts)

@bp.route('/discuss/post/', methods=['POST', 'GET'])
def show_post():
    if request.method == 'GET':
        data = dict(
            title="Post"
        )
        postId = request.args.get('id', '')
        res = CRUD.get_post(postId)
        d = json.loads(res.content)
        d['id'] = res.id
        post = d
        return render_template('post.html', data=data, post=post)
    else:
        name = session.get('name')
        title = request.form['title']
        content = request.form['content']
        data = {'name': name, 'title': title, 'content': content, 'dt':dt()}
        res = CRUD.save_post(json.dumps(data))
        if res:
            return redirect(url_for('discuss.discuss'))
        else:
            return "发帖失败！"

@bp.route('/createPost/', methods=['POST'])
def createPost():
    name = session.get('name')
    title = request.form['title']
    content = request.form['content']
    data = {'name': name, 'title': title, 'content': content, 'dt':dt()}
    res = CRUD.save_post(json.dumps(data))
    if res:
        return {"code" : "发帖成功！"}
    else:
        return {"code" : "发帖失败！"}

@bp.route('/newest/')
def newest():
    res = CRUD.get_posts()
    posts = []
    for i in res:
        d = json.loads(i.content)
        d['id'] = i.id
        posts.append(d)
    template = """
        {% for post in posts %}
        <div class="post card" post-id="{{ post['id'] }}" >
            <div class="card-body">
                <h2 class="card-title">{{ post['title'] }}</h2>
                <p class="card-subtitle mb-2 text-muted">Posted by {{ post['name'] }} on {{ post['dt'] }}</p>
                <p class="card-text">{{ post['content'] }}</p>
            </div>
        </div>
        {% endfor %}
    """
    return render_template_string(template, posts=posts)

@bp.route('/hottest/')
def hottest():
    res = CRUD.get_posts()
    posts = []
    for i in res:
        d = json.loads(i.content)
        d['id'] = i.id
        posts.append(d)
    template = """
        {% for post in posts %}
        <div class="post card" post-id="{{ post['id'] }}" >
            <div class="card-body">
                <h2 class="card-title">{{ post['title'] }}</h2>
                <p class="card-subtitle mb-2 text-muted">Posted by {{ post['name'] }} on {{ post['dt'] }}</p>
                <p class="card-text">{{ post['content'] }}</p>
            </div>
        </div>
        {% endfor %}
    """
    return render_template_string(template, posts=posts)

@bp.route('/recommended/')
def recommended():
    res = CRUD.get_posts()
    posts = []
    for i in res:
        d = json.loads(i.content)
        d['id'] = i.id
        posts.append(d)
    template = """
        {% for post in posts %}
        <div class="post card" post-id="{{ post['id'] }}" >
            <div class="card-body">
                <h2 class="card-title">{{ post['title'] }}</h2>
                <p class="card-subtitle mb-2 text-muted">Posted by {{ post['name'] }} on {{ post['dt'] }}</p>
                <p class="card-text">{{ post['content'] }}</p>
            </div>
        </div>
        {% endfor %}
    """
    return render_template_string(template, posts=posts)