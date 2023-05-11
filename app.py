import datetime
from blueprints.conn import bp as conn
from blueprints.discuss import bp as discuss
from blueprints.sockjs import ChatRoomHandler,CanvasConnection as BoardHandler, AudioHandler, checkHandler
import tornado.ioloop
import tornado.web
from tornado.web import Application, FallbackHandler
from tornado.wsgi import WSGIContainer
import sockjs.tornado
import sockjs
import config
from flask import Flask, session, g, request, redirect, render_template, url_for
from flask_sockets import Sockets
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
from blueprints.renmark import bp as renmark
from flask_migrate import Migrate
from flask_wtf import CSRFProtect
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config.from_object(config)
app.debug=True
# 视图绑定
blueprint_list = [
    main, regist, login, userprofile, logout, upload, playchat,
    build, myStream, stream, msg, index, course, dm, test, service,
    hhelp, screen, renmark, conn, discuss
]
for cur_bp in blueprint_list:
    app.register_blueprint(cur_bp)



if __name__ == '__main__':
    IP = '127.0.0.1' if 1 else '10.70.43.81'
    # app.run(host=IP, port=8000)
    ChatRouter = sockjs.tornado.SockJSRouter(ChatRoomHandler, '/chatroom')
    BoardRouter = sockjs.tornado.SockJSRouter(BoardHandler, '/board')
    AudioRouter = sockjs.tornado.SockJSRouter(AudioHandler, '/audio')
    checkRouter = sockjs.tornado.SockJSRouter(checkHandler, '/check')
    wsgi_app = WSGIContainer(app)
    application = tornado.web.Application(
        ChatRouter.urls + BoardRouter.urls + AudioRouter.urls + checkRouter.urls +[(r'.*', FallbackHandler, dict(fallback=wsgi_app))]
    )
    application.listen(8000, address=IP)
    tornado.ioloop.IOLoop.instance().start()


