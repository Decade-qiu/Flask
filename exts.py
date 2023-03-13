# exts.py：这个文件存在的意义就是为了解决循环引用的问题

# flask-sqlalchemy
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

db = SQLAlchemy()
mail = Mail()
