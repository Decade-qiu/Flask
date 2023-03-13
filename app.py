from flask import Flask, session, g
import config

from blueprints.login import bp as login
from blueprints.logout import bp as logout
from blueprints.regist import bp as regist
from blueprints.main import bp as main
from blueprints.upload import bp as upload
from blueprints.userprofile import bp as userprofile

from exts import db, mail
from flask_migrate import Migrate
from flask_wtf import CSRFProtect

app = Flask(__name__)

# 阻止跨域请求
# CSRFProtect(app)
# 绑定配置文件
app.config.from_object(config)

db.init_app(app)
mail.init_app(app)
migrate = Migrate(app, db)

# 视图绑定
# app.register_blueprint(qa_bp)
# app.register_blueprint(auth_bp)
app.register_blueprint(main)
app.register_blueprint(regist)
app.register_blueprint(login)
app.register_blueprint(userprofile)
app.register_blueprint(logout)
app.register_blueprint(upload)

# flask db init：只需要执行一次
# flask db migrate：将orm模型生成迁移脚本
# flask db upgrade：将迁移脚本映射到数据库中

# before_request/ before_first_request/ after_request
# hook
# @app.before_request
# def my_before_request():
#     user_id = session.get("user_id")
#     if user_id:
#         user = User.query.get(user_id)
#         setattr(g, "user", user)
#     else:
#         setattr(g, "user", None)

#
# @app.context_processor
# def my_context_processor():
#     return {"user": g.user}


if __name__ == '__main__':
    app.debug=True
    app.run()
