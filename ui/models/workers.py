import json
import os
from copy import deepcopy

import pywintypes
import winerror
from PyQt5 import QtCore
from PyQt5.QtCore import Qt

from treeModel import FileSystem, TreeModelFile
from pipes import ClientPipe


class AddWorker(QtCore.QObject):
    statusBarMessage = QtCore.pyqtSignal(str)
    progressBarValue = QtCore.pyqtSignal(int)
    stackAdd = QtCore.pyqtSignal(str)
    finished = QtCore.pyqtSignal()

    def __init__(self, currentTreeFile: str, stackSize: int, selectedItems: dict):
        super(AddWorker, self).__init__()
        self.currentTreeFile = currentTreeFile
        self.actionsStackSize = stackSize
        self.selectedItems = selectedItems
        self.fileSystem = FileSystem()
        self.progressThresholds = [int(i / (len(selectedItems['#_folders']) + 1) * 100) for i, p in
                                   enumerate(selectedItems['#_folders'])] + [100]
        self.currentProgress = 1
        self.fileSystem.statusBarMessage.connect(self.sendMessage)
        self.fileSystem.progressBarValue.connect(self.sendValue)

    def sendMessage(self, message):
        self.statusBarMessage.emit(message)

    def sendValue(self, value):
        if self.currentProgress < len(self.progressThresholds) - 1:
            finalValue = min(self.progressThresholds[self.currentProgress] + value,
                             self.progressThresholds[self.currentProgress + 1] - 1)
        else:
            finalValue = min(self.progressThresholds[self.currentProgress] + value, 95)
        self.progressBarValue.emit(finalValue)

    def run(self):
        try:
            with open(self.currentTreeFile, "r") as jFile:
                originalDict = json.load(jFile)
        except json.JSONDecodeError:
            originalDict = {
                "<Files>": {"#_files": [], "#_size": 0, "#_nrFiles": 0},
                "#_size": 0,
                "#_nrFiles": 0,
            }

        copyDict = deepcopy(originalDict)
        self.currentProgress = 0
        for folder in self.selectedItems["#_folders"]:
            self.statusBarMessage.emit('Adding: ' + folder)
            it = 0
            while it < len(copyDict["<Files>"]["#_files"]):
                if copyDict["<Files>"]["#_files"][it]["filename"].find(folder) != -1:
                    copyDict["<Files>"]["#_size"] -= copyDict["<Files>"]["#_files"][it]["#_size"]
                    copyDict["<Files>"]["#_nrFiles"] -= 1
                    del copyDict["<Files>"]["#_files"][it]
                else:
                    it += 1
            folderDict = self.fileSystem.getFileStructure(folder, withSize=True)
            finalDict = folderDict
            for key in copyDict.copy().keys():
                if key in ["#_size", "#_nrFiles", "<Files>"]:
                    continue
                if key == folder:
                    copyDict["#_size"] -= copyDict[key]["#_size"]
                    copyDict["#_nrFiles"] -= copyDict[key]["#_nrFiles"]
                elif folder.find(key) != -1:
                    try:
                        folderCopy = {key: deepcopy(copyDict[key])}
                        keys = [k for k in folder[len(key) + 1:].split("\\")[:-1] if k]
                        folderIterator = self.fileSystem.updateSizeAndFiles(folderCopy[key], keys,
                                                                            folderDict[folder]["#_size"],
                                                                            folderDict[folder]["#_nrFiles"])
                        foldKey = folder.rsplit("\\", 1)[1]
                        if foldKey in folderIterator.keys():
                            copyDict["#_size"] -= folderIterator[foldKey]["#_size"]
                            copyDict["#_nrFiles"] -= folderIterator[foldKey]["#_nrFiles"]
                            self.fileSystem.updateSizeAndFiles(folderCopy[key], keys,
                                                               folderIterator[foldKey]["#_size"],
                                                               folderIterator[foldKey]["#_nrFiles"], -1)
                        folderIterator.update(folderDict)
                        folderIterator[foldKey] = folderIterator.pop(folder)
                        finalDict = folderCopy
                    except KeyError:
                        pass
                elif key.find(folder) != -1:
                    copyDict["#_size"] -= copyDict[key]["#_size"]
                    copyDict["#_nrFiles"] -= copyDict[key]["#_nrFiles"]
                    del copyDict[key]
                    if key in finalDict.keys():
                        del finalDict[key]
            copyDict["#_size"] += folderDict[folder]["#_size"]
            copyDict["#_nrFiles"] += folderDict[folder]["#_nrFiles"]
            copyDict.update(finalDict)
            self.progressBarValue.emit(self.progressThresholds[self.currentProgress])
            self.currentProgress += 1

        filesLength = len(self.selectedItems["#_files"])
        fileProgress = 1
        if self.selectedItems["#_files"]:
            existingFiles = {f["filename"]: (f["#_size"], idx) for idx, f in
                             enumerate(copyDict["<Files>"]["#_files"])}
            for file in self.selectedItems["#_files"]:
                self.statusBarMessage.emit('Adding: ' + file)
                fileSize = os.stat(file).st_size
                try:
                    size, idx = existingFiles[file]
                    if size != fileSize:
                        copyDict["<Files>"]["#_size"] += fileSize - size
                        copyDict["#_size"] += fileSize - size
                        copyDict["<Files>"]["#_files"][idx]["#_size"] = fileSize
                except KeyError:
                    copyDict["<Files>"]["#_size"] += fileSize
                    copyDict["<Files>"]["#_nrFiles"] += 1
                    copyDict["<Files>"]["#_files"].append({"filename": file, "#_size": fileSize})
                    copyDict["#_size"] += fileSize
                    copyDict["#_nrFiles"] += 1
                self.progressBarValue.emit(
                    self.progressThresholds[self.currentProgress] + int(fileProgress / filesLength * 10))
                fileProgress += 1

        self.progressBarValue.emit(100)
        self.statusBarMessage.emit("Finished! Now preparing the file tree for rendering!")
        with open(self.currentTreeFile, "w") as jFile:
            json.dump(copyDict, jFile)

        with open(os.path.abspath("./files/temp/userTreeTemp") + str(self.actionsStackSize)
                  + ".json", "w") as jFileTemp:
            json.dump(originalDict, jFileTemp)
            self.stackAdd.emit(jFileTemp.name)
        self.finished.emit()


class DeleteWorker(QtCore.QObject):
    statusBarMessage = QtCore.pyqtSignal(str)
    progressBarValue = QtCore.pyqtSignal(int)
    stackAdd = QtCore.pyqtSignal(str)
    finished = QtCore.pyqtSignal()

    def __init__(self, currentTreeFile: str, stackSize: int, treeModel: TreeModelFile):
        super(DeleteWorker, self).__init__()
        self.currentTreeFile = currentTreeFile
        self.actionsStackSize = stackSize
        self.fileTreeModel = treeModel
        self.fileSystem = FileSystem()

    def run(self):
        with open(self.currentTreeFile, "r+") as jFile:
            treeDict = json.load(jFile)
            newTreeDict = {"#_size": treeDict["#_size"], "#_nrFiles": treeDict["#_nrFiles"]}
            _, selectedFiles = self.fileTreeModel.selectLength()
            progress, oldProgress = 0, 0
            delete = False
            for child in self.fileTreeModel.getRootItem().childItems:
                if child.getCheckedState() == Qt.Unchecked:
                    newTreeDict[child.path[0]] = deepcopy(treeDict[child.path[0]])
                else:
                    delete = True
                    progress += treeDict[child.path[0]]["#_nrFiles"]
                    newTreeDict["#_size"] -= treeDict[child.path[0]]["#_size"]
                    newTreeDict["#_nrFiles"] -= treeDict[child.path[0]]["#_nrFiles"]
                    self.statusBarMessage.emit('Deleting: ' + '/'.join(child.path))
                for subChild in child.childItems:
                    for item in self.fileSystem.treeIterator(subChild):  # TODO: more efficient
                        if item.__itemType__() == 1:
                            if item.getCheckedState() == Qt.Checked:
                                if item.parentItem.getCheckedState() == Qt.Unchecked:
                                    self.statusBarMessage.emit('Deleting: ' + '\\'.join(item.path))
                                    folder = self.fileSystem.updateSizeAndFiles(newTreeDict, item.parentItem.path,
                                                                                item.size,
                                                                                item.nrFiles, -1)
                                    del folder[item.path[-1]]
                                    progress += item.nrFiles
                                    self.progressBarValue.emit(int(progress / selectedFiles * 100))
                            elif item.parentItem.getCheckedState() == Qt.Checked:
                                folder = self.fileSystem.treeWalk(treeDict, item.path)
                                newTreeDict["\\".join(item.path)] = deepcopy(folder)
                                newTreeDict["#_size"] += item.size
                                newTreeDict["#_nrFiles"] += item.nrFiles
                                progress -= item.nrFiles
                        else:
                            if item.getCheckedState() == Qt.Checked:
                                if item.parentItem.getCheckedState() == Qt.Unchecked:
                                    self.statusBarMessage.emit('Deleting: ' + item.fileName + item.extension)
                                    folder = self.fileSystem.updateSizeAndFiles(newTreeDict, item.parentItem.path,
                                                                                item.size, 1, -1)
                                    for ind, file in enumerate(folder["#_files"]):  # TODO: better deletion
                                        if file["filename"] == item.fileName + item.extension:
                                            foundInd = ind
                                            break
                                    del folder["#_files"][foundInd]
                                    progress += 1
                                    self.progressBarValue.emit(progress / selectedFiles * 100)
                            elif item.parentItem.getCheckedState() == Qt.Checked:
                                folder = self.fileSystem.treeWalk(treeDict, item.parentItem.path)
                                for file in folder["#_files"]:
                                    if file["filename"] == item.fileName + item.extension:
                                        newTreeDict["<Files>"]["#_files"].append(
                                            {"filename": "\\".join(item.parentItem.path + [file["filename"]]),
                                             "#_size": file["#_size"]}
                                        )
                                        newTreeDict["<Files>"]["#_size"] += item.size
                                        newTreeDict["<Files>"]["#_nrFiles"] += 1
                                        progress -= 1
                                        break
                if delete:
                    self.progressBarValue.emit(int(progress / selectedFiles * 100))
                    delete = False
            self.statusBarMessage.emit("Finished! Now preparing the file tree for rendering!")
            with open(os.path.abspath("./files/temp/userTreeTemp") + str(self.actionsStackSize)
                      + ".json", "w") as jFileTemp:
                json.dump(treeDict, jFileTemp)
                self.stackAdd.emit(jFileTemp.name)
            jFile.seek(0)
            jFile.truncate()
            if newTreeDict.get("<Files>", None) is None:
                newTreeDict["<Files>"] = {"#_size": 0, "#_nrFiles": 0, "#_files": []}
            json.dump(newTreeDict, jFile)
        self.finished.emit()


class DownLoadWorker(QtCore.QObject):
    finished = QtCore.pyqtSignal()

    def __init__(self, currentTreeFile: str, treeModel: TreeModelFile):
        super(DownLoadWorker, self).__init__()
        self.currentTreeFile = currentTreeFile
        self.fileTreeModel = treeModel
        self.fileSystem = FileSystem()

    def run(self):
        with open(self.currentTreeFile, "r") as jFile:
            treeDict = json.load(jFile)
            downTreeDict = {"#_size": treeDict["#_size"], "#_nrFiles": treeDict["#_nrFiles"]}
            for child in self.fileTreeModel.getRootItem().childItems:
                if child.getCheckedState() == Qt.Checked:
                    downTreeDict[child.path[0]] = deepcopy(treeDict[child.path[0]])
                else:
                    downTreeDict["#_size"] -= treeDict[child.path[0]]["#_size"]
                    downTreeDict["#_nrFiles"] -= treeDict[child.path[0]]["#_nrFiles"]
                for subChild in child.childItems:
                    for item in self.fileSystem.treeIterator(subChild):  # TODO: more efficient
                        if item.__itemType__() == 1:
                            if item.getCheckedState() == Qt.Unchecked:
                                if item.parentItem.getCheckedState() == Qt.Checked:
                                    folder = self.fileSystem.updateSizeAndFiles(downTreeDict, item.parentItem.path,
                                                                                item.size,
                                                                                item.nrFiles, -1)
                                    del folder[item.path[-1]]
                            elif item.parentItem.getCheckedState() == Qt.Unchecked:
                                folder = self.fileSystem.treeWalk(treeDict, item.path)
                                downTreeDict[os.path.join(*item.path)] = deepcopy(folder)
                                downTreeDict["#_size"] += item.size
                                downTreeDict["#_nrFiles"] += item.nrFiles
                        else:
                            if item.getCheckedState() == Qt.Unchecked:
                                if item.parentItem.getCheckedState() == Qt.Checked:
                                    folder = self.fileSystem.updateSizeAndFiles(downTreeDict, item.parentItem.path,
                                                                                item.size, 1, -1)
                                    for ind, file in enumerate(folder["#_files"]):  # TODO: better deletion
                                        if file["filename"] == item.fileName + item.extension:
                                            foundInd = ind
                                            break
                                    del folder["#_files"][foundInd]
                            elif item.parentItem.getCheckedState() == Qt.Unchecked:
                                folder = self.fileSystem.treeWalk(treeDict, item.parentItem.path)
                                for file in folder["#_files"]:
                                    if file["filename"] == item.fileName + item.extension:
                                        downTreeDict["<Files>"]["#_files"].append(
                                            {"filename": os.path.join(*(item.parentItem.path + [file["filename"]])),
                                             "#_size": file["#_size"]}
                                        )
                                        downTreeDict["<Files>"]["#_size"] += item.size
                                        downTreeDict["<Files>"]["#_nrFiles"] += 1
                                        break
            fileName = os.path.splitext(os.path.split(self.currentTreeFile)[-1])[0]
            if downTreeDict["#_size"] != 0:
                if downTreeDict.get("<Files>", None) is None:
                    downTreeDict["<Files>"] = {"#_size": 0, "#_nrFiles": 0, "#_files": []}
                with open(os.path.join(*[os.path.abspath("./files/downloads/"), fileName + "_down.json"]), "w") as jFileDown:
                    json.dump(downTreeDict, jFileDown)
        self.finished.emit()


# class PipeWorker(QtCore.QObject):
#     def __init__(self, pipeName=None, readBuffSize=8192):
#         super(PipeWorker, self).__init__()
#         self.pipeName = pipeName
#         self.readBuffSize = readBuffSize
#         self.pipe = None
#
#     def run(self):
#         self.pipe = ClientPipe(self.pipeName, self.readBuffSize)
#         self.pipe.connectPipe()
#         # print("Pipe was connected!")
#         try:
#             while True:
#                 message = self.pipe.readMessage()
#         except pywintypes.error as e:
#             if e.args[0] == 2:
#                 print("no pipe, trying again in a sec")
#                 time.sleep(1)
#             elif e.args[0] == 109:
#                 print("broken pipe, bye bye")


# class FilterWorker(QtCore.QObject):
#     def __init__(self, currentTreeFile: str, searchText: str):
#         super(FilterWorker, self).__init__()
#         self.treeFile = currentTreeFile
#         self.search = searchText.lower()
#
#     def __fullSearch(self, search: str, folder: dict):
#         newBranch = {"#_size": 0, "#_nrFiles": 0, "#_files": []}
#         for file in folder["#_files"]:
#             if search in file["filename"]:
#                 newBranch["#_files"].append(file)
#                 newBranch["#_size"] += file["#_size"]
#                 newBranch["#_nrFiles"] += 1
#         for subFold in folder.keys():
#             if subFold not in ["#_size", "#_nrFiles", "#_files"]:
#                 if search in subFold:
#                     newBranch[subFold] = copy.deepcopy(folder[subFold])
#                 else:
#                     branch = self.__fullSearch(search, folder[subFold])
#                     if branch["#_size"] != 0:
#                         newBranch[subFold] = branch
#                         newBranch["#_size"] += branch["#_size"]
#                         newBranch["#_nrFiles"] += branch["#_nrFiles"]
#         return newBranch
#
#     def run(self):
#         newDict = {"#_size": 0, "#_nrFiles": 0, "<Files>": {"#_size": 0, "#_nrFiles": 0, "#_files": []}}
#         with open(self.treeInput, "r") as treeFile:
#             treeDict = json.load(treeFile)
#         for file in treeDict["<Files>"]["#_files"]:
#             if self.search in file['filename']:
#                 newDict["<Files>"]["#_files"].append(file)
#                 newDict["<Files>"]["#_size"] += file["#_size"]
#                 newDict["<Files>"]["#_nrFiles"] += 1
#         for fold in treeDict.keys():
#             if fold not in ["#_size", "#_nrFiles", "<Files>"]:
#                 if self.search in fold:
#                     newDict[fold] = copy.deepcopy(treeDict[fold])
#                 else:
#                     branch = self.__fullSearch(self.search, treeDict[fold])
#                     if branch["#_size"] != 0:
#                         newDict[fold] = branch
#                 if newDict.get(fold, None) is not None:
#                     newDict["#_size"] += newDict[fold]["#_size"]
#                     newDict["#_nrFiles"] += newDict[fold]["#_nrFiles"]
#         return newDict
