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
        self.connectionId = 0
        self.lock = threading.Lock()
        self.runningExecutions = []
        self.executers = {}

    def sendMessage(self, message, requireVerbose=False, *, connId):
        """
        Sends a message to a specific connection.
        Args:
            message (str): The message to be sent.
            requireVerbose (bool, optional): Flag to indicate if the message should be printed.
                Defaults to False.
            connId (int): The ID of the connection to send the message to.
        Returns:
            None
        """
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
        """
        Retrieves a device from the `allDevices` dictionary based on the provided `scriptData['name']`.
        If the device is not found, it initializes the device using the `initialize` function and adds it to the `allDevices` dictionary.
        Parameters:
            scriptData (dict): The script data containing the device name.
            connId (int): The connection ID.
        Returns:
            Any: The device corresponding to the provided `scriptData['name']`.
        """
        if self.allDevices.get(scriptData['name']) is None:
            self.sendMessage(f'Device not found. Initializing...', True, connId=connId)
            ui = initialize(scriptData)
            self.allDevices[scriptData['name']] = ui
            self.sendMessage(f'Device initialized.', True, connId=connId)
        return self.allDevices[scriptData['name']]

    def processInstruction(self, scriptName, *, instruction = None, connId = None, allowExec = False, file = False):
        """
        Process an instruction by executing a script.

        Args:
            scriptName (str): The name of the script to execute.
            instruction (str, optional): The instruction to execute. Defaults to None.
            connId (int, optional): The connection ID. Defaults to None.
            allowExec (bool, optional): Whether to allow execution. Defaults to False.

        Returns:
            None

        Raises:
            SystemExit: If the script is not found.
        """
        print(file, type(file))
        if file == 'True':
            print(f'Using file: {scriptName}')
            scriptPath = scriptName
        else:
            scriptPath = findScript(scriptName)
        if scriptPath is None or not os.path.exists(scriptPath):
            self.sendMessage(f'Script {scriptName} not found.', connId=connId)
            exit(1)

        scriptData = readScript(scriptPath)
        allKeys = getAllKeys()
        
        def executeScript():
            self.runningExecutions.append([connId, instruction])
            ui = self.getDevice(scriptData, connId=connId)
            executer = Executer(parent=self, connId=connId, ui=ui, allKeys=allKeys, allowExec=allowExec)
            self.executers[connId] = executer
            executer.execute(scriptData)
            self.runningExecutions.remove([connId, instruction])
            self.executers.pop(connId)
            self.sendMessage(f'{instruction} end', connId=connId)
        
        executionThread = threading.Thread(target=executeScript)
        executionThread.start()

    def sessionServer(self, socketPath=serverAddress):
        """
        Start a session server that listens for incoming connections on the specified socket path.

        Parameters:
            socketPath (str): The path of the socket to listen on. Defaults to serverAddress.

        Returns:
            None

        Raises:
            OSError: If the socket path already exists and cannot be unlinked.

        Note:
            This function is typically called once to start the session server.
        """
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
                    self.connectionId += 1
                    connId = self.connectionId
                    self.connections[connId] = conn
                
                thread = threading.Thread(target=self.handleConnection, args=(connId,))
                thread.start()

    def handleConnection(self, connId):
        """
        This function handles a connection from a client. It receives instructions from the client and performs
        the corresponding actions.

        Args:
            connId (int): The connection ID.

        Returns:
            None

        Raises:
            None
        """
        try:
            conn = self.connections[connId]
            while True:
                instruction = conn.recv(1024).decode()
                if not instruction:
                    break
                print(f'Received instruction: {instruction}')

                if instruction == 'ping':
                    self.sendMessage(f'{instruction} end', connId=connId)

                elif instruction == 'kill':
                    self.sendMessage(f'{instruction} end', connId=connId)
                    break

                elif instruction.split('-')[0] == 'killExecution':
                    try:
                        executer = self.executers[int(instruction.split('-')[1])]
                        executer.stop()
                    except KeyError:
                        self.sendMessage(f'Execution {instruction.split("-")[1]} not found.', connId=connId)
                    except ValueError:
                        self.sendMessage(f'Invalid execution ID: {instruction.split("-")[1]}', connId=connId)
                    self.sendMessage(f'{instruction} end', connId=connId)

                elif instruction == 'listRunning':
                    for execution in self.runningExecutions:
                        self.sendMessage(f'{execution[0]}: {execution[1].split("-")[1]}', connId=connId)
                    self.sendMessage(f'{instruction} end', connId=connId)
                    
                elif instruction.split('-')[0] == 'execute':
                    scriptName = instruction.split('-')[1]
                    allowExec = instruction.split('-')[2]
                    self.verbose = instruction.split('-')[3]
                    file = instruction.split('-')[4]

                    self.processInstruction(scriptName, instruction=instruction, connId=connId, allowExec=bool(allowExec), file=file)

                else:
                    self.sendMessage(f'Unknown instruction: {instruction}', connId=connId)
                    self.sendMessage(f'{instruction} end', connId=connId)
        finally:
            with self.lock:
                conn = self.connections.pop(connId)
                conn.close()

if __name__ == "__main__":
    server = Svr()
    server.sessionServer()
