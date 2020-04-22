# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QMessageBox, QLineEdit, QPushButton, QVBoxLayout, QSplitter, QTextEdit, QDialog)
import hashlib
from PyQt5 import QtCore
from PyQt5.QtGui import QTextCursor
import sys
import socket
from threading import Thread
import select
import time
import threading


class Settings_host:
    port = 0
    host = socket.gethostbyname(socket.gethostname())
    server = (host, 6046)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, port))
    sock.setblocking(0)
    join = False
    data_From_Server_chat = ""
    name = ''
    password = ''
    state1 = False
    state2 = True
    num = 0
    data_From_Server_check = ""
    flag_thread = False
    lock = threading.Lock()

class ClientThread(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        while True:
            if Settings_host.flag_thread == False: # после включения второго потока ( по открытию формы чата) меняется флаг,
                                                   # этот учаток кода более не работает, так как больше не нужен.
                                                   # Можно было бы отключить поток и вовсе, однако это небезопасно,
                                                   # следовательно поток дожидается своего завершения через join
                ready = select.select([Settings_host.sock], [], [], 1)
                if ready[0]:
                    try:
                        Settings_host.lock.acquire()
                        data, adr = Settings_host.sock.recvfrom(1024)
                        Settings_host.data_From_Server_check = str(data.decode("cp1251"))
                        Settings_host.lock.release()
                    except BlockingIOError:
                        print("error1") #при увеличение смс более 30-35 в базе данных(история переписок) возникает ошибка и баги, как закрытие формы



class ChatThread(Thread):
    def __init__(self, window):
        Thread.__init__(self)
        self.window = window
        self.temp_counter = 1

    def run(self):

        Settings_host.sock.sendto(("P").encode("cp1251"),
                                  Settings_host.server)
        while True:
            ready = select.select([Settings_host.sock], [], [], 1)
            if ready[0]:
                try:
                    data, adr = Settings_host.sock.recvfrom(1024)
                    if (data):
                        data1 = data.decode("cp1251")
                        if (data1[0] == "P"):
                            Settings_host.data_From_Server_chat = data1[1:]
                            res = [element.strip(" ['[ ']'] \\n") for element in Settings_host.data_From_Server_chat.split(", ")]
                            d = list(res)
                            for f in d:
                                if self.temp_counter == 3:
                                   self.window.chat.append(f + "\n")
                                   self.temp_counter = 0
                                else:
                                  self.window.chat.append(f)
                                self.temp_counter = self.temp_counter +1
                        elif (data1[0] != "P" and data1[0] != "A" and data1[0] != "R" and data1[0] != "M"):
                            times = time.strftime("%H.-%M.-%S", time.localtime())
                            self.window.chat.append("\n[" + times + "]" + data.decode("cp1251"))
                except BlockingIOError:
                    print("error2") #при увеличение смс более 30-35 в базе данных(история переписок) возникает ошибка и баги, как закрытие формы


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(371, 500)
        MainWindow.setMaximumSize(371, 500)
        MainWindow.setMinimumSize(371, 500)
        MainWindow.setStyleSheet("\n""background-color: rgb(167, 198, 255);")

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(196, 150, 121, 31))
        self.textEdit.setStyleSheet("background-color: rgb(251, 255, 255);\n"
                                    "font: 75 italic 13pt \"MS Shell Dlg 2\";")
        self.textEdit.setObjectName("textEdit")

        self.QLineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.QLineEdit_2.setGeometry(QtCore.QRect(196, 210, 121, 31))
        self.QLineEdit_2.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                      "font: 75 italic 13pt \"MS Shell Dlg 2\";")
        self.QLineEdit_2.setObjectName("textEdit_2")
        self.QLineEdit_2.setEchoMode(QLineEdit.Password)

        self.textEdit.setTabChangesFocus(True) # FOR TAB-BUTTON
        self.QLineEdit_2.setTabOrder(self.textEdit, self.QLineEdit_2)

        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(36, 150, 131, 31))
        self.label_7.setStyleSheet("background-color: rgb(221, 221, 255);\n"
                                   "font: 75 italic 14pt \"MS Shell Dlg 2\";")
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")

        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(36, 210, 131, 31))
        self.label_8.setStyleSheet("background-color: rgb(221, 221, 255);\n"
                                   "font: 75 italic 14pt \"MS Shell Dlg 2\";")
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label_8")

        self.label_13 = QtWidgets.QLabel(self.centralwidget)
        self.label_13.setGeometry(QtCore.QRect(30, 60, 300, 40))
        self.label_13.setStyleSheet("background-color: rgb(226, 255, 207);\n"
                                    "font: 75 italic 16pt \"MS Shell Dlg 2\";")
        self.label_13.setAlignment(QtCore.Qt.AlignCenter)
        self.label_13.setObjectName("label_13")

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(100, 270, 151, 51))
        self.pushButton.setStyleSheet("background-color: rgb(104, 140, 140);\n"
                                      "font: 75 italic 16pt \"MS Shell Dlg 2\";\n"
                                      "color: rgb(255, 255, 255);")

        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(80, 370, 200, 51))
        self.pushButton_2.setStyleSheet("background-color: rgb(104, 140, 140, 0.05);\n"
                                        "font: 75 italic 16pt \"MS Shell Dlg 2\";\n"
                                        "color: rgb(0, 0, 0);")
        self.pushButton_2.setObjectName("pushButton2")

        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(80, 370, 200, 51))
        self.pushButton_3.setStyleSheet("background-color: rgb(104, 140, 140);\n"
                                        "font: 75 italic 16pt \"MS Shell Dlg 2\";\n"
                                        "color: rgb(255, 255, 255);")
        self.pushButton_3.setObjectName("pushButton3")
        self.pushButton_3.hide()

        MainWindow.setCentralWidget(self.centralwidget)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.pushButton.clicked.connect(self.openewin);
        self.pushButton_2.clicked.connect(self.openewin2);
        self.pushButton_3.clicked.connect(self.back);

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def openewin(self):
        if (Settings_host.state1 == False):#переменная для смены местоположения кнопок
            Settings_host.name = self.textEdit.toPlainText()
            Settings_host.password = self.QLineEdit_2.text()
            h = hashlib.md5(Settings_host.password.encode('cp1251')).hexdigest()
            values = (Settings_host.name, h)

            if(Settings_host.name == '' or Settings_host.password == ''):
                QMessageBox.about(self, "Предупреждение", "Заполните пожалуйста поля")
                flag_for_check = 0#переменная для смены местоположения кнопок
            else:
                flag_for_check = 1

            if (flag_for_check == 1):
                str1 = str(values[0]) + "," + str(values[1])
                Settings_host.sock.sendto(("A" + str1).encode("cp1251"),
                                          Settings_host.server)
                while True:
                    if Settings_host.lock.locked() == True: # ожидание момента захвата потоком thread1
                        break
                Settings_host.lock.acquire()
                #time.sleep(1)
                if Settings_host.data_From_Server_check[0] == "A":
                    res = Settings_host.data_From_Server_check[1:]
                Settings_host.lock.release()
                if res == 'False':
                    QMessageBox.about(self, "Предупреждение", "Проверьте правильность введенных данных. Если вас нет в системе - зарегистрируйтесь.")
                elif res == 'True':
                    self.hide()
                    Settings_host.flag_thread = True
                    window = Window()
                    chat = ChatThread(window)
                    chat.start()
                    if Settings_host.join == False:
                        Settings_host.sock.sendto(("[" + Settings_host.name + "] is connected to the chat").encode("cp1251"),
                                                  Settings_host.server)
                        Settings_host.join = True
                    window.exec()
                    chat.join()


    def openewin2(self):
        Settings_host.num += 1 #переменная для смены местоположения кнопок
        if(Settings_host.state2 == True or Settings_host.num == 1):
            self.pushButton.setGeometry(QtCore.QRect(80, 370, 200, 51))
            self.pushButton.setStyleSheet("background-color: rgb(104, 140, 140, 0.05);\n"
                                          "font: 75 italic 16pt \"MS Shell Dlg 2\";\n"
                                          "color: rgb(0, 0, 0);")
            self.pushButton_2.setGeometry(QtCore.QRect(70, 270, 220, 51))
            self.pushButton_2.setStyleSheet("background-color: rgb(104, 140, 140);\n"
                                            "font: 75 italic 16pt \"MS Shell Dlg 2\";\n"
                                            "color: rgb(255, 255, 255);")
            self.pushButton.hide()
            Settings_host.state2 == False#переменная для смены местоположения кнопок
            self.pushButton_3.show()



        if(Settings_host.state2 == False or Settings_host.num >= 2):
            Settings_host.name = self.textEdit.toPlainText() # данные с формы
            Settings_host.password = self.QLineEdit_2.text()
            h = hashlib.md5(Settings_host.password.encode('cp1251')).hexdigest()
            values = (Settings_host.name, h)
            if (Settings_host.name == '' or Settings_host.password == ''):
                QMessageBox.about(self, "Предупреждение", "Заполните пожалуйста поля")
                flag_for_check = 0#переменная для смены местоположения кнопок
            else:
                flag_for_check = 1

            if (flag_for_check == 1):
                str1 = str(values[0]) + "," + str(values[1])
                Settings_host.sock.sendto(("R" + str1).encode("cp1251"),
                                          Settings_host.server)
                while True:
                    if Settings_host.lock.locked() == True:  # ожидание момента захвата потоком thread1
                        break
                Settings_host.lock.acquire()
                #time.sleep(2)
                if Settings_host.data_From_Server_check[0] == "R":
                    res = Settings_host.data_From_Server_check[1:]
                Settings_host.lock.release()
                if res == "True":
                    self.hide()
                    Settings_host.flag_thread = True
                    window = Window()
                    chat = ChatThread(window)
                    chat.start()
                    if Settings_host.join == False:
                        Settings_host.sock.sendto(("[" + Settings_host.name + "] is connected to the chat").encode("cp1251"),
                                                  Settings_host.server)
                        Settings_host.join = True
                    window.exec()
                    chat.join()
                elif res == "False":
                    QMessageBox.about(self, "Предупреждение",
                                      "Такое имя уже существует в системе. Если вы уже зарегистрированы, авторизуйтесь.")

    def back(self):
        self.pushButton_3.hide()
        self.pushButton.setGeometry(QtCore.QRect(100, 270, 151, 51))
        self.pushButton.setStyleSheet("background-color: rgb(104, 140, 140);\n"
                                      "font: 75 italic 16pt \"MS Shell Dlg 2\";\n"
                                      "color: rgb(255, 255, 255);")
        self.pushButton_2.setGeometry(QtCore.QRect(80, 370, 200, 51))
        self.pushButton_2.setStyleSheet("background-color: rgb(104, 140, 140, 0.05);\n"
                                        "font: 75 italic 16pt \"MS Shell Dlg 2\";\n"
                                        "color: rgb(0, 0, 0);")
        self.pushButton.show()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Авторизация"))
        self.label_7.setText(_translate("MainWindow", "Логин"))
        self.label_8.setText(_translate("MainWindow", "Пароль"))
        self.label_13.setText(_translate("MainWindow", "Выполните вход/авторизацию"))
        self.pushButton.setText(_translate("MainWindow", "Войти"))
        self.pushButton_2.setText(_translate("MainWindow", "Зарегистрироваться"))
        self.pushButton_3.setText(_translate("MainWindow", "Назад"))


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

class MainApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainApp()
    window.show()
    Thread = ClientThread()
    Thread.start()
    app.exec_()
    Thread.join()
    Settings_host.sock.close()

if __name__ == '__main__':
    main()