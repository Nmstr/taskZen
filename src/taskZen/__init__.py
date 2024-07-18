from .actions import *
import initialize

ui = initialize.initialize()
allKeys = initialize.getAllKeys()
actions.setVariables(ui, allKeys)

__all__ = ['actions']
