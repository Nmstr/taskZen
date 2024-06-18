from evdev import ecodes as e
import subprocess
import time

class Executer:
    def __init__(self, scriptData, ui, allKeys):
        self.scriptData = scriptData
        self.ui = ui
        self.allKeys = allKeys

    def actionWait(self, sleepTime):
        time.sleep(sleepTime / 1000)

    def actionPressKey(self, key):
        self.ui.write(e.EV_KEY, self.allKeys.get(key), 1)
        self.ui.syn()

    def actionReleaseKey(self, key):
        self.ui.write(e.EV_KEY, self.allKeys.get(key), 0)
        self.ui.syn()

    def actionTapKey(self, key, modifier=None):
        if modifier == 'SHIFT':
            self.ui.write(e.EV_KEY, e.KEY_LEFTSHIFT, 1)
        self.ui.write(e.EV_KEY, self.allKeys.get(key), 1)
        self.ui.write(e.EV_KEY, self.allKeys.get(key), 0)
        if modifier == 'SHIFT':
            self.ui.write(e.EV_KEY, e.KEY_LEFTSHIFT, 0)
        self.ui.syn()
    
    def actionMoveAbsolute(self, x, y):
        self.ui.write(e.EV_ABS, e.ABS_X, x)
        self.ui.write(e.EV_ABS, e.ABS_Y, y)
        self.ui.syn()

    def actionMoveRelative(self, x, y):
        self.ui.write(e.EV_REL, e.REL_X, x)
        self.ui.write(e.EV_REL, e.REL_Y, y)
        self.ui.syn()
    
    def actionExec(self, command, blocking=False):
        if blocking:
            subprocess.call(command)
        else:
            subprocess.Popen(command)

    def execute(self):
        executionSpeed = self.scriptData['speed']
        for step in self.scriptData['steps']:
            print(step)
            if step['type'] == 'wait':
                self.actionWait(step['value'])
            elif step['type'] == 'press':
                self.actionPressKey(step['value'])
            elif step['type'] == 'release':
                self.actionReleaseKey(step['value'])
            elif step['type'] == 'tap':
                self.actionTapKey(step['value'], step.get('modifier', None))
            elif step['type'] == 'move-absolute':
                self.actionMoveAbsolute(step['x'], step['y'])
            elif step['type'] == 'move-relative':
                self.actionMoveRelative(step['x'], step['y'])
            elif step['type'] == 'exec':
                self.actionExec(step['value'].split(), step.get('blocking', False))

            time.sleep(executionSpeed / 1000)

        time.sleep(0.1) # Let the device process the events
        self.ui.close()
