from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import QPen, QBrush, QColor, QPainter, QFont
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView, QMessageBox, QInputDialog, QDialog, QLineEdit, \
    QDialogButtonBox, QFormLayout
from window import Ui_MainWindow
from PyQt5.QtCore import Qt, QRect
import sys

class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton_5.clicked.connect(self.exit)
        self.create_scene()
        self.move(200, 0)

    def create_scene(self):
        self.scene = QGraphicsScene()
        graphicView = QGraphicsView(self.scene, self)
        self.pen = QPen(Qt.white, 4)
        graphicView.setGeometry(400, 10, 980, 900)
        self.scene.setBackgroundBrush(QColor(255, 255, 255));

    def exit(self):
        self.close()

app = QtWidgets.QApplication([])
application = mywindow()
application.show()

sys.exit(app.exec())
