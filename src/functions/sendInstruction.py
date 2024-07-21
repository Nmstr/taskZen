import socket

HEADER_LENGTH = 10
SOCKET_PATH = '/tmp/taskZen.sock'

def sendInstruction(instruction: str) -> None:
    """
    A function that sends an instruction over a Unix socket connection and recieves a response.

    Parameters:
        - instruction (str): The instruction to be sent.

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
        try:
            s.connect(socketPath)
            message = f"{len(instruction):<{HEADER_LENGTH}}" + instruction
            s.sendall(message.encode())
        except (ConnectionRefusedError, FileNotFoundError) as e:
            print('Error contacting server')
            print('Did you start the server?')
            print(f'\nError: {e}')
            exit(1)
        
        while True:
            response = receiveMessage(s)
            print(response)
            if response == 'end':
                break
