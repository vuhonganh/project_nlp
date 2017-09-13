from PyQt5.QtCore import pyqtSignal, QThread, QMutex, QMutexLocker, QWaitCondition
import tempfile
import subprocess
from google.cloud import speech
import keras
import tensorflow as tf
import numpy as np
from scipy.misc import imread, imresize, imsave, imshow
import socket               # Import socket module

classes_reader = ["apple", "pen", "book", "monitor", "mouse", "wallet", "keyboard",
                  "banana", "key", "mug", "pear", "orange"]


end_from_server = 'MyEnd'.encode()
end = 'MyEnd'

def recv_end(the_socket):
    total_data = []
    i = 1
    while True:
            cur_data = the_socket.recv(8192)
            #print(type(cur_data))
            if end_from_server in cur_data:
                total_data.append(cur_data[:cur_data.find(end_from_server)])
                break
            total_data.append(cur_data)
            if len(total_data) > 1:
                # check if end_of_data was split
                last_pair = total_data[-2] + total_data[-1]
                if end_from_server in last_pair:
                    total_data[-2] = last_pair[:last_pair.find(end_from_server)]
                    total_data.pop()
                    break
            print('reading until end.... %d' % i)
            i += 1
    return b''.join(total_data)


# Image Detector thread
class Detector(QThread):
    signal_detect_done = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self._mutex = QMutex()
        self._abort = False
        self._condition = QWaitCondition()
        self.cur_img = None

        # load model and default graph
        # self.classifier = keras.models.load_model('resnet_512.h5')
        # self.graph = tf.get_default_graph()  # REALLY IMPORTANT

        # setup client
        self.s = socket.socket()  # Create a socket object
        # host = socket.gethostname() # Get local machine name
        host = "graphic02.doc.ic.ac.uk"
        port = 12348  # Reserve a port for your service.
        self.serverUp = True
        try:
            self.s.connect((host, port))
            print('SERVER CONNECTED')
        except Exception as e:
            print('CANNOT CONNECT TO SERVER: ', e)
            self.serverUp = False

    def shutdown_server(self):
        if self.serverUp:
            msg = 'exit'.encode()
            print('sending exit message with end-symbole to shutdown client properly')
            self.s.sendall(msg + end.encode())

    def __del__(self):
        self._abort = True
        self.wait()

    def activate(self, img_np_arr):
        self.cur_img = img_np_arr
        try:
            print(type(self.cur_img))
            print(self.cur_img.shape)
        except:
            pass
        self._condition.wakeAll()

    def run(self):
        while True:
            if self._abort:
                return
            self._mutex.lock()
            self._condition.wait(self._mutex)
            # Doing thing
            if self.cur_img is None:
                continue

            working = False

            if self.serverUp:
                # detecting: sending to server and wait for reply
                # msg = self.cur_img.tostring()
                msg = self.cur_img.tobytes()
                print('encoded image to string message')
                print('sending message with end-symbole')
                self.s.sendall(msg + end.encode())

                try:
                    reply_from_server = recv_end(self.s)
                    res_img = np.fromstring(reply_from_server, dtype=np.uint8)
                    print(res_img.shape)
                    res_img = res_img.reshape(264, 352, 3)
                    imsave('cur_res_img.JPEG', res_img)
                    working = True
                    # imshow(res_img)
                except Exception as e:
                    print('reading error:', e)

            # emit signal
            if working:
                self.signal_detect_done.emit('succeed')
            else:
                self.signal_detect_done.emit('fail')

            # DONE DOING THING
            self._mutex.unlock()


# Image Classifier thread
class Classifier(QThread):
    signal_classify_done = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self._mutex = QMutex()
        self._abort = False
        self._condition = QWaitCondition()
        self.cur_img = None

        # load model and default graph
        self.classifier = keras.models.load_model('resnet_512.h5')
        self.graph = tf.get_default_graph()  # REALLY IMPORTANT

    def __del__(self):
        self._abort = True
        self.wait()

    def activate(self, img_np_arr):
        self.cur_img = img_np_arr
        print(type(self.cur_img))
        print(self.cur_img.shape)
        self._condition.wakeAll()

    def run(self):
        while True:
            if self._abort:
                return
            self._mutex.lock()
            self._condition.wait(self._mutex)
            # Doing thing
            if self.cur_img is None:
                continue
            # classify top3

            x = np.asarray([self.cur_img])
            res = ''
            with self.graph.as_default():
                predictions = self.classifier.predict(x, batch_size=1)[0]  # note that predictions is a 2D array
                idx_max = np.argsort(predictions)
                top3 = idx_max[-1:-4:-1]
                for idx in top3:
                    res += '%s:%.2f,' % (classes_reader[idx], predictions[idx])

            # emit signal
            self.signal_classify_done.emit(res)
            # DONE DOING THING
            self._mutex.unlock()

# Speech To Text thread
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

