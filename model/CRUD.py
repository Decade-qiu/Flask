# -*- coding: utf-8 -*-
import datetime  # 导入日期时间模块
from model.models import User, Video, Msg, Stream
from tools.orm import ORM
from werkzeug.security import generate_password_hash  # 生成哈希密码


# 定义生成日期时间的函数
def dt():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# 专门用于增删改查
class CRUD:
    # 验证用户唯一性，昵称1、邮箱2、手机3
    @staticmethod
    def user_unique(data, method=1):
        # 创建会话
        session = ORM.db()
        user = None
        # 事务处理的逻辑
        try:
            model = session.query(User)
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
            session.rollback()  # 如果发生异常直接回滚
        else:
            session.commit()  # 没有发生异常直接提交
        finally:
            session.close()  # 无论是否发生异常最后一定关闭会话
        if user:
            return True
        else:
            return False

    @staticmethod
    # 保存注册用户
    def save_regist_user(form):
        # 创建会话
        session = ORM.db()
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
            session.add(user)
        except Exception as e:
            session.rollback()
            return False
        else:
            session.commit()
            return True
        finally:
            session.close()

    # 登录验证
    @staticmethod
    def check_login(name, pwd):
        session = ORM.db()
        result = False
        try:
            user = session.query(User).filter_by(name=name).first()
            if user:
                if user.check_pwd(pwd):
                    result = True
        except Exception as e:
            session.rollback()
        else:
            session.commit()
        finally:
            session.close()
        return result

    # 保存用户信息
    @staticmethod
    def save_user(form):
        session = ORM.db()
        try:
            user = session.query(User).filter_by(id=int(form.data['id'])).first()
            user.name = form.data['name']
            user.email = form.data['email']
            user.phone = form.data['phone']
            user.sex = int(form.data['sex'])
            user.xingzuo = int(form.data['xingzuo'])
            user.face = form.data['face']
            user.info = form.data['info']
            user.updatedAt = dt()
            user.role = form.data['role']
            session.add(user)
            print(form.data['role'])
            print(user.role)
            print("!!!!!!!!!")
        except Exception as e:
            session.rollback()
        else:
            session.commit()
        finally:
            session.close()
        return True

    # 获取用户
    @staticmethod
    def user(name):
        session = ORM.db()
        user = None
        try:
            user = session.query(User).filter_by(name=name).first()
        except Exception as e:
            session.rollback()
        else:
            session.commit()
        finally:
            session.close()
        return user

    # 获取视频
    @staticmethod
    def video(id):
        session = ORM.db()
        video = None
        try:
            video = session.query(Video).filter_by(id=int(id)).first()
        except Exception as e:
            session.rollback()
        else:
            session.commit()
        finally:
            session.close()
        return video

    # 保存消息
    @staticmethod
    def save_msg(content):
        session = ORM.db()
        try:
            msg = Msg(
                content=content,
                createdAt=dt(),
                updatedAt=dt()
            )
            session.add(msg)
        except Exception as e:
            session.rollback()
        else:
            session.commit()
        finally:
            session.close()

    # 查询消息
    @staticmethod
    def new_msg():
        session = ORM.db()
        data = None
        try:
            data = session.query(Msg).order_by(Msg.createdAt.asc()).limit(200).all()
        except Exception as e:
            session.rollback()
        else:
            session.commit()
        finally:
            session.close()
        return data

    # 保存直播信息
    @staticmethod
    def save_stream(form):
        session = ORM.db()
        try:
            stream = Stream(
                title=form.data['title'],
                url=form.data['url'],
                createdAt=dt(),
                userid=form.data['userid']
            )
            session.add(stream)
        except Exception as e:
            session.rollback()
            return False
        else:
            session.commit()
            return True
        finally:
            session.close()

