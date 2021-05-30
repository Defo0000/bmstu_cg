from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap, QPainter, QPen, QColor, QFont
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView, QMessageBox, QTableWidgetItem, QButtonGroup, QLabel
from PyQt5.QtCore import Qt, QEventLoop, QPoint
from window import Ui_MainWindow
import sys
import time
import numpy as np
from PIL import Image

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
        self.move(255, 50)

        self.dots = []
        self.figures = []
        self.current_color = QColor(255, 255, 255)
        self.scene_width = 785
        self.scene_height = 605

        self.is_key_ctrl_pressed = False
        self.is_key_h_pressed = False
        self.is_key_v_pressed = False

        self.work_pixel = None
        self.ellipse_params = []

        self.to_end = 0
        self.connect = True

        self.table_index = 0

        self.mode_dots = QButtonGroup()
        self.mode_dots.addButton(self.ui.dot, 0)
        self.mode_dots.addButton(self.ui.pixel, 1)
        self.mode_dots.addButton(self.ui.ellipse, 2)

        self.mood = QButtonGroup()
        self.mood.addButton(self.ui.with_delay, 0)
        self.mood.addButton(self.ui.no_delay, 1)

        self.ui.with_delay.setChecked(True)
        self.ui.dot.setChecked(True)
        self.setMouseTracking(True)

        self.ui.add.clicked.connect(self.add)
        self.ui.fill.clicked.connect(self.fill)
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
        self.border_colors.setGeometry(800, 330, 280, 40)
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
        self.fill_colors.setGeometry(800, 420, 280, 40)
        self.fill_colors.setStyleSheet("background-color: rgb(255, 255, 255); "
                                  "color: rgb(0, 0, 0)")

        font = QFont()
        font.setPointSize(14)
        self.border_colors.setFont(font)
        self.fill_colors.setFont(font)

        self.ui.table.setColumnCount(2)
        self.ui.table.setRowCount(1)
        self.ui.table.setHorizontalHeaderLabels(["X", "Y"])
        self.ui.table.horizontalHeaderItem(0).setTextAlignment(Qt.AlignHCenter)
        self.ui.table.horizontalHeaderItem(1).setTextAlignment(Qt.AlignHCenter)

        self.ui.table_pixel.setColumnCount(2)
        self.ui.table_pixel.setRowCount(1)
        self.ui.table_pixel.setHorizontalHeaderLabels(["X", "Y"])
        self.ui.table_pixel.horizontalHeaderItem(0).setTextAlignment(Qt.AlignHCenter)
        self.ui.table_pixel.horizontalHeaderItem(1).setTextAlignment(Qt.AlignHCenter)

        self.create_scene()

    '''def create_scene(self):
        self.scene = QGraphicsScene()
        #self.label = QLabel()
        #self.label.setFrameRect(QRect(0, 0, 780, 600))
        #self.label.setGeometry(0, 0, 790, 610)
        #self.pixmap = QPixmap("image.jpg")
        self.pixmap = QPixmap(self.scene_width, self.scene_height)
        self.pixmap.fill(Qt.white)
        self.painter = QPainter(self.pixmap)
        self.painter.setBrush(Qt.black)
        #self.label.setPixmap(self.pixmap)
        #self.label.update()
        self.imItem = self.scene.addPixmap(self.pixmap)
        graphicView = QGraphicsView(self.scene, self)
        self.pen = QPen(Qt.black, 1)
        self.scene.setSceneRect(0, 0, 780, 600)
        graphicView.setGeometry(0, 0, 790, 610)
        self.scene.setBackgroundBrush(QColor(255, 255, 255))'''

    def create_scene(self):
        self.label = QLabel(self)
        self.label.setGeometry(0, 0, 790, 610)
        self.pixmap = QPixmap(self.label.size())
        self.pixmap.fill(Qt.white)
        self.label.setPixmap(self.pixmap)
        self.label.show()
        self.painter = QPainter(self.pixmap)

    def fill(self):
        stack = []

        if self.work_pixel:
            stack.append(self.work_pixel)
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setStandardButtons(QMessageBox.Ok)
            msg.setWindowTitle("Ошибка")
            msg.setText("Затравочный пиксель не введен.")
            msg.exec_()
            return

        border_color = self.get_border_color()
        fill_color = self.get_fill_color()

        self.painter.setPen(QPen(self.get_fill_color(), 1))

        proc_time = 0

        while stack:
            start_time = time.time()
            current_point = stack.pop()
            self.paint(current_point.x, current_point.y)

            x = current_point.x + 1
            y = current_point.y

            pixel_color = self.color(x, y)

            while pixel_color != border_color and pixel_color != fill_color and x < self.scene_width:
                self.paint(x, y)
                x += 1
                pixel_color = self.color(x, y)

            rx = x - 1
            x = current_point.x - 1

            pixel_color = self.color(x, y)

            while pixel_color != border_color and pixel_color != fill_color and x > 0:
                self.paint(x, y)
                x -= 1
                pixel_color = self.color(x, y)

            lx = x + 1

            for i in [1, -1]:
                x = lx
                y = current_point.y + i

                if y < 0 or y > self.scene_height:
                    continue

                while x <= rx:

                    flag = False

                    pixel_color = self.color(x, y)

                    while pixel_color != fill_color and pixel_color != border_color and x <= rx:
                        flag = True
                        x += 1
                        pixel_color = self.color(x, y)

                    if flag:
                        if x == rx and pixel_color != border_color and pixel_color != fill_color:
                            stack.append(Point(x, y))
                        else:
                            stack.append(Point(x - 1, y))

                    xi = x
                    while (pixel_color == border_color or pixel_color == fill_color) and x < rx:
                        x += 1
                        pixel_color = self.color(x, y)

                    if x == xi:
                        x += 1

            end_time = time.time()
            proc_time += end_time - start_time

            if self.ui.with_delay.isChecked():
                QtWidgets.QApplication.processEvents(QEventLoop.AllEvents)

        self.show_time_info(proc_time)

    def show_time_info(self, time):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setWindowTitle("Время закраски")
        msg.move(1050, 350)
        msg.setText("Время закраски составило " + str("%.3f" % (time / 1000)) + " с.")
        msg.exec_()


    def color(self, x, y):
        return self.pixmap.toImage().pixelColor(x, y)

    def paint(self, x, y):
        self.painter.drawPoint(x, y)
        self.label.setPixmap(self.pixmap)

    def draw_line(self, x_begin, y_begin, x_end, y_end, color):
        self.painter.setPen(QPen(color, 1))
        line = self.brezenham_int(x_begin, y_begin, x_end, y_end)
        for dot in line:
            self.paint(dot.x, dot.y)

    def add_to_table(self, x, y):
        i = self.table_index
        self.table_index += 1
        self.ui.table.setRowCount(i + 1)
        self.ui.table.setItem(i, 0, QTableWidgetItem(str(int(x))))
        self.ui.table.setItem(i, 1, QTableWidgetItem(str(int(y))))

    def add_pixel_to_table(self, x, y):
        self.ui.table_pixel.setItem(0, 0, QTableWidgetItem(str(int(x))))
        self.ui.table_pixel.setItem(0, 1, QTableWidgetItem(str(int(y))))

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

    def mousePressEvent(self, event):

        x = event.x()
        y = event.y()

        if not(x <= self.scene_width and y <= self.scene_height):
            return

        if self.ui.dot.isChecked():
            self.ellipse_params = []

            if not self.connect:

                self.figures.append(self.dots)
                self.dots = []

                self.connect = True
                self.to_end = len(self.dots)

                self.dots.append(Point(x, y))
                self.draw_line(x, y, x, y, self.get_border_color())
                self.add_to_table(x, y)

            else:

                last = len(self.dots) - 1

                if self.is_key_h_pressed and self.is_key_ctrl_pressed:
                    y = self.dots[last].y

                if self.is_key_v_pressed and self.is_key_ctrl_pressed:
                    x = self.dots[last].x

                self.dots.append(Point(x, y))
                self.draw_line(x, y, self.dots[last].x, self.dots[last].y, self.get_border_color())
                self.add_to_table(x, y)
                
        elif self.ui.pixel.isChecked():
            self.ellipse_params = []

            if self.work_pixel:
                x_to_del, y_to_del = self.work_pixel.x, self.work_pixel.y
                self.draw_line(x_to_del, y_to_del, x_to_del, y_to_del, Qt.white)

            self.draw_line(x, y, x, y, self.get_fill_color())
            self.work_pixel = Point(x, y)
            self.add_pixel_to_table(x, y)

        else:
            if len(self.ellipse_params) == 1:
                self.painter.setPen(QPen(self.get_border_color(), 1))
                self.painter.drawEllipse(self.ellipse_params[0].x, self.ellipse_params[0].y,
                                         (x - self.ellipse_params[0].x), (y - self.ellipse_params[0].y))
                self.label.setPixmap(self.pixmap)
                self.ellipse_params = []
            else:
                self.ellipse_params.append(Point(x, y))


    def add(self):
        res = self.get_dot()

        if isinstance(res, tuple):

            x, y = res

            if self.ui.dot.isChecked():
                last = len(self.dots) - 1
                self.dots.append(Point(x, y))
                self.draw_line(x, y, self.dots[last].x, self.dots[last].y, self.get_border_color())

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setStandardButtons(QMessageBox.Ok)
                msg.setWindowTitle("Добавление точки")
                msg.setText("Точка успешно добавлена.")
                msg.exec_()

                self.add_to_table(x, y)

            elif self.ui.pixel.isChecked():

                if self.work_pixel:
                    x_to_del, y_to_del = self.work_pixel.x, self.work_pixel.y
                    self.draw_line(x_to_del, y_to_del, x_to_del, y_to_del, Qt.white)

                self.draw_line(x, y, x, y, self.get_fill_color())
                self.work_pixel = Point(x, y)

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setStandardButtons(QMessageBox.Ok)
                msg.setWindowTitle("Добавление затравочного пикселя")
                msg.setText("Затравочный пиксель успешно добавлен.")
                msg.exec_()
                self.add_pixel_to_table(x, y)

    def end(self):
        self.connect = False

        last = len(self.dots) - 1
        self.draw_line(self.dots[self.to_end].x, self.dots[self.to_end].y,
                           self.dots[last].x, self.dots[last].y, self.get_border_color())

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

    def get_border_color(self):
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

    def get_fill_color(self):
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
        self.pixmap.fill(Qt.white)
        self.label.setPixmap(self.pixmap)
        self.painter.setPen(QPen(self.get_border_color(), 1))
        self.figures.clear()
        self.dots.clear()
        self.pixel_params = None
        self.to_end = 0
        self.connect = True
        self.table_index = 0
        self.ui.table_pixel.setRowCount(1)
        self.ui.table_pixel.setItem(0, 0, QTableWidgetItem(""))
        self.ui.table_pixel.setItem(0, 1, QTableWidgetItem(""))
        self.ui.table.setRowCount(1)
        self.ui.table.setItem(0, 0, QTableWidgetItem(""))
        self.ui.table.setItem(0, 1, QTableWidgetItem(""))

    def exit(self):
        self.close()


app = QtWidgets.QApplication([])
application = mywindow()
application.show()

sys.exit(app.exec())