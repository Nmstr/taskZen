import asyncio
import os

HEADER_LENGTH = 10
socket_path = '/tmp/taskZen.sock'

async def handleClient(reader, writer):
    # Read data from the client
    data = await reader.read(100)
    message = data.decode()
    print(f"Received: {message}")

    # Prepare header and message
    messageLength = len(message)
    header = f"{messageLength:<{HEADER_LENGTH}}".encode('utf-8')

    # Send header and message
    writer.write(header + message.encode('utf-8'))
    await writer.drain()

    # Close the connection
    writer.close()

async def main():
    # Create the Unix socket
    try:
        os.unlink(socket_path)
    except OSError:
        if os.path.exists(socket_path):
            raise
    server = await asyncio.start_unix_server(handleClient, socket_path)

    async with server: # Serve until done
        await server.serve_forever()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Server stopped manually")
    finally:
        os.unlink(socket_path)
