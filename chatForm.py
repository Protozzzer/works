# -*- coding: cp1251 -*
from PyQt5 import QtCore
from PyQt5.QtWidgets import (QPushButton, QVBoxLayout, QSplitter, QTextEdit, QApplication, QDialog)
from PyQt5.QtGui import QTextCursor
import sys
import socket
from threading import Thread
import select
import time



class Settings_host:
  port = 0
  host = socket.gethostbyname(socket.gethostname())
  server = (host, 6046)
  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  sock.bind((host, port))
  sock.setblocking(0)
  f = False
  join = False
  data = 0
  name = ''
  data_From_Server = ""



class ClientThread(Thread):
    def __init__(self, window):
        Thread.__init__(self)
        self.window = window

    def run(self):
        f = open('data.txt', 'r')
        Settings_host.name = str(f.read())
        f.close()

        Settings_host.sock.sendto(("P").encode("cp1251"),
                                  Settings_host.server)
        while True:
            ready = select.select([Settings_host.sock], [], [], 1)
            if ready[0]:
                data, adr = Settings_host.sock.recvfrom(1024)
                if (data):
                    data1 = data.decode("cp1251")
                    time.sleep(0.05)
                    if (data1[0] == "P"):
                        Settings_host.data_From_Server = data1[1:]
                        res = [element.strip(" ['[ ']'] \\n") for element in Settings_host.data_From_Server.split(", ")]
                        d = list(res)
                        for f in d:
                            window.chat.append(f)
                        window.chat.append("\n")
                    elif (data1[0] != "P" and data1[0] != "A" and data1[0] != "R" and data1[0] != "M"):
                        times = time.strftime("%H.-%M.-%S", time.localtime())
                        window.chat.append("\n[" + times + "]" + data.decode("cp1251"))
                if not data:
                    break

class Window(QDialog):
    def __init__(self):
        super().__init__()
        self.setObjectName("Chat")
        self.resize(371, 500)
        self.setMaximumSize(300, 700)
        self.setMinimumSize(400, 700)
        self.setStyleSheet("\n""background-color: rgb(167, 198, 255);")

        self.chatTextField = QTextEdit(self)
        self.chatTextField.resize(480, 100)
        self.chatTextField.move(10, 350)
        self.chatTextField.setStyleSheet("background-color: rgb(255, 255, 255, 0.4);\n"
                                         "font: 75 italic 15pt \"MS Shell Dlg 2\";")

        self.btnSend = QPushButton("Send", self)
        self.btnSend.resize(480, 30)
        self.btnSend.setStyleSheet("background-color: rgb(104, 140, 140);\n"
                                   "font: 75 italic 20pt \"MS Shell Dlg 2\";\n"
                                   "color: rgb(0, 0, 0);")
        self.btnSend.move(10, 460)
        self.btnSend.clicked.connect(self.send)

        self.chatBody = QVBoxLayout(self)
        splitter = QSplitter(QtCore.Qt.Vertical)

        self.chat = QTextEdit()
        self.chat.setStyleSheet("background-color: rgb(255, 255, 255);\n")
        self.chat.moveCursor(QTextCursor.End, QTextCursor.MoveAnchor)
        self.chat.setReadOnly(True)

        splitter.addWidget(self.chat)
        splitter.addWidget(self.chatTextField)
        splitter.setSizes([400, 100])

        splitter2 = QSplitter(QtCore.Qt.Vertical)
        splitter2.addWidget(splitter)
        splitter2.addWidget(self.btnSend)
        splitter2.setSizes([200, 10])

        self.chatBody.addWidget(splitter2)
        self.setWindowTitle("Chat Application")
        self.resize(500, 500)

    def send(self):
        text = self.chatTextField.toPlainText()
        font = self.chat.font()
        font.setPointSize(15)
        self.chat.setFont(font)
        textFormatted = '{:>80}'.format(text)
        self.chat.append(textFormatted)

        if Settings_host.join == True:
            message = text
            self.chatTextField.clear()
            if message!= "":
                Settings_host.sock.sendto(("[" +Settings_host.name+ "] :: "+message+ " ").encode("cp1251"), Settings_host.server)

                str1 = "M" + str(Settings_host.name) + "," + str(message)
                Settings_host.sock.sendto(str1.encode("cp1251"),
                                          Settings_host.server)
                time.sleep(0.5)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    serThread = ClientThread(window)
    serThread.start()
    if Settings_host.join == False:
        f = open('data.txt', 'r')
        name = str(f.read())
        f.close()
        Settings_host.sock.sendto(("[" + name + "] is connected to the chat").encode("cp1251"), Settings_host.server)
        Settings_host.join = True
    window.exec()
    sys.exit(app.exec_())
    serThread.join()
    sock.close()

