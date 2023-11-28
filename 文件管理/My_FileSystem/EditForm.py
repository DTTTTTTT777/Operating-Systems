# 这个文件定义了编辑文件相关的内容

"""
编辑文件
"""
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon,QStandardItem,QStandardItemModel
import PyQt5.QtCore
from PyQt5.Qt import *
from BLOCK import Block
from FAT import FAT
from FCB import FCB
from Catelog import CatalogNode
import time
import os
import pickle
from File_Widget import File_Widget


class editForm(QWidget):
    _signal = PyQt5.QtCore.pyqtSignal(str) # 用于在编辑内容发生更改后发出信号。

    def __init__(self, name, data):
        super().__init__()
        self.resize(1200, 800)
        self.setWindowTitle(name)
        self.name = name
        self.setWindowIcon(QIcon('img/file.png'))

        self.resize(900, 600)
        self.text_edit = QTextEdit(self)  # 实例化一个QTextEdit对象
        self.text_edit.setText(data)  # 设置编辑框初始化时显示的文本
        self.text_edit.setPlaceholderText("在此输入文件内容")  # 设置占位字符串
        self.text_edit.textChanged.connect(self.changeMessage)  # 判断文本是否发生改变
        self.initialData = data

        self.h_layout = QHBoxLayout()
        self.v_layout = QVBoxLayout()

        self.v_layout.addWidget(self.text_edit)
        self.v_layout.addLayout(self.h_layout)

        self.setLayout(self.v_layout)

        self.setWindowModality(PyQt5.QtCore.Qt.ApplicationModal)

    def closeEvent(self, event): # 重写的窗口关闭事件处理方法。在窗口关闭时，会弹出一个询问框，询问用户是否保存修改的内容。
        if self.initialData == self.text_edit.toPlainText(): # 如果打开后没有修改，则直接关闭即可
            event.accept()
            return

        reply = QMessageBox()
        reply.setWindowTitle('提醒')
        reply.setText('是否保存修改?')
        reply.setStandardButtons(QMessageBox.Yes | QMessageBox.No | QMessageBox.Ignore)
        buttonY = reply.button(QMessageBox.Yes)
        buttonY.setText('保存')
        buttonN = reply.button(QMessageBox.No)
        buttonN.setText('不保存')
        buttonI = reply.button(QMessageBox.Ignore)
        buttonI.setText('取消')

        reply.exec_()

        if reply.clickedButton() == buttonI:
            event.ignore()
        elif reply.clickedButton() == buttonY:
            self._signal.emit(self.text_edit.toPlainText())
            event.accept()
        else:
            event.accept()

    def changeMessage(self): # 文本编辑框内容改变时的槽函数
        # self.statusBar().showMessage('共'+str(len(self.text_edit.toPlainText()))+'字')
        pass

