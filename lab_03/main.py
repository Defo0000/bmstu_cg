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
        self.ui.radioButton_4.setChecked(True)

        self.color_group = QButtonGroup()
        self.color_group.addButton(self.ui.radioButton_10, 0)
        self.color_group.addButton(self.ui.radioButton_12, 1)
        self.color_group.addButton(self.ui.radioButton_8, 2)
        self.color_group.addButton(self.ui.radioButton_11, 3)
        self.color_group.addButton(self.ui.radioButton_7, 4)
        self.color_group.addButton(self.ui.radioButton_9, 5)
        self.ui.radioButton_10.setChecked(True)

        self.ui.pushButton.clicked.connect(self.draw_line)
        self.ui.pushButton_2.clicked.connect(self.draw_spectrum)
        self.ui.pushButton_3.clicked.connect(self.analysys_time)
        self.ui.pushButton_6.clicked.connect(self.analysys_stepping)
        self.ui.pushButton_4.clicked.connect(self.clear)
        self.ui.pushButton_5.clicked.connect(self.exit)
        self.create_scene()

        self.ui.lineEdit.setText("200")
        self.ui.lineEdit_2.setText("400")
        self.ui.lineEdit_3.setText("800")
        self.ui.lineEdit_4.setText("300")

        self.ui.lineEdit_5.setText("400")
        self.ui.lineEdit_6.setText("5")

        self.current_color = [0, 0, 0]
        self.center = [485, 430]

        self.ui.lineEdit_8.setText(str(self.center[0]))
        self.ui.lineEdit_7.setText(str(self.center[1]))

        self.line_coordinates = [0, 0, 1, 1]
        self.spectrum_params = [0, 0]

    def create_scene(self):
        self.scene = QGraphicsScene()
        graphicView = QGraphicsView(self.scene, self)
        self.pen = QPen(Qt.white, 1)
        graphicView.setGeometry(400, 10, 980, 870)
        self.scene.setBackgroundBrush(QColor(0, 0, 0))
        self.scene.setSceneRect(0, 0, 970, 860)

    def draw_line(self):
        self.get_current_color()
        if ((self.get_line_coordinates()) == 0):
            self.go_to_current_method()

    def draw_spectrum(self):
        self.get_current_color()
        if ((self.get_spectrum_params()) == 0 and self.get_center() == 0):
            self.line_coordinates = [self.center[0], self.center[1], self.center[0] + 1, self.center[1] + 1]
            r, angle = self.spectrum_params[0], self.spectrum_params[1]
            if self.go_to_current_method() != -1:
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
            self.scene.addLine(dots[i], dots[i + 1], dots[i], dots[i + 1], self.pen)

    def cda(self):
        line = list()
        x_begin, y_begin = int(self.line_coordinates[0]), int(self.line_coordinates[1])
        x_end, y_end = int(self.line_coordinates[2]), int(self.line_coordinates[3])
        if (x_end == x_begin) and (y_end == y_begin):
            line.append(x_begin)
            line.append(y_begin)
            line.append(self.current_color)
            return line
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
        if (x_end == x_begin) and (y_end == y_begin):
            line.append(x_begin)
            line.append(y_begin)
            line.append(self.current_color)
            return line
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
        x_begin, y_begin = int(self.line_coordinates[0]), int(self.line_coordinates[1])
        x_end, y_end = int(self.line_coordinates[2]), int(self.line_coordinates[3])
        if fabs(x_end - x_begin) < 1e-5 and fabs(y_end - y_begin) < 1e-5:
            line.append(x_begin)
            line.append(y_begin)
            line.append(self.current_color)
            return line
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
        if fabs(x_end - x_begin) < 1e-5 and fabs(y_end - y_begin) < 1e-5:
            line.append(x_begin)
            line.append(y_begin)
            line.append(self.current_color)
            return line
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

        if fabs(x_end - x_begin) < 1e-5 and fabs(y_end - y_begin) < 1e-5:
            line.append(x_begin)
            line.append(y_begin)
            line.append(self.current_color)
            return line

        dx = x_end - x_begin
        dy = y_end - y_begin

        m = 1
        if fabs(dy) > fabs(dx):
            if y_begin > y_end:
                x_begin, x_end = x_end, x_begin
                y_begin, y_end = y_end, y_begin
            if dy != 0:
                m = dx / dy
            for y in range(round(y_begin), round(y_end) + 1):
                d1 = x_begin - floor(x_begin)
                d2 = 1 - d1
                line.append(int(x_begin))
                line.append(y)
                temp_color = self.current_color[:]
                for j in range(3):
                    temp_color[j] = temp_color[j] * round(fabs(d2))
                line.append(temp_color)
                line.append(int(x_begin) + 1)
                line.append(y)
                temp_color = self.current_color[:]
                for j in range(3):
                    temp_color[j] = temp_color[j] * round(fabs(d1))
                line.append(temp_color)
                x_begin += m
        else:
            if x_begin > x_end:
                x_begin, x_end = x_end, x_begin
                y_begin, y_end = y_end, y_begin

            if dx != 0:
                m = dy / dx
            for x in range(round(x_begin), round(x_end) + 1):
                d1 = y_begin - floor(y_begin)
                d2 = 1 - d1
                line.append(x)
                line.append(int(y_begin))
                temp_color = self.current_color[:]
                for j in range(3):
                    temp_color[j] = temp_color[j] * round(fabs(d2))
                line.append(temp_color)
                line.append(x)
                line.append(int(y_begin) + 1)
                temp_color = self.current_color[:]
                for j in range(3):
                    temp_color[j] = temp_color[j] * round(fabs(d1))
                line.append(temp_color)
                y_begin += m
        return line

    def lib_method(self):
        self.get_current_color()
        self.pen.setColor(QColor(self.current_color[0], self.current_color[1], self.current_color[2]))
        x_begin, y_begin = self.line_coordinates[0], self.line_coordinates[1]
        x_end, y_end = self.line_coordinates[2], self.line_coordinates[3]
        self.scene.addLine(x_begin, y_begin, x_end, y_end, self.pen)

    def analysys_time(self):
        self.pen.setColor(QColor(255, 255, 255))
        times = [0] * 6

        reps = 20

        start = time.time()
        self.line_coordinates = [0, 0, 300, 600]
        r, angle = 300, 15
        for angle in range(0, 360 * reps, abs(int(angle))):
            self.line_coordinates = [self.center[0], self.center[1],
                                     r * sin(radians(angle)) + self.center[0],
                                     -r * cos(radians(angle)) + self.center[1]]
            self.cda()
        end = time.time()
        times[0] = end - start

        start = time.time()
        self.line_coordinates = [0, 0, 300, 600]
        r, angle = 300, 15
        for angle in range(0, 360 * reps, abs(int(angle))):
            self.line_coordinates = [self.center[0], self.center[1],
                                     r * sin(radians(angle)) + self.center[0],
                                     -r * cos(radians(angle)) + self.center[1]]
            self.brezenham_int()
        end = time.time()
        times[1] = end - start

        start = time.time()
        self.line_coordinates = [0, 0, 300, 600]
        r, angle = 300, 15
        for angle in range(0, 360 * reps, abs(int(angle))):
            self.line_coordinates = [self.center[0], self.center[1],
                                     r * sin(radians(angle)) + self.center[0],
                                     -r * cos(radians(angle)) + self.center[1]]
            self.brezenham_float()
        end = time.time()
        times[2] = end - start

        start = time.time()
        self.line_coordinates = [0, 0, 300, 600]
        r, angle = 300, 15
        for angle in range(0, 360 * reps, abs(int(angle))):
            self.line_coordinates = [self.center[0], self.center[1],
                                     r * sin(radians(angle)) + self.center[0],
                                     -r * cos(radians(angle)) + self.center[1]]
            self.brezenham_smooth()
        end = time.time()
        times[3] = end - start

        start = time.time()
        self.line_coordinates = [0, 0, 360, 600]
        r, angle = 300, 15
        for angle in range(0, 360 * reps, abs(int(angle))):
            self.line_coordinates = [self.center[0], self.center[1],
                                     r * sin(radians(angle)) + self.center[0],
                                     -r * cos(radians(angle)) + self.center[1]]
            self.vu()
        end = time.time()
        times[4] = end - start

        start = time.time()
        self.line_coordinates = [0, 0, 300, 600]
        r, angle = 300, 15
        for angle in range(0, 360 * reps, abs(int(angle))):
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

    def analysys_stepping(self):

        self.pen.setColor(QColor(255, 255, 255))
        steppings = []
        r, angle = 300, 5
        for i in range(angle, 90, angle):
            self.line_coordinates = [self.center[0], self.center[1],
                                     r * sin(radians(i)) + self.center[0],
                                     -r * cos(radians(i)) + self.center[1]]
            line = self.cda()
            xb, yb = line[0], line[1]
            xe, ye = line[len(line) - 3], line[len(line) - 2]
            dx = abs(xe-xb)
            dy = abs(ye-yb)
            steppings.append([i, min(dx, dy)])
        x = []
        y = []
        for i in range(len(steppings)):
            x.append(steppings[i][0])
            y.append(steppings[i][1])

        plt.plot(x, y, color = "r", label = "ЦДА")
        plt.xlabel("Угол в градусах")
        plt.ylabel("Кол-во ступенек")
        plt.legend()

        steppings = []
        r, angle = 300, 5
        for i in range(angle, 90, angle):
            self.line_coordinates = [self.center[0], self.center[1],
                                     r * sin(radians(i)) + self.center[0],
                                     -r * cos(radians(i)) + self.center[1]]
            line = self.brezenham_int()
            xb, yb = line[0], line[1]
            xe, ye = line[len(line) - 3], line[len(line) - 2]
            dx = abs(xe - xb)
            dy = abs(ye - yb)
            steppings.append([i, min(dx, dy)])
        x = []
        y = []
        for i in range(len(steppings)):
            x.append(steppings[i][0])
            y.append(steppings[i][1])

        plt.plot(x, y, color="g", label="Брезенхем(int)")
        plt.xlabel("Угол в градусах")
        plt.ylabel("Кол-во ступенек")
        plt.legend()

        steppings = []
        r, angle = 300, 5
        for i in range(angle, 90, angle):
            self.line_coordinates = [self.center[0], self.center[1],
                                     r * sin(radians(i)) + self.center[0],
                                     -r * cos(radians(i)) + self.center[1]]
            line = self.brezenham_float()
            xb, yb = line[0], line[1]
            xe, ye = line[len(line) - 3], line[len(line) - 2]
            dx = abs(xe - xb)
            dy = abs(ye - yb)
            steppings.append([i, min(dx, dy)])
        x = []
        y = []
        for i in range(len(steppings)):
            x.append(steppings[i][0])
            y.append(steppings[i][1])

        plt.plot(x, y, color="b", label="Брезенхем(float)")
        plt.xlabel("Угол в градусах")
        plt.ylabel("Кол-во ступенек")
        plt.legend()

        steppings = []
        r, angle = 300, 5
        for i in range(angle, 90, angle):
            self.line_coordinates = [self.center[0], self.center[1],
                                     r * sin(radians(i)) + self.center[0],
                                     -r * cos(radians(i)) + self.center[1]]
            line = self.brezenham_smooth()
            xb, yb = line[0], line[1]
            xe, ye = line[len(line) - 3], line[len(line) - 2]
            dx = abs(xe - xb)
            dy = abs(ye - yb)
            steppings.append([i, min(dx, dy)])
        x = []
        y = []
        for i in range(len(steppings)):
            x.append(steppings[i][0])
            y.append(steppings[i][1])

        plt.plot(x, y, color="y", label="Брезенхем(сглаживание)")
        plt.xlabel("Угол в градусах")
        plt.ylabel("Кол-во ступенек")
        plt.legend()

        steppings = []
        r, angle = 300, 1
        for i in range(angle, 90, angle):
            self.line_coordinates = [self.center[0], self.center[1],
                                     r * sin(radians(i)) + self.center[0],
                                     -r * cos(radians(i)) + self.center[1]]
            line = self.vu()
            xb, yb = line[0], line[1]
            xe, ye = line[len(line) - 3], line[len(line) - 2]
            dx = abs(xe - xb)
            dy = abs(ye - yb)
            steppings.append([i, min(dx, dy)])
        x = []
        y = []
        for i in range(len(steppings)):
            x.append(steppings[i][0])
            y.append(steppings[i][1])

        plt.plot(x, y, color="c", label="ВУ")
        plt.xlabel("Угол в градусах")
        plt.ylabel("Кол-во ступенек")
        length = sqrt((self.line_coordinates[0] - self.line_coordinates[2]) ** 2 +
        (self.line_coordinates[1] - self.line_coordinates[3]) ** 2)
        plt.title("Длина отрезка: " + str(int(length)))
        plt.legend()

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
            return -1
        angle = self.ui.lineEdit_6.text()
        if (self.valid_float(angle)):
            return -1
        angle = float(angle)
        if int(angle) == 0:
            msg_error = QMessageBox()
            msg_error.setIcon(QMessageBox.Critical)
            msg_error.setStandardButtons(QMessageBox.Close)
            msg_error.setWindowTitle("Ошибка ввода данных")
            msg_error.setText("Ошибка: модуль величины угла не может быть меньше 1.")
            msg_error.exec_()
            return -1
        self.spectrum_params = [r, angle]
        return 0

    def get_center(self):
        x = self.ui.lineEdit_8.text()
        y = self.ui.lineEdit_7.text()
        if (self.valid_float(x)):
            return -1
        if (self.valid_float(y)):
            return -1
        x = float(x)
        y = float(y)
        self.center = [x, y]
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
