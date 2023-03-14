# -*- coding: utf-8 -*-
import datetime  # 导入日期时间模块
from model.models import User, Video, Msg, Stream
from tools.orm import ORM
from werkzeug.security import generate_password_hash  # 生成哈希密码
import math
from flask import request

# 定义生成日期时间的函数
def dt():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# 专门用于增删改查
class CRUD:
    # 验证用户唯一性，昵称1、邮箱2、手机3
    @staticmethod
    def user_unique(data, method=1):
        # 创建会话
        connect = ORM.db()
        user = None
        # 事务处理的逻辑
        try:
            model = connect.query(User)
            if method == 1:
                # 昵称
                user = model.filter_by(name=data).first()
            if method == 2:
                # 邮箱
                user = model.filter_by(email=data).first()
            if method == 3:
                # 手机
                user = model.filter_by(phone=data).first()
        except Exception as e:
            connect.rollback()  # 如果发生异常直接回滚
        else:
            connect.commit()  # 没有发生异常直接提交
        finally:
            connect.close()  # 无论是否发生异常最后一定关闭会话
        if user:
            return True
        else:
            return False

    @staticmethod
    # 保存注册用户
    def save_regist_user(form):
        # 创建会话
        connect = ORM.db()
        try:
            user = User(
                name=form.data['name'],
                pwd=generate_password_hash(form.data['pwd']),
                email=form.data['email'],
                phone=form.data['phone'],
                sex=None,
                xingzuo=None,
                face=None,
                info=None,
                createdAt=dt(),
                updatedAt=dt()
            )
            # 添加记录
            connect.add(user)
        except Exception as e:
            connect.rollback()
            return False
        else:
            connect.commit()
            return True
        finally:
            connect.close()

    # 登录验证
    @staticmethod
    def check_login(name, pwd):
        connect = ORM.db()
        result = False
        try:
            user = connect.query(User).filter_by(name=name).first()
            if user:
                if user.check_pwd(pwd):
                    result = True
        except Exception as e:
            connect.rollback()
        else:
            connect.commit()
        finally:
            connect.close()
        return result

    # 保存用户信息
    @staticmethod
    def save_user(form):
        connect = ORM.db()
        try:
            user = connect.query(User).filter_by(id=int(form.data['id'])).first()
            user.name = form.data['name']
            user.email = form.data['email']
            user.phone = form.data['phone']
            user.sex = int(form.data['sex'])
            user.xingzuo = int(form.data['xingzuo'])
            user.face = form.data['face']
            user.info = form.data['info']
            user.updatedAt = dt()
            user.role = form.data['role']
            connect.add(user)
            print(form.data['role'])
            print(user.role)
            print("!!!!!!!!!")
        except Exception as e:
            connect.rollback()
        else:
            connect.commit()
        finally:
            connect.close()
        return True

    # 获取用户
    @staticmethod
    def user(name):
        connect = ORM.db()
        user = None
        try:
            user = connect.query(User).filter_by(name=name).first()
        except Exception as e:
            connect.rollback()
        else:
            connect.commit()
        finally:
            connect.close()
        return user

    # 获取视频
    @staticmethod
    def video(id):
        connect = ORM.db()
        video = None
        try:
            video = connect.query(Video).filter_by(id=int(id)).first()
        except Exception as e:
            connect.rollback()
        else:
            connect.commit()
        finally:
            connect.close()
        return video

    # 保存消息
    @staticmethod
    def save_msg(content, streamid):
        connect = ORM.db()
        try:
            msg = Msg(
                content=content,
                createdAt=dt(),
                updatedAt=dt(),
                streamId=streamid
            )
            connect.add(msg)
        except Exception as e:
            print(e)
            connect.rollback()
        else:
            connect.commit()
        finally:
            connect.close()

    # 查询消息
    @staticmethod
    def new_msg(sid):
        connect = ORM.db()
        data = None
        try:
            data = connect.query(Msg).filter_by(streamId=sid).order_by(Msg.createdAt.asc()).limit(200).all()
        except Exception as e:
            connect.rollback()
        else:
            connect.commit()
        finally:
            connect.close()
        return data

    # 保存直播信息
    @staticmethod
    def save_stream(form):
        connect = ORM.db()
        try:
            stream = Stream(
                title=form.data['title'],
                url=form.data['url'],
                createdAt=dt(),
                userid=form.data['userid']
            )
            connect.add(stream)
        except Exception as e:
            connect.rollback()
            return False
        else:
            connect.commit()
            return True
        finally:
            connect.close()

    # 显示直播信息
    @staticmethod
    def show_stream(name):
        connect = ORM.db()
        model = None
        try:
            model = connect.query(Stream).filter_by(userid=name).order_by(Stream.createdAt.desc())
        except Exception as e:
            connect.rollback()
            print(e)
        else:
            connect.commit()
        finally:
            connect.close()
        return CRUD.page(model)

    @staticmethod
    def page(model):
        # 获取页码
        page = request.args.get("page", 1)
        page = int(page)
        # 统计数据表中有多少条记录
        total = model.count()
        if total:
            # 每页显示多少条
            shownum = 6
            # 确定总共显示多少页
            pagenum = int(math.ceil(total / shownum))
            # 判断小于第一页
            if page < 1:
                page = 1
            # 判断大于最后一页
            if page > pagenum:
                page = pagenum

            # sql限制查询，每次查询限制多少条，偏移量是多少
            offset = (page - 1) * shownum
            # 分页查询
            data = model.limit(shownum).offset(offset)
            # 上一页
            prev_page = page - 1
            next_page = page + 1
            if prev_page < 1:
                prev_page = 1
            if next_page > pagenum:
                next_page = pagenum
            arr = dict(
                pagenum=pagenum,
                page=page,
                prev_page=prev_page,
                next_page=next_page,
                data=data
            )
        else:
            arr = dict(
                data=[]
            )
        return arr
