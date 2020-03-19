# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import (QMessageBox)
import MySQLdb
import hashlib
from os import system as sh

class Settings:
    num1 = ''
    num2 = ''
    state1 = False
    state2 = True
    num = 0


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

        self.textEdit_2 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_2.setGeometry(QtCore.QRect(196, 210, 121, 31))
        self.textEdit_2.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                      "font: 75 italic 13pt \"MS Shell Dlg 2\";")
        self.textEdit_2.setObjectName("textEdit_2")

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

            db = MySQLdb.connect("localhost", "root", "protozerg", "datachat")
            db.autocommit(True)
            cursor = db.cursor()
            Settings.num1 = self.textEdit.toPlainText()
            Settings.num2 = self.textEdit_2.toPlainText()
            h =  hashlib.md5(Settings.num2.encode('utf-8')).hexdigest()
            values = (Settings.num1, h)

            if(Settings.num1 == '' or Settings.num2 == ''):
                QMessageBox.about(self, "Предупреждение", "Заполните пожалуйста поля")
                flag = 0
            else:
                flag = 1

            if (flag == 1):
                cursor.execute("Select 'name', `password` from `Users` Where `name` = %s and `password` = %s;", values)
                rows = cursor.fetchone()
                if rows is None :
                    QMessageBox.about(self, "Предупреждение", "Проверьте правильность введенных данных. Если вас нет в системе - зарегистрируйтесь.")
                    flag = 0
                elif rows is not None:
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
            db = MySQLdb.connect("localhost", "root", "protozerg", "datachat")
            db.autocommit(True)
            cursor = db.cursor()

            Settings.num1 = self.textEdit.toPlainText()
            Settings.num2 = self.textEdit_2.toPlainText()
            h = hashlib.md5(Settings.num2.encode('utf-8')).hexdigest()
            values = (Settings.num1, h)
            if (Settings.num1 == '' or Settings.num2 == ''):
                QMessageBox.about(self, "Предупреждение", "Заполните пожалуйста поля")
                flag = 0
            else:
                flag = 1

            if (flag == 1):
                cursor.execute("Select 'name' from `Users` Where `name` = %s;", [Settings.num1])
                rows = cursor.fetchone()
                if rows is None:
                    cursor.execute("INSERT Users(name, password) VALUES (%s, %s);", values)
                    self.close()
                    f = open('data.txt', 'w')
                    f.write(Settings.num1)
                    f.close()
                    sh("python chatForm.py")
                elif rows is not None:
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
