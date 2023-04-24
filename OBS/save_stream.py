import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy, QFrame, QStackedLayout
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget

class Player(QMainWindow):
    def __init__(self):
        super().__init__()

        # 创建Qt窗口
        self.setWindowTitle('RTMP Player')
        self.setGeometry(100, 100, 800, 600)

        # 创建QMediaPlayer和QVideoWidget实例
        self.media_player = QMediaPlayer(self)
        self.video_widget = QVideoWidget(self)

        # 设置QVideoWidget的大小策略
        self.video_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # 创建垂直布局和水平布局
        vertical_layout = QVBoxLayout()
        horizontal_layout = QHBoxLayout()

        # 将QVideoWidget添加到水平布局中
        horizontal_layout.addWidget(self.video_widget)

        # 创建QFrame并将其添加到垂直布局中
        frame = QFrame(self)
        frame.setLayout(horizontal_layout)
        vertical_layout.addWidget(frame)

        # 创建QWidget并将垂直布局设置为其布局
        widget = QWidget(self)
        widget.setLayout(vertical_layout)
        self.setCentralWidget(widget)

        # 设置QMediaPlayer的媒体内容
        media_url = QUrl("rtmp://localhost:1935/myapp/video")
        media_content = QMediaContent(media_url)
        self.media_player.setMedia(media_content)

        # 设置QMediaPlayer的视频输出
        self.media_player.setVideoOutput(self.video_widget)

        # 播放视频
        self.media_player.play()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = Player()
    player.show()
    sys.exit(app.exec_())