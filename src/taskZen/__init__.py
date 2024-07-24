from . import _devices
from .actions import *

def registerDevice(deviceName: str) -> _devices.UInput:
    device = _devices.initialize(deviceName)
    allKeys = _devices.getAllKeys()
    actions.setVariables(device, allKeys)
