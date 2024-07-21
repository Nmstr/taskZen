import asyncio
import json
import os

HEADER_LENGTH = 10
SOCKET_PATH = '/tmp/taskZen.sock'

async def sendMessage(message: str, *, writer: asyncio.StreamWriter) -> None:
    """
    Asynchronously sends a message to a writer.

    Args:
        message (str): The message to send.
        writer (asyncio.StreamWriter): The writer to send the message to.

    Returns:
        None
    """
    # Prepare header and message
    message = str(message)
    messageLength = len(message)
    header = f"{messageLength:<{HEADER_LENGTH}}".encode('utf-8')

    # Send header and message
    writer.write(header + message.encode('utf-8'))

    await writer.drain()

async def executeScript(scriptPath: str, writer: asyncio.StreamWriter) -> None:
    currentDir = os.path.dirname(os.path.realpath(__file__))
    if 'FLATPAK_ID' in os.environ:
        pythonExecutable = "/usr/bin/python"
    else:
        pythonExecutable = os.path.join(os.getenv('VIRTUAL_ENV', ''), 'bin/python')
    env = os.environ.copy()
    env['PYTHONPATH'] = currentDir + os.pathsep + env.get('PYTHONPATH', '')
    
    process = await asyncio.create_subprocess_exec(
        pythonExecutable, '-u', scriptPath,
        cwd=currentDir,
        env=env,
        stdout=asyncio.subprocess.PIPE,
    )

    async for line in process.stdout: # Process its output
        print(f'{scriptPath} - {process.pid}: {line.decode().strip()}')
        await sendMessage(line.decode().strip(), writer=writer)

    # Wait for the subprocess to exit
    await process.wait()

async def handleClient(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
    header = await reader.read(HEADER_LENGTH)
    messageLength = int(header.decode().strip())

    # Read data from the client
    data = await reader.read(messageLength)
    message = data.decode()
    message = json.loads(message)

    print(message)
    if message['instruction'] == 'ping':
        pass

    elif message['instruction'] == 'kill':
        await sendMessage('end', writer=writer)
        exit(0)

    elif message['instruction'] == 'killExecution':
        try:
            pass
            #runningExecutions[message['scriptName']]['executer'].stop()
        except KeyError:
            await sendMessage('Error: Execution not found', writer=writer)

    elif message['instruction'] == 'listRunning':
        #print(runningExecutions)
        #for execution in runningExecutions:
        #    print(execution)
        #    await sendMessage(f'{execution}', writer=writer)
        pass

    elif message['instruction'] == 'execute':
        await executeScript(scriptPath=message['path'], writer=writer)

    # Close the connection
    await sendMessage(f'end', writer=writer)
    writer.close()

async def main() -> None:
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
    print(f'Server started')

    async with server: # Serve until done
        await server.serve_forever()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Server stopped manually")
    finally:
        os.unlink(SOCKET_PATH)
