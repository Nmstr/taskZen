from initialize import readScript, findScript, scriptContainsExec
from functions.sendInstruction import sendInstruction
from functions.server import startServer, stopServer
from functions.checkDirs import checkDirs

import argparse
import yaml
import json
import os

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

        try:
            instruction = {
                'instruction': 'execute',
                'scriptName': args.name,
                'file': args.file,
                'verbose': args.verbose
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
            print(f'\t- {scriptData["name"]} ({os.path.abspath(scriptDir + file)})')

    elif args.command in ['server']:
        if args.start:
            print('Starting taskZen server')
            print(startServer()[1])

        elif args.kill:
            print('Killing taskZen server')
            print(stopServer()[1])

        else:
            parserServer.print_help()
    
    elif args.command in ['gui']:
        from subprocess import DEVNULL
        import subprocess
        currentPath = f'{os.path.dirname(os.path.realpath(__file__))}'
        if 'FLATPAK_ID' in os.environ:
            pythonExecutable = "/usr/bin/python"
        else:
            pythonExecutable = os.path.join(os.getenv('VIRTUAL_ENV', ''), 'bin/python')
        subprocess.Popen(
            [pythonExecutable, f'{currentPath}/gui/homeWindow.py'],
            start_new_session=True,
            stdout=DEVNULL,
            stderr=DEVNULL,
            stdin=DEVNULL,
            cwd=os.path.dirname(currentPath),
        )

if __name__ == '__main__':
    checkDirs()
    main()
