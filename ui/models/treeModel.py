import copy
import json
import os
from pathlib import Path
from typing import Tuple

from PyQt5 import QtCore
from PyQt5.QtCore import QAbstractItemModel, Qt, QModelIndex

from items import FolderItem, formatSize

if os.name == "nt":
    import win32api
    import win32con

    excluded = {
        "$RECYCLE.BIN",
        "DumpStack.log.tmp",
        "System Volume Information",
        "Windows",
    }


class FileSystem(QtCore.QObject):
    statusBarMessage = QtCore.pyqtSignal(str)
    progressBarValue = QtCore.pyqtSignal(int)

    @staticmethod
    def isHiddenOrSystem(path: str) -> bool:
        if os.name == "nt":
            attribute = win32api.GetFileAttributes(path)
            result = True if attribute & (
                win32con.FILE_ATTRIBUTE_HIDDEN | win32con.FILE_ATTRIBUTE_SYSTEM) != 0 else False
            return result
        else:
            return path.rsplit("/", 1)[-1].startswith(".")

    def getSizes(self, dictionary: dict) -> Tuple[int, int]:
        final_size, final_number = 0, 0
        for key in dictionary.keys():
            if key != "#_size" and key != "#_nrFiles" and key != "#_files":
                size, nr = self.getSizes(dictionary[key])
                final_size += size
                final_number += nr
        dictionary["#_size"] += final_size
        dictionary["#_nrFiles"] += final_number
        return dictionary["#_size"], dictionary["#_nrFiles"]

    def getSimpleTreeFileStructure(self, dirpath: str) -> dict:
        root = dirpath if dirpath[-1] != "\\" else dirpath[:-1]
        rootDict = {root: {"#_files": [], "#_size": 0, "#_nrFiles": 0}}
        for path, subDirs, files in os.walk(dirpath):
            folderDict = rootDict[root]
            path_extension = path[len(dirpath):]
            self.statusBarMessage.emit("Analyzing: " + path)
            for folder in path_extension.split("\\"):
                if folder:
                    folderDict = folderDict[folder]
            for file in files:
                if file not in excluded and not self.isHiddenOrSystem(path + "\\" + file):
                    self.statusBarMessage.emit("Analyzing: " + file)
                    fileSize = os.stat(path + "/" + file).st_size
                    folderDict["#_nrFiles"] += 1
                    folderDict["#_size"] += fileSize
                    folderDict["#_files"].append({"filename": file, "#_size": fileSize})
            # if not folderDict["#_files"]:
            #     del folderDict["#_files"]
            else:
                folderDict["#_nrFiles"] = len(folderDict["#_files"])
            subDirs[:] = [d for d in subDirs if d not in excluded and not self.isHiddenOrSystem(path + "\\" + d)]
            for folder in subDirs:
                folderDict[folder] = {"#_files": [], "#_size": 0, "#_nrFiles": 0}
        return rootDict

    def getFullFileStructure(self, dirpath: str, nrDirs=1) -> dict:
        root = dirpath if dirpath[-1] != "\\" else dirpath[:-1]
        folderDict = {"#_files": [], "#_size": 0, "#_nrFiles": 0}
        self.statusBarMessage.emit("Analyzing: " + root)
        currentDirs = 1
        with os.scandir(dirpath) as dirs:
            for entry in dirs:
                foldPath = root + "\\" + entry.name
                if entry.name not in excluded and not self.isHiddenOrSystem(foldPath):
                    if entry.is_file():
                        fileSize = os.stat(dirpath + "\\" + entry.name).st_size
                        folderDict["#_nrFiles"] += 1
                        folderDict["#_size"] += fileSize
                        folderDict["#_files"].append({"filename": entry.name, "#_size": fileSize})
                        self.statusBarMessage.emit("Analyzing: " + root + entry.name)
                    elif entry.is_dir():
                        try:
                            folderDict[entry.name] = self.getFullFileStructure(foldPath, nrDirs)
                            folderDict["#_size"] += folderDict[entry.name]["#_size"]
                            folderDict["#_nrFiles"] += folderDict[entry.name]["#_nrFiles"]
                            currentDirs += 1
                        except WindowsError:
                            pass
            # if not folderDict["#_files"]:
            #     del folderDict["#_files"]
        nrDirs += currentDirs
        self.progressBarValue.emit(int(currentDirs / nrDirs * 10))
        return folderDict

    def getFileStructure(self, dirpath: str, withSize=False) -> dict:
        if withSize:
            root = dirpath if dirpath[-1] != "\\" else dirpath[:-1]
            return {root: self.getFullFileStructure(dirpath)}
        return self.getSimpleTreeFileStructure(dirpath)

    def checkIntegrity(self, tree: dict, inconsistencies: list, parent: Path) -> (int, int):
        actualSize, actualNrFiles = 0, 0
        it = 0
        while it < len(tree.get('#_files', [])):
            fileObj = parent / tree['#_files'][it]['filename']
            if fileObj.is_file():
                self.statusBarMessage.emit("Checking: " + fileObj.resolve().__str__())
                size = fileObj.stat().st_size
                if size != tree['#_files'][it]['size']:
                    inconsistencies.append((fileObj.resolve().__str__(), 'szf', size, tree['#_files'][it]['size']))
                    tree['#_files'][it]['size'] = size
                actualSize += size
                actualNrFiles += 1
                it += 1
            else:
                inconsistencies.append((fileObj.resolve().__str__(), 'nef'))
                del tree['#_files'][it]
        for key in list(tree.keys()):
            if key not in ['size', 'nrFiles', '#_files']:
                folder = parent / key
                if folder.is_dir():
                    self.statusBarMessage.emit("Checking: " + folder.resolve().__str__())
                    size, nrFiles = self.checkIntegrity(tree[key], inconsistencies, folder)
                    if size != tree[key]['size']:
                        inconsistencies.append((folder.resolve().__str__(), 'szd', size, tree[key]['size']))
                        tree[key]['size'] = size
                    if nrFiles != tree[key]['nrFiles']:
                        inconsistencies.append((folder.resolve().__str__(), 'nrd', nrFiles, tree[key]['nrFiles']))
                        tree[key]['nrFiles'] = nrFiles
                    actualSize += size
                    actualNrFiles += nrFiles
                else:
                    inconsistencies.append((folder.resolve().__str__(), 'ned'))
        return actualSize, actualNrFiles

    def checkTreeIntegrity(self, tree: dict) -> list:
        actualSize, actualNrFiles, inconsistencies, treeLength = 0, 0, [], len(tree) - 2
        if treeLength > 0:
            # progress = 1
            for key in tree.keys():
                if key != 'size' and key != 'nrFiles':
                    self.statusBarMessage.emit("Checking: " + key)
                    # if progressBar and statusBar:
                    #     statusBar.showMessage("Checking: " + key)
                    #     progressBar.setValue(int(progress / treeLength * 100))
                    #     progress += 1
                    parentPath = key if key != '<Files>' else ''
                    size, nrFiles = self.checkIntegrity(tree[key], inconsistencies, Path(parentPath))
                    if size != tree[key]['size']:
                        inconsistencies.append((key, 'szd', size, tree[key]['size']))
                        tree[key]['size'] = size
                    if nrFiles != tree[key]['nrFiles']:
                        inconsistencies.append((key, 'nrd', nrFiles, tree[key]['nrFiles']))
                        tree[key]['nrFiles'] = nrFiles
                    actualSize += size
                    actualNrFiles += nrFiles
            if actualSize != tree['size']:
                inconsistencies.append(('All', 'szd', actualSize, tree['size']))
                tree['size'] = actualSize
            if actualNrFiles != tree['nrFiles']:
                inconsistencies.append(('All', 'nrd', actualNrFiles, tree['nrFiles']))
                tree['nrFiles'] = actualNrFiles
        else:
            inconsistencies.append('NTD')
        return inconsistencies

    def treeIterator(self, currentItem):
        yield currentItem
        try:
            if currentItem.isExpanded():
                for child in currentItem.childItems:
                    yield from self.treeIterator(child)
        except AttributeError:
            pass

    @staticmethod
    def updateSizeAndFiles(branch: dict, path: list, size: int, nrFiles: int, multiplier=1) -> dict:
        branch["#_size"] += multiplier * size
        branch["#_nrFiles"] += multiplier * nrFiles
        for key in path:
            branch = branch[key]
            branch["#_size"] += multiplier * size
            branch["#_nrFiles"] += multiplier * nrFiles
        return branch

    @staticmethod
    def treeWalk(tree: dict, path: list) -> dict:
        for key in path:
            tree = tree[key]
        return tree


class TreeModelFile(QAbstractItemModel):
    selectedSizeSignal = QtCore.pyqtSignal(str)
    selectedFilesSignal = QtCore.pyqtSignal(int)

    def __init__(self, parent=None, columns=None, treeInput=None, foldIcon=None, fileIcon=None):
        super(TreeModelFile, self).__init__(parent)
        if columns is None:
            columns = ["Name", "File type", "Size", "Contains"]
        assert treeInput is not None, "treeInput must be a valid file!"

        self.columnNames = columns
        # self.treeDict = {}
        self.treeInput = treeInput
        self.foldIcon = foldIcon
        self.fileIcon = fileIcon
        # self.load_treeDict()
        self.rootItem = FolderItem(path=[], treeInput=treeInput, foldIcon=self.foldIcon, fileIcon=self.fileIcon)
        self.rootItem.load_children()
        self.selectedSize = 0
        self.selectedFiles = 0

    # def load_treeDict(self):
    #     with open(self.treeInput, "r") as jsonFile:
    #         self.treeDict = json.load(jsonFile)
    #     self.selectedFilesSignal.emit(0)
    #     self.selectedSizeSignal.emit(0)

    def columnCount(self, parent=None):
        return len(self.columnNames)

    def data(self, index, role=None):
        if not index.isValid():
            return None

        item = index.internalPointer()

        if role == Qt.DisplayRole:
            return item.data(index.column())
        elif role == Qt.CheckStateRole and index.column() == 0:
            return item.getCheckedState()
        elif role == Qt.ToolTipRole:
            return item.toolTip(index.column())
        elif role == Qt.DecorationRole and index.column() == 0:
            return item.icon
        else:
            return None

    def setData(self, index, value, role=Qt.EditRole):
        if role == Qt.CheckStateRole:
            item = index.internalPointer()
            size, files = item.setCheckedState(value)
            self.selectedSize += size
            self.selectedFiles += files
            self.selectedSizeSignal.emit(formatSize(self.selectedSize))
            self.selectedFilesSignal.emit(self.selectedFiles)
            self.dataChanged.emit(QtCore.QModelIndex(), QtCore.QModelIndex())
        return True

    def getRootItem(self) -> FolderItem:
        return self.rootItem

    def selectLength(self) -> (int, int):
        return self.selectedSize, self.selectedFiles

    def canFetchMore(self, index):
        if not index.isValid():
            return False
        item = index.internalPointer()
        return not item.is_loaded

    def fetchMore(self, index):
        item = index.internalPointer()
        item.load_children()

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags

        return Qt.ItemIsEnabled | Qt.ItemIsUserCheckable

    def headerData(self, section, orientation, role=None):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.columnNames[section]

        return None

    def index(self, row, column, parent=None):
        if not self.hasIndex(row, column, parent):
            return QModelIndex()

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return QModelIndex()

        childItem = index.internalPointer()
        parentItem = childItem.parent()

        if parentItem == self.rootItem:
            return QModelIndex()

        return self.createIndex(parentItem.row(), 0, parentItem)

    def rowCount(self, parent=None):
        if parent.column() > 0:
            return 0

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        return parentItem.childCount()

    def getTotalSizeFiles(self):
        with open(self.treeInput, "r") as jsonFile:
            treeDict = json.load(jsonFile)
        return formatSize(treeDict["#_size"]), treeDict["#_nrFiles"]

    def __fullSearch(self, search: str, folder: dict):
        newBranch = {"#_size": 0, "#_nrFiles": 0, "#_files": []}
        for file in folder["#_files"]:
            if search in file["filename"]:
                newBranch["#_files"].append(file)
                newBranch["#_size"] += file["#_size"]
                newBranch["#_nrFiles"] += 1
        for subFold in folder.keys():
            if subFold not in ["#_size", "#_nrFiles", "#_files"]:
                if search in subFold:
                    newBranch[subFold] = copy.deepcopy(folder[subFold])
                else:
                    branch = self.__fullSearch(search, folder[subFold])
                    if branch["#_size"] != 0:
                        newBranch[subFold] = branch
                        newBranch["#_size"] += branch["#_size"]
                        newBranch["#_nrFiles"] += branch["#_nrFiles"]
        return newBranch

    def filterTree(self, search: str):
        newDict = {"#_size": 0, "#_nrFiles": 0, "<Files>": {"#_size": 0, "#_nrFiles": 0, "#_files": []}}
        search = search.lower()
        with open(self.treeInput, "r") as treeFile:
            treeDict = json.load(treeFile)
        for file in treeDict["<Files>"]["#_files"]:
            if search in file['filename']:
                newDict["<Files>"]["#_files"].append(file)
                newDict["<Files>"]["#_size"] += file["#_size"]
                newDict["<Files>"]["#_nrFiles"] += 1
        for fold in treeDict.keys():
            if fold not in ["#_size", "#_nrFiles", "<Files>"]:
                if search in fold:
                    newDict[fold] = copy.deepcopy(treeDict[fold])
                else:
                    branch = self.__fullSearch(search, treeDict[fold])
                    if branch["#_size"] != 0:
                        newDict[fold] = branch
                if newDict.get(fold, None) is not None:
                    newDict["#_size"] += newDict[fold]["#_size"]
                    newDict["#_nrFiles"] += newDict[fold]["#_nrFiles"]
        return newDict
