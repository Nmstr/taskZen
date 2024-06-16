from evdev import UInput, ecodes as e, AbsInfo
import time
import yaml

# Create the allKeys dictionary
allKeys = {}
for key, values in e.keys.items():
    if isinstance(values, list):
        for value in values:
            allKeys[value] = key
    else:
        allKeys[values] = key
    
# Open the YAML file and load the data
with open("example.yaml", "r") as file:
    data = yaml.safe_load(file)

# Create the key list
keyList = []
for key in data['keys']:
    number = allKeys.get(key)
    keyList.append(number)

cap = {
    e.EV_KEY: keyList,
    e.EV_ABS: [
        (e.ABS_X, AbsInfo(value=0, min=0, max=1920, fuzz=0, flat=0, resolution=0)),
        (e.ABS_Y, AbsInfo(value=0, min=0, max=1080, fuzz=0, flat=0, resolution=0)),
    ],
}

# Create the virtual input device with absolute positioning
ui = UInput(cap, name='virtual-input-device', version=0x3)

executionSpeed = data['speed']
for step in data['steps']:
    print(step)
    if step['type'] == 'wait':
        time.sleep(step['value'] / 1000)

    elif step['type'] == 'press':
        ui.write(e.EV_KEY, allKeys.get(step['value']), 1)
        ui.syn()

    elif step['type'] == 'release':
        ui.write(e.EV_KEY, allKeys.get(step['value']), 0)
        ui.syn()

    elif step['type'] == 'tap':
        modifier = step.get('modifier', None)
        if modifier == 'SHIFT':
            ui.write(e.EV_KEY, e.KEY_LEFTSHIFT, 1)
            ui.write(e.EV_KEY, allKeys.get(step['value']), 1)
            ui.write(e.EV_KEY, allKeys.get(step['value']), 0)
            ui.write(e.EV_KEY, e.KEY_LEFTSHIFT, 0)
        else:
            ui.write(e.EV_KEY, allKeys.get(step['value']), 1)
            ui.write(e.EV_KEY, allKeys.get(step['value']), 0)
        ui.syn()

    elif step['type'] == 'move-absolute':
        ui.write(e.EV_ABS, e.ABS_X, step['valueX'])
        ui.write(e.EV_ABS, e.ABS_Y, step['valueY'])
        ui.syn()

    time.sleep(executionSpeed / 1000)

# Close the device when done
time.sleep(0.1) # Let the device process the events
ui.close()