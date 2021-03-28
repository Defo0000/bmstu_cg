from PyQt5 import QtWidgets
from PyQt5.QtGui import QPen, QColor
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView, QMessageBox, QButtonGroup
from window import Ui_MainWindow
from PyQt5.QtCore import Qt
import sys
from math import *
import numpy as np

class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.move(200, 0)

        self.method_group = QButtonGroup()
        self.method_group.addButton(self.ui.radioButton_4, 0)
        self.method_group.addButton(self.ui.radioButton_3, 1)
        self.method_group.addButton(self.ui.radioButton_2, 2)
        self.method_group.addButton(self.ui.radioButton, 3)
        self.method_group.addButton(self.ui.radioButton_5, 4)
        self.method_group.addButton(self.ui.radioButton_6, 5)

        self.color_group = QButtonGroup()
        self.color_group.addButton(self.ui.radioButton_10, 0)
        self.color_group.addButton(self.ui.radioButton_12, 1)
        self.color_group.addButton(self.ui.radioButton_8, 2)
        self.color_group.addButton(self.ui.radioButton_11, 3)
        self.color_group.addButton(self.ui.radioButton_7, 4)
        self.color_group.addButton(self.ui.radioButton_9, 5)

        self.ui.pushButton.clicked.connect(self.draw_line)
        self.ui.pushButton_2.clicked.connect(self.draw_spectrum)
        self.ui.pushButton_4.clicked.connect(self.clear)
        self.ui.pushButton_5.clicked.connect(self.exit)
        self.ui.radioButton_4.toggled.connect(self.cda)
        self.create_scene()

        self.current_color = (255, 255, 255)
        self.line_coordinates = [0, 0, 0, 0]
        self.spectrum_params = [0, 0]

    def create_scene(self):
        self.scene = QGraphicsScene()
        graphicView = QGraphicsView(self.scene, self)
        self.pen = QPen(Qt.white, 4)
        graphicView.setGeometry(400, 10, 980, 870)
        self.scene.setBackgroundBrush(QColor(255, 255, 255))
        self.scene.setSceneRect(0, 0, 970, 860)

    def draw_line(self):
        self.get_current_color()
        if ((self.get_line_coordinates()) == 0):
            self.go_to_current_method()

    def draw_spectrum(self):
        self.get_current_color()
        if ((self.get_spectrum_params()) == 0):
            r, angle = self.spectrum_params[0], self.spectrum_params[1]
            padx = 485
            pady = 430
            for angle in range(0, 360, abs(int(angle))):
                self.line_coordinates = [padx, pady, r * sin(radians(angle)) + padx, -r * cos(radians(angle)) + pady]
                self.go_to_current_method()

    def get_spectrum_params(self):
        r = self.ui.lineEdit_5.text()
        if (self.valid_float(r)):
            return -1
        r = float(r)
        if (r <= 0):
            msg_error = QMessageBox()
            msg_error.setIcon(QMessageBox.Critical)
            msg_error.setStandardButtons(QMessageBox.Close)
            msg_error.setWindowTitle("Ошибка ввода данных")
            msg_error.setText("Ошибка: радиус должен быть положительным вещественным числом.")
            msg_error.exec_()

        angle = self.ui.lineEdit_6.text()
        if (self.valid_float(angle)):
            return -1

        angle = float(angle)
        self.spectrum_params = [r, angle]
        return 0

    def get_line_coordinates(self):

        x_begin = self.ui.lineEdit.text()
        if (self.valid_float(x_begin)):
            return -1

        y_begin = self.ui.lineEdit_2.text()
        if (self.valid_float(y_begin)):
            return -1

        x_end = self.ui.lineEdit_3.text()
        if (self.valid_float(x_end)):
            return -1

        y_end = self.ui.lineEdit_4.text()
        if (self.valid_float(y_end)):
            return -1

        x_begin = float(x_begin)
        y_begin = float(y_begin)
        x_end = float(x_end)
        y_end = float(y_end)
        self.line_coordinates = [x_begin, y_begin, x_end, y_end]

        return 0

    def go_to_current_method(self):
        if self.ui.radioButton_4.isChecked():
            self.draw_line_by_dots(self.cda())
        elif self.ui.radioButton_2.isChecked():
            self.draw_line_by_dots(self.brezenham_float())

    def draw_line_by_dots(self, dots):
        for i in range(0, len(dots), 2):
            self.scene.addEllipse(dots[i], dots[i + 1], 1, 1, self.pen)

    def get_current_color(self):
        if self.ui.radioButton_10.isChecked():
            self.current_color = QColor(0, 255, 0)
        elif self.ui.radioButton_12.isChecked():
            self.current_color = QColor(255, 0, 0)
        elif self.ui.radioButton_8.isChecked():
            self.current_color = QColor(0, 0, 255)
        elif self.ui.radioButton_11.isChecked():
            self.current_color = QColor(255, 255, 0)
        elif self.ui.radioButton_7.isChecked():
            self.current_color = QColor(255, 255, 255)
        else:
            self.current_color = QColor(0, 0, 0)
        self.pen.setColor(self.current_color)

    def cda(self):
        line = list()
        x_begin, y_begin = self.line_coordinates[0], self.line_coordinates[1]
        x_end, y_end = self.line_coordinates[2], self.line_coordinates[3]
        dx, dy = x_end - x_begin, y_end - y_begin
        delta_x, delta_y = abs(dx), abs(dy)
        l = delta_x if delta_x > delta_y else delta_y
        dx /= l
        dy /= l
        x, y = x_begin, y_begin
        for i in range(int(l)):
            line.append(round(x))
            line.append(round(y))
            x += dx
            y += dy
        return line

    def brezenham_int(self):
        pass

    def brezenham_float(self):
        line = list()
        x_begin, y_begin = self.line_coordinates[0], self.line_coordinates[1]
        x_end, y_end = self.line_coordinates[2], self.line_coordinates[3]
        x, y = x_begin, y_begin
        dx = x_end - x_begin
        dy = y_end - y_begin
        sx = int(np.sign(dx))
        sy = int(np.sign(dy))
        dx, dy = abs(dx), abs(dy)
        if dx > dy:
            fl = 0
        else:
            fl = 1
            dx, dy = dy, dx
        m = dy/dx
        e = m - 0.5
        for i in range(int(dx)):
            line.append(int(x))
            line.append(int(y))
            if fl == 0:
                if e >= 0:
                    y += sy
                    e -= 1
                x += sx
                e += m
            else:
                if e >= 0:
                    x += sx
                    e -= 1
                y += sy
                e += m
        return line

    def brezenham_antistepping(self):
        pass

    def vu(self):
        pass

    def lib_method(self):
        pass

    def valid_float(self, x):
        msg_error = QMessageBox()
        msg_error.setIcon(QMessageBox.Critical)
        msg_error.setStandardButtons(QMessageBox.Close)
        msg_error.setWindowTitle("Ошибка ввода данных")
        try:
            x = float(x)
            return 0
        except:
            if x == "":
                msg_error.setText("Ошибка: пустое поле ввода.")
                msg_error.exec_()
                return -1
            else:
                msg_error.setText("Ошибка: введено невещественное число.")
                msg_error.exec_()
                return -2

    def clear(self):
        self.scene.clear()

    def exit(self):
        self.close()

app = QtWidgets.QApplication([])
application = mywindow()
application.show()

sys.exit(app.exec())
