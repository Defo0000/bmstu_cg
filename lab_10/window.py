# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'window.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1044, 910)
        font = QtGui.QFont()
        font.setPointSize(15)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(770, 10, 181, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(780, 100, 181, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(780, 200, 181, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(380, 440, 201, 20))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(800, 550, 101, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.draw = QtWidgets.QPushButton(self.centralwidget)
        self.draw.setGeometry(QtCore.QRect(30, 810, 261, 61))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.draw.setFont(font)
        self.draw.setStyleSheet("color: rgb(0, 0, 0);\n"
"background-color: rgb(0, 166, 0);")
        self.draw.setObjectName("draw")
        self.clear = QtWidgets.QPushButton(self.centralwidget)
        self.clear.setGeometry(QtCore.QRect(390, 810, 261, 61))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.clear.setFont(font)
        self.clear.setStyleSheet("color: rgb(0, 0, 0);\n"
"background-color: rgb(255, 255, 255);")
        self.clear.setObjectName("clear")
        self.exit = QtWidgets.QPushButton(self.centralwidget)
        self.exit.setGeometry(QtCore.QRect(760, 810, 261, 61))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.exit.setFont(font)
        self.exit.setStyleSheet("background-color: rgb(255, 65, 65);\n"
"background-color: rgb(182, 46, 46);\n"
"color: rgb(0, 0, 0);")
        self.exit.setObjectName("exit")
        self.label_12 = QtWidgets.QLabel(self.centralwidget)
        self.label_12.setGeometry(QtCore.QRect(360, 490, 31, 20))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")
        self.scale = QtWidgets.QPushButton(self.centralwidget)
        self.scale.setGeometry(QtCore.QRect(480, 480, 151, 41))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.scale.setFont(font)
        self.scale.setStyleSheet("color: rgb(0, 0, 0);\n"
"background-color: rgb(154, 154, 154);")
        self.scale.setObjectName("scale")
        self.label_13 = QtWidgets.QLabel(self.centralwidget)
        self.label_13.setGeometry(QtCore.QRect(750, 600, 31, 20))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_13.setFont(font)
        self.label_13.setObjectName("label_13")
        self.label_14 = QtWidgets.QLabel(self.centralwidget)
        self.label_14.setGeometry(QtCore.QRect(750, 660, 31, 20))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_14.setFont(font)
        self.label_14.setObjectName("label_14")
        self.label_15 = QtWidgets.QLabel(self.centralwidget)
        self.label_15.setGeometry(QtCore.QRect(750, 720, 31, 20))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_15.setFont(font)
        self.label_15.setObjectName("label_15")
        self.rotate_but_x = QtWidgets.QPushButton(self.centralwidget)
        self.rotate_but_x.setGeometry(QtCore.QRect(870, 590, 151, 41))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.rotate_but_x.setFont(font)
        self.rotate_but_x.setStyleSheet("color: rgb(0, 0, 0);\n"
"background-color: rgb(154, 154, 154);")
        self.rotate_but_x.setObjectName("rotate_but_x")
        self.rotate_but_y = QtWidgets.QPushButton(self.centralwidget)
        self.rotate_but_y.setGeometry(QtCore.QRect(870, 650, 151, 41))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.rotate_but_y.setFont(font)
        self.rotate_but_y.setStyleSheet("color: rgb(0, 0, 0);\n"
"background-color: rgb(154, 154, 154);")
        self.rotate_but_y.setObjectName("rotate_but_y")
        self.rotate_but_z = QtWidgets.QPushButton(self.centralwidget)
        self.rotate_but_z.setGeometry(QtCore.QRect(870, 710, 151, 41))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.rotate_but_z.setFont(font)
        self.rotate_but_z.setStyleSheet("color: rgb(0, 0, 0);\n"
"background-color: rgb(154, 154, 154);")
        self.rotate_but_z.setObjectName("rotate_but_z")
        self.label_16 = QtWidgets.QLabel(self.centralwidget)
        self.label_16.setGeometry(QtCore.QRect(870, 250, 31, 20))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_16.setFont(font)
        self.label_16.setObjectName("label_16")
        self.label_17 = QtWidgets.QLabel(self.centralwidget)
        self.label_17.setGeometry(QtCore.QRect(970, 250, 31, 20))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_17.setFont(font)
        self.label_17.setObjectName("label_17")
        self.label_18 = QtWidgets.QLabel(self.centralwidget)
        self.label_18.setGeometry(QtCore.QRect(730, 290, 111, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_18.setFont(font)
        self.label_18.setObjectName("label_18")
        self.label_19 = QtWidgets.QLabel(self.centralwidget)
        self.label_19.setGeometry(QtCore.QRect(730, 340, 101, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_19.setFont(font)
        self.label_19.setObjectName("label_19")
        self.label_20 = QtWidgets.QLabel(self.centralwidget)
        self.label_20.setGeometry(QtCore.QRect(730, 390, 111, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_20.setFont(font)
        self.label_20.setObjectName("label_20")
        self.scale_k = QtWidgets.QSpinBox(self.centralwidget)
        self.scale_k.setGeometry(QtCore.QRect(400, 480, 71, 41))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.scale_k.setFont(font)
        self.scale_k.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")
        self.scale_k.setMinimum(1)
        self.scale_k.setMaximum(1000)
        self.scale_k.setObjectName("scale_k")
        self.step_x = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.step_x.setGeometry(QtCore.QRect(850, 380, 81, 41))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.step_x.setFont(font)
        self.step_x.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")
        self.step_x.setDecimals(1)
        self.step_x.setMinimum(0.1)
        self.step_x.setMaximum(1.0)
        self.step_x.setSingleStep(0.1)
        self.step_x.setObjectName("step_x")
        self.step_z = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.step_z.setGeometry(QtCore.QRect(950, 380, 81, 41))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.step_z.setFont(font)
        self.step_z.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")
        self.step_z.setDecimals(1)
        self.step_z.setMinimum(0.1)
        self.step_z.setMaximum(1.0)
        self.step_z.setSingleStep(0.1)
        self.step_z.setObjectName("step_z")
        self.angle_x = QtWidgets.QSpinBox(self.centralwidget)
        self.angle_x.setGeometry(QtCore.QRect(790, 590, 71, 41))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.angle_x.setFont(font)
        self.angle_x.setStyleSheet("color: rgb(0, 0, 0);\n"
"background-color: rgb(255, 255, 255);")
        self.angle_x.setMinimum(-360)
        self.angle_x.setMaximum(360)
        self.angle_x.setObjectName("angle_x")
        self.angle_y = QtWidgets.QSpinBox(self.centralwidget)
        self.angle_y.setGeometry(QtCore.QRect(790, 650, 71, 41))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.angle_y.setFont(font)
        self.angle_y.setStyleSheet("color: rgb(0, 0, 0);\n"
"background-color: rgb(255, 255, 255);")
        self.angle_y.setMinimum(-360)
        self.angle_y.setMaximum(360)
        self.angle_y.setObjectName("angle_y")
        self.angle_z = QtWidgets.QSpinBox(self.centralwidget)
        self.angle_z.setGeometry(QtCore.QRect(790, 710, 71, 41))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.angle_z.setFont(font)
        self.angle_z.setStyleSheet("color: rgb(0, 0, 0);\n"
"background-color: rgb(255, 255, 255);")
        self.angle_z.setMinimum(-360)
        self.angle_z.setMaximum(360)
        self.angle_z.setObjectName("angle_z")
        self.start_x = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.start_x.setGeometry(QtCore.QRect(850, 280, 81, 41))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.start_x.setFont(font)
        self.start_x.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")
        self.start_x.setDecimals(1)
        self.start_x.setMinimum(-100.0)
        self.start_x.setMaximum(100.0)
        self.start_x.setSingleStep(0.1)
        self.start_x.setObjectName("start_x")
        self.end_x = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.end_x.setGeometry(QtCore.QRect(850, 330, 81, 41))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.end_x.setFont(font)
        self.end_x.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")
        self.end_x.setDecimals(1)
        self.end_x.setMinimum(-100.0)
        self.end_x.setMaximum(100.0)
        self.end_x.setSingleStep(0.1)
        self.end_x.setObjectName("end_x")
        self.start_z = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.start_z.setGeometry(QtCore.QRect(950, 280, 81, 41))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.start_z.setFont(font)
        self.start_z.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")
        self.start_z.setDecimals(1)
        self.start_z.setMinimum(-100.0)
        self.start_z.setMaximum(100.0)
        self.start_z.setSingleStep(0.1)
        self.start_z.setObjectName("start_z")
        self.end_z = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.end_z.setGeometry(QtCore.QRect(950, 330, 81, 41))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.end_z.setFont(font)
        self.end_z.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")
        self.end_z.setDecimals(1)
        self.end_z.setMinimum(-100.0)
        self.end_z.setMaximum(100.0)
        self.end_z.setSingleStep(0.1)
        self.end_z.setObjectName("end_z")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1044, 18))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Цвет фигуры"))
        self.label_2.setText(_translate("MainWindow", "Функция"))
        self.label_3.setText(_translate("MainWindow", "Пределы"))
        self.label_4.setText(_translate("MainWindow", "Масштабирование"))
        self.label_5.setText(_translate("MainWindow", "Поворот"))
        self.draw.setText(_translate("MainWindow", "Нарисовать"))
        self.clear.setText(_translate("MainWindow", "Очистить поле"))
        self.exit.setText(_translate("MainWindow", "Выход"))
        self.label_12.setText(_translate("MainWindow", "К:"))
        self.scale.setText(_translate("MainWindow", "Применить"))
        self.label_13.setText(_translate("MainWindow", "X:"))
        self.label_14.setText(_translate("MainWindow", "Y:"))
        self.label_15.setText(_translate("MainWindow", "Z:"))
        self.rotate_but_x.setText(_translate("MainWindow", "Применить"))
        self.rotate_but_y.setText(_translate("MainWindow", "Применить"))
        self.rotate_but_z.setText(_translate("MainWindow", "Применить"))
        self.label_16.setText(_translate("MainWindow", "X:"))
        self.label_17.setText(_translate("MainWindow", "Z:"))
        self.label_18.setText(_translate("MainWindow", "Начало:"))
        self.label_19.setText(_translate("MainWindow", "Конец:"))
        self.label_20.setText(_translate("MainWindow", "Шаг:"))
