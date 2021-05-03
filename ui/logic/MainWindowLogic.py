
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow

from eventTypes import UserTreeFileDispatchedEvent, UsersListDispatchedEvent
from ui.logic.BrowseWidgetLogic import BrowseWidget
from ui.design.mainWindowDesign import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, window):
        super(MainWindow, self).__init__(window)
        self.window = window
        self.setupUi(window)
        self.browseWidget = BrowseWidget(self.browseTab)
        # self.downloadsTab = DownloadsWidget(self.downloadsTab)

    def customEvent(self, event):
        print("Main customEvent: ", event.type())
        try:
            eventData = event.getData()
            print(f"Received : {eventData}")
            if event.type() == UserTreeFileDispatchedEvent.idType and eventData != UserTreeFileDispatchedEvent.idType:
                self.browseWidget.renderTree(eventData)
            elif event.type() == UsersListDispatchedEvent.idType:
                self.browseWidget.renderUsersList()

        except Exception as e:
            print(e)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    ui = MainWindow(mainWindow)
    mainWindow.showMaximized()
    sys.exit(app.exec_())