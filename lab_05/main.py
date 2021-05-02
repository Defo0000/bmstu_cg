from PyQt5 import QtWidgets
from PyQt5.QtGui import QPen, QColor, QFont, QKeySequence
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView, QMessageBox
from PyQt5.QtCore import Qt
from window import Ui_MainWindow
import sys


class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

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
        self.current_color = QColor(255, 255, 255)
        self.scene_width = 880
        self.scene_height = 650

        self.is_key_ctrl_pressed = False
        self.is_key_h_pressed = False
        self.is_key_w_pressed = False

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

        last = len(self.dots) - 1

        if x <= self.scene_width and y <= self.scene_height:
            if self.is_key_h_pressed and self.is_key_ctrl_pressed:
                y = self.dots[last].y

            if self.is_key_w_pressed and self.is_key_ctrl_pressed:
                x = self.dots[last].x

            self.dots.append(Point(x, y))
            self.scene.addLine(x, y, self.dots[last].x, self.dots[last].y, self.pen)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_H:
            self.is_key_h_pressed = True
        if event.key() == Qt.Key_W:
            self.is_key_w_pressed = True
        if event.key() == Qt.Key_Control:
            self.is_key_ctrl_pressed = True
        super(mywindow, self).keyPressEvent(event)

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_H:
            self.is_key_h_pressed = False
        if event.key() == Qt.Key_W:
            self.is_key_w_pressed = False
        if event.key() == Qt.Key_Control:
            self.is_key_ctrl_pressed = False
        super(mywindow, self).keyReleaseEvent(event)

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
        pass

    def end(self):
        self.current_color = self.get_current_color()
        self.pen.setColor(self.current_color)

        last = len(self.dots) - 1
        self.scene.addLine(self.dots[0].x, self.dots[0].y, self.dots[last].x, self.dots[last].y, self.pen)

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
            msg_error.setText("Ошибка ввода координаты Х: должно быть введено корректное вещественное число.")
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
            msg_error.setText("Ошибка ввода координаты Y: должно быть введено корректное вещественное число.")
            msg_error.exec_()

        return res

    def is_valid_coordinates(self, x, y):
        try:
            x = float(x)
            if not (0 <= x <= self.scene_width):
                return -1
        except:
            if x == "":
                return -2
            else:
                return -3

        try:
            y = float(y)
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

    def exit(self):
        self.close()

app = QtWidgets.QApplication([])
application = mywindow()
application.show()

sys.exit(app.exec())