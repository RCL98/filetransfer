from PyQt5.QtCore import Qt, QAbstractTableModel

from items import formatSize


class InconsistenciesTableModel(QAbstractTableModel):
    def __init__(self, parent=None, columns=None, inconsistencies=None):
        super(InconsistenciesTableModel, self).__init__(parent)
        if columns is None:
            columns = ["Item Name", "Problem", "Size Difference", "Nr of Files Difference"]
        assert inconsistencies is not None, "The inconsistencies parameter must contain a non-empty list!"

        self.columnNames = columns
        self.data = self.formatData(inconsistencies)

    def columnCount(self, parent=None):
        return len(self.columnNames)

    def rowCount(self, parent=None):
        return len(self.data)

    def headerData(self, section, orientation, role=None):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.columnNames[section]
        return None

    def data(self, index, role=None):
        if not index.isValid():
            return None

        if role == Qt.DisplayRole:
            return self.data[index.row()][index.column()]
        if role == Qt.TextAlignmentRole:
            if index.column() in [1, 2, 3]:
                return Qt.AlignVCenter + Qt.AlignHCenter
        else:
            return None

    @staticmethod
    def formatData(problems: list):
        formattedData = []
        for item in problems:
            sizeDiff, nrDiff, problem = "0 bytes", 0, item[1].upper()
            if item[1] == "szf":
                # problem = "File Size Different"
                sizeDiff = formatSize(item[2] - item[3])
            elif item[1] == 'szd':
                # problem = "Folder Size Different"
                sizeDiff = formatSize(item[2] - item[3])
            elif item[1] == 'nrd':
                # problem = 'Nr of Files Differs'
                nrDiff = item[2] - item[3]
            formattedData.append((item[0], problem, sizeDiff, nrDiff))
        # elif self.inconsistencies[itemIdx][1] == 'nef':
        #     problem = "Non-Existent File"
        # elif self.inconsistencies[itemIdx][1] == 'ned':
        #     problem = "Non-Existent Folder"
        return formattedData


class DownloadsTableModel(QAbstractTableModel):
    _RetrieveDownFile = Qt.UserRole + 5

    def __init__(self, parent=None, columns=None, downloadList=None):
        super(DownloadsTableModel, self).__init__(parent)
        if columns is None:
            columns = ["Name", "Size", "Progress", "Download Speed"]
        assert downloadList is not None, "The downloadList parameter must contain a non-empty list!"

        self.columnNames = columns
        self.tableData = downloadList

    def columnCount(self, parent=None):
        return len(self.columnNames)

    def rowCount(self, parent=None):
        return len(self.tableData)

    def headerData(self, section, orientation, role=None):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.columnNames[section]
        return None

    def data(self, index, role=None):
        if not index.isValid():
            return None

        if role == Qt.DisplayRole:
            return self.tableData[self.columnNames[index.column()]][index.row()]
        if role == Qt.TextAlignmentRole:
            if index.column() == 0:
                return Qt.AlignVCenter + Qt.AlignLeft
            return Qt.AlignVCenter + Qt.AlignHCenter
        if role == self._RetrieveDownFile:
            return self.tableData.iloc[index.row(), -1]
        else:
            return

    # def itemData(self, index: QModelIndex) -> typing.Dict[int, typing.Any]:
    #     if not index.isValid():
    #         return None



    @property
    def RetrieveDownFile(self):
        return self._RetrieveDownFile
