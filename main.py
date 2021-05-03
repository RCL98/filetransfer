import json
import sys

from PyQt5 import QtWidgets, QtCore

from eventTypes import UserTreeFileDispatchedEvent, pipeName
from ui.logic.StartWindowLogic import StartWindow
from ui.logic.MainWindowLogic import MainWindow
from ui.models.pipes import ClientPipe
from ui.models.workers import PipeClientWorker

import icons.icons


class AppInterface:
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.window = QtWidgets.QMainWindow()
        self.accepted = False
        self.startWindow = None
        self.mainWindow = None
        self.userName = None
        self.treeFile = None
        self.goClientProcces = None

        self.gotUserTreeFileEvent = UserTreeFileDispatchedEvent()
        # self.app.aboutToQuit.connect(self.closeApp)

    # def closeApp(self):
    #     if self.startWindow is None:
    #         closeMessage = json.dumps("packet_type: CLOSE_GO_CLIENT")
    #         print("DAAAA")
    #         try:
    #             pipe = ClientPipe(pipeName)
    #             pipe.connectPipe()
    #             pipe.sendMessage(closeMessage)
    #             pipe.closePipe()
    #         except Exception as e:
    #             print(e)

    def handleGoStdOutput(self):
        data = self.goClientProcces.readAllStandardOutput()
        stdout = bytes(data).decode("utf8")
        print(stdout)
        try:
            packeges = [pak.strip() for pak in stdout.split('\n') if len(pak) > 0]
            for pack in packeges:
                if pack[0] == '{':
                    print("IS PACKET")
                    packet = json.loads(pack.strip())
                    print(packet)
                    if packet['packet_type'] == 'RESPONSE_REQUEST_USER_FILE_STRUCTURE_PATH':
                        print("Send EVENT!")
                        self.gotUserTreeFileEvent.setData(packet["file_path"])
                        self.app.sendEvent(self.mainWindow, self.gotUserTreeFileEvent)
        except Exception as e:
            print(e)

    def handleGoError(self):
        data = self.goClientProcces.readAllStandardError()
        stderr = bytes(data).decode("utf8")
        print(stderr)

    @staticmethod
    def handleGoState(state):
        states = {
            QtCore.QProcess.NotRunning: 'Not running',
            QtCore.QProcess.Starting: 'Starting',
            QtCore.QProcess.Running: 'Running',
        }
        state_name = states[state]
        print(f"State changed: {state_name}")

    @staticmethod
    def goFinished():
        print("GO WAS TERMINATED")

    def activateGoClient(self):
        try:
            self.goClientProcces = QtCore.QProcess()
            # r'E:\GoProjects\GoPipes\main.exe', ['goPipe1']
            self.goClientProcces.start('go', ['run', r'E:\GoProjects\GoPipes\main.go', pipeName])  # 'go', ['run', r'E:\GoProjects\GoPipes\main.go', 'goPipe1']
            self.goClientProcces.readyReadStandardOutput.connect(self.handleGoStdOutput)
            self.goClientProcces.readyReadStandardError.connect(self.handleGoError)
            self.goClientProcces.stateChanged.connect(self.handleGoState)
            self.goClientProcces.finished.connect(self.goFinished)
        except Exception as e:
            print(e)

    def accept(self, acceptMessage: dict):
        self.userName, self.treeFile = acceptMessage['name'], acceptMessage['path_struct_data']
        acceptMessage = json.dumps(acceptMessage)  # json.dumps(acceptMessage)
        try:
            self.thread = QtCore.QThread()
            self.worker = PipeClientWorker(pipeName, acceptMessage)
            self.worker.moveToThread(self.thread)

            self.thread.started.connect(self.worker.run)
            self.worker.finished.connect(self.thread.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)

            self.thread.start()
        except Exception as e:
            print(e)
        self.accepted = True

    def startApp(self):
        self.activateGoClient()
        self.startWindow = StartWindow(self.window)
        self.startWindow.acceptState.connect(self.accept)
        self.window.showMaximized()
        resp = self.app.exec_()
        if resp == 0:
            if self.accepted:
                self.startWindow = None
                self.mainApp()
        else:
            raise Exception(f"Something bad happened to the starting window! {resp}")

    def mainApp(self):
        self.window = QtWidgets.QMainWindow()
        self.mainWindow = MainWindow(self.window)
        self.window.showMaximized()
        resp = self.app.exec_()


if __name__ == '__main__':
    try:
        app = AppInterface()
        app.startApp()
    except Exception as exc:
        print(exc)
