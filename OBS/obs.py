import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets

import Main

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.width = 1280
        self.height = 720

        # 设置软件图标
        #self.setWindowIcon(QtGui.QIcon("icon.ico"))
        # 设置主界面标题
        self.setWindowTitle("面向对象课程第二十小组作品")
        # 设置固定尺寸
        self.setFixedSize(self.width, self.height)
        # 设置主界面背景色
        self.setStyleSheet("background-color:rgb(84,82,119)")

        self.init_widget()


    def init_widget(self):
        # 1. 创建一级菜单栏
        # 1.1 创建一级菜单栏的窗口
        self.widget_menu = QtWidgets.QWidget(self)  # 注意，传入参数代表一个从属关系，表示创建的QWidget属于self，也就是MainWindow自身
        self.widget_menu.setObjectName("widget_menu")
        self.widget_menu.setGeometry(QtCore.QRect(0, 0, 1280, 50))
        self.widget_menu.setStyleSheet("QWidget{background-color:rgb(123,223,223);border:2px solid balck;}")
        # 1.2 创建一个水平布局
        self.menuLayout = QHBoxLayout(self.widget_menu)
        # 1.3 设置水平布局的属性
        self.menuLayout.setSpacing(30)  # 设置间距
        self.menuLayout.setDirection(0)  # 自左向右的布局
        self.menuLayout.addSpacing(30)  # 最左端增加30像素的间距
        # 1.4 为菜单栏设置按钮组
        self.menuButtonGroup = QButtonGroup()
        # 1.5设置文字和字体
        menuStr = []
        menuStr.append("AAA")
        menuStr.append("BBB")
        menuStr.append("CCC")
        self.font = QFont()  # 设置字样式
        self.font.setFamily("黑体")  # 设置字体
        self.font.setBold(1)  # 设置为粗体
        self.font.setPixelSize(24)  # 字体大小
        # 1.5 添加按钮至按钮组
        count = 0  # 设置按钮在按钮组内的序号
        for menu_str in menuStr:
            menuBtn = QPushButton()  # 创建按钮
            menuBtn.setStyleSheet("QPushButton{color:rgb(0,0,0);border:none;}"
                                  "QPushButton::checked{color:rgb(58,164,98)}")
            menuBtn.setFont(self.font)  # 加载字体
            menuBtn.setText(menu_str)  # 加载文字
            menuBtn.setParent(self.widget_menu)  # 属于一级菜单栏的窗口
            menuBtn.setCheckable(True)
            self.menuLayout.addWidget(menuBtn)  # 一级菜单栏的水平布局中添加该按钮
            self.menuButtonGroup.addButton(menuBtn, count)  # 把按钮添加到按钮组中
            count += 1

        # 1.6 将按钮组内的按钮设置为互斥
        self.menuButtonGroup.setExclusive(True)
        # 1.7 菜单栏最后再添加弹簧
        self.menuLayout.addStretch()
        # 1.8 为按钮组内的按钮添加信号槽
        self.menuButtonGroup.button(0).clicked.connect(self.slot_AAA)  # 为按钮组中序号为0的按钮建立信号槽，点击就会触发slot_AAA()函数
        self.menuButtonGroup.button(1).clicked.connect(self.slot_BBB)  # 为按钮组中序号为1的按钮建立信号槽，点击就会触发slot_BBB()函数
        self.menuButtonGroup.button(2).clicked.connect(self.slot_CCC)  # 为按钮组中序号为2的按钮建立信号槽，点击就会触发slot_CCC()函数

        # 2.1 创建多分页窗口
        self.stackedWidget_func = QtWidgets.QStackedWidget(self) # QStackedWidget表示多分页的窗口
        self.stackedWidget_func.setObjectName("stackedWidget_func")
        self.stackedWidget_func.setGeometry(QtCore.QRect(0, 50, 1280, 50))
        self.stackedWidget_func.setStyleSheet("QWidget{background-color:rgb(211,240,168);border:none}")

        # 2.2 创建分页对象，并载入分页
        self.file_page = Main.AAA_Page()
        self.stackedWidget_func.addWidget(self.file_page)
        self.common_page = Main.AAA_Page()
        self.stackedWidget_func.addWidget(self.common_page)
        self.advance_page = Main.AAA_Page()
        self.stackedWidget_func.addWidget(self.advance_page)

        # 3.创建属性栏
        self.stackedWidget_param = QtWidgets.QStackedWidget(self)  # QStackedWidget表示多分页的窗口
        self.stackedWidget_param.setObjectName("stackedWidget_param")
        self.stackedWidget_param.setGeometry(QtCore.QRect(10, 110, 220, 600))
        self.stackedWidget_param.setStyleSheet("QWidget{background-color:rgb(188,188,188);border:none}")
        # 3.2 创建分页对象，并载入分页（略）

        # 4. 创建主窗口
        self.image_widget = QtWidgets.QWidget(self)
        self.image_widget.setGeometry(QtCore.QRect(240, 110, 820, 560))
        self.image_widget.setStyleSheet("QWidget{background-color:rgb(255,255,235);border:none}")
        # 可自由进行个性化设计，参考设计一级菜单的方式

        # 5. 创建其他窗口
        self.image_widget = QtWidgets.QWidget(self)
        self.image_widget.setGeometry(QtCore.QRect(1070, 110, 200, 560))
        self.image_widget.setStyleSheet("QWidget{background-color:rgb(255,200,235);border:none}")
        # 可自由进行个性化设计，参考设计一级菜单的方式

        # 6.创建下方文字栏
        self.text_widget = QtWidgets.QWidget(self)
        self.text_widget.setGeometry(QtCore.QRect(240, 680, 1030, 30))
        self.text_widget.setStyleSheet("QWidget{background-color:rgb(200,223,200);border:none}")
        # 可自由进行个性化设计，参考设计一级菜单的方式

    def slot_AAA(self):
        self.stackedWidget_func.setCurrentIndex(0)  # 将多页面窗口切换至页面序号0


    def slot_BBB(self):
        self.stackedWidget_func.setCurrentIndex(1)  # 将多页面窗口切换至页面序号1


    def slot_CCC(self):
        self.stackedWidget_func.setCurrentIndex(2)  # 将多页面窗口切换至页面序号2


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())


