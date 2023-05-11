
from sqlalchemy import Column  # 定义字段
from sqlalchemy.dialects.mysql import *  # 导入字段类型
from werkzeug.security import check_password_hash  # 检查密码
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()
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
    streamId = Column(INTEGER)
    createdAt = Column(DATETIME, nullable=False)  # 创建时间
    updatedAt = Column(DATETIME, nullable=False)  # 修改时间

class Post(Base):
    __tablename__ = "post"
    id = Column(BIGINT, primary_key=True)  # 编号
    content = Column(TEXT)  # 消息
    createdAt = Column(DATETIME, nullable=False)  # 创建时间
    comment = Column(TEXT)  

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
    cktAt = Column(DATETIME, nullable=False)  # 修改时间
    pwd = Column(INTEGER, nullable=False)  
    mute = Column(INTEGER, nullable=False)  # 编号

class Check(Base):
    __tablename__ = "check"
    id = Column(INTEGER, primary_key=True)  # 编号
    key = Column(INTEGER, nullable=False, unique=True)  
    name = Column(VARCHAR(20), nullable=False, unique=True) 
    ckt = Column(DATETIME, nullable=False)  # 修改时间

