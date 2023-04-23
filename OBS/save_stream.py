
import sys
import datetime
import os

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

p1 = sys.argv[1]
p2 = sys.argv[2]

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
    print("Success!")
    print("Your url is "+"http://127.0.0.1:80/live?port=1935&app="+p1+"&stream="+p2)
finally:
    connect.close()

play = "ffplay http://127.0.0.1:80/live?port=1935&app=myapp&stream=video"
os.system(play)