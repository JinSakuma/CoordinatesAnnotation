#!/usr/bin/env python
# coding: utf-8
#

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QFileDialog
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt, QPoint

from util import resize, reproduce

import numpy as np
import os
import cv2
import json


class ExampleWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.left = 300
        self.top = 300
        self.width = 1200
        self.height = 800
        self.img_x = 200
        self.img_y = 0
        self.SIZE = 800
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowTitle('Image View')
        self.setButton()
        self.initUI()

    def initUI(self):
        self.px = None
        self.py = None
        self.points = []
        self.ori_points = []
        self.psets = {}
        self.image = None
        self.images = []
        self.idx = 0
        self.save_dir = None

        self.le = QLabel(self)
        self.le.setPixmap(QPixmap.fromImage(QImage(self.SIZE, self.SIZE, QImage.Format_ARGB32)))
        self.le.move(self.img_x, self.img_y)
        self.show()

    def setButton(self):
        self.btn1 = QPushButton("Open File", self)
        self.btn1.clicked.connect(self.open_file)
        self.btn1.move(0, 0)

        self.btn2 = QPushButton("Open Dir", self)
        self.btn2.move(0, 50)
        self.btn2.clicked.connect(self.open_dir)

        self.btn3 = QPushButton("Select Save Dir", self)
        self.btn3.move(0, 100)
        self.btn3.clicked.connect(self.set_save_dir)

        self.btn4 = QPushButton("Next", self)
        self.btn4.move(0, 150)
        self.btn4.clicked.connect(self.next_img)

        self.btn5 = QPushButton("Previous", self)
        self.btn5.move(0, 200)
        self.btn5.clicked.connect(self.pre_img)

        self.btn6 = QPushButton("Save", self)
        self.btn6.move(0, 250)
        self.btn6.clicked.connect(self.save)

        self.btn7 = QPushButton("Delete A Point", self)
        self.btn7.move(0, 300)
        self.btn7.clicked.connect(self.delete)

        self.btn7 = QPushButton("Delete All Point", self)
        self.btn7.move(0, 350)
        self.btn7.clicked.connect(self.deleteAll)

        self.btn8 = QPushButton("export", self)
        self.btn8.move(0, 400)
        self.btn8.clicked.connect(self.export)

    def open_file(self):
        file = QFileDialog.getOpenFileName(self, 'Open file', "Image files (*.jpg *.gif)")
        print(file)
        if file[0]:
            self.images.append(file[0])
            self.idx += 1
            self.showImage(file[0])

    def open_dir(self):
        path = QFileDialog.getExistingDirectory(self, 'Open dir')
        if path:
            img_names = os.listdir(path)
            for name in img_names:
                self.images.append(os.path.join(path, name))

            self.showImage(self.images[0])

    def set_save_dir(self):
        path = QFileDialog.getExistingDirectory(self, 'Open dir')
        if path:
            self.save_dir = path

    def next_img(self):
        if (self.image is not None) or (len(self.images) > 0):
            if self.idx < len(self.images)-1:
                self.idx += 1
                self.points = []
                self.ori_points = []
                self.showImage(self.images[self.idx])

    def pre_img(self):
        if (self.image is not None) or (len(self.images) > 0):
            if self.idx > 0:
                self.idx -= 1
                self.points = []
                self.ori_points = []
                self.showImage(self.images[self.idx])

    def showImage(self, path):
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
            if x > self.img_x and x < self.img_x+self.SIZE:
                if y > self.img_y and y < self.img_y+self.SIZE:
                    self.points.append((x, y))
                    x_, y_ = reproduce(self.ori_h, self.ori_w, np.asarray([x, y]), self.SIZE)
                    self.ori_points.append((round(x_, 1), round(y_, 1)))

            self.drawPoint()
            self.update()

    def save(self):
        result = {}
        result["path"] = self.images[self.idx]
        result["points"] = self.ori_points
        self.psets["{}".format(self.idx)] = result

    def drawPoint(self):
        copy = self.image.copy()
        for x, y in self.points:
            cv2.circle(copy, (x, y), 5, (255, 0, 255), -1)

        h, w = copy.shape[:2]
        qimg = QImage(copy.flatten(), w, h, QImage.Format_RGB888)
        self.le.setPixmap(QPixmap.fromImage(qimg))

    def delete(self):
        if len(self.points) > 0:
            del self.points[-1]

        self.drawPoint()

    def deleteAll(self):
        if len(self.points) > 0:
            self.points.clear()

        self.drawPoint()

    def get_points(self):
        print(self.psets)

    def export(self):
        json_file = open('test.json', 'w')
        json.dump(self.psets, json_file)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ew = ExampleWidget()
    # ew.main()
    sys.exit(app.exec_())
