from initialize import initialize, readScript
from executer import execute

# Initialize the input device and load data
scriptData = readScript('examples/exampleMouse.yaml')
allKeys, ui = initialize(scriptData)

execute(scriptData, ui, allKeys)
