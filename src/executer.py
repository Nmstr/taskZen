from evdev import ecodes as e
import subprocess
import time

class Executer:
    def __init__(self, ui, allKeys: dict, verbose: bool = False) -> None:
        """
        Initialize the executer
        
        Parameters:
            - ui (UInput): The UInput object
            - allKeys (dict): The dictionary of all keys
            - verbose (bool, optional): Whether to print verbose output. Defaults to False.
        """
        self.scriptData = None
        self.ui = ui
        self.allKeys = allKeys
        self.verbose = verbose

    def actionWait(self, sleepTime: int) -> None:
        """
        Sleep for the specified amount of time
        
        Parameters:
            - sleepTime (int): The amount of time to sleep in milliseconds
        """
        time.sleep(sleepTime / 1000)

    def actionPressKey(self, key: str) -> None:
        """
        Press the specified key
        
        Parameters:
            - key (str): The key to press
        """
        self.ui.write(e.EV_KEY, self.allKeys.get(key), 1)
        self.ui.syn()

    def actionReleaseKey(self, key: str) -> None:
        """
        Release the specified key
        
        Parameters:
            - key (str): The key to release
        """
        self.ui.write(e.EV_KEY, self.allKeys.get(key), 1)
        self.ui.write(e.EV_KEY, self.allKeys.get(key), 0)
        self.ui.syn()

    def actionTapKey(self, key: str, modifier: str = None) -> None:
        """
        Tap the specified key
        
        Parameters:
            - key (str): The key to tap
            - modifier (str, optional): The modifier to use. Defaults to None.
        """
        if modifier == 'SHIFT':
            self.ui.write(e.EV_KEY, e.KEY_LEFTSHIFT, 1)
        self.ui.write(e.EV_KEY, self.allKeys.get(key), 1)
        self.ui.write(e.EV_KEY, self.allKeys.get(key), 0)
        if modifier == 'SHIFT':
            self.ui.write(e.EV_KEY, e.KEY_LEFTSHIFT, 0)
        self.ui.syn()
    
    def actionMoveAbsolute(self, x: int, y: int) -> None:
        """
        Move the mouse to the specified coordinates
        
        Parameters:
            - x (int): The x coordinate
            - y (int): The y coordinate
        """
        self.ui.write(e.EV_ABS, e.ABS_X, x)
        self.ui.write(e.EV_ABS, e.ABS_Y, y)
        self.ui.syn()

    def actionMoveRelative(self, x: int, y: int) -> None:
        """
        Move the mouse relative to the current position
        
        Parameters:
            - x (int): The x coordinate
            - y (int): The y coordinate
        """
        self.ui.write(e.EV_REL, e.REL_X, x)
        self.ui.write(e.EV_REL, e.REL_Y, y)
        self.ui.syn()
    
    def actionExec(self, command: list, blocking: bool = False) -> None:
        """
        Execute the specified command
        
        Parameters:
            - command (list): The command to execute
            - blocking (bool, optional): Whether to block the thread. Defaults to False.
        """
        if blocking:
            subprocess.call(command)
        else:
            subprocess.Popen(command)

    def execute(self, scriptData: dict) -> None:
        """
        Execute the script
        
        Parameters:
            - scriptData (dict): The script data
        """
        self.scriptData = scriptData
        if not self.scriptData:
            print("Error: No script data")
            return

        executionSpeed = self.scriptData['speed']
        for step in self.scriptData['steps']:
            if self.verbose:
                print(step)
            
            self.executeIteration(step)

            time.sleep(executionSpeed / 1000)

        time.sleep(0.1) # Let the device process the events
        self.ui.close()

    def executeIteration(self, step: dict) -> None:
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
            elif step['type'] == 'loop':
                for _ in range(step['value']):
                    for subStep in step['subSteps']:
                        if self.verbose:
                            print('->', subStep)
                        self.executeIteration(subStep)
