import socket
import time
import sys
from PyQt5 import QtWidgets
from threading import Thread
from PyQt5 import QtCore
from PyQt5.QtWidgets import (QVBoxLayout, QSplitter, QTextEdit, QWidget)
from PyQt5.QtGui import QTextCursor
#import mysqlclient


class Settings_server:
    host = socket.gethostbyname(socket.gethostname())
    port = 6046
    clients = []
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("",port))


class ServerThread(Thread):
    def __init__(self, window):
        Thread.__init__(self)
        self.window = window

    def run(self):

        window.chat.append("Server started")
        while True:
            data, adr = Settings_server.sock.recvfrom(1024)
            if adr not in Settings_server.clients:
                Settings_server.clients.append(adr)
            times = time.strftime("%Y-%m-%d-%H.-%M.-%S", time.localtime())
            window.chat.append("[" + adr[0] + "]=[" + str(adr[1]) + "]=[" + times + "]")
            for client in Settings_server.clients:
                if adr != client:
                    Settings_server.sock.sendto(data, client)
            window.chat.append(data.decode("utf-8"))

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setObjectName("Server")
        self.resize(371, 500)
        self.setMaximumSize(300, 700)
        self.setMinimumSize(400, 700)
        self.setStyleSheet("\n""background-color: rgb(167, 198, 255);")
        self.chat = QTextEdit()
        self.chat.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                "font: 75 italic 15pt \"MS Shell Dlg 2\";")
        self.chat.moveCursor(QTextCursor.End, QTextCursor.MoveAnchor)
        self.chat.setReadOnly(True)

        self.chatBody = QVBoxLayout(self)
        splitter = QSplitter(QtCore.Qt.Vertical)
        splitter.addWidget(self.chat)
        splitter.setSizes([400, 100])

        splitter2 = QSplitter(QtCore.Qt.Vertical)
        splitter2.addWidget(splitter)
        splitter2.setSizes([200, 10])
        self.chatBody.addWidget(splitter2)

        self.setWindowTitle("Chat Application")
        self.resize(500, 500)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    ServerThread = ServerThread(window)
    ServerThread.start()
    window.show()
    window.hide()
    app.exec_()
    ServerThread.join()
    Settings_server.sock.close()
