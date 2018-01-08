# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
import os
import time

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from get_filename import getFileName
from convertImg import convertDicomTojpg

class TopButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super(TopButton, self).__init__(*args, **kwargs)
        # self.setMinimumSize(20, 40)
        self.setMaximumSize(120, 50)
        self.setDefault(True)
        self.setFont(QFont("楷体",14, QFont.Bold))

class ImgWidget(QFrame):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        self.default_pixmap = QPixmap('./imgs/blank.png')
        self.pixmap = None
        self.imageLabel = QLabel()
        self.imageLabel.setAlignment(Qt.AlignCenter)
        self._painter = QPainter()
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.imageLabel, Qt.AlignCenter)
        # print(self.default_pixmap.isNull())
        # self.imageLabel.setMinimumSize(200,200)
        self.setContentsMargins(0, 0, 0, 0)
        self.imageLabel.setPixmap(self.default_pixmap)
        self.setLayout(layout)
        # self.setStyleSheet('''
        # border: 1px solid black
        # ''')
        # self.setSizePolicy(QtGui.QSizePolicy.MinimumExpanding,
        #                    QtGui.QSizePolicy.MinimumExpanding,)
        self.filename = ''

    def resizeEvent(self, event):
        self.updatePixmap()

    def updatePixmap(self, qpixmap=None, resize_tag=False):
        if qpixmap is not None:
            self.pixmap = qpixmap
            # print('qpixmap {}'.format(qpixmap))

        if self.pixmap:
            # print('self')
            show_pixmap = self.pixmap.copy()
        else:
            show_pixmap = self.default_pixmap.copy()
        # print(self.imageLabel.height())

        show_pixmap = show_pixmap.scaledToHeight(
            # self.imageLabel.width(),
            self.height(),
            Qt.SmoothTransformation)
        # print(self.imageLabel.width())
        # print('show_pixmap {}'.format(show_pixmap))
        self.imageLabel.setPixmap(show_pixmap)
        self.update()

    # def paintEvent(self, event):
    #     qp = QPainter()
    #     qp.begin(self.pixmap)
    #     qp.setPen(Qt.green)
    #     qp.end()

    def mydrawRect(self, bbox, savename):
        bbox_rect = QRect(bbox[0], bbox[1], bbox[2], bbox[3])
        pixmap = self.pixmap.copy()
        qimg = QImage(self.pixmap.copy())

        qp = QPainter()
        pen = QPen()
        pen.setColor(Qt.green)
        pen.setWidth(3)
        qp.begin(pixmap)
        qp.setPen(pen)
        # myPaint.drawLine(x1, y1, x2, y2)
        qp.drawRect(bbox_rect)
        qp.end()
        self.updatePixmap(pixmap)
        # print('save')

        self.filename = 'H:\code\medicalUI\imgs\saveImg\{}_save.jpg'.format(savename)
        # print(self.filename)
        image_save  = qimg.copy(bbox_rect)
        image_save.save(self.filename, "jpg")
        # print(qimg)

    def mousePressEvent(self, QMouseEvent):
        pass

class ImageRecogWidget(QWidget):
    def __init__(self, parent = None):
        super(ImageRecogWidget, self).__init__(parent)

        self.font = QFont("楷体", 14, QFont.Bold)

        openButton = TopButton("导入照片")
        openButton.setIcon(QIcon(QPixmap("imgs/folder.png")))

        searchButton = TopButton("检测")
        searchButton.setIcon(QIcon("imgs/glass.png"))

        #self layout
        self.Layout = QGridLayout()
        self.Layout.setSpacing(20)

        self.Layout.setRowStretch(0, 1)
        self.Layout.setRowStretch(1, 8)
        self.Layout.setColumnStretch(0, 3)
        self.Layout.setColumnStretch(1, 1)

        self.setLayout(self.Layout)

        #pic widget
        self.picWidget = QFrame()
        # self.picWidget.setStyleSheet(
        #     '''
        #     background-color: rgb(51, 180, 255, 200);
        #     border-top: 2px solid rgb(51, 200, 255, 230);
        #     border-left: 2px solid rgb(51, 200, 255, 230);
        #     border-right: 2px solid rgb(51, 150, 255, 230);
        #     border-bottom: 2px solid rgb(51, 150, 255, 230);
        #     '''
        # )
        self.picLayout = QVBoxLayout()
        self.picLayout.setContentsMargins(0, 0, 0, 0)
        self.picWidget.setLayout(self.picLayout)
        self.Layout.addWidget(self.picWidget, 1, 0)

        #button widget
        self.buttonWidget = QWidget()
        self.buttonLayout = QGridLayout()

        self.buttonWidget.setLayout(self.buttonLayout)
        self.buttonLayout.addWidget(openButton, 0, 0)
        self.buttonLayout.addWidget(searchButton, 0, 1)

        self.Layout.addWidget(self.buttonWidget, 0, 0)

        #right widget
        self.rightFrame = QFrame()
        self.rightLayout = QGridLayout()
        self.rightLayout.setContentsMargins(0, 0, 0, 0)
        self.rightFrame.setLayout(self.rightLayout)

        self.Layout.addWidget(self.rightFrame, 1, 1)

        #select area
        self.selectAreaFrame = QFrame()
        self.selectAreaLabel = QLabel("所选区域")
        self.selectAreaLabel.setFont(self.font)
        self.selectAreaImg = ImgWidget()
        self.selectAreaImg.pixmap = QPixmap()
        self.selectAreaImg.update()

        self.selectAreaLayout = QVBoxLayout()
        self.selectAreaLayout.addWidget(self.selectAreaLabel)
        self.selectAreaLayout.addWidget(self.selectAreaImg)
        self.selectAreaFrame.setLayout(self.selectAreaLayout)

        self.rightLayout.addWidget(self.selectAreaFrame, 0, 0)

        #result widget
        self.objectLabel = QLabel("检测结果")
        self.objectLabel.setFont(self.font)
        self.resultLabel = QLabel()
        self.resultLabel.setFont(QFont("Roman times", 16))
        self.resultLabel.setMinimumWidth(140)

        self.resultWidget = QWidget()
        self.resultWidLayout = QVBoxLayout()
        self.resultWidget.setLayout(self.resultWidLayout)
        self.resultWidLayout.addWidget(self.objectLabel)
        self.resultWidLayout.addWidget(self.resultLabel)
        self.rightLayout.addWidget(self.resultWidget, 1, 0, Qt.AlignTop)

        self.files = ''
        self.onlyfileName = ''
        self.get = getFileName()
        self.convert = convertDicomTojpg()

        openButton.clicked.connect(self.openPicture)
        searchButton.clicked.connect(self.search)

    def updateInfo(self, res_list):
        # print('update res：{}'.format(res_list))
        self.resultLabel.setText('结果是： {}\n用时： {:.2f}s'.format(res_list[0], res_list[1]))
        self.imageWidget.mydrawRect(res_list[2], res_list[4])
        print(self.imageWidget.filename)
        self.selectAreaImg.pixmap = QPixmap(self.imageWidget.filename)
        self.selectAreaImg.updatePixmap()

    def cleanPic(self):
        if self.picWidget.layout():
            layout = self.picWidget.layout()
            # print(layout.count())
            for i in reversed(range(layout.count())):
                item = layout.itemAt(i)
                if isinstance(item, QWidgetItem):
                    item.widget().close()
                layout.removeItem(item)

            QWidget().setLayout(self.picWidget.layout())
            self.picLayout = QHBoxLayout()
            self.picWidget.setLayout(self.picLayout)

    def openPicture(self):
        self.filename = QFileDialog.getOpenFileName(self, 'Open file', './')
        print(self.filename)
        print(self.files)

        # file name judgement
        if self.filename[0] == '':
            return
        else:
            extension_name = self.filename[0].split('.')[-1]

        convertedName = False
        if extension_name == "dcm":
            convertedName = self.convert.convert(self.filename[0])
        elif extension_name == "jpg":
            convertedName = self.filename[0]

        # if open file type is allowed, open it, else show warning information
        if convertedName == False:
            QMessageBox.information(self, "Image Viewer", "Cannot load {}".format(self.filename[0]))
            return
        else:
            self.files = self.filename[0]
            image = QPixmap(convertedName)
            if image.isNull():
                QMessageBox.information(self, "Image Viewer", "Cannot load {}".format(self.filename[0]))
                return
            self.cleanPic()
            self.imageWidget = ImgWidget()
            self.imageWidget.pixmap = QPixmap(convertedName)
            self.imageWidget.updatePixmap()

            self.picLayout.addWidget(self.imageWidget, Qt.AlignCenter)
            self.picWidget.show()
            self.onlyfileName = self.get.getName(convertedName, '/')


    def search(self):
        if self.files ==  '':
            QMessageBox.information(self, "Query Viewer", "请先导入图片！")
            return
        # print(self.files)
        thread = MyThread(self.files, self.onlyfileName, self)
        thread.start_trigger.connect(self.startCompute)
        thread.end_trigger.connect(self.updateInfo)
        thread.start()

    def startCompute(self):
        self.resultLabel.setText('正在计算...')

class MyThread(QThread):
    start_trigger = pyqtSignal()
    end_trigger = pyqtSignal(list)
    # [reuslt, time, [x1, y1, x2, y2]]
    def __init__(self, files, filename=None, parent=None):
        super(MyThread, self).__init__(parent)
        self.file = files
        self.filename = filename

    def run(self):

        print('sleep ..')
        # print(self.filename)
        self.start_trigger.emit()
        startTime = time.time()

        time.sleep(2)
        totalTime = time.time() - startTime

        time.sleep(0.3)
        self.end_trigger.emit(['xxx', totalTime, [500, 800, 1200, 1300], self.file, self.filename])
        # self.end_trigger.emit(['xxx', totalTime, [500, 800, 1200, 1300]])
        # self.end_trigger.emit(str(totalTime))