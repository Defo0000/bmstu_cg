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
        self.setWindowTitle("Лабораторная работа № 4")
        self.move(225, 50)

        self.create_scene()

        self.ui.exit_btn.clicked.connect(self.exit)
        self.ui.clear_btn.clicked.connect(self.clear)

        self.r_lbl = QtWidgets.QLabel(self)
        self.r_lbl.setText("  Радиус окр-ти:")
        self.r_lbl.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(0, 0, 0)")
        self.r_lbl.setGeometry(890, 270, 160, 30)

        self.enter_r = QtWidgets.QLineEdit(self)
        self.enter_r.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(0, 0, 0)")
        self.enter_r.setGeometry(1070, 270, 130, 30)

        self.a_lbl = QtWidgets.QLabel(self)
        self.a_lbl.setText("  Полуось а:")
        self.a_lbl.setStyleSheet("background-color: rgb(52, 101, 164); color: rgb(136, 138, 133);")
        self.a_lbl.setGeometry(890, 310, 160, 30)

        self.enter_a = QtWidgets.QLineEdit(self)
        self.enter_a.setStyleSheet("background-color: rgb(52, 101, 164); color: rgb(136, 138, 133);")
        self.enter_a.setGeometry(1070, 310, 130, 30)
        self.enter_a.setDisabled(True)

        self.b_lbl = QtWidgets.QLabel(self)
        self.b_lbl.setText("  Полуось b:")
        self.b_lbl.setStyleSheet("background-color: rgb(52, 101, 164); color: rgb(136, 138, 133);")
        self.b_lbl.setGeometry(890, 350, 160, 30)

        self.enter_b = QtWidgets.QLineEdit(self)
        self.enter_b.setStyleSheet("background-color: rgb(52, 101, 164); color: rgb(136, 138, 133);")
        self.enter_b.setGeometry(1070, 350, 130, 30)
        self.enter_b.setDisabled(True)

        self.begin_spectrum = QtWidgets.QLabel(self)
        self.begin_spectrum.setText("Нач. р.:")
        self.begin_spectrum.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(0, 0, 0)")
        self.begin_spectrum.setGeometry(890, 570, 80, 30)

        self.enter_begin = QtWidgets.QLineEdit(self)
        self.enter_begin.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(0, 0, 0)")
        self.enter_begin.setGeometry(980, 570, 70, 30)
        self.enter_begin.setDisabled(False)

        self.end_spectrum = QtWidgets.QLabel(self)
        self.end_spectrum.setText("Кон. р.:")
        self.end_spectrum.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(0, 0, 0)")
        self.end_spectrum.setGeometry(1060, 570, 80, 30)

        # Рисование спектра
        self.mode = QtWidgets.QComboBox(self)
        self.mode.addItem("Окружность")
        self.mode.addItem("Эллипс")
        self.mode.setGeometry(890, 50, 315, 40)
        self.mode.setStyleSheet("background-color: rgb(255, 255, 255); "
                           "color: rgb(0, 0, 0)")

        # Выпадающий список алгоритмов
        self.algorithms = QtWidgets.QComboBox(self)
        self.algorithms.addItem("Каноническое уравнение")
        self.algorithms.addItem("Параметрическое уравнение")
        self.algorithms.addItem("Алгоритм Брезенхема")
        self.algorithms.addItem("Алгоритм средней точки")
        self.algorithms.addItem("Библиотечный алгоритм")
        self.algorithms.setGeometry(890, 130, 315, 40)
        self.algorithms.setStyleSheet("background-color: rgb(255, 255, 255); "
                                 "color: rgb(0, 0, 0)")

        # Выпадающий список цветов рисования
        self.colors = QtWidgets.QComboBox(self)
        self.colors.addItem("Черный")
        self.colors.addItem("Белый(цвет фона)")
        self.colors.addItem("Красный")
        self.colors.addItem("Зеленый")
        self.colors.addItem("Синий")
        self.colors.setGeometry(890, 210, 315, 40)
        self.colors.setStyleSheet("background-color: rgb(255, 255, 255); "
                             "color: rgb(0, 0, 0)")

        self.mode.activated.connect(self.change_visible)

    def change_visible(self):
        if self.mode.currentText() == "Эллипс":
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

    def create_scene(self):
        self.scene = QGraphicsScene()
        graphicView = QGraphicsView(self.scene, self)
        self.pen = QPen(Qt.white, 1)
        graphicView.setGeometry(25, 25, 850, 850)
        self.scene.setBackgroundBrush(QColor(255, 255, 255))

    def clear(self):
        self.scene.clear()

    def exit(self):
        self.close()

app = QtWidgets.QApplication([])
application = mywindow()
application.show()

sys.exit(app.exec())