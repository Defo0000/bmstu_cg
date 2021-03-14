from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import QPen, QBrush, QColor, QPainter, QFont
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView, QMessageBox, QInputDialog, QDialog, QLineEdit, \
    QDialogButtonBox, QFormLayout
from window import Ui_MainWindow
from PyQt5.QtCore import Qt, QRect
import sys
from math import *


class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.exit)
        self.ui.pushButton_2.clicked.connect(self.enter_scale)
        self.ui.pushButton_3.clicked.connect(self.enter_rotate)
        self.ui.pushButton_4.clicked.connect(self.enter_move)
        self.ui.pushButton_5.clicked.connect(self.show_info)
        self.ui.pushButton_6.clicked.connect(self.undo)
        self.ui.pushButton_7.clicked.connect(self.redo)

        self.actions = []
        self.cur_action = -1

        self.deck = [50, 50, 300, 50, 300, 100, 50, 100]
        self.cellar = [0, 100, 350, 100, 350, 200, 0, 200]
        self.arc_start_angle = 90

        # Инициализация центров выемок в виде колес
        width = (sqrt((self.cellar[0] - self.cellar[2]) ** 2 + (self.cellar[1] - self.cellar[3]) ** 2))
        height = (sqrt((self.cellar[0] - self.cellar[6]) ** 2 + (self.cellar[1] - self.cellar[7]) ** 2))
        self.wheel_r = height / 4
        self.wheels_step = (width - 10 * self.wheel_r) / 4
        x_c = self.cellar[0] + (self.cellar[6] - self.cellar[0]) / 2 + self.wheel_r
        y_c = self.cellar[1] + (self.cellar[7] - self.cellar[1]) / 2
        self.wheels_centers = [x_c, y_c]
        for i in range(1, 5):
            self.wheels_centers.append(x_c + (self.wheels_step + 2 * self.wheel_r) * i)
            self.wheels_centers.append(y_c)

        # Инициализация одного колеса
        r = self.wheel_r
        self.wheel_dots = []
        angle = 0
        while angle < 360:
            x = cos(radians(angle)) * r
            y = - sin(radians(angle)) * r
            self.wheel_dots.append(x)
            self.wheel_dots.append(y)
            angle += 1 / r

        # Инициализация дуги эллипса
        self.ellipse_dots = []
        angle = 180
        x_c = self.deck[0] + (self.deck[2] - self.deck[0]) / 2
        y_c = self.deck[1]
        a, b = x_c - self.deck[0], (x_c - self.deck[0]) / 2
        while angle < 360:
            x = a * cos(radians(angle)) + x_c
            y = b * sin(radians(angle)) + y_c
            self.ellipse_dots.append(x)
            self.ellipse_dots.append(y)
            angle += 1 / (sqrt(a ** 2 + b ** 2))

        # Инициализация боковых полуокружностей
        self.left_arc_dots = []
        x_c = self.cellar[0] + (self.cellar[6] - self.cellar[0]) / 2
        y_c = self.cellar[1] + (self.cellar[7] - self.cellar[1]) / 2
        r = sqrt((self.cellar[0] - x_c) ** 2 + (self.cellar[1] - y_c) ** 2)
        angle = self.arc_start_angle
        end_angle = angle + 180
        while angle < end_angle:
            x = x_c + cos(radians(angle)) * r
            y = y_c - sin(radians(angle)) * r
            self.left_arc_dots.append(x)
            self.left_arc_dots.append(y)
            angle += 1 / r

        self.right_arc_dots = []
        x_c = self.cellar[2] + (self.cellar[4] - self.cellar[2]) / 2
        y_c = self.cellar[3] + (self.cellar[5] - self.cellar[3]) / 2
        angle = self.arc_start_angle + 180
        end_angle = angle + 180
        while angle < end_angle:
            x = x_c + cos(radians(angle)) * r
            y = y_c - sin(radians(angle)) * r
            self.right_arc_dots.append(x)
            self.right_arc_dots.append(y)
            angle += 1 / r

        # Инициализация флюгеля
        height, angle = 50, 8
        x_c = self.deck[0] + (self.deck[2] - self.deck[0]) / 2
        y_c = self.deck[1]

        a, b = x_c - self.deck[0], (x_c - self.deck[0]) / 2

        lx = a * cos(radians(240)) + x_c
        ly = b * sin(radians(240)) + y_c

        rx = a * cos(radians(240 + angle)) + x_c
        hy = b * sin(radians(240 + angle)) + y_c

        self.vane_dots = [lx, ly, lx, ly - height + (hy - ly), lx + height, ly - height + (hy - ly),
                          lx + height, ly - height + (hy - ly) + (rx - lx), rx, ly - height + (hy - ly) + (rx - lx), rx, hy]

        self.copy_deck = [0] * len(self.deck)
        self.copy_cellar = [0] * len(self.cellar)
        self.copy_wheel_r = self.wheel_r
        self.copy_wheels_step = self.wheels_step
        self.copy_wheels_centers = [0] * len(self.wheels_centers)
        self.copy_wheel_dots = [0] * len(self.wheel_dots)
        self.copy_ellipse_dots = [0] * len(self.ellipse_dots)
        self.copy_left_arc_dots = [0] * len(self.left_arc_dots)
        self.copy_right_arc_dots = [0] * len(self.right_arc_dots)
        self.copy_vane_dots = [0] * len(self.vane_dots)

        self.create_scene()

    def copy(self):
        for i in range(len(self.deck)):
            self.copy_deck[i] = self.deck[i]
        for i in range(len(self.cellar)):
            self.copy_cellar[i] = self.cellar[i]
        self.copy_wheel_r = self.wheel_r
        self.copy_wheels_step = self.wheels_step
        for i in range(len(self.wheels_centers)):
            self.copy_wheels_centers[i] = self.wheels_centers[i]
        for i in range(len(self.wheel_dots)):
            self.copy_wheel_dots[i] = self.wheel_dots[i]
        for i in range(len(self.ellipse_dots)):
            self.copy_ellipse_dots[i] = self.ellipse_dots[i]
        for i in range(len(self.left_arc_dots)):
            self.copy_left_arc_dots[i] = self.left_arc_dots[i]
        for i in range(len(self.right_arc_dots)):
            self.copy_right_arc_dots[i] = self.right_arc_dots[i]
        for i in range(len(self.vane_dots)):
            self.copy_vane_dots[i] = self.vane_dots[i]

    def ret(self):
        for i in range(len(self.copy_deck)):
            self.deck[i] = self.copy_deck[i]
        for i in range(len(self.copy_cellar)):
            self.cellar[i] = self.copy_cellar[i]
        self.wheel_r = self.copy_wheel_r
        self.wheels_step = self.copy_wheels_step
        for i in range(len(self.copy_wheels_centers)):
            self.wheels_centers[i] = self.copy_wheels_centers[i]
        for i in range(len(self.copy_wheel_dots)):
            self.wheel_dots[i] = self.copy_wheel_dots[i]
        for i in range(len(self.copy_ellipse_dots)):
            self.ellipse_dots[i] = self.copy_ellipse_dots[i]
        for i in range(len(self.copy_left_arc_dots)):
            self.left_arc_dots[i] = self.copy_left_arc_dots[i]
        for i in range(len(self.copy_right_arc_dots)):
            self.right_arc_dots[i] = self.copy_right_arc_dots[i]
        for i in range(len(self.copy_vane_dots)):
            self.vane_dots[i] = self.copy_vane_dots[i]

    def create_scene(self):
        self.scene = QGraphicsScene()
        graphicView = QGraphicsView(self.scene, self)
        self.pen = QPen(Qt.white, 4)
        graphicView.setGeometry(0, 0, 1400, 800)
        self.draw()

    def draw(self):
        self.draw_deck()
        self.draw_cellar()
        self.draw_arcs()
        self.draw_ellipse()
        self.draw_wheels()
        self.draw_vane()

    def scale(self, x_c, y_c, k_x, k_y):
        if k_x == 0 or k_y == 0:
            self.copy()
        # Масштабирование палубы
        for i in range(0, len(self.deck), 2):
            self.deck[i] = x_c + (self.deck[i] - x_c) * k_x
            self.deck[i + 1] = y_c + (self.deck[i + 1] - y_c) * k_y

        # Масштабирование подводной части лодки
        for i in range(0, len(self.cellar), 2):
            self.cellar[i] = x_c + (self.cellar[i] - x_c) * k_x
            self.cellar[i + 1] = y_c + (self.cellar[i + 1] - y_c) * k_y

        # Масштабирование выемок в виде колес
        width = (sqrt((self.cellar[0] - self.cellar[2]) ** 2 + (self.cellar[1] - self.cellar[3]) ** 2))
        height = (sqrt((self.cellar[0] - self.cellar[6]) ** 2 + (self.cellar[1] - self.cellar[7]) ** 2))
        self.wheel_r = height / 4
        self.wheels_step = (width - 10 * self.wheel_r) / 4

        for i in range(0, 10, 2):
            x = self.wheels_centers[i]
            y = self.wheels_centers[i + 1]
            self.wheels_centers[i] = x_c + (x - x_c) * k_x
            self.wheels_centers[i + 1] = y_c + (y - y_c) * k_y

        # Масштабирование колес
        for i in range(0, len(self.wheel_dots), 2):
            self.wheel_dots[i] = (self.wheel_dots[i]) * k_x
            self.wheel_dots[i + 1] = (self.wheel_dots[i + 1]) * k_y

        # Масштабирование дуги эллипса
        for i in range(0, len(self.ellipse_dots), 2):
            x = self.ellipse_dots[i]
            y = self.ellipse_dots[i+1]
            self.ellipse_dots[i] = x_c + (x - x_c) * k_x
            self.ellipse_dots[i + 1] = y_c + (y - y_c) * k_y

        # Масштабирование флюгеля
        for i in range(0, len(self.vane_dots), 2):
            x = self.vane_dots[i]
            y = self.vane_dots[i + 1]
            self.vane_dots[i] = x_c + (x - x_c) * k_x
            self.vane_dots[i + 1] = y_c + (y - y_c) * k_y

        # Масштабирование боковых полуокружностей
        for i in range(0, len(self.left_arc_dots), 2):
            x = self.left_arc_dots[i]
            y = self.left_arc_dots[i + 1]
            self.left_arc_dots[i] = x_c + (x - x_c) * k_x
            self.left_arc_dots[i + 1] = y_c + (y - y_c) * k_y
        for i in range(0, len(self.right_arc_dots), 2):
            x = self.right_arc_dots[i]
            y = self.right_arc_dots[i + 1]
            self.right_arc_dots[i] = x_c + (x - x_c) * k_x
            self.right_arc_dots[i + 1] = y_c + (y - y_c) * k_y

        self.scene.clear()
        self.draw()

    def rotate(self, x_c, y_c, angle):

        # Поворот "палубы"
        for i in range(0, len(self.deck), 2):
            x = self.deck[i]
            y = self.deck[i+1]
            self.deck[i] = y_c + (x - x_c) * cos(radians(angle)) - (y - y_c) * sin(radians(angle))
            self.deck[i+1] = x_c + (x - x_c) * sin(radians(angle)) + (y - y_c) * cos(radians(angle))

        # Поворот подводной части лодки
        for i in range(0, len(self.cellar), 2):
            x = self.cellar[i]
            y = self.cellar[i+1]
            self.cellar[i] = y_c + (x - x_c) * cos(radians(angle)) - (y - y_c) * sin(radians(angle))
            self.cellar[i+1] = x_c + (x - x_c) * sin(radians(angle)) + (y - y_c) * cos(radians(angle))

        # Поворот боковых полукоружностей
        self.arc_start_angle -= angle
        for i in range(0, len(self.left_arc_dots), 2):
            x = self.left_arc_dots[i]
            y = self.left_arc_dots[i + 1]
            self.left_arc_dots[i] = y_c + (x - x_c) * cos(radians(angle)) - (y - y_c) * sin(radians(angle))
            self.left_arc_dots[i + 1] = x_c + (x - x_c) * sin(radians(angle)) + (y - y_c) * cos(radians(angle))
        for i in range(0, len(self.right_arc_dots), 2):
            x = self.right_arc_dots[i]
            y = self.right_arc_dots[i + 1]
            self.right_arc_dots[i] = y_c + (x - x_c) * cos(radians(angle)) - (y - y_c) * sin(radians(angle))
            self.right_arc_dots[i + 1] = x_c + (x - x_c) * sin(radians(angle)) + (y - y_c) * cos(radians(angle))

        # Поворот выемок в виде колес
        width = (sqrt((self.cellar[0] - self.cellar[2]) ** 2 + (self.cellar[1] - self.cellar[3]) ** 2))
        height = (sqrt((self.cellar[0] - self.cellar[6]) ** 2 + (self.cellar[1] - self.cellar[7]) ** 2))
        self.wheel_r = height / 4
        self.wheels_step = (width - 10 * self.wheel_r) / 4

        for i in range(0, 10, 2):
            x = self.wheels_centers[i]
            y = self.wheels_centers[i + 1]
            self.wheels_centers[i] = y_c + (x - x_c) * cos(radians(angle)) - (y - y_c) * sin(radians(angle))
            self.wheels_centers[i + 1] = x_c + (x - x_c) * sin(radians(angle)) + (y - y_c) * cos(radians(angle))

        # Поворот колес
        for i in range(0, len(self.wheel_dots), 2):
            x = self.wheel_dots[i]
            y = self.wheel_dots[i + 1]
            self.wheel_dots[i] = x * cos(radians(angle)) - y * sin(radians(angle))
            self.wheel_dots[i + 1] = x * sin(radians(angle)) + y * cos(radians(angle))

        # Поворот дуги эллипса
        for i in range(0, len(self.ellipse_dots), 2):
            x = self.ellipse_dots[i]
            y = self.ellipse_dots[i+1]
            self.ellipse_dots[i] = y_c + (x - x_c) * cos(radians(angle)) - (y - y_c) * sin(radians(angle))
            self.ellipse_dots[i + 1] = x_c + (x - x_c) * sin(radians(angle)) + (y - y_c) * cos(radians(angle))

        # Поворот флюгеля
        for i in range(0, len(self.vane_dots), 2):
            x = self.vane_dots[i]
            y = self.vane_dots[i + 1]
            self.vane_dots[i] = y_c + (x - x_c) * cos(radians(angle)) - (y - y_c) * sin(radians(angle))
            self.vane_dots[i + 1] = x_c + (x - x_c) * sin(radians(angle)) + (y - y_c) * cos(radians(angle))

        self.scene.clear()
        self.draw()

    def move(self, d_x, d_y):

        # перенос палубы
        for i in range(0, len(self.deck), 2):
            self.deck[i] += d_x
            self.deck[i+1] += d_y

        # Перенос подводной части лодки
        for i in range(0, len(self.cellar), 2):
            self.cellar[i] += d_x
            self.cellar[i+1] += d_y

        # Перенос боковых полуокружностей
        for i in range(0, len(self.left_arc_dots), 2):
            self.left_arc_dots[i] += d_x
            self.left_arc_dots[i + 1] += d_y
        for i in range(0, len(self.right_arc_dots), 2):
            self.right_arc_dots[i] += d_x
            self.right_arc_dots[i + 1] += d_y

        # Перенос центров выемок в виде колес
        width = (sqrt((self.cellar[0] - self.cellar[2]) ** 2 + (self.cellar[1] - self.cellar[3]) ** 2))
        height = (sqrt((self.cellar[0] - self.cellar[6]) ** 2 + (self.cellar[1] - self.cellar[7]) ** 2))
        self.wheel_r = height / 4
        self.wheels_step = (width - 10 * self.wheel_r) / 4

        for i in range(0, 10, 2):
            self.wheels_centers[i] += d_x
            self.wheels_centers[i + 1] += d_y

        # Перенос колес - не нужен

        # Перенос дуги эллипса
        for i in range(0, len(self.ellipse_dots), 2):
            self.ellipse_dots[i] += d_x
            self.ellipse_dots[i + 1] += d_y

        # Перенос флюгеля
        for i in range(0, len(self.vane_dots), 2):
            self.vane_dots[i] += d_x
            self.vane_dots[i + 1] += d_y

        self.scene.clear()
        self.draw()

    def draw_deck(self):
        x1, y1, x2, y2, x3, y3, x4, y4 = self.deck

        self.scene.addLine(x2, y2, x3, y3, self.pen)
        self.scene.addLine(x1, y1, x4, y4, self.pen)
        self.scene.addLine(x4, y4, x3, y3, self.pen)

    def draw_cellar(self):
        x1, y1, x2, y2, x3, y3, x4, y4 = self.cellar

        self.scene.addLine(x1, y1, x2, y2, self.pen)
        self.scene.addLine(x4, y4, x3, y3, self.pen)

    def draw_arcs(self):
        for i in range(0, len(self.left_arc_dots), 2):
            self.scene.addEllipse(self.left_arc_dots[i], self.left_arc_dots[i+1], 1, 1, self.pen)
        for i in range(0, len(self.right_arc_dots), 2):
            self.scene.addEllipse(self.right_arc_dots[i], self.right_arc_dots[i+1], 1, 1, self.pen)

    def draw_ellipse(self):

        for i in range(0, len(self.ellipse_dots), 2):
            self.scene.addEllipse(self.ellipse_dots[i], self.ellipse_dots[i+1], 1, 1, self.pen)

    def draw_vane(self):
        for i in range(0, len(self.vane_dots) - 3, 2):
            self.scene.addLine(self.vane_dots[i], self.vane_dots[i + 1], self.vane_dots[i + 2], self.vane_dots[i + 3], self.pen)

    def draw_wheels(self):

        r = self.wheel_r
        if r != 0:
            for i in range(0, 10, 2):
                x_c, y_c = self.wheels_centers[i], self.wheels_centers[i+1]
                for j in range(0, len(self.wheel_dots), 2):
                    self.scene.addEllipse(x_c + self.wheel_dots[j], y_c + self.wheel_dots[j+1], 1, 1, self.pen)

    def draw_copy(self):
        self.scene.clear()
        x1, y1, x2, y2, x3, y3, x4, y4 = self.copy_deck

        self.scene.addLine(x2, y2, x3, y3, self.pen)
        self.scene.addLine(x1, y1, x4, y4, self.pen)
        self.scene.addLine(x4, y4, x3, y3, self.pen)

        x1, y1, x2, y2, x3, y3, x4, y4 = self.copy_cellar

        self.scene.addLine(x1, y1, x2, y2, self.pen)
        self.scene.addLine(x4, y4, x3, y3, self.pen)

        for i in range(0, len(self.copy_left_arc_dots), 2):
            self.scene.addEllipse(self.copy_left_arc_dots[i], self.copy_left_arc_dots[i + 1], 1, 1, self.pen)
        for i in range(0, len(self.copy_right_arc_dots), 2):
            self.scene.addEllipse(self.copy_right_arc_dots[i], self.copy_right_arc_dots[i + 1], 1, 1, self.pen)

        for i in range(0, len(self.copy_ellipse_dots), 2):
            self.scene.addEllipse(self.copy_ellipse_dots[i], self.copy_ellipse_dots[i + 1], 1, 1, self.pen)

        for i in range(0, len(self.copy_vane_dots) - 3, 2):
            self.scene.addLine(self.copy_vane_dots[i], self.copy_vane_dots[i + 1], self.copy_vane_dots[i + 2],
                               self.copy_vane_dots[i + 3], self.pen)

        r = self.copy_wheel_r
        if r != 0:
            for i in range(0, 10, 2):
                x_c, y_c = self.copy_wheels_centers[i], self.copy_wheels_centers[i + 1]
                for j in range(0, len(self.copy_wheel_dots), 2):
                    self.scene.addEllipse(x_c + self.copy_wheel_dots[j], y_c + self.copy_wheel_dots[j + 1], 1, 1, self.pen)

    def undo(self):
        if self.cur_action >= 0:
            i = self.cur_action
            if self.actions[i][0] == "s":
                if self.actions[i][3] == 0 or self.actions[i][4] == 0:
                    self.draw_copy()
                    self.ret()
                else:
                    self.scale(self.actions[i][1], self.actions[i][2], 1 / self.actions[i][3], 1 / self.actions[i][4])
            elif self.actions[i][0] == "r":
                self.rotate(self.actions[i][1], self.actions[i][2], -self.actions[i][3])
            else:
                self.move(-self.actions[i][1], -self.actions[i][2])
            self.cur_action -= 1

    def redo(self):
        if self.cur_action + 1 < len(self.actions):
            i = self.cur_action + 1
            if self.actions[i][0] == "s":
                self.scale(self.actions[i][1], self.actions[i][2], self.actions[i][3], self.actions[i][4])
            elif self.actions[i][0] == "r":
                self.rotate(self.actions[i][1], self.actions[i][2], self.actions[i][3])
            else:
                self.move(self.actions[i][1], self.actions[i][2])
            self.cur_action += 1

    def enter_scale(self):

        msg_error = QMessageBox()
        msg_error.setIcon(QMessageBox.Critical)
        msg_error.setStandardButtons(QMessageBox.Close)
        msg_error.setWindowTitle("Ошибка ввода данных")

        msg = QDialog()
        msg.x_c = QLineEdit(msg)
        msg.y_c = QLineEdit(msg)
        msg.k_x = QLineEdit(msg)
        msg.k_y = QLineEdit(msg)

        if self.cur_action != -1:
            i = len(self.actions) - 1
            while self.actions[i][0] != "s" and i >= 0:
                i -= 1
            if i != -1:
                msg.x_c.setText(str(self.actions[i][1]))
                msg.y_c.setText(str(self.actions[i][2]))
                msg.k_x.setText(str(self.actions[i][3]))
                msg.k_y.setText(str(self.actions[i][4]))

        msg.setWindowTitle("Масштабирование")
        msg.move(1150, 150)
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, msg);

        layout = QFormLayout(msg)
        layout.addRow("Центр масштабирования по Х", msg.x_c)
        layout.addRow("Центр масштабирования по У", msg.y_c)
        layout.addRow("Коэффициент по Х", msg.k_x)
        layout.addRow("Коэффициент по У", msg.k_y)
        layout.addWidget(buttonBox)

        buttonBox.accepted.connect(msg.accept)
        buttonBox.rejected.connect(msg.reject)

        res = msg.exec_()
        if res == QDialog.Accepted:
            x_c = msg.x_c.text()
            y_c = msg.y_c.text()
            k_x = msg.k_x.text()
            k_y = msg.k_y.text()
            flag = False
            try:
                x_c = float(x_c)
                y_c = float(y_c)
                k_x = float(k_x)
                k_y = float(k_y)
            except:
                if x_c == "":
                    flag = True
                    msg_error.setText("Ошибка: поле ввода центра масштабирования по Х пустое.")
                    msg_error.exec_()
                elif y_c == "":
                    flag = True
                    msg_error.setText("Ошибка: поле ввода центра масштабирования Y пустое.")
                    msg_error.exec_()
                elif k_x == "":
                    flag = True
                    msg_error.setText("Ошибка: поле ввода коэффицента масштабирования по Х пустое.")
                    msg_error.exec_()
                elif k_y == "":
                    flag = True
                    msg_error.setText("Ошибка: поле ввода коэффициента масштабирования по Y пустое.")
                    msg_error.exec_()
                else:
                    flag = True
                    msg_error.setText("Ошибка: введенное число не является вещественным.")
                    msg_error.exec_()
            if not flag:
                self.actions = self.actions[:self.cur_action + 1]
                self.actions.append(["s", x_c, y_c, k_x, k_y])
                self.cur_action += 1
                self.scale(x_c, y_c, k_x, k_y)

    def enter_rotate(self):
        msg_error = QMessageBox()
        msg_error.setIcon(QMessageBox.Critical)
        msg_error.setStandardButtons(QMessageBox.Close)
        msg_error.setWindowTitle("Ошибка ввода данных")

        msg = QDialog()
        msg.x_c = QLineEdit(msg)
        msg.y_c = QLineEdit(msg)
        msg.angle = QLineEdit(msg)
        msg.setWindowTitle("Поворот")
        msg.move(1150, 150)
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, msg);

        if self.cur_action != -1:
            i = len(self.actions) - 1
            while self.actions[i][0] != "r" and i >= 0:
                i -= 1
            if i != -1:
                msg.x_c.setText(str(self.actions[i][1]))
                msg.y_c.setText(str(self.actions[i][2]))
                msg.angle.setText(str(self.actions[i][3]))

        layout = QFormLayout(msg)
        layout.addRow("Центр поворота по Х", msg.x_c)
        layout.addRow("Центр поворота по У", msg.y_c)
        layout.addRow("Угол поворота (в градусах, против ч.с.)", msg.angle)
        layout.addWidget(buttonBox)

        buttonBox.accepted.connect(msg.accept)
        buttonBox.rejected.connect(msg.reject)

        res = msg.exec_()
        if res == QDialog.Accepted:
            x_c = msg.x_c.text()
            y_c = msg.y_c.text()
            angle = msg.angle.text()
            flag = False
            try:
                x_c = float(x_c)
                y_c = float(y_c)
                angle = float(angle)
            except:
                if x_c == "":
                    flag = True
                    msg_error.setText("Ошибка: поле Х пустое.")
                    msg_error.exec_()
                elif y_c == "":
                    flag = True
                    msg_error.setText("Ошибка: поле Y пустое.")
                    msg_error.exec_()
                elif angle == "":
                    flag = True
                    msg_error.setText("Ошибка: поле ввода угла пустое.")
                    msg_error.exec_()
                else:
                    flag = True
                    msg_error.setText("Ошибка: введенное число не является вещественным.")
                    msg_error.exec_()
            if not flag:
                self.actions = self.actions[:self.cur_action + 1]
                self.actions.append(["r", x_c, y_c, -angle])
                self.cur_action += 1
                self.rotate(x_c, y_c, -angle)

    def enter_move(self):
        msg_error = QMessageBox()
        msg_error.setIcon(QMessageBox.Critical)
        msg_error.setStandardButtons(QMessageBox.Close)
        msg_error.setWindowTitle("Ошибка ввода данных")

        msg = QDialog()
        msg.d_x = QLineEdit(msg)
        msg.d_y = QLineEdit(msg)
        msg.setWindowTitle("Перенос")
        msg.move(1150, 150)
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, msg);

        if self.cur_action != -1:
            i = len(self.actions) - 1
            while self.actions[i][0] != "m" and i >= 0:
                i -= 1
            if i != -1:
                msg.d_x.setText(str(self.actions[i][1]))
                msg.d_y.setText(str(self.actions[i][2]))

        layout = QFormLayout(msg)
        layout.addRow("Смещение по Х", msg.d_x)
        layout.addRow("Смещение по У", msg.d_y)
        layout.addWidget(buttonBox)

        buttonBox.accepted.connect(msg.accept)
        buttonBox.rejected.connect(msg.reject)

        res = msg.exec_()
        if res == QDialog.Accepted:
            d_x = msg.d_x.text()
            d_y = msg.d_y.text()
            flag = False
            try:
                d_x = float(d_x)
                d_y = float(d_y)
            except:
                if d_x == "":
                    flag = True
                    msg_error.setText("Ошибка: поле Х пустое.")
                    msg_error.exec_()
                elif d_y == "":
                    flag = True
                    msg_error.setText("Ошибка: поле Y пустое.")
                    msg_error.exec_()
                else:
                    flag = True
                    msg_error.setText("Ошибка: введенное число не является вещественным.")
                    msg_error.exec_()
            if not flag:
                self.actions = self.actions[:self.cur_action + 1]
                self.actions.append(["m", d_x, d_y])
                self.cur_action += 1
                self.move(d_x, d_y)

    def show_info(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setWindowTitle("Справка о программе")
        msg.setText("Лабораторная работа №2 по компьютерной графике:\n\n"
                                "Начертить заданный рисунок (подводную лодку), осуществить его перенос, "
                                "поворот и масштабирование.\n\nАвтор: Сироткина Полина, ИУ7-46Б.\n"
                                "Дата: 6 марта 2021 года.")
        msg.exec_()

    def exit(self):
        self.close()

app = QtWidgets.QApplication([])
application = mywindow()
application.show()

sys.exit(app.exec())