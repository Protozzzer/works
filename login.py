# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import (QMessageBox, QLineEdit)
import hashlib
from os import system as sh
import socket
from threading import Thread
import select
import time

class Settings:
    num1 = ''
    num2 = ''
    state1 = False
    state2 = True
    num = 0
    data_From_Server = ""

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
        while True:
            ready = select.select([Settings_host.sock], [], [], 1)
            if ready[0]:
                data, adr = Settings_host.sock.recvfrom(1024)
                Settings.data_From_Server = str(data.decode("cp1251"))
                if not data:
                    break

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
        if (Settings.state1 == False):
            flag = 0
            Settings.num1 = self.textEdit.toPlainText()
            Settings.num2 = self.QLineEdit_2.text()
            h = hashlib.md5(Settings.num2.encode('cp1251')).hexdigest()
            values = (Settings.num1, h)

            if(Settings.num1 == '' or Settings.num2 == ''):
                QMessageBox.about(self, "Предупреждение", "Заполните пожалуйста поля")
                flag = 0
            else:
                flag = 1

            if (flag == 1):
                str1 = str(values[0]) + "," + str(values[1])
                Settings_host.sock.sendto(("A" + str1).encode("cp1251"),
                                          Settings_host.server)
                time.sleep(1)
                if Settings.data_From_Server[0] == "A":
                    res = Settings.data_From_Server[1:]
                if res == 'False':
                    QMessageBox.about(self, "Предупреждение", "Проверьте правильность введенных данных. Если вас нет в системе - зарегистрируйтесь.")
                    flag = 0
                elif res == 'True':
                    f = open('data.txt', 'w')
                    f.write(Settings.num1)
                    f.close()
                    self.close()
                    sh("python chatForm.py")


    def openewin2(self):
        Settings.num += 1
        if(Settings.state2 == True or Settings.num == 1):
            self.pushButton.setGeometry(QtCore.QRect(80, 370, 200, 51))
            self.pushButton.setStyleSheet("background-color: rgb(104, 140, 140, 0.05);\n"
                                          "font: 75 italic 16pt \"MS Shell Dlg 2\";\n"
                                          "color: rgb(0, 0, 0);")
            self.pushButton_2.setGeometry(QtCore.QRect(70, 270, 220, 51))
            self.pushButton_2.setStyleSheet("background-color: rgb(104, 140, 140);\n"
                                            "font: 75 italic 16pt \"MS Shell Dlg 2\";\n"
                                            "color: rgb(255, 255, 255);")
            self.pushButton.hide()
            Settings.state2 == False
            self.pushButton_3.show()



        if(Settings.state2 == False or Settings.num >= 2):
            flag = 0
            Settings.num1 = self.textEdit.toPlainText()
            Settings.num2 = self.QLineEdit_2.text()
            h = hashlib.md5(Settings.num2.encode('cp1251')).hexdigest()
            values = (Settings.num1, h)
            if (Settings.num1 == '' or Settings.num2 == ''):
                QMessageBox.about(self, "Предупреждение", "Заполните пожалуйста поля")
                flag = 0
            else:
                flag = 1

            if (flag == 1):
                str1 = str(values[0]) + "," + str(values[1])
                Settings_host.sock.sendto(("R" + str1).encode("cp1251"),
                                          Settings_host.server)
                time.sleep(2)
                if Settings.data_From_Server[0] == "R":
                    res = Settings.data_From_Server[1:]
                if res == "True":
                    self.close()
                    f = open('data.txt', 'w')
                    f.write(Settings.num1)
                    f.close()
                    sh("python chatForm.py")
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
