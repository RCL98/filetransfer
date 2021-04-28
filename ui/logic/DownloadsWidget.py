from os.path import abspath
import pandas as pd

from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QWidget

from ui.logic.BrowseWidget import BrowseWidget
from ui.models.tableModel import DownloadsTableModel
from ui.models.treeModel import TreeModelFile


class DownloadsWidget(QWidget):
    def __init__(self, parent=None):
        super(DownloadsWidget, self).__init__(parent)
        self.parent = parent
        self.gridLayout_3 = QtWidgets.QGridLayout(self.parent)
        self.downTableFrame = QtWidgets.QFrame(self.parent)
        self.gridLayout = QtWidgets.QGridLayout(self.downTableFrame)
        self.downsTable = QtWidgets.QTableView(self.downTableFrame)
        self.detailsFrame = QtWidgets.QFrame(self.parent)
        self.gridLayout_2 = QtWidgets.QGridLayout(self.detailsFrame)
        self.tabWidget = QtWidgets.QTabWidget(self.detailsFrame)
        self.generalTab = QtWidgets.QWidget()
        self.contenTab = QtWidgets.QTreeView()
        self.foldIcon = QtGui.QIcon()
        self.fileIcon = QtGui.QIcon()
        # self.fileTreeView = QtWidgets.QTreeView(self.tabWidget)
        self.downloadsTableModel = None
        self.fileTreeModel = None
        self.setupUi()

    def renderTree(self, index):
        t = self.downsTable.model().data(index,
                                        DownloadsTableModel._RetrieveDownFile)
        t = abspath("./files/downloads/" + t)
        self.fileTreeModel = TreeModelFile(treeInput=t,
                                           foldIcon=self.foldIcon, fileIcon=self.fileIcon)
        # self.fileTreeView.setModel(self.fileTreeModel)
        # self.contenTab = QtWidgets.QTreeView(self.contenTab)
        self.contenTab.setModel(self.fileTreeModel)

    def setupUi(self):
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.downTableFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.downTableFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.downTableFrame.setObjectName("downTableFrame")
        self.gridLayout.setObjectName("gridLayout")

        self.downsTable.setObjectName("downsTable")
        # self.downsTable.setColumnCount(4)
        # self.downsTable.setRowCount(2)
        # item = QtWidgets.QTableWidgetItem()
        # self.downsTable.setVerticalHeaderItem(0, item)
        # item = QtWidgets.QTableWidgetItem()
        # self.downsTable.setVerticalHeaderItem(1, item)
        # item = QtWidgets.QTableWidgetItem()
        # self.downsTable.setHorizontalHeaderItem(0, item)
        # item = QtWidgets.QTableWidgetItem()
        # self.downsTable.setHorizontalHeaderItem(1, item)
        # item = QtWidgets.QTableWidgetItem()
        # self.downsTable.setHorizontalHeaderItem(2, item)
        # item = QtWidgets.QTableWidgetItem()
        # self.downsTable.setHorizontalHeaderItem(3, item)

        # item = UserItem("User1", abspath("./files/downloads/") + "user_tree_down.json")
        # self.downsTable.setItem(0, 0, item)
        # item = QtWidgets.QTableWidgetItem()
        # self.downsTable.setItem(0, 1, item)
        # item = QtWidgets.QTableWidgetItem()
        # self.downsTable.setItem(0, 2, item)
        # item = QtWidgets.QTableWidgetItem()
        # self.downsTable.setItem(0, 3, item)

        self.gridLayout.addWidget(self.downsTable, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.downTableFrame, 0, 0, 1, 1)

        self.detailsFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.detailsFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.detailsFrame.setObjectName("detailsFrame")
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.tabWidget.setObjectName("tabWidget")
        self.generalTab.setObjectName("generalTab")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/windowIcons/fileIcon"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.generalTab, icon, "")
        self.contenTab.setObjectName("contenTab")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/buttonIcons/openIcon"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.contenTab, icon1, "")
        self.gridLayout_2.addWidget(self.tabWidget, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.detailsFrame, 1, 0, 1, 1)

        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(self)

        # item = self.downsTable.verticalHeaderItem(0)
        # item.setText("1")
        # item = self.downsTable.verticalHeaderItem(1)
        # item.setText("2")
        # item = self.downsTable.horizontalHeaderItem(0)
        # item.setText("Name")
        # item = self.downsTable.horizontalHeaderItem(1)
        # item.setText("Dimension")
        # item = self.downsTable.horizontalHeaderItem(2)
        # item.setText("Progress")
        # item = self.downsTable.horizontalHeaderItem(3)
        # item.setText("Down speed")

        # item = self.downsTable.item(0, 0)
        # item.setText("User1 dasdasd asd asd asd asf asrf aw daw awfgaw egawf awsd")
        # item = self.downsTable.item(0, 1)
        # item.setText("54,6 GB")
        # item = self.downsTable.item(0, 2)
        # item.setText("76%")
        # item = self.downsTable.item(0, 3)
        # item.setText("34 Mb/s")

        self.fileIcon.addPixmap(QtGui.QPixmap(":/windowIcons/fileIcon"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.foldIcon.addPixmap(QtGui.QPixmap(":/windowIcons/foldIcon"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        downloadsData = pd.read_csv(abspath("./files/downloads/downloads_list.csv"))
        self.downloadsTableModel = DownloadsTableModel(self, downloadList=downloadsData)
        self.downsTable.setModel(self.downloadsTableModel)
        self.downsTable.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.generalTab), "General")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.contenTab), "Content")

        header = self.downsTable.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)

        self.downsTable.clicked['QModelIndex'].connect(self.renderTree)
        # self.downsTable.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        # self.downsTable.resizeColumnToContents(0)

    # def disableButtons(self):
    #     self.downloadButton.setEnabled(False)
    #
    # def enableButtons(self):
    #     self.downloadButton.setEnabled(True)
    #
    # def fillUsersList(self, users_input):
    #     self.usersModel = QStandardItemModel()
    #     with open(users_input, "r") as inp:
    #         for line in inp.readlines():
    #             item = UserItem(name=line.strip(), structFile=abspath('./files/user_tree.json'))
    #             self.usersModel.appendRow(item)
    #     self.usersList.setModel(self.usersModel)
    #     self.verticalLayout_3.addWidget(self.usersList)
    #
    # def filterUsersList(self, text):
    #     # search = QtCore.QRegExp(text,
    #     #                         QtCore.Qt.CaseInsensitive,
    #     #                         QtCore.QRegExp.RegExp
    #     #                         )
    #     # self.usersProxyModel.setFilterRegExp(search)
    #     searchedText = text.lower()
    #     for row in range(self.usersModel.rowCount()):
    #         if searchedText in str(self.usersModel.item(row).text()).lower():
    #             self.usersList.setRowHidden(row, False)
    #         else:
    #             self.usersList.setRowHidden(row, True)
    #
    # def renderTree(self, treeFile: str):
    #     self.fileTreeModel = TreeModelFile(treeInput=treeFile, foldIcon=self.foldIcon, fileIcon=self.fileIcon)
    #     # Allows for scrolling optimizations.
    #     self.fileTreeView.setAlternatingRowColors(True)
    #     self.fileTreeView.setUniformRowHeights(True)
    #     self.fileProxyModel.setSourceModel(self.fileTreeModel)
    #     # self.fileProxyModel.sort()
    #     self.fileTreeView.setModel(self.fileProxyModel)
    #     # self.header.setStretchLastSection(False)
    #     # self.header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
    #     # self.header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
    #     # self.header.setSectionResizeMode(0, QHeaderView.Stretch)
    #     self.enableButtons()
    #
    # def fillStructTree(self, index):
    #     self.chosenUserTreeFile = self.usersList.model().itemData(index)[UserItem.StructFileRole]
    #     self.renderTree(self.chosenUserTreeFile)
    #
    # def simpleTreeFilter(self, searchText):
    #     if self.fileTreeModel is not None and self.filterType == 0:
    #         search = QtCore.QRegExp(searchText,
    #                                 QtCore.Qt.CaseInsensitive,
    #                                 QtCore.QRegExp.RegExp
    #                                 )
    #         self.fileProxyModel.setFilterRegExp(search)
    #
    # def complexTreeFilter(self):
    #     searchText = self.browseFileLineEdit.text()
    #     if searchText == "":
    #         self.renderTree(self.chosenUserTreeFile)
    #     if self.fileTreeModel is not None and self.filterType == 1:
    #         if self.lastSearchedTreeFilter is not None and searchText not in self.lastSearchedTreeFilter:
    #             self.fileTreeModel = TreeModelFile(treeInput=self.chosenUserTreeFile,
    #                                                foldIcon=self.foldIcon, fileIcon=self.fileIcon)
    #         newTreeDict = self.fileTreeModel.filterTree(searchText)
    #         if newTreeDict["#_size"] != 0:
    #             with open(abspath("./files/temp/treeFilterTemp.json"), "w") as filteredTree:
    #                 json.dump(newTreeDict, filteredTree)
    #                 self.chosenUserTreeFile = self.fileTreeModel.treeInput
    #                 self.lastSearchedTreeFilter = searchText
    #             self.renderTree(filteredTree.name)
    #
    # def prepareDownloadItemsAction(self):
    #     self.disableButtons()
    #     try:
    #         self.thread = QtCore.QThread()
    #         self.worker = DownLoadWorker(self.chosenUserTreeFile, self.fileTreeModel)
    #         self.worker.moveToThread(self.thread)
    #
    #         self.thread.started.connect(self.worker.run)
    #         self.worker.finished.connect(self.thread.quit)
    #         self.worker.finished.connect(self.worker.deleteLater)
    #         self.thread.finished.connect(self.thread.deleteLater)
    #         # self.worker.statusBarMessage.connect(self.setStatusBarMessage)
    #         # self.worker.progressBarValue.connect(self.setProgressBarValue)
    #         # self.worker.stackAdd.connect(self.fillActionStack)
    #
    #         self.thread.start()
    #         self.thread.finished.connect(lambda x: {self.renderTree(self.chosenUserTreeFile)})
    #     except Exception as e:
    #         print(e)
    #         self.enableButtons()
