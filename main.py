import sys
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PySide6.QtGui import QAction, QImage, QPixmap, QIcon
from PySide6.QtWidgets import (QApplication,QWidget, QLabel, 
QMainWindow, QHBoxLayout, QVBoxLayout, 
QPushButton, QFileDialog, QToolBar, QStatusBar, QMessageBox)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simple Photoshop")

        #메뉴바
        toolbar = QToolBar("Main toolbar")
        self.addToolBar(toolbar)

        #메인화면 레이아웃
        main_layout = QHBoxLayout()

        #사이드바 메뉴버튼
        sidebar = QVBoxLayout()
        button1 = QPushButton("이미지 열기")
        button2 = QPushButton("저장")
        button3 = QPushButton("이전")
        button4 = QPushButton("작업 취소")
        button5 = QPushButton("나가기")
        #사이드바 메뉴-기능 연결
        button1.clicked.connect(self.show_file_dialog) 
        button2.clicked.connect(self.save_file)
        #... 나머지 추가 예정
        button4.clicked.connect(self.clear_label)
        button5.clicked.connect(qApp.quit)
        #6까지 추가
        #사이드바에 메뉴버튼 추가(위젯)
        sidebar.addWidget(button1)
        sidebar.addWidget(button2)
        sidebar.addWidget(button3)
        sidebar.addWidget(button4)
        sidebar.addWidget(button5)

        main_layout.addLayout(sidebar)

        #----- 기능 ------

        #기본 편집
        #확대
        bigger = QAction("확대", self) #버튼 이름
        bigger.setStatusTip("확대") #setStatusTip : 커서를 올려뒀을 때 나오는 설명창
        bigger.triggered.connect(self.bigger) #연결할 기능

        #축소
        smaller  = QAction("축소", self) 
        smaller.setStatusTip("축소") 
        smaller.triggered.connect(self.smaller) 

        #회전
        rotation  = QAction("회전", self)
        rotation.setShortcut('Ctrl+r')
        rotation.setStatusTip("회전")
        rotation.triggered.connect(self.rotation)

        #좌우반전
        lr_flip  = QAction("좌우반전", self)
        lr_flip.setStatusTip("좌우반전")
        lr_flip.triggered.connect(self.lr_flip)

        #상하반전
        ud_flip  = QAction("상하반전", self)
        ud_flip.setStatusTip("상하반전")
        ud_flip.triggered.connect(self.ud_flip)

        #자르기
        cut = QAction("자르기", self) 
        cut.setStatusTip("자르기")
        cut.triggered.connect(self.cut) 

        #원형으로 자르기
        circle_cut = QAction("원형 자르기", self)
        circle_cut.setStatusTip("원형 자르기")
        circle_cut.triggered.connect(self.circle_cut)


        #이미지
        #뒤틀리기
        twist = QAction("뒤틀리기", self)
        twist.setStatusTip("뒤틀리기")
        twist.triggered.connect(self.twist)

        #리퀴파이
        liquefy = QAction("리퀴파이", self)
        liquefy.setStatusTip("리퀴파이")
        liquefy.triggered.connect(self.liquefy)

        #렌즈 왜곡
        distortion = QAction("렌즈 왜곡", self)
        distortion.setStatusTip("렌즈 왜곡")
        distortion.triggered.connect(self.distortion)

        #모자이크
        mosaic = QAction("모자이크", self)
        mosaic.setStatusTip("모자이크")
        mosaic.triggered.connect(self.mosaic)

        #합성
        compose = QAction("합성", self)
        compose.setStatusTip("합성")
        compose.triggered.connect(self.compose)


        #색상
        #밝기 조절
        bright = QAction("밝기 조절", self)
        bright.setStatusTip("밝기 조절")
        bright.triggered.connect(self.bright) 

        #색상반전
        color_inversion = QAction("색상 반전", self)
        color_inversion.setStatusTip("색상 반전")
        color_inversion.triggered.connect(self.color_inversion)

        #흑백
        gray_scale = QAction("흑백", self)
        gray_scale.setStatusTip("흑백")
        gray_scale.triggered.connect(self.gray_scale)

        #특정 색상 반전
        set_color_inversion = QAction("특정 색상 반전", self)
        set_color_inversion.setStatusTip("특정 색상 반전")
        set_color_inversion.triggered.connect(self.set_color_inversion)


        #그리기
        #원그리기
        circle = QAction("원", self)
        circle.setStatusTip("원")
        circle.triggered.connect(self.circle)
        
        #사각형 그리기
        square = QAction("사각형", self)
        square.setStatusTip("사각형")
        square.triggered.connect(self.square)

        #삼각형 그리기
        triangle = QAction("삼각형", self)
        triangle.setStatusTip("삼각형")
        triangle.triggered.connect(self.triangle)

        #직선 그리기
        line = QAction("직선", self)
        line.setStatusTip("직선")
        line.triggered.connect(self.line)

        #브러쉬
        brush = QAction("브러쉬", self)
        brush.setStatusTip("브러쉬")
        brush.triggered.connect(self.brush)

        #선택
        select = QAction("선택", self)
        select.setStatusTip("선택")
        select.triggered.connect(self.select)


        #---메뉴 추가---
        self.setStatusBar(QStatusBar(self))

        menu = self.menuBar()
        file_menu1 = menu.addMenu("&기본 편집") #메뉴바에 메뉴 추가
        file_menu1.addAction(bigger)
        file_menu1.addAction(smaller)
        file_menu1.addAction(rotation)
        file_menu1.addAction(lr_flip)
        file_menu1.addAction(ud_flip)
        file_menu1.addAction(cut)
        file_menu1.addAction(circle_cut)

        file_menu2 = menu.addMenu("&이미지")
        file_menu2.addAction(twist)
        file_menu2.addAction(liquefy)
        file_menu2.addAction(distortion)
        file_menu2.addAction(mosaic)
        file_menu2.addAction(compose)

        file_menu3 = menu.addMenu("&선택")
        file_menu3.addAction(select)

        file_menu4 = menu.addMenu("&색상")
        file_menu4.addAction(bright)
        file_menu4.addAction(color_inversion)
        file_menu4.addAction(gray_scale)
        file_menu4.addAction(set_color_inversion)

        file_menu5 = menu.addMenu("&그리기")
        file_menu5.addAction(circle)
        file_menu5.addAction(square)
        file_menu5.addAction(triangle)
        file_menu5.addAction(line)
        file_menu5.addAction(brush)
        
        
        #메인 화면 구성
        self.label1 = QLabel(self)
        self.label1.setFixedSize(640, 480) #사이드바 제외 한 여백의 크기
        main_layout.addWidget(self.label1)

        self.label2 = QLabel(self)
        self.label2.setFixedSize(640, 480) 
        main_layout.addWidget(self.label2)

        widget = QWidget(self)
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

#------기능 관련 함수 -----

    #파일 불러오기
    def show_file_dialog(self):
        file_name = QFileDialog.getOpenFileName(self, "이미지 열기", "./")
        print(file_name)
        self.image = cv2.imread(file_name[0]) #튜플 형태: 파일 주소
        h, w, _ = self.image.shape #높이 너비 채널
        bytes_per_line = 3 * w
        image = QImage(self.image.data, w, h, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
        pixmap = QPixmap(image)
        self.label1.setPixmap(pixmap)

    #메뉴바 버튼 클릭 확인용 - 추후에 삭제
    def toolbarButtonClick(self, s):
        print("click", s)
    
    #작업 취소
    def clear_label(self):
        self.label2.clear()

    #저장
    def save_file(self):
        save_file = QFileDialog.getSaveFileName(self, 'Save file', './')
        self.label2.setText(save_file[0])
        print("저장")

    #확대
    def bigger(self):
        print("확대")
    
    #축소
    def smaller(self):
        print("축소")
    
    #회전
    def rotation(self): #수정중
        h, w, _ = self.image.shape
        d90 = 90.0 * np.pi / 180.0 #90도
        m90 = np.float32([
            [np.cos(d90), -1*np.sin(d90), h],
            [np.sin(d90), np.cos(d90), 0]
        ])
        r90 = cv2.warpAffine(self.image, m90, (h, w))

        bytes_per_line = 3 * w
        image = QImage(r90.data, w, h, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
        pixmap = QPixmap(image)
        self.label2.setPixmap(pixmap)

        print("회전")
    
    #좌우반전
    def lr_flip(self):
        image = cv2.flip(self.image, 1) #1은 좌우반전을 의미
        h, w, _ = image.shape #높이 너비 채널
        bytes_per_line = 3 * w
        image = QImage(image.data, w, h, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
        pixmap = QPixmap(image)
        self.label2.setPixmap(pixmap)

    
    def ud_flip(self):
        print("상하반전")

    def cut(self):
        print("자르기")

    def circle_cut(self): #수정중
        h, w, _ = self.image.shape
        mask = np.zeros_like(self.image)
        cv2.circle(mask, (int(w/2), int(w/2)), int(w/2), (255, 255, 255), -1)
        cv2.bitwise_and(self.image, mask)

        bytes_per_line = 3 * w
        image = QImage(self.image.data, w, h, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
        pixmap = QPixmap(image)
        self.label2.setPixmap(pixmap)
        print("원형 자르기")

    def twist(self):
        print("뒤틀리기")

    def liquefy(self):
        print("리퀴파이")

    def distortion(self):
        print("렌즈왜곡")

    def mosaic(self):
        print("모자이크")

    def compose(self):
        print("사진 합성")

    def select(self):
        print("배경 선택")

    def bright(self):
        print("밝기 조절")

    def color_inversion(self):
        h, w, _ = self.image.shape #높이 너비 채널
        bytes_per_line = 3 * w
        image = QImage(self.image.data, w, h, bytes_per_line, QImage.Format_BGR888).rgbSwapped()
        pixmap = QPixmap(image)
        self.label2.setPixmap(pixmap)
        print("색상 반전")

    def gray_scale(self):
        # cv2.IMREAD_GRAYSCALE(self.image)
        image = cv2.cvtColor(self.image, cv2.COLOR_RGB2GRAY)
        h, w, _ = self.image.shape #높이 너비 채널
        bytes_per_line = 3 * w
        image = QImage(self.image.data, w, h, bytes_per_line, QImage.Format_Alpha8).rgbSwapped()
        pixmap = QPixmap(image)
        self.label2.setPixmap(pixmap)
        print("흑백")

    def set_color_inversion(self):
        print("특정 색상 반전")

    def circle(self):
        print("원")

    def square(self):
        print("사각형")

    def triangle(self):
        print("삼각형")
    
    def line(self):
        print("직선 그리기")

    def brush(self):
        print("브러쉬")
    


#창 보이기
if __name__ == "__main__":
    app = QApplication()
    window = MainWindow()
    window.show()
    sys.exit(app.exec())