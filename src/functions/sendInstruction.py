import socket

HEADER_LENGTH = 10
SOCKET_PATH = '/tmp/taskZen.sock'

def sendInstruction(instruction: str, *, verbose: bool = True) -> None:
    """
    A function that sends an instruction over a Unix socket connection and recieves a response.

    Parameters:
        - instruction (str): The instruction to be sent.
        - verbose (bool, optional): Flag to indicate whether to print the response. Defaults to True.

    Returns:
        None
    """
    def receiveMessage(sock: socket.socket) -> str:
        header = sock.recv(HEADER_LENGTH).decode('utf-8')
        if not header:
            return None
        messageLength = int(header.strip())
        return sock.recv(messageLength).decode('utf-8')

    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
        socketPath = SOCKET_PATH
        s.connect(socketPath)
        message = f"{len(instruction):<{HEADER_LENGTH}}" + instruction
        s.sendall(message.encode())
        
        while True:
            response = receiveMessage(s)
            if response == 'end':
                break
            if verbose and response:
                print(response)
