from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget

from ui.downloadWidgetDesign import Ui_DownloadWidget


class DownloadWidget(QWidget, Ui_DownloadWidget):
    def __init__(self, window):
        super(DownloadWidget, self).__init__(window)
        self.window = window
        self.setupUi(window)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    downloadWidget = QtWidgets.QWidget()
    ui = DownloadWidget(downloadWidget)
    downloadWidget.show()
    sys.exit(app.exec_())
