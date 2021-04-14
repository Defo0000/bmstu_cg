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
        MainWindow.resize(1375, 900)
        MainWindow.setStyleSheet("background-color: rgb(52, 101, 164);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.exit_btn = QtWidgets.QPushButton(self.centralwidget)
        self.exit_btn.setGeometry(QtCore.QRect(1039, 800, 311, 41))
        self.exit_btn.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.exit_btn.setObjectName("exit_btn")
        self.clear_btn = QtWidgets.QPushButton(self.centralwidget)
        self.clear_btn.setGeometry(QtCore.QRect(1040, 750, 311, 41))
        self.clear_btn.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.clear_btn.setObjectName("clear_btn")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(1040, 290, 161, 41))
        self.label_4.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")
        self.label_4.setObjectName("label_4")
        self.r_lbl = QtWidgets.QLineEdit(self.centralwidget)
        self.r_lbl.setGeometry(QtCore.QRect(1220, 290, 131, 41))
        self.r_lbl.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.r_lbl.setObjectName("r_lbl")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(1040, 340, 161, 41))
        self.label_5.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")
        self.label_5.setObjectName("label_5")
        self.a_lbl = QtWidgets.QLineEdit(self.centralwidget)
        self.a_lbl.setGeometry(QtCore.QRect(1220, 340, 131, 41))
        self.a_lbl.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.a_lbl.setObjectName("a_lbl")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(1040, 390, 161, 41))
        self.label_6.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")
        self.label_6.setObjectName("label_6")
        self.b_lbl = QtWidgets.QLineEdit(self.centralwidget)
        self.b_lbl.setGeometry(QtCore.QRect(1220, 390, 131, 41))
        self.b_lbl.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.b_lbl.setObjectName("b_lbl")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(1040, 450, 311, 41))
        self.label.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")
        self.label.setObjectName("label")
        self.xc_lbl = QtWidgets.QLineEdit(self.centralwidget)
        self.xc_lbl.setGeometry(QtCore.QRect(1070, 510, 121, 41))
        self.xc_lbl.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.xc_lbl.setObjectName("xc_lbl")
        self.yc_lbl = QtWidgets.QLineEdit(self.centralwidget)
        self.yc_lbl.setGeometry(QtCore.QRect(1230, 510, 121, 41))
        self.yc_lbl.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.yc_lbl.setObjectName("yc_lbl")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(1200, 510, 21, 41))
        self.label_3.setObjectName("label_3")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(1040, 510, 21, 41))
        self.label_2.setObjectName("label_2")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(1170, 20, 85, 22))
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(1160, 100, 121, 22))
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(1180, 180, 51, 22))
        self.label_9.setObjectName("label_9")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1375, 27))
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
        self.exit_btn.setText(_translate("MainWindow", "Выход"))
        self.clear_btn.setText(_translate("MainWindow", "Очистить поле"))
        self.label_4.setText(_translate("MainWindow", "  Радиус окр-ти:"))
        self.label_5.setText(_translate("MainWindow", "    Полуось а:"))
        self.label_6.setText(_translate("MainWindow", "    Полуось b:"))
        self.label.setText(_translate("MainWindow", "              Координаты центра:"))
        self.label_3.setText(_translate("MainWindow", "У:"))
        self.label_2.setText(_translate("MainWindow", "Х:"))
        self.label_7.setText(_translate("MainWindow", "Режим"))
        self.label_8.setText(_translate("MainWindow", "Алгоритм"))
        self.label_9.setText(_translate("MainWindow", "Цвет"))
