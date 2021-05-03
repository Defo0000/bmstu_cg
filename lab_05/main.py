from PyQt5 import QtWidgets
from PyQt5.QtGui import QPen, QColor, QFont
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView, QMessageBox
from PyQt5.QtCore import Qt
from window import Ui_MainWindow
import sys
import time


class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Edge():
    def __init__(self, x_start, y_start, x_end, y_end):
        self.x0 = x_start
        self.y0 = y_start
        self.x1 = x_end
        self.y1 = y_end


class GroupInfo():
    def __init__(self, x_start, dx, scanline_amount):
        self.x = x_start
        self.dx = dx
        self.scanline_amount = scanline_amount

class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Лабораторная работа № 5: реализация алгоритмов растрового"
                            " заполнения сплошных областей.")
        self.move(225, 50)
        self.create_scene()

        self.dots = []
        self.figures = []
        self.current_color = QColor(255, 255, 255)
        self.scene_width = 880
        self.scene_height = 650

        self.is_key_ctrl_pressed = False
        self.is_key_h_pressed = False
        self.is_key_v_pressed = False

        self.to_end = 0
        self.connect = True

        self.ui.with_delay.setChecked(True)
        self.setMouseTracking(True)

        self.ui.add.clicked.connect(self.add)
        self.ui.fill.clicked.connect(self.fill)
        self.ui.end.clicked.connect(self.end)
        self.ui.clear.clicked.connect(self.clear)
        self.ui.exit.clicked.connect(self.exit)

        # Выпадающий список цветов
        self.colors = QtWidgets.QComboBox(self)
        self.colors.addItem("Черный")
        self.colors.addItem("Белый")
        self.colors.addItem("Красный")
        self.colors.addItem("Зеленый")
        self.colors.addItem("Синий")
        self.colors.addItem("Желтый")
        self.colors.addItem("Розовый")
        self.colors.setGeometry(910, 290, 280, 45)
        self.colors.setStyleSheet("background-color: rgb(255, 255, 255); "
                                  "color: rgb(0, 0, 0)")
        font = QFont()
        font.setPointSize(16)
        self.colors.setFont(font)

    def create_scene(self):
        self.scene = QGraphicsScene()
        graphicView = QGraphicsView(self.scene, self)
        self.pen = QPen(Qt.black, 5)
        self.scene.setSceneRect(0, 0, 880, 650)
        graphicView.setGeometry(0, 0, 890, 660)
        self.scene.setBackgroundBrush(QColor(255, 255, 255))

    def mousePressEvent(self, event):

        self.current_color = self.get_current_color()
        self.pen.setColor(self.current_color)

        x = event.x()
        y = event.y()

        if not self.connect:

            self.figures.append(self.dots)
            self.dots = []

            self.connect = True
            self.to_end = len(self.dots)

            self.dots.append(Point(x, y))
            self.scene.addLine(x, y, x, y, self.pen)

        else:

            last = len(self.dots) - 1

            if x <= self.scene_width and y <= self.scene_height:
                if self.is_key_h_pressed and self.is_key_ctrl_pressed:
                    y = self.dots[last].y

                if self.is_key_v_pressed and self.is_key_ctrl_pressed:
                    x = self.dots[last].x

                self.dots.append(Point(x, y))
                self.scene.addLine(x, y, self.dots[last].x, self.dots[last].y, self.pen)

    def add(self):
        res = self.get_dot()

        if isinstance(res, tuple):

            self.current_color = self.get_current_color()
            self.pen.setColor(self.current_color)

            x, y = res
            last = len(self.dots) - 1
            self.dots.append(Point(x, y))
            self.scene.addLine(x, y, self.dots[last].x, self.dots[last].y, self.pen)

            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setStandardButtons(QMessageBox.Ok)
            msg.setWindowTitle("Добавление точки")
            msg.setText("Точка успешно добавлена.")
            msg.exec_()

    def fill(self):

        if len(self.dots):
            self.figures.append(self.dots)

        edges = []
        for figure in self.figures:
            edges += self.make_edges(figure)

        y_group = [[] for i in range(self.scene_height)]

        for edge in edges:
            scanline_amount = abs(edge.y1 - edge.y0)
            if scanline_amount:
                dx = (edge.x1 - edge.x0) / scanline_amount
                x_start = edge.x0
                y_group[edge.y0].append(GroupInfo(x_start, dx, scanline_amount))

        active_edges = []

        for scanline in range(self.scene_height):

            # Обновляем список активных ребер (добавляем новые, если они есть)
            for i in range(len(y_group[scanline])):
                active_edges.append(y_group[scanline][i])

            active_edges.sort(key=lambda edge: edge.x)

            # Выполняем закраску
            for i in range(0, len(active_edges), 2):
                self.scene.addLine(active_edges[i].x, scanline,
                                   active_edges[i + 1].x, scanline, self.pen)
                if self.ui.with_delay.isChecked():
                    QtWidgets.QApplication.processEvents()
                    time.sleep(0.01)

            # Обновляем список активных ребер и удаляем неактивные, если они есть
            i = 0
            while i < len(active_edges):
                active_edges[i].x += active_edges[i].dx
                active_edges[i].scanline_amount -= 1
                if active_edges[i].scanline_amount < 1:
                    active_edges.pop(i)
                else:
                    i += 1

    def make_edges(self, dots):

        edges = []

        for i in range(len(dots) - 1):
            x0, y0 = dots[i].x, dots[i].y
            x1, y1 = dots[i + 1].x, dots[i + 1].y
            if y0 > y1:
                y1, y0 = y0, y1
                x1, x0 = x0, x1

            edges.append(Edge(x0, y0, x1, y1))

        i = len(dots) - 1
        x0, y0 = dots[0].x, dots[0].y
        x1, y1 = dots[i].x, dots[i].y
        if y0 > y1:
            y1, y0 = y0, y1
            x1, x0 = x0, x1

        edges.append(Edge(x0, y0, x1, y1))

        return edges

    def end(self):
        self.current_color = self.get_current_color()
        self.pen.setColor(self.current_color)

        self.connect = False

        last = len(self.dots) - 1
        self.scene.addLine(self.dots[self.to_end].x, self.dots[self.to_end].y,
                           self.dots[last].x, self.dots[last].y, self.pen)

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

    def get_current_color(self):
        color = self.colors.currentText()
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


    def clear(self):
        self.scene.clear()
        self.figures = []
        self.dots = []

    def exit(self):
        self.close()

app = QtWidgets.QApplication([])
application = mywindow()
application.show()

sys.exit(app.exec())