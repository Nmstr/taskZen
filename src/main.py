from evdev import ecodes as e
import time

# Initialize the input device and load data
from initialize import initialize
allKeys, data, ui = initialize()

executionSpeed = data['speed']
# Execute the steps
for step in data['steps']:
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