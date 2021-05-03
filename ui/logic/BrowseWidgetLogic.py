from os.path import abspath
import json

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt, QSortFilterProxyModel
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QWidget

from eventTypes import pipeName
from ui.design.browseWidgetDesign import Ui_DownloadWidget
from ui.models.treeModel import TreeModelFile
from ui.models.workers import PipeClientWorker, DownLoadWorker

from fakeData import generateFakeUsers


class BrowseWidget(QWidget, Ui_DownloadWidget):
    def __init__(self, window):
        super(BrowseWidget, self).__init__(window)
        self.window = window
        self.setupUi(window)

        self.foldIcon = QtGui.QIcon()
        self.fileIcon = QtGui.QIcon()

        self.usersListFile = abspath("./files/users_list.txt")
        self.usersModel = None
        self.fileTreeModel = None
        self.fileProxyModel = QSortFilterProxyModel()

        self.chosenUserTreeFile = None
        self.lastSearchedTreeFilter = None

        self.browseFileLineEdit.setStyleSheet('background-color: rgb(255, 255, 255);')
        self.browseUsersLineEdit.setStyleSheet('background-color: rgb(255, 255, 255);')
        self.userListView.setStyleSheet('background-color: rgb(255, 255, 255);')
        self.fileTreeView.setStyleSheet('background-color: rgb(255, 255, 255);')

        self.fileIcon.addPixmap(QtGui.QPixmap(":/windowIcons/fileIcon"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.foldIcon.addPixmap(QtGui.QPixmap(":/windowIcons/foldIcon"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        self.setLogic()

    def setLogic(self):
        self.userListView.clicked['QModelIndex'].connect(self.requestUserFileTree)
        self.browseUsersLineEdit.textChanged.connect(self.filterUsersList)
        self.refreshUsersButton.clicked.connect(self.requestRefreshUsersList)
        self.browseFileLineEdit.textChanged.connect(self.simpleTreeFilter)
        self.downloadButton.clicked.connect(self.prepareDownloadItemsAction)

    def disableButtons(self):
        self.downloadButton.setEnabled(False)

    def enableButtons(self):
        self.downloadButton.setEnabled(True)

    def makeRequest(self, requestMessage):
        try:
            self.thread = QtCore.QThread()
            self.worker = PipeClientWorker(pipeName, requestMessage)
            self.worker.moveToThread(self.thread)

            self.thread.started.connect(self.worker.run)
            self.worker.finished.connect(self.thread.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)

            self.thread.start()
        except Exception as e:
            print(e)

    def renderUsersList(self):
        self.usersModel = QStandardItemModel()
        self.browseUsersLineEdit.setText("")
        with open(self.usersListFile, "r") as inp:
            for line in inp.readlines():
                item = QStandardItem(line.strip())
                self.usersModel.appendRow(item)
        self.nrUsersLabel.setText(f"<html><head/><body><p><span style=\" font-size:10pt;\">Number of current users: "
                                  f"{str(self.usersModel.rowCount())} users</span></p></body></html>")
        self.userListView.setModel(self.usersModel)

    def filterUsersList(self, text):
        searchedText = text.lower()
        for row in range(self.usersModel.rowCount()):
            if searchedText in str(self.usersModel.item(row).text()).lower():
                self.userListView.setRowHidden(row, False)
            else:
                self.userListView.setRowHidden(row, True)

    def requestRefreshUsersList(self):
        generateFakeUsers()     # for testing
        requestMessage = json.dumps({'packet_type': 'REQUEST_USERS_LIST'})
        self.makeRequest(requestMessage)

    def requestUserFileTree(self, index):
        chosenUser = self.userListView.model().itemData(index)[Qt.DisplayRole]
        requestMessage = json.dumps({'packet_type': 'RQUEST_USER_FILE_STRUCTURE_PATH', 'foreign_user_id': chosenUser})
        self.makeRequest(requestMessage)

    def renderTree(self, treeFile: str):
        self.fileTreeModel = TreeModelFile(treeInput=treeFile, foldIcon=self.foldIcon, fileIcon=self.fileIcon)
        # Allows for scrolling optimizations.
        self.fileTreeView.setAlternatingRowColors(True)
        self.fileTreeView.setUniformRowHeights(True)
        self.fileProxyModel.setSourceModel(self.fileTreeModel)
        # self.fileProxyModel.sort()
        self.fileTreeView.setModel(self.fileProxyModel)
        self.enableButtons()

    def simpleTreeFilter(self, searchText):
        if self.fileTreeModel is not None and self.filterType == 0:
            search = QtCore.QRegExp(searchText,
                                    QtCore.Qt.CaseInsensitive,
                                    QtCore.QRegExp.RegExp
                                    )
            self.fileProxyModel.setFilterRegExp(search)

    def complexTreeFilter(self):
        searchText = self.browseFileLineEdit.text()
        if searchText == "":
            self.renderTree(self.chosenUserTreeFile)
        if self.fileTreeModel is not None and self.filterType == 1:
            if self.lastSearchedTreeFilter is not None and searchText not in self.lastSearchedTreeFilter:
                self.fileTreeModel = TreeModelFile(treeInput=self.chosenUserTreeFile,
                                                   foldIcon=self.foldIcon, fileIcon=self.fileIcon)
            newTreeDict = self.fileTreeModel.filterTree(searchText)
            if newTreeDict["#_size"] != 0:
                with open(abspath("./files/temp/treeFilterTemp.json"), "w") as filteredTree:
                    json.dump(newTreeDict, filteredTree)
                    self.chosenUserTreeFile = self.fileTreeModel.treeInput
                    self.lastSearchedTreeFilter = searchText
                self.renderTree(filteredTree.name)

    def prepareDownloadItemsAction(self):
        self.disableButtons()
        try:
            self.thread = QtCore.QThread()
            self.worker = DownLoadWorker(self.chosenUserTreeFile, self.fileTreeModel)
            self.worker.moveToThread(self.thread)

            self.thread.started.connect(self.worker.run)
            self.worker.finished.connect(self.thread.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)

            self.thread.start()
            self.thread.finished.connect(lambda: {self.renderTree(self.chosenUserTreeFile)})
        except Exception as e:
            print(e)
            self.enableButtons()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    downloadWidget = QtWidgets.QWidget()
    ui = BrowseWidget(downloadWidget)
    downloadWidget.show()
    sys.exit(app.exec_())
