import datetime, json, os, signal, subprocess, sys, threading, psutil, wx,av
import wx.html2 as html2
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import *
from PyQt5.QtChart import *
os.environ['PYTHON_VLC_MODULE_PATH'] = "E://DeskTop//flask//OBS//VLC"
import vlc, mss, time
from sqlalchemy import *
from sqlalchemy.dialects.mysql import *
from sqlalchemy.orm import *
from werkzeug.security import check_password_hash

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
    cktAt = Column(DATETIME, nullable=False)  # 修改时间
    pwd = Column(INTEGER, nullable=False)  
    mute = Column(INTEGER, nullable=False)  # 编号
class Check(Base):
    __tablename__ = "check"
    id = Column(INTEGER, primary_key=True)  # 编号
    key = Column(INTEGER, nullable=False, unique=True)  
    name = Column(VARCHAR(20), nullable=False, unique=True) 
    ckt = Column(DATETIME, nullable=False)  # 修改时间
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
class Course(Base):
    __tablename__ = "course"
    id = Column(INTEGER, primary_key=True)  # 编号
    title = Column(VARCHAR(20), nullable=False)  #
    content = Column(TEXT)  # 消息
    createdAt = Column(DATETIME, nullable=False)  # 创建时间
    face = Column(VARCHAR(100), nullable=True) 
    own = Column(VARCHAR(20), nullable=False, unique=True)  # 昵称
    streamid = Column(INTEGER)
class Mic(Base):
    __tablename__ = "mic"
    id = Column(INTEGER, primary_key=True)  # 编号
    streamid = Column(INTEGER)
    name = Column(VARCHAR(20))  # 昵称
    status = Column(INTEGER, nullable=False)  # 编号
    createdAt = Column(DATETIME, nullable=False)  # 创建时间
SECRET_KEY = "asdfasdfjasdfjasd;lf"
HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'chatroom_project'
USERNAME = 'root'
PASSWORD = '123456'
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI
class MainWindow(wx.Frame):
    def __init__(self):
        super().__init__(None, title='White Board')
        self.webview = html2.WebView.New(self)
        self.webview.LoadURL('http://localhost:8000/screenShare/')
        self.SetClientSize((800*2, 600*2)) 
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.webview, 1, wx.EXPAND)
        self.SetSizer(sizer)
def dt():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
class ORM:
    @classmethod
    def db(cls):
        link = DB_URI
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
        self.chart_dialog = None
        self.key = 1
        # 设置窗口标题和大小
        self.setWindowTitle("OBS直播推流界面")
        self.resize(800*2.3, 600*2.3)
        self.setObjectName("Main")
        self.setStyleSheet("#Main{background-color:rgb(176, 196, 222);}")
        # 创建登录按钮
        self.login_button = QPushButton("登录")
        self.login_button.clicked.connect(self.on_login_button_clicked)
        # 创建画板按钮并连接槽函数
        self.draw_button = QPushButton("画板")
        self.draw_button.clicked.connect(self.on_draw_button_clicked)
        # 创建签到按钮并连接槽函数
        self.checkin_button = QPushButton("签到")
        self.checkin_button.clicked.connect(self.on_checkin_button_clicked)
        # 创建在人数按钮并连接槽函数
        self.online_button = QPushButton("在线学生")
        self.online_button.clicked.connect(self.on_online_button_clicked)
        # 创建全员静音按钮并连接槽函数
        self.mute_all_button = QPushButton("全员静音")
        self.mute_all_button.clicked.connect(self.on_mute_all_button_clicked)
        # 录屏
        self.record_button = QPushButton("录制屏幕")
        self.record_button.clicked.connect(self.record_screen)
        # 创建视频预览区域
        self.preview_label = QLabel("视频预览区域")
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setStyleSheet("border: 1px solid black;")
        self.preview_label.setScaledContents(True)
        # 创建推流设置区域
        self.stream_settings_box = QVBoxLayout()
        self.stream_url_edit = QLineEdit()
        self.stream_url_edit.setPlaceholderText("推流应用名称")
        self.stream_url_edit.setText("myapp")
        self.stream_settings_box.addWidget(self.stream_url_edit)
        self.stream_key_edit = QLineEdit()
        self.stream_key_edit.setPlaceholderText("推流密钥")
        self.stream_settings_box.addWidget(self.stream_key_edit)
        # 创建课程选择框
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
        top_layout.addWidget(self.draw_button)
        top_layout.addWidget(self.checkin_button)
        top_layout.addWidget(self.online_button)
        top_layout.addWidget(self.mute_all_button)
        top_layout.addWidget(self.record_button)
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
            self.course_combo = QComboBox()
            connect = ORM.db()
            try:
                courses = connect.query(Course).filter(Course.own == self.login_button.text()).order_by(Course.createdAt.desc())
                print(self.login_button.text())
                for course in courses:
                    print(course.title)
                    self.course_combo.addItem(course.title)
            except Exception as e:
                connect.rollback()
                print(e)
            else:
                connect.commit()
            finally:
                connect.close()
            self.stream_settings_box.addWidget(self.course_combo)
    def kill_ffmpeg(self):
        connections = psutil.net_connections(kind='tcp')
        for conn in connections:
            if conn.status == psutil.CONN_ESTABLISHED and conn.laddr.port == 1935:
                os.kill(conn.pid, signal.SIGTERM)
                break
    def on_stop_button_clicked(self):
        self.start_stop_button.setText("开始")
        if self.player != None: self.player.stop()
        self.player = None
        self.timer = None
        self.chat_edit.clear()
        self.kill_ffmpeg()
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
                title=stream_key,
                url='rtmp://127.0.0.1:1935/'+stream_url+'/'+stream_key,
                createdAt=dt(),
                userid="decade",
                mute = 0,
            )
            connect.add(stream)
        except Exception as e:
            connect.rollback()
            QMessageBox.information(self, "ERROR", "创建失败！")
        else:
            connect.commit()
            self.key = connect.query(Stream).filter(Stream.title == stream_key).order_by(Stream.createdAt.desc()).first().id
            QMessageBox.information(self, "Sucess", "你的推流地址为\n"+'rtmp://127.0.0.1:1935/myapp/'+stream_key+" id ="+str(self.key))
        finally:
            connect.close()
        session = ORM.db()
        sss = session.query(Stream).filter(Stream.title == self.stream_key_edit.text()).first()
        self.streamid = sss.id
        session.commit()
        session.close()
        session = ORM.db()
        cou = session.query(Course).filter(Course.title==self.course_combo.currentText()).update({Course.streamid:self.streamid})
        print(self.streamid)
        print(cou)
        session.commit()
        session.close()
        self.url = r'ffmpeg -f dshow -i video="@device_pnp_\\?\usb#vid_04f2&pid_b67c&mi_00#6&26fcf372&1&0000#{65e8773d-8f56-11d0-a3b9-00a0c9223196}\global" -f dshow -i audio="@device_cm_{33D9A762-90C8-11D0-BD43-00A0C911CE86}\wave_{4D3E6045-E4F5-48E3-9474-54421A73A77B}" -r 30 -vcodec libx264 -preset:v ultrafast -tune:v zerolatency -f flv -bufsize 100k rtmp://127.0.0.1:1935/myapp/'+stream_key
        print("********正在推流!********")
        if self.stream_source_combo.currentText() != "摄像头":
            self.url = r'ffmpeg -f gdigrab -i desktop -r 30 -vcodec libx264 -preset:v ultrafast -tune:v zerolatency -f flv -bufsize 100k rtmp://127.0.0.1:1935/myapp/'+stream_key
        self.th = threading.Thread(target=self.Display)
        self.th.start()
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
    def on_draw_button_clicked(self):
        app = wx.App()
        window = MainWindow()
        window.Show()
        app.MainLoop()
    def show_checkin_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("签到设置")
        dialog.setFixedSize(700, 200)
        form = QFormLayout(dialog)
        time_edit = QLineEdit()
        form.addRow("签到时限（分钟）：", time_edit)
        password_edit = QLineEdit()
        password_edit.setEchoMode(QLineEdit.Password)
        form.addRow("签到口令码：", password_edit)
        type_combo = QComboBox()
        type_combo.addItem("限时签到")
        type_combo.addItem("不限时签到")
        form.addRow("签到类型：", type_combo)
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, dialog)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        form.addRow(button_box)
        time_edit.setMinimumWidth(200)
        password_edit.setMinimumWidth(200)
        type_combo.setMinimumWidth(200)
        if dialog.exec_() == QDialog.Accepted:
            time_limit = int(time_edit.text())
            password = password_edit.text()
            session = ORM.db()
            stream = session.query(Stream).filter(Stream.id==self.key).first()
            stream.cktAt = (datetime.datetime.now()+datetime.timedelta(minutes=time_limit)).strftime("%Y-%m-%d %H:%M:%S")
            stream.pwd = int(password)
            session.commit()
            session.close()
            self.show_chart_dialog()
    def show_chart_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("签到统计")
        dialog.setFixedSize(400, 300)
        chart = QChart()
        chart.setTitle("签到统计")
        series = QPieSeries()
        series.append("已签到", 50)
        series.append("未签到", 50)
        chart.addSeries(series)
        chart.legend().hide()
        chartview = QChartView(chart, dialog)
        chartview.setRenderHint(QPainter.Antialiasing)
        chartview.setGeometry(20, 20, 360, 260)
        dialog.exec_()
        self.chart_dialog = dialog 
    def on_checkin_button_clicked(self):
        if self.chart_dialog is not None:
            self.chart_dialog.show()
        else:
            self.show_checkin_dialog()
    def on_online_button_clicked(self):
        # 获取当前在线学生的人数和昵称
        online_students = ["小明", "小红", "小刚"]
        online_status = [1, 1, 1]
        session = ORM.db()
        stream = session.query(Stream).filter(Stream.id==self.key).first()
        time = stream.cktAt
        persons = session.query(Check).filter(Check.key == self.key).all()
        course = session.query(Course).filter_by(title=self.course_combo.currentText()).order_by(Course.createdAt.desc()).first()
        session.close()
        ac_stu = json.loads(course.content)['name'].split()
        for sss in ac_stu:
            online_students.append(sss)
            online_status.append(-1)
        for person in persons:
            if person.name not in online_students:
                online_students.append(person.name)
                st = 1
                if person.ckt > time:
                    st = 0
                online_status.append(st)
            else:
                index = online_students.index(person.name)
                online_status[index] = 1
                if person.ckt > time: 
                    online_status[index] = 0
        session = ORM.db()
        mic = session.query(Mic).filter(Mic.streamid==self.key).all()
        mic_on = [mic for i in mic if i.status == 1]
        session.close()
        # 创建多行文本框和滚动区域
        widget = QWidget()
        layout = QVBoxLayout(widget)
        self.student_layouts = []
        for student, status in sorted(zip(online_students, online_status), key=lambda x: x[1], reverse=True):
            student_label = QLabel(student)
            font = QFont()
            font.setPointSize(25)  # 设置学生姓名的字体大小
            student_label.setFont(font)
            online_label = QLabel()
            online_label.setFixedSize(50, 50)  # 调整旁边圆圈的大小
            online_pixmap = QPixmap(25, 25)
            col = "green"
            if status == -1:
                col = "red"
            elif status == 0:
                col = "yellow"
            online_pixmap.fill(QColor(col))
            painter = QPainter(online_pixmap)
            painter.setBrush(QBrush(QColor("white")))
            painter.drawEllipse(2, 2, 12, 12)
            painter.end()
            online_label.setPixmap(online_pixmap)
            student_layout = QHBoxLayout()
            student_layout.addWidget(student_label)
            student_layout.addWidget(online_label)
            # 添加开麦按钮并连接槽函数
            mic_button = QPushButton()
            mic_button.setFixedSize(50, 25)  # 设置按钮大小
            if student in mic_on:
                mic_button.setText("闭麦")
                mic_button.setStyleSheet("background-color: green; color: white")
            else:
                mic_button.setText("开麦")
                mic_button.setStyleSheet("background-color: gray; color: black")
            print(student)
            mic_button.clicked.connect(lambda _, s=student: self.turn_on_microphone(s))
            student_layout.addWidget(mic_button)
            self.student_layouts.append(student_layout)
        students_layout = QVBoxLayout()
        for student_layout in self.student_layouts:
            students_layout.addLayout(student_layout)
        layout.addLayout(students_layout)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(widget)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFixedSize(400, 500)
        # 显示多行文本框和滚动区域
        self.scroll_area.show()
    def on_mute_all_button_clicked(self):
        session = ORM.db()
        stream = session.query(Stream).filter(Stream.id==self.key).first()
        stream.mute = 1-stream.mute
        session.commit()
        session.close()
        if self.mute_all_button.text() == "全员静音":
            self.mute_all_button.setText("全员开启")
        else:
            self.mute_all_button.setText("全员静音")
    def turn_on_microphone(self, name):
        session = ORM.db()
        mics = session.query(Mic).filter(and_(Mic.streamid==self.key,
                Mic.name==name)).order_by(Mic.createdAt.desc()).first()
        if mics == None:
            mics = Mic(
                streamid=self.key,
                name=name,
                createdAt=dt(),
                status=1
            )
            session.add(mics)
            for layout in self.student_layouts:
                label = layout.itemAt(0).widget()
                button = layout.itemAt(2).widget()
                if label.text() == name:
                    button.setText("闭麦")
                    button.setStyleSheet("background-color: green; color: white")
                    break
        else:
            mics.status = 1-mics.status
            for layout in self.student_layouts:
                label = layout.itemAt(0).widget()
                button = layout.itemAt(2).widget()
                if label.text() == name:
                    if mics.status == 0:
                        button.setText("开麦")
                        button.setStyleSheet("background-color: gray; color: black")
                        break
                    else:
                        button.setText("闭麦")
                        button.setStyleSheet("background-color: green; color: white")
                        break
        session.commit()
        session.close()
        print(name)
    def record_screen(self):
        import subprocess
        cmd = ['python', 'OBS\saveVideo.py']
        subprocess.Popen(cmd)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    obs = OBS()
    obs.show()
    sys.exit(app.exec_())