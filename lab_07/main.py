from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap, QPainter, QPen, QColor, QFont
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView, QMessageBox, QTableWidgetItem, QButtonGroup, QLabel
from PyQt5.QtCore import Qt, QEventLoop, QPoint, QRectF
from window import Ui_MainWindow
import sys
import time
from math import sqrt

LEFT = 0
RIGHT = 1
BOTTOM = 2
TOP = 3

class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("ЛР № 7: Реализация и исследование простого алгоритма отчесения "
                            "отрезка регулярным отсекателем.")
        self.move(255, 150)

        self.ui.c_lx.setText("100")
        self.ui.c_ly.setText("100")
        self.ui.c_rx.setText("400")
        self.ui.c_ry.setText("400")

        self.ui.s_xs.setText("50")
        self.ui.s_ys.setText("250")
        self.ui.s_xe.setText("150")
        self.ui.s_ye.setText("150")

        self.cutter = []
        self.sections = []

        self.temp_section = []
        self.temp_cutter = []
        self.last_point = []

        self.ctrl_pressed = False
        self.shift_pressed = False
        self.v_pressed = False
        self.h_pressed = False
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
        self.result_colors.setCurrentIndex(3)
        self.result_colors.setGeometry(800, 250, 280, 40)
        self.result_colors.setStyleSheet("background-color: rgb(255, 255, 255); "
                                          "color: rgb(0, 0, 0)")

        font = QFont()
        font.setPointSize(16)
        self.cutter_colors.setFont(font)
        self.section_colors.setFont(font)
        self.result_colors.setFont(font)

        self.ui.cut.clicked.connect(self.cut)
        self.ui.draw_cutter.clicked.connect(self.draw_cutter_by_dot_entry)
        self.ui.draw_section.clicked.connect(self.draw_section_by_dot_entry)
        self.ui.exit.clicked.connect(self.exit)
        self.ui.clear.clicked.connect(self.clear)

        self.scene_width = 770
        self.scene_height = 550

        self.create_scene()

    def cut(self):
        if self.cutter == []:
            self.show_error("Не введен отсекатель.")
            return
        if self.sections == []:
            self.show_error("Не введен ни один отрезок.")
            return
        mask_left = 0b0001
        mask_right = 0b0010
        mask_bottom = 0b0100
        mask_top = 0b1000

        self.painter.setPen(QPen(self.get_result_color(), 1))

        for section in self.sections:

            bits = list()

            bits.append(self.set_bits(section[0], self.cutter))
            bits.append(self.set_bits(section[1], self.cutter))

            #Полностью видимый отрезок, обе точки внутри границы
            if bits[0] == 0 and bits[1] == 0:
                self.painter.drawLine(section[0].x, section[0].y, section[1].x, section[1].y)
                self.label.setPixmap(self.pixmap)
                continue

            #Полностью невидимый отрезок
            if bits[0] & bits[1]:
                continue

            cur_index = 0
            res = list()

            if bits[0] == 0:
                res.append(section[0])
                cur_index = 1
            elif bits[1] == 0:
                res.append(section[1])
                cur_index = 1
                section.reverse()
                bits.reverse()

            while cur_index < 2:

                #Случай вертикальной прямой
                if section[0].x == section[1].x:
                    res.append(self.find_vertical_section(section[cur_index], self.cutter))
                    cur_index += 1
                    continue

                #Тангенс угла наклона отрезка
                m = (section[1].y - section[0].y) / (section[1].x - section[0].x)

                #Проверка пересечения с левым ребром
                if bits[cur_index] & mask_left: #Если вершина находится левее левой границы
                    #находим точку пересения
                    y = round(m * (self.cutter[LEFT] - section[cur_index].x) + section[cur_index].y)
                    if self.cutter[BOTTOM] <= y <= self.cutter[TOP]:
                        res.append(Point(self.cutter[LEFT], y))
                        cur_index += 1
                        continue

                # Проверка пересечения с правым ребром
                elif bits[cur_index] & mask_right:
                    y = round(m * (self.cutter[RIGHT] - section[cur_index].x) + section[cur_index].y)
                    if self.cutter[BOTTOM] <= y <= self.cutter[TOP]:
                        res.append(Point(self.cutter[RIGHT], y))
                        cur_index += 1
                        continue

                #if m == 0: # горизонтальный отрезок
                #    cur_index += 1
                #    continue

                # Проверка пересечения с врехним ребром
                if bits[cur_index] & mask_top:
                    x = round((self.cutter[TOP] - section[cur_index].y) / m + section[cur_index].x)
                    if self.cutter[LEFT] <= x <= self.cutter[RIGHT]:
                        res.append(Point(x, self.cutter[TOP]))
                        cur_index += 1
                        continue

                # Проверка пересечения с нижним ребром
                elif bits[cur_index] & mask_bottom:
                    x = round((self.cutter[BOTTOM] - section[cur_index].y) / m + section[cur_index].x)
                    if self.cutter[LEFT] <= x <= self.cutter[RIGHT]:
                        res.append(Point(x, self.cutter[BOTTOM]))
                        cur_index += 1
                        continue

                break

            if res:
                self.painter.drawLine(res[0].x, res[0].y, res[1].x, res[1].y)
                self.label.setPixmap(self.pixmap)


    def set_bits(self, vertex, cutter):

        mask_left = 0b0001
        mask_right = 0b0010
        mask_bottom = 0b0100
        mask_top = 0b1000

        bits = 0b0000

        if vertex.x < cutter[LEFT]:
            bits += mask_left
        if vertex.x > cutter[RIGHT]:
            bits += mask_right
        if vertex.y < cutter[BOTTOM]:
            bits += mask_bottom
        if vertex.y > cutter[TOP]:
            bits += mask_top

        return bits

    def find_vertical_section(self, vertex, cutter):
        if vertex.y > cutter[TOP]:
            return Point(vertex.x, cutter[TOP])
        elif vertex.y < cutter[BOTTOM]:
            return Point(vertex.x, cutter[BOTTOM])
        else:
            return vertex

    def draw_cutter_by_dot_entry(self):
        res_l = self.get_dot(self.ui.c_lx.text(), self.ui.c_ly.text())
        if not isinstance(res_l, tuple):
            return

        res_r = self.get_dot(self.ui.c_rx.text(), self.ui.c_ry.text())
        if not isinstance(res_r, tuple):
            return

        if self.cutter:
            self.delete_cutter()

        if res_l[0] == res_r[0] or res_l[1] == res_r[1]:
            self.show_error("Отсекатель не может вырождаться в прямую или точку.")
            return

        self.cutter = [res_l[0], res_r[0], res_l[1], res_r[1]]
        self.draw_cutter()

    def draw_section_by_dot_entry(self):
        res_s = self.get_dot(self.ui.s_xs.text(), self.ui.s_ys.text())
        if not isinstance(res_s, tuple):
            return

        res_e = self.get_dot(self.ui.s_xe.text(), self.ui.s_ye.text())
        if not isinstance(res_e, tuple):
            return

        self.draw_line(res_s[0], res_s[1], res_e[0], res_e[1])
        self.sections.append([Point(res_s[0], res_s[1]), Point(res_e[0], res_e[1])])

    def find_end(self, x, y):
        if self.cutter == []:
            self.show_error("Не введен отсекатель.")
            return

        xl, xr, yb, yt = self.cutter

        dist1 = abs(x - xl)
        dist2 = abs(x - xr)
        dist3 = abs(y - yb)
        dist4 = abs(y - yt)

        m = min(dist1, dist2, dist3, dist4)

        if m == dist1:
            return xl, y
        if m == dist2:
            return xr, y
        if m == dist3:
            return x, yb
        if m == dist4:
            return x, yt

    def find_nearest_end(self, x, y):
        if self.cutter == []:
            self.show_error("Не введен отсекатель.")
            return

        xl, xr, yb, yt = self.cutter

        if x < xl:
            if y < yb:
                return xl, yb
            if y > yt:
                return xl, yt
            return xl, y
        if x > xr:
            if y < yb:
                return xr, yb
            if y > yt:
                return xr, yt
            return xr, y

        if y < yb:
            if x < xl:
                return xl, yb
            if x > xr:
                return xr, yb
            return x, yb
        if y > yt:
            if x < xl:
                return xl, yt
            if x > xr:
                return xr, yt
            return x, yt

        if min(y - yb, yt - y) < min(x - xl, xr - x):
            if y - yb < yt - y:
                return x, yb
            else:
                return x, yt
        else:
            if x - xl < xr - x:
                return xl, y
            else:
                return xr, y

    def mousePressEvent(self, event):
        x, y = event.x(), event.y()
        self.last_point = Point(x, y)
        if self.ctrl_pressed:
            if self.alt_pressed:
                x, y = self.find_end(x, y)

            if not self.temp_section:
                self.temp_section.append(Point(x, y))
                self.draw_point(x, y)
            else:
                x0, y0 = self.temp_section[0].x, self.temp_section[0].y
                if self.v_pressed:
                    x = x0
                elif self.h_pressed:
                    y = y0

                self.draw_point(x, y)
                self.draw_line(x0, y0, x, y)

                self.sections.append([Point(x, y), Point(x0, y0)])
                self.update_section_label()
                self.temp_section = []

        if self.shift_pressed:

            if not self.temp_cutter:
                self.temp_cutter.append(Point(x, y))
            else:
                x0, y0 = self.temp_cutter[0].x, self.temp_cutter[0].y

                if x == x0 or y == y0:
                    self.show_error("Отсекатель не может вырождаться в прямую или точку.")
                    self.temp_section = []
                    return

                if self.cutter:
                    self.delete_cutter()
                self.cutter = [min(x0, x), max(x0, x), min(y0, y), max(y0, y)]
                self.draw_cutter()
                self.update_cutter_label()
                self.temp_cutter = []

    def draw_point(self, x, y):
        self.painter.setPen(QPen(Qt.black, 3))
        self.painter.drawPoint(QPoint(x, y))
        self.label.setPixmap(self.pixmap)

    def draw_line(self, x0, y0, x1, y1):
        self.painter.setPen(QPen(self.get_section_color(), 1))
        self.painter.drawLine(x0, y0, x1, y1)
        self.label.setPixmap(self.pixmap)

    def draw_cutter(self):
        self.painter.setPen(QPen(self.get_cutter_color(), 1))
        xl, xr, yb, yt = self.cutter
        self.painter.drawRect(xl, yb, xr - xl, yt - yb)
        self.label.setPixmap(self.pixmap)

    def delete_cutter(self):
        self.pixmap.fill(Qt.white)
        self.label.setPixmap(self.pixmap)
        self.label.setGeometry(0, 0, 770, 550)
        for section in self.sections:
            self.draw_line(section[0].x, section[0].y, section[1].x, section[1].y)

    def update_cutter_label(self):
        self.ui.c_lx.setText(str(self.cutter[LEFT]))
        self.ui.c_ly.setText(str(self.cutter[BOTTOM]))
        self.ui.c_rx.setText(str(self.cutter[RIGHT]))
        self.ui.c_ry.setText(str(self.cutter[TOP]))

    def update_section_label(self):
        self.ui.s_xs.setText(str(self.sections[-1][0].x))
        self.ui.s_ys.setText(str(self.sections[-1][0].y))
        self.ui.s_xe.setText(str(self.sections[-1][1].x))
        self.ui.s_ye.setText(str(self.sections[-1][1].y))

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
        super(mywindow, self).keyReleaseEvent(event)

    def get_dot(self, str_x, str_y):
        msg_error = QMessageBox()
        msg_error.setIcon(QMessageBox.Critical)
        msg_error.setStandardButtons(QMessageBox.Close)
        msg_error.setWindowTitle("Ошибка ввода данных")

        res = self.is_valid_coordinates(str_x, str_y)

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
        self.label = QLabel(self)
        self.label.setGeometry(0, 0, 770, 550)
        self.pixmap = QPixmap(self.label.size())
        self.pixmap.fill(Qt.white)
        self.label.setPixmap(self.pixmap)
        self.label.show()
        self.painter = QPainter(self.pixmap)

    def clear(self):
        self.pixmap.fill(Qt.white)
        self.label.setGeometry(0, 0, 770, 550)
        self.label.setPixmap(self.pixmap)
        self.painter.setPen(QPen(self.get_cutter_color(), 1))
        self.cutter = []
        self.sections = []
        self.temp_section = []
        self.temp_cutter = []
        self.last_point = []

    def exit(self):
        self.close()

app = QtWidgets.QApplication([])
application = mywindow()
application.show()

sys.exit(app.exec())