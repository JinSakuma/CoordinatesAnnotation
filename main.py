#!/usr/bin/env python
# coding: utf-8
#

import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLabel,
                             QFileDialog, QMessageBox)
from PyQt5.QtGui import QImage, QPixmap, QIcon
from PyQt5.QtCore import QSize

from util import resize, reproduce

import numpy as np
import os
import cv2
import json


class Widget(QWidget):

    def __init__(self):
        super().__init__()
        self.left = 300
        self.top = 300
        self.width = 1000
        self.height = 800
        self.img_x = 160
        self.img_y = 0
        self.SIZE = 800
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowTitle('CoordinatesAnnotation')
        self.setButton()
        self.initUI()
        self.show()

    def initPrams(self):
        self.px = None
        self.py = None
        self.points = []
        self.ori_points = []
        self.psets = {}
        self.image = None
        self.images = []
        self.save_flg = []
        self.idx = -1
        self.save_dir = None

    def initUI(self):
        self.px = None
        self.py = None
        self.points = []
        self.ori_points = []
        self.psets = {}
        self.image = None
        self.images = []
        self.save_flg = []
        self.idx = -1
        self.save_dir = None

        self.le = QLabel(self)
        image = cv2.imread("white.jpg")
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        h, w = image.shape[:2]
        qimg = QImage(image.flatten(), w, h, QImage.Format_RGB888)
        self.le.setPixmap(QPixmap.fromImage(qimg))
        self.le.move(self.img_x, self.img_y)

    def setButton(self):
        self.btn1 = QPushButton(self)
        self.btn1.setIcon(QIcon('icons/open.png'))
        self.btn1.setIconSize(QSize(80, 40))
        self.btn1.move(0, 0)
        self.btn1.clicked.connect(self.open_file)
        self.lbl1 = QLabel("Open File", self)
        self.lbl1.move(20, 55)

        self.btn2 = QPushButton(self)
        # self.btn2 = QPushButton("Open Dir", self)
        self.btn2.setIcon(QIcon('icons/open.png'))
        self.btn2.setIconSize(QSize(80, 40))
        self.btn2.move(0, 80)
        self.btn2.clicked.connect(self.open_dir)
        self.lbl2 = QLabel("Open Dir", self)
        self.lbl2.move(20, 135)

        self.btn3 = QPushButton(self)
        self.btn3.setIcon(QIcon('icons/open.png'))
        self.btn3.setIconSize(QSize(80, 40))
        self.btn3.move(0, 160)
        self.btn3.clicked.connect(self.set_save_dir)
        self.lbl3 = QLabel("Select Save Dir", self)
        self.lbl3.move(20, 215)

        self.btn4 = QPushButton(self)
        self.btn4.setIcon(QIcon('icons/next.png'))
        self.btn4.setIconSize(QSize(80, 40))
        self.btn4.move(0, 240)
        self.btn4.clicked.connect(self.next_img)
        self.lbl4 = QLabel("Next", self)
        self.lbl4.move(20, 295)

        self.btn5 = QPushButton(self)
        self.btn5.setIcon(QIcon('icons/prev.png'))
        self.btn5.setIconSize(QSize(80, 40))
        self.btn5.move(0, 320)
        self.btn5.clicked.connect(self.pre_img)
        self.lbl5 = QLabel("Previous", self)
        self.lbl5.move(20, 375)

        self.btn6 = QPushButton(self)
        self.btn6.setIcon(QIcon('icons/save.png'))
        self.btn6.setIconSize(QSize(80, 40))
        self.btn6.move(0, 400)
        self.btn6.clicked.connect(self.save)
        self.lbl6 = QLabel("Save", self)
        self.lbl6.move(20, 455)

        self.btn7 = QPushButton(self)
        self.btn7.setIcon(QIcon('icons/undo.png'))
        self.btn7.setIconSize(QSize(80, 40))
        self.btn7.move(0, 480)
        self.btn7.clicked.connect(self.delete)
        self.lbl7 = QLabel("Delete A Point", self)
        self.lbl7.move(20, 535)

        self.btn8 = QPushButton(self)
        self.btn8.setIcon(QIcon('icons/undo.png'))
        self.btn8.setIconSize(QSize(80, 40))
        self.btn8.move(0, 560)
        self.btn8.clicked.connect(self.deleteAll)
        self.lbl8 = QLabel("Delete All Points", self)
        self.lbl8.move(20, 615)

        self.btn9 = QPushButton(self)
        self.btn9.setIcon(QIcon('icons/done.png'))
        self.btn9.setIconSize(QSize(80, 40))
        self.btn9.move(0, 640)
        self.btn9.clicked.connect(self.export)
        self.lbl9 = QLabel("Export", self)
        self.lbl9.move(20, 695)

    def open_file(self):
        if len(self.psets) > 0:
            buttonReply = QMessageBox.question(self, "confirm message", "The annotation will be reseted. Do you want to change the file?",
                                               QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if buttonReply == QMessageBox.Yes:
                flg = True
            else:
                flg = False
        else:
            flg = True

        if flg:
            self.initPrams()
            file = QFileDialog.getOpenFileName(self, 'Open file', "Image files (*.jpg *.gif)")
            self.name = file[0].split("/")[-1]
            if file[0]:
                self.images.append(file[0])
                self.save_flg.append(False)
                self.idx += 1
                self.showImage(file[0])

    def open_dir(self):
        if len(self.psets) > 0:
            buttonReply = QMessageBox.question(self, "confirm message", "The annotation will be reseted. Do you want to change the folder?",
                                               QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if buttonReply == QMessageBox.Yes:
                flg = True
            else:
                flg = False
        else:
            flg = True

        if flg:
            self.initPrams()
            path = QFileDialog.getExistingDirectory(self, 'Open dir')
            self.name = path.split("/")[-1]
            if path:
                img_names = os.listdir(path)
                for name in img_names:
                    if ".jpg" in name or ".jpeg" in name or ".png" in name:
                        self.images.append(os.path.join(path, name))
                        self.save_flg.append(False)

                if len(self.images) > 0:
                    self.idx += 1
                    self.showImage(self.images[0])

    def set_save_dir(self):
        path = QFileDialog.getExistingDirectory(self, 'Open dir')
        if path:
            self.save_dir = path

    def next_img(self):
        if (self.image is not None) or (len(self.images) > 0):
            flg = False
            if not self.save_flg[self.idx]:
                buttonReply = QMessageBox.question(self, "confirm message", "The result is not saved. Do you show the next image?",
                                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if buttonReply == QMessageBox.Yes:
                    flg = True
                else:
                    flg = False
            else:
                flg = True

            if flg:
                if self.idx < len(self.images)-1:
                    self.idx += 1
                    self.points = []
                    self.ori_points = []
                    self.showImage(self.images[self.idx])
                    self.repaint()
                else:
                    QMessageBox.warning(self, "warning message", "This is the last image", QMessageBox.Yes)
        else:
            QMessageBox.warning(self, "warning message", "Select image dir or image file", QMessageBox.Yes)

    def pre_img(self):
        if (self.image is not None) or (len(self.images) > 0):
            flg = False
            if not self.save_flg[self.idx]:
                buttonReply = QMessageBox.question(self, "confirm message", "The result is not saved. Do you select the next image?",
                                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if buttonReply == QMessageBox.Yes:
                    flg = True
                else:
                    flg = False
            else:
                flg = True

            if flg:
                if self.idx > 0:
                    self.idx -= 1
                    self.points = []
                    self.ori_points = []
                    self.showImage(self.images[self.idx])
                    self.repaint()
                else:
                    QMessageBox.warning(self, "warning message", "This is the first image", QMessageBox.Yes)
        else:
            QMessageBox.warning(self, "warning message", "Select image dir or image file", QMessageBox.Yes)

    def showImage(self, path):
        print(path)
        image = cv2.imread(path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        self.ori_h, self.ori_w = image.shape[:2]
        self.image = resize(image, self.SIZE)
        h, w = self.image.shape[:2]
        qimg = QImage(self.image.flatten(), w, h, QImage.Format_RGB888)
        self.le.setPixmap(QPixmap.fromImage(qimg))

    def mousePressEvent(self, event):
        if self.image is not None:
            x = event.pos().x() - self.img_x
            y = event.pos().y() - self.img_y
            if x > 0 and x < self.SIZE:
                if y > 0 and y < self.SIZE:
                    self.points.append((x, y))
                    x_, y_ = reproduce(self.ori_h, self.ori_w, np.asarray([x, y]), self.SIZE)
                    self.ori_points.append((round(x_, 1), round(y_, 1)))

            self.drawPoint()
            self.update()

    def save(self):
        if self.save_flg[self.idx]:
            buttonReply = QMessageBox.question(self, "confirm message", "The result was saved. Do you want to overwrite?",
                                               QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if buttonReply == QMessageBox.Yes:
                flg = True
            else:
                flg = False
        else:
            flg = True

        if flg:
            if (self.image is not None) or (len(self.images) > 0):
                if len(self.ori_points) == 7:
                    self.save_flg[self.idx] = True
                    result = {}
                    result["path"] = self.images[self.idx]
                    result["points"] = self.ori_points
                    self.psets["{}".format(self.idx)] = result
                else:
                    QMessageBox.warning(self, "warning message", "You must plot just 7 points", QMessageBox.Yes)
            else:
                QMessageBox.warning(self, "warning message", "Select image dir or image file", QMessageBox.Yes)

    def drawPoint(self):
        copy = self.image.copy()
        for i, (x, y) in enumerate(self.points):
            cv2.circle(copy, (x, y), 2, (255, 0, 255), -1)
            cv2.putText(copy, str(i+1), (x-10, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 1)

        h, w = copy.shape[:2]
        qimg = QImage(copy.flatten(), w, h, QImage.Format_RGB888)
        self.le.setPixmap(QPixmap.fromImage(qimg))

    def delete(self):
        if (self.image is not None) or (len(self.images) > 0):
            if len(self.points) > 0:
                del self.points[-1]
                del self.ori_points[-1]
                print("delete")

            self.drawPoint()
            self.repaint()
        else:
            QMessageBox.warning(self, "warning message", "Select image dir or image file", QMessageBox.Yes)

    def deleteAll(self):
        if (self.image is not None) or (len(self.images) > 0):
            if len(self.points) > 0:
                self.points.clear()
                self.ori_points.clear()

            self.drawPoint()
            self.repaint()
        else:
            QMessageBox.warning(self, "warning message", "Select image dir or image file", QMessageBox.Yes)

    def get_points(self):
        print(self.psets)

    def export(self):
        if (self.image is not None) or (len(self.images) > 0):
            r = QMessageBox.question(self, "Confirmation", "Do you want to export the results to json file?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if r == QMessageBox.Yes:
                if self.save_dir is None:
                    QMessageBox.warning(self, "warning message", "Select folder to export json file.\nUse 'Select Save Dir' button.", QMessageBox.Yes)
                else:
                    json_file = open(os.path.join(self.save_dir, self.name + '_' + 'results.json'), 'w')
                    json.dump(self.psets, json_file)
                    QMessageBox.information(None, "Information", "results exported", QMessageBox.Ok)
            else:
                pass

        else:
            QMessageBox.warning(self, "warning message", "Select image dir or image file", QMessageBox.Yes)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    w = Widget()
    sys.exit(app.exec_())
