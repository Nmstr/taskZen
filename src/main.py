from functions.checkDirs import checkDirs

import argparse
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

    parserList = subparsers.add_parser('list', aliases=['ls'], help='list all scripts')

    parserGui = subparsers.add_parser('gui', help='Start the taskZen GUI')

    args = parser.parse_args()

    if args.command is None:
        # Print help
        parser.print_help()
        exit(0)


    elif args.command in ['execute']:
        if args.file:
            scriptPath = args.name
        else:
            scriptDir = os.getenv('XDG_CONFIG_HOME', default=os.path.expanduser('~/.config')) + '/taskZen/scripts/'
            scriptPath = scriptDir + args.name + '.py'

        if scriptPath is None or not os.path.exists(scriptPath):
            print(f'Script {args.name} not found.')
            exit(1)

        from subprocess import DEVNULL
        import subprocess
        currentDir = os.path.dirname(os.path.realpath(__file__))
        if 'FLATPAK_ID' in os.environ:
            pythonExecutable = "/usr/bin/python"
        else:
            pythonExecutable = os.path.join(os.getenv('VIRTUAL_ENV', ''), 'bin/python')
        env = os.environ.copy()
        env['PYTHONPATH'] = currentDir + os.pathsep + env.get('PYTHONPATH', '')
        
        subprocess.call(
            [pythonExecutable, scriptPath],
            cwd=currentDir,
            env=env
        )


    elif args.command in ['list', 'ls']:
        print('\ttaskZen\nAutomation utility for Wayland\n')
        # List all scripts
        print('Available scripts:')
        for file in os.listdir(scriptDir):
            print(f'\t- {os.path.splitext(file)[0]} ({os.path.abspath(scriptDir + file)})')


    elif args.command in ['gui']:
        from subprocess import DEVNULL
        import subprocess
        currentDir = f'{os.path.dirname(os.path.realpath(__file__))}'
        if 'FLATPAK_ID' in os.environ:
            pythonExecutable = "/usr/bin/python"
        else:
            pythonExecutable = os.path.join(os.getenv('VIRTUAL_ENV', ''), 'bin/python')
        subprocess.Popen(
            [pythonExecutable, f'{currentDir}/gui/homeWindow.py'],
            start_new_session=True,
            stdout=DEVNULL,
            stderr=DEVNULL,
            stdin=DEVNULL,
            cwd=os.path.dirname(currentDir),
        )

if __name__ == '__main__':
    checkDirs()
    main()
