from PyQt5 import QtWidgets
from PyQt5.QtGui import QPen, QColor
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView, QMessageBox, QButtonGroup
from window import Ui_MainWindow
from PyQt5.QtCore import Qt
import sys
from math import *
import numpy as np
import time

import matplotlib.pyplot as plt

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
        self.ui.pushButton_3.clicked.connect(self.analys_time)
        self.ui.pushButton_6.clicked.connect(self.analys_stepping)
        self.ui.pushButton_4.clicked.connect(self.clear)
        self.ui.pushButton_5.clicked.connect(self.exit)
        self.create_scene()

        self.current_color = [0, 0, 0]
        self.center = [485, 430]
        self.line_coordinates = [0, 0, 1, 1]
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
            for angle in range(0, 360, abs(int(angle))):
                self.line_coordinates = [self.center[0], self.center[1],
                     r * sin(radians(angle)) + self.center[0], -r * cos(radians(angle)) + self.center[1]]
                self.go_to_current_method()

    def get_current_color(self):
        if self.ui.radioButton_10.isChecked():
            self.current_color = [0, 255, 0]
        elif self.ui.radioButton_12.isChecked():
            self.current_color = [255, 0, 0]
        elif self.ui.radioButton_8.isChecked():
            self.current_color = [0, 0, 255]
        elif self.ui.radioButton_11.isChecked():
            self.current_color = [255, 255, 0]
        elif self.ui.radioButton_7.isChecked():
            self.current_color = [255, 255, 255]
        else:
            self.current_color = [0, 0, 0]

    def go_to_current_method(self):
        if self.ui.radioButton_4.isChecked():
            self.draw_line_by_dots(self.cda())
        elif self.ui.radioButton_3.isChecked():
            self.draw_line_by_dots(self.brezenham_int())
        elif self.ui.radioButton_2.isChecked():
            self.draw_line_by_dots(self.brezenham_float())
        elif self.ui.radioButton.isChecked():
            self.draw_line_by_dots(self.brezenham_smooth())
        elif self.ui.radioButton_5.isChecked():
            self.draw_line_by_dots(self.vu())
        elif self.ui.radioButton_6.isChecked():
            self.lib_method()

    def draw_line_by_dots(self, dots):
        for i in range(0, len(dots), 3):
            self.pen.setColor(QColor(int(dots[i + 2][0]), int(dots[i + 2][1]), int(dots[i + 2][2])))
            self.scene.addEllipse(dots[i], dots[i + 1], 1, 1, self.pen)

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
            line.append(self.current_color)
            x += dx
            y += dy
        return line

    def brezenham_int(self):
        line = list()
        x_begin, y_begin = int(self.line_coordinates[0]), int(self.line_coordinates[1])
        x_end, y_end = int(self.line_coordinates[2]), int(self.line_coordinates[3])
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
        e = dy + dy - dx
        for _ in range(dx):
            line.append(x)
            line.append(y)
            line.append(self.current_color)
            if fl:
                if e >= 0:
                    x += sx
                    e -= dx + dx
                y += sy
            else:
                if e >= 0:
                    y += sy
                    e -= dx + dx
                x += sx
            e += dy + dy
        return line

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
            line.append(self.current_color)
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

    def brezenham_smooth(self):
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
        e = 0.5
        w = 1 - m

        if not fl:
            for i in range(int(dx)):
                line.append(int(x))
                line.append(int(y + sy))
                temp_color = self.current_color[:]
                for j in range(3):
                    temp_color[j] *= e
                line.append(temp_color)
                if e >= w:
                    y += sy
                    e -= w + m
                x += sx
                e += m
        else:
            for i in range(int(dx)):
                line.append(int(x + sx))
                line.append(int(y))
                temp_color = self.current_color[:]
                for j in range(3):
                    temp_color[j] *= e
                line.append(temp_color)
                if e >= w:
                    x += sx
                    e -= w + m
                y += sy
                e += m

        return line

    def vu(self):
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
        e = -1

        if not fl:
            for i in range(int(dx)):
                line.append(int(x))
                line.append(int(y))
                temp_color = self.current_color[:]
                for j in range(3):
                    temp_color[j] *= (1 - e)
                line.append(temp_color)

                line.append(int(x))
                line.append(int(y + sy))
                temp_color = self.current_color[:]
                for j in range(3):
                    temp_color[j] *= (1 + e)
                line.append(temp_color)
                e += m
                if e >= 0:
                    y += sy
                    e -= 1
                x += sx
        else:
            for i in range(int(dx)):
                line.append(int(x))
                line.append(int(y))
                temp_color = self.current_color[:]
                for j in range(3):
                    temp_color[j] *= (1 - e)
                line.append(temp_color)

                line.append(int(x + sx))
                line.append(int(y))
                temp_color = self.current_color[:]
                for j in range(3):
                    temp_color[j] *= (1 + e)
                line.append(temp_color)
                e += m
                if e >= 0:
                    x += sx
                    e -= 1
                y += sy
        return line

    def lib_method(self):
        x_begin, y_begin = self.line_coordinates[0], self.line_coordinates[1]
        x_end, y_end = self.line_coordinates[2], self.line_coordinates[3]
        self.scene.addLine(x_begin, y_begin, x_end, y_end, self.pen)

    def analys_time(self):
        self.pen.setColor(QColor(255, 255, 255))
        times = [0] * 6

        start = time.time()
        self.line_coordinates = [0, 0, 300, 600]
        r, angle = 300, 15
        for angle in range(0, 360 * 20, abs(int(angle))):
            self.line_coordinates = [self.center[0], self.center[1],
                                     r * sin(radians(angle)) + self.center[0],
                                     -r * cos(radians(angle)) + self.center[1]]
            self.cda()
        end = time.time()
        times[0] = end - start

        start = time.time()
        self.line_coordinates = [0, 0, 300, 600]
        r, angle = 300, 15
        for angle in range(0, 360 * 20, abs(int(angle))):
            self.line_coordinates = [self.center[0], self.center[1],
                                     r * sin(radians(angle)) + self.center[0],
                                     -r * cos(radians(angle)) + self.center[1]]
            self.brezenham_int()
        end = time.time()
        times[1] = end - start

        start = time.time()
        self.line_coordinates = [0, 0, 300, 600]
        r, angle = 300, 15
        for angle in range(0, 360 * 20, abs(int(angle))):
            self.line_coordinates = [self.center[0], self.center[1],
                                     r * sin(radians(angle)) + self.center[0],
                                     -r * cos(radians(angle)) + self.center[1]]
            self.brezenham_float()
        end = time.time()
        times[2] = end - start

        start = time.time()
        self.line_coordinates = [0, 0, 300, 600]
        r, angle = 300, 15
        for angle in range(0, 360 * 20, abs(int(angle))):
            self.line_coordinates = [self.center[0], self.center[1],
                                     r * sin(radians(angle)) + self.center[0],
                                     -r * cos(radians(angle)) + self.center[1]]
            self.brezenham_smooth()
        end = time.time()
        times[3] = end - start

        start = time.time()
        self.line_coordinates = [0, 0, 360 * 3, 600]
        r, angle = 300, 15
        for angle in range(0, 360 * 20, abs(int(angle))):
            self.line_coordinates = [self.center[0], self.center[1],
                                     r * sin(radians(angle)) + self.center[0],
                                     -r * cos(radians(angle)) + self.center[1]]
            self.vu()
        end = time.time()
        times[4] = end - start

        start = time.time()
        self.line_coordinates = [0, 0, 300, 600]
        r, angle = 300, 15
        for angle in range(0, 360 * 20, abs(int(angle))):
            self.line_coordinates = [self.center[0], self.center[1],
                                     r * sin(radians(angle)) + self.center[0],
                                     -r * cos(radians(angle)) + self.center[1]]
            self.lib_method()
        end = time.time()
        times[5] = end - start

        fig, ax = plt.subplots()
        plt.title("Сравнение алгоритмов")
        ax.bar(["ЦДА", "Брезенхем\n(int)", "Брезенхем\n(float)", "Брезенхем\n(сглаживание)",
                "Ву", "Библиотечный\nметод"], times)
        ax.set_facecolor('white')
        ax.set_xlabel('Алгоритм')
        ax.set_ylabel('Время')
        fig.set_facecolor('white')
        fig.set_figwidth(8)
        fig.set_figheight(4)

        plt.show()

        self.scene.clear()

    def analys_stepping(self):
        self.pen.setColor(QColor(255, 255, 255))
        steppings = []
        r, angle = 300, 15
        for i in range(angle, 90, angle):
            self.line_coordinates = [self.center[0], self.center[1],
                                     r * sin(radians(i)) + self.center[0],
                                     -r * cos(radians(i)) + self.center[1]]
            xb, yb = self.line_coordinates[0], self.line_coordinates[1]
            xe, ye = self.line_coordinates[2], self.line_coordinates[3]
            length = sqrt((xb-xe) ** 2 + (yb-ye) ** 2)
            dx = abs(xe-xb)
            dy = abs(ye-yb)
            steppings.append([i, length / min(dx, dy)])
        x = []
        y = []
        for i in range(len(steppings)):
            x.append(steppings[i][0])
            y.append(steppings[i][1])

        plt.plot(x, y)
        plt.xlabel("Угол в градусах")
        plt.ylabel("Кол-во ступенек")
        plt.show()


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

    def show_color_error(self):
        msg_error = QMessageBox()
        msg_error.setIcon(QMessageBox.Critical)
        msg_error.setStandardButtons(QMessageBox.Close)
        msg_error.setWindowTitle("Ошибка ввода данных")
        msg_error.setText("Необходимо выбрать один из предложенных цветов.")
        msg_error.exec_()

    def show_method_error(self):
        msg_error = QMessageBox()
        msg_error.setIcon(QMessageBox.Critical)
        msg_error.setStandardButtons(QMessageBox.Close)
        msg_error.setWindowTitle("Ошибка ввода данных")
        msg_error.setText("Необходимо выбрать один из предложенных методов.")
        msg_error.exec_()

    def clear(self):
        self.scene.clear()

    def exit(self):
        self.close()

app = QtWidgets.QApplication([])
application = mywindow()
application.show()

sys.exit(app.exec())
