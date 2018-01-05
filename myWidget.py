# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
import os
import time
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class TopButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super(TopButton, self).__init__(*args, **kwargs)
        # self.setMinimumSize(20, 40)
        self.setMaximumSize(120, 50)
        self.setDefault(True)
        self.setFont(QFont("楷体",14, QFont.Bold))

class ImgWidget(QFrame):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        # self.default_pixmap = QPixmap(picture)
        self.default_pixmap = QPixmap('./images/train.jpg')
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

    def resizeEvent(self, event):
        self.updatePixmap()

    def updatePixmap(self):
        if self.pixmap:
            show_pixmap = self.pixmap.copy()
        else:
            show_pixmap = self.default_pixmap.copy()
        # print(self.imageLabel.height())

        show_pixmap = show_pixmap.scaledToHeight(
            # self.imageLabel.width(),
            self.height(),
            Qt.SmoothTransformation)
        # print(self.imageLabel.width())
        self.imageLabel.setPixmap(show_pixmap)

    def paintEvent(self, event):
        pass

    def mousePressEvent(self, QMouseEvent):
        pass

class MyThread(QThread):
    start_trigger = pyqtSignal(str)
    end_trigger = pyqtSignal(str)

    def __init__(self, files, parent=None):
        super(MyThread, self).__init__(parent)
        self.file = files

    def run(self):
        print('sleep ..')
        self.start_trigger.emit('正在计算...')
        startTime = time.time()

        time.sleep(2)
        totalTime = time.time() - startTime

        self.end_trigger.emit('结果是...')
        time.sleep(0.3)
        self.end_trigger.emit("耗时: {:.2f}s".format(totalTime))
        # self.end_trigger.emit(str(totalTime))

class ImageRecogWidget(QWidget):
    def __init__(self,parent=None):
        super(ImageRecogWidget, self).__init__(parent)
        self.files = ''

        self.font = QFont("楷体", 14, QFont.Bold)

        openButton = TopButton("导入照片")
        openButton.setIcon(QIcon(QPixmap("imgs/folder0.png")))

        searchButton = TopButton("查询")
        searchButton.setIcon(QIcon("imgs/glass.png"))

        self.objectLabel = QLabel("识别结果")
        self.objectLabel.setFont(self.font)

        #result widget
        self.resultLabel = QLabel()
        self.resultLabel.setFont(QFont("Roman times", 16))

        self.resultWidget = QWidget()
        self.resultWidLayout = QVBoxLayout()
        self.resultWidget.setLayout(self.resultWidLayout)
        self.resultWidLayout.addWidget(self.resultLabel)
        #
        self.buttonWidget = QWidget()
        self.buttonLayout = QGridLayout()

        self.buttonWidget.setLayout(self.buttonLayout)
        self.buttonLayout.addWidget(openButton, 1, 0)
        self.buttonLayout.addWidget(searchButton, 1, 1)

        self.Layout = QGridLayout()
        self.Layout.setSpacing(20)

        self.Layout.addWidget(self.buttonWidget, 0, 0)

        self.Layout.addWidget(self.objectLabel, 0, 1, Qt.AlignCenter)
        self.Layout.addWidget(self.resultWidget, 1, 1, Qt.AlignCenter)
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

        openButton.clicked.connect(self.openPicture)
        searchButton.clicked.connect(self.search)

    def updateText(self, text):
        print('update text：{}'.format(text))
        self.resultLabel.setText(text)

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
        self.files = self.filename[0]
        print(self.filename)
        if self.filename[0]:
            image = QPixmap(self.filename[0])
            if image.isNull():
                QMessageBox.information(self, "Image Viewer", "Cannot load %s." % self.filename[0])
                return
            # self.openSite.setText(self.filename[0])
            self.cleanPic()
            self.imageWidget = ImgWidget()
            self.imageWidget.pixmap = QPixmap(self.filename[0])
            self.imageWidget.updatePixmap()

            self.picLayout.addWidget(self.imageWidget, Qt.AlignCenter)
            self.picWidget.show()

    def search(self):
        if self.files ==  '':
            QMessageBox.information(self, "Query Viewer", "请先导入图片！")
            return
        # print(self.files)
        thread = MyThread(self.files, self)
        thread.start_trigger.connect(self.updateText)
        thread.end_trigger.connect(self.updateText)
        thread.start()