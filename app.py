from blueprints.chatroom import ChatRoomHandler
import tornado.ioloop
import tornado.web
from tornado.web import Application, FallbackHandler
from tornado.wsgi import WSGIContainer
import sockjs.tornado
import config
from flask import Flask, session, g, request, redirect, render_template, url_for
from blueprints.screen import bp as screen
from blueprints.dm import bp as dm
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
from blueprints.complaint import bp as test
from blueprints.service import bp as service
from blueprints.help import bp as hhelp
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
    build, myStream, stream, msg, index, course, dm, test, service,
    hhelp, screen
]
for cur_bp in blueprint_list:
    app.register_blueprint(cur_bp)


if __name__ == '__main__':
    IP = '127.0.0.1' if 0 else '10.70.64.143'
    # app.run(host=IP, port=8000)
    ChatRouter = sockjs.tornado.SockJSRouter(ChatRoomHandler, '/chatroom')
    wsgi_app = WSGIContainer(app)
    application = tornado.web.Application(
        ChatRouter.urls + [(r'.*', FallbackHandler, dict(fallback=wsgi_app))]
    )
    application.listen(8000, address=IP)
    tornado.ioloop.IOLoop.instance().start()


