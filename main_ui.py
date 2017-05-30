from utils import reader
from utils import robot_simu
from ui.ui_chat import Ui_MainWindow
from PyQt5 import QtWidgets, QtGui, QtCore
import sys

# set Rules text
rules = "go forward/backward X \nturn left/right X (degrees)"

class Chat(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        # super(Chat, self).__init__()
        super().__init__()  # python 3 syntax allows this
        self.setupUi(self)
        self.teRules.setText(rules)
        self.pbSend.clicked.connect(self.sendClicked)
        self.rd = reader.Reader("data/small_synonyms.txt", debug=False)
        self.robot = robot_simu.Robot()

    def sendClicked(self):
        text = self.mleChat.text()
        self.mleChat.clear()
        self.human_log(text)
        intent, specs = self.rd.get_response(text)
        self.robot.do_cmd(intent, specs)

    def human_log(self, text):
        self.teLog.setTextColor(QtGui.QColor('blue'))
        self.teLog.insertPlainText("You: ")
        self.teLog.moveCursor(QtGui.QTextCursor.End)
        self.teLog.setTextColor(QtGui.QColor('black'))
        self.teLog.insertPlainText(text + "\n")


    def keyPressEvent(self, a0: QtGui.QKeyEvent):
        if a0.key() == QtCore.Qt.Key_Escape:
            self.close()
        super().keyPressEvent(a0)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    my_chat = Chat()
    my_chat.show()

    sys.exit(app.exec_())
