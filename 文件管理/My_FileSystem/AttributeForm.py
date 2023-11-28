# 这个文件定义了属性窗口

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QFont
from PyQt5.Qt import *
from BLOCK import *
from FAT import *
from FCB import *
from Catelog import *
import time
import os
import pickle
from File_Widget import File_Widget

class attributeForm(QWidget): # 用于创建属性窗口界面。

    def __init__(self, name, isFile, createTime, updateTime, child=0):
        super().__init__()

        self.setWindowTitle('属性')
        self.name = name
        self.setWindowIcon(QIcon('img/attribute.png'))

        self.resize(206, 206)

        layout = QVBoxLayout()

        if isFile: # 根据文件类型（isFile）加载相应的图片
            self.icon = QPixmap('img/file.png')
        else:
            self.icon = QPixmap('img/folder.png')

        font = QFont()
        font.setPointSize(10)

        fileType = QLabel(self)
        if isFile:
            fileType.setText('类型: 文件')
        else:
            fileType.setText('类型: 文件夹')
        fileType.setFont(font)
        layout.addWidget(fileType)

        fileName = QLabel(self) # 显示文件名
        fileName.setText('名称: ' + self.name)

        fileName.setFont(font)
        layout.addWidget(fileName)

        createLabel = QLabel(self) # 显示创建时间
        year = str(createTime.tm_year)
        month = str(createTime.tm_mon)
        day = str(createTime.tm_mday)
        hour = str(createTime.tm_hour)
        hour = hour.zfill(2)
        minute = str(createTime.tm_min)
        minute = minute.zfill(2)
        second = str(createTime.tm_sec)
        second = second.zfill(2)
        createLabel.setText('创建时间: ' + year + '年' + month + '月' + day + '日 ' + hour + ':' + minute + ':' + second)
        createLabel.setFont(font)

        layout.addWidget(createLabel)

        if isFile: # 显示更新时间
            updateLabel = QLabel(self)
            year = str(updateTime.tm_year)
            month = str(updateTime.tm_mon)
            day = str(updateTime.tm_mday)
            hour = str(updateTime.tm_hour)
            hour = hour.zfill(2)
            minute = str(updateTime.tm_min)
            minute = minute.zfill(2)
            second = str(updateTime.tm_sec)
            second = second.zfill(2)
            updateLabel.setText('更新时间：' + year + '年' + month + '月' + day + '日 ' + hour + ':' + minute + ':' + second)
            updateLabel.setFont(font)

            layout.addWidget(updateLabel)

        else: # 显示目录下文件数目
            updateLabel = QLabel(self)
            updateLabel.setText('目录下共' + str(child) + '个项目')
            updateLabel.setFont(font)

            layout.addWidget(updateLabel)

        self.setLayout(layout)
        self.setWindowModality(Qt.ApplicationModal)