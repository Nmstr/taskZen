import shutil
import os

def checkDirs() -> None:
    """
    Creates necessary directories. Also copies example scripts and devices.
    """
    # Handle config
    configDir = os.getenv('XDG_CONFIG_HOME', default=os.path.expanduser('~/.config')) + '/taskZen/'
    os.makedirs(configDir, exist_ok=True)
    os.makedirs(configDir + 'scripts/', exist_ok=True)
    os.makedirs(configDir + 'devices/', exist_ok=True)
    currentPath = os.path.dirname(os.path.realpath(__file__))
    for script in os.listdir(currentPath + '/../../examples/scripts'):
        if not os.path.exists(configDir + 'scripts/' + script):
            shutil.copyfile(currentPath + '/../../examples/scripts/' + script, configDir + 'scripts/' + script)
    for device in os.listdir(currentPath + '/../../examples/devices'):
        if not os.path.exists(configDir + 'devices/' + device):
            shutil.copyfile(currentPath + '/../../examples/devices/' + device, configDir + 'devices/' + device)

    # Handle cache
    cacheDir = os.getenv('XDG_CACHE_HOME', default=os.path.expanduser('~/.cache')) + '/taskZen/'
    os.makedirs(cacheDir, exist_ok=True)
