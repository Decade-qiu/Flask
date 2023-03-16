import json
import os
import uuid
from datetime import datetime

from flask import Blueprint, render_template, jsonify, redirect, url_for, session
from flask_mail import Message
from flask import request
import string
import random
from tools.rd import rd
from tools.forms import *
from model.models import User
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint("dm", __name__)


@bp.route("/dm/v3/", methods=['GET', 'POST'])
def dm():
    if request.method == 'GET':
        id = request.args.get("id", None)  # 获取视频ID
        if id:
            key = 'dm{}'.format(id)  
            if rd.llen(key):
                data = rd.lrange(key, 0, 3000)  # 列表
                data = [json.loads(v) for v in data]  # json字符串，转化成字典
                res = {
                    "code": 1,
                    "data": [
                        [v['time'], v['type'], v['color'], v['author'], v['text']]
                        for v in data
                    ]
                }
            else:
                res = {
                    "code": 0,
                    "data": []
                }
            # 返回接口
            return res
    else:
        data = request.json  # 直接获取json数据，二进制
        rd.lpush('dm{}'.format(data['id']), json.dumps(data))
        # 返回接口
        return dict(
            code=0,
            data=data
        )
