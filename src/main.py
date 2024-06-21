from initialize import initialize, readScript, findScript, scriptContainsExec
from executer import Executer
import argparse
import yaml
import os

def main():
    scriptDir = os.getenv('XDG_CONFIG_HOME', default=os.path.expanduser('~/.config')) + '/taskZen/'
    if not os.path.exists(scriptDir):
        os.makedirs(scriptDir, exist_ok=True)

    parser = argparse.ArgumentParser(prog='taskZen', description='Automation utility for Wayland')
    subparsers = parser.add_subparsers(dest='command')

    parserAdd = subparsers.add_parser('execute', help='Execute a script')
    parserAdd.add_argument('name', help='name of the script to execute')
    parserAdd.add_argument('-f', '--file', action='store_true', help='Use file path instead of name')
    parserAdd.add_argument('-v', '--verbose', action='store_true', help='Make the output verbose')
    parserAdd.add_argument('-y', '--yes', action='store_true', help='Answer yes to all prompts')

    parserList = subparsers.add_parser('list', aliases=['ls'], help='list all connections')

    args = parser.parse_args()

    if args.command is None:
        # Print help
        parser.print_help()
        exit(0)

    elif args.command in ['execute']:
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

        # Initialize the input device
        allKeys, ui = initialize(scriptData)
        
        executer = Executer(ui=ui, allKeys=allKeys, verbose=args.verbose, allowExec=allowExec)
        executer.execute(scriptData)

    elif args.command in ['list', 'ls']:
        # List all scripts
        print('\ttaskZen\nAutomation utility for Wayland\n')
        print('Available scripts:')
        for file in os.listdir(scriptDir):
            with open(scriptDir + file, 'r') as f:
                scriptData = yaml.safe_load(f)
            print(f'\t- {scriptData['name']} ({os.path.abspath(scriptDir + file)})')

if __name__ == '__main__':
    main()
