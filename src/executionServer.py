from initialize import initialize, readScript, findScript, getAllKeys
from executer import Executer
import socket
import os

serverAddress = '/tmp/taskZen_socket'
HEADER_LENGTH = 10

class Svr:
    def __init__(self):
        self.allDevices = {}

    def sendMessage(self, message):
        # Prepend the length of the message as a fixed-size header
        messageLength = len(message)
        header = f"{messageLength:<{HEADER_LENGTH}}".encode('utf-8')
        self.conn.sendall(header + message.encode('utf-8'))

    def getDevice(self, scriptData):
        if self.allDevices.get(scriptData['name']) is None:
            ui = initialize(scriptData)
            self.allDevices[scriptData['name']] = ui
        return self.allDevices[scriptData['name']]

    def processInstruction(self, instruction):
        scriptPath = findScript(instruction)
        if scriptPath is None or not os.path.exists(scriptPath):
            print(f'Script {instruction} not found.')
            exit(1)

        scriptData = readScript(scriptPath)
        allKeys = getAllKeys()
        ui = self.getDevice(scriptData)
        allowExec = False
        
        self.sendMessage('test')
        executer = Executer(ui=ui, allKeys=allKeys, verbose=True, allowExec=allowExec)
        executer.execute(scriptData)
        self.sendMessage('test')

        return instruction

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
                    if instruction == 'ping':
                        self.sendMessage('end')
                    elif instruction == 'kill':
                        self.sendMessage('end')
                        break
                    else:
                        response = self.processInstruction(instruction)
                        self.sendMessage(response)
                        self.sendMessage('end')

if __name__ == "__main__":
    server = Svr()
    server.sessionServer()
