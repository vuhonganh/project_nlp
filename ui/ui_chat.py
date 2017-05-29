# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'simple_chat.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(586, 632)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.teLog = QtWidgets.QTextEdit(self.centralwidget)
        self.teLog.setGeometry(QtCore.QRect(20, 170, 531, 331))
        self.teLog.setReadOnly(True)
        self.teLog.setObjectName("teLog")
        self.pbSend = QtWidgets.QPushButton(self.centralwidget)
        self.pbSend.setGeometry(QtCore.QRect(480, 560, 61, 31))
        self.pbSend.setObjectName("pbSend")
        self.pbVoice = QtWidgets.QPushButton(self.centralwidget)
        self.pbVoice.setGeometry(QtCore.QRect(30, 510, 71, 31))
        self.pbVoice.setObjectName("pbVoice")
        self.teRules = QtWidgets.QTextEdit(self.centralwidget)
        self.teRules.setGeometry(QtCore.QRect(20, 19, 531, 141))
        self.teRules.setAutoFillBackground(False)
        self.teRules.setReadOnly(True)
        self.teRules.setObjectName("teRules")
        self.mleChat = QtWidgets.QLineEdit(self.centralwidget)
        self.mleChat.setGeometry(QtCore.QRect(20, 550, 451, 41))
        self.mleChat.setObjectName("mleChat")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 586, 19))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.mleChat.returnPressed.connect(self.pbSend.animateClick)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pbSend.setText(_translate("MainWindow", "Send"))
        self.pbVoice.setText(_translate("MainWindow", "Use Voice"))

