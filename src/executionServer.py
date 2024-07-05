from initialize import initialize, readScript, findScript, getAllKeys
from executer import Executer
import datetime
import asyncio
import json
import os

HEADER_LENGTH = 10
SOCKET_PATH = '/tmp/taskZen.sock'

runningExecutions = {}
allDevices = {}
verbose = False

async def sendMessage(message, requireVerbose=False, *, writer):
    """
    Asynchronously sends a message to a writer.

    Args:
        message (str): The message to send.
        requireVerbose (bool, optional): Whether the message should be sent only if verbose is True. Defaults to False.
        writer (asyncio.StreamWriter): The writer to send the message to.

    Returns:
        None
    """
    message = str(message)

    if requireVerbose and verbose is False:
        print(f'Withheld message: {message}')
        return
    else:
        print(f'Send message: {message}')

    # Prepare header and message
    messageLength = len(message)
    header = f"{messageLength:<{HEADER_LENGTH}}".encode('utf-8')

    # Send header and message
    writer.write(header + message.encode('utf-8'))

    await writer.drain()

async def processInstruction(scriptName, *, writer, file = False, allowExec = False):
    """
    Processes an instruction to execute a script.
    Asumes that the script exists. This should have been verified by the client.

    Args:
        scriptName (str): The name of the script to execute.
        writer (asyncio.StreamWriter): The writer to send messages to.
        file (bool, optional): Whether to use script name or file path. Defaults to False.
        verbose (bool, optional): Whether to print verbose messages. Defaults to False.
        allowExec (bool, optional): Whether to allow execution of exec statements. Defaults to False.

    Returns:
        None
    """
    # Find the script
    if file == 'True':
        scriptPath = scriptName
    else:
        scriptPath = findScript(scriptName)

    scriptData = readScript(scriptPath)
    allKeys = getAllKeys()
    ui, error = await getDevice(scriptData, writer=writer)

    if not ui: # Failed to initialize
        await sendMessage(f'Failed to initialize device.', writer=writer)
        await sendMessage(f'Error: {error}', writer=writer)
        return
    await sendMessage(f'Device initialized.', writer=writer)

    executer = Executer(sendMessageFunction=sendMessage, writer=writer, ui=ui, allKeys=allKeys, allowExec=allowExec)
    runningExecutions[scriptName] = {'executer': executer, 'creationTime': datetime.datetime.now()}
    await executer.execute(scriptData)
    runningExecutions.pop(scriptName)
        
async def getDevice(scriptData, *, writer):
    """
    Retrieves a device from the `allDevices` dictionary based on the provided `scriptData['name']`.
    If the device is not found, it initializes the device using the `initialize` function and adds it to the `allDevices` dictionary.

    Parameters:
        scriptData (dict): The script data containing the device name.
        writer: The asyncio.StreamWriter to send messages to.

    Returns:
        Any: The device corresponding to the provided `scriptData['name']`.
    """
    error = None
    if allDevices.get(scriptData['name']) is None:
        await sendMessage(f'Device not found. Initializing...', writer=writer)
        ui, error = await initialize(scriptData)
        allDevices[scriptData['name']] = ui
    return allDevices[scriptData['name']], error

async def handleClient(reader, writer):
    """
    Asynchronously handles a client connection by reading its instructions and executing them.
    
    The supported instructions are:
    - 'ping': Sends a response indicating the end of the message.
    - 'kill': Sends a response indicating the end of the message and exits the program.
    - 'killExecution': Stops the execution of the specified script if it is currently running.
    - 'listRunning': Prints the list of currently running executions and sends each execution 
      as a response.
    - 'execute': Processes the instruction by executing the specified script with the given 
      parameters.
    
    Parameters:
        reader (asyncio.StreamReader): The reader object for reading data from the client.
        writer (asyncio.StreamWriter): The writer object for sending data to the client.
    
    Returns:
        None
    """
    header = await reader.read(HEADER_LENGTH)
    messageLength = int(header.decode().strip())
    
    # Read data from the client
    data = await reader.read(messageLength)
    message = data.decode()

    message = json.loads(message)

    print(message)
    if message['instruction'] == 'ping':
        await sendMessage('end', writer=writer)

    elif message['instruction'] == 'kill':
        await sendMessage('end', writer=writer)
        exit(0)

    elif message['instruction'] == 'killExecution':
        try:
            runningExecutions[message['scriptName']]['executer'].stop()
        except KeyError:
            await sendMessage('Error: Execution not found', writer=writer)

    elif message['instruction'] == 'listRunning':
        print(runningExecutions)
        for execution in runningExecutions:
            print(execution)
            await sendMessage(f'{execution}', writer=writer)

    elif message['instruction'] == 'execute':
        global verbose
        verbose = message['verbose']

        await processInstruction(message['scriptName'], writer=writer, file=message['file'], allowExec=message['allowExec'])

    # Close the connection
    await sendMessage(f'end', writer=writer)
    writer.close()

async def main():
    """
    Asynchronously creates a Unix socket and starts serving it until done.

    Parameters:
        None

    Returns:
        None
    """
    # Create the Unix socket
    try:
        os.unlink(SOCKET_PATH)
    except OSError:
        if os.path.exists(SOCKET_PATH):
            raise
    server = await asyncio.start_unix_server(handleClient, SOCKET_PATH)

    async with server: # Serve until done
        await server.serve_forever()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Server stopped manually")
    finally:
        os.unlink(SOCKET_PATH)
