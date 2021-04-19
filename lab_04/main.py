from PyQt5 import QtWidgets
from PyQt5.QtGui import QPen, QBrush, QColor
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
        self.setWindowTitle("Лабораторная работа № 4")
        self.move(225, 50)

        self.current_color = QColor(255, 255, 255)
        self.algorithm = "Каноническое уравнение"
        self.mode = "Окружность"

        self.create_scene()

        self.ui.exit_btn.clicked.connect(self.exit)
        self.ui.clear_btn.clicked.connect(self.clear)
        self.ui.draw_btn.clicked.connect(self.draw)

        self.ui.xc_lbl.setText("400")
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

        self.b_lbl = QtWidgets.QLabel(self)
        self.b_lbl.setText("  Полуось b:")
        self.b_lbl.setStyleSheet("background-color: rgb(52, 101, 164); color: rgb(136, 138, 133);")
        self.b_lbl.setGeometry(900, 270, 160, 30)

        self.enter_b = QtWidgets.QLineEdit(self)
        self.enter_b.setStyleSheet("background-color: rgb(52, 101, 164); color: rgb(136, 138, 133);")
        self.enter_b.setGeometry(1080, 270, 130, 30)
        self.enter_b.setDisabled(True)

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

        self.spec_params = QtWidgets.QComboBox(self)
        self.spec_params.addItem("Шаг")
        self.spec_params.addItem("Кол-во окр-тей")
        self.spec_params.setGeometry(900, 480, 165, 30)
        self.spec_params.setStyleSheet("background-color: rgb(255, 255, 255); "
                                "color: rgb(0, 0, 0)")

        self.enter_spec_params = QtWidgets.QLineEdit(self)
        self.enter_spec_params.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(0, 0, 0)")
        self.enter_spec_params.setGeometry(1080, 480, 130, 30)

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
        self.scene.setSceneRect(0, 0, 800, 600)
        graphicView.setGeometry(25, 100, 825, 700)
        self.scene.setBackgroundBrush(QColor(255, 255, 255))

    def draw(self):
        self.algorithm = self.algorithms.currentText()
        self.mode = self.modes.currentText()
        self.current_color = self.convert_to_qcolor(self.colors.currentText())
        if self.mode == "Окружность":
            res = self.get_circle_params()
            if res != -1:
                radius, x_center, y_center = res
                if self.algorithm == "Каноническое уравнение":
                    dots = self.canonical_circle(radius, x_center, y_center)
                    self.draw_circle(dots)
                if self.algorithm == "Параметрическое уравнение":
                    dots = self.parametric_circle(radius, x_center, y_center)
                    self.draw_circle(dots)

    def draw_spectrum(self):
        self.algorithm = self.algorithms.currentText()
        self.mode = self.modes.currentText()
        self.current_color = self.convert_to_qcolor(self.colors.currentText())
        if self.mode == "Окружность":
            res = self.get_circle_spectrum_params()
            if res != -1:
                start, end, k = res
                if self.algorithm == "Параметрическое уравнение":
                    pass

    def convert_to_qcolor(self, s):
        if s == "Черный":
            return QColor(0, 0, 0)
        elif s == "Красный":
            return QColor(255, 0, 0)
        elif s == "Зеленый":
            return QColor(0, 255, 0)
        elif s == "Синий":
            return QColor(0, 0, 255)
        else:
            return QColor(255, 255, 255)

    def draw_circle(self, dots):
        self.pen.setColor(self.current_color)

        for i in range(0, len(dots) - 2, 2):
            self.scene.addLine(dots[i], dots[i + 1], dots[i + 2], dots[i + 3], self.pen)

    def parametric_circle(self, radius, x_center, y_center):

        dots = []

        step = round(1 / radius) + 1
        for angle in range(0, 720, step):
            dots.append(x_center + radius * cos(radians(angle)))
            dots.append(y_center + radius * sin(radians(angle)))

        return dots

    def parametrical_ellipse(self):
        pass

    def canonical_circle(self, radius, x_center, y_center):
        dots = []

        for x in range(int(x_center), int(x_center + radius) + 1):
            y = sqrt(radius * radius - (x - x_center) * (x - x_center)) + y_center
            dots.append(x)
            dots.append(y)

        mirror = []
        n = len(dots)
        for i in range(n - 1, 0, -2):
            mirror.append(dots[i - 1])
            mirror.append(2 * y_center - dots[i])
        for i in range(0, n, 2):
            mirror.append(2 * x_center - dots[i])
            mirror.append(2 * y_center - dots[i + 1])
        for i in range(n - 1, 0, -2):
            mirror.append(2 * x_center - dots[i - 1])
            mirror.append(dots[i])

        return dots + mirror

    def canonical_ellipse(self):
        pass

    def brezenham_circle(self):
        pass

    def brezenham_ellipse(self):
        pass

    def middle_point_circle(self):
        pass

    def middle_point_ellipse(self):
        pass

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
            self.spec_params.removeItem(1)
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

    def get_circle_spectrum_params(self):
        start = self.enter_spec_first.text()
        if self.valid_pos_float(start):
            return -1
        start = float(start)

        end = self.enter_spec_sec.text()
        if self.valid_pos_float(end):
            return -1
        end = float(end)

        k = self.enter_spec_params.text()
        if self.valid_pos_float(k):
            return -1
        k = float(k)

        return start, end, k


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

    def valid_pos_float(self, x):
        msg_error = QMessageBox()
        msg_error.setIcon(QMessageBox.Critical)
        msg_error.setStandardButtons(QMessageBox.Close)
        msg_error.setWindowTitle("Ошибка ввода данных")
        if (self.valid_float(x)):
            return -1
        x = float(x)
        if x < 0:
            msg_error.setText("Ошибка: необходимо ввести неотрицательное число.")
            msg_error.exec_()

    def clear(self):
        self.scene.clear()

    def exit(self):
        self.close()

app = QtWidgets.QApplication([])
application = mywindow()
application.show()

sys.exit(app.exec())