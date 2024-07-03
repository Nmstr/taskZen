from evdev import ecodes as e
import subprocess
import asyncio

class Executer:
    def __init__(self, *, sendMessageFunction, writer, ui, allKeys: dict, allowExec: bool = False) -> None:
        """
        Initialize the executer
        
        Parameters:
            - sendMessageFunction (function): The function to send a message
            - writer (asyncio.StreamWriter): The writer
            - ui (evdev.InputDevice): The input device
            - allKeys (dict): A dictionary of all keys
            - allowExec (bool, optional): Whether to allow execution. Defaults to False.
        """
        self.writer = writer
        self.sendMessage = staticmethod(sendMessageFunction)
        self.scriptData = None
        self.ui = ui
        self.allKeys = allKeys
        self.allowExec = allowExec
        self.executionSpeed = None
        self.stopFlag = False

    async def actionWait(self, sleepTime: int) -> None:
        """
        Sleep for the specified amount of time
        
        Parameters:
            - sleepTime (int): The amount of time to sleep in milliseconds
        """
        sleepTime = await self.retrieveValue(sleepTime)
        await asyncio.sleep(sleepTime / 1000)

    async def actionPressKey(self, key: str) -> None:
        """
        Press the specified key
        
        Parameters:
            - key (str): The key to press
        """
        key = await self.retrieveValue(key)

        self.ui.write(e.EV_KEY, self.allKeys.get(key), 1)
        self.ui.syn()

    async def actionReleaseKey(self, key: str) -> None:
        """
        Release the specified key
        
        Parameters:
            - key (str): The key to release
        """
        key = await self.retrieveValue(key)

        self.ui.write(e.EV_KEY, self.allKeys.get(key), 1)
        self.ui.write(e.EV_KEY, self.allKeys.get(key), 0)
        self.ui.syn()

    async def actionTapKey(self, key: str, modifier: str = None) -> None:
        """
        Tap the specified key
        
        Parameters:
            - key (str): The key to tap
            - modifier (str, optional): The modifier to use. Defaults to None.
        """
        key = await self.retrieveValue(key)
        modifier = await self.retrieveValue(modifier)

        if modifier == 'SHIFT':
            self.ui.write(e.EV_KEY, e.KEY_LEFTSHIFT, 1)
        self.ui.write(e.EV_KEY, self.allKeys.get(key), 1)
        self.ui.write(e.EV_KEY, self.allKeys.get(key), 0)
        if modifier == 'SHIFT':
            self.ui.write(e.EV_KEY, e.KEY_LEFTSHIFT, 0)
        self.ui.syn()
    
    async def actionMoveAbsolute(self, x: int, y: int) -> None:
        """
        Move the mouse to the specified coordinates
        
        Parameters:
            - x (int): The x coordinate
            - y (int): The y coordinate
        """
        x = await self.retrieveValue(x)
        y = await self.retrieveValue(y)

        self.ui.write(e.EV_ABS, e.ABS_X, x)
        self.ui.write(e.EV_ABS, e.ABS_Y, y)
        self.ui.syn()

    async def actionMoveRelative(self, x: int, y: int) -> None:
        """
        Move the mouse relative to the current position
        
        Parameters:
            - x (int): The x coordinate
            - y (int): The y coordinate
        """
        x = await self.retrieveValue(x)
        y = await self.retrieveValue(y)

        self.ui.write(e.EV_REL, e.REL_X, x)
        self.ui.write(e.EV_REL, e.REL_Y, y)
        self.ui.syn()
    
    async def actionExec(self, command: list, blocking: bool = False) -> None:
        """
        Execute the specified command
        
        Parameters:
            - command (list): The command to execute
            - blocking (bool, optional): Whether to block the thread. Defaults to False.
        """
        command = await self.retrieveValue(command)
        blocking = await self.retrieveValue(blocking)

        if blocking:
            subprocess.call(command)
        else:
            subprocess.Popen(command)

    async def actionModifyVariable(self, variable: str, operation: str, value) -> None:
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
            self.variableData[variable] = await self.retrieveValue(value)
        elif operation == 'add':
            self.variableData[variable] += await self.retrieveValue(value)
        elif operation == 'subtract':
            self.variableData[variable] -= await self.retrieveValue(value)
        elif operation == 'multiply':
            self.variableData[variable] *= await self.retrieveValue(value)
        elif operation == 'divide':
            self.variableData[variable] /= await self.retrieveValue(value)

        await self.sendMessage(f'Variable Modified: {variable} {operation} {value} -> {self.variableData[variable]}', True, writer=self.writer)

    async def execute(self, scriptData: dict) -> None:
        """
        Execute the script
        
        Parameters:
            - scriptData (dict): The script data
        """
        # Load the script
        self.scriptData = scriptData
        if not self.scriptData:
            await self.sendMessage(f'Error: No script data', writer=self.writer)
            return
        self.executionSpeed = self.scriptData['speed']
        if 'variables' in self.scriptData:
            self.variableData = self.scriptData['variables']

        # Execute the script
        for step in self.scriptData['steps']:
            await self.sendMessage(step, True, writer=self.writer)
            
            await self.executeIteration(step)

        await asyncio.sleep(0.1) # Let the device process the events

    async def executeIteration(self, step: dict) -> None:
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
            await self.actionWait(step['value'])
        elif step['type'] == 'press':
            await self.actionPressKey(step['value'])
        elif step['type'] == 'release':
            await self.actionReleaseKey(step['value'])
        elif step['type'] == 'tap':
            await self.actionTapKey(step['value'], step.get('modifier', None))
        elif step['type'] == 'move-absolute':
            await self.actionMoveAbsolute(step['x'], step['y'])
        elif step['type'] == 'move-relative':
            await self.actionMoveRelative(step['x'], step['y'])
        elif step['type'] == 'exec':
            if self.allowExec:
                await self.actionExec(step['value'].split(), step.get('blocking', False))
        elif step['type'] == 'modify-variable':
            await self.actionModifyVariable(step['variable'], step['operation'], step['value'])
        elif step['type'] == 'loop':
            for _ in range(await self.retrieveValue(step['value'])):
                for subStep in step['subSteps']:    
                    await self.sendMessage(f'-> {subStep}', True, writer=self.writer)
                    await self.executeIteration(subStep)
        elif step['type'] == 'if':
            if await self.evaluateCondition(step['operation'], step['value1'], step.get('value2', None)):
                if 'trueSteps' not in step: # If there are no true steps, return
                    return
                for subStep in step['trueSteps']:    
                    await self.sendMessage(f'-> {subStep}', True, writer=self.writer)
                    await self.executeIteration(subStep)
            else:
                if 'falseSteps' not in step: # If there are no true steps, return
                    return
                for subStep in step['falseSteps']:    
                    await self.sendMessage(f'-> {subStep}', True, writer=self.writer)
                    await self.executeIteration(subStep)

        await asyncio.sleep(self.executionSpeed / 1000)

    async def evaluateCondition(self, operation: str, value1, value2 = None) -> bool:
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
        value1 = await self.retrieveValue(value1)
        if value2 is not None:
            value2 = await self.retrieveValue(value2)
            
        await self.sendMessage(f'Condition: {value1} ({type(value1)}) {operation} {value2} ({type(value2)})', True, writer=self.writer)

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

    async def retrieveValue(self, value):
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
            await self.sendMessage(f'Variable -> {value}: {self.variableData.get(value[1:])}', True, writer=self.writer)
            return self.variableData.get(value[1:])
        
        elif value.startswith('-$'): # Invert variable
            await self.sendMessage(f'Variable -> {value[1:]}: {-self.variableData.get(value[2:])}', True, writer=self.writer)
            return -self.variableData.get(value[2:])
        
        return value

    def stop(self) -> None:
        """
        Stops the execution of the script.
        """
        self.stopFlag = True
