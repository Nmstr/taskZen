from initialize import initialize, readScript, findScript
from executer import execute
import argparse
import yaml
import os

def main():
    scriptDir = os.getenv('XDG_CONFIG_HOME', default=os.path.expanduser('~/.config')) + '/taskZen/'
    if not os.path.exists(scriptDir):
        os.makedirs(scriptDir, exist_ok=True)

    parser = argparse.ArgumentParser(prog='taskZen', description='Automation utility for Wayland')
    subparsers = parser.add_subparsers(dest='command')

    parser_add = subparsers.add_parser('execute', help='Execute a script')
    parser_add.add_argument('name', help='name of the script to execute')

    parser_list = subparsers.add_parser('list', aliases=['ls'], help='list all connections')

    args = parser.parse_args()

    if args.command is None:
        # Print help
        parser.print_help()
        exit(0)

    elif args.command in ['execute']:
        print(f'Executing {args.name}')

        # Find the script
        scriptPath = findScript(args.name)        

        # Initialize the input device and load data
        scriptData = readScript(scriptPath)
        allKeys, ui = initialize(scriptData)
        
        execute(scriptData, ui, allKeys)

    elif args.command in ['list', 'ls']:
        # List all scripts
        print('\ttaskZen\nAutomation utility for Wayland\n')
        print('Available scripts:')
        for file in os.listdir(scriptDir):
            with open(scriptDir + file, 'r') as f:
                scriptData = yaml.safe_load(f)
            print(f'\t- {scriptData["name"]} ({os.path.abspath(scriptDir + file)})')

if __name__ == '__main__':
    main()
