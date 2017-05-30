from utils import reader_2
from utils import robot_simu
from ui.ui_chat import Ui_MainWindow
from PyQt5 import QtWidgets, QtGui, QtCore
import sys
from utils.action import ActionGo, ActionTurn

# set Rules text
rules = "go forward/backward X (centimeters) \nturn left/right X (degrees)"
act_dict = {"go": ActionGo, "turn": ActionTurn}


class Chat(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        # super(Chat, self).__init__()
        super().__init__()  # python 3 syntax allows this
        self.setupUi(self)
        self.teRules.setText(rules)
        self.pbSend.clicked.connect(self.sendClicked)
        self.rd = reader_2.Reader2("data/small_synonyms.txt")
        self.robot = robot_simu.Robot()

    def sendClicked(self):
        human_cmd = self.mleChat.text()
        self.mleChat.clear()
        self.human_log(human_cmd)
        info_dict = self.rd.read(human_cmd)
        act = act_dict[info_dict["intent"]](info_dict)
        robot_rep = act.do_act(self.robot)
        self.robot_log(robot_rep)

    def human_log(self, text):
        self.teLog.setTextColor(QtGui.QColor('blue'))
        self.teLog.insertPlainText("You: ")
        self.teLog.moveCursor(QtGui.QTextCursor.End)
        self.teLog.setTextColor(QtGui.QColor('black'))
        self.teLog.insertPlainText(text + "\n")

    def robot_log(self, text):
        self.teLog.setTextColor(QtGui.QColor('orange'))
        self.teLog.insertPlainText("Robot: ")
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
