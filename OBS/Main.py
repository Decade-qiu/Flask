from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class AAA_Page(QWidget):
    def __init__(self):
        super().__init__()
        # 创建水平布局
        self.hLayout = QHBoxLayout(self)
        self.hLayout.setContentsMargins(0, 0, 0, 0)  # 设置水平布局在Widget内上下左右的间距
        self.hLayout.setSpacing(10)  # 设置间距
        self.hLayout.setDirection(0)  # 自左向右的布局
        self.hLayout.addSpacing(10)  # 左侧空隙

        self.font = QFont()
        self.font.setFamily("黑体")
        self.font.setBold(1)  # 设置为粗体
        self.font.setPixelSize(24)  # 字体大小

        # 创建a1图像按钮
        self.btn_a1 = QPushButton() # 创建按钮
        self.btn_a1.setStyleSheet("QPushButton{color:white;background-color:rgb(51,204,255);font-family:黑体;}"
                                      "QPushButton:pressed{background-color:rgb(51,129,172)}")
        self.btn_a1.setFont(self.font)
        self.btn_a1.setText("a1")
        self.btn_a1.setFixedHeight(50)
        self.btn_a1.setFixedWidth(120)
        self.btn_a1.setParent(self)
        self.btn_a1.setCheckable(True)
        self.btn_a1.clicked.connect(self.slot_a1)
        self.hLayout.addWidget(self.btn_a1)

        # 创建a2图标
        self.btn_a2 = QPushButton()
        self.btn_a2.setStyleSheet("QPushButton{color:white;background-color:rgb(51,204,255);}"
                                      "QPushButton:pressed{background-color:rgb(51,129,172)}")
        self.btn_a2.setFont(self.font)
        self.btn_a2.setText("a2")
        self.btn_a2.setFixedHeight(50)
        self.btn_a2.setFixedWidth(120)
        self.btn_a2.setParent(self)
        self.btn_a2.setCheckable(True)
        self.btn_a2.clicked.connect(self.slot_a2)
        self.hLayout.addWidget(self.btn_a2)


        # 创建a3图标
        self.btn_a3 = QPushButton()
        self.btn_a3.setStyleSheet("QPushButton{color:white;background-color:rgb(51,204,255)}"
                                      "QPushButton:pressed{background-color:rgb(51,129,172)}")
        self.btn_a3.setFont(self.font)
        self.btn_a3.setText("a3")
        self.btn_a3.setFixedHeight(50)
        self.btn_a3.setFixedWidth(120)
        self.btn_a3.setParent(self)
        self.btn_a3.setCheckable(True)
        self.btn_a3.clicked.connect(self.slot_a3)
        self.hLayout.addWidget(self.btn_a3)

        # 最后，在尾端添加弹簧，以至于布局呈现靠左而不是居中
        self.hLayout.addStretch()

    def slot_a1(self):
        print("slot_a1 ")

    def slot_a2(self):
        print("slot_a2 ")

    def slot_a3(self):
        print("slot_a3 ")


