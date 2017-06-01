from PyQt5.QtCore import pyqtSignal, QThread, QMutex, QMutexLocker, QWaitCondition
import tempfile
import subprocess
from google.cloud import speech

class STT(QThread):
    signal_stt_done = pyqtSignal(list)

    def __init__(self, max_alternatives=1):
        super().__init__()
        self.max_alter = max_alternatives
        self._mutex = QMutex()
        self._abort = False
        self._condition = QWaitCondition()
        self.client = speech.Client()
        self.file_path = None

    def __del__(self):
        self._abort = True
        self.wait()

    def activate(self, audio_file_path):
        self.file_path = audio_file_path
        self._condition.wakeOne()

    def run(self):
        while True:
            if self._abort:
                return
            self._mutex.lock()
            self._condition.wait(self._mutex)
            ### DOING THING
            trans = []
            with open(self.file_path, 'rb') as audio_file:
                sample = self.client.sample(content=audio_file.read(),
                                            sample_rate=16000,
                                            encoding=speech.Encoding.FLAC)
                try:
                    alternatives = sample.sync_recognize(language_code='en-US',
                                                         max_alternatives=self.max_alter
                                                         )
                    for a in alternatives:
                        trans.append(a.transcript)
                except ValueError as e:
                    print("error: ", e)

            self.signal_stt_done.emit(trans)
            ### DONE DOING THING
            self._mutex.unlock()



class VoiceRec(QThread):
    signal_recording_done = pyqtSignal(str)

    def __init__(self, recording_time=5):
        super().__init__()
        self._rec_time = recording_time
        # self._is_active = False
        self._mutex = QMutex()
        self._abort = False
        self._condition = QWaitCondition()

    def __del__(self):
        self._abort = True
        self.wait()

    def activate(self):
        # self._mutex.lock()
        # self._is_active = True
        # self._mutex.unlock()
        # self._is_active = True
        self._condition.wakeOne()

    # def deactivate(self):
    #     self._mutex.lock()
    #     self._is_active = False
    #     self._mutex.unlock()

    def run(self):
        while True:
            if self._abort:
                return
            # activating = self._is_active
            # if activating:
            #     with tempfile.NamedTemporaryFile(suffix=".flac", delete=False) as f:
            #         flacFilename = f.name
            #     cmd = 'rec --channels=1 --bits=16 --rate=16000 {} trim 0 {:d}'.format(flacFilename, self._rec_time)
            #     print("recording...")
            #     p = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
            #     # wait for subprocess to finished
            #     p.communicate()
            #     print("finished recording")
            #
            #     self._mutex.lock()
            #     self._is_active = False
            #     self._mutex.unlock()
            #
            #     self.signal_recording_done.emit(flacFilename)
            # else:
            #     self._mutex.lock()
            #     self._condition.wait(self._mutex)
            #     self._mutex.unlock()

            self._mutex.lock()
            self._condition.wait(self._mutex)
            # DOING STUFF
            with tempfile.NamedTemporaryFile(suffix=".flac", delete=False) as f:
                flacFilename = f.name
            cmd = 'rec --channels=1 --bits=16 --rate=16000 {} trim 0 {:d}'.format(flacFilename, self._rec_time)
            print("recording...")
            p = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
            # wait for subprocess to finished
            p.communicate()
            print("finished recording")
            self.signal_recording_done.emit(flacFilename)

            self._mutex.unlock()



class BackgroundThread(QThread):
    def __init__(self, parent=None):
        super(BackgroundThread, self).__init__(parent)

        self._mutex = QMutex()
        self._condition = QWaitCondition()

        self._activating = False
        self._input = None
        # when program is closed
        self._abort = False

    def __del__(self):
        self._mutex.lock()
        self._abort = True
        self._condition.wakeOne()
        self._mutex.unlock()

        # wait for gracefully stop
        self.wait()

    def _taskStart(self, taskInput):
        '''
        this function should not be called from outside
        :return: 
        '''
        # this must re-implemented in derived class
        pass


    def _taskEnd(self, taskOutput):
        '''
        this function should not be called from outside
        :return: 
        '''
        # this must re-implemented in derived class
        pass

    def activate(self, input = None):
        locker = QMutexLocker(self._mutex)
        if not self._activating:
            self._activating = True
            self._input = input
            # if not running than we start the thread, otherwise we wake it up
            if not self.isRunning():
                self.start()
            else:
                self._condition.wakeOne()

    def run(self):
        while True:
            if self._abort:
                return

            self._mutex.lock()
            activating = self._activating
            input = self._input
            self._mutex.unlock()

            if activating:
                # start long running task
                taskOutput = self._taskStart(input)

                # task comleted => report result
                self._taskEnd(taskOutput)

                # switch off self._activating
                self._mutex.lock()
                self._activating = False
                self._mutex.unlock()
            else:
                self._mutex.lock()
                self._condition.wait(self._mutex)
                self._mutex.unlock()


class RecThread(BackgroundThread):
    speechReady = pyqtSignal(str)

    def __init__(self, parent=None, num_secs=5):
        super(RecThread, self).__init__(parent)

        self._num_secs = num_secs

    @property
    def encoding(self):
        return 'FLAC'

    def record(self):
        self.activate()

    def _taskStart(self, input):
        with tempfile.NamedTemporaryFile(suffix=".flac", delete=False) as f:
            flacFilename = f.name
        cmd = 'rec --channels=1 --bits=16 --rate=16000 {} trim 0 {:d}'.format(flacFilename, self._num_secs)
        print("recording...")
        p = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
        # wait for subprocess to finished
        p.communicate()
        print("finished recording")
        return flacFilename

    def _taskEnd(self, flacFilename):
        self.speechReady.emit(flacFilename)

