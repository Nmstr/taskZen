from evdev import UInput, ecodes as e, AbsInfo
import yaml
import os

async def initialize(scriptData: dict):
    # Find all matching devices
    deviceDir = os.getenv('XDG_CONFIG_HOME', default=os.path.expanduser('~/.config')) + '/taskZen/devices/'
    foundDevices = []
    for file in os.listdir(deviceDir):
        with open(deviceDir + file, 'r') as f:
            deviceData = yaml.safe_load(f)
        if scriptData['device'] == deviceData['name']:
            foundDevices.append(file)

    finalDevice = None
    # Match the version
    if scriptData.get('device-version') is None: # Get newest version
        foundDevicesData = []
        for device in foundDevices:
            with open(deviceDir + device, 'r') as f:
                device = yaml.safe_load(f)
            foundDevicesData.append(device)
        finalDevice = max(foundDevicesData, key=lambda x: x['version'])

    else: # Get matching version
        for device in foundDevices:
            with open(deviceDir + device, 'r') as f:
                deviceData = yaml.safe_load(f)
            if deviceData['version'] == scriptData.get('device-version'):
                finalDevice = deviceData
                break

    if finalDevice is None:
        return None, 'Device not found'

    # Create the allKeys dictionary
    allKeys = getAllKeys()
        
    # Create the key list
    keyList = []
    for key in finalDevice['keys']:
        number = allKeys.get(key)
        keyList.append(number)

    screenWidth = scriptData.get('screen', {}).get('width', 1920)
    screenHeight = scriptData.get('screen', {}).get('height', 1080)
    # Create the capabilities dictionary
    cap = {
        e.EV_KEY: keyList,
        e.EV_ABS: [
            (e.ABS_X, AbsInfo(value=0, min=0, max=screenWidth, fuzz=0, flat=0, resolution=0)),
            (e.ABS_Y, AbsInfo(value=0, min=0, max=screenHeight, fuzz=0, flat=0, resolution=0)),
        ],
        e.EV_REL: [
            (e.REL_X),
            (e.REL_Y),
        ],
    }

    # Create the virtual input device with absolute positioning
    ui = UInput(cap, name='taskZen-virtual-input-device', phys='taskZen-virtual-input-device')

    return ui, None

def getAllKeys():
    # Create the allKeys dictionary
    allKeys = {}
    for key, values in e.keys.items():
        if isinstance(values, list):
            for value in values:
                allKeys[value] = key
        else:
            allKeys[values] = key
    return allKeys

def readScript(scriptPath: str):
    """
    Read the YAML file and return the data

    Parameters:
        - scriptPath (str, optional): The path to the YAML file. Defaults to "examples/exampleKeyboard.yaml".
    
    Returns:
        - scriptData (dict): The data from the YAML file
    """
    # Open the YAML file and load the data
    with open(scriptPath, "r") as file:
        scriptData = yaml.safe_load(file)
    
    return scriptData

def findScript(scriptName: str):
    """
    Finds the file path for any given script

    Parameters:
        - scriptName (str): The name of the script

    Returns:
        - scriptPath (str): The path to the script
    """
    scriptDir = os.getenv('XDG_CONFIG_HOME', default=os.path.expanduser('~/.config')) + '/taskZen/scripts/'
    for script in os.listdir(scriptDir):
        with open(scriptDir + script, 'r') as file:
            data = yaml.safe_load(file)
            if data['name'] == scriptName:
                return scriptDir + script

def scriptContainsExec(scriptData: dict) -> bool:
    """
    Checks if the script contains an exec command, including within loops
    
    Parameters:
        - scriptData (dict): The script data
    
    Returns:
        - bool: Whether the script contains an exec command
    """
    def containsExec(steps):
        for step in steps:
            if step['type'] == 'exec':
                return True
            elif step['type'] == 'loop' and 'subSteps' in step:
                if containsExec(step['subSteps']):
                    return True
            elif step['type'] == 'if' and 'trueSteps' in step and 'falseSteps' in step:
                if containsExec(step['trueSteps']) or containsExec(step['falseSteps']):
                    return True
            elif step['type'] == 'if' and 'trueSteps' in step:
                if containsExec(step['trueSteps']):
                    return True
            elif step['type'] == 'if' and 'falseSteps' in step:
                if containsExec(step['falseSteps']):
                    return True                
        return False

    return containsExec(scriptData.get('steps', []))
