from evdev import UInput, ecodes as e, AbsInfo
import yaml

def initialize():
    # Create the allKeys dictionary
    allKeys = {}
    for key, values in e.keys.items():
        if isinstance(values, list):
            for value in values:
                allKeys[value] = key
        else:
            allKeys[values] = key
        
    # Open the YAML file and load the data
    with open("examples/exampleKeyboard.yaml", "r") as file:
        data = yaml.safe_load(file)

    # Create the key list
    keyList = []
    for key in data['keys']:
        number = allKeys.get(key)
        keyList.append(number)

    # Create the capabilities dictionary
    cap = {
        e.EV_KEY: keyList,
        e.EV_ABS: [
            (e.ABS_X, AbsInfo(value=0, min=0, max=1920, fuzz=0, flat=0, resolution=0)),
            (e.ABS_Y, AbsInfo(value=0, min=0, max=1080, fuzz=0, flat=0, resolution=0)),
        ],
        e.EV_REL: [
            (e.REL_X),
            (e.REL_Y),
        ],
    }

    # Create the virtual input device with absolute positioning
    ui = UInput(cap, name='virtual-input-device', version=0x3)

    return allKeys, data, ui
