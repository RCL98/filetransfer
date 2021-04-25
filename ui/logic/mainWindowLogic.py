
from PyQt5 import QtWidgets

from PyQt5.QtWidgets import QMainWindow

from ui.logic.DownloadsWidget import DownloadsWidget
from ui.mainWindowDesign import Ui_MainWindow
from ui.logic.BrowseWidget import BrowseWidget

import icons.icons


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, window):
        super(MainWindow, self).__init__(window)
        self.window = window
        self.setupUi(window)
        self.browseWidget = BrowseWidget(self.browseTab)
        self.downloadsTab = DownloadsWidget(self.downloadsTab)
        # self.showMaximized()
        # self.foldIcon = QtGui.QIcon()
        # self.fileIcon = QtGui.QIcon()
        # self.fileTreeModel = None
        # self.fileSystem = FileSystem()

        # self.setLogicAndAdjustments()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    ui = MainWindow(mainWindow)
    mainWindow.showMaximized()
    sys.exit(app.exec_())