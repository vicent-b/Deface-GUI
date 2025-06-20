import sys
from queue import Queue


class streamEmitter(object): #queues are thread safe
    def __init__(self,sharedQueue):
        self.sharedQueue = sharedQueue

    def write(self,text_str,info:str=""):
        self.sharedQueue.put((text_str, info))

    def flush(var1):
        return


class streamReceiver():
    def __init__(self, sharedQueue, process_function):
        self.process_function = process_function
        self.sharedQueue = sharedQueue


    def run(self):
        while(True):
            queue_element = self.sharedQueue.get()
            self.process_function(queue_element)


"""
#Example for Qt

def ManipulateStdoutQueue(queueElement):
    global MainWindow
    s=queueElement[0]
    #MainWindow.textEdit_ConsoleOutput.append(s)
    MainWindow.textEdit_ConsoleOutput.moveCursor (QTextCursor.End)
    MainWindow.textEdit_ConsoleOutput.insertPlainText (s)
    MainWindow.textEdit_ConsoleOutput.moveCursor (QTextCursor.End)


def OverloadStdout():
    global stdout_emitter
    global stdout_receiver
    global stdout_thread

    sharedQueue = QS.Queue()
    sys.stdout = QS.streamEmitter(sharedQueue)
    sys.stderr = sys.stdout
    stdout_receiver = QS.streamReceiver(sharedQueue, ManipulateStdoutQueue)

    stdout_thread = threading.Thread(target = lambda:stdout_receiver.run(), daemon=True)
    stdout_thread.start()


"""
