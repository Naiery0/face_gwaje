# -*- coding: utf-8 -*-
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtWidgets import QFileDialog

class ImageViewer(QtWidgets.QWidget):   # 이미지 불러오기 
    def __init__(self, parent=None):
        super(ImageViewer, self).__init__(parent)
        self.image = QtGui.QImage()
        self.setAttribute(QtCore.Qt.WA_OpaquePaintEvent)

    def paintEvent(self, event):    # 위젯 그리기
        painter = QtGui.QPainter(self)
        painter.drawImage(0, 0, self.image)
        self.image = QtGui.QImage()

    def initUI(self):   # 객체를 인스턴스로 받을 매개변수 지
        self.setWindowTitle('Test')

    @QtCore.pyqtSlot(QtGui.QImage)
    def setImage(self, image):
        if image.isNull():
            #print("Viewer Dropped frame!")
            pass

        self.image = image
        if image.size() != self.size():     # 이미지 사이즈 조정
            self.setFixedSize(image.size())
        self.update()

class Ui_MainWindow(object):    # UI 창 
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(600, 485)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        #
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(2, 437, 596, 47))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(20)
        self.groupBox.setFont(font)
        self.groupBox.setFlat(False)
        self.groupBox.setCheckable(False)
        self.groupBox.setObjectName("groupBox")
        self.push_button1 = QtWidgets.QPushButton('Start',self.centralwidget)
        self.push_button1.setGeometry(QtCore.QRect(5, 440, 292, 40))
        self.push_button1.setObjectName("Start")
        self.push_button2 = QtWidgets.QPushButton('Quit', self.centralwidget)
        self.push_button2.setGeometry(QtCore.QRect(305, 440, 292, 40))
        self.push_button2.setObjectName("Quit")
        self.image_viewer1 = ImageViewer(self.centralwidget)
        self.image_viewer1.hide()

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):    # 설정창 
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Face Detector"))
        self.centralwidget.setStyleSheet("QWidget {background-color: #FFFFFF }")

        self.push_button1.setText(_translate("MainWindow","Start"))
        self.push_button2.setText(_translate("MainWindow", "Quit"))

    def fileDialog(self):
        fileName = QFileDialog.getOpenFileName(None)
        return fileName[0]


        
