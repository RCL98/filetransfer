import json
from copy import deepcopy
from socket import gethostname
from os.path import abspath

from PyQt5.QtGui import QKeySequence

from ui.models.fileDialog import FileDialog
from ui.models.treeModel import TreeModelFile, FileSystem
from ui.models.workers import AddWorker, DeleteWorker
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QFrame, QShortcut
from PyQt5.QtWidgets import QMainWindow

from ui.startWindowDesign import Ui_StartWindow
import icons.icons


class VLine(QFrame):
    # a simple VLine, like the one you get from designer
    def __init__(self):
        super(VLine, self).__init__()
        self.setFrameShape(self.VLine | self.Sunken)


class StartWindow(QMainWindow, Ui_StartWindow):
    acceptState = QtCore.pyqtSignal(bool)

    def __init__(self, window):
        super(StartWindow, self).__init__(window)
        self.window = window
        self.progressWidget = QtWidgets.QWidget()
        self.progressHorizontalLayout = QtWidgets.QHBoxLayout()
        self.progressBar = QtWidgets.QProgressBar()
        self.progressLabel = QtWidgets.QLabel()
        self.foldIcon = QtGui.QIcon()
        self.fileIcon = QtGui.QIcon()
        self.saveShortCut = QShortcut(QKeySequence("Ctrl+S"), self)
        self.saveAsShortCut = QShortcut(QKeySequence("Ctrl+A+S"), self)
        self.currentTreeFile = abspath("./files/user_tree.json")
        self.fileTreeModel = None
        self.lastSaveFile = None
        self.fileSystem = FileSystem()
        self.progressValue = 0
        self.undoStack = []
        self.redoStack = []
        self.thread = None
        self.worker = None
        self.setupUi(window)
        self.setLogicAndAdjustments()

    def setLogicAndAdjustments(self):
        self.nameEdit.setPlaceholderText(gethostname())
        self.fileIcon.addPixmap(QtGui.QPixmap(":/windowIcons/fileIcon"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.foldIcon.addPixmap(QtGui.QPixmap(":/windowIcons/foldIcon"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        self.progressHorizontalLayout.setObjectName('progressHorizontalLayout')
        self.progressWidget.setLayout(self.progressHorizontalLayout)
        self.progressWidget.setMaximumWidth(450)
        self.progressWidget.layout().addWidget(self.progressLabel)
        self.progressWidget.layout().addWidget(self.progressBar)
        self.progressBar.setMaximumWidth(350)
        self.progressBar.setObjectName("progressBar")
        self.progressBar.setValue(0)
        self.progressLabel.setObjectName("progressLabel")
        self.progressLabel.setText("Progress:")
        self.statusbar.showMessage("Ready")
        self.statusbar.addPermanentWidget(VLine())
        self.statusbar.addPermanentWidget(self.progressWidget)
        self.statusbar.addPermanentWidget(VLine())

        self.undoButton.setEnabled(False)
        self.redoButton.setEnabled(False)
        self.renderTree()

        self.openButton.setToolTip('Open')
        self.addButton.setToolTip('Add Files')
        self.deleteButton.setToolTip('Delete Files')
        self.saveButton.setToolTip('Save')
        self.saveAsButton.setToolTip('Save As')
        self.undoButton.setToolTip('Undo Action')
        self.redoButton.setToolTip('Redo Action')

        self.saveShortCut.activated.connect(self.saveAction)
        self.saveAsShortCut.activated.connect(self.saveAsAction)

        self.acceptButton.clicked.connect(self.acceptAction)
        self.addButton.clicked.connect(self.addItemsAction)
        self.deleteButton.clicked.connect(self.deleteItemsAction)
        self.undoButton.clicked.connect(self.undoAction)
        self.redoButton.clicked.connect(self.redoAction)
        self.saveButton.clicked.connect(self.saveAction)
        self.saveAsButton.clicked.connect(self.saveAsAction)
        self.openButton.clicked.connect(self.openAction)

    def renderTree(self):
        self.fileTreeModel = TreeModelFile(parent=self.treeView, treeInput=self.currentTreeFile,
                                           foldIcon=self.foldIcon, fileIcon=self.fileIcon)

        self.selectedSizeLabel.setText("Selected Size: 0 ")
        self.selectedFilesLabel.setText("Selected Files: 0")

        self.fileTreeModel.selectedSizeSignal.connect(lambda size:
                                                      {self.selectedSizeLabel.setText("Selected Size: " + size)})
        self.fileTreeModel.selectedFilesSignal.connect(
            lambda files: {self.selectedFilesLabel.setText(f"Selected Files: {files}")})

        self.treeView.setModel(self.fileTreeModel)
        totalSize, totalFiles = self.fileTreeModel.getTotalSizeFiles()
        self.totalSizeLabel.setText("Total Size: " + totalSize)
        self.totalFilesLabel.setText(f"Total Files: {totalFiles}")
        self.treeView.resizeColumnToContents(0)
        self.statusbar.showMessage('Ready')
        self.progressBar.setValue(0)
        self.enableButtons()

    def acceptAction(self):
        # mainWin = QtWidgets.QMainWindow()
        # mainWindow.Ui_MainWindow(mainWin)
        self.acceptState.emit(True)
        self.hide()
        self.window.close()
        # mainWin.show()

    def disableButtons(self):
        self.addButton.setEnabled(False)
        self.deleteButton.setEnabled(False)
        self.undoButton.setEnabled(False)
        self.redoButton.setEnabled(False)
        self.saveButton.setEnabled(False)
        self.saveAsButton.setEnabled(False)
        self.acceptButton.setEnabled(False)
        self.openButton.setEnabled(False)

    def enableButtons(self):
        self.addButton.setEnabled(True)
        self.deleteButton.setEnabled(True)
        if self.undoStack:
            self.undoButton.setEnabled(True)
        if self.redoStack:
            self.redoButton.setEnabled(True)
        self.saveButton.setEnabled(True)
        self.saveAsButton.setEnabled(True)
        self.acceptButton.setEnabled(True)
        self.openButton.setEnabled(True)

    def addItemsAction(self):
        self.disableButtons()
        fileDialog = FileDialog()
        if fileDialog.exec_() == QtWidgets.QDialog.Accepted:
            try:
                self.thread = QtCore.QThread()
                self.worker = AddWorker(self.currentTreeFile, len(self.undoStack), fileDialog.selectedFiles())
                self.worker.moveToThread(self.thread)

                self.thread.started.connect(self.worker.run)
                self.worker.finished.connect(self.thread.quit)
                self.worker.finished.connect(self.worker.deleteLater)
                self.thread.finished.connect(self.thread.deleteLater)
                self.worker.statusBarMessage.connect(self.setStatusBarMessage)
                self.worker.progressBarValue.connect(self.setProgressBarValue)
                self.worker.stackAdd.connect(self.fillActionStack)

                self.thread.start()
                self.thread.finished.connect(self.renderTree)
            except Exception as e:
                print(e)
                self.enableButtons()

    def deleteItemsAction(self):
        self.disableButtons()
        try:
            self.thread = QtCore.QThread()
            self.worker = DeleteWorker(self.currentTreeFile, len(self.undoStack), self.fileTreeModel)
            self.worker.moveToThread(self.thread)

            self.thread.started.connect(self.worker.run)
            self.worker.finished.connect(self.thread.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)
            self.worker.statusBarMessage.connect(self.setStatusBarMessage)
            self.worker.progressBarValue.connect(self.setProgressBarValue)
            self.worker.stackAdd.connect(self.fillActionStack)

            self.thread.start()
            self.thread.finished.connect(self.renderTree)
        except Exception as e:
            print(e)
            self.enableButtons()

    def swapActions(self, treeFile):
        self.disableButtons()
        with open(treeFile, "r+") as jStackFile:
            newDict = json.load(jStackFile)
            with open(self.currentTreeFile, "r+") as jCurrentFile:
                oldDict = json.load(jCurrentFile)
                jCurrentFile.seek(0)
                jCurrentFile.truncate()
                json.dump(newDict, jCurrentFile)
            jStackFile.seek(0)
            jStackFile.truncate()
            json.dump(oldDict, jStackFile)
        self.renderTree()

    def fillActionStack(self, action: str):
        self.undoStack.append(action)

    def undoAction(self):
        if self.undoStack:
            treeFile = self.undoStack.pop()
            self.redoStack.append(treeFile)
            self.swapActions(treeFile)

    def redoAction(self):
        if self.redoStack:
            treeFile = self.redoStack.pop()
            self.undoStack.append(treeFile)
            self.swapActions(treeFile)

    def saveFile(self):
        try:
            with open(self.lastSaveFile, "w") as saveFile:
                with open(self.currentTreeFile, "r") as jFile:
                    currentState = json.load(jFile)
                json.dump(currentState, saveFile)
        except Exception as e:
            print(e)
            self.lastSaveFile = None

    def saveAsAction(self):
        self.disableButtons()
        self.lastSaveFile, _ = QtWidgets.QFileDialog.getSaveFileName(parent=self.centralwidget,
                                                                     caption='Save As', filter='JSON (*.json)')
        self.saveFile()
        self.enableButtons()

    def saveAction(self):
        if not self.lastSaveFile:
            self.saveAsAction()
        else:
            self.saveFile()

    def openAction(self):
        self.disableButtons()
        newFile, _ = QtWidgets.QFileDialog.getOpenFileName(parent=self.centralwidget, caption='Open',
                                                           filter='JSON (*.json)')
        try:
            with open(newFile, "r+") as jFile:
                tree = json.load(jFile)
                treeCopy = deepcopy(tree)
                inconsistencies = self.fileSystem.checkTreeIntegrity(treeCopy)
                jFile.seek(0)
                jFile.truncate()
                json.dump(treeCopy, jFile)
            self.currentTreeFile = newFile
            self.renderTree()
        except Exception as e:
            print(e)
            self.statusbar.showMessage('Ready')
            self.progressBar.setValue(0)
            self.enableButtons()

    def setStatusBarMessage(self, message: str):
        self.statusbar.showMessage(message)

    def setProgressBarValue(self, value: int):
        self.progressBar.setValue(value)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    startWindow = QtWidgets.QMainWindow()
    ui = StartWindow(startWindow)
    startWindow.showMaximized()
    sys.exit(app.exec_())
