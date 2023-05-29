from screenShot import Ui_Form
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import cv2
from PIL import ImageGrab
import numpy as np
import time
from datetime import datetime
global img
global point1, point2


class MainWindow(QMainWindow, Ui_Form):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent=parent)
        self.setupUi(self)
        self.savePath = datetime.now().strftime('%Y%m%d%H%M%S')
        self.MyTimer = QTimer()
        self.MyTimer1 = QTimer()
        self.name = None
        self.ROIname = None

    def startCapture(self):
        self.countSave = 0
        self.fps = 13
        self.flag = False
        self.count = 1
        self.name = self.savePath + ".avi"
        self.screen = ImageGrab.grab()
        self.width, self.high = self.screen.size
        self.fourcc = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')
        self.video = cv2.VideoWriter('%s.avi' % self.name, self.fourcc, self.fps, (self.width, self.high))
        print('开始录制!')
        self.label_2.setText("录制中！")
        self.start_time = time.time()
        self.showMinimized()
        self.MyTimer.start(30)
        self.MyTimer.timeout.connect(self.video_record)

    def video_record(self):  # 录入视频
        if self.flag:
            print("录制结束！")
            self.final_time = time.time()
            self.video.release()
        if self.count == 1:
            self.label_2.setText("录制中.")
        elif self.count == 2:
            self.label_2.setText("录制中..")
        else:
            self.label_2.setText("录制中...")
        self.count += 1
        self.count = self.count % 4
        self.im = ImageGrab.grab()
        frame = cv2.cvtColor(np.array(self.im), cv2.COLOR_RGB2BGR)
        self.video.write(frame)

    def stopCapture(self):
        if self.MyTimer.isActive():
            self.MyTimer.stop()
        self.label_2.setText("录制结束\n录制文件名:{}".format(self.name))
        if self.name is None:
            self.label_2.setText("视频还未录制！")
        else:
            self.flag = True

    def startROICapture(self):
        curScreen = ImageGrab.grab()  # 获取屏幕对象
        point1, point2 = select_roi(curScreen)
        self.showMinimized()
        self.min_x = min(point1[0], point2[0])
        self.min_y = min(point1[1], point2[1])
        self.max_x = max(point1[0], point2[0])
        self.max_y = max(point1[1], point2[1])
        height, width = self.max_y - self.min_y, self.max_x - self.min_x
        print(height, width)
        fourcc = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')
        self.ROIname = self.savePath + ".avi"
        self.video1 = cv2.VideoWriter(self.ROIname, fourcc, 13, (width, height))
        self.label_2.setText("录制中...")
        self.MyTimer1.start(30)
        self.MyTimer1.timeout.connect(self.ROIRect)

    def ROIRect(self):
        captureImage = ImageGrab.grab()  # 抓取屏幕
        frame = cv2.cvtColor(np.array(captureImage), cv2.COLOR_RGB2BGR)
        frame = frame[self.min_y:self.max_y, self.min_x:self.max_x, :]
        self.video1.write(frame)

    def stopROICapture(self):
        if self.MyTimer1.isActive():
            self.MyTimer1.stop()
        self.label_2.setText("录制结束\n录制文件名:{}".format(self.ROIname))
        if self.ROIname is None:
            self.label_2.setText("视频还未录制！")
            
    def selectSavePath(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(self,"选择保存路径","","All Files (*);;Video Files (*.avi)", options=options)
        if fileName:
            self.savePath = fileName
            print(self.savePath)


# 鼠标事件
def on_mouse(event, x, y, flags, key):
    global img, point1, point2
    img2 = img.copy()
    if event == cv2.EVENT_LBUTTONDOWN:  # 左键点击
        point1 = (x, y)
        cv2.circle(img2, point1, 10, (0, 255, 0), thickness=2)
        cv2.imshow('image', img2)
    elif event == cv2.EVENT_MOUSEMOVE and (flags & cv2.EVENT_FLAG_LBUTTON):  # 按住左键拖曳
        cv2.rectangle(img2, point1, (x, y), (255, 0, 0), thickness=2)
        cv2.imshow('image', img2)
    elif event == cv2.EVENT_LBUTTONUP:  # 左键释放
        point2 = (x, y)
        cv2.rectangle(img2, point1, point2, (0, 0, 255), thickness=2)
        cv2.imshow('image', img2)


# 选择ROI区域
def select_roi(frame):
    global img, point1, point2
    img = cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR)
    winname = 'image'
    cv2.namedWindow(winname, cv2.WINDOW_NORMAL)
    cv2.setWindowProperty(winname, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.setMouseCallback(winname, on_mouse)
    cv2.imshow(winname, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return point1, point2


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
