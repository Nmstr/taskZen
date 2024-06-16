from evdev import ecodes as e
import subprocess
import time

def execute(scriptData, ui, allKeys):
    executionSpeed = scriptData['speed']
    # Execute the steps
    for step in scriptData['steps']:
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
            ui.write(e.EV_ABS, e.ABS_X, step['x'])
            ui.write(e.EV_ABS, e.ABS_Y, step['y'])
            ui.syn()
        
        elif step['type'] == 'move-relative':
            ui.write(e.EV_REL, e.REL_X, step['x'])
            ui.write(e.EV_REL, e.REL_Y, step['y'])
            ui.syn()

        elif step['type'] == 'exec':
            blocking = step.get('blocking', False)
            print(step['value'].split())
            if blocking:
                subprocess.call(step['value'].split())
            else:
                subprocess.Popen(step['value'].split())

        time.sleep(executionSpeed / 1000)

    # Close the device when done
    time.sleep(0.1) # Let the device process the events
    ui.close()
