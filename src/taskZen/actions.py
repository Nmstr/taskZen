from evdev import ecodes as e
import time

scriptData = None
ui = None
device = None
allKeys = None
executionSpeed = None
stopFlag = False

def setVariables(uiValue, allKeysValue) -> None:
    global ui
    global allKeys
    global device

    ui = uiValue
    device = uiValue
    allKeys = allKeysValue

def pressKey(key: str) -> None:
    """
    Press the specified key
    
    Parameters:
        - key (str): The key to press
    """
    key = retrieveValue(key)

    ui.write(e.EV_KEY, allKeys.get(key), 1)
    ui.syn()

def releaseKey(key: str) -> None:
    """
    Release the specified key
    
    Parameters:
        - key (str): The key to release
    """
    key = retrieveValue(key)

    ui.write(e.EV_KEY, allKeys.get(key), 1)
    ui.write(e.EV_KEY, allKeys.get(key), 0)
    ui.syn()

def tapKey(key: str, modifier: str = None) -> None:
    """
    Tap the specified key
    
    Parameters:
        - key (str): The key to tap
        - modifier (str, optional): The modifier to use. Defaults to None.
    """
    key = retrieveValue(key)
    modifier = retrieveValue(modifier)

    if modifier == 'SHIFT':
        ui.write(e.EV_KEY, e.KEY_LEFTSHIFT, 1)
    ui.write(e.EV_KEY, allKeys.get(key), 1)
    ui.write(e.EV_KEY, allKeys.get(key), 0)
    if modifier == 'SHIFT':
        ui.write(e.EV_KEY, e.KEY_LEFTSHIFT, 0)
    ui.syn()
    
def moveAbsolute(x: int, y: int) -> None:
    """
    Move the mouse to the specified coordinates
    
    Parameters:
        - x (int): The x coordinate
        - y (int): The y coordinate
    """
    x = retrieveValue(x)
    y = retrieveValue(y)

    device.write(e.EV_ABS, e.ABS_X, x)
    device.write(e.EV_ABS, e.ABS_Y, y)
    device.syn()

def moveRelative(x: int, y: int) -> None:
    """
    Move the mouse relative to the current position
    
    Parameters:
        - x (int): The x coordinate
        - y (int): The y coordinate
    """
    x = retrieveValue(x)
    y = retrieveValue(y)

    ui.write(e.EV_REL, e.REL_X, x)
    ui.write(e.EV_REL, e.REL_Y, y)
    ui.syn()
    
def modifyVariable(self, variable: str, operation: str, value) -> None:
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

    # await self.sendMessage(f'Variable Modified: {variable} {operation} {value} -> {self.variableData[variable]}', True, writer=self.writer)

def execute(self, scriptData: dict) -> None:
    """
    Execute the script
    
    Parameters:
        - scriptData (dict): The script data
    """
    # Load the script
    self.scriptData = scriptData
    if not self.scriptData:
        #await self.sendMessage(f'Error: No script data', writer=self.writer)
        return
    self.executionSpeed = self.scriptData['speed']
    if 'variables' in self.scriptData:
        self.variableData = self.scriptData['variables']

    # Execute the script
    for step in self.scriptData['steps']:
        #await self.sendMessage(step, True, writer=self.writer)
        
        self.executeIteration(step)

    time.sleep(0.1) # Let the device process the events

def executeIteration(self, step: dict) -> None:
    """
    Executes a single iteration of the script based on the given step.
    Args:
        step (dict): A dictionary representing a step in the script.
    Returns:
        None: This function does not return anything.
    """
    if self.stopFlag:
        return
    if step['type'] == 'wait':
        self.wait(step['value'])
    elif step['type'] == 'press':
        self.pressKey(step['value'])
    elif step['type'] == 'release':
        self.releaseKey(step['value'])
    elif step['type'] == 'tap':
        self.tapKey(step['value'], step.get('modifier', None))
    elif step['type'] == 'move-absolute':
        self.moveAbsolute(step['x'], step['y'])
    elif step['type'] == 'move-relative':
        self.moveRelative(step['x'], step['y'])
    elif step['type'] == 'modify-variable':
        self.modifyVariable(step['variable'], step['operation'], step['value'])
    elif step['type'] == 'loop':
        for _ in range(self.retrieveValue(step['value'])):
            for subStep in step['subSteps']:    
                #await self.sendMessage(f'-> {subStep}', True, writer=self.writer)
                self.executeIteration(subStep)
    elif step['type'] == 'if':
        if self.evaluateCondition(step['operation'], step['value1'], step.get('value2', None)):
            if 'trueSteps' not in step: # If there are no true steps, return
                return
            for subStep in step['trueSteps']:    
                #await self.sendMessage(f'-> {subStep}', True, writer=self.writer)
                self.executeIteration(subStep)
        else:
            if 'falseSteps' not in step: # If there are no true steps, return
                return
            for subStep in step['falseSteps']:    
                #await self.sendMessage(f'-> {subStep}', True, writer=self.writer)
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
            
    #await self.sendMessage(f'Condition: {value1} ({type(value1)}) {operation} {value2} ({type(value2)})', True, writer=self.writer)

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

def retrieveValue(value):
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
        #await self.sendMessage(f'Variable -> {value}: {self.variableData.get(value[1:])}', True, writer=self.writer)
        return variableData.get(value[1:])
        
    elif value.startswith('-$'): # Invert variable
        #await self.sendMessage(f'Variable -> {value[1:]}: {-self.variableData.get(value[2:])}', True, writer=self.writer)
        return -variableData.get(value[2:])
        
    return value

def stop(self) -> None:
    """
    Stops the execution of the script.
    """
    self.stopFlag = True
