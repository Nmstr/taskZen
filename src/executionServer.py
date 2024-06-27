from initialize import initialize, readScript, findScript, getAllKeys
from executer import Executer
import threading
import socket
import os

serverAddress = '/tmp/taskZen_socket'
HEADER_LENGTH = 10

class Svr:
    def __init__(self):
        self.allDevices = {}
        self.verbose = False

    def sendMessage(self, message, requireVerbose=False):
        if requireVerbose and self.verbose == 'False':
            print(f'withheld message: {message}')
            return
        message = str(message)
        messageLength = len(message)
        header = f"{messageLength:<{HEADER_LENGTH}}".encode('utf-8')
        self.conn.sendall(header + message.encode('utf-8'))
        print(message)

    def getDevice(self, scriptData):
        if self.allDevices.get(scriptData['name']) is None:
            self.sendMessage(f'Device not found. Initializing...', True)
            ui = initialize(scriptData)
            self.allDevices[scriptData['name']] = ui
            self.sendMessage(f'Device initialized.', True)
        return self.allDevices[scriptData['name']]

    def processInstruction(self, scriptName, *, allowExec = False):
        scriptPath = findScript(scriptName)
        if scriptPath is None or not os.path.exists(scriptPath):
            self.sendMessage(f'Script {scriptName} not found.')
            exit(1)

        scriptData = readScript(scriptPath)
        allKeys = getAllKeys()
        ui = self.getDevice(scriptData)
        
        executer = Executer(parent=self, ui=ui, allKeys=allKeys, allowExec=allowExec)
        executionThread = threading.Thread(target=executer.execute, args=(scriptData,))
        executionThread.start()

        return 'Done'

    def sessionServer(self, socketPath=serverAddress):
        # Make sure the socket does not already exist
        try:
            os.unlink(socketPath)
        except OSError:
            if os.path.exists(socketPath):
                raise

        print(f"Listening on {socketPath}")
        
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
            s.bind(socketPath)
            s.listen()
            while True:
                self.conn, addr = s.accept()
                with self.conn:
                    instruction = self.conn.recv(1024).decode()
                    print(f'Received instruction: {instruction}')

                    if instruction == 'ping':
                        self.sendMessage('end')

                    elif instruction == 'kill':
                        self.sendMessage('end')
                        break
                    
                    elif instruction.split('-')[0] == 'execute':
                        scriptName = instruction.split('-')[1]
                        allowExec = instruction.split('-')[2]
                        self.verbose = instruction.split('-')[3]

                        response = self.processInstruction(scriptName, allowExec=bool(allowExec))
                        self.sendMessage(response)
                        self.sendMessage('end')

                    else:
                        self.sendMessage(f'Unknown instruction: {instruction}')
                        self.sendMessage('end')

if __name__ == "__main__":
    server = Svr()
    server.sessionServer()
