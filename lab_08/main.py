from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap, QPainter, QPen, QColor, QFont
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView, QMessageBox, QTableWidgetItem, QButtonGroup, QLabel
from PyQt5.QtCore import Qt, QEventLoop, QPoint, QRectF
from window import Ui_MainWindow
import sys
from math import sqrt, fabs, atan, cos, sin, radians

class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Vector():
    def __init__(self, x, y):
        self.x = x
        self.y = y

class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("ЛР № 8: Реализация и исследование алгоритма отчесения "
                            "отрезка произвольным выпуклым отсекателем (Алгоритм Кируса-Бека).")
        self.move(255, 150)

        self.connected = False
        self.cutter = []
        self.sections = []
        self.temp_section = []
        self.cutter_ended = False

        self.shift_pressed = False
        self.ctrl_pressed = False
        self.v_pressed = False
        self.h_pressed = False
        self.p_pressed = False
        self.alt_pressed = False

        self.cutter_colors = QtWidgets.QComboBox(self)
        self.cutter_colors.addItem("Черный")
        self.cutter_colors.addItem("Белый")
        self.cutter_colors.addItem("Красный")
        self.cutter_colors.addItem("Зеленый")
        self.cutter_colors.addItem("Синий")
        self.cutter_colors.addItem("Желтый")
        self.cutter_colors.addItem("Розовый")
        self.cutter_colors.setGeometry(800, 60, 280, 40)
        self.cutter_colors.setStyleSheet("background-color: rgb(255, 255, 255); "
                                         "color: rgb(0, 0, 0)")

        self.section_colors = QtWidgets.QComboBox(self)
        self.section_colors.addItem("Черный")
        self.section_colors.addItem("Белый")
        self.section_colors.addItem("Красный")
        self.section_colors.addItem("Зеленый")
        self.section_colors.addItem("Синий")
        self.section_colors.addItem("Желтый")
        self.section_colors.addItem("Розовый")
        self.section_colors.setCurrentIndex(2)
        self.section_colors.setGeometry(800, 150, 280, 40)
        self.section_colors.setStyleSheet("background-color: rgb(255, 255, 255); "
                                          "color: rgb(0, 0, 0)")

        self.result_colors = QtWidgets.QComboBox(self)
        self.result_colors.addItem("Черный")
        self.result_colors.addItem("Белый")
        self.result_colors.addItem("Красный")
        self.result_colors.addItem("Зеленый")
        self.result_colors.addItem("Синий")
        self.result_colors.addItem("Желтый")
        self.result_colors.addItem("Розовый")
        self.result_colors.setGeometry(800, 250, 280, 40)
        self.result_colors.setCurrentIndex(3)
        self.result_colors.setStyleSheet("background-color: rgb(255, 255, 255); "
                                         "color: rgb(0, 0, 0)")

        font = QFont()
        font.setPointSize(16)
        self.cutter_colors.setFont(font)
        self.section_colors.setFont(font)
        self.result_colors.setFont(font)

        self.ui.cut.clicked.connect(self.cut)
        self.ui.end_cutter.clicked.connect(self.end_cutter)
        self.ui.exit.clicked.connect(self.exit)
        self.ui.clear.clicked.connect(self.clear)

        self.create_scene()

    def cut(self):
        if not self.check_cutter():
            return

        for section in self.sections:
            t_start = 0
            t_end = 1

            normals = self.get_normals()

            d = self.get_vector(section[0], section[1])

            vertices = self.cutter
            for i in range(len(vertices)):

                if vertices[i] != section[0]:
                    wi = self.get_vector(vertices[i], section[0])
                else:
                    wi = self.get_vector(vertices[(i + 1 ) % (len(vertices))], section[0])

                Dck = self.get_scalar_prod(d, normals[i])
                Wck = self.get_scalar_prod(wi, normals[i])

                if Dck == 0:
                    if Wck < 0:
                        return
                    else:
                        continue

                t = - Wck / Dck

                if Dck > 0:
                    if t > t_start:
                        t_start = t
                else:
                    if t < t_end:
                        t_end = t

            if t_start < t_end:
                p1 = Point(round(section[0].x + d.x * t_start), round(section[0].y + d.y * t_start))
                p2 = Point(round(section[0].x + d.x * t_end), round(section[0].y + d.y * t_end))
                self.scene.addLine(p1.x, p1.y, p2.x, p2.y, QPen(self.get_result_color(), 3))

    # Под знаком векторного произведения подразумевается проекция вектора на OZ
    def check_cutter(self):
        cutter = self.cutter
        if len(cutter) < 3:
            self.show_error("У многоугольника (отсекателя) не может быть меньше трёх вершин.")
            return False

        if not self.cutter_ended:
            self.show_error("Отсекатель не замкнут.")
            return False

        if self.get_vector_prod(self.get_vector(cutter[0], cutter[1]),
                                self.get_vector(cutter[1], cutter[2])) > 0:
            sign = 1
        else:
            sign = -1

        n = len(cutter)
        for i in range(1, len(cutter)):
            if sign * self.get_vector_prod(self.get_vector(cutter[i], cutter[(i + 1) % n]),
                            self.get_vector(cutter[(i + 1) % n], cutter[(i + 2) % n])) < 0:
                self.show_error("Отсекатель не является выпуклым.")
                return False

        if sign < 0:
           self.cutter.reverse()

        return True

    def get_normals(self):
        normals = list()
        vertices = self.cutter
        n = len(self.cutter)
        for i in range(n):
            normals.append(self.get_normal(vertices[i], vertices[(i + 1) % n], vertices[(i + 2) % n]))
        return normals

    def get_normal(self, p1, p2, p3):
        v = self.get_vector(p1, p2)
        normal = Point(1, 0) if v.x == 0 else Point(-v.y / v.x, 1)

        if self.get_scalar_prod(self.get_vector(p2, p3), normal) < 0:
            normal.x *= -1
            normal.y *= -1

        return normal

    def get_vector(self, start, end):
        return Vector(end.x - start.x, end.y - start.y)

    def get_vector_prod(self, a, b):
        return a.x * b.y - a.y * b.x

    def get_scalar_prod(self, a, b):
        return a.x * b.x + a.y * b.y

    def mousePressEvent(self, event):
        x, y = event.x(), event.y()
        if self.shift_pressed:
            if not self.connected:
                if self.cutter:
                    x0, y0 = self.cutter[-1].x, self.cutter[-1].y
                    self.scene.addLine(x0, y0, x, y, self.get_cutter_color())
                    self.cutter.append(Point(x, y))
                    self.scene.addLine(x, y, x, y, QPen(self.get_cutter_color(), 3))
                    self.update_cutter_label()
                else:
                    self.cutter.append(Point(x, y))
                    self.scene.addLine(x, y, x, y, QPen(self.get_cutter_color(), 3))
            else:
                self.delete_cutter()
                self.cutter = []
                self.cutter.append(Point(x, y))
                self.connected = False

        if self.ctrl_pressed:
            if not self.temp_section:
                self.temp_section.append(Point(x, y))
                self.scene.addLine(x, y, x, y, QPen(self.get_section_color(), 3))
            else:
                x0, y0 = self.temp_section[0].x, self.temp_section[0].y
                if self.v_pressed:
                    x = x0
                elif self.h_pressed:
                    y = y0
                elif self.p_pressed and len(self.cutter) >= 2:

                    if x == x0:
                        m = 1e10
                    else:
                        m = (y - y0) / (x - x0)

                    k = self.find_parallel(m)

                    l = (x - x0) ** 2 + (y - y0) ** 2

                    if x0 < x:
                        x = x0 + sqrt(l / (1 + k ** 2))
                    else:
                        x = x0 - sqrt(l / (1 + k ** 2))

                    if y0 < y:
                        y = y0 + fabs(k * (x - x0))
                    else:
                        y = y0 - fabs(k * (x - x0))

                    x = int(x)
                    y = int(y)

                self.scene.addLine(x0, y0, x, y, self.get_section_color())
                self.scene.addLine(x, y, x, y, QPen(self.get_section_color(), 3))

                self.sections.append([Point(x, y), Point(x0, y0)])
                self.update_section_label()
                self.temp_section = []

    def find_parallel(self, k):
        if not self.cutter:
            return
        m = list()

        n = len(self.cutter)
        vertices = self.cutter

        for i in range(n):
            dx = (vertices[i].x - vertices[(i + 1) % n].x)
            dy = (vertices[i].y - vertices[(i + 1) % n].y)

            if dx == 0:
                m.append(1e10)
            else:
                m.append(dy / dx)

        delta = fabs(k - m[0])
        pos = 0
        for i in range(1, len(m)):
            if fabs(k - m[i]) < delta:
                delta = fabs(k - m[i])
                pos = i

        return m[pos]

    def end_cutter(self):
        if len(self.cutter) < 3:
            self.show_error("Отсекатель не может быть прямой или точкой.")
            return

        self.connected = True
        x, y = self.cutter[0].x, self.cutter[0].y
        self.scene.addLine(x, y, x, y, QPen(self.get_cutter_color(), 3))
        x0, y0 = self.cutter[-1].x, self.cutter[-1].y
        self.scene.addLine(x0, y0, x, y, self.get_cutter_color())
        self.cutter_ended = True

    def delete_cutter(self):
        self.scene.clear()
        for section in self.sections:
            self.scene.addLine(section[0].x, section[0].y, section[1].x, section[1].y,
                               self.get_section_color())
        self.cutter_ended = False

    def update_section_label(self):
        self.ui.s_xs.setText(str(self.sections[-1][0].x))
        self.ui.s_ys.setText(str(self.sections[-1][0].y))
        self.ui.s_xe.setText(str(self.sections[-1][1].x))
        self.ui.s_ye.setText(str(self.sections[-1][1].y))

    def update_cutter_label(self):
        self.ui.c_xs.setText(str(self.cutter[-1].x))
        self.ui.c_ys.setText(str(self.cutter[-1].y))
        self.ui.c_xe.setText(str(self.cutter[-2].x))
        self.ui.c_ye.setText(str(self.cutter[-2].y))

    def show_error(self, msg):
        msg_error = QMessageBox()
        msg_error.setIcon(QMessageBox.Critical)
        msg_error.setStandardButtons(QMessageBox.Close)
        msg_error.setWindowTitle("Ошибка ввода данных")
        msg_error.setText(msg)
        msg_error.exec_()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Control:
            self.ctrl_pressed = True
        if event.key() == Qt.Key_Shift:
            self.shift_pressed = True
        if event.key() == Qt.Key_V:
            self.v_pressed = True
        if event.key() == Qt.Key_H:
            self.h_pressed = True
        if event.key() == Qt.Key_Alt:
            self.alt_pressed = True
        if event.key() == Qt.Key_P:
            self.p_pressed = True
        super(mywindow, self).keyPressEvent(event)

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Control:
            self.ctrl_pressed = False
        if event.key() == Qt.Key_Shift:
            self.shift_pressed = False
        if event.key() == Qt.Key_V:
            self.v_pressed = False
        if event.key() == Qt.Key_H:
            self.h_pressed = False
        if event.key() == Qt.Key_Alt:
            self.alt_pressed = False
        if event.key() == Qt.Key_P:
            self.p_pressed = False
        super(mywindow, self).keyReleaseEvent(event)

    def get_cutter_color(self):
        color = self.cutter_colors.currentText()
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

    def get_section_color(self):
        color = self.section_colors.currentText()
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

    def get_result_color(self):
        color = self.result_colors.currentText()
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

    def create_scene(self):
        self.scene = QGraphicsScene()
        graphicView = QGraphicsView(self.scene, self)
        self.pen = QPen(Qt.black, 5)
        self.scene.setSceneRect(0, 0, 770, 550)
        graphicView.setGeometry(0, 0, 780, 560)
        self.scene.setBackgroundBrush(QColor(255, 255, 255))

    #def create_scene(self):
    #    self.label = QLabel(self)
    #    self.label.setGeometry(0, 0, 770, 550)
    #    self.pixmap = QPixmap(self.label.size())
    #    self.pixmap.fill(Qt.white)
    #    self.label.setPixmap(self.pixmap)
    #    self.label.show()
    #    self.painter = QPainter(self.pixmap)

    def clear(self):
        self.scene.clear()
        self.connected = False
        self.cutter = []
        self.sections = []
        self.cutter_ended = False
        self.temp_section = []

    def exit(self):
        self.close()

app = QtWidgets.QApplication([])
application = mywindow()
application.show()

sys.exit(app.exec())