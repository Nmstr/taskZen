from evdev import UInput, ecodes as e, AbsInfo
import yaml
import os

def initialize(deviceName) -> tuple:
    finalDevice = getFinalDevice(deviceName)
    if finalDevice is None:
        return None, 'Device not found'

    # Create the allKeys dictionary
    allKeys = getAllKeys()
        
    # Create the key list
    keyList = []
    for key in finalDevice['keys']:
        number = allKeys.get(key)
        keyList.append(number)

    # Create capabilities
    cap = {
        e.EV_KEY: keyList,
        e.EV_REL: [
            (e.REL_X),
            (e.REL_Y)
        ],
        e.EV_ABS: [
            (e.ABS_X, AbsInfo(0, 0, 1920, 0, 0, 0)),
            (e.ABS_Y, AbsInfo(0, 0, 1080, 0, 0, 0))
        ]
    }

    device = UInput(cap, name=finalDevice['name'], phys=finalDevice['phys'])
    return device

def getFinalDevice(deviceName: int) -> dict:
    finalDevice = None
    # Find the device
    deviceDir = os.getenv('XDG_CONFIG_HOME', default=os.path.expanduser('~/.config')) + '/taskZen/devices/'
    for file in os.listdir(deviceDir):
        with open(deviceDir + file, 'r') as f:
            deviceData = yaml.safe_load(f)
            if deviceName == deviceData['name']:
                finalDevice = deviceData

    if not finalDevice:
        print("Device not found")
        exit(1)
    return finalDevice

def getAllKeys() -> dict:
    # Create the allKeys dictionary
    allKeys = {}
    for key, values in e.keys.items():
        if isinstance(values, list):
            for value in values:
                allKeys[value] = key
        else:
            allKeys[values] = key
    return allKeys

def readScript(scriptPath: str) -> dict:
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

def findScript(scriptName: str) -> str:
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
