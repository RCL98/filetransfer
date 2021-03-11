import json
from os.path import splitext

from PyQt5.QtCore import Qt

def formatSize(size: int) -> str:
    sizeString = ""
    if size < 1024:
        sizeString = f"{size:.2f} bytes"
    elif size >= 1024 and size < 1024 ** 2:
        sizeString = f"{size / 1024:.2f} KB"
    elif size >= 1024 ** 2 and size < 1024 ** 3:
        sizeString = f"{size / 1024 ** 2:.2f} MB"
    elif size >= 1024 ** 4 and size < 1024 ** 5:
        sizeString = f"{size / 1024 ** 3:.2f} GB"
    else:
        sizeString = f"{size / 1024 ** 4:.2f} TB"
    return sizeString

class FileItem:
    def __init__(self, filename, size, parent=None):
        self.parentItem = parent
        self.fileName, self.extension = splitext(filename)
        self.size = size
        self.checkedState = False

    @staticmethod
    def childCount():
        return 0

    @staticmethod
    def columnCount():
        return 4

    def data(self, column):
        if column == 0:
            if '\\' in self.fileName:
                return self.fileName.rsplit('\\', 1)[1]
            return self.fileName
        elif column == 1:
            return self.extension
        elif column == 2:
            return formatSize(self.size)
        else:
            return "1 file"

    def parent(self):
        return self.parentItem

    def row(self):
        return self.parentItem.childItems.index(self)

    def toolTip(self, column):
        if column == 0:
            return '\\'.join(self.parentItem.path + [self.fileName])
        elif column == 1:
            return self.extension
        elif column == 2:
            return f"{self.size:,} bytes"
        else:
            return "1 file"

    def setCheckedState(self, value):
        selectedItems = 0
        if value == 2:
            self.checkedState = True
            selectedItems += 1
        else:
            self.checkedState = False
            selectedItems -= 1
        return selectedItems
        # return '/'.join(self.parentItem.path) + '/' + self.itemData[0] + self.itemData[1]

    def getCheckedState(self):
        if self.checkedState:
            return Qt.Checked
        else:
            return Qt.Unchecked

    def __itemType__(self):
        return 0


class FolderItem:
    def __init__(self, path=None, parent=None, treeInput=None):
        if path is None:
            path = []
        self.treeInput = treeInput
        self.parentItem = parent
        self.path = path
        self.size = 0
        self.type = 'File folder'
        self.nrFiles = 0
        self.checkedState = False
        self.childItems = []

        if self.path:
            folder_content = self.get_dict_from_path()
            if folder_content.get('#_files', False):
                self.n_children = len(
                    folder_content['#_files']) + len(folder_content) - 3
            else:
                self.n_children = len(folder_content)
                self.n_children = self.n_children - 2 if folder_content.get('#_files', False) == False else self.n_children - 3 # TODO: more efficient
            self.size = folder_content['size']
            self.nrFiles = folder_content['nrFiles']
        else:
            with open(self.treeInput, "r") as jFile:  # TODO: handle files at root level
                self.n_children = len(json.load(jFile)) - 2

        self.is_loaded = False

    def get_dict_from_path(self):
        with open(self.treeInput, "r") as jFile:
            current_level = json.load(jFile)
            for folder in self.path:
                current_level = current_level[folder]
            return current_level

    def load_children(self):
        self.childItems = []
        selectedItems = 0
        if self.path:
            child_dirs = []
            folder_content = self.get_dict_from_path()
            for folder in folder_content.keys():
                if folder == '#_files':
                    for file in folder_content['#_files']:
                        fileItem = FileItem(file['filename'], file['size'], parent=self)
                        if self.getCheckedState() == Qt.Checked:
                            fileItem.setCheckedState(2)
                            selectedItems += 1
                        self.childItems.append(fileItem)
                elif folder != 'size' and folder != 'nrFiles':
                    child_dirs.append(folder)
        else:  # special case of root node. TODO: handle files at root level
            with open(self.treeInput, "r") as jFile:
                child_dirs = json.load(jFile).keys()

        for child_dir in child_dirs:
            if child_dir != 'size' and child_dir != 'nrFiles':
                child_path = self.path + [child_dir]
                folderItem = FolderItem(path=child_path, parent=self, treeInput=self.treeInput)
                if self.getCheckedState() == Qt.Checked:
                    folderItem.setCheckedState(2)
                    selectedItems += 1
                self.childItems.append(folderItem)
        self.is_loaded = True
        return selectedItems

    def child(self, row):
        return self.childItems[row]

    def childCount(self):
        return self.n_children

    def isEpanded(self):
        return self.is_loaded == True

    def __itemType__(self):
        return 1

    @staticmethod
    def columnCount():
        return 4

    def setCheckedState(self, value):
        selectedItems = 0
        if value == 2:
            self.checkedState = True
            selectedItems += 1
        else:
            self.checkedState = False
            selectedItems -= 1
        for child in self.childItems:
            if child.getCheckedState() != self.getCheckedState():
                selectedItems += child.setCheckedState(value)
        return selectedItems
        #return '/'.join(self.path)

    def toolTip(self, column):
        if column == 0:
            return '\\'.join(self.path)
        elif column == 1:
            return "FileFolder"
        elif column == 2:
            return f"{self.size:,} bytes"
        else:
            return f"{self.nrFiles:,} files"

    def getCheckedState(self):
        if self.checkedState:
            return Qt.Checked
        else:
            return Qt.Unchecked

    def data(self, column):
        if column == 0 and self.path:
            if '\\' in self.path[-1]:
                return self.path[-1].rsplit('\\', 1)[1]
            return self.path[-1]
        elif column == 1:
            return self.type
        elif column == 2:
            return formatSize(self.size)
        elif column == 3:
            return f"{self.nrFiles:,} files"
        else:
            return None

    def parent(self):
        return self.parentItem

    def row(self):
        if self.parentItem:
            return self.parentItem.childItems.index(self)
        return 0

