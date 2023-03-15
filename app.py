from blueprints.chatroom import ChatRoomHandler
import tornado.ioloop
import tornado.web
from tornado.web import Application, FallbackHandler
from tornado.wsgi import WSGIContainer
import sockjs.tornado

from flask import Flask, session, g, request, redirect, render_template
import config
from blueprints.course import bp as course
from blueprints.build import bp as build
from blueprints.login import bp as login
from blueprints.logout import bp as logout
from blueprints.msg import bp as msg
from blueprints.myStream import bp as myStream
from blueprints.playchat import bp as playchat
from blueprints.regist import bp as regist
from blueprints.main import bp as main
from blueprints.stream import bp as stream
from blueprints.upload import bp as upload
from blueprints.userprofile import bp as userprofile
from blueprints.index import bp as index
from flask_migrate import Migrate
from flask_wtf import CSRFProtect

app = Flask(__name__)

# 阻止跨域请求
# CSRFProtect(app)
# 绑定配置文件
app.config.from_object(config)
app.debug=True

# 视图绑定
blueprint_list = [
    main, regist, login, userprofile, logout, upload, playchat,
    build, myStream, stream, msg, index, course
]
for cur_bp in blueprint_list:
    app.register_blueprint(cur_bp)

# before_request/ before_first_request/ after_request
# @app.before_request
# def is_login():
#     if request.path == "/login" or request.path == "/main":
#         return None
#     if not session.get("name", ''):
#         data = dict(
#             title="登录"
#         )
#         return render_template("login.html", data=data)

# html global var
# @app.context_processor
# def my_context_processor():
#     return {"user": g.user}

if __name__ == '__main__':
    # app.run()

    ChatRouter = sockjs.tornado.SockJSRouter(ChatRoomHandler, '/chatroom')
    wsgi_app = WSGIContainer(app)
    application = tornado.web.Application(
        ChatRouter.urls + [(r'.*', FallbackHandler, dict(fallback=wsgi_app))]
    )
    application.listen(8000)
    tornado.ioloop.IOLoop.instance().start()


