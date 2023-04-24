import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *


class LoginDialog(QWidget):

    def __init__(self):
        super().__init__()

        # 设置窗口标题和大小
        self.setWindowTitle("Login")
        self.resize(400, 300)

        # 创建表单布局和控件
        form_layout = QFormLayout()
        username_edit = QLineEdit()
        password_edit = QLineEdit()
        password_edit.setEchoMode(QLineEdit.Password)
        form_layout.addRow("Username:", username_edit)
        form_layout.addRow("Password:", password_edit)

        # 创建OK和Cancel按钮
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        form_layout.addRow(buttons)

        # 设置主布局
        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        self.setLayout(main_layout)

    def sizeHint(self):
        return self.minimumSizeHint()

class OBS(QWidget):

    def __init__(self):
        super().__init__()

        # 设置窗口标题和大小
        self.setWindowTitle("OBS直播推流界面")
        self.resize(800, 600)

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
        self.stream_url_edit.setPlaceholderText("推流地址")
        self.stream_settings_box.addWidget(self.stream_url_edit)

        self.stream_key_edit = QLineEdit()
        self.stream_key_edit.setPlaceholderText("推流密钥")
        self.stream_settings_box.addWidget(self.stream_key_edit)

        # 创建开始/停止按钮
        self.start_stop_button = QPushButton("开始")
        self.start_stop_button.setFixedWidth(100)

        # 创建顶部布局，包含登录按钮和标题
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.login_button)
        top_layout.addStretch()
        top_layout.addWidget(QLabel("OBS直播推流界面"))
        top_layout.addStretch()

        # 将所有控件添加到主布局中
        main_layout = QVBoxLayout()
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.preview_label)
        main_layout.addLayout(self.stream_settings_box)
        main_layout.addWidget(self.start_stop_button)
        self.setLayout(main_layout)

        # 设置登录对话框
        self.login_dialog = LoginDialog()

    def on_login_button_clicked(self):
        result = self.login_dialog.exec_()
        if result == QDialog.Accepted:
            print("登录成功！")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    obs = OBS()
    obs.show()
    sys.exit(app.exec_())