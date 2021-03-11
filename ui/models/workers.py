import json
import os
from copy import deepcopy

from PyQt5 import QtCore
from PyQt5.QtCore import Qt

from ui.models.treeModel import FileSystem, TreeModelFile


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
        self.fileSystem.statusBarMessage.connect(self.sendMessage)
        self.fileSystem.progressBarValue.connect(self.sendValue)

    def sendMessage(self, message):
        self.statusBarMessage.emit(message)

    def sendValue(self, value):
        self.progressBarValue.emit(value)

    def run(self):
        try:
            with open(self.currentTreeFile, "r") as jFile:
                originalDict = json.load(jFile)
        except json.JSONDecodeError:
            originalDict = {
                "<Files>": {"#_files": [], "size": 0, "nrFiles": 0},
                "size": 0,
                "nrFiles": 0,
            }

        copyDict = deepcopy(originalDict)
        selectedItems = self.selectedItems
        selectedLength = len(selectedItems['#_files']) + len(selectedItems['#_folders'])
        progress = 1
        for folder in selectedItems["#_folders"]:
            self.statusBarMessage.emit('Adding: ' + folder)
            self.progressBarValue.emit(int(progress / selectedLength * 100))
            progress += 1
            it = 0
            while it < len(copyDict["<Files>"]["#_files"]):
                if copyDict["<Files>"]["#_files"][it]["filename"].find(folder) != -1:
                    copyDict["<Files>"]["size"] -= copyDict["<Files>"]["#_files"][it]["size"]
                    copyDict["<Files>"]["nrFiles"] -= 1
                    del copyDict["<Files>"]["#_files"][it]
                else:
                    it += 1
            folderDict = self.fileSystem.getFileStructure(folder, withSize=True)
            finalDict = folderDict
            for key in copyDict.copy().keys():
                if key in ["size", "nrFiles", "<Files>"]:
                    continue
                if key == folder:
                    copyDict["size"] -= copyDict[key]["size"]
                    copyDict["nrFiles"] -= copyDict[key]["nrFiles"]
                elif folder.find(key) != -1:
                    try:
                        folderCopy = {key: deepcopy(copyDict[key])}
                        keys = [k for k in folder[len(key) + 1:].split("\\")[:-1] if k]
                        folderIterator = self.fileSystem.updateSizeAndFiles(folderCopy[key], keys,
                                                                            folderDict[folder]["size"],
                                                                            folderDict[folder]["nrFiles"])
                        foldKey = folder.rsplit("\\", 1)[1]
                        if foldKey in folderIterator.keys():
                            copyDict["size"] -= folderIterator[foldKey]["size"]
                            copyDict["nrFiles"] -= folderIterator[foldKey]["nrFiles"]
                            self.fileSystem.updateSizeAndFiles(folderCopy[key], keys,
                                                               folderIterator[foldKey]["size"],
                                                               folderIterator[foldKey]["nrFiles"], -1)
                        folderIterator.update(folderDict)
                        folderIterator[foldKey] = folderIterator.pop(folder)
                        finalDict = folderCopy
                    except KeyError:
                        pass
                elif key.find(folder) != -1:
                    copyDict["size"] -= copyDict[key]["size"]
                    copyDict["nrFiles"] -= copyDict[key]["nrFiles"]
                    del copyDict[key]
                    if key in finalDict.keys():
                        del finalDict[key]
            copyDict["size"] += folderDict[folder]["size"]
            copyDict["nrFiles"] += folderDict[folder]["nrFiles"]
            copyDict.update(finalDict)

        if selectedItems["#_files"]:
            existingFiles = {f["filename"]: (f["size"], idx) for idx, f in
                             enumerate(copyDict["<Files>"]["#_files"])}
            for file in selectedItems["#_files"]:
                self.statusBarMessage.emit('Adding: ' + file)
                self.progressBarValue.emit(int(progress / selectedLength * 100))
                progress += 1
                fileSize = os.stat(file).st_size
                try:
                    size, idx = existingFiles[file]
                    if size != fileSize:
                        copyDict["<Files>"]["size"] += fileSize - size
                        copyDict["size"] += fileSize - size
                        copyDict["<Files>"]["#_files"][idx]["size"] = fileSize
                except KeyError:
                    copyDict["<Files>"]["size"] += fileSize
                    copyDict["<Files>"]["nrFiles"] += 1
                    copyDict["<Files>"]["#_files"].append({"filename": file, "size": fileSize})
                    copyDict["size"] += fileSize
                    copyDict["nrFiles"] += 1

        with open(self.currentTreeFile, "w") as jFile:
            json.dump(copyDict, jFile)

        with open("..\\files\\temp\\userTreeTemp" + str(self.actionsStackSize) + ".json", "w") as jFileTemp:
            json.dump(originalDict, jFileTemp)
            self.stackAdd.emit(jFileTemp.name)
        self.statusBarMessage.emit('Ready')
        self.progressBarValue.emit(0)
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
            newTreeDict = {"size": treeDict["size"], "nrFiles": treeDict["nrFiles"]}
            selectedLength, progress = self.fileTreeModel.selectLength(), 1
            for child in self.fileTreeModel.getRootItem().childItems:
                if child.getCheckedState() == Qt.Unchecked:
                    newTreeDict[child.path[0]] = deepcopy(treeDict[child.path[0]])
                else:
                    self.statusBarMessage.emit('Deleting: ' + '/'.join(child.path))
                    self.progressBarValue.emit(int(progress / selectedLength * 100))
                    progress += 1
                    newTreeDict["size"] -= treeDict[child.path[0]]["size"]
                    newTreeDict["nrFiles"] -= treeDict[child.path[0]]["nrFiles"]
                for subChild in child.childItems:
                    for item in self.fileSystem.treeIterator(subChild):  # TODO: more efficient
                        if item.__itemType__() == 1:
                            if item.getCheckedState() == Qt.Checked:
                                self.statusBarMessage.emit('Deleting: ' + '\\'.join(item.path))
                                self.progressBarValue.emit(int(progress / selectedLength * 100))
                                progress += 1
                                if item.parentItem.getCheckedState() == Qt.Unchecked:
                                    folder = self.fileSystem.updateSizeAndFiles(newTreeDict, item.parentItem.path,
                                                                                item.size,
                                                                                item.nrFiles, -1)
                                    del folder[item.path[-1]]
                            elif item.parentItem.getCheckedState() == Qt.Checked:
                                folder = self.fileSystem.treeWalk(treeDict, item.path)
                                newTreeDict["\\".join(item.path)] = deepcopy(folder)
                                newTreeDict["size"] += item.size
                                newTreeDict["nrFiles"] += item.nrFiles
                        else:
                            if item.getCheckedState() == Qt.Checked:
                                self.statusBarMessage.emit('Deleting: ' + item.fileName + item.extension)
                                self.progressBarValue.emit(progress / selectedLength * 100)
                                progress += 1
                                if item.parentItem.getCheckedState() == Qt.Unchecked:
                                    folder = self.fileSystem.updateSizeAndFiles(newTreeDict, item.parentItem.path,
                                                                                item.size, 1, -1)
                                    for ind, file in enumerate(folder["#_files"]):  # TODO: better deletion
                                        if file["filename"] == item.fileName + item.extension:
                                            foundInd = ind
                                            break
                                    del folder["#_files"][foundInd]
                            elif item.parentItem.getCheckedState() == Qt.Checked:
                                folder = self.fileSystem.treeWalk(treeDict, item.parentItem.path)
                                for file in folder["#_files"]:
                                    if file["filename"] == item.fileName + item.extension:
                                        newTreeDict["<Files>"]["#_files"].append(
                                            {"filename": "\\".join(item.parentItem.path + [file["filename"]]),
                                             "size": file["size"]}
                                        )
                                        newTreeDict["<Files>"]["size"] += item.size
                                        newTreeDict["<Files>"]["nrFiles"] += 1
                                        break
            with open("..\\files\\temp\\userTreeTemp" + str(self.actionsStackSize) + ".json", "w") as jFileTemp:
                json.dump(treeDict, jFileTemp)
                self.stackAdd.emit(jFileTemp.name)
            jFile.seek(0)
            jFile.truncate()
            json.dump(newTreeDict, jFile)
        self.statusBarMessage.emit('Ready')
        self.progressBarValue.emit(0)
        self.finished.emit()

    # def addAction(self):
    #     fileDialog = FileDialog()
    #     if fileDialog.exec_() == QtWidgets.QDialog.Accepted:  # TODO: Deal with rejected items.
    #         try:
    #             try:
    #                 with open(self.currentTreeFile, "r") as jFile:
    #                     originalDict = json.load(jFile)
    #             except json.JSONDecodeError:
    #                 originalDict = {
    #                     "<Files>": {"#_files": [], "size": 0, "nrFiles": 0},
    #                     "size": 0,
    #                     "nrFiles": 0,
    #                 }
    #
    #             copyDict = deepcopy(originalDict)
    #             selectedItems = fileDialog.selectedFiles()
    #             selectedLength = len(selectedItems['#_files']) + len(selectedItems['#_folders'])
    #             progress = 1
    #             for folder in selectedItems["#_folders"]:
    #                 self.statusBar.showMessage('Adding: ' + folder)
    #                 print(int(progress / selectedLength * 100), progress / selectedLength * 100)
    #                 self.progressBar.setValue(int(progress / selectedLength * 100))
    #                 progress += 1
    #                 it = 0
    #                 while it < len(copyDict["<Files>"]["#_files"]):
    #                     if copyDict["<Files>"]["#_files"][it]["filename"].find(folder) != -1:
    #                         copyDict["<Files>"]["size"] -= copyDict["<Files>"]["#_files"][it]["size"]
    #                         copyDict["<Files>"]["nrFiles"] -= 1
    #                         del copyDict["<Files>"]["#_files"][it]
    #                     else:
    #                         it += 1
    #                 folderDict = self.fileSystem.getFileStructure(folder, withSize=True)
    #                 finalDict = folderDict
    #                 for key in copyDict.copy().keys():
    #                     if key in ["size", "nrFiles", "<Files>"]:
    #                         continue
    #                     if key == folder:
    #                         copyDict["size"] -= copyDict[key]["size"]
    #                         copyDict["nrFiles"] -= copyDict[key]["nrFiles"]
    #                     elif folder.find(key) != -1:
    #                         try:
    #                             folderCopy = {key: deepcopy(copyDict[key])}
    #                             keys = [k for k in folder[len(key) + 1:].split("\\")[:-1] if k]
    #                             folderIterator = self.fileSystem.updateSizeAndFiles(folderCopy[key], keys,
    #                                                                                 folderDict[folder]["size"],
    #                                                                                 folderDict[folder]["nrFiles"])
    #                             foldKey = folder.rsplit("\\", 1)[1]
    #                             if foldKey in folderIterator.keys():
    #                                 copyDict["size"] -= folderIterator[foldKey]["size"]
    #                                 copyDict["nrFiles"] -= folderIterator[foldKey]["nrFiles"]
    #                                 self.fileSystem.updateSizeAndFiles(folderCopy[key], keys,
    #                                                                    folderIterator[foldKey]["size"],
    #                                                                    folderIterator[foldKey]["nrFiles"], -1)
    #                             folderIterator.update(folderDict)
    #                             folderIterator[foldKey] = folderIterator.pop(folder)
    #                             finalDict = folderCopy
    #                         except KeyError:
    #                             pass
    #                     elif key.find(folder) != -1:
    #                         copyDict["size"] -= copyDict[key]["size"]
    #                         copyDict["nrFiles"] -= copyDict[key]["nrFiles"]
    #                         del copyDict[key]
    #                         if key in finalDict.keys():
    #                             del finalDict[key]
    #                 copyDict["size"] += folderDict[folder]["size"]
    #                 copyDict["nrFiles"] += folderDict[folder]["nrFiles"]
    #                 copyDict.update(finalDict)
    #
    #             if selectedItems["#_files"]:
    #                 existingFiles = {f["filename"]: (f["size"], idx) for idx, f in
    #                                  enumerate(copyDict["<Files>"]["#_files"])}
    #                 for file in selectedItems["#_files"]:
    #                     self.statusBar.showMessage('Adding: ' + file)
    #                     self.progressBar.setValue(int(progress / selectedLength * 100))
    #                     progress += 1
    #                     fileSize = os.stat(file).st_size
    #                     try:
    #                         size, idx = existingFiles[file]
    #                         if size != fileSize:
    #                             copyDict["<Files>"]["size"] += fileSize - size
    #                             copyDict["size"] += fileSize - size
    #                             copyDict["<Files>"]["#_files"][idx]["size"] = fileSize
    #                     except KeyError:
    #                         copyDict["<Files>"]["size"] += fileSize
    #                         copyDict["<Files>"]["nrFiles"] += 1
    #                         copyDict["<Files>"]["#_files"].append({"filename": file, "size": fileSize})
    #                         copyDict["size"] += fileSize
    #                         copyDict["nrFiles"] += 1
    #
    #             with open(self.currentTreeFile, "w") as jFile:
    #                 json.dump(copyDict, jFile)
    #             self.renderTree()
    #
    #             with open("..\\files\\temp\\userTreeTemp" + str(len(self.undoStack)) + ".json", "w") as jFileTemp:
    #                 json.dump(originalDict, jFileTemp)
    #                 self.undoStack.append(jFileTemp.name)
    #
    #         except Exception as e:
    #             print(e)
    #         time.sleep(1)
    #         self.statusBar.showMessage('Ready')
    #         self.progressBar.setValue(0)

    # def deleteAction(self):
    #     try:
    #         with open(self.currentTreeFile, "r+") as jFile:
    #             treeDict = json.load(jFile)
    #             newTreeDict = {"size": treeDict["size"], "nrFiles": treeDict["nrFiles"]}
    #             selectedLength, progress = self.fileTreeModel.selectLength(), 1
    #             for child in self.fileTreeModel.getRootItem().childItems:
    #                 if child.getCheckedState() == Qt.Unchecked:
    #                     newTreeDict[child.path[0]] = deepcopy(treeDict[child.path[0]])
    #                 else:
    #                     self.statusBar.showMessage('Deleting: ' + '/'.join(child.path))
    #                     self.progressBar.setValue(int(progress / selectedLength * 100))
    #                     progress += 1
    #                     newTreeDict["size"] -= treeDict[child.path[0]]["size"]
    #                     newTreeDict["nrFiles"] -= treeDict[child.path[0]]["nrFiles"]
    #                 for subChild in child.childItems:
    #                     for item in self.fileSystem.treeIterator(subChild):  # TODO: more efficient
    #                         if item.__itemType__() == 1:
    #                             if item.getCheckedState() == Qt.Checked:
    #                                 self.statusBar.showMessage('Deleting: ' + '\\'.join(item.path))
    #                                 self.progressBar.setValue(int(progress / selectedLength * 100))
    #                                 progress += 1
    #                                 if item.parentItem.getCheckedState() == Qt.Unchecked:
    #                                     folder = self.fileSystem.updateSizeAndFiles(newTreeDict, item.parentItem.path,
    #                                                                                 item.size,
    #                                                                                 item.nrFiles, -1)
    #                                     del folder[item.path[-1]]
    #                             elif item.parentItem.getCheckedState() == Qt.Checked:
    #                                 folder = self.fileSystem.treeWalk(treeDict, item.path)
    #                                 newTreeDict["\\".join(item.path)] = deepcopy(folder)
    #                                 newTreeDict["size"] += item.size
    #                                 newTreeDict["nrFiles"] += item.nrFiles
    #                         else:
    #                             if item.getCheckedState() == Qt.Checked:
    #                                 self.statusBar.showMessage('Deleting: ' + item.fileName + item.extension)
    #                                 self.progressBar.setValue(progress / selectedLength * 100)
    #                                 progress += 1
    #                                 if item.parentItem.getCheckedState() == Qt.Unchecked:
    #                                     folder = self.fileSystem.updateSizeAndFiles(newTreeDict, item.parentItem.path,
    #                                                                                 item.size, 1, -1)
    #                                     for ind, file in enumerate(folder["#_files"]):  # TODO: better deletion
    #                                         if file["filename"] == item.fileName + item.extension:
    #                                             foundInd = ind
    #                                             break
    #                                     del folder["#_files"][foundInd]
    #                             elif item.parentItem.getCheckedState() == Qt.Checked:
    #                                 folder = self.fileSystem.treeWalk(treeDict, item.parentItem.path)
    #                                 for file in folder["#_files"]:
    #                                     if file["filename"] == item.fileName + item.extension:
    #                                         newTreeDict["<Files>"]["#_files"].append(
    #                                             {"filename": "\\".join(item.parentItem.path + [file["filename"]]),
    #                                              "size": file["size"]}
    #                                         )
    #                                         newTreeDict["<Files>"]["size"] += item.size
    #                                         newTreeDict["<Files>"]["nrFiles"] += 1
    #                                         break
    #             with open("..\\files\\temp\\userTreeTemp" + str(len(self.undoStack)) + ".json", "w") as jFileTemp:
    #                 json.dump(treeDict, jFileTemp)
    #                 self.undoStack.append(jFileTemp.name)
    #             jFile.seek(0)
    #             jFile.truncate()
    #             json.dump(newTreeDict, jFile)
    #         self.renderTree()
    #     except Exception as e:
    #         print(e)
    #     time.sleep(1)
    #     self.statusBar.showMessage('Ready')
    #     self.progressBar.setValue(0)
