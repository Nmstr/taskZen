from functions.sendInstruction import sendInstruction
import json
import os

def pingServer() -> tuple[bool, str]:
    """
    Pings the execution server.

    Returns:
        tuple[bool, str]: A tuple containing a boolean indicating whether the server was pinged and a string
        indicating the status of the server.
    """
    try:
        instruction = {
            'instruction': 'ping'
        }
        sendInstruction(json.dumps(instruction))
        return True, 'Pinged successfully'
    except (ConnectionRefusedError, FileNotFoundError):
        return False, 'Server not running'

def startServer() -> tuple[bool, str]:
    """
    Starts the execution server.

    Returns:
        tuple[bool, str]: A tuple containing a boolean indicating whether the server was started and a string
        indicating the status of the server.
    """
    if pingServer()[0]:
        return False, 'Server already running'
    else:
        from subprocess import DEVNULL
        import subprocess
        currentPath = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        if 'FLATPAK_ID' in os.environ:
            pythonExecutable = "/usr/bin/python"
        else:
            pythonExecutable = os.path.join(os.getenv('VIRTUAL_ENV', ''), 'bin/python')
        logFile = os.getenv('XDG_CACHE_HOME', default=os.path.expanduser('~/.cache')) + '/taskZen/server.log'
        with open(logFile, 'w') as f:
            subprocess.Popen(
                [pythonExecutable, '-u', f'{currentPath}/executionServer.py'],
                start_new_session=True,
                stdout=f,
                stderr=DEVNULL,
                stdin=DEVNULL
            )
        return True, 'Server started'

def stopServer() -> tuple[bool, str]:
    """
    Stops the execution server.

    Returns:
        tuple[bool, str]: A tuple containing a boolean indicating whether the server was stopped and a string
        indicating the status of the server.
    """
    try:
        instruction = {
            'instruction': 'kill'
        }
        sendInstruction(json.dumps(instruction))
        return True, 'Server stopped'
    except (ConnectionRefusedError, FileNotFoundError):
        return False, 'Server not running'
