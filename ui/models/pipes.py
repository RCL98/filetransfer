import sys
import time

from win32ctypes.pywin32 import pywintypes
import win32file
import win32pipe
import winerror


class ServerPipe:
    def __init__(self, name=None, pipeBufferSize=65536, readBuffSize=8192):
        self.pipe_name = r"\\.\pipe\\" + name if name is not None else r"\\.\pipe\defaultPipe"
        self.pipe_buffer_size = pipeBufferSize
        self.read_buf = win32file.AllocateReadBuffer(readBuffSize)
        self.read_msg = None
        self.pipe_open = False
        self.pipe_handle = None

    def createPipe(self):
        if not self.pipe_open:
            self.pipe_handle = win32pipe.CreateNamedPipe(self.pipe_name, win32pipe.PIPE_ACCESS_DUPLEX,
                                                         win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_READMODE_MESSAGE | win32pipe.PIPE_WAIT,
                                                         1, self.pipe_buffer_size, self.pipe_buffer_size, 0, None)
            if self.pipe_handle == winerror.ERROR_INVALID_HANDLE:
                raise ValueError(self.pipe_name + " did not produce a valid pipe handle!")
            self.pipe_open = True
        return True

    def waitConnection(self):
        if self.pipe_open:
            try:
                result = win32pipe.ConnectNamedPipe(self.pipe_handle, None)
                if result == winerror.ERROR_IO_PENDING:
                    raise ValueError("Pending error!")
                # ERROR_IO_PENDING is normal
            except pywintypes.error as e:
                self.handleError(e.args[0])
                return False
            return True
        raise AssertionError("Pipe was not created!")

    def readMessage(self):
        result, data = win32file.ReadFile(self.pipe_handle, self.read_buf)
        self.read_msg = data.decode()
        while True:
            if result == winerror.ERROR_MORE_DATA:
                result, data = win32file.ReadFile(self.pipe_handle, self.read_buf)
                self.read_msg += data.decode()
                continue
            elif result == winerror.ERROR_SUCCESS:
                break
        return self.read_msg

    def sendMessage(self, message: str):
        try:
            message = str.encode(message)
            errCode, nBytes = win32file.WriteFile(self.pipe_handle, message)
            if errCode == winerror.ERROR_IO_PENDING:
                return nBytes
        except pywintypes.error as e:
            self.handleError(e.args[0])
            return 0
        return nBytes

    def closePipe(self):
        win32file.CloseHandle(self.pipe_handle)

    def handleError(self, result):
        reset_pipe = False
        if result == winerror.ERROR_BROKEN_PIPE:
            win32pipe.DisconnectNamedPipe(self.pipe_handle)
            reset_pipe = True
        elif result == winerror.ERROR_NO_DATA:
            reset_pipe = True

        if reset_pipe:
            self.pipe_handle = None
            self.pipe_open = False


class ClientPipe:
    def __init__(self, name=None, readBufferSize=8192):
        self.pipe_open = False
        self.pipe_handle = None
        self.pipe_name = r"\\.\pipe\\" + name if name is not None else r"\\.\pipe\defaultPipe"
        self.read_buf = win32file.AllocateReadBuffer(readBufferSize)
        self.read_msg = None

    def connectPipe(self):
        if not self.pipe_open:
            try:
                self.pipe_handle = win32file.CreateFile(self.pipe_name,
                                                        win32file.GENERIC_WRITE,  # win32file.GENERIC_READ |
                                                        0, None, win32file.OPEN_EXISTING,
                                                        0, None)
                win32pipe.SetNamedPipeHandleState(self.pipe_handle,
                                                  win32pipe.PIPE_READMODE_MESSAGE | win32pipe.PIPE_WAIT, None, None)
                self.pipe_open = True
                self.read_msg = None
            except pywintypes.error as e:
                self.handleError(e.args[0])
                return False
        return True

    def readMessage(self):
        result, data = win32file.ReadFile(self.pipe_handle, self.read_buf)
        self.read_msg = data.decode()
        while True:
            if result == winerror.ERROR_MORE_DATA:
                result, data = win32file.ReadFile(self.pipe_handle, self.read_buf)
                self.read_msg += data.decode()
                continue
            elif result == winerror.ERROR_SUCCESS:
                break
        return self.read_msg

    def sendMessage(self, message: str):
        try:
            message = str.encode(message)
            errCode, nBytes = win32file.WriteFile(self.pipe_handle, message)
            if errCode == winerror.ERROR_IO_PENDING:
                return nBytes
        except pywintypes.error as e:
            self.handleError(e.args[0])
            return 0
        return nBytes

    def closePipe(self):
        win32file.CloseHandle(self.pipe_handle)

    def handleError(self, result):
        reset_pipe = False
        if result == winerror.ERROR_BROKEN_PIPE:
            win32pipe.DisconnectNamedPipe(self.pipe_handle)
            reset_pipe = True
        elif result == winerror.ERROR_NO_DATA:
            reset_pipe = True

        if reset_pipe:
            self.pipe_handle = None
            self.pipe_open = False
            self.read_msg = None


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("need s or c as argument")
    elif sys.argv[1] == "s":
        # pipe_server()
        svp = ServerPipe("goPipe", 2048, 128)
        svp.createPipe()
        print("Pipe created!")
        svp.waitConnection()
        print("Client connected!")
        for i in range(1):
            smsg = f"MESSAGE1 MESSAGE2 MESSAGE3 MESSAGE4 MESSAGE5 MESSAGE6 MESSAGE7 MESSAGE8 MESSAGE9 MESSAGE10 MESSAGE11 MESSAGE12: {i}"
            nbyts = svp.sendMessage(smsg)
            print(nbyts)
            time.sleep(1)
            rmsg = svp.readMessage()
            print(f"RECEIVED: {rmsg}")

        svp.closePipe()
        print("Done server!")
    elif sys.argv[1] == "c":
        # pipe_client()
        clp = ClientPipe("goPipe", 16)
        clp.connectPipe()
        print("Pipe was connected!")
        try:
            while True:
                msg = clp.readMessage()
                print(f"RECEVIED: {msg}")
                time.sleep(1)
                smsg = f"Client message: received {msg}"
                n = clp.sendMessage(smsg)
                print(n)
        except pywintypes.error as er:
            if er.args[0] == 2:
                print("no pipe, trying again in a sec")
                time.sleep(1)
            elif er.args[0] == 109:
                print("broken pipe, bye bye")
    else:
        print(f"no can do: {sys.argv[1]}")
