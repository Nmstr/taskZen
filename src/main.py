from initialize import readScript, findScript, scriptContainsExec
import argparse
import socket
import shutil
import yaml
import json
import os

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

def checkConfig() -> None:
    configDir = os.getenv('XDG_CONFIG_HOME', default=os.path.expanduser('~/.config')) + '/taskZen/'
    os.makedirs(configDir, exist_ok=True)
    os.makedirs(configDir + 'scripts/', exist_ok=True)
    os.makedirs(configDir + 'devices/', exist_ok=True)
    currentPath = f'{os.path.dirname(os.path.realpath(__file__))}'
    for script in os.listdir(currentPath + '/../examples/scripts'):
        if not os.path.exists(configDir + 'scripts/' + script):
            shutil.copyfile(currentPath + '/../examples/scripts/' + script, configDir + 'scripts/' + script)
    for device in os.listdir(currentPath + '/../examples/devices'):
        if not os.path.exists(configDir + 'devices/' + device):
            shutil.copyfile(currentPath + '/../examples/devices/' + device, configDir + 'devices/' + device)

def main() -> None:
    scriptDir = os.getenv('XDG_CONFIG_HOME', default=os.path.expanduser('~/.config')) + '/taskZen/scripts/'
    if not os.path.exists(scriptDir):
        os.makedirs(scriptDir, exist_ok=True)

    parser = argparse.ArgumentParser(prog='taskZen', description='Automation utility for Wayland')
    subparsers = parser.add_subparsers(dest='command')

    parserAdd = subparsers.add_parser('execute', help='Execute a script')
    parserAdd.add_argument('name', help='name of the script to execute')
    parserAdd.add_argument('-f', '--file', action='store_true', help='Use file path instead of name')
    parserAdd.add_argument('-v', '--verbose', action='store_true', help='Make the output verbose')
    parserAdd.add_argument('-y', '--yes', action='store_true', help='Answer yes to all prompts')
    parserAdd.add_argument('-k', '--kill', action='store_true', help='Kill the running script')

    parserList = subparsers.add_parser('list', aliases=['ls'], help='list all scripts')
    parserList.add_argument('-r', '--running', action='store_true', help='list all running scripts')

    parserServer = subparsers.add_parser('server', help='Manage the taskZen server')
    parserServer.add_argument('-s', '--start', action='store_true', help='start the execution server')
    parserServer.add_argument('-k', '--kill', action='store_true', help='kill the execution server')

    parserGui = subparsers.add_parser('gui', help='Start the taskZen GUI')
    
    args = parser.parse_args()

    if args.command is None:
        # Print help
        parser.print_help()
        exit(0)

    elif args.command in ['execute']:
        if args.kill:
            print(f'Killing execution of script: {args.name}')
            instruction = {
                'instruction': 'killExecution',
                'scriptName': args.name
            }
            try:
                sendInstruction(json.dumps(instruction))
            except (ConnectionRefusedError, FileNotFoundError):
                print()
                print('Failed to send instruction. Server not running?')
                print('You can start the server using `taskZen server -s`')
            exit(0)
        print(f'Executing {args.name}')

        if args.file:
            scriptPath = args.name
        else:
            scriptPath = findScript(args.name)

        if scriptPath is None or not os.path.exists(scriptPath):
            print(f'Script {args.name} not found.')
            exit(1)

        # Load the data
        scriptData = readScript(scriptPath)

        allowExec = False
        if scriptContainsExec(scriptData):
            print('Script contains an exec command. Are you sure you want to execute it?')
            print('These scripts may be unsafe. Use it at your own risk.')
            if not args.yes:
                result = input('Type "YES" to continue: ')
                if result == 'YES':
                    allowExec = True
                else:
                    print('Aborting.')
                    exit(1)
            else:
                allowExec = True

        try:
            instruction = {
                'instruction': 'execute',
                'scriptName': args.name,
                'file': args.file,
                'verbose': args.verbose,
                'allowExec': allowExec
            }
            sendInstruction(json.dumps(instruction))
        except (ConnectionRefusedError, FileNotFoundError):
            print()
            print('Failed to send instruction. Server not running?')
            print('You can start the server using `taskZen server -s`')

    elif args.command in ['list', 'ls']:
        print('\ttaskZen\nAutomation utility for Wayland\n')
        # List running scripts
        if args.running:
            print('Running scripts:')
            instruction = {
                'instruction': 'listRunning'
            }
            result = sendInstruction(json.dumps(instruction))
            exit(0)
        
        # List all scripts
        print('Available scripts:')
        for file in os.listdir(scriptDir):
            with open(scriptDir + file, 'r') as f:
                scriptData = yaml.safe_load(f)
            print(f'\t- {scriptData['name']} ({os.path.abspath(scriptDir + file)})')

    elif args.command in ['server']:
        if args.start:
            print('Starting taskZen server')
            try:
                instruction = {
                    'instruction': 'ping'
                }
                sendInstruction(json.dumps(instruction))
                print('Server already running')
            except (ConnectionRefusedError, FileNotFoundError):
                from subprocess import DEVNULL
                import subprocess
                scriptPath = f'{os.path.dirname(os.path.realpath(__file__))}/executionServer.py'
                # Start the subprocess in a new session and redirect standard streams to DEVNULL
                subprocess.Popen(
                    [f"{os.path.join(os.getenv('VIRTUAL_ENV', ''), 'bin/python')}", scriptPath],
                    start_new_session=True,
                    stdout=DEVNULL,
                    stderr=DEVNULL,
                    stdin=DEVNULL
                )

        elif args.kill:
            print('Killing taskZen server')
            try:
                instruction = {
                    'instruction': 'kill'
                }
                sendInstruction(json.dumps(instruction))
            except (ConnectionRefusedError, FileNotFoundError):
                print('Server not running')

        else:
            parserServer.print_help()
    
    elif args.command in ['gui']:
        from subprocess import DEVNULL
        import subprocess
        currentPath = f'{os.path.dirname(os.path.realpath(__file__))}'
        # Start the subprocess in a new session and redirect standard streams to DEVNULL
        subprocess.Popen(
            [f"{os.path.join(os.getenv('VIRTUAL_ENV', ''), 'bin/python')}", f'{currentPath}/gui/homeWindow.py'],
            start_new_session=True,
            stdout=DEVNULL,
            stderr=DEVNULL,
            stdin=DEVNULL,
            cwd=os.path.dirname(currentPath) # Change the working dir to the dir of the script
        )

if __name__ == '__main__':
    checkConfig()
    main()
