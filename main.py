from PyQt5 import QtWidgets
import login
import sys


class MainApp(QtWidgets.QMainWindow, login.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainApp()
    window.show()
    Thread = login.ClientThread(window)
    Thread.start()
    app.exec_()

if __name__ == '__main__':
    main()