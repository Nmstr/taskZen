from initialize import initialize, readScript, findScript, getAllKeys
from executer import Executer
import asyncio
import json
import os

HEADER_LENGTH = 10
SOCKET_PATH = '/tmp/taskZen.sock'
verbose = False

async def sendMessage(message, requireVerbose=False, *, writer):
    message = str(message)

    if requireVerbose and verbose == 'False':
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

async def processInstruction(scriptName, *, writer, file = False, verbose = False, allowExec = False):
    # Find the script
    if file == 'True':
        scriptPath = scriptName
    else:
        scriptPath = findScript(scriptName)
    if scriptPath is None or not os.path.exists(scriptPath):
        await sendMessage(f'Script {scriptName} not found.', writer=writer)
        exit(1)

    print('a')

    scriptData = readScript(scriptPath)
    allKeys = getAllKeys()
    ui = await getDevice(scriptData, writer=writer)

    executer = Executer(sendMessageFunction=sendMessage, writer=writer, ui=ui, allKeys=allKeys, allowExec=allowExec)
    await executer.execute(scriptData)
        
async def getDevice(scriptData, *, writer):
    allDevices = {}                                                         # TODO: Make allDevices work (device caching)
    if allDevices.get(scriptData['name']) is None:
        await sendMessage(f'Device not found. Initializing...', writer=writer)
        ui = initialize(scriptData)
        allDevices[scriptData['name']] = ui
        await sendMessage(f'Device initialized.', writer=writer)
    return allDevices[scriptData['name']]





async def handleClient(reader, writer):
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

    elif message['instruction'] == 'killExecution':
        pass

    elif message['instruction'] == 'listRunning':
        pass

    elif message['instruction'] == 'execute':
        print('--')
        #await asyncio.sleep(5)
        await processInstruction(message['scriptName'], writer=writer, file=message['file'], verbose=message['verbose'], allowExec=message['allowExec'])
        print('execute')

    else:
        pass

    # Close the connection
    await sendMessage(f'end', writer=writer)
    writer.close()

async def main():
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