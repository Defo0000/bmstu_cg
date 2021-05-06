from PyQt5 import QtWidgets
from PyQt5.QtGui import QPen, QColor, QFont
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView, QMessageBox, QLineEdit, QTableWidgetItem, QPushButton
from PyQt5.QtCore import Qt
from window import Ui_MainWindow
import sys
import time
import numpy as np

class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y


class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Лабораторная работа № 6: Реализация и исследование построчного алгоритма"
                            " затравочного заполнения.")
        self.move(225, 50)
        self.create_scene()

        self.dots = []
        self.figures = []
        self.current_color = QColor(255, 255, 255)
        self.scene_width = 880
        self.scene_height = 750

        self.is_key_ctrl_pressed = False
        self.is_key_h_pressed = False
        self.is_key_v_pressed = False

        self.pixel_params = []

        self.to_end = 0
        self.connect = True

        self.ui.with_delay.setChecked(True)
        self.ui.dot.setChecked(True)
        self.setMouseTracking(True)

        self.ui.add.clicked.connect(self.add)
        #self.ui.fill.clicked.connect(self.fill)
        self.ui.end.clicked.connect(self.end)
        self.ui.clear.clicked.connect(self.clear)
        self.ui.exit.clicked.connect(self.exit)

        # Выпадающий список цветов для границы
        self.border_colors = QtWidgets.QComboBox(self)
        self.border_colors.addItem("Черный")
        self.border_colors.addItem("Белый")
        self.border_colors.addItem("Красный")
        self.border_colors.addItem("Зеленый")
        self.border_colors.addItem("Синий")
        self.border_colors.addItem("Желтый")
        self.border_colors.addItem("Розовый")
        self.border_colors.setGeometry(920, 340, 280, 45)
        self.border_colors.setStyleSheet("background-color: rgb(255, 255, 255); "
                                  "color: rgb(0, 0, 0)")

        # Выпадающий список цветов для заполнения
        self.fill_colors = QtWidgets.QComboBox(self)
        self.fill_colors.addItem("Черный")
        self.fill_colors.addItem("Белый")
        self.fill_colors.addItem("Красный")
        self.fill_colors.addItem("Зеленый")
        self.fill_colors.addItem("Синий")
        self.fill_colors.addItem("Желтый")
        self.fill_colors.addItem("Розовый")
        self.fill_colors.setGeometry(920, 430, 280, 45)
        self.fill_colors.setStyleSheet("background-color: rgb(255, 255, 255); "
                                  "color: rgb(0, 0, 0)")

        font = QFont()
        font.setPointSize(16)
        self.border_colors.setFont(font)
        self.fill_colors.setFont(font)

        self.ui.table.setColumnCount(2)
        self.ui.table.setRowCount(1)
        self.ui.table.setHorizontalHeaderLabels(["X", "Y"])
        self.ui.table.horizontalHeaderItem(0).setTextAlignment(Qt.AlignHCenter)
        self.ui.table.horizontalHeaderItem(1).setTextAlignment(Qt.AlignHCenter)

    def create_scene(self):
        self.scene = QGraphicsScene()
        graphicView = QGraphicsView(self.scene, self)
        self.pen = QPen(Qt.black, 5)
        self.scene.setSceneRect(0, 0, 880, 750)
        graphicView.setGeometry(0, 0, 890, 760)
        self.scene.setBackgroundBrush(QColor(255, 255, 255))

    def fill(self):
        pass

    def mousePressEvent(self, event):

        self.pen.setColor(self.get_current_border_color())

        x = event.x()
        y = event.y()

        if self.ui.dot.isChecked():

            if not self.connect:

                self.figures.append(self.dots)
                self.dots = []

                self.connect = True
                self.to_end = len(self.dots)

                self.dots.append(Point(x, y))
                self.draw_line(x, y, x, y)

                self.add_to_table()

            else:

                last = len(self.dots) - 1

                if x <= self.scene_width and y <= self.scene_height:
                    if self.is_key_h_pressed and self.is_key_ctrl_pressed:
                        y = self.dots[last].y

                    if self.is_key_v_pressed and self.is_key_ctrl_pressed:
                        x = self.dots[last].x

                    self.dots.append(Point(x, y))
                    self.draw_line(x, y, self.dots[last].x, self.dots[last].y)
                    self.add_to_table()

        else:

            if self.pixel_params:
                x_to_del, y_to_del = self.pixel_params
                self.scene.addEllipse(x_to_del - 2, y_to_del - 2, 4, 4, Qt.white, Qt.white)
                self.scene.addEllipse(x_to_del - 20, y_to_del - 20, 40, 40, Qt.white)

            self.scene.addEllipse(x - 2, y - 2, 4, 4, Qt.black, Qt.black)
            self.scene.addEllipse(x - 20, y - 20, 40, 40, Qt.red)
            self.pixel_params = [x, y]

    def add_to_table(self):
        x, y = self.dots[-1].x, self.dots[-1].y
        index = len(self.dots)
        for dots in self.figures:
            index += len(dots)
        index -= 1
        self.ui.table.setRowCount(index + 1)
        self.ui.table.setItem(index, 0, QTableWidgetItem(str(int(x))))
        self.ui.table.setItem(index, 1, QTableWidgetItem(str(int(y))))

    def add(self):
        res = self.get_dot()

        if isinstance(res, tuple):

            self.pen.setColor(self.get_current_border_color())
            x, y = res

            if self.ui.dot.isChecked():
                last = len(self.dots) - 1
                self.dots.append(Point(x, y))
                self.draw_line(x, y, self.dots[last].x, self.dots[last].y)

                self.add_to_table()

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setStandardButtons(QMessageBox.Ok)
                msg.setWindowTitle("Добавление точки")
                msg.setText("Точка успешно добавлена.")
                msg.exec_()

            else:

                if self.pixel_params:
                    x_to_del, y_to_del = self.pixel_params
                    self.scene.addEllipse(x_to_del - 2, y_to_del - 2, 4, 4, Qt.white, Qt.white)
                    self.scene.addEllipse(x_to_del - 20, y_to_del - 20, 40, 40, Qt.white)

                self.scene.addEllipse(x - 2, y - 2, 4, 4, Qt.black, Qt.black)
                self.scene.addEllipse(x - 20, y - 20, 40, 40, Qt.red)
                self.pixel_params = [x, y]

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setStandardButtons(QMessageBox.Ok)
                msg.setWindowTitle("Добавление затравочного пикселя")
                msg.setText("Затравочный пиксель успешно добавлен.")
                msg.exec_()

    def end(self):
        self.pen.setColor(self.get_current_border_color())

        self.connect = False

        last = len(self.dots) - 1
        self.draw_line(self.dots[self.to_end].x, self.dots[self.to_end].y,
                           self.dots[last].x, self.dots[last].y)

    def draw_line(self, x_begin, y_begin, x_end, y_end):
        line = self.brezenham_int(x_begin, y_begin, x_end, y_end)
        for dot in line:
            self.scene.addLine(dot.x, dot.y, dot.x, dot.y, self.pen)

    def brezenham_int(self, x_begin, y_begin, x_end, y_end):
        line = []
        if (x_end == x_begin) and (y_end == y_begin):
            line.append(Point(x_begin, y_begin))
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

        if not fl:
            for _ in range(dx):
                line.append(Point(x, y))

                if e >= 0:
                    y += sy
                    e -= dx + dx
                x += sx
                e += dy + dy
        else:
            for _ in range(dx):
                line.append(Point(x, y))

                if e >= 0:
                    x += sx
                    e -= dx + dx
                y += sy
                e += dy + dy

        return line

    def get_dot(self):
        msg_error = QMessageBox()
        msg_error.setIcon(QMessageBox.Critical)
        msg_error.setStandardButtons(QMessageBox.Close)
        msg_error.setWindowTitle("Ошибка ввода данных")

        x = self.ui.x.text()
        y = self.ui.y.text()

        res = self.is_valid_coordinates(x, y)

        if res == -1:
            msg_error.setText("Ошибка ввода координаты Х: координата должна быть положительным числом "
                              "и не выходить за пределы сцены (Ширина сцены - " + str(self.scene_width) +
                              ", высота - " + str(self.scene_height) + ").")
            msg_error.exec_()
        if res == -2:
            msg_error.setText("Ошибка ввода координаты Х: пустое поле ввода.")
            msg_error.exec_()
        if res == -3:
            msg_error.setText("Ошибка ввода координаты Х: должно быть введено корректное целое число.")
            msg_error.exec_()
        if res == -4:
            msg_error.setText("Ошибка ввода координаты Y: координата должна быть положительным числом "
                              "и не выходить за пределы сцены (Ширина сцены - " + str(self.scene_width) +
                              ", высота - " + str(self.scene_height) + ").")
            msg_error.exec_()
        if res == -5:
            msg_error.setText("Ошибка ввода координаты Y: пустое поле ввода.")
            msg_error.exec_()
        if res == -6:
            msg_error.setText("Ошибка ввода координаты Y: должно быть введено корректное целое число.")
            msg_error.exec_()

        return res

    def is_valid_coordinates(self, x, y):
        try:
            x = int(x)
            if not (0 <= x <= self.scene_width):
                return -1
        except:
            if x == "":
                return -2
            else:
                return -3

        try:
            y = int(y)
            if not (0 <= y <= self.scene_height):
                return -4
        except:
            if y == "":
                return -5
            else:
                return -6

        return x, y

    def get_current_border_color(self):
        color = self.border_colors.currentText()
        if color == "Черный":
            return QColor(0, 0, 0)
        if color == "Белый":
            return QColor(255, 255, 255)
        if color == "Красный":
            return QColor(255, 0, 0)
        if color == "Зеленый":
            return QColor(0, 255, 0)
        if color == "Синий":
            return QColor(0, 0, 255)
        if color == "Желтый":
            return QColor(255, 255, 0)
        if color == "Розовый":
            return QColor(255, 110, 150)

    def get_current_fill_color(self):
        color = self.fill_colors.currentText()
        if color == "Черный":
            return QColor(0, 0, 0)
        if color == "Белый":
            return QColor(255, 255, 255)
        if color == "Красный":
            return QColor(255, 0, 0)
        if color == "Зеленый":
            return QColor(0, 255, 0)
        if color == "Синий":
            return QColor(0, 0, 255)
        if color == "Желтый":
            return QColor(255, 255, 0)
        if color == "Розовый":
            return QColor(255, 110, 150)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_H:
            self.is_key_h_pressed = True
        if event.key() == Qt.Key_V:
            self.is_key_v_pressed = True
        if event.key() == Qt.Key_Control:
            self.is_key_ctrl_pressed = True
        super(mywindow, self).keyPressEvent(event)

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_H:
            self.is_key_h_pressed = False
        if event.key() == Qt.Key_V:
            self.is_key_v_pressed = False
        if event.key() == Qt.Key_Control:
            self.is_key_ctrl_pressed = False
        super(mywindow, self).keyReleaseEvent(event)

    def clear(self):
        self.scene.clear()
        self.ui.table.setRowCount(1)
        self.ui.table.setItem(0, 0, QTableWidgetItem(""))
        self.ui.table.setItem(0, 1, QTableWidgetItem(""))

    def exit(self):
        self.close()


app = QtWidgets.QApplication([])
application = mywindow()
application.show()

sys.exit(app.exec())