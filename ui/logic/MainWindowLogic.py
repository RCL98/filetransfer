
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow

from eventTypes import UserTreeFileDispatchedEvent
from ui.logic.BrowseWidgetLogic import BrowseWidget
from ui.design.mainWindowDesign import Ui_MainWindow
from ui.logic.DownloadsWidget import DownloadsWidget


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, window):
        super(MainWindow, self).__init__(window)
        self.window = window
        self.setupUi(window)
        self.browseWidget = BrowseWidget(self.browseTab)
        self.downloadsTab = DownloadsWidget(self.downloadsTab)

    def customEvent(self, event):
        print("Main customEvent: ", event.type())
        try:
            if event.type() == UserTreeFileDispatchedEvent.idType:
                eventData = event.getData()
                print(f"Received : {eventData}")
                if eventData != UserTreeFileDispatchedEvent.idType:
                    self.browseWidget.renderTree(eventData)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    ui = MainWindow(mainWindow)
    mainWindow.showMaximized()
    sys.exit(app.exec_())