import os

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QPushButton, QTreeView

from treeModel import FileSystem


class FileDialog(QFileDialog):
    def __init__(self, *args, **kwargs):
        QFileDialog.__init__(self, *args, **kwargs)
        self.selectedItems = {'#_folders': [], '#_files': []}
        self.setOption(self.DontUseNativeDialog, True)
        self.setFileMode(self.ExistingFiles)
        buttons = self.findChildren(QPushButton)
        self.openBtn = [x for x in buttons if 'open' in str(x.text()).lower()][0]
        self.openBtn.clicked.disconnect()
        self.openBtn.clicked.connect(self.openClicked)
        self.tree = self.findChild(QTreeView)
        self.fileSystem = FileSystem()

    def openClicked(self):
        indexes = self.tree.selectionModel().selectedIndexes()
        accepted = True
        for i in indexes:
            if i.column() == 0:
                path = os.path.join(str(self.directory().absolutePath()), i.data())
                if os.name == "nt":
                    path = path.replace('/', '\\')
                if os.path.islink(path) or os.path.ismount(path):  # TO DO: resolve mount problem
                    accepted = False
                    break
                if os.path.isdir(path):
                    self.selectedItems['#_folders'].append(path)
                elif os.path.isfile(path):
                    self.selectedItems['#_files'].append(path)
        if not accepted:
            self.reject()
        else:
            self.accept()
        self.hide()

    def selectedFiles(self) -> dict:
        return self.selectedItems

    def accept(self):
        for file in self.selectedItems['#_files']:
            if self.fileSystem.isHiddenOrSystem(file):
                QtWidgets.QDialog.reject(self)
        QtWidgets.QDialog.accept(self)


# def getOpenFilesAndDirs(parent=None, caption='', directory='',
#                         filter='', initialFilter='', options=None):
#     def updateText():
#         # update the contents of the line edit widget with the selected files
#         selected = []
#         for index in view.selectionModel().selectedRows():
#             selected.append('"{}"'.format(index.data()))
#         lineEdit.setText(' '.join(selected))
#
#     dialog = QtWidgets.QFileDialog(parent, windowTitle=caption)
#     dialog.setFileMode(dialog.ExistingFiles)
#     if options:
#         dialog.setOptions(options)
#     dialog.setOption(dialog.DontUseNativeDialog, True)
#     if directory:
#         dialog.setDirectory(directory)
#     if filter:
#         dialog.setNameFilter(filter)
#         if initialFilter:
#             dialog.selectNameFilter(initialFilter)
#
#     # by default, if a directory is opened in file listing mode,
#     # QFileDialog.accept() shows the contents of that directory, but we
#     # need to be able to "open" directories as we can do with files, so we
#     # just override accept() with the default QDialog implementation which
#     # will just return exec_()
#     dialog.accept = lambda: QtWidgets.QDialog.accept(dialog)
#
#     # there are many item views in a non-native dialog, but the ones displaying
#     # the actual contents are created inside a QStackedWidget; they are a
#     # QTreeView and a QListView, and the tree is only used when the
#     # viewMode is set to QFileDialog.Details, which is not this case
#     stackedWidget = dialog.findChild(QtWidgets.QStackedWidget)
#     view = stackedWidget.findChild(QtWidgets.QListView)
#     view.selectionModel().selectionChanged.connect(updateText)
#
#     lineEdit = dialog.findChild(QtWidgets.QLineEdit)
#     # clear the line edit contents whenever the current directory changes
#     dialog.directoryEntered.connect(lambda: lineEdit.setText(''))
#
#     dialog.exec_()
#     return dialog.selectedFiles()
