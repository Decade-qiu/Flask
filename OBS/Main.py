import ctypes
import json
import sys, cv2
import threading
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from subprocess import run
import subprocess
import sys
import datetime
from tornado.websocket import WebSocketClientConnection
from tornado.httpclient import HTTPRequest
from tornado.websocket import websocket_connect
import os
os.environ['PYTHON_VLC_MODULE_PATH'] = "E://DeskTop//flask//OBS//VLC"
import time, vlc
from matplotlib import image
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column  # 定义字段
from sqlalchemy.dialects.mysql import *  # 导入字段类型
from werkzeug.security import check_password_hash  # 检查密码
from sqlalchemy.orm import declarative_base

Base = declarative_base()
class Msg(Base):
    __tablename__ = "msg"
    id = Column(BIGINT, primary_key=True)  # 编号
    content = Column(TEXT)  # 消息
    streamId = Column(INTEGER)
    createdAt = Column(DATETIME, nullable=False)  # 创建时间
    updatedAt = Column(DATETIME, nullable=False)  # 修改时间
class Stream(Base):
    __tablename__ = "stream"
    id = Column(INTEGER, primary_key=True)  # 编号
    title = Column(VARCHAR(20), nullable=False, unique=True)  #
    url = Column(VARCHAR(255), nullable=False)  #
    createdAt = Column(DATETIME, nullable=False)  # 创建时间
    userid = Column(VARCHAR(20), nullable=True)
    # updatedAt = Column(DATETIME, nullable=False)  # 修改时间
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
SECRET_KEY = "asdfasdfjasdfjasd;lf"
# 数据库的配置信息
HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'chatroom_project'
USERNAME = 'root'
PASSWORD = '123456'
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI
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
class Player:
    '''
        args:设置 options
    '''
    def __init__(self, *args):
        if args:
            instance = vlc.Instance(*args)
            self.media = instance.media_player_new()
        else:
            self.media = vlc.MediaPlayer()

    # 设置待播放的url地址或本地文件路径，每次调用都会重新加载资源
    def set_uri(self, uri):
        self.media.set_mrl(uri)

    # 播放 成功返回0，失败返回-1
    def play(self, path=None):
        if path:
            self.set_uri(path)
            return self.media.play()
        else:
            return self.media.play()

    # 暂停
    def pause(self):
        self.media.pause()

    # 恢复
    def resume(self):
        self.media.set_pause(0)

    # 停止
    def stop(self):
        self.media.stop()

    # 释放资源
    def release(self):
        return self.media.release()

    # 是否正在播放
    def is_playing(self):
        return self.media.is_playing()

    # 已播放时间，返回毫秒值
    def get_time(self):
        return self.media.get_time()

    # 拖动指定的毫秒值处播放。成功返回0，失败返回-1 (需要注意，只有当前多媒体格式或流媒体协议支持才会生效)
    def set_time(self, ms):
        return self.media.get_time()

    # 音视频总长度，返回毫秒值
    def get_length(self):
        return self.media.get_length()

    # 获取当前音量（0~100）
    def get_volume(self):
        return self.media.audio_get_volume()

    # 设置音量（0~100）
    def set_volume(self, volume):
        return self.media.audio_set_volume(volume)

    # 返回当前状态：正在播放；暂停中；其他
    def get_state(self):
        state = self.media.get_state()
        if state == vlc.State.Playing:
            return 1
        elif state == vlc.State.Paused:
            return 0
        else:
            return -1

    # 当前播放进度情况。返回0.0~1.0之间的浮点数
    def get_position(self):
        return self.media.get_position()

    # 拖动当前进度，传入0.0~1.0之间的浮点数(需要注意，只有当前多媒体格式或流媒体协议支持才会生效)
    def set_position(self, float_val):
        return self.media.set_position(float_val)

    # 获取当前文件播放速率
    def get_rate(self):
        return self.media.get_rate()

    # 设置播放速率（如：1.2，表示加速1.2倍播放）
    def set_rate(self, rate):
        return self.media.set_rate(rate)

    # 设置宽高比率（如"16:9","4:3"）
    def set_ratio(self, ratio):
        self.media.video_set_scale(0)  # 必须设置为0，否则无法修改屏幕宽高
        self.media.video_set_aspect_ratio(ratio)

    # 注册监听器
    def add_callback(self, event_type, callback):
        self.media.event_manager().event_attach(event_type, callback)

    # 移除监听器
    def remove_callback(self, event_type, callback):
        self.media.event_manager().event_detach(event_type, callback)
class OBS(QWidget):
    def __init__(self):
        super().__init__()
        self.player = None
        self.p = None
        # 设置窗口标题和大小
        self.setWindowTitle("OBS直播推流界面")
        self.resize(800*2.3, 600*2.3)
        # bg_image = QPixmap("./bg.png")
        self.setObjectName("Main")
        self.setStyleSheet("#Main{background-color:rgb(176, 196, 222);}")
        # 创建登录按钮
        self.login_button = QPushButton("登录")
        self.login_button.clicked.connect(self.on_login_button_clicked)
        # 创建视频预览区域
        self.preview_label = QLabel("视频预览区域")
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setStyleSheet("border: 1px solid black;")
        self.preview_label.setScaledContents(True)
        # 创建推流设置区域
        self.stream_settings_box = QVBoxLayout()
        self.stream_url_edit = QLineEdit()
        self.stream_url_edit.setPlaceholderText("推流应用名称")
        self.stream_settings_box.addWidget(self.stream_url_edit)
        self.stream_key_edit = QLineEdit()
        self.stream_key_edit.setPlaceholderText("推流密钥")
        self.stream_settings_box.addWidget(self.stream_key_edit)
        # 创建推流来源选择框
        self.stream_source_combo = QComboBox()
        self.stream_source_combo.addItem("摄像头")
        self.stream_source_combo.addItem("桌面")
        self.stream_settings_box.addWidget(self.stream_source_combo)
        # 创建开始
        self.start_stop_button = QPushButton("开始")
        self.start_stop_button.setFixedWidth(100)
        self.start_stop_button.clicked.connect(self.on_start_stop_button_clicked)
        # 创建停止 跟开始按钮在一行
        self.stop_button = QPushButton("停止")
        self.stop_button.setFixedWidth(100)
        self.stop_button.clicked.connect(self.on_stop_button_clicked)
        # 创建顶部布局，包含登录按钮和标题
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.login_button)
        top_layout.addStretch()
        top_layout.addWidget(QLabel("OBS直播推流界面"))
        top_layout.addStretch()
        # 创建主布局和分裂器
        main_layout = QVBoxLayout()
        main_layout.addLayout(top_layout)
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter, 8)
        # 将视频预览标签添加到分裂器的左侧
        video_widget = QWidget()
        video_layout = QVBoxLayout()
        video_layout.addWidget(self.preview_label)
        video_widget.setLayout(video_layout)
        splitter.addWidget(video_widget)
        # 将弹幕聊天窗口添加到分裂器的右侧
        self.chat_edit = QTextEdit()
        self.chat_edit.setReadOnly(True)  # 禁止编辑
        self.chat_edit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        # 修改聊天窗口颜色为灰色
        self.chat_edit.setStyleSheet("background-color: #F2F2F2;")
        chat_widget = QWidget()
        chat_layout = QVBoxLayout()
        chat_layout.addWidget(self.chat_edit)
        chat_widget.setLayout(chat_layout)
        splitter.addWidget(chat_widget)
        # 设置聊天区大小为视频区的1/3
        splitter.setSizes([self.width() * 2 / 3, self.width() / 3])
        main_layout.addLayout(self.stream_settings_box)
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.start_stop_button)
        button_layout.addWidget(self.stop_button)
        self.button_frame = QFrame(self)
        self.button_frame.setLayout(button_layout)
        main_layout.addWidget(self.button_frame)
        self.setLayout(main_layout)
    def on_login_button_clicked(self):
        # 创建登录对话框，让用户输入用户名和密码
        dialog = QDialog()
        form = QFormLayout(dialog)
        # 设置form大小 标题
        dialog.setWindowTitle("登录")
        dialog.resize(300*2, 100*2)
        username_edit = QLineEdit()
        username_edit.setPlaceholderText("用户名")
        form.addRow("用户名：", username_edit)
        password_edit = QLineEdit()
        password_edit.setEchoMode(QLineEdit.Password)
        password_edit.setPlaceholderText("密码")
        form.addRow("密码：", password_edit)
        # 添加OK和Cancel按钮
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, dialog)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        form.addRow(buttons)
        # 显示登录对话框
        if dialog.exec_() == QDialog.Accepted:
            # 获取用户输入的用户名和密码
            username = username_edit.text()
            password = password_edit.text()
            # 检查用户名和密码是否正确
            session = ORM.db()
            user = session.query(User).filter(User.name == username).first()
            if user is None:
                QMessageBox.warning(self, "登录", "用户名不存在！")
                return
            if not check_password_hash(user.pwd, password):
                QMessageBox.warning(self, "登录", "密码错误！")
                return
            # 登录成功
            QMessageBox.information(self, "登录", "登录成功！")
            self.login_button.setText(username)
    def on_stop_button_clicked(self):
        self.player.stop()
        self.player = None
        self.start_stop_button.setText("开始")
        self.timer = None
        self.chat_edit.clear()
    def on_start_stop_button_clicked(self):
        # 获取推流地址和密钥
        stream_url = self.stream_url_edit.text()
        stream_key = self.stream_key_edit.text()
        if not stream_url or not stream_key:
            QMessageBox.warning(self, "推流设置", "推流地址或密钥不能为空！")
            return
        if not stream_url or not stream_key:
            QMessageBox.warning(self, "推流设置", "推流地址或密钥不能为空！")
            return
        if self.player != None:
            if self.player.get_state() == 1:
                self.player.pause()
                self.start_stop_button.setText("开始")
            if self.player.get_state() == 0:
                self.player.play()
                self.start_stop_button.setText("暂停")
            return
        connect = ORM.db()
        try:
            stream = Stream(
                title=stream_url,
                url="http://127.0.0.1:80/live?port=1935&app="+stream_url+"&stream="+stream_key,
                createdAt=dt(),
                userid="decade"
            )
            connect.add(stream)
        except Exception as e:
            connect.rollback()
            QMessageBox.information(self, "ERROR", "创建失败！")
        else:
            connect.commit()
            QMessageBox.information(self, "Sucess", "你的推流地址为\n"+"http://127.0.0.1:80/live?port=1935&app="+stream_url+"&stream="+stream_key)
        finally:
            connect.close()
        self.url = r'ffmpeg -f dshow -i video="@device_pnp_\\?\usb#vid_04f2&pid_b67c&mi_00#6&26fcf372&1&0000#{65e8773d-8f56-11d0-a3b9-00a0c9223196}\global" -f dshow -i audio="@device_cm_{33D9A762-90C8-11D0-BD43-00A0C911CE86}\wave_{4AEC28D7-6B71-40EA-9CE2-8BED96C1541C}" -r 30 -vcodec libx264 -preset:v ultrafast -tune:v zerolatency -f flv -bufsize 100k rtmp://127.0.0.1:1935/'+stream_url+'/'+stream_key
        print("********正在推流!********")
        if self.stream_source_combo.currentText() != "摄像头":
            self.url = r'ffmpeg -f gdigrab -i desktop -r 30 -vcodec libx264 -preset:v ultrafast -tune:v zerolatency -f flv -bufsize 100k rtmp://127.0.0.1:1935/'+stream_url+'/'+stream_key
        self.th = threading.Thread(target=self.Display)
        self.th.start()
        print(self.url)
        stream_url = "rtmp://127.0.0.1:1935/"+stream_url+"/"+stream_key
        self.player = Player()
        self.player.media.set_hwnd(self.preview_label.winId())
        self.player.play(stream_url)
        self.start_stop_button.setText("暂停")
        # 创建定时器，每隔1秒钟执行一次读取数据库操作
        self.timer = QTimer()
        self.timer.timeout.connect(self.read_from_database)
        self.timer.start(1000)  # 1秒钟
    def Display(self):
        subprocess.Popen(self.url, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    def insert_message(self, message, color):
        self.chat_edit.append('<span style="color:{};">{}</span><br>'.format(color, message))
    def read_from_database(self):
        # 从数据库读取聊天记录
        session = ORM.db()
        chat_records = session.query(Msg).all()
        # 将聊天记录显示到聊天区
        session.close()
        self.chat_edit.clear()
        for chat_record in chat_records:
            data = json.loads(chat_record.content)
            self.insert_message(data['name'] + "["+str(chat_record.createdAt)+"]"+": ", 'blue')
            self.insert_message(data['content'], 'red')



if __name__ == '__main__':
    app = QApplication(sys.argv)
    obs = OBS()
    obs.show()
    sys.exit(app.exec_())