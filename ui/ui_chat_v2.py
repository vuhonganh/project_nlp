# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'simple_chat_v2.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1076, 632)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.pbVoice = QtWidgets.QPushButton(self.centralwidget)
        self.pbVoice.setObjectName("pbVoice")
        self.gridLayout.addWidget(self.pbVoice, 2, 1, 1, 1)
        self.pbSend = QtWidgets.QPushButton(self.centralwidget)
        self.pbSend.setObjectName("pbSend")
        self.gridLayout.addWidget(self.pbSend, 3, 2, 1, 1)
        self.mleChat = QtWidgets.QLineEdit(self.centralwidget)
        self.mleChat.setObjectName("mleChat")
        self.gridLayout.addWidget(self.mleChat, 3, 1, 1, 1)
        self.teRules = QtWidgets.QTextEdit(self.centralwidget)
        self.teRules.setAutoFillBackground(False)
        self.teRules.setReadOnly(True)
        self.teRules.setObjectName("teRules")
        self.gridLayout.addWidget(self.teRules, 0, 1, 1, 2)
        self.teLog = QtWidgets.QTextEdit(self.centralwidget)
        self.teLog.setReadOnly(True)
        self.teLog.setObjectName("teLog")
        self.gridLayout.addWidget(self.teLog, 1, 1, 1, 2)
        self.imgView = QtWidgets.QWidget(self.centralwidget)
        self.imgView.setObjectName("imgView")
        self.lImg = QtWidgets.QLabel(self.imgView)
        self.lImg.setGeometry(QtCore.QRect(10, 10, 361, 281))
        self.lImg.setObjectName("lImg")
        self.gridLayout.addWidget(self.imgView, 0, 0, 2, 1)
        self.gridLayout.setColumnStretch(0, 40)
        self.gridLayout.setColumnStretch(1, 60)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1076, 19))
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
        self.pbVoice.setText(_translate("MainWindow", "Use Voice"))
        self.pbSend.setText(_translate("MainWindow", "Send"))
        self.lImg.setText(_translate("MainWindow", "TextLabel"))

