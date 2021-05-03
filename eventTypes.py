from PyQt5 import QtCore

pipeName = "goPipe38"


class UserTreeFileDispatchedEvent(QtCore.QEvent):
    idType = QtCore.QEvent.registerEventType()

    def __init__(self, data=None):
        super(UserTreeFileDispatchedEvent, self).__init__(UserTreeFileDispatchedEvent.idType)
        self.data = UserTreeFileDispatchedEvent.idType if data is None else data
        print("UserTreeFileDispatchedEvent.idType ", UserTreeFileDispatchedEvent.idType)

    def setData(self, inputData: str):
        self.data = inputData

    def getData(self):
        return self.data


class UsersListDispatchedEvent(QtCore.QEvent):
    idType = QtCore.QEvent.registerEventType()

    def __init__(self, data=None):
        super(UsersListDispatchedEvent, self).__init__(UsersListDispatchedEvent.idType)
        self.data = UsersListDispatchedEvent.idType if data is None else data
        print("UsersListDispatchedEvent.idType ", UsersListDispatchedEvent.idType)

    def setData(self, inputData: str):
        self.data = inputData

    def getData(self):
        return self.data
