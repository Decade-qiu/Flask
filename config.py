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
