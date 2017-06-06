from utils import reader_2
from utils import robot_simu
from utils.asr import VoiceRec
from utils.asr import RecThread
from utils.asr import STT
from ui.ui_chat import Ui_MainWindow
from PyQt5 import QtWidgets, QtGui, QtCore
import sys
from utils.action import ActionGo, ActionTurn
import cozmo
# set Rules text
rules = "go forward/backward X (millimeters) \nturn left/right X (degrees)"
act_dict = {"go": ActionGo, "turn": ActionTurn}


class Chat(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, acozmo=None):
        # super(Chat, self).__init__()
        super().__init__()  # python 3 syntax allows this
        self.rd = reader_2.Reader2("data/small_synonyms.txt")
        self.robot = robot_simu.Robot(acozmo)
        self.setupUi(self)
        self.teRules.setText(rules)

        # click button bind to appropriate function
        self.pbSend.clicked.connect(self.sendClicked)
        self.pbVoice.clicked.connect(self.voiceClicked)

        # FIRST try
        self.voice_thread = None
        self.voice_thread = VoiceRec(recording_time=5)
        self.voice_thread.signal_recording_done.connect(self.recordReady)
        self.voice_thread.start()

        # SECOND try
        self._speechRecWorker = None
        # self._speechRecWorker = RecThread(1)
        # self._speechRecWorker.speechReady.connect(self.recordReady)

        self.stt_thread = STT()
        self.stt_thread.signal_stt_done.connect(self.sttReady)
        self.stt_thread.start()

        # make cursor focus on chat line
        self.mleChat.setFocus()

    def sendClicked(self):
        human_cmd = self.mleChat.text()
        self.mleChat.clear()
        self.human_log(human_cmd)
        info_dict = self.rd.read(human_cmd)

        if info_dict["intent"] not in act_dict.keys():
            self.robot_log("Unknown command!")
        else:
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

    def voiceClicked(self):
        print("voice clicked")
        self.pbVoice.setEnabled(False)
        if self.voice_thread:
            self.voice_thread.activate()
        if self._speechRecWorker:
            self._speechRecWorker.record()

    @QtCore.pyqtSlot(str)
    def recordReady(self, filename):
        print("record ready")
        # if self.voice_thread:
        #     self.voice_thread.deactivate()
        self.pbVoice.setEnabled(True)
        self.teLog.insertPlainText('LOG: sound is recorded to ' + filename + '\n')
        self.stt_thread.activate(filename)


    @QtCore.pyqtSlot(list)
    def sttReady(self, list_trans):
        print("stt ready")
        if len(list_trans) > 0:
            best = list_trans[0]
            self.mleChat.setText(best)
            self.sendClicked()
        else:
            print("list of transcripts is empty")

    def keyPressEvent(self, a0: QtGui.QKeyEvent):
        if a0.key() == QtCore.Qt.Key_Escape:
            self.close()

        super().keyPressEvent(a0)


def run(sdk_conn):
    qt_app = QtWidgets.QApplication(sys.argv)
    my_cozmo = sdk_conn.wait_for_robot()
    my_cozmo.drive_off_charger_on_connect = False
    my_cozmo.camera.color_image_enabled = True
    # img = my_cozmo.world.latest_image
    this_chat = Chat(my_cozmo)
    this_chat.show()
    sys.exit(qt_app.exec_())

if __name__ == "__main__":
    try:
        cozmo.connect(run)
    except cozmo.NoDevicesFound:
        print("cozmo not connected, running without it")
        app = QtWidgets.QApplication(sys.argv)
        my_chat = Chat()
        my_chat.show()
        sys.exit(app.exec_())
