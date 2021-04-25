import json
from os.path import abspath

from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import QSortFilterProxyModel
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import QWidget

from ui.models.treeModel import TreeModelFile
from ui.models.workers import DownLoadWorker


class UserItem(QStandardItem):
    StructFileRole = QtCore.Qt.UserRole + 5

    def __init__(self, parent=None, name=None, structFile=None):
        super(UserItem, self).__init__(parent)
        self.setData(structFile, UserItem.StructFileRole)
        self.setText(name)


class BrowseWidget(QWidget):
    def __init__(self, parent=None):
        super(BrowseWidget, self).__init__(parent)
        self.parent = parent
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.parent)
        self.usersFrame = QtWidgets.QFrame(self.parent)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.usersFrame)
        self.browseUsersFrame = QtWidgets.QFrame(self.usersFrame)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.browseUsersFrame)
        self.browseUsersLabel = QtWidgets.QLabel(self.browseUsersFrame)
        self.browseUsersLineEdit = QtWidgets.QLineEdit(self.browseUsersFrame)
        self.usersList = QtWidgets.QListView(self.usersFrame)
        self.buttonsFrame = QtWidgets.QFrame(self.parent)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.buttonsFrame)
        self.downloadButton = QtWidgets.QPushButton(self.buttonsFrame)
        self.treeFrame = QtWidgets.QFrame(self.parent)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.treeFrame)
        self.browseFileFrame = QtWidgets.QFrame(self.treeFrame)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.browseFileFrame)
        self.browseFileLabel = QtWidgets.QLabel(self.browseFileFrame)
        self.browseFileLineEdit = QtWidgets.QLineEdit(self.browseFileFrame)
        self.fileTreeView = QtWidgets.QTreeView(self.treeFrame)
        self.foldIcon = QtGui.QIcon()
        self.fileIcon = QtGui.QIcon()
        self.filterType = 0
        self.lastSearchedTreeFilter = None
        self.chosenUserTreeFile = None
        self.usersModel = None
        self.fileTreeModel = None
        self.worker = None
        self.thread = None
        self.fileProxyModel = QSortFilterProxyModel()
        self.setupUi()

    def disableButtons(self):
        self.downloadButton.setEnabled(False)

    def enableButtons(self):
        self.downloadButton.setEnabled(True)

    def fillUsersList(self, users_input):
        self.usersModel = QStandardItemModel()
        with open(users_input, "r") as inp:
            for line in inp.readlines():
                item = UserItem(name=line.strip(), structFile=abspath('./files/user_tree.json'))
                self.usersModel.appendRow(item)
        self.usersList.setModel(self.usersModel)
        self.verticalLayout_3.addWidget(self.usersList)

    def filterUsersList(self, text):
        # search = QtCore.QRegExp(text,
        #                         QtCore.Qt.CaseInsensitive,
        #                         QtCore.QRegExp.RegExp
        #                         )
        # self.usersProxyModel.setFilterRegExp(search)
        searchedText = text.lower()
        for row in range(self.usersModel.rowCount()):
            if searchedText in str(self.usersModel.item(row).text()).lower():
                self.usersList.setRowHidden(row, False)
            else:
                self.usersList.setRowHidden(row, True)

    def renderTree(self, treeFile: str):
        self.fileTreeModel = TreeModelFile(treeInput=treeFile, foldIcon=self.foldIcon, fileIcon=self.fileIcon)
        # Allows for scrolling optimizations.
        self.fileTreeView.setAlternatingRowColors(True)
        self.fileTreeView.setUniformRowHeights(True)
        self.fileProxyModel.setSourceModel(self.fileTreeModel)
        # self.fileProxyModel.sort()
        self.fileTreeView.setModel(self.fileProxyModel)
        self.enableButtons()

    def fillStructTree(self, index):
        self.chosenUserTreeFile = self.usersList.model().itemData(index)[UserItem.StructFileRole]
        self.renderTree(self.chosenUserTreeFile)

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

    def setupUi(self):
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.usersFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.usersFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.usersFrame.setObjectName("usersFrame")
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.browseUsersFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.browseUsersFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.browseUsersFrame.setObjectName("browseUsersFrame")
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(9)
        self.browseUsersLabel.setFont(font)
        self.browseUsersLabel.setObjectName("browseUsersLabel")
        self.horizontalLayout_2.addWidget(self.browseUsersLabel)
        self.browseUsersLineEdit.setObjectName("browseUsersLineEdit")
        self.horizontalLayout_2.addWidget(self.browseUsersLineEdit)
        self.verticalLayout_3.addWidget(self.browseUsersFrame)
        self.usersList.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.usersList.setObjectName("usersList")

        self.horizontalLayout.addWidget(self.usersFrame)
        self.buttonsFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.buttonsFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.buttonsFrame.setObjectName("buttonsFrame")
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem)
        self.downloadButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.downloadButton.setLayoutDirection(QtCore.Qt.RightToLeft)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/buttonIcons/downloadIcon"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.downloadButton.setIcon(icon)
        self.downloadButton.setIconSize(QtCore.QSize(15, 15))
        self.downloadButton.setObjectName("downloadButton")
        self.verticalLayout_4.addWidget(self.downloadButton)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem1)
        self.horizontalLayout.addWidget(self.buttonsFrame)
        self.treeFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.treeFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.treeFrame.setObjectName("treeFrame")
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.browseFileFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.browseFileFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.browseFileFrame.setObjectName("browseFileFrame")
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(9)
        self.browseFileLabel.setFont(font)
        self.browseFileLabel.setObjectName("browseFileLabel")
        self.horizontalLayout_4.addWidget(self.browseFileLabel)
        self.browseFileLineEdit.setObjectName("browseFileLineEdit")
        self.horizontalLayout_4.addWidget(self.browseFileLineEdit)
        self.verticalLayout_5.addWidget(self.browseFileFrame)
        self.fileTreeView.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.fileTreeView.setObjectName("fileTreeView")
        self.verticalLayout_5.addWidget(self.fileTreeView)
        self.horizontalLayout.addWidget(self.treeFrame)
        self.browseUsersLabel.setBuddy(self.browseUsersLineEdit)
        self.browseFileLabel.setBuddy(self.browseFileLineEdit)

        self.browseFileLineEdit.setStyleSheet('background-color: rgb(255, 255, 255);')
        self.browseUsersLineEdit.setStyleSheet('background-color: rgb(255, 255, 255);')
        self.usersList.setStyleSheet('background-color: rgb(255, 255, 255);')
        self.fileTreeView.setStyleSheet('background-color: rgb(255, 255, 255);')

        QtCore.QMetaObject.connectSlotsByName(self)

        self.browseUsersLabel.setText("Browse Users:")
        self.downloadButton.setText("DownLoad")
        self.browseFileLabel.setText("Browse Files:")

        self.fileIcon.addPixmap(QtGui.QPixmap(":/windowIcons/fileIcon"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.foldIcon.addPixmap(QtGui.QPixmap(":/windowIcons/foldIcon"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        self.disableButtons()
        self.fillUsersList(abspath('./files/users_list.txt'))

        self.usersList.clicked['QModelIndex'].connect(self.fillStructTree)
        self.browseUsersLineEdit.textChanged.connect(self.filterUsersList)
        self.browseFileLineEdit.textChanged.connect(self.simpleTreeFilter)
        self.downloadButton.clicked.connect(self.prepareDownloadItemsAction)
