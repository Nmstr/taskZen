from . import _devices
from .actions import *

#ui = _devices.initialize()
#allKeys = _devices.getAllKeys()
#actions.setVariables(ui, allKeys)

def registerDevice(deviceName: str) -> _devices.UInput:
    ui = _devices.initialize(deviceName)
    allKeys = _devices.getAllKeys()
    actions.setVariables(ui, allKeys)
