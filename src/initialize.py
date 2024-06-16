from evdev import UInput, ecodes as e, AbsInfo
import yaml

def initialize(scriptData: dict):
    # Create the allKeys dictionary
    allKeys = {}
    for key, values in e.keys.items():
        if isinstance(values, list):
            for value in values:
                allKeys[value] = key
        else:
            allKeys[values] = key
        
    # Create the key list
    keyList = []
    for key in scriptData['keys']:
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
    ui = UInput(cap, name='virtual-input-device', version=0x3)

    return allKeys, ui

def readScript(scriptPath: str = "examples/exampleKeyboard.yaml"):
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
