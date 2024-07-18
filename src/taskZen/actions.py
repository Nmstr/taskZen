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
    ui.write(e.EV_KEY, allKeys.get(key), 1)
    ui.syn()

def releaseKey(key: str) -> None:
    """
    Release the specified key
    
    Parameters:
        - key (str): The key to release
    """
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
    ui.write(e.EV_REL, e.REL_X, x)
    ui.write(e.EV_REL, e.REL_Y, y)
    ui.syn()
