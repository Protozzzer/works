from PyQt5 import QtCore
from PyQt5.QtWidgets import (QPushButton, QVBoxLayout, QSplitter, QTextEdit, QApplication, QDialog)
from PyQt5.QtGui import QTextCursor
import sys
import socket
import time
import MySQLdb
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


class ClientThread(Thread):
    def __init__(self, window):
        Thread.__init__(self)
        self.window = window

    def run(self):
        f = open('data.txt', 'r')
        Settings_host.name = str(f.read())
        f.close()

        db = MySQLdb.connect("localhost", "root", "protozerg", "datachat")
        db.autocommit(True)
        cursor = db.cursor()
        cursor.execute("Select M.text, M.date, U.name from `Messages` M INNER JOIN `Users` U ON U.id = M.User_id;")
        row = cursor.fetchall()
        for rall in row:
            window.chat.append("\n[" + rall[2] + "]  " + "[" + str(rall[1]) + "]  "  + rall[0])
        while True:
            ready = select.select([Settings_host.sock], [], [], 1)
            if ready[0]:
                data, adr = Settings_host.sock.recvfrom(1024)
                times = time.strftime("%H.-%M.-%S", time.localtime())
                window.chat.append("\n[" + times + "]" + data.decode("utf-8"))
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
            if message!= "":
                Settings_host.sock.sendto(("[" +Settings_host.name+ "] :: "+message+ " ").encode("utf-8"), Settings_host.server)

                db = MySQLdb.connect("localhost", "root", "protozerg", "datachat")
                db.autocommit(True)
                cursor = db.cursor()
                cursor.execute("Select `id`, `name` from `Users` Where `name` = %s", [Settings_host.name])
                row = cursor.fetchone()
                values = (message, int(row[0]))
                cursor.execute("INSERT INTO Messages(text, User_id, date) VALUES (%s, %s, NOW());", values)
                db.close()
                time.sleep(0.3)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    serThread = ClientThread(window)
    serThread.start()
    if Settings_host.join == False:
        f = open('data.txt', 'r')
        name = str(f.read())
        f.close()
        Settings_host.sock.sendto(("[" + name + "] is connected to the chat").encode("utf-8"), Settings_host.server)
        Settings_host.join = True
    window.exec()
    sys.exit(app.exec_())
    serThread.join()
    sock.close()

