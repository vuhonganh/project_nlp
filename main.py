from utils import reader
from utils import robot_simu
from ui.ui_chat import Ui_MainWindow
from PyQt5 import QtWidgets, QtGui, QtCore
import sys
# rd = reader.Reader("data/small_synonyms.txt", debug=True)
# robot = robot_simu.Robot()
# while True:
#     print("Enter command: ", end='')
#     cmd = input()
#     if cmd == "exit":
#         break
#     intent, specs = rd.get_response(cmd)
#     if intent == "UNK":
#         print("Do not understand. Make sure you use predefined syntax correctly!")
#     else:
#         robot.do_cmd(intent, specs)

# set Rules text
rules = """
go forward/backward X 
turn left/right X (degrees)
"""

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
        self.teLog.append("you:" + text)
        intent, specs = self.rd.get_response(text)
        self.robot.do_cmd(intent, specs)


    def keyPressEvent(self, a0: QtGui.QKeyEvent):
        if a0.key() == QtCore.Qt.Key_Escape:
            self.close()
        super().keyPressEvent(a0)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    my_chat = Chat()
    my_chat.show()

    sys.exit(app.exec_())