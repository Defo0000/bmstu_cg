# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'window.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1446, 849)
        MainWindow.setStyleSheet("background-color: rgb(173, 173, 173);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.cutter_color = QtWidgets.QLabel(self.centralwidget)
        self.cutter_color.setGeometry(QtCore.QRect(840, 30, 181, 31))
        font = QtGui.QFont()
        font.setPointSize(17)
        self.cutter_color.setFont(font)
        self.cutter_color.setStyleSheet("color: rgb(0, 0, 0);")
        self.cutter_color.setObjectName("cutter_color")
        self.section_color = QtWidgets.QLabel(self.centralwidget)
        self.section_color.setGeometry(QtCore.QRect(840, 120, 181, 31))
        font = QtGui.QFont()
        font.setPointSize(17)
        self.section_color.setFont(font)
        self.section_color.setStyleSheet("color: rgb(0, 0, 0);")
        self.section_color.setObjectName("section_color")
        self.result_color = QtWidgets.QLabel(self.centralwidget)
        self.result_color.setGeometry(QtCore.QRect(840, 210, 181, 31))
        font = QtGui.QFont()
        font.setPointSize(17)
        self.result_color.setFont(font)
        self.result_color.setStyleSheet("color: rgb(0, 0, 0);")
        self.result_color.setObjectName("result_color")
        self.cut = QtWidgets.QPushButton(self.centralwidget)
        self.cut.setGeometry(QtCore.QRect(790, 320, 301, 51))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.cut.setFont(font)
        self.cut.setStyleSheet("color: rgb(0, 0, 0);\n"
"alternate-background-color:  rgb(133, 133, 199);\n"
"background-color: rgb(133, 133, 199);\n"
"")
        self.cut.setObjectName("cut")
        self.clear = QtWidgets.QPushButton(self.centralwidget)
        self.clear.setGeometry(QtCore.QRect(790, 410, 301, 51))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.clear.setFont(font)
        self.clear.setStyleSheet("color: rgb(0, 0, 0);\n"
"alternate-background-color: rgb(118, 145, 161);\n"
"background-color: rgb(118, 145, 161);")
        self.clear.setObjectName("clear")
        self.exit = QtWidgets.QPushButton(self.centralwidget)
        self.exit.setGeometry(QtCore.QRect(790, 500, 301, 51))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.exit.setFont(font)
        self.exit.setStyleSheet("color: rgb(0, 0, 0);\n"
"background-color: rgb(255, 97, 97);")
        self.exit.setObjectName("exit")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(1170, 20, 231, 31))
        font = QtGui.QFont()
        font.setPointSize(17)
        self.label.setFont(font)
        self.label.setStyleSheet("color: rgb(0, 0, 0);")
        self.label.setObjectName("label")
        self.c_lx = QtWidgets.QLineEdit(self.centralwidget)
        self.c_lx.setGeometry(QtCore.QRect(1160, 90, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.c_lx.setFont(font)
        self.c_lx.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")
        self.c_lx.setObjectName("c_lx")
        self.c_ly = QtWidgets.QLineEdit(self.centralwidget)
        self.c_ly.setGeometry(QtCore.QRect(1300, 90, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.c_ly.setFont(font)
        self.c_ly.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")
        self.c_ly.setObjectName("c_ly")
        self.c_rx = QtWidgets.QLineEdit(self.centralwidget)
        self.c_rx.setGeometry(QtCore.QRect(1160, 160, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.c_rx.setFont(font)
        self.c_rx.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")
        self.c_rx.setObjectName("c_rx")
        self.c_ry = QtWidgets.QLineEdit(self.centralwidget)
        self.c_ry.setGeometry(QtCore.QRect(1300, 160, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.c_ry.setFont(font)
        self.c_ry.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")
        self.c_ry.setObjectName("c_ry")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(1180, 70, 76, 20))
        self.label_2.setStyleSheet("color: rgb(0, 0, 0);")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(1320, 70, 76, 20))
        self.label_3.setStyleSheet("color: rgb(0, 0, 0);")
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(1320, 140, 76, 20))
        self.label_4.setStyleSheet("color: rgb(0, 0, 0);")
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(1180, 140, 76, 20))
        self.label_5.setStyleSheet("color: rgb(0, 0, 0);")
        self.label_5.setObjectName("label_5")
        self.draw_cutter = QtWidgets.QPushButton(self.centralwidget)
        self.draw_cutter.setGeometry(QtCore.QRect(1140, 210, 281, 61))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.draw_cutter.setFont(font)
        self.draw_cutter.setStyleSheet("color: rgb(0, 0, 0);\n"
"background-color: rgb(186, 255, 161);")
        self.draw_cutter.setObjectName("draw_cutter")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(200, 600, 1081, 21))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.label_6.setFont(font)
        self.label_6.setStyleSheet("color: rgb(0, 0, 0);")
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(1320, 350, 76, 20))
        self.label_7.setStyleSheet("color: rgb(0, 0, 0);")
        self.label_7.setObjectName("label_7")
        self.draw_section = QtWidgets.QPushButton(self.centralwidget)
        self.draw_section.setGeometry(QtCore.QRect(1140, 490, 281, 61))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.draw_section.setFont(font)
        self.draw_section.setStyleSheet("color: rgb(0, 0, 0);\n"
"background-color: rgb(186, 255, 161);")
        self.draw_section.setObjectName("draw_section")
        self.s_xe = QtWidgets.QLineEdit(self.centralwidget)
        self.s_xe.setGeometry(QtCore.QRect(1160, 440, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.s_xe.setFont(font)
        self.s_xe.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")
        self.s_xe.setObjectName("s_xe")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(1170, 300, 231, 31))
        font = QtGui.QFont()
        font.setPointSize(17)
        self.label_8.setFont(font)
        self.label_8.setStyleSheet("color: rgb(0, 0, 0);")
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(1320, 420, 76, 20))
        self.label_9.setStyleSheet("color: rgb(0, 0, 0);")
        self.label_9.setObjectName("label_9")
        self.s_xs = QtWidgets.QLineEdit(self.centralwidget)
        self.s_xs.setGeometry(QtCore.QRect(1160, 370, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.s_xs.setFont(font)
        self.s_xs.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")
        self.s_xs.setObjectName("s_xs")
        self.s_ye = QtWidgets.QLineEdit(self.centralwidget)
        self.s_ye.setGeometry(QtCore.QRect(1300, 440, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.s_ye.setFont(font)
        self.s_ye.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")
        self.s_ye.setObjectName("s_ye")
        self.s_ys = QtWidgets.QLineEdit(self.centralwidget)
        self.s_ys.setGeometry(QtCore.QRect(1300, 370, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.s_ys.setFont(font)
        self.s_ys.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")
        self.s_ys.setObjectName("s_ys")
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setGeometry(QtCore.QRect(1180, 420, 76, 20))
        self.label_10.setStyleSheet("color: rgb(0, 0, 0);")
        self.label_10.setObjectName("label_10")
        self.label_11 = QtWidgets.QLabel(self.centralwidget)
        self.label_11.setGeometry(QtCore.QRect(1180, 350, 76, 20))
        self.label_11.setStyleSheet("color: rgb(0, 0, 0);")
        self.label_11.setObjectName("label_11")
        self.label_12 = QtWidgets.QLabel(self.centralwidget)
        self.label_12.setGeometry(QtCore.QRect(200, 650, 1081, 21))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.label_12.setFont(font)
        self.label_12.setStyleSheet("color: rgb(0, 0, 0);")
        self.label_12.setObjectName("label_12")
        self.label_13 = QtWidgets.QLabel(self.centralwidget)
        self.label_13.setGeometry(QtCore.QRect(200, 700, 1081, 21))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.label_13.setFont(font)
        self.label_13.setStyleSheet("color: rgb(0, 0, 0);")
        self.label_13.setObjectName("label_13")
        self.label_14 = QtWidgets.QLabel(self.centralwidget)
        self.label_14.setGeometry(QtCore.QRect(200, 740, 1081, 21))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.label_14.setFont(font)
        self.label_14.setStyleSheet("color: rgb(0, 0, 0);")
        self.label_14.setObjectName("label_14")
        self.label_15 = QtWidgets.QLabel(self.centralwidget)
        self.label_15.setGeometry(QtCore.QRect(200, 780, 1081, 21))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.label_15.setFont(font)
        self.label_15.setStyleSheet("color: rgb(0, 0, 0);")
        self.label_15.setObjectName("label_15")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1446, 32))
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
        self.cutter_color.setText(_translate("MainWindow", "Цвет отсекателя"))
        self.section_color.setText(_translate("MainWindow", "Цвет отрезков"))
        self.result_color.setText(_translate("MainWindow", "Цвет результата"))
        self.cut.setText(_translate("MainWindow", "Отсечь"))
        self.clear.setText(_translate("MainWindow", "Очистить поле"))
        self.exit.setText(_translate("MainWindow", "Выход"))
        self.label.setText(_translate("MainWindow", "Границы отсекателя"))
        self.label_2.setText(_translate("MainWindow", "X (лев.)"))
        self.label_3.setText(_translate("MainWindow", "У (нижн.)"))
        self.label_4.setText(_translate("MainWindow", "У (верх.)"))
        self.label_5.setText(_translate("MainWindow", "X (прав.)"))
        self.draw_cutter.setText(_translate("MainWindow", "Отобразить отсекатель"))
        self.label_6.setText(_translate("MainWindow", " Зажмите Shift и кликните 2 раза мышкой, обозначив верхний левый и нижний правый угол, для ввода отсекателя."))
        self.label_7.setText(_translate("MainWindow", "У (нач.)"))
        self.draw_section.setText(_translate("MainWindow", "Отобразить отрезок"))
        self.label_8.setText(_translate("MainWindow", "Координаты отрезка"))
        self.label_9.setText(_translate("MainWindow", "У (кон.)"))
        self.label_10.setText(_translate("MainWindow", "Х (кон.)"))
        self.label_11.setText(_translate("MainWindow", "X (нач.)"))
        self.label_12.setText(_translate("MainWindow", " Зажмите Ctrl и кликните 2 раза мышкой, обозначив концы отрезка, для ввода отрезка."))
        self.label_13.setText(_translate("MainWindow", " Зажмите Ctrl+V и кликните 2 раза мышкой, обозначив концы отрезка, для ввода вертикального отрезка."))
        self.label_14.setText(_translate("MainWindow", " Зажмите Ctrl+H и кликните 2 раза мышкой, обозначив концы отрезка, для ввода горизонтального отрезка."))
        self.label_15.setText(_translate("MainWindow", "Зажмите Ctrl + ALT для привязки точки к границе"))
