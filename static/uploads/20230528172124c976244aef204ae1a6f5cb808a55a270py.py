
from subprocess import run
import subprocess
import sys
import datetime
import os
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy import Column  # 定义字段
from sqlalchemy.dialects.mysql import *  # 导入字段类型
from werkzeug.security import check_password_hash  # 检查密码
from sqlalchemy.orm import declarative_base
Base = declarative_base()

class Stream(Base):
    __tablename__ = "stream"
    id = Column(INTEGER, primary_key=True)  # 编号
    title = Column(VARCHAR(20), nullable=False, unique=True)  #
    url = Column(VARCHAR(255), nullable=False)  #
    createdAt = Column(DATETIME, nullable=False)  # 创建时间
    userid = Column(VARCHAR(20), nullable=True)
    # updatedAt = Column(DATETIME, nullable=False)  # 修改时间

SECRET_KEY = "asdfasdfjasdfjasd;lf"

# 数据库的配置信息
HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'chatroom_project'
USERNAME = 'root'
PASSWORD = '123456'
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI


# redis主机、端口、库
redis_configs = dict(
    host="localhost",
    port=6379,
    db=0
)

# 邮箱配置
MAIL_SERVER = "smtp.qq.com"
MAIL_USE_SSL = True
MAIL_PORT = 465
MAIL_USERNAME = "3622739389@qq.com"
MAIL_PASSWORD = "aguyecxruwelcjgb"
MAIL_DEFAULT_SENDER = "3622739389@qq.com"

def dt():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

class ORM:
    @classmethod
    def db(cls):
        link = DB_URI
        # 创建连接引擎，encoding编码，echo是[True]否[False]输出日志
        engine = create_engine(
            link,
            echo=False,
            pool_size=100,
            pool_recycle=10,
            connect_args={'charset': "utf8"}
        )
        # 创建用于操作数据表的会话
        Session = sessionmaker(
            bind=engine,
            autocommit=False,
            autoflush=True,
            expire_on_commit=False
        )
        # autocommit，自动提交，True[开启]，False[关闭]，采用手动的方式，自己写事务处理的逻辑
        # autoflush，自动刷新权限，True[开启]
        return Session()
    
p3 = input("请输入你的用户名：")
p4 = input("请输入你的密码：")

print("=========登陆成功=========")

p1 = input("请输入你的频道名：")
p2 = input("请输入你的流名：")

connect = ORM.db()
try:
    stream = Stream(
        title=p1,
        url="http://127.0.0.1:80/live?port=1935&app="+p1+"&stream="+p2,
        createdAt=dt(),
        userid="decade"
    )
    connect.add(stream)
except Exception as e:
    connect.rollback()
    print("Failed!")
else:
    connect.commit()
    print("********Success create!********")
    print("Your strem url is "+"http://127.0.0.1:80/live?port=1935&app="+p1+"&stream="+p2)
finally:
    connect.close()

url = r'ffmpeg -f dshow -i video="@device_pnp_\\?\usb#vid_04f2&pid_b67c&mi_00#6&26fcf372&1&0000#{65e8773d-8f56-11d0-a3b9-00a0c9223196}\global" -f dshow -i audio="@device_cm_{33D9A762-90C8-11D0-BD43-00A0C911CE86}\wave_{4AEC28D7-6B71-40EA-9CE2-8BED96C1541C}" -r 30 -vcodec libx264 -preset:v ultrafast -tune:v zerolatency -f flv -bufsize 100k rtmp://127.0.0.1:1935/'+p1+'/'+p2
print("********正在推流!********")
p = subprocess.Popen(url, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
print("********推流成功!********")
print("是否开始播放？(y/n)")
ff = input()
if ff == "y":
    print("等待播放器中...")
    play = "ffplay rtmp://127.0.0.1:1935/"+p1+'/'+p2
    subprocess.Popen(play, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print("********播放成功!********")
p.communicate()
