# -*- coding: utf-8 -*-

from utils import reader
from utils import robot_simu

import sys

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        # reader and robot simulator
        self.rd = reader.Reader("data/small_synonyms.txt", debug=True)
        self.robot = robot_simu.Robot()


        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(621, 587)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(20, 10, 551, 431))
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName("textEdit")
        self.textEdit.setHtml("<img src=images/test.png />")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setGeometry(QtCore.QRect(20, 484, 491, 51))
        self.plainTextEdit.setObjectName("plainTextEdit")
        # self.plainTextEdit.keyPressEvent.connect(self.textEntered)
        # button SEND
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(520, 490, 51, 31))
        self.pushButton.setObjectName("pushButton")

        self.pushButton.clicked.connect(self.sendClicked)

        # button USE VOICE
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(60, 450, 71, 31))
        self.pushButton_2.setObjectName("pushButton_2")

        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 621, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)




    def sendClicked(self):
        input_text = self.plainTextEdit.toPlainText()
        intent, specs = self.rd.get_response(input_text)
        self.statusbar.showMessage("current intent is " + intent)
        self.robot.do_cmd(intent, specs)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Send"))
        self.pushButton_2.setText(_translate("MainWindow", "Use Voice"))

    # def send_button_clicked(self):
    #     # self.statusbar.showMessage()
    #     self.statusBar().showMessage(self.sender().text() + "was pressed")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainWindow()
    wd = QtWidgets.QMainWindow()
    ui.setupUi(wd)

    wd.show()
    sys.exit(app.exec_())