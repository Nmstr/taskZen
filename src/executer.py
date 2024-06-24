from evdev import ecodes as e
import subprocess
import time

class Executer:
    def __init__(self, *, parent = None, ui, allKeys: dict, allowExec: bool = False) -> None:
        """
        Initialize the executer
        
        Parameters:
            - ui (UInput): The UInput object
            - allKeys (dict): The dictionary of all keys
            - verbose (bool, optional): Whether to print verbose output. Defaults to False.
        """
        self.parent = parent
        self.scriptData = None
        self.ui = ui
        self.allKeys = allKeys
        self.allowExec = allowExec
        self.executionSpeed = None

    def actionWait(self, sleepTime: int) -> None:
        """
        Sleep for the specified amount of time
        
        Parameters:
            - sleepTime (int): The amount of time to sleep in milliseconds
        """
        sleepTime = self.retrieveValue(sleepTime)
        time.sleep(sleepTime / 1000)

    def actionPressKey(self, key: str) -> None:
        """
        Press the specified key
        
        Parameters:
            - key (str): The key to press
        """
        key = self.retrieveValue(key)

        self.ui.write(e.EV_KEY, self.allKeys.get(key), 1)
        self.ui.syn()

    def actionReleaseKey(self, key: str) -> None:
        """
        Release the specified key
        
        Parameters:
            - key (str): The key to release
        """
        key = self.retrieveValue(key)

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
        key = self.retrieveValue(key)
        modifier = self.retrieveValue(modifier)

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
        x = self.retrieveValue(x)
        y = self.retrieveValue(y)

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
        x = self.retrieveValue(x)
        y = self.retrieveValue(y)

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
        command = self.retrieveValue(command)
        blocking = self.retrieveValue(blocking)

        if blocking:
            subprocess.call(command)
        else:
            subprocess.Popen(command)

    def actionModifyVariable(self, variable: str, operation: str, value) -> None:
        """
        Modify a variable
        
        Parameters:
            - variable (str): The variable to modify
            - operation (str): The operation to perform
                - set
                - add
                - subtract
                - multiply
                - divide
            - value (any): The value to use for the operation
        """
        if operation == 'set':
            self.variableData[variable] = self.retrieveValue(value)
        elif operation == 'add':
            self.variableData[variable] += self.retrieveValue(value)
        elif operation == 'subtract':
            self.variableData[variable] -= self.retrieveValue(value)
        elif operation == 'multiply':
            self.variableData[variable] *= self.retrieveValue(value)
        elif operation == 'divide':
            self.variableData[variable] /= self.retrieveValue(value)

        self.parent.sendMessage(f'Variable Modified: {variable} {operation} {value} -> {self.variableData[variable]}', True)

    def execute(self, scriptData: dict) -> None:
        """
        Execute the script
        
        Parameters:
            - scriptData (dict): The script data
        """
        # Load the script
        self.scriptData = scriptData
        if not self.scriptData:
            self.parent.sendMessage(f'Error: No script data')
            return
        self.executionSpeed = self.scriptData['speed']
        if 'variables' in self.scriptData:
            self.variableData = self.scriptData['variables']

        # Execute the script
        for step in self.scriptData['steps']:
            self.parent.sendMessage(step, True)
            
            self.executeIteration(step)

        time.sleep(0.1) # Let the device process the events
        #self.ui.close()

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
                if self.allowExec:
                    self.actionExec(step['value'].split(), step.get('blocking', False))
            elif step['type'] == 'modify-variable':
                self.actionModifyVariable(step['variable'], step['operation'], step['value'])
            elif step['type'] == 'loop':
                for _ in range(self.retrieveValue(step['value'])):
                    for subStep in step['subSteps']:    
                        self.parent.sendMessage(f'-> {subStep}', True)
                        self.executeIteration(subStep)
            elif step['type'] == 'if':
                if self.evaluateCondition(step['operation'], step['value1'], step.get('value2', None)):
                    if 'trueSteps' not in step: # If there are no true steps, return
                        return
                    for subStep in step['trueSteps']:    
                        self.parent.sendMessage(f'-> {subStep}', True)
                        self.executeIteration(subStep)
                else:
                    if 'falseSteps' not in step: # If there are no true steps, return
                        return
                    for subStep in step['falseSteps']:    
                        self.parent.sendMessage(f'-> {subStep}', True)
                        self.executeIteration(subStep)

            time.sleep(self.executionSpeed / 1000)

    def evaluateCondition(self, operation: str, value1, value2 = None) -> bool:
        """
        Evaluate a condition
        
        Parameters:
            - operation (str): The operation to perform
                - bool (checks if bool is true)
                - ==
                - !=
                - >
                - <
                - >=
                - <=
            - value1 (any): The first value
            - value2 (any, optional): The second value. Defaults to None.

        Returns:
            - The result of the evaluation
        """
        # Retrieve values
        value1 = self.retrieveValue(value1)
        if value2 is not None:
            value2 = self.retrieveValue(value2)
            
        self.parent.sendMessage(f'Condition: {value1} ({type(value1)}) {operation} {value2} ({type(value2)})', True)

        # Evaluate condition
        if operation == 'bool':
            if value1 is True:
                return True
            else:
                return False
        elif operation == '==':
            return value1 == value2
        elif operation == '!=':
            return value1 != value2
        elif operation == '>':
            return value1 > value2
        elif operation == '<':
            return value1 < value2
        elif operation == '>=':
            return value1 >= value2
        elif operation == '<=':
            return value1 <= value2

    def retrieveValue(self, value):
        """
        Checks if a value is a variable and if so retrieves the value. If not, it returns the value as is.
        
        Parameters:
            - value (any): The value to retrieve

        Returns:
            - The retrieved value (any)
        """

        if value == None:
            return None
        if not isinstance(value, str):
            return value
        
        if value.startswith('$'):
            self.parent.sendMessage(f'Variable -> {value}: {self.variableData.get(value[1:])}', True)
            return self.variableData.get(value[1:])
        
        elif value.startswith('-$'): # Invert variable
            self.parent.sendMessage(f'Variable -> {value[1:]}: {-self.variableData.get(value[2:])}', True)
            return -self.variableData.get(value[2:])
        
        return value
