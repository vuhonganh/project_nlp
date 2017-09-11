from utils import reader_2
from utils import robot_simu
from utils.asr import VoiceRec
from utils.asr import RecThread
from utils.asr import Classifier
from utils.asr import STT
# from ui.ui_chat import Ui_MainWindow
from ui.ui_chat_v2 import Ui_MainWindow
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QFrame
import sys
from utils.action import ActionGo, ActionTurn, ActionWhat
import cozmo
# set Rules text
rules = "go forward/backward X (millimeters) \nturn left/right X (degrees)\nwhat is it"
act_dict = {"go": ActionGo, "turn": ActionTurn, "what": ActionWhat}


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
        self.voice_thread = VoiceRec(recording_time=8)
        self.voice_thread.signal_recording_done.connect(self.recordReady)
        self.voice_thread.start()

        # SECOND try
        self._speechRecWorker = None
        # self._speechRecWorker = RecThread(1)
        # self._speechRecWorker.speechReady.connect(self.recordReady)

        self.stt_thread = STT()
        self.stt_thread.signal_stt_done.connect(self.sttReady)
        self.stt_thread.start()

        # classifer thread
        self.classifier_thread = Classifier()
        self.classifier_thread.signal_classify_done.connect(self.classifyReady)
        self.classifier_thread.start()
        # make cursor focus on chat line
        self.mleChat.setFocus()

        # set image view
        self.lImg.setFrameShadow(QFrame.Sunken)
        self.lImg.setFrameShape(QFrame.StyledPanel)
        self.lImg.setMinimumSize(QSize(320, 320))

    def sendClicked(self):
        human_cmd = self.mleChat.text()
        self.mleChat.clear()
        self.human_log(human_cmd)

        # read command and maps into an information dict
        info_dict = self.rd.read(human_cmd)

        img = None  # buffer for image
        if info_dict["intent"] not in act_dict.keys():
            self.robot_log("Unknown command!")
        else:
            act = act_dict[info_dict["intent"]](info_dict)
            if info_dict["intent"] == "what":
                print("doing What intent")
                robot_rep, img = act.do_act(self.robot)
            else:
                robot_rep = act.do_act(self.robot)
            self.robot_log(robot_rep)
            if img is not None:
                self.classifier_thread.activate(img)


    def human_log(self, text):
        self.teLog.setTextColor(QtGui.QColor('blue'))
        self.teLog.insertPlainText("You: ")
        self.teLog.moveCursor(QtGui.QTextCursor.End)
        self.teLog.setTextColor(QtGui.QColor('black'))
        self.teLog.insertPlainText(text + "\n")

    def robot_log(self, text):
        # self.teLog.clear()
        self.teLog.setTextColor(QtGui.QColor('orange'))
        self.teLog.insertPlainText("Robot: ")
        self.teLog.moveCursor(QtGui.QTextCursor.End)
        self.teLog.setTextColor(QtGui.QColor('black'))
        self.teLog.insertPlainText(text + "\n")
        # self.teLog.setHtml('<html> <body> There is a an image after this word <img src="./im01.png" />.</body></html>')
        # pic = QtWidgets.QLabel(self.imgView)
        # pic.setGeometry(0, 0, 320, 240)
        # pixmap = QtGui.QPixmap("./im01.png")
        # # pixmap = pixmap.scaledToHeight(200)
        # pic.setPixmap(pixmap)
        # self.imgView.show()
        #self.imgView.
        if 'turn' in text:
            pixmap = QtGui.QPixmap("./im01.png")
        else:
            pixmap = QtGui.QPixmap("./im02.png")
        self.lImg.setPixmap(pixmap)



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

    @QtCore.pyqtSlot(str)
    def classifyReady(self, top3_str):
        print("classification done")
        top3_list = top3_str.split(sep=',')
        top3_class = []
        top3_proba = []
        for c_p in top3_list:
            if len(c_p) > 0:
                c_p_split = c_p.split(sep=':')
                top3_class.append(c_p_split[0])
                top3_proba.append(float(c_p_split[1]))
        rep = 'I think it is a(n) %s\n' % top3_class[0]
        self.teLog.insertPlainText(rep)
        self.teLog.insertPlainText('LOG: top 3 classes: %s (%f), %s (%f), %s (%f)\n' % (top3_class[0], top3_proba[0],
                                                                                        top3_class[1], top3_proba[1],
                                                                                        top3_class[2], top3_proba[2]))
        self.robot.say_text(top3_class[0])

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
    my_cozmo.camera.image_stream_enabled = True
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
