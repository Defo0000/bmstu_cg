from PyQt5 import QtWidgets
from PyQt5.QtGui import QPen, QColor
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView, QMessageBox
from window import Ui_MainWindow
from PyQt5.QtCore import Qt
import sys
import numpy as np
import time
import matplotlib.pyplot as plt

from canonical import *
from parametric import *
from brezenham import *
from middle_point import *

class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Лабораторная работа № 4: генерация окружностей и эллипсов.")
        self.move(225, 50)

        self.current_color = QColor(255, 255, 255)
        self.algorithm = "Каноническое уравнение"
        self.mode = "Окружность"

        self.create_scene()

        self.ui.exit_btn.clicked.connect(self.exit)
        self.ui.clear_btn.clicked.connect(self.clear)
        self.ui.draw_btn.clicked.connect(self.figure)
        self.ui.spectrum_btn.clicked.connect(self.spectrum)

        self.ui.xc_lbl.setText("415")
        self.ui.yc_lbl.setText("300")

        self.r_lbl = QtWidgets.QLabel(self)
        self.r_lbl.setText("  Радиус окр-ти:")
        self.r_lbl.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(0, 0, 0)")
        self.r_lbl.setGeometry(900, 190, 160, 30)

        self.enter_r = QtWidgets.QLineEdit(self)
        self.enter_r.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(0, 0, 0)")
        self.enter_r.setGeometry(1080, 190, 130, 30)
        self.enter_r.setText("150")

        self.a_lbl = QtWidgets.QLabel(self)
        self.a_lbl.setText("  Полуось а:")
        self.a_lbl.setStyleSheet("background-color: rgb(52, 101, 164); color: rgb(136, 138, 133);")
        self.a_lbl.setGeometry(900, 230, 160, 30)

        self.enter_a = QtWidgets.QLineEdit(self)
        self.enter_a.setStyleSheet("background-color: rgb(52, 101, 164); color: rgb(136, 138, 133);")
        self.enter_a.setGeometry(1080, 230, 130, 30)
        self.enter_a.setDisabled(True)
        self.enter_a.setText("200")

        self.b_lbl = QtWidgets.QLabel(self)
        self.b_lbl.setText("  Полуось b:")
        self.b_lbl.setStyleSheet("background-color: rgb(52, 101, 164); color: rgb(136, 138, 133);")
        self.b_lbl.setGeometry(900, 270, 160, 30)

        self.enter_b = QtWidgets.QLineEdit(self)
        self.enter_b.setStyleSheet("background-color: rgb(52, 101, 164); color: rgb(136, 138, 133);")
        self.enter_b.setGeometry(1080, 270, 130, 30)
        self.enter_b.setDisabled(True)
        self.enter_b.setText("100")

        self.spec_first_lbl = QtWidgets.QLabel(self)
        self.spec_first_lbl.setText("    Нач. радиус:")
        self.spec_first_lbl.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(0, 0, 0)")
        self.spec_first_lbl.setGeometry(900, 400, 165, 30)

        self.enter_spec_first = QtWidgets.QLineEdit(self)
        self.enter_spec_first.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(0, 0, 0)")
        self.enter_spec_first.setGeometry(1080, 400, 130, 30)

        self.spec_sec_lbl = QtWidgets.QLabel(self)
        self.spec_sec_lbl.setText("  Конеч. радиус:")
        self.spec_sec_lbl.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(0, 0, 0)")
        self.spec_sec_lbl.setGeometry(900, 440, 165, 30)

        self.enter_spec_sec = QtWidgets.QLineEdit(self)
        self.enter_spec_sec.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(0, 0, 0)")
        self.enter_spec_sec.setGeometry(1080, 440, 130, 30)

        self.spec_step_lbl = QtWidgets.QLabel(self)
        self.spec_step_lbl.setText("  Шаг изменения:")
        self.spec_step_lbl.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(0, 0, 0)")
        self.spec_step_lbl.setGeometry(900, 480, 165, 30)

        self.enter_spec_step = QtWidgets.QLineEdit(self)
        self.enter_spec_step.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(0, 0, 0)")
        self.enter_spec_step.setGeometry(1080, 480, 130, 30)

        self.spec_amount_lbl = QtWidgets.QLabel(self)
        self.spec_amount_lbl.setText("  Кол-во окр-тей:")
        self.spec_amount_lbl.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(0, 0, 0)")
        self.spec_amount_lbl.setGeometry(900, 520, 165, 30)

        self.enter_spec_amount = QtWidgets.QLineEdit(self)
        self.enter_spec_amount.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(0, 0, 0)")
        self.enter_spec_amount.setGeometry(1080, 520, 130, 30)

        self.enter_spec_first.setText("50")
        self.enter_spec_sec.setText("250")
        self.enter_spec_step.setText("20")
        self.enter_spec_amount.setText("")

        # Рисование спектра
        self.modes = QtWidgets.QComboBox(self)
        self.modes.addItem("Окружность")
        self.modes.addItem("Эллипс")
        self.modes.setGeometry(25, 40, 200, 40)
        self.modes.setStyleSheet("background-color: rgb(255, 255, 255); "
                           "color: rgb(0, 0, 0)")

        # Выпадающий список алгоритмов
        self.algorithms = QtWidgets.QComboBox(self)
        self.algorithms.addItem("Каноническое уравнение")
        self.algorithms.addItem("Параметрическое уравнение")
        self.algorithms.addItem("Алгоритм Брезенхема")
        self.algorithms.addItem("Алгоритм средней точки")
        self.algorithms.addItem("Библиотечный алгоритм")
        self.algorithms.setGeometry(275, 40, 290, 40)
        self.algorithms.setStyleSheet("background-color: rgb(255, 255, 255); "
                                 "color: rgb(0, 0, 0)")

        # Выпадающий список цветов рисования
        self.colors = QtWidgets.QComboBox(self)
        self.colors.addItem("Черный")
        self.colors.addItem("Белый(цвет фона)")
        self.colors.addItem("Красный")
        self.colors.addItem("Зеленый")
        self.colors.addItem("Синий")
        self.colors.setGeometry(615, 40, 200, 40)
        self.colors.setStyleSheet("background-color: rgb(255, 255, 255); "
                             "color: rgb(0, 0, 0)")

        self.modes.activated.connect(self.change_visible)

    def create_scene(self):
        self.scene = QGraphicsScene()
        graphicView = QGraphicsView(self.scene, self)
        self.pen = QPen(Qt.red, 3)
        self.scene.setSceneRect(0, 0, 830, 600)
        graphicView.setGeometry(25, 100, 855, 700)
        self.scene.setBackgroundBrush(QColor(255, 255, 255))

    def figure(self):
        self.algorithm = self.algorithms.currentText()
        self.mode = self.modes.currentText()
        self.current_color = self.convert_to_qcolor(self.colors.currentText())
        self.pen.setColor(self.current_color)

        if self.mode == "Окружность":
            res = self.get_circle_params()
            if res != -1:
                radius, x_center, y_center = res

                if self.algorithm == "Каноническое уравнение":
                    dots = canonical_circle(radius, x_center, y_center)
                    self.draw_figure(dots)

                if self.algorithm == "Параметрическое уравнение":
                    dots = parametric_circle(radius, x_center, y_center)
                    self.draw_figure(dots)

                if self.algorithm == "Алгоритм Брезенхема":
                    dots = brezenham_circle(radius, x_center, y_center)
                    self.draw_figure(dots)

                if self.algorithm == "Библиотечный алгоритм":
                    self.scene.addEllipse(x_center - radius, y_center - radius,
                                          2 * radius, 2 * radius, self.pen)
        else:
            res = self.get_ellipse_params()
            if res != -1:
                a, b, x_center, y_center = res

                if self.algorithm == "Каноническое уравнение":
                    dots = canonical_ellipse(a, b, x_center, y_center)
                    self.draw_figure(dots)

                if self.algorithm == "Параметрическое уравнение":
                    dots = parametric_ellipse(a, b, x_center, y_center)
                    self.draw_figure(dots)

                if self.algorithm == "Библиотечный алгоритм":
                    self.scene.addEllipse(x_center - a, y_center - b,
                                          2 * a, 2 * b, self.pen)

                if self.algorithm == "Алгоритм Брезенхема":
                    dots = brezenham_ellipse(a, b, x_center, y_center)
                    self.draw_figure(dots)

    def spectrum(self):
        self.algorithm = self.algorithms.currentText()
        self.mode = self.modes.currentText()
        self.current_color = self.convert_to_qcolor(self.colors.currentText())
        self.pen.setColor(self.current_color)

        if self.mode == "Окружность":
            res = self.get_circle_spectrum_params(False)
            if res != -1:
                self.draw_circle_spectrum(*res)
        else:
            spectrum_params = self.get_ellipse_spectrum_params()
            if spectrum_params != -1:
                self.draw_ellipse_spectrum(*spectrum_params)

    def draw_figure(self, dots):
        for i in range(0, len(dots) - 1, 1):
            self.scene.addLine(dots[i].x, dots[i].y, dots[i + 1].x, dots[i + 1].y, self.pen)

    def draw_circle_spectrum(self, k1, k2, k3, x_center, y_center, mood):
        if self.algorithm == "Каноническое уравнение":
            if mood == "SES":
                for radius in np.arange(k1, k2, k3):
                    dots = canonical_circle(radius, x_center, y_center)
                    self.draw_figure(dots)

            if mood == "SEA":
                step = (k2 - k1) / k3
                for radius in np.arange(k1, k2, step):
                    dots = canonical_circle(radius, x_center, y_center)
                    self.draw_figure(dots)

            if mood == "SSA":
                end = k1 + k2 * k3
                for radius in np.arange(k1, end, k2):
                    dots = canonical_circle(radius, x_center, y_center)
                    self.draw_figure(dots)

        if self.algorithm == "Параметрическое уравнение":
            if mood == "SES":
                for radius in np.arange(k1, k2, k3):
                    dots = parametric_circle(radius, x_center, y_center)
                    self.draw_figure(dots)

            if mood == "SEA":
                step = (k2 - k1) / k3
                for radius in np.arange(k1, k2, step):
                    dots = parametric_circle(radius, x_center, y_center)
                    self.draw_figure(dots)

            if mood == "SSA":
                end = k1 + k2 * k3
                for radius in np.arange(k1, end, k2):
                    dots = parametric_circle(radius, x_center, y_center)
                    self.draw_figure(dots)

        if self.algorithm == "Библиотечный алгоритм":
            if mood == "SES":
                for radius in np.arange(k1, k2, k3):
                    self.scene.addEllipse(x_center - radius, y_center - radius,
                                          2 * radius, 2 * radius, self.pen)

            if mood == "SEA":
                step = (k2 - k1) / k3
                for radius in np.arange(k1, k2, step):
                    self.scene.addEllipse(x_center - radius, y_center - radius,
                                          2 * radius, 2 * radius, self.pen)

            if mood == "SSA":
                end = k1 + k2 * k3
                for radius in np.arange(k1, end, k2):
                    self.scene.addEllipse(x_center - radius, y_center - radius,
                                          2 * radius, 2 * radius, self.pen)

        if self.algorithm == "Алгоритм Брезенхема":
            if mood == "SES":
                for radius in np.arange(k1, k2, k3):
                    dots = brezenham_circle(radius, x_center, y_center)
                    self.draw_figure(dots)

            if mood == "SEA":
                step = (k2 - k1) / k3
                for radius in np.arange(k1, k2, step):
                    dots = brezenham_circle(radius, x_center, y_center)
                    self.draw_figure(dots)

            if mood == "SSA":
                end = k1 + k2 * k3
                for radius in np.arange(k1, end, k2):
                    dots = brezenham_circle(radius, x_center, y_center)
                    self.draw_figure(dots)

    def draw_ellipse_spectrum(self, a, b, x_center, y_center, step, amount):
        if self.algorithm == "Каноническое уравнение":
            for _ in range(amount):
                dots = canonical_ellipse(a, b, x_center, y_center)
                self.draw_figure(dots)
                a += step
                b += step

        if self.algorithm == "Параметрическое уравнение":
            for _ in range(amount):
                dots = parametric_ellipse(a, b, x_center, y_center)
                self.draw_figure(dots)
                a += step
                b += step

        if self.algorithm == "Алгоритм Брезенхема":
            for _ in range(amount):
                dots = brezenham_ellipse(a, b, x_center, y_center)
                self.draw_figure(dots)
                a += step
                b += step

        if self.algorithm == "Библиотечный алгоритм":
            for _ in range(amount):
                self.scene.addEllipse(x_center - a, y_center - b,
                                      2 * a, 2 * b, self.pen)
                a += step
                b += step

    def change_visible(self):
        if self.modes.currentText() == "Эллипс":
            self.enter_a.setDisabled(False)
            self.enter_a.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(0, 0, 0)")
            self.a_lbl.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(0, 0, 0)")
            self.enter_b.setDisabled(False)
            self.enter_b.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(0, 0, 0)")
            self.b_lbl.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(0, 0, 0)")
            self.enter_r.setDisabled(True)
            self.enter_r.setStyleSheet("background-color: rgb(52, 101, 164); color: rgb(136, 138, 133);")
            self.r_lbl.setStyleSheet("background-color: rgb(52, 101, 164); color: rgb(136, 138, 133);")

            self.ui.draw_btn.setText("Построить эллипс")
            self.spec_first_lbl.setText("  Нач. полуось а:")
            self.spec_sec_lbl.setText("  Нач. полуось b:")
            self.spec_amount_lbl.setText(" Кол-во эллипсов:")

            self.enter_spec_first.setText("80")
            self.enter_spec_sec.setText("10")
            self.enter_spec_step.setText("20")
            self.enter_spec_amount.setText("10")
            self.mode = "ellipse"
        else:
            self.enter_a.setDisabled(True)
            self.enter_a.setStyleSheet("background-color: rgb(52, 101, 164); color: rgb(136, 138, 133);")
            self.a_lbl.setStyleSheet("background-color: rgb(52, 101, 164); color: rgb(136, 138, 133);")
            self.enter_b.setDisabled(True)
            self.enter_b.setStyleSheet("background-color: rgb(52, 101, 164); color: rgb(136, 138, 133);")
            self.b_lbl.setStyleSheet("background-color: rgb(52, 101, 164); color: rgb(136, 138, 133);")
            self.enter_r.setDisabled(False)
            self.enter_r.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(0, 0, 0)")
            self.r_lbl.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(0, 0, 0)")
            self.ui.draw_btn.setText("Построить окружность")
            self.spec_first_lbl.setText("    Нач. радиус:")
            self.spec_sec_lbl.setText("  Конеч. радиус:")
            self.spec_amount_lbl.setText("  Кол-во окр-тей:")

            self.enter_spec_first.setText("50")
            self.enter_spec_sec.setText("250")
            self.enter_spec_step.setText("20")
            self.enter_spec_amount.setText("")
            self.mode = "circle"

    def get_circle_params(self):
        x_center = self.ui.xc_lbl.text()
        if self.valid_float(x_center):
            return -1
        x_center = float(x_center)

        y_center = self.ui.yc_lbl.text()
        if self.valid_float(y_center):
            return - 1
        y_center = float(y_center)

        radius = self.enter_r.text()
        if self.valid_pos_float(radius):
            return -1
        radius = float(radius)

        return radius, x_center, y_center

    def get_ellipse_params(self):
        x_center = self.ui.xc_lbl.text()
        if self.valid_float(x_center):
            return -1
        x_center = float(x_center)

        y_center = self.ui.yc_lbl.text()
        if self.valid_float(y_center):
            return - 1
        y_center = float(y_center)

        a = self.enter_a.text()
        if self.valid_pos_float(a):
            return -1
        a = float(a)

        b = self.enter_b.text()
        if self.valid_pos_float(b):
            return -1
        b = float(b)

        return a, b, x_center, y_center

    def get_circle_spectrum_params(self, prnt = True):
        x_center = self.ui.xc_lbl.text()
        if self.valid_float(x_center, prnt):
            return -1
        x_center = float(x_center)

        y_center = self.ui.yc_lbl.text()
        if self.valid_float(y_center, prnt):
            return - 1
        y_center = float(y_center)

        # Возможны 3 комбинации ввода:
        # 1) нач.радиус, конеч.радиус, шаг
        # 2) нач.радиус, конеч.радиус, кол-во
        # 3) нач.радиус, шаг, кол-во
        # Что первое случится, то и возьмется за основу

        start = self.enter_spec_first.text()
        end = self.enter_spec_sec.text()
        step = self.enter_spec_step.text()
        amount = self.enter_spec_amount.text()

        if self.valid_pos_float(start, prnt):
            return -1
        start = float(start)

        if self.valid_pos_float(end, prnt) == -1: # Возможна только третья комбинация
            if self.valid_pos_float(step, prnt):
                return -1
            step = float(step)
            if self.valid_pos_int(amount, prnt):
                return -1
            amount = int(amount)
            return start, step, amount, x_center, y_center, "SSA"
        elif self.valid_pos_float(end, prnt):
            return -1
        end = float(end)

        if start > end:
            msg_error = QMessageBox()
            msg_error.setIcon(QMessageBox.Critical)
            msg_error.setStandardButtons(QMessageBox.Close)
            msg_error.setWindowTitle("Ошибка ввода данных")
            msg_error.setText("Ошибка: начальный радиус окружности больше конечного.")
            msg_error.exec_()
            return -1

        if self.valid_pos_float(step, prnt) == -1:
            if self.valid_pos_int(amount, prnt):
                return -1
            amount = int(amount)
            return start, end, amount, x_center, y_center, "SEA"
        elif self.valid_pos_float(step, prnt):
            return -1

        step = float(step)
        return start, end, step, x_center, y_center, "SES"

    def get_ellipse_spectrum_params(self):
        x_center = self.ui.xc_lbl.text()
        y_center = self.ui.yc_lbl.text()
        a = self.enter_spec_first.text()
        b = self.enter_spec_sec.text()
        step = self.enter_spec_step.text()
        amount = self.enter_spec_amount.text()

        if self.valid_float(x_center):
            return -1
        x_center = float(x_center)

        if self.valid_float(y_center):
            return - 1
        y_center = float(y_center)

        if self.valid_pos_float(a):
            return -1
        a = float(a)

        if self.valid_pos_float(b):
            return -1
        b = float(b)

        if self.valid_pos_float(step):
            return -1
        step = float(step)

        if self.valid_pos_int(amount):
            return -1
        amount = int(amount)

        return a, b, x_center, y_center, step, amount

    def convert_to_qcolor(self, s):
        if s == "Черный":
            return QColor(0, 0, 0)
        if s == "Красный":
            return QColor(255, 0, 0)
        if s == "Зеленый":
            return QColor(0, 255, 0)
        if s == "Синий":
            return QColor(0, 0, 255)
        if s == "Белый(цвет фона)":
            return QColor(255, 255, 255)

    def valid_float(self, x, prnt = True):
        msg_error = QMessageBox()
        msg_error.setIcon(QMessageBox.Critical)
        msg_error.setStandardButtons(QMessageBox.Close)
        msg_error.setWindowTitle("Ошибка ввода данных")
        try:
            x = float(x)
            return 0
        except:
            if x == "":
                if prnt:
                    msg_error.setText("Ошибка: пустое поле ввода.")
                    msg_error.exec_()
                return -1
            else:
                if prnt:
                    msg_error.setText("Ошибка: введено невещественное число.")
                    msg_error.exec_()
                return -2

    def valid_pos_int(self, x, prnt = True):
        msg_error = QMessageBox()
        msg_error.setIcon(QMessageBox.Critical)
        msg_error.setStandardButtons(QMessageBox.Close)
        msg_error.setWindowTitle("Ошибка ввода данных")
        try:
            x = int(x)
            return 0
        except:
            if x == "":
                if prnt:
                    msg_error.setText("Ошибка: пустое поле ввода.")
                    msg_error.exec_()
                return -1
            elif x <= 0:
                if prnt:
                    msg_error.setText("Ошибка: количество не может быть неположительным.")
                    msg_error.exec_()
                return -1
            else:
                if prnt:
                    msg_error.setText("Ошибка: введено невещественное число.")
                    msg_error.exec_()
                return -2

    def valid_pos_float(self, x, prnt = True):
        msg_error = QMessageBox()
        msg_error.setIcon(QMessageBox.Critical)
        msg_error.setStandardButtons(QMessageBox.Close)
        msg_error.setWindowTitle("Ошибка ввода данных")
        res = self.valid_float(x, prnt)
        if res:
            return res
        x = float(x)
        if x < 0:
            if prnt:
                msg_error.setText("Ошибка: необходимо ввести неотрицательное число.")
                msg_error.exec_()
            return -3

    def clear(self):
        self.scene.clear()

    def exit(self):
        self.close()

app = QtWidgets.QApplication([])
application = mywindow()
application.show()

sys.exit(app.exec())