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
        self.move(175, 50)

        self.create_scene()

        # Рисование спектра
        mode = QtWidgets.QComboBox(self)
        mode.addItem("Окружность")
        mode.addItem("Эллипс")
        mode.setGeometry(1040, 50, 315, 40)
        mode.setStyleSheet("background-color: rgb(255, 255, 255); "
                               "color: rgb(0, 0, 0)")

        # Выпадающий список алгоритмов
        algorithms = QtWidgets.QComboBox(self)
        algorithms.addItem("Каноническое уравнение")
        algorithms.addItem("Параметрическое уравнение")
        algorithms.addItem("Алгоритм Брезенхема")
        algorithms.addItem("Алгоритм средней точки")
        algorithms.addItem("Библиотечный алгоритм")
        algorithms.setGeometry(1040, 130, 315, 40)
        algorithms.setStyleSheet("background-color: rgb(255, 255, 255); "
                                 "color: rgb(0, 0, 0)")

        # Выпадающий список цветов рисования
        colors = QtWidgets.QComboBox(self)
        colors.addItem("Черный")
        colors.addItem("Белый(цвет фона)")
        colors.addItem("Красный")
        colors.addItem("Зеленый")
        colors.addItem("Синий")
        colors.setGeometry(1040, 210, 315, 40)
        colors.setStyleSheet("background-color: rgb(255, 255, 255); "
                                 "color: rgb(0, 0, 0)")

        self.ui.exit_btn.clicked.connect(self.exit)
        self.ui.clear_btn.clicked.connect(self.clear)

    def create_scene(self):
        self.scene = QGraphicsScene()
        graphicView = QGraphicsView(self.scene, self)
        self.pen = QPen(Qt.white, 1)
        graphicView.setGeometry(25, 25, 1000, 850)
        self.scene.setBackgroundBrush(QColor(255, 255, 255))

    def clear(self):
        self.scene.clear()

    def exit(self):
        self.close()

app = QtWidgets.QApplication([])
application = mywindow()
application.show()

sys.exit(app.exec())