# -*- coding: utf-8 -*-
import sys
import cv2
import dlib
from imutils.video import FPS
from UI import *

fpsValue = 0.1e-5
DOWNSAMPLE_RATIO = 1
SKIP_FRAMES = 1
count = 0
currentRect = [0,0,0,0]
frameCount = 0
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")   #  shape_predictor 로드

def drawRect(faceRect):     # 얼굴 사각형 영역
    global DOWNSAMPLE_RATIO
    global currentRect
    x1 = int(faceRect.left()*DOWNSAMPLE_RATIO)
    y1 = int(faceRect.top()*DOWNSAMPLE_RATIO)
    x2 = int(faceRect.right()*DOWNSAMPLE_RATIO)
    y2 = int(faceRect.bottom()*DOWNSAMPLE_RATIO)
    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
    currentRect = [x1,y1,x2,y2]

def drawFakeRect():     
    global DOWNSAMPLE_RATIO
    global currentRect

    x1 = int(currentRect[0])
    y1 = int(currentRect[1])
    x2 = int(currentRect[2])
    y2 = int(currentRect[3])
    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

class ShowVideo(QtCore.QObject):    # cv에서 캡쳐한 영상 윈도우에 보여주기
    VideoSignal1 = QtCore.pyqtSignal(QtGui.QImage)
    t_UI = QtCore.pyqtSignal()
    cap = cv2.VideoCapture(0)

    def __init__(self, parent=None):
        super(ShowVideo, self).__init__(parent) # ShowVideo 상속

    @QtCore.pyqtSlot()
    def startVideo(self):   # 영상 불러오기
        global frame
        global gray
        global fpsValue
        global DOWNSAMPLE_RATIO
        global SKIP_FRAMES
        global count
        global currentRect
        global frame_counter
        
        

        fps = FPS().start()
        ui.image_viewer1.show()

        while True:     # 영상 재생 중

            ret, frame = self.cap.read()    # 프레임 Ture 반환 

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # 그레이 스케일링
            if (DOWNSAMPLE_RATIO != 1.0):
                gray = cv2.resize(gray, (0, 0), fx=1 / DOWNSAMPLE_RATIO, fy=1 / DOWNSAMPLE_RATIO, interpolation = cv2.INTER_LINEAR)

            count += 1
            if(count % SKIP_FRAMES == 0):
                faceRects = detector(gray, 0)
                #
                    

                if (len(faceRects) == 0):   # 얼굴 감지 안됐을 때
                    print("Face Not Detected.")
                    fps.update()
                    fps.stop()

                else:
                    fps.update()
                    fps.stop()
                    fpsValue = fps.fps()
                    drawRect(personRect(faceRects))

            else:
                drawFakeRect()     

            frame = cv2.resize(frame, (600, 440))       # 600, 440으로 리사이즈
            color_swapped_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            qt_image1 = QtGui.QImage(color_swapped_image.data,
                                    int(600),
                                    int(440-4),
                                    color_swapped_image.strides[0],
                                    QtGui.QImage.Format_RGB888)
            self.VideoSignal1.emit(qt_image1)
            self.t_UI.emit()

            loop = QtCore.QEventLoop()
            QtCore.QTimer.singleShot(10, loop.quit)
            loop.exec_()

def personRect(faceRects):  # 여러 개의 얼굴이 인식될 시, 가장 큰 면적을 가진 사람의 얼굴을 인식
    biggestArea = 0
    if (len(faceRects) == 1):
        return faceRects[0]
    else:
        for faceRect in faceRects:
            x1 = faceRect.left()
            y1 = faceRect.top()
            x2 = faceRect.right()
            y2 = faceRect.bottom()
            area = (x2-x1) * (y2-y1)

            if (area>biggestArea):
                biggestArea = area
                person= faceRect

        return person

def setVideoPath(ui,vid):   # 비디오 경로 
    if ui.radio.isChecked():
        vid.cap = cv2.VideoCapture(0)

if __name__ == '__main__':  # ui on
    app = QtWidgets.QApplication(sys.argv)

    thread = QtCore.QThread()
    thread.start()
    vid = ShowVideo()
    vid.moveToThread(thread)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    vid.VideoSignal1.connect(ui.image_viewer1.setImage)
    ui.push_button1.clicked.connect(vid.startVideo)
    ui.push_button2.clicked.connect(QtCore.QCoreApplication.instance().quit)
    MainWindow.show()

    sys.exit(app.exec_())

    