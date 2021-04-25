import sys

from PyQt5 import QtWidgets

from ui.logic.startWindowLogic import StartWindow
from ui.logic.mainWindowLogic import MainWindow


class AppInterface:
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.window = QtWidgets.QMainWindow()
        self.accepted = False
        self.startWindow = None
        self.mainWindow = None

    def accept(self, t: bool):
        self.accepted = t

    def startApp(self):
        self.startWindow = StartWindow(self.window)
        self.startWindow.acceptState.connect(self.accept)
        self.window.showMaximized()
        resp = self.app.exec_()
        if resp == 0:
            if self.accepted:
                del self.startWindow
                self.mainApp()
        else:
            raise Exception(f"Something bad happened to the starting window! {resp}")

    def mainApp(self):
        self.window = QtWidgets.QMainWindow()
        self.mainWindow = MainWindow(self.window)
        self.window.showMaximized()
        resp = self.app.exec_()


if __name__ == '__main__':
    app = AppInterface()
    app.startApp()
