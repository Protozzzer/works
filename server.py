# -*- coding: cp1251 -*
import socket
import time
import sys
from PyQt5 import QtWidgets
from threading import Thread
from PyQt5 import QtCore
from PyQt5.QtWidgets import (QVBoxLayout, QSplitter, QTextEdit, QWidget)
from PyQt5.QtGui import QTextCursor
import MySQLdb


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

        db = MySQLdb.connect("localhost", "root", "protozerg", "datachat1", charset='cp1251')
        db.autocommit(True)
        cursor = db.cursor()

        window.chat.append("Server started")
        while True:
            data, adr = Settings_server.sock.recvfrom(1024)
            if adr not in Settings_server.clients:
                Settings_server.clients.append(adr)
            times = time.strftime("%Y-%m-%d-%H.-%M.-%S", time.localtime())
            window.chat.append("[" + adr[0] + "]=[" + str(adr[1]) + "]=[" + times + "]\n")
            for client in Settings_server.clients:
                if adr != client:
                    Settings_server.sock.sendto(data, client)
            window.chat.append(data.decode("cp1251") + "\n")

            data_dec = str(data.decode("cp1251"))
            if data_dec[0] == "A":
                data1 = data_dec[1:]
                res = [element for element in data1.split(",")]
                cursor.execute("Select 'name', `password` from `Users` Where `name` = %s and `password` = %s;", res)
                rows = cursor.fetchone()
                if rows is None:
                    data_to_client = "A" + "False"
                    Settings_server.sock.sendto(data_to_client.encode("cp1251"), client)
                else:
                    data_to_client = "A" + "True"
                    Settings_server.sock.sendto(data_to_client.encode("cp1251"), client)
            elif data_dec[0] == "R":
                data1 = data_dec[1:]
                res = [element for element in data1.split(",")]
                cursor.execute("Select 'name' from `Users` Where `name` = %s;", [res[0]])
                rows = cursor.fetchone()
                if rows is None:
                    cursor.execute("INSERT Users(name, password) VALUES (%s, %s);", res)
                    data_to_client = "R" + "True"
                    Settings_server.sock.sendto(data_to_client.encode("cp1251"), client)
                elif rows is not None:
                    data_to_client = "R" + "False"
                    Settings_server.sock.sendto(data_to_client.encode("cp1251"), client)
            elif data_dec[0] == "M":
                data1 = data_dec[1:]
                res = [element for element in data1.split(",")]
                cursor.execute("Select `id`, `name` from `Users` Where `name` = %s", [res[0]])
                row = cursor.fetchone()
                values = []
                values.append(res[1])
                values.append(int(row[0]))
                cursor.execute("INSERT INTO Messages(text, User_id, date) VALUES (%s, %s, NOW());", values)
            elif data_dec[0] == "P":
                cursor.execute(
                    "Select M.text, M.date, U.name from `Messages` M INNER JOIN `Users` U ON U.id = M.User_id ORDER BY M.date;")
                row = cursor.fetchall()
                l = []
                for rall in row:
                    new = []
                    new.append(rall[2])
                    new.append(str(rall[1]))
                    new.append(rall[0])
                    l.append(new)
                for d in l:
                    Settings_server.sock.sendto(("P" + str(d)).encode("cp1251"), client)
        db.close()



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
