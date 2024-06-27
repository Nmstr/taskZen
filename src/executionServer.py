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
        self.connections = {}
        self.connection_id = 0
        self.lock = threading.Lock()

    def sendMessage(self, message, requireVerbose=False, *, connId):
        if requireVerbose and self.verbose == 'False':
            print(f'withheld message: {message}')
            return
        message = str(message)
        messageLength = len(message)
        header = f"{messageLength:<{HEADER_LENGTH}}".encode('utf-8')
        with self.lock:
            conn = self.connections[connId]
            conn.sendall(header + message.encode('utf-8'))
        print(message)

    def getDevice(self, scriptData, *, connId):
        if self.allDevices.get(scriptData['name']) is None:
            self.sendMessage(f'Device not found. Initializing...', True, connId=connId)
            ui = initialize(scriptData)
            self.allDevices[scriptData['name']] = ui
            self.sendMessage(f'Device initialized.', True, connId=connId)
        return self.allDevices[scriptData['name']]

    def processInstruction(self, scriptName, *, instruction = None, connId = None, allowExec = False):
        scriptPath = findScript(scriptName)
        if scriptPath is None or not os.path.exists(scriptPath):
            self.sendMessage(f'Script {scriptName} not found.')
            exit(1)

        scriptData = readScript(scriptPath)
        allKeys = getAllKeys()
        
        def executeScript():
            ui = self.getDevice(scriptData, connId=connId)
            executer = Executer(parent=self, connId=connId, ui=ui, allKeys=allKeys, allowExec=allowExec)
            executer.execute(scriptData)
            self.sendMessage(f'{instruction} end', connId=connId)
        
        executionThread = threading.Thread(target=executeScript)
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
                conn, addr = s.accept()
                with self.lock:
                    self.connection_id += 1
                    connId = self.connection_id
                    self.connections[connId] = conn
                
                thread = threading.Thread(target=self.handleConnection, args=(connId,))
                thread.start()

    def handleConnection(self, connId):
        try:
            conn = self.connections[connId]
            while True:
                instruction = conn.recv(1024).decode()
                if not instruction:
                    break
                print(f'Received instruction: {instruction}')

                if instruction == 'ping':
                    self.sendMessage(f'{instruction} end', connId)

                elif instruction == 'kill':
                    self.sendMessage(f'{instruction} end', connId)
                    break
                    
                elif instruction.split('-')[0] == 'execute':
                    scriptName = instruction.split('-')[1]
                    allowExec = instruction.split('-')[2]
                    self.verbose = instruction.split('-')[3]

                    self.processInstruction(scriptName, instruction=instruction, connId=connId, allowExec=bool(allowExec))

                else:
                    self.sendMessage(f'Unknown instruction: {instruction}', connId)
                    self.sendMessage(f'{instruction} end', connId)
        finally:
            with self.lock:
                conn = self.connections.pop(connId)
                conn.close()

if __name__ == "__main__":
    server = Svr()
    server.sessionServer()
