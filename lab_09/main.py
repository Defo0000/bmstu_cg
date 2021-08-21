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
        self.setWindowTitle("ЛР № 9: Реализация и исследование алгоритма отчесения "
                            "произвольного многоугольника произвольным выпуклым отсекателем (Алгоритм Сазерленда-Ходжмена).")
        self.move(15, 10)

        self.cutter_colors = QtWidgets.QComboBox(self)
        self.cutter_colors.addItem("Черный")
        self.cutter_colors.addItem("Белый")
        self.cutter_colors.addItem("Красный")
        self.cutter_colors.addItem("Зеленый")
        self.cutter_colors.addItem("Синий")
        self.cutter_colors.addItem("Желтый")
        self.cutter_colors.addItem("Розовый")
        self.cutter_colors.setGeometry(1640, 180, 170, 40)
        self.cutter_colors.setCurrentIndex(0)
        self.cutter_colors.setStyleSheet("background-color: rgb(255, 255, 255); "
                                         "color: rgb(0, 0, 0)")

        self.polygon_colors = QtWidgets.QComboBox(self)
        self.polygon_colors.addItem("Черный")
        self.polygon_colors.addItem("Белый")
        self.polygon_colors.addItem("Красный")
        self.polygon_colors.addItem("Зеленый")
        self.polygon_colors.addItem("Синий")
        self.polygon_colors.addItem("Желтый")
        self.polygon_colors.addItem("Розовый")
        self.polygon_colors.setCurrentIndex(2)
        self.polygon_colors.setGeometry(1640, 245, 170, 40)
        self.polygon_colors.setStyleSheet("background-color: rgb(255, 255, 255); "
                                         "color: rgb(0, 0, 0)")

        self.result_colors = QtWidgets.QComboBox(self)
        self.result_colors.addItem("Черный")
        self.result_colors.addItem("Белый")
        self.result_colors.addItem("Красный")
        self.result_colors.addItem("Зеленый")
        self.result_colors.addItem("Синий")
        self.result_colors.addItem("Желтый")
        self.result_colors.addItem("Розовый")
        self.result_colors.setGeometry(1640, 310, 170, 40)
        self.result_colors.setCurrentIndex(3)
        self.result_colors.setStyleSheet("background-color: rgb(255, 255, 255); "
                                         "color: rgb(0, 0, 0)")

        font = QFont()
        font.setPointSize(13)
        self.cutter_colors.setFont(font)
        self.polygon_colors.setFont(font)
        self.result_colors.setFont(font)

        self.ui.cut_mode.setChecked(True)
        self.ui.enter_x.setValue(200)
        self.ui.enter_y.setValue(300)

        self.ui.add_to_polygon.clicked.connect(self.add_to_polygon)
        self.ui.add_to_cutter.clicked.connect(self.add_to_cutter)
        self.ui.end_polygon.clicked.connect(self.end_polygon)
        self.ui.end_cutter.clicked.connect(self.end_cutter)

        self.ui.cut.clicked.connect(self.solve)
        self.ui.exit.clicked.connect(self.exit)
        self.ui.clear.clicked.connect(self.clear)

        self.is_cutter_ended = False
        self.is_polygon_ended = False

        self.b_pressed = False
        self.p_pressed = False

        self.cutter = []
        self.polygon = []

        self.create_scene()

    def get_vector(self, start, end):
        return Vector(end.x - start.x, end.y - start.y)

    def get_vector_prod(self, a, b):
        return a.x * b.y - a.y * b.x

    def get_scalar_prod(self, a, b):
        return a.x * b.x + a.y * b.y

    def solve(self):
        if not self.ready():
            return

        cutted_polygon = self.cut(self.polygon, self.cutter, self.get_normals())

        n = len(cutted_polygon)
        for i in range(n):
            self.scene.addLine(cutted_polygon[i].x, cutted_polygon[i].y,
                               cutted_polygon[(i + 1) % n].x, cutted_polygon[(i + 1) % n].y,
                               QPen(self.get_result_color(), 3))

    # Функция отсечения многоугольника отсекателем
    def cut(self, polygon, cutter, normals):
        if not self.ready():
            return

        for i in range(len(cutter)):
            cur_edge = [cutter[i], cutter[(i + 1) % len(cutter)]]

            polygon = self.cut_with_edge(polygon, cur_edge, normals[i])

            if len(polygon) < 3:
                return []

        return polygon

    # Фнкция отсечения многоугольника относительно одного ребра отсекателя
    def cut_with_edge(self, polygon, edge, normal):
        if len(polygon) < 3:
            return []

        res_polygon = list()

        prev_is_visible = self.is_visible(polygon[0], *edge)

        n = len(polygon)
        for i in range(1, n + 1):
            cur_is_visible = self.is_visible(polygon[i % n], *edge)

            if prev_is_visible:
                if cur_is_visible:
                    res_polygon.append(polygon[i % n])
                else:
                    intersection = self.find_intersection([polygon[i - 1], polygon[i % n]], edge, normal)
                    res_polygon.append(intersection)
            else:
                if cur_is_visible:
                    intersection = self.find_intersection([polygon[i - 1], polygon[i % n]], edge, normal)
                    res_polygon.append(intersection)
                    res_polygon.append(polygon[i % n])

            prev_is_visible = cur_is_visible

        return res_polygon

    # Функция проверки принадлежности точки отсекателю относительно одного ребра
    def is_visible(self, point, start, end):
        a = self.get_vector(start, end)
        b = self.get_vector(start, point)
        
        if self.get_vector_prod(a, b) >= 0:
            return True
        else:
            return False

    # Нахождение пересечения отрезка многоугольника с прямой, содержащей ребро отсекателя
    def find_intersection(self, section, edge, normal):
        wi = self.get_vector(edge[0], section[0])
        d = self.get_vector(section[0], section[1])
        Wck = self.get_scalar_prod(wi, normal)
        Dck = self.get_scalar_prod(d, normal)

        t = - Wck / Dck

        diff = Point(section[1].x - section[0].x, section[1].y - section[0].y)

        return Point(section[0].x + diff.x * t, section[0].y + diff.y * t)

    def ready(self):
        if not self.check_cutter():
            return False

        if not self.polygon:
            self.show_error("Многоугольник не введен.")
            return False

        if not self.is_polygon_ended:
            self.show_error("Многоугольник не замкнут.")
            return False

        return True

    def check_cutter(self):
        if len(self.cutter) < 3:
            self.show_error("У многоугольника (отсекателя) не может быть меньше трёх вершин.")
            return False

        if not self.is_cutter_ended:
            self.show_error("Отсекатель не замкнут.")
            return False

        if self.get_vector_prod(self.get_vector(self.cutter[0], self.cutter[1]),
                                self.get_vector(self.cutter[1], self.cutter[2])) > 0:
            sign = 1
        else:
            sign = -1

        n = len(self.cutter)
        for i in range(1, len(self.cutter)):
            if sign * self.get_vector_prod(self.get_vector(self.cutter[i], self.cutter[(i + 1) % n]),
                            self.get_vector(self.cutter[(i + 1) % n], self.cutter[(i + 2) % n])) < 0:
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

    def distance(self, line, point):
        line_len = self.length(line[0], line[1])
        start_len = self.length(line[0], point)
        end_len = self.length(line[1], point)

        half_p = (line_len + start_len + end_len) / 2

        h = 2 * sqrt(half_p * (half_p - line_len) * (half_p - start_len) * (half_p - end_len)) / line_len

        return h

    def length(self, point_a, point_b):
        dx = point_a.x - point_b.x
        dy = point_a.y - point_b.y
        return sqrt(dx ** 2 + dy ** 2)

    def mousePressEvent(self, event):
        x, y = event.x(), event.y()
        if 0 <= x <= self.scene.width() and 0 <= y <= self.scene.height():
            self.add_to_scene(x, y)

    def add_to_scene(self, x, y):
        if self.ui.cut_mode.isChecked():
            if not self.is_cutter_ended:

                if self.cutter:
                    x0, y0 = self.cutter[-1].x, self.cutter[-1].y
                    self.scene.addLine(x, y, x0, y0, QPen(self.get_cutter_color(), 1))

            else:
                self.delete_cutter()

            self.cutter.append(Point(x, y))
            self.scene.addLine(x, y, x, y, QPen(self.get_cutter_color(), 3))
        else:
            if not self.is_polygon_ended:

                if self.polygon:

                    x0, y0 = self.polygon[len(self.polygon) - 1].x, self.polygon[len(self.polygon) - 1].y

                    if self.p_pressed and len(self.cutter) > 1:
                        n = len(self.cutter)

                        min_dist = -1
                        edge = -1

                        for i in range(n):
                            if i == n - 1:
                                dist = self.distance([self.cutter[i], self.cutter[0]], Point(x0, y0))
                            else:
                                dist = self.distance([self.cutter[i], self.cutter[i + 1]], Point(x0, y0))

                            if min_dist == -1:
                                min_dist = dist
                                edge = i
                            elif dist < min_dist:
                                min_dist = dist
                                edge = i

                        k = self.get_coeff(self.cutter, edge)

                        if k == None:
                            x = x0
                        elif k == 0:
                            y = y0
                        else:
                            b = y0 - k * x0
                            x = (y - b) / k
                            if x > self.scene.width():
                                x = self.scene.width() - 2
                                y = k * x + b
                            elif x < 0:
                                x = 2
                                y = k * x + b

                    if self.b_pressed and len(self.cutter) > 1: # Нужно выполнить привязку
                        min_dist = 10000  # минимальное расстояние до ребра
                        k_min = None
                        vertex = 0
                        for i in range(len(self.cutter)):
                            # угловой коэффициент ребра (ах + ву + с = 0)
                            # проверка вертикальности ребра
                            if abs(self.cutter[(i + 1) % len(self.cutter)].x - self.cutter[i].x) > 1e-7:
                                a = (self.cutter[(i + 1) % len(self.cutter)].y - self.cutter[i].y) \
                                    / (self.cutter[(i + 1) % len(self.cutter)].x - self.cutter[i].x)
                                b = -1
                                c = self.cutter[i].y - a * self.cutter[i].x
                                # расстояние до i-го ребра отсекателя от первой точки отрезка
                                dist = abs(a * x + b * y + c) / sqrt(a * a + b * b)
                            else:
                                dist = abs(x - self.cutter[i].x)
                                a = None
                            if dist < min_dist:
                                min_dist = dist
                                k_min = a
                                vertex = i
                        if k_min != None:
                            dy = min_dist / sqrt(k_min * k_min + 1)
                            dx = -k_min * dy
                            if abs(k_min * (x + dx) - (y + dy) + self.cutter[vertex].y - k_min * self.cutter[
                                vertex].x) > 1e-5:
                                dx, dy = -dx, -dy
                        else:
                            dy = 0
                            dx = self.cutter[vertex].x - x

                        x += dx
                        y += dy

                    self.scene.addLine(x, y, x0, y0, QPen(self.get_polygon_color(), 1))

            else:
                self.delete_polygon()

            self.polygon.append(Point(x, y))
            self.scene.addLine(x, y, x, y, QPen(self.get_polygon_color(), 3))

    def get_coeff(self, points, edge):
        x1, y1 = points[edge].x, points[edge].y
        if edge == len(points) - 1:
            x2, y2 = points[0].x, points[0].y
        else:
            x2, y2 = points[edge + 1].x, points[edge + 1].y

        if x2 - x1 != 0:
            return (y2 - y1) / (x2 - x1)
        return None

    def delete_cutter(self):
        self.scene.clear()
        self.cutter = []
        self.is_cutter_ended = False

        n = len(self.polygon)

        if not n:
            return

        color = self.get_polygon_color()

        for i in range(n - 1):
            self.scene.addLine(self.polygon[i].x, self.polygon[i].y,
                                   self.polygon[i + 1].x, self.polygon[i + 1].y,
                                   color)
            self.scene.addLine(self.polygon[i].x, self.polygon[i].y,
                               self.polygon[i].x, self.polygon[i].y,
                               QPen(color, 3))

        if self.is_polygon_ended:
            self.scene.addLine(self.polygon[0].x, self.polygon[0].y,
                               self.polygon[-1].x, self.polygon[-1].y,
                               color)

    def delete_polygon(self):
        self.scene.clear()
        self.polygon = []
        self.is_polygon_ended = False

        n = len(self.cutter)

        if not n:
            return

        color = self.get_cutter_color()

        for i in range(n - 1):
            self.scene.addLine(self.cutter[i].x, self.cutter[i].y,
                                   self.cutter[i + 1].x, self.cutter[i + 1].y,
                                   color)
            self.scene.addLine(self.cutter[i].x, self.cutter[i].y,
                               self.cutter[i].x, self.cutter[i].y,
                               QPen(color, 3))

        if self.is_cutter_ended:
            self.scene.addLine(self.cutter[0].x, self.cutter[0].y,
                               self.cutter[-1].x, self.cutter[-1].y,
                               color)

    def end_cutter(self):
        if len(self.cutter) < 3:
            self.show_error("Недостаточно ребер, чтобы замкнуть отсекатель.")
            return

        x, y = self.cutter[0].x, self.cutter[0].y
        self.scene.addLine(x, y, x, y, QPen(self.get_cutter_color(), 3))
        x0, y0 = self.cutter[-1].x, self.cutter[-1].y
        self.scene.addLine(x0, y0, x, y, self.get_cutter_color())

        self.is_cutter_ended = True

    def end_polygon(self):
        if len(self.polygon) < 3:
            self.show_error("Недостаточно ребер, чтобы замкнуть многоугольник.")
            return

        x, y = self.polygon[0].x, self.polygon[0].y
        self.scene.addLine(x, y, x, y, QPen(self.get_polygon_color(), 3))
        x0, y0 = self.polygon[-1].x, self.polygon[-1].y
        self.scene.addLine(x0, y0, x, y, self.get_polygon_color())

        self.is_polygon_ended = True

    def add_to_cutter(self):
        x = self.ui.enter_x.value()
        y = self.ui.enter_y.value()
        self.add_to_scene(x, y)

    def add_to_polygon(self):
        x = self.ui.enter_x.value()
        y = self.ui.enter_y.value()
        self.add_to_scene(x, y)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_B:
            self.b_pressed = True
        if event.key() == Qt.Key_P:
            self.p_pressed = True
        super(mywindow, self).keyPressEvent(event)

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_B: # Привязка
            self.b_pressed = False
        if event.key() == Qt.Key_P: # Параллельный ввод
            self.p_pressed = False
        super(mywindow, self).keyReleaseEvent(event)

    def show_error(self, msg):
        msg_error = QMessageBox()
        msg_error.setIcon(QMessageBox.Critical)
        msg_error.setStandardButtons(QMessageBox.Close)
        msg_error.setWindowTitle("Ошибка ввода данных")
        msg_error.setText(msg)
        msg_error.exec_()

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

    def get_polygon_color(self):
        color = self.polygon_colors.currentText()
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
        self.scene.setSceneRect(0, 0, 1280, 920)
        graphicView.setGeometry(0, 0, 1290, 930)
        self.scene.setBackgroundBrush(QColor(255, 255, 255))

    def clear(self):
        self.scene.clear()

        self.is_cutter_ended = False
        self.is_polygon_ended = False

        self.cutter = []
        self.polygon = []

    def exit(self):
        self.close()

app = QtWidgets.QApplication([])
application = mywindow()
application.show()

sys.exit(app.exec())