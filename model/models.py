from exts import db
from sqlalchemy import Column  # 定义字段
from sqlalchemy.dialects.mysql import *  # 导入字段类型
from werkzeug.security import check_password_hash  # 检查密码
from datetime import datetime

Base = db.Model
# Column = db.Column
# INTEGER = db.Integer
# DATETIME = db.DateTime
# TEXT = db.Text
# VARCHAR = db.String

# 定义视频数据模型
class Video(Base):
    __tablename__ = "video"  # 定义数据表的名称
    id = Column(INTEGER, primary_key=True)  # 编号
    name = Column(VARCHAR(255), nullable=False)
    url = Column(VARCHAR(255), nullable=False)
    logo = Column(VARCHAR(255), nullable=False)
    createdAt = Column(DATETIME, nullable=False)  # 创建时间
    updatedAt = Column(DATETIME, nullable=False)  # 修改时间


# 定义聊天数据模型
class Msg(Base):
    __tablename__ = "msg"
    id = Column(BIGINT, primary_key=True)  # 编号
    content = Column(TEXT)  # 消息
    createdAt = Column(DATETIME, nullable=False)  # 创建时间
    updatedAt = Column(DATETIME, nullable=False)  # 修改时间


class User(Base):
    __tablename__ = "user"
    id = Column(INTEGER, primary_key=True)  # 编号
    name = Column(VARCHAR(20), nullable=False, unique=True)  # 昵称
    pwd = Column(VARCHAR(255), nullable=False)  #
    role = Column(VARCHAR(255), nullable=False)  #
    email = Column(VARCHAR(100), nullable=False, unique=True)  #
    phone = Column(VARCHAR(11), nullable=False, unique=True)  #
    sex = Column(TINYINT, nullable=True)  # 性别
    xingzuo = Column(TINYINT, nullable=True)  #
    face = Column(VARCHAR(100), nullable=True)  #
    info = Column(VARCHAR(600), nullable=True)  # 个性签名
    createdAt = Column(DATETIME, nullable=False)  # 创建时间
    updatedAt = Column(DATETIME, nullable=False)  # 修改时间

    def check_pwd(self, pwd):
        return check_password_hash(self.pwd, pwd)

class Stream(Base):
    __tablename__ = "stream"
    id = Column(INTEGER, primary_key=True)  # 编号
    title = Column(VARCHAR(20), nullable=False, unique=True)  #
    url = Column(VARCHAR(255), nullable=False)  #
    createdAt = Column(DATETIME, nullable=False)  # 创建时间
    userid = Column(VARCHAR(20), nullable=True)
    # updatedAt = Column(DATETIME, nullable=False)  # 修改时间


# class UserModel(db.Model):
#     __tablename__ = "user"
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     username = db.Column(db.String(100), nullable=False)
#     password = db.Column(db.String(200), nullable=False)
#     email = db.Column(db.String(100), nullable=False, unique=True)
#     join_time = db.Column(db.DateTime, default=datetime.now)
#
#
# class EmailCaptchaModel(db.Model):
#     __tablename__ = "email_captcha"
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     email = db.Column(db.String(100), nullable=False)
#     captcha = db.Column(db.String(100), nullable=False)
#
#
# class QuestionModel(db.Model):
#     __tablename__ = "question"
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     title = db.Column(db.String(100), nullable=False)
#     content = db.Column(db.Text, nullable=False)
#     create_time = db.Column(db.DateTime, default=datetime.now)
#
#     # 外键
#     author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
#     author = db.relationship(UserModel, backref="questions")
#
#
# class AnswerModel(db.Model):
#     __tablename__ = "answer"
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     content = db.Column(db.Text, nullable=False)
#     create_time = db.Column(db.DateTime, default=datetime.now)
#
#     # 外键
#     question_id = db.Column(db.Integer, db.ForeignKey("question.id"))
#     author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
#
#     # 关系
#     question = db.relationship(QuestionModel, backref=db.backref("answers", order_by=create_time.desc()))
#     author = db.relationship(UserModel, backref="answers")